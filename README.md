# ma-skills

A personal library of reusable agent skills for the owner's workflows. Skills can support software projects, personal writing, research, and other repeatable work. Each lives in its own folder with instructions and any supporting files it needs.

## Skill catalog

| Skill | Purpose |
| --- | --- |
| [evidence-led-partner](skills/evidence-led-partner/SKILL.md) | Install a persistent evidence-led thinking partner policy into a project and run structured critiques for consequential decisions. |
| [install-this-skill](skills/install-this-skill/SKILL.md) | Stage, security-scan, evaluate, install, and explain external agent skills before adding them to your skills directory. |
| [project-git-identity](skills/project-git-identity/SKILL.md) | Set up and maintain the owner's project-specific Git identity and publishing policy. |

## New project starter run

When opening a new project (software, writing, research, or general work), run the starter skills you want persisted in that project's `AGENTS.md` (and any tool-specific instruction file such as `GEMINI.md` or `CLAUDE.md`):

1. **`project-git-identity`** — if the project uses Git/GitHub, establish the persistent PRIMARY/SECONDARY account and attribution policy.
2. **`evidence-led-partner`** — install the compact evidence-led thinking partner policy into `AGENTS.md` so it stays active across every session.
3. **Additional workflow skills** — add any task-specific skills (or vet external ones first with `install-this-skill`).

Each starter skill preserves existing instructions and keeps project-specific choices inside the target project.

## Getting started

1. Browse the catalog and choose a skill for the task or project.
2. Copy the whole `skills/<skill-name>/` directory—including any references, scripts, and assets—to the skill location supported by your agent. See [tool compatibility](docs/compatibility.md).
3. Start or reload the agent if needed, then invoke the skill by name or explicitly ask it to read the skill's `SKILL.md`. Confirm it can access the files in the environment where it runs.
4. Follow the skill's own setup instructions and authorization requirements. For project-specific skills, keep project choices and persistent rules in the target project.
5. Record the library commit or release used if you want a reproducible snapshot. Update installed copies deliberately; changing this library does not automatically update them.

A skill provides instructions for a workflow; it does not itself grant permission to publish, send messages, access private services, or perform other external actions. Individual tools may use different invocation syntax or instruction files.

## Repository layout

```text
ma-skills/
├── AGENTS.md                   # Instructions for working on this library
├── README.md                   # Catalog and getting started
├── docs/compatibility.md       # Tool discovery and portability notes
├── project-identity-policy.md  # Git identity policy for this library
└── skills/
    └── <skill-name>/
        ├── SKILL.md            # Skill entry point
        ├── references/         # Optional supporting guidance
        ├── scripts/            # Optional helpers
        └── assets/             # Optional templates or other resources
```

## Adding or updating a skill

Give each skill a clear name and a `SKILL.md` describing what it does and when to use it. Include only supporting files the workflow needs, document any tool or service dependencies, and update the catalog. Test the changed skill and its relevant references or scripts before distributing it.

Skills can include private-workflow instructions, such as how to use a diary service, but actual diary entries, credentials, tokens, and other secrets do not belong in this public repository.

For agents working on this library, see [AGENTS.md](AGENTS.md). Its Git identity policy applies to this repository; individual projects keep their own policy and account selection.
