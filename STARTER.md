# New Project Starter Runbook (`ma-skills`)

Use this runbook when the owner opens a new project and asks you to set it up using `https://github.com/developer-mohanaditya/ma-skills`.

> **Critical boundary:** Do **NOT** copy `ma-skills`'s own `AGENTS.md` or `ma-skills`'s own `project-identity-policy.md` into the target project. Those files govern the `ma-skills` repository itself. Always generate fresh, project-specific files for the target project by following the skills in `skills/`.

---

## How the Owner's Two-Thread Workflow Works

- **Thread 1 (This thread — Setup & Governance):** Used to initialize the project and, later, to add or modify project instructions and skills.
- **Thread 2+ (Work threads):** Fresh conversations where actual project work happens.
- **Persistence requirement:** Thread 2+ reads **files on disk**, not Thread 1's chat history. Every rule, policy, or instruction change agreed in Thread 1 MUST be written to the target project's instruction files (`AGENTS.md`, `GEMINI.md`, `CLAUDE.md`, linked policy files, or `.agents/skills/`).

---

## Step-by-Step Bootstrap Procedure

### Step 1: Fetch `ma-skills` in Isolation
Clone `ma-skills` into a temporary directory **outside** the target project (never inside the target project workspace):

```bash
TMP_MA_SKILLS=$(mktemp -d)
git -c core.hooksPath=/dev/null clone --depth 1 https://github.com/developer-mohanaditya/ma-skills.git "$TMP_MA_SKILLS"
```

### Step 2: Inspect the Target Project
Check the target project root for:
- Whether it is a Git repository (`.git/`) or will use Git/GitHub.
- Any existing `AGENTS.md`, `GEMINI.md`, `CLAUDE.md`, `.agents/`, or `project-identity-policy.md`.

Never overwrite or delete existing unrelated project instructions — always preserve and merge cleanly.

### Step 3: Ask the Owner to Confirm Project Choices (One Concise Turn)
Before writing project policies or configuring Git, ask the owner to confirm:

1. **Starter policies to install** (default: all applicable):
   - **`evidence-led-partner`** — Persistent evidence-led thinking partner policy in `AGENTS.md` (recommended for all projects: coding, writing, research, strategy).
   - **`project-git-identity`** — Project-specific Git/GitHub identity and no-AI-attribution policy (for Git projects). If included, ask the exact PRIMARY account selection question from `skills/project-git-identity/SKILL.md`:
     - `1. developer-mohanaditya — developer.mohanaditya@gmail.com`
     - `2. work-ma — workofma@gmail.com`
2. **Optional skills to copy into this project** (`.agents/skills/<name>/`) or globally (`~/.gemini/config/skills/<name>/`), e.g. `install-this-skill` or others from `ma-skills/skills/`.
3. **Agent tools used in this project** (default: Antigravity via `AGENTS.md`; add a lightweight pointer in `CLAUDE.md` / `GEMINI.md` if the owner also uses Claude Code or Gemini CLI).

Wait for the owner's answers before writing policy files or changing Git config.

### Step 4: Apply Selected Modules to the Target Project

1. **Create or update root `AGENTS.md`** in the target project (preserving any existing sections):
   - If **`evidence-led-partner`** is selected: follow `$TMP_MA_SKILLS/skills/evidence-led-partner/SKILL.md` (Mode 1) and add the compact policy snippet from `$TMP_MA_SKILLS/skills/evidence-led-partner/references/project-policy-snippet.md`.
   - If **`project-git-identity`** is selected: follow `$TMP_MA_SKILLS/skills/project-git-identity/SKILL.md` in full — write the target project's own `project-identity-policy.md` with the owner's chosen PRIMARY/SECONDARY accounts, set repo-local Git config (`user.name`, `user.email`, `user.useConfigOnly true`), and add a clear reference in root `AGENTS.md` requiring agents to read `project-identity-policy.md` before any commit or publishing action.
   - Add a brief **`## Project Rules & Maintenance`** note in `AGENTS.md` stating that persistent project rules live in `AGENTS.md` (and linked policy files) and must not be weakened or bypassed without explicit owner approval.
2. **Wire up cross-tool pointers (if needed):**
   - Antigravity auto-loads `AGENTS.md` and `GEMINI.md` at the repository root.
   - If Claude Code is used, create/update `CLAUDE.md` with a concise pointer: `Read and follow all instructions in AGENTS.md and its referenced policy files.`
3. **Install requested skills (if any):**
   - Copy each requested skill folder cleanly (`skills/<name>/`) into `.agents/skills/<name>/` (project-local) or the owner's global skills folder, excluding `.git`.

### Step 5: Clean Up & Verify
1. Remove the temporary clone: `rm -rf "$TMP_MA_SKILLS"`.
2. Verify every created/updated file in the target project:
   - No leftover placeholders (`<approved username>`, `<PRIMARY_NAME>`, etc.).
   - No accidental copies of `ma-skills`'s own `AGENTS.md` or `ma-skills` repo URL in the target project's identity record.
   - If Git is initialized, verify `git config --local --list` matches the chosen PRIMARY account.
3. Do **not** auto-commit or push unless the owner explicitly asks.
4. Report a concise **Setup Complete** summary listing:
   - Exact files created or updated
   - Active policies (PRIMARY Git account if configured, evidence-led partner active, installed skills)
   - Confirmation that the owner can now open **Thread 2** to start actual project work with all rules active automatically, and return to **Thread 1** anytime to update rules.

---

## Returning to Thread 1 Later to Modify Rules

When the owner returns to Thread 1 to add, edit, or remove instructions:
1. Update the persisted files on disk (`AGENTS.md`, `project-identity-policy.md`, `.agents/skills/`, etc.) rather than only acknowledging in chat.
2. Preserve unrelated policies unless explicitly asked to change them.
3. Confirm the exact file changes so the owner knows **new threads (Thread 2+)** will immediately pick them up.
