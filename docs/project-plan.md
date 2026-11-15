# Project plan

Approved direction as of 2026-11-15. The [schema and Sprint 1 design](superpowers/specs/2026-11-15-sprint-1-design.md) is the detailed requirements source; GitHub issues define active assignments.

## Product

Up to 100 invited account holders log personal workouts. Groups are optional; users can join multiple groups by invitation link or code. Membership never exposes private workout rows.

Plans support Push/Pull/Legs, Upper/Lower, Full Body, Body Part Split, and Freestyle. Ordered rotations handle missed days without requiring weekdays. Quick logging loads planned exercises; actual sessions and strength sets preserve history independently of plan changes. Rest reminders provide general guidance rather than claiming full recovery.

After completing a workout, users may select groups and preview a post. Date, split/day, muscles, and exercise names are included; sets/reps, weights, notes, start time, and duration require explicit selection. Manual highlights preserve achievements and are private unless shared. Personal history stays until deletion; the default 90-day feed view is a filter, not a deletion schedule.

## Delivery

- Sprint 0 complete: FastAPI foundation, CI, protection and coordination.
- Sprint 1 active kickoff: local database/CI tests, controlled registration and profiles, private schema, group membership/invitation backend, and independent authorization verification.
- Sprint 2 planned: usable account/group/workout screens, workout APIs, five plan starters, quick logging, rotations, history, and rest reminders.
- Sprint 3 planned: group feed, privacy controls, personal/group comparisons, and manual highlights.
- Sprint 4 reserved for release validation and friends-trial preparation; detailed scope unassigned.
- Sprint 5 planned: separately authorized deployment and recovery verification.

## Boundaries

Sprint 1 excludes workout UI, workout CRUD routes, group feed, highlight implementation, and deployment. Automatic PR detection, reactions, comments, routine copying, public discovery, wearables, AI coaching, and advanced infrastructure remain deferred.

The backend currently only provides health/configuration functionality. Preserve the hosted database; inspect before any separately authorized migration. No resource purchases or hosted changes are authorized by this plan.

## Workflow

Senior SWE defines assignments; DevOps prepares database testing first; Builder implements dependency-ready tasks; Reviewer and QA independently verify each PR. The product owner retains merge and deployment authorization. See [sprint tracking](sprints.md) and [agent instructions](../AGENTS.md).
