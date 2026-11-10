# Workout Buddys

A workout tracker for logging your own workouts and viewing an approved buddy's progress summaries.

## Current status

Repository setup only. There is no runnable application, database schema, deployment, or test suite yet.

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

1. Create the backend foundation, dependency setup, health endpoint, and relevant CI.
2. Add versioned database migrations, authentication, and ownership policies.
3. Implement an authenticated workout workflow and approved buddy summaries.
4. Add a frontend and prepare deployment.

See [docs/project-plan.md](docs/project-plan.md) for scope and acceptance criteria.
