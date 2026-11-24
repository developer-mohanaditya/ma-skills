#!/usr/bin/env python3
"""Static security scanner for candidate agent skills.

Performs zero-execution static analysis on a staged skill directory:
- File inventory, size, binary, hidden file, and symlink escape checks
- Invisible / bidirectional Unicode spoofing checks
- Prompt-injection, credential-access, exfiltration, and unsafe-execution pattern checks
- SKILL.md YAML frontmatter validation

Exit codes:
  0 = No findings (still requires manual review of SKILL.md and scripts)
  1 = Warnings / medium findings (review carefully)
  2 = High-severity findings detected
  3 = Usage or path error
"""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path
from typing import NamedTuple


class Finding(NamedTuple):
    severity: str  # HIGH, MEDIUM, INFO
    category: str
    path: str
    line: int | None
    detail: str


SCRIPT_EXTS = {
    ".sh", ".bash", ".zsh", ".fish", ".ps1", ".bat", ".cmd",
    ".py", ".js", ".mjs", ".cjs", ".ts", ".mts", ".rb", ".pl", ".php", ".lua",
}
DOC_EXTS = {".md", ".markdown", ".txt", ".rst"}

# Invisible / bidi control characters commonly used for Trojan Source / hidden prompts
SUSPICIOUS_UNICODE = {
    "\u200b": "ZERO WIDTH SPACE",
    "\u200c": "ZERO WIDTH NON-JOINER",
    "\u200d": "ZERO WIDTH JOINER",
    "\u2060": "WORD JOINER",
    "\ufeff": "BOM / ZERO WIDTH NO-BREAK SPACE (mid-file)",
    "\u202a": "LEFT-TO-RIGHT EMBEDDING",
    "\u202b": "RIGHT-TO-LEFT EMBEDDING",
    "\u202c": "POP DIRECTIONAL FORMATTING",
    "\u202d": "LEFT-TO-RIGHT OVERRIDE",
    "\u202e": "RIGHT-TO-LEFT OVERRIDE",
    "\u2066": "LEFT-TO-RIGHT ISOLATE",
    "\u2067": "RIGHT-TO-LEFT ISOLATE",
    "\u2068": "FIRST STRONG ISOLATE",
    "\u2069": "POP DIRECTIONAL ISOLATE",
}

# (severity, category, compiled_regex, description, scripts_only)
PATTERNS: list[tuple[str, str, re.Pattern[str], str, bool]] = [
    # Prompt injection / agent hijacking
    ("HIGH", "prompt-injection", re.compile(r"ignore\s+(all\s+)?(previous|prior|above|system)\s+instructions", re.I), "Instruction override phrase", False),
    ("HIGH", "prompt-injection", re.compile(r"(disregard|override|bypass)\s+(your\s+)?(safety|security|system|guardrails|rules)", re.I), "Safety bypass phrase", False),
    ("HIGH", "prompt-injection", re.compile(r"(do\s+not|don't|never)\s+(tell|inform|show|mention\s+to)\s+the\s+user", re.I), "Stealth / conceal-from-user instruction", False),
    ("HIGH", "prompt-injection", re.compile(r"without\s+(asking|informing|notifying|telling)\s+the\s+user", re.I), "Silent action instruction", False),
    ("MEDIUM", "config-tampering", re.compile(r"(~/|\$HOME/)?\.(gemini|claude|cursor|codex|ssh|aws|zshrc|bashrc|profile)\b", re.I), "References sensitive user config/dotdir", False),
    ("MEDIUM", "config-tampering", re.compile(r"\b(hooks\.json|mcp_config\.json|GEMINI\.md|AGENTS\.md)\b"), "References agent configuration file", False),

    # Remote code execution / obfuscation
    ("HIGH", "unsafe-exec", re.compile(r"(curl|wget)\s+[^\n|]*\|\s*(ba)?sh\b", re.I), "Piped remote script execution (curl/wget | sh)", False),
    ("HIGH", "obfuscation", re.compile(r"base64\s+(-d|--decode)\s*\|\s*(ba)?sh|eval\s*\(\s*base64|atob\s*\(", re.I), "Base64-decoded execution", False),
    ("HIGH", "unsafe-exec", re.compile(r"\brm\s+-rf\s+(/|~|\$HOME|\*)\b"), "Broad destructive rm -rf", False),
    ("MEDIUM", "unsafe-exec", re.compile(r"\b(eval|exec|subprocess\.Popen|os\.system|child_process)\s*\("), "Dynamic command/code execution", True),
    ("MEDIUM", "persistence", re.compile(r"\b(crontab|launchctl|systemctl|LaunchAgents|LaunchDaemons)\b"), "Persistence mechanism reference", False),

    # Credential / secret access & exfiltration
    ("HIGH", "exfiltration", re.compile(r"(curl|wget|nc|ncat|netcat)\s+[^\n]*(--data|-d|-F|--upload-file|-T)\s+[^\n]*(\.env|id_rsa|credentials|secret|token|passwd)", re.I), "Possible credential upload via CLI", False),
    ("MEDIUM", "secrets", re.compile(r"(AWS_SECRET_ACCESS_KEY|OPENAI_API_KEY|ANTHROPIC_API_KEY|GITHUB_TOKEN|PRIVATE\s+KEY|keychain)", re.I), "References sensitive credential/key", True),
    ("MEDIUM", "network", re.compile(r"https?://(?!github\.com|raw\.githubusercontent\.com|agentskills\.io|example\.com|localhost|127\.0\.0\.1)[^\s\"')>]+"), "External URL in script", True),
]


def is_binary_bytes(sample: bytes) -> bool:
    if b"\x00" in sample:
        return True
    try:
        sample.decode("utf-8")
        return False
    except UnicodeDecodeError:
        return True


def check_frontmatter(skill_md: Path, findings: list[Finding]) -> None:
    try:
        text = skill_md.read_text(encoding="utf-8")
    except Exception as exc:
        findings.append(Finding("HIGH", "frontmatter", str(skill_md), 1, f"Cannot read SKILL.md: {exc}"))
        return

    if not text.startswith("---\n") and not text.startswith("---\r\n"):
        findings.append(Finding("MEDIUM", "frontmatter", "SKILL.md", 1, "Missing YAML frontmatter block"))
        return

    end = text.find("\n---", 3)
    if end == -1:
        findings.append(Finding("MEDIUM", "frontmatter", "SKILL.md", 1, "Unterminated YAML frontmatter"))
        return

    fm = text[4:end]
    name_m = re.search(r"^name:\s*(.+)$", fm, re.M)
    desc_m = re.search(r"^description:\s*(.+)$", fm, re.M)
    if not name_m:
        findings.append(Finding("MEDIUM", "frontmatter", "SKILL.md", 1, "Missing required 'name' field"))
    else:
        raw_name = name_m.group(1).strip().strip("\"'")
        if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", raw_name):
            findings.append(Finding("INFO", "frontmatter", "SKILL.md", 1, f"Non-standard skill name '{raw_name}' (recommended: lowercase letters, digits, hyphens)"))
    if not desc_m:
        findings.append(Finding("MEDIUM", "frontmatter", "SKILL.md", 1, "Missing required 'description' field"))


def scan_directory(root: Path) -> tuple[list[Finding], dict[str, int]]:
    findings: list[Finding] = []
    stats = {"files": 0, "markdown": 0, "scripts": 0, "binaries": 0, "symlinks": 0, "hidden": 0}
    resolved_root = root.resolve()

    skill_md = root / "SKILL.md"
    if not skill_md.exists():
        findings.append(Finding("MEDIUM", "structure", "SKILL.md", None, "No SKILL.md at root of scanned directory"))
    else:
        check_frontmatter(skill_md, findings)

    for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
        # Skip .git directory
        if ".git" in dirnames:
            dirnames.remove(".git")

        for name in filenames + dirnames:
            full = Path(dirpath) / name
            rel = str(full.relative_to(root))

            if full.is_symlink():
                stats["symlinks"] += 1
                try:
                    target = full.resolve()
                    target.relative_to(resolved_root)
                    findings.append(Finding("INFO", "symlink", rel, None, f"Internal symlink -> {target}"))
                except ValueError:
                    findings.append(Finding("HIGH", "symlink", rel, None, f"Symlink escapes skill directory -> {os.readlink(full)}"))
                continue

            if full.is_dir():
                if name.startswith("."):
                    stats["hidden"] += 1
                    findings.append(Finding("INFO", "hidden", rel, None, "Hidden directory"))
                continue

            stats["files"] += 1
            if name.startswith("."):
                stats["hidden"] += 1
                findings.append(Finding("INFO", "hidden", rel, None, "Hidden file"))

            ext = full.suffix.lower()
            is_script = ext in SCRIPT_EXTS or (os.access(full, os.X_OK) and ext not in DOC_EXTS)
            if ext in DOC_EXTS:
                stats["markdown"] += 1
            if is_script:
                stats["scripts"] += 1

            try:
                raw = full.read_bytes()
            except Exception as exc:
                findings.append(Finding("MEDIUM", "io", rel, None, f"Unreadable file: {exc}"))
                continue

            if len(raw) > 512_000:
                findings.append(Finding("MEDIUM", "size", rel, None, f"Large file ({len(raw)} bytes)"))

            if is_binary_bytes(raw[:4096]):
                stats["binaries"] += 1
                findings.append(Finding("HIGH" if is_script else "MEDIUM", "binary", rel, None, f"Binary / non-UTF8 file ({len(raw)} bytes)"))
                continue

            text = raw.decode("utf-8", errors="replace")
            lines = text.splitlines()

            for lineno, line in enumerate(lines, start=1):
                # Check suspicious unicode (allow BOM only at file start)
                for ch, label in SUSPICIOUS_UNICODE.items():
                    if ch in line:
                        if ch == "\ufeff" and lineno == 1 and line.startswith("\ufeff") and line.count("\ufeff") == 1:
                            continue
                        findings.append(Finding("HIGH", "unicode", rel, lineno, f"Hidden/bidi character: {label} (U+{ord(ch):04X})"))

                # Check very long single lines (possible minified/obfuscated payload)
                if len(line) > 2000:
                    findings.append(Finding("MEDIUM", "obfuscation", rel, lineno, f"Very long line ({len(line)} chars) — possible minified/obfuscated blob"))

                # Regex pattern checks
                for sev, cat, regex, desc, scripts_only in PATTERNS:
                    if scripts_only and not is_script:
                        continue
                    if regex.search(line):
                        findings.append(Finding(sev, cat, rel, lineno, f"{desc}: {line.strip()[:120]}"))

    return findings, stats


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python3 scan_skill.py <skill_directory>", file=sys.stderr)
        return 3

    target = Path(sys.argv[1])
    if not target.is_dir():
        print(f"Error: '{target}' is not a directory", file=sys.stderr)
        return 3

    findings, stats = scan_directory(target)

    print(f"=== Skill Static Security Scan: {target} ===")
    print(
        f"Files: {stats['files']} | Docs: {stats['markdown']} | Scripts: {stats['scripts']} "
        f"| Binaries: {stats['binaries']} | Symlinks: {stats['symlinks']} | Hidden: {stats['hidden']}"
    )

    highs = [f for f in findings if f.severity == "HIGH"]
    meds = [f for f in findings if f.severity == "MEDIUM"]
    infos = [f for f in findings if f.severity == "INFO"]

    print(f"Findings: HIGH={len(highs)} MEDIUM={len(meds)} INFO={len(infos)}")
    for f in highs + meds + infos:
        loc = f"{f.path}:{f.line}" if f.line is not None else f.path
        print(f"[{f.severity}] ({f.category}) {loc} — {f.detail}")

    if highs:
        return 2
    if meds:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
