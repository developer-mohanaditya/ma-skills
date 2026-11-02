---
name: project-git-identity
description: Set up and maintain the owner's project-specific Git identity and GitHub publishing policy. Use when the user invokes this skill to initialize a project, select or change its primary account, or apply the policy to Git and GitHub work.
---

# Project Git identity

Implement the owner's policy in [references/identity-policy.md](references/identity-policy.md). Read it before project initialization and before any commit or publishing operation covered by this skill. Higher-priority instructions and mandatory requirements prevail; stop an affected operation if they prevent compliance.

## Initialize a project

1. Identify the intended project root. Inspect existing project instructions and identity records without disturbing unrelated content. If the project is unclear, ask; do not initialize an arbitrary directory.
2. Find a confirmed project-specific PRIMARY selection. Never infer it from Git configuration, credentials, repository ownership or history. If absent, ask exactly the account-selection question in section 3 of the policy and wait for an explicit answer before committing or publishing. Development and read-only investigation may continue. Do not ask again if a valid selection exists.
3. Once selected, persist the complete policy and the PRIMARY/SECONDARY identity record in the project, preferably in a dedicated root policy document referenced by root `AGENTS.md`. Preserve unrelated instructions. Include the confirmed destination URL and remote only if known; otherwise record `NOT CONFIGURED`. Do not store credentials. For each tool in use, use its documented project instruction mechanism as appropriate. Do not claim another platform reads `AGENTS.md` without verification. Invoking setup authorizes these project-local instruction files; it does not authorize a commit or publication.
4. Where the project is a Git repository, set the PRIMARY baseline using repository-local `user.name`, `user.email`, and `user.useConfigOnly`, as described in the policy. First inspect configuration scope and worktree sharing; avoid a shared configuration change that would affect a concurrent task. Do not touch global identity or credentials. If not yet a repository, leave configuration pending rather than initializing Git unless requested.
5. Verify effective settings and relevant overrides, without displaying secret values. Report the chosen account, policy location, destination status, configuration scope, and any remaining setup. No push, PR, merge, or release is implied by setup.

## Continue work

Read the project policy and recorded selection at the start of each applicable session and before commits or publishing. Follow its detailed checks, authorization boundaries, exception handling, attribution, GitHub authentication, outgoing history inspection, and reporting requirements. Communicate the policy and effective account to any authorized delegated agents and retain them in handoffs.

For an explicitly requested SECONDARY task, record its scope in task state, prefer operation-scoped overrides, verify actual commits, and restore and verify PRIMARY afterward. An exception does not authorize publishing or rewriting history. Stop the affected operation if identity, destination, exception scope, authentication, or mandatory attribution cannot be established as required. Never silently switch accounts or change global configuration to work around failure.

The project-local policy and supported instruction files are what make the rule available across sessions; invoking this skill alone does not ensure that other products or cloud environments load it. Check the active environment and document any limitation.
