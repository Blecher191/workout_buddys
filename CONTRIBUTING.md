# Contributing

## Workflow

- Keep `main` as the integration branch.
- Use a short-lived branch: `feat/`, `fix/`, `docs/`, or `chore/`.
- Keep each pull request focused on one outcome.
- Describe intended behavior, acceptance criteria, and verification.
- Resolve required review findings before merging.
- Never force-push shared branches or overwrite another contributor's work.

Branch protection is not configured by these files; this document describes the team's workflow.

## Verification

Run checks appropriate to the change and record the commands and results in the pull request.
For documentation-only changes, inspect links and run `git diff --check`.
The Python backend has tests and the `Backend` Actions workflow. From `backend/`, run `python -m pip check`, `ruff check .`, `ruff format --check .`, and `pytest -q -W error` in the configured environment (see backend/README.md).
CI runs on every pull request, including documentation-only changes, so the required `checks` status can always report. Do not replace the root placeholder npm test with a fake success.

## Credentials and dependencies

- Keep real credentials in local environment files or the deployment platform's secret store.
- Commit only placeholder values in example environment files.
- Do not print secrets in logs, issues, or pull requests.
- Commit dependency lockfiles when dependency tooling is introduced.
- Include versioned migrations for database changes.

## Coordination

One contributor owns a change. Use separate branches and worktrees for concurrent implementation.
Share the task scope, revision, changed files, test results, and known blockers at handoff.
Review the exact revision intended for integration.

See [docs/sprints.md](docs/sprints.md) for milestones, status labels, assignment gates, and completion criteria. Use the implementation-task issue template for new work.
