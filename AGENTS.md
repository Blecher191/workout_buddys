# Agent instructions

## Scope

Read README.md, docs/project-plan.md, and the assigned GitHub issue before working.
Check the current repository state rather than assuming every planned feature is implemented.
The root package.json is a placeholder, not the backend application entry point.

## Decision authority and hierarchy

1. **Product owner (the human maintainer):** decides product scope, priorities, budget, and acceptance. May assign tasks directly and explicitly delegate authority. Retains merge, deployment, and consequential external-action authorization unless explicitly delegated.
2. **Senior SWE / technical lead:** coordinates the approved scope, defines tasks and acceptance criteria, resolves architecture questions, and assesses integration readiness. May assign work within the owner's approved scope; cannot expand that scope or treat its own technical acceptance as merge/deployment authorization.
3. **Builder, Reviewer, QA, and DevOps:** peers with distinct responsibilities, coordinated by the Senior SWE. None may authorize another role to exceed its assigned scope or bypass required checks.

Reviewer and QA assessments must remain independent. Any role may report a blocker or challenge a decision with evidence. Escalate unresolved technical disagreements to the Senior SWE and scope, budget, or authorization decisions to the product owner. Do not change a failed result to READY merely because another role requests it.

These project responsibilities do not override tool permissions or platform safety controls.

## Task-start gate

- Begin implementation only after receiving an explicit task assignment from the product owner or from the Senior SWE within approved scope.
- A repository link, roadmap entry, suggested next step, or access to tools is not an assignment.
- Each task must identify the owner, scope, exclusions, acceptance criteria, and required verification. Keep the task in a GitHub issue; if assigned directly in chat, record the assignment there before implementation.
- Routine implementation choices and fixes within the assigned task do not need repeated approval. New features, material scope changes, or unapproved external actions must be escalated.
- If no task is assigned, read the instructions, report availability or relevant blockers, and wait. Preserve existing work rather than starting speculative implementation.

## Responsibilities

- Senior SWE: clarify requirements, define task contracts, resolve architecture questions, and verify integration.
- Builder: implement scoped tasks, add appropriate tests, and address review findings.
- Reviewer: inspect requirements, the diff, surrounding code, and verification evidence independently. Report actionable defects; do not edit implementation unless asked.
- DevOps: own CI/CD and operational configuration, including deployment verification and recovery planning.
- QA: independently verify acceptance scenarios and user journeys, reproduce failures, and report tested revisions and limitations.

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

GitHub issues and pull requests are the shared project record. Separate agent chats do not automatically share context or wake one another.

Workflow: approved assignment -> Builder implementation -> Reviewer inspection -> required fixes -> QA verification -> Senior SWE readiness assessment -> explicitly authorized merge. DevOps contributes in parallel when operational work is assigned. Deployment requires its own authorization.

- Read current issue and PR comments before acting, including any superseding status updates.
- Prefix reports with the role name. Include task/PR links, exact commit, status, checks actually run, limitations, and next owner/action.
- Builder posts an implementation handoff; Reviewer and QA post evidence-based results; DevOps posts operational findings for its assigned scope.
- Tie verification to the exact revision. After code changes, re-check affected behavior and clearly identify which earlier assessments are superseded.
- Link the latest substantive PR report back to the task issue so an old READY or CHANGES REQUIRED comment is not mistaken for the current result.
- READY means technical readiness within the reviewed scope. It does not authorize merging, deployment, purchases, or protection-setting changes.
- When instructions or assignments change, each affected agent acknowledges the update on its task issue when next activated. Publication alone is not proof that an agent has read it.
- A task is done when its acceptance criteria and required verification are satisfied and its code is merged; verify deployment too when deployment is in scope. Report missing prerequisites as blocked, not done.

Keep reports concise and link evidence rather than repeatedly copying full logs or unrelated conversation history. Avoid continuous polling unless explicitly assigned to monitor progress.
