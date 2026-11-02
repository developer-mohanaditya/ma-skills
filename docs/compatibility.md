# Compatibility

Skills follow the [Agent Skills format](https://agentskills.io/specification): a skill is a directory containing `SKILL.md` and any supporting files. Common formatting does not guarantee identical discovery, tools, or behavior in every product.

| Tool | Project skill location | Evidence and limits |
| --- | --- | --- |
| Codex | `.agents/skills/<skill-name>/` | [OpenAI documentation](https://developers.openai.com/blog/skills-agents-sdk) describes repo-local skills and `AGENTS.md` project instructions. |
| Claude Code | `.claude/skills/<skill-name>/` | [Anthropic documentation](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview) describes project skills. |
| Freebuff | Verify for the active product and environment | [Public source](https://github.com/CodebuffAI/freebuff/blob/main/agents/base2/base-deep.ts) references `.agents/skills/`. Discovery in a specific Desktop or web session has not been verified here. |

Copy the entire skill directory, including references. Start or reload the tool if needed and confirm it can discover the installed skill. The skill file's format is portable, but project instructions, supported commands, permissions, and local versus hosted filesystem access differ. Check each tool's current documentation and actual behavior.

The identity policy is persistent project guidance. Put or reference it in the instruction mechanism each tool actually loads; an installed skill alone does not guarantee automatic enforcement. For a cloud environment, confirm the files exist and are read in that environment.
