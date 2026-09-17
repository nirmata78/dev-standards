---
name: doc-sync
description: Synchronize CodeWiki documentation with finalized code at a pull request boundary. Use before creating, opening or submitting a pull request - when the user says "create a PR", "open a pull request", "submit for review", "push this for review", or invokes /doc-sync - to update derived docs from the branch diff and audit intent docs for drift.
---

# doc-sync

Documentation work is deferred to the end of a branch on purpose. During a
feature loop the code is still moving, so every doc update written mid-loop is
paid for twice: once to write it and once to rewrite it. This skill is where
that deferred cost is settled, once, against the finished diff.

Everything below assumes the repository follows the Pragmatic CodeWiki layout:
a `DOCUMENTATION.md` index at the root and modular docs under `/docs`. If
`DOCUMENTATION.md` is absent, stop and say so — suggest
`/pragmatic-codewiki:codewiki-init` rather than inventing a structure.

## Phase 1 — Establish the diff

Resolve the base branch instead of assuming `main`:

```bash
base=$(git symbolic-ref --quiet refs/remotes/origin/HEAD 2>/dev/null | sed 's|refs/remotes/||')
[ -n "$base" ] || for c in origin/main origin/master origin/develop main master; do
  git rev-parse --verify --quiet "$c" >/dev/null && base=$c && break
done
echo "base: $base"
git diff --name-status "$base"...HEAD
```

Use three dots. `base...HEAD` diffs against the merge base — the changes *this
branch* introduced. `base..HEAD` also drags in whatever landed on the base
branch meanwhile, and produces doc updates for other people's work.

If the branch has no commits relative to the base, stop: there is nothing to
document.

## Phase 2 — Classify every changed path

| Tier | Owner | Action |
|---|---|---|
| **Intent** — ADRs, RFCs, architecture rationale | human | audit only, never rewrite |
| **Derived** — API reference, schemas, config keys, module maps | code | rewrite to match code |
| **Generated** — OpenAPI dumps, typedoc, coverage | build tool | leave alone; report if stale |

When a file is ambiguous, treat it as **Intent** and report it. The failure
modes are asymmetric: a stale derived doc costs one cycle, a silently rewritten
ADR erases a decision. Full classification rules, including how to read tier
markers declared in `DOCUMENTATION.md`:
[`reference/doc-taxonomy.md`](../../reference/doc-taxonomy.md).

## Phase 3 — Map code changes to the docs they affect

Read `DOCUMENTATION.md` first. It is the index; it tells you which docs exist
and what each covers. **Then read only the docs that the changed paths plausibly
touch.** Do not read all of `/docs` — that is the context cost this whole
approach exists to avoid.

Update a derived doc when the diff changed something the doc states:

- a public signature, exported symbol, endpoint, or CLI flag
- a schema, data model, or event payload
- a config key, environment variable, or default
- a setup or build step
- a module's responsibility or its place in the architecture

Do **not** update a doc for: internal refactors with no interface change,
test-only changes, lockfile or dependency bumps, formatting, or comment edits.
These are the majority of commits, and treating them as documentation events is
how doc noise starts.

If the change adds a new public interface that no existing doc covers, create
the doc and register it in `DOCUMENTATION.md`. If it adds something internal,
do not.

## Phase 4 — Detect conflicts, do not resolve them

The case the original framework misses: **a code file and an intent doc covering
it both changed on the same branch.**

That is not a sync problem. It is either a decision being implemented (fine) or
an implementation that drifted and an ADR being edited to match it after the
fact (not fine, and invisible in review once merged).

When both changed, report it under **Conflicts** with the ADR, the code paths,
and one sentence on whether the implementation appears to follow the decision.
Never edit the intent doc to close the gap.

Also flag a doc-only change to a **derived** doc: someone hand-edited a file
that the next sync will overwrite. Say so.

## Phase 5 — Verify and stage

1. Every link in `DOCUMENTATION.md` resolves to a file that exists.
2. Every doc file you created or moved is registered in `DOCUMENTATION.md`.
3. Stage only the documentation files you changed:
   `git add DOCUMENTATION.md docs/` plus any module README you touched.
4. Do not commit unless asked. Do not create the PR yourself unless asked.

## Output

Report in this shape, every time. Sections with nothing in them are omitted
rather than padded:

```
doc-sync — base <base>, <n> files changed

Updated
  docs/api/overview.md      — added POST /sessions, removed deprecated /login
  docs/setup.md             — new SESSION_TTL config key

Conflicts
  docs/adr/0007-auth.md changed alongside src/auth/*.ts — the ADR now describes
  token rotation that the implementation does not do. Needs a human.

Drift
  docs/schemas/user.md references src/models/user.ts:Profile, which no longer
  exists. Not updated: outside this branch's diff.

No impact
  14 files (tests, lockfile, CI config)
```

## When to stop

A skill that cannot conclude "nothing to do" will invent work. Stop and report
exactly that when:

- the diff contains no change to a public interface, schema, config, or setup
  step — **the common case, and a clean result**
- only tests, fixtures, lockfiles, formatting, or CI config changed
- every affected doc already matches the code

"No documentation impact" is a successful run. Report it in one line and stop.
Do not go looking for unrelated staleness to justify the invocation — that is
what `/pragmatic-codewiki:doc-audit` is for, and it is a separate decision.

## Cost discipline

- Read `DOCUMENTATION.md`, then only the mapped docs. Never the whole tree.
- Read the diff, not the files, unless the diff is ambiguous.
- Edit surgically. Rewriting a whole doc to change one signature produces a
  review-hostile diff and loses human prose that was fine.
