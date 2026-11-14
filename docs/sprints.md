# Sprint tracking

GitHub milestones are the sprint record. GitHub issues define assignments; PRs contain the authoritative implementation-readiness reports. This is an issue-and-label workflow, not an automated GitHub Projects board or agent dispatcher.

## Milestones

| Milestone | Outcome | State at planning |
| --- | --- | --- |
| Sprint 0 - Foundation and workflow | Backend foundation, hierarchy, agent handoffs, reliable CI and branch protection | Close only after issue #7 acceptance checks pass |
| Sprint 1 - Identity and private data | Schema migrations, authentication, ownership rules | Backlog; implementation unassigned |
| Sprint 2 - Workout tracking | Log, view, edit and delete workouts through a usable flow | Proposed |
| Sprint 3 - Personal progress | History filters and accurate personal aggregates | Proposed |
| Sprint 4 - Buddy summaries | Explicit sharing and restricted aggregates | Proposed |
| Sprint 5 - Deployment | Verified hosted application and recovery procedure | Proposed |

Dates are deliberately unset. Later milestones describe direction, not authorization to implement their contents. The live milestone and issue states in GitHub supersede this planning snapshot.

## Task statuses

Use exactly one status label per task. Replace the old label when the status changes.

| Label | Meaning |
| --- | --- |
| status:backlog | Proposed; not assigned for implementation |
| status:ready | Explicitly assigned; scope and acceptance criteria recorded; prerequisites satisfied |
| status:in-progress | Assigned owner is working |
| status:review | Exact revision ready for independent review |
| status:qa | Review findings addressed; ready for assigned behavior verification |
| status:ready-to-merge | Required checks, review and QA evidence complete; merge authorization still required |
| status:blocked | Record the missing dependency and next action |
| status:done | Acceptance criteria met and applicable changes merged; close the issue |

Labels are manually maintained, not security controls. Agent roles are stated in the issue body because multiple agents currently use the same GitHub account. A label or comment does not activate an agent.

## Definition of done

- Acceptance criteria demonstrated with evidence for the exact revision.
- Required findings resolved; Reviewer and QA reports linked where applicable.
- CI passes and code/documentation changes are merged when applicable.
- Documentation and issue status reflect the result.
- Deployment verified only when deployment is in scope; otherwise no deployment is implied.

Read-only coordination issues can close when their reports have been accepted; they do not require a code PR.

## Sprint 0 record

- PR #1: repository foundation, merged.
- PR #5: backend foundation and test-isolation fix, merged; Reviewer and QA reports recorded on the PR; CI passed 17 tests at 157b74d.
- PR #6: hierarchy and assignment rules, merged. Builder, Reviewer, QA and DevOps acknowledged the update in issues #2-4 and PR #6.
- Issue #7: final CI hardening, tracking, and protection verification. Its final report records the actual required check and post-merge result.

Classic branch protection is the enforcement mechanism for main. Retain PR requirements, administrator enforcement, conversation resolution, and blocked force pushes/deletions. Zero formal approving reviews accommodates the shared owner account; independent role reports remain a process requirement, not a GitHub-enforced identity check.

The legacy ruleset named `Protect main` was disabled and had no branch target at inspection. Leave it disabled; it is not the active source of enforcement. Do not enable or delete it as an incidental task.

## Sprint 1 planning decisions

The owner agreed to individual strength sets: workout sessions contain exercise entries, and strength entries have child strength_sets rows for set number, reps, and weight. Cardio entries record duration and optional distance. Count sessions, not sets, for workout frequency.

Before database implementation, inspect the hosted schema for manual changes and preserve existing data. Propose versioned migrations, grants, RLS and ownership tests in a dedicated task. Confirm unit conventions, date handling, profile creation, and initial buddy scope in that task. This document does not authorize hosted schema changes or new feature work.
