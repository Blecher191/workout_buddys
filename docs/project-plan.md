# Initial project plan

## Product

Users log their own workout sessions and view progress summaries shared with an explicitly approved buddy.
This is a summary dashboard, not a social feed.

## MVP scope

- Authentication.
- Create, read, edit, and delete owned workout sessions and exercise entries.
- Personal progress summaries.
- Approved buddy summaries without exposing private notes or raw records.

Defer social feeds, wearable integrations, notifications, AI coaching, and advanced infrastructure.

## First implementation tasks

### 1. Backend foundation

Create a minimal Python/FastAPI service with reproducible dependencies, placeholder environment examples, a health endpoint, setup instructions, and relevant CI.

Acceptance: a fresh checkout can follow documented steps to start the service and pass its checks. No credentials are committed.

### 2. Data and access rules

Design versioned migrations for sessions, entries, and approved buddy relationships.
Implement authentication and ownership policies alongside database-backed routes.

Acceptance: owners can manage their data; unrelated users cannot access it; buddy summaries do not grant raw-record access. Test with an owner, approved buddy, and unrelated user.

### 3. Authenticated workout workflow

Implement session and entry operations, validation, pagination, and summary calculations.
Define units and date-range behavior explicitly.

Acceptance: a complete authenticated create/read/update/delete flow works; summaries count sessions rather than exercise rows; unauthorized operations fail.

## Decisions for implementation

- Confirm dependency tooling and supported runtime versions.
- Specify summary fields, units, and timezone behavior.
- Define how an approved buddy relationship is established and revoked.
- Choose a narrow authorization design for aggregate-only sharing.
- Revisit hosting before deployment; no AWS or other resources are provisioned by repository setup.
