# AI Playbook

## When I Reach For AI First

- Drafting release docs from evidence I already collected.
- Generating checklists for CI, Docker, README, and security review.
- Asking for a second pass on a small diff when I can verify every suggestion.
- Turning rough course notes into concise evidence tables.

## When I Do Not Reach For AI First

- Before I understand the repo structure, tests, and assignment scope myself.
- When a change could expose secrets, personal data, or production logs.
- When AI suggests a new product feature instead of protecting the existing app.
- When I am trying to learn the core concept and need to reason through it manually first.

## My Non-Negotiables

- No secrets or real personal/customer data in prompts, commits, docs, or Docker images.
- No hidden failures: no skipped tests, `continue-on-error`, or `|| true` in final evidence.
- No app/frontend edits unless there is a small documented bug or security fix.
- I must be able to explain every final changed line.

## My Review Rules

- Read the relevant files before accepting AI output.
- Inspect the diff for scope creep, vague claims, and copied boilerplate.
- Run the exact command the README or CI claims will work.
- Grade AI review comments as useful, noise, or wrong, then record the decision.
- Downgrade or reject findings that are out of scope for the course project.

## What I Am Still Figuring Out

- How teams should record local Docker blockers when CI can verify the same container but the laptop cannot provide virtualization.
- How to balance concise docs with enough evidence for a teammate to maintain the project.
- When a security warning is worth fixing immediately versus documenting as course-scope risk.

## Decision Card

| Situation | My rule |
|---|---|
| New feature | Pause and check scope before coding. |
| Code review | Ask AI for findings, but grade each one with file evidence. |
| Debugging | Reproduce the issue locally before changing code. |
| Infrastructure | Prefer boring, explicit commands that fail loudly. |
| Never-paste | Keep secrets, tokens, `.env` values, personal data, and production logs out of AI and Git. |
| One rule | Evidence beats confidence. |
