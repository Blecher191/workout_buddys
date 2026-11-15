# Workout Buddys

A personal workout tracker for up to 100 registered users, with flexible workout rotations and optional private groups. Sharing is explicit; personal workout records stay private.

## Current status

The backend foundation exists in [backend/](backend/README.md): a FastAPI service with a health endpoint, pinned dependencies, tests, and CI. There is no database schema, authentication, workout functionality, frontend, or deployment yet.

The existing `package.json` is an initial npm placeholder. Its `npm test` command intentionally fails because no tests have been configured; it is not an application setup command.

## Proposed direction

- Backend: Python and FastAPI.
- Database and authentication: Supabase PostgreSQL and Auth.
- Frontend: React and TypeScript after the authenticated API works.
- Hosting: evaluate AWS Lightsail for hands-on AWS learning.

These are planning decisions, not installed dependencies or provisioned services. The repository's GitHub description may still refer to the earlier Node/Express and Render proposal.

## Start contributing

1. Clone this repository and create a short-lived branch from `main`.
2. Read [CONTRIBUTING.md](CONTRIBUTING.md) and [AGENTS.md](AGENTS.md).
3. Define the task and acceptance criteria before implementing it.
4. Open a pull request containing the change and verification evidence.

```sh
git clone https://github.com/Blecher191/workout_buddys.git
cd workout_buddys
git switch -c feat/short-description
```

Do not commit credentials. Local environment files and virtual environments are ignored.

## Next milestones

1. Sprint 0 complete: backend foundation, CI, branch protection, and agent handoffs.
2. Sprint 1: local database testing, controlled registration, profiles, private schema, groups/invitations.
3. Sprint 2: usable workout logging, five split options, rotations, and rest reminders.
4. Sprint 3: explicit group sharing, progress comparisons, and manually saved highlights.
5. Later: release validation and authorized deployment for a friends trial.

The owner approved the [schema and Sprint 1 design](docs/superpowers/specs/2026-11-15-sprint-1-design.md) on 2026-11-15. Approval records scope, not completed functionality.

See [project plan](docs/project-plan.md) and [sprint tracking](docs/sprints.md). Planned work is not an instruction for agents to start implementation; follow assigned GitHub issues.
