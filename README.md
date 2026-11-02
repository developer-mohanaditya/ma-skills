# ma-skills

A personal library of reusable agent skills for project work. Each skill is a self-contained directory with a `SKILL.md` and any supporting files it needs.

## Skills

| Skill | Purpose |
| --- | --- |
| [project-git-identity](skills/project-git-identity/SKILL.md) | Set up and maintain the owner's project-specific Git identity and publishing policy. |

## Use in a project

1. Choose the skills needed for the project and copy each complete skill directory into the skill location supported by your agent.
2. Open the project in the agent and invoke the skill by name or explicitly ask the agent to read its `SKILL.md`.
3. Follow the skill's setup instructions. For `project-git-identity`, select the project's primary account and persist the policy in the project before creating commits or publishing.
4. Keep a note of the library commit or release used by the project. Update installed copies deliberately when you want newer instructions.

Codex supports project skills in `.agents/skills/`; Claude Code supports `.claude/skills/`. See [compatibility](docs/compatibility.md). Tool support, discovery, and permissions vary; verify the skill is available in the actual local or cloud workspace.

Project instructions and identity selections belong to the project, not this library. Installing a skill does not itself authorize a commit, push, or other publishing action.

## Maintain a skill

Keep a skill focused and portable. Put detailed supporting information in its own `references/`, `scripts/`, or `assets/` directory when needed. Review changes and update project copies intentionally. Never commit credentials or secrets.
