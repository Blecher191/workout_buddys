# Workout Buddys: schema and Sprint 1 proposal

Status: APPROVED by the product owner on 2026-11-15. Sprint 1 kickoff authorized; individual GitHub assignments control execution.
Date: 2026-11-15
Prepared by: Senior SWE

## Read this first

Build a personal workout tracker for up to 100 registered users, with optional private groups. Users follow a flexible workout rotation, log their actual exercises, and choose whether to share each completed workout with selected groups.

This document captures the agreed product direction, proposes the database structure, and defines a bounded Sprint 1 backlog. Approval of the design is separate from assigning implementation, merging PRs, or changing the hosted database. No app, database, or hosting changes accompany this draft.

The earlier `docs/project-plan.md` describes a two-person, summary-only product. The approved design replaces that product direction. README, project plan, sprint tracking, and milestone descriptions are reconciled in S1-01. A roadmap entry alone is not an implementation assignment.

### Agreed requirements

- An account is required. Initially allow invited friends, with a maximum of 100 registered accounts across the app.
- Each user owns their workout history and can use the tracker without any group.
- Users can create and join multiple groups. Offer both invitation links and codes; no public group directory initially.
- Five plan types: Push/Pull/Legs, Upper/Lower, Full Body, Body Part Split, and Freestyle.
- Plans use ordered rotations, not mandatory weekdays. Completion advances the rotation; rest does not.
- Plan changes preserve historical workouts. Quick logging loads a planned day's exercises.
- Muscle-group rest reminders use completed exercises and elapsed time, with 48 hours as general guidance, never a guarantee of full recovery. They do not block logging.
- Sharing is manual after completing a workout: select groups, preview, select optional fields, then post. Users can unshare.
- Shared posts include workout date, split/day, muscle groups, and exercise names. Sets/reps/weights, notes, exact start time, and duration are optional and private by default.
- Compare recorded routines/activity without claiming to identify the most effective or efficient routine.
- Users manually save personal highlights, such as a dated bench-press milestone. No automatic PR detection in the initial feature.
- Reactions, automatic personal records, routine copying, comments, public discovery, and deployment are later work.

### Approved defaults

These architect recommendations were accepted when the owner approved the complete proposal on 2026-11-15.

1. Use email/password authentication with verified email. App-access invitations are separate from group invitations and bound to an email address.
2. Count all existing authentication accounts toward 100, including unverified accounts. Deleted accounts free a place; outstanding invitations do not reserve places. The first owner account counts too.
3. One owner per group, with other users as members. Only the owner creates/revokes group invitations, removes members, transfers ownership, or deletes the group. Ownership transfers only to an existing member.
4. Group invitations expire after seven days, support link and code redemption, and default to ten distinct redemptions. Owners can revoke them early. The code is a random 12-character human-readable value; the link uses a separate high-entropy secret for the same invitation.
5. A group member can see posts shared before they joined. Leaving/removal hides the departing member's posts from the group and removes that member's access. Rejoining does not automatically republish old posts.
6. A shared post is a selected snapshot. Editing the private workout does not silently change a post; updating it requires another preview/confirmation. Unsharing or deleting the original workout removes the post.
7. Offer kilograms/pounds and kilometers/miles preferences, initially kg/km with a clear choice during setup. Store canonical kg, meters, and seconds using decimal measurements. Bodyweight sets allow zero added weight.
8. Store timestamps in UTC and an IANA timezone on the profile. Preserve the workout's local date and timezone when recorded, so travel/profile changes do not move past workouts to another date.
9. Full Body starts with one day; users may add A/B days. Body Part defaults to Chest, Back, Shoulders, Legs, Arms, but days are editable. Freestyle uses the same ordered-day model without a prescribed template; users can also log an unplanned workout.
10. Optional start time/duration means users may omit recording them as well as omit sharing them. Keep a system completion timestamp for sequencing. Label rest estimates approximate when actual workout time is unknown; use the explicitly supplied occurrence date/time for backdated logs, never the date of data entry.
11. Retain personal workouts and highlights until the user deletes them or their account. The group feed initially shows the last 90 days, with older posts accessible; this is a display filter, not automatic deletion. This retention policy and manual highlights are approved.

## Approaches and tradeoffs

| Choice | Alternatives | Direction |
| --- | --- | --- |
| Scheduling | Fixed weekdays vs ordered rotation | Rotation was selected: missed days do not disrupt the sequence. |
| Joining a group | Code only, link only, or both | Both were recommended and accepted; one invitation backs both methods, so expiry/revocation/use limits remain consistent. |
| Sharing | Automatic group visibility vs explicit posts | Manual sharing was selected, with per-group choices and a preview. |
| Feed storage | Live access to workout rows vs selected snapshots | Propose selected snapshots: prevent private fields and later edits leaking into an existing post. Requires explicit post updates. |
| Delivery | Build all social/workout features in Sprint 1 vs foundation first | Propose foundation first; agree the wider schema now but ship it in verifiable increments. |

## Logical schema

This is a design, not executable SQL. UUID primary keys and server-controlled creation timestamps are the default. Required relations have foreign keys. Owned records cannot be reassigned by a client. Authentication accounts are managed by Supabase Auth; do not build a password table.

### Identity and admission

| Table | Main fields | Constraints/purpose |
| --- | --- | --- |
| `profiles` | `id` referencing auth user, `display_name`, `timezone`, `weight_unit`, `distance_unit`, timestamps | One profile per account. Display name trimmed, 1–50 characters. Private profile preferences; groups receive only a display-name projection. |
| `app_invitations` (private schema) | `id`, normalized target email, token digest, expiry, creator, redeemed user/time, revoked time | Single-account admission, distinct from group membership. No client listing or raw secret storage. |
| `registration_capacity` (private schema) | singleton id, `max_users=100` | Serialized admission coordination; the actual authentication account count is authoritative. Not editable by regular users. |

Admission must execute at an authoritative account-creation boundary, including direct authentication API requests. Serialize the capacity check and invitation consumption with account creation; two simultaneous claims on place 100 must yield only one account. No frontend-only count, public signup bypass, or privileged service-account bypass of the product limit. DevOps/Builder must verify the supported Auth mechanism locally against current documentation before committing to its implementation. If atomic enforcement cannot be demonstrated, stop the registration task rather than weaken the limit.

Profile initialization is idempotent. A failed/retried request must not duplicate profiles or consume another invitation. Authentication identities and foreign keys use UUIDs; the previously observed public `Users` table with bigint identity is not the account model. Inspect it again before implementation and preserve it unless removal is separately approved.

### Personal plans

| Table | Main fields | Constraints/purpose |
| --- | --- | --- |
| `workout_plans` | `id`, `user_id`, name, `split_type`, `is_active`, `next_day_id`, timestamps | At most one active plan per user; five allowed split types. Next day must belong to this plan. |
| `workout_plan_days` | `id`, `plan_id`, name, position | Unique position within a plan. Users may rename/reorder days. |
| `exercises` | `id`, optional owner id, name, `exercise_type`, archived flag | Small shared catalog plus private custom exercises; users cannot edit catalog or others' custom exercises. Type is strength or cardio. Archive referenced exercises rather than destroying history. |
| `muscle_groups` | stable id/key, display name | Shared reference list maintained with code/migrations. |
| `exercise_muscle_groups` | `exercise_id`, `muscle_group_id`, involvement (primary/secondary) | Unique exercise/muscle pair; both categories can be surfaced as overlap without pretending to measure fatigue. |
| `workout_plan_exercises` | `id`, `plan_day_id`, `exercise_id`, position, optional target sets/reps | Unique position per day; positive targets when present. These are intentions, not completed sets. |

A plan may use catalog exercises or its owner's custom exercises only. Rotation advancement is atomic and idempotent: completing the expected day advances once to its successor. Completing a repeat, unplanned workout, or different day leaves the pointer alone unless the user explicitly chooses to change the next day. Deleting/reordering days repairs the pointer within the same transaction. Plan history references are optional; historical snapshots survive plan deletion.

### Actual workouts

| Table | Main fields | Constraints/purpose |
| --- | --- | --- |
| `workout_sessions` | `id`, `user_id`, optional source plan/day, split/day name snapshot, occurrence date/timezone, optional actual start time/duration, status, completion timestamp, optional notes | Draft/completed states. Only completed sessions can be shared. System timestamps are distinct from optional actual workout timing. |
| `workout_entries` | `id`, `session_id`, optional exercise reference, exercise name/type snapshot, position, performance state (planned/performed/skipped), optional cardio duration/distance | Belongs to one owned session; ordered exercises preserve their historical names. Cardio duration positive when provided; distance nonnegative. |
| `workout_entry_muscles` | `entry_id`, muscle group, involvement | Snapshot of the muscles associated with the actual exercise; later catalog edits do not rewrite workout history/rest estimates. |
| `strength_sets` | `id`, `entry_id`, set number, reps, weight kg | Unique positive set number within an entry; positive reps, nonnegative weight; only valid on strength entries. |

Enforce ownership through the full parent chain, including insert/update parent changes. A user cannot attach a set to another user's entry, a workout to another user's plan, or a plan entry to another user's custom exercise. Validate same-owner references and child types, not just the root table. Count completed sessions for workout frequency, never exercise or set rows. Optional values remain null, not fabricated zeros.

Rest reminders are derived from performed exercises with recorded activity, not merely exercises preloaded into a draft. Completion must distinguish skipped/preloaded entries from actual work. Exact occurrence times permit an elapsed-hours estimate; date-only historical entries show the known date and uncertainty rather than an invented countdown. Do not persist an authoritative `fully_recovered` flag.

### Groups and sharing

| Table | Main fields | Constraints/purpose |
| --- | --- | --- |
| `groups` | `id`, name, `owner_id`, timestamps | Owner must be a member. Group creation and initial membership are one transaction. |
| `group_memberships` | `id`, `group_id`, `user_id`, joined time | Unique group/user. A fresh membership id on rejoin prevents old posts reappearing. Owner role derives from `groups.owner_id`, avoiding conflicting role sources. |
| `group_invitations` (private schema) | `id`, group, creator, link/code digests, expiry, max uses, revoked time | Both credentials resolve to one invitation. Users cannot list invitation secrets. Rate-limit redemption attempts and avoid revealing private group details before validation. |
| `group_invitation_redemptions` (private schema) | invitation, user, redeemed time | Unique invitation/user; atomic membership creation and usage accounting; retries do not spend another use. |
| `workout_shares` | `id`, `session_id`, `group_id`, author membership id, selected visibility flags, selected payload, publication/update timestamps | One post per workout/group. Payload has a validated, versioned allowlist; contains only approved fields. Creator must own the completed workout and currently belong to the group. |

A share payload contains the agreed required fields and only the selected optional fields. Sets/reps and working weights have separate flags, as do notes, actual start time, and duration. Never copy the entire private workout into a feed response then hide fields in the UI. The payload is built by trusted application/database logic from the owned workout; clients cannot spoof the author or substitute another person's session.

Unsharing deletes the accessible post. Deleting a workout deletes its posts; deleting a group deletes its memberships/invitations/posts, not personal workouts. Removing a membership removes its authored posts and revokes group read access immediately on subsequent requests. Previously viewed or copied information cannot be recalled. No push/email copies in the initial feed.

### Manually saved highlights (after basic workout logging)

The owner confirmed manual highlights. Proposed behavior: save a milestone from an owned completed workout, preview its exercise/date and selected weight/reps, add an optional note, and save privately. It is a user-declared achievement, not an automatically verified personal record. Saving a highlight does not publish it.

| Table | Main fields | Constraints/purpose |
| --- | --- | --- |
| `workout_highlights` | `id`, `user_id`, optional source session/entry, title, achievement date, exercise-name snapshot, optional weight kg/reps, optional note, timestamps | Independent owned record; source references must belong to its owner and agree on session. Snapshot survives source deletion when the user chooses to keep it. Weight nonnegative and reps positive when provided. |
| `highlight_shares` | `id`, `highlight_id`, group id, author membership id, selected payload, publication/update timestamps | One share per highlight/group; manual preview and explicit field selection. Same current-membership, author-only editing, unsharing, and removal rules as workout posts. |

Deleting the source workout presents an explicit choice: keep saved highlights or delete related highlights too. Keeping them clears source references and preserves their selected snapshots and existing explicit highlight shares; the confirmation must explain that those shares remain visible. Deleting a highlight also deletes its shares. Account deletion removes owned highlights and shares. Deleting a group or leaving it removes group highlight shares but preserves the personal highlights. Editing a source workout does not silently rewrite a highlight; updating a shared highlight requires a new preview/confirmation.

Highlights are displayed separately from the recent workout feed, without a 90-day cutoff. They never count as extra workouts, sets, training volume, or new muscle activity. Private highlights and optional notes must not leak through group membership. No unrestricted HTML, attachments, comments, or automatic record ranking in this first version.

Later feature acceptance tests must cover private-by-default saving, cross-user source rejection, per-group selected fields, keep/delete source-workout choices, share removal, account deletion, and absence of double-counting in progress/rest calculations. Document backup retention before launch; removal from active storage is not a promise of instantaneous removal from backups.

## Access rules

Use database row-level security and explicit grants on exposed tables, plus authenticated backend checks. Normal requests retain the user's identity; privileged credentials are limited to narrowly scoped administrative/admission operations and never sent to the client. Views/functions must not accidentally bypass row policies. Invitations and capacity records are not public CRUD resources.

| Actor | Own workouts/plans | Someone else's private workouts | Group posts | Group management |
| --- | --- | --- | --- | --- |
| Signed out | No | No | No | No |
| Signed-in user outside group | Own only | No | No | Can create own group |
| Current member | Own only | No | Read that group's selected posts; manage own posts | Leave; redeem valid invitations |
| Group owner | Own only | No | Same visibility as other members | Invite/remove, rename/delete group, transfer ownership |
| Former member | Own only | No | No access to former group | None |

Membership does not expose full profiles, email addresses, preferences, invitation records, or underlying workout rows. Use a minimal member display projection. Membership changes must be checked against current database state rather than stale token claims. Author-only controls on posts remain independent of group ownership; an owner can remove a member/delete a group but cannot edit that member's workout/post content.

Test policies through the actual user access path, not solely with service credentials or mocked authorization. Index ownership, membership lookups, ordered children, and group feed pagination. UUIDs alone are not an access-control mechanism.

## Sprint boundary

Sprint 1 outcome: a reproducible, tested identity and private-data foundation, including group membership/invitation operations. No claim that the usable app or friends trial is complete.

Sprint 1 includes identity/admission, authentication/profile backend, owned plan/workout migrations, muscle reference model, group membership/invitation migrations and backend, and negative authorization tests. Define the sharing contract here but implement share storage/policies with the feed in a later sprint, so unused feed interfaces do not become accidental APIs.

Sprint 2 proposed: usable workout flow, five plan starters, quick logging, rotation advancement, editing/history, rest reminders, and user-facing account/group management screens. Sprint 1 backend tests do not replace later UI verification.

Sprint 3 proposed: explicit group sharing/feed, privacy controls, manually saved highlights and their optional sharing, and descriptive personal/group comparisons. Highlight tables/routes/UI are implemented here after basic workout logging, not in Sprint 1. Reconcile existing milestone names after approval; do not silently rename the live milestones during drafting.

Friends trial follows a verified usable app, privacy checks, deployed environment, basic backup/recovery, and a short data-sharing notice. Deployment needs a separate task and authorization. No autoscaling, microservices, AI coaching, public discovery, or Pixel Office work is needed for this scope.

## Sprint 1 task contracts

These task contracts define approved scope, not blanket implementation permission. GitHub issues record active assignments and dependencies. Prepare implementation steps against the current repository for each task before coding. No sprint dates or effort estimates are promised yet.

### S1-01 — Approve and reconcile the design

- Owner: Senior SWE; product owner accepts scope/defaults.
- Scope: incorporate requested edits; reconcile README, project plan, sprint tracker/milestone descriptions; record decisions and the version approved.
- Excludes: product code, database changes, dispatching other agents before assignment.
- Acceptance: no conflicting active summary-only/two-person roadmap; future work clearly separated; every task links to approved spec.
- Verification: documentation diff and link checks; independent review; existing required CI for the documentation PR.

### S1-02 — Reproducible database and authorization test environment

- Owner: DevOps. Depends on S1-01.
- Scope: local Supabase setup, pinned supported tooling, documented reset/setup, isolated test identities, CI database test job, and an admission-mechanism feasibility check against current official docs.
- Excludes: hosted changes, production secrets, deployment, application feature routes.
- Acceptance: clean checkout can start/reset the test database; CI can run actual RLS/Auth integration tests; all test targets are local/test-only; account-creation hook/admission transaction feasibility documented with evidence.
- Verification: fresh setup/reset twice, one known-denied cross-user request, existing backend checks remain green. Record platform requirements and any Windows prerequisites.
- Why first: Builder needs a reliable environment to prove policies and the global account limit.

### S1-03 — Controlled registration and profile lifecycle

- Owner: Builder. Depends on S1-02.
- Scope: identity/admission migrations, verified email/password flow, backend token validation, idempotent profiles, restricted app-invitation issuance, authoritative 100-account limit; environment examples/docs without secrets.
- Excludes: group invitations, UI, workout routes, hosted execution. Initial owner provisioning must use the same counted-account model; product owner alone issues app access initially.
- Acceptance: valid invitation permits one account; invalid/expired/revoked/wrong-email/reused invitation fails; direct auth signup cannot bypass admission; two concurrent final-slot claims yield exactly one new account; user 101 rejected; existing users can sign in at capacity; retries do not duplicate profiles; invalid/expired tokens denied; profiles cannot be spoofed/read across users.
- Verification: real Auth integration and concurrent registration tests, profile RLS tests, existing backend suite; Reviewer and QA independently inspect exact revision.

### S1-04 — Private plan and workout schema

- Owner: Builder. Depends on S1-03.
- Scope: versioned migrations/constraints/RLS for plans, days, catalog/custom exercises, muscles, entries, and strength sets; minimal reference seeds and database fixtures proving the five split types and historical snapshots.
- Excludes: workout UI/CRUD routes, template library expansion, automatic rotation/recovery UI, feed storage.
- Acceptance: clean migrations apply; each user sees/writes only their own records; all cross-user parent attachments and owner reassignment fail; invalid reps/weights/duplicate positions or set numbers fail; deleting/editing a plan preserves logged workout snapshots; strength/cardio mismatches fail; no muscle history from unperformed preloaded exercises.
- Verification: authenticated SQL/Data API policy tests as two users, constraint and deletion tests, clean rebuild and migration-forward test; no privileged-only evidence.
- Why separate: data integrity can be reviewed before introducing a large user-facing workout flow.

### S1-05 — Groups and invitations

- Owner: Builder. Depends on S1-03; follows S1-04 for a single Builder to avoid migration/file conflicts.
- Scope: group/membership/invitation migrations and authenticated backend operations for create, join by code/link, leave, remove, transfer, revoke, delete. Atomic operations, bounded redemption rate, idempotent retries.
- Excludes: public search, posts/feed, group UI, automatic app registration from group invitation.
- Acceptance: users can join multiple groups; creator becomes owner/member atomically; duplicates do not create duplicate memberships or consume extra uses; concurrent final-use redemptions respect the limit; link/code revocation is shared; expired/revoked codes fail; nonowners cannot manage groups; owner must transfer/delete before leaving; deleting group retains workouts; signed-out requests cannot join or enumerate private details.
- Verification: independent users and groups, concurrency tests, direct Data API bypass attempts, membership change tests, rate-limit behavior tests without logging raw invitation secrets.

### S1-06 — Integrated acceptance and handoff

- Owners: Reviewer and QA independently; Senior SWE assesses readiness; DevOps verifies CI scope.
- Depends on S1-03 through S1-05, with review/QA also applied to each earlier PR rather than postponed until this task.
- Scope: fresh environment walkthrough: invite/register two users, initialize profiles, prove private data isolation, create two groups, redeem both invitation formats, revoke/remove/transfer/delete, verify unauthorized access and capacity evidence.
- Acceptance: all required checks green for exact final revisions; limitations documented; no live database modification; proposed hosted migration/recovery checklist prepared for later authorization; Sprint 2 handoff identifies what is implemented vs schema-only.
- Verification: reviewer diff findings and independent QA evidence linked to task issues/PRs; record commands, environment, commit, results. Do not claim browser flows passed when only API/database flows exist.

## Coordination and completion

Each GitHub issue names one implementation owner, dependencies, scope/exclusions, criteria, and verification. Reviewer and QA report independently on each PR with exact commits. DevOps owns environment/CI files; Builder owns migrations and backend features. Coordinate shared files before parallel work; tasks are not assignments until explicitly activated.

Flow: assigned task → implementation → independent review → fixes → QA → Senior SWE readiness assessment → product-owner-authorized merge. Updated code supersedes affected earlier test/review results. READY is not merge or deployment authorization. The owner authorized Sprint 1 kickoff after approving this design. Task issues are the shared handoff record; publication does not prove an agent has read them.

## Review checklist for the product owner

- Are the proposed defaults acceptable, especially invitation expiry/uses and who can invite?
- Should new group members see older shared posts, and should a departing member's posts disappear as proposed?
- Is snapshot sharing with explicit updates the expected behavior?
- Is the initial Sprint 1 boundary clear: tested foundation first, then workout screens and group feed?

You can request changes directly against any section. Approval is of the revised document, not an instruction to deploy or modify hosted data.

## Draft review record

An independent builder-check reviewer read this draft on 2026-11-15 and reported no important unanswered questions blocking an implementation plan. The registration feasibility gate remains an implementation prerequisite, and all proposed defaults still need product-owner review. This was a design review, not a code, database, security certification, or runtime test.

Subsequent revision: added the confirmed manual-highlight requirement and proposed retention/highlight lifecycle details. These additions were checked for consistency by the author; the earlier independent review does not cover this revision. Sprint 1 implementation scope is unchanged.

Approval record: the product owner said everything looks good, then explicitly requested starting Sprint 1 on 2026-11-15. This approves the document including highlight and retention defaults; merges and hosted changes still require separate authorization.
