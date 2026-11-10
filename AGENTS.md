# Agent instructions

## Scope

This repository is in its setup phase. Read README.md and docs/project-plan.md before working.
Do not treat proposed architecture or the placeholder package.json as a working application.

## Responsibilities

- Senior SWE: clarify requirements, define task contracts, resolve architecture questions, and verify integration.
- Builder: implement scoped tasks, add appropriate tests, and address review findings.
- Reviewer: inspect requirements, the diff, surrounding code, and verification evidence independently. Report actionable defects; do not edit implementation unless asked.
- DevOps: own CI/CD and operational configuration, including deployment verification and recovery planning.
- QA, when assigned: verify actual user journeys and reproduce failures.

These are role boundaries, not an instruction to launch additional agents. Delegate only when authorized.

## Working rules

- Preserve existing work and keep changes scoped.
- Inspect relevant files before editing.
- State material assumptions and ask only when ambiguity blocks safe, correct progress.
- Prefer simple implementations and current official documentation.
- Never expose credentials or use privileged access to bypass authorization requirements.
- Do not purchase services, deploy to production, change DNS, or destroy resources without explicit authorization.
- Do not merge a pull request unless requested.
- Verify results before claiming completion.
- Distinguish prepared configuration from applied infrastructure and verified deployments.

## Handoff

Report the branch or commit, changes made, checks actually run, remaining limitations, and the next owner/action.
Keep reports concise and avoid repeatedly copying full logs or unrelated conversation history.
