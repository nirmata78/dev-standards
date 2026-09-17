---
name: doc-audit
description: Audit a repository's CodeWiki documentation for drift, broken links, orphaned pages and stale derived docs, without reference to any branch diff. Use when the user asks "are the docs stale", "check documentation drift", "audit the docs", "is anything undocumented", or before a release, an onboarding, or an architecture review.
---

# doc-audit

`doc-sync` settles the documentation debt a branch created. It is blind to
everything outside that diff — deliberately, because scanning the repository on
every pull request is the cost this approach avoids.

That leaves a gap. Documentation also rots without anyone touching it: a doc
falls behind code that changed on another branch, a page is deleted and its
index entry survives, an ADR sits in `proposed` for a year. This skill is the
periodic sweep that covers it.

**This skill reports. It does not write.** Fixing is a separate decision with a
separate blast radius — hand the findings to the user, or to `doc-sync` on a
branch created for the purpose.

## Phase 1 — Read the index

Read `DOCUMENTATION.md`. If it is absent, report that the repository has no
CodeWiki root and stop; suggest `/pragmatic-codewiki:codewiki-init`.

Enumerate what actually exists:

```bash
find docs -name '*.md' | sort
```

## Phase 2 — Index integrity

| Finding | How to detect |
|---|---|
| **Broken link** | an entry in `DOCUMENTATION.md` whose target file does not exist |
| **Orphan** | a file under `docs/` that no index entry points to |
| **Dead cross-link** | a relative link inside any doc that resolves to nothing |
| **Unregistered subtree** | a whole directory under `docs/` absent from the index |

An orphan is not automatically a defect — it may be an include, a template, or
an image. Report it as a question, not a failure.

## Phase 3 — Staleness

For each **derived** doc, compare the last time the doc changed against the last
time the code it describes changed:

```bash
git log -1 --format=%ci -- docs/api/overview.md
git log -1 --format=%ci -- src/api/
```

Code newer than the doc is a *signal*, not a verdict — a refactor with no
interface change moves the code date without invalidating the doc. Confirm by
reading the doc's claims against the current code before reporting drift, and
say which claim is wrong. "Possibly stale, code is newer" on its own wastes the
reader's time.

Skip **intent** docs here entirely. An ADR from 2023 describing a decision still
in force is correct, not stale; age is not evidence against it. See
[`reference/doc-taxonomy.md`](../../reference/doc-taxonomy.md) for the tiers.

## Phase 4 — Coverage gaps

Public surface with no documentation at all:

- exported modules or packages with no entry in the index
- HTTP routes, CLI commands, or public classes absent from any derived doc
- environment variables read by the code but missing from the setup doc
- a top-level source directory that the architecture doc never mentions

Report the gap and where the doc should live. Do not write it.

## Phase 5 — Decision hygiene

- ADRs in `proposed` older than 90 days — decided informally and never recorded?
- ADRs marked `superseded` with no link to what superseded them
- ADRs referencing code paths that no longer exist — the decision may still
  hold, but the record no longer points anywhere
- Accepted ADRs the implementation visibly contradicts (report; never edit)

## Output

Findings ordered by cost of being wrong, not by count:

```
doc-audit — 31 docs indexed, 34 on disk

Broken (index points at nothing)
  DOCUMENTATION.md → docs/api/webhooks.md — deleted in 8f2a1c0, entry remains

Stale (verified, not guessed)
  docs/setup.md — documents REDIS_URL as required; config.ts made it optional
  with a default in March

Undocumented
  src/billing/ — 3 public modules, no index entry, no doc

Orphans
  docs/_partials/header.md, docs/images/ — likely intentional, confirm

Decision hygiene
  ADR-0004 "Event sourcing for audit" — proposed, 14 months, no follow-up

Healthy
  api, schemas, architecture: index resolves, no drift found
```

Lead with what is wrong. End with what is fine, in one line — that line is what
makes the report trustworthy, because a reviewer can see the clean areas were
actually checked rather than skipped.

## When to stop

Report a clean bill of health and stop when the index resolves, no derived doc
contradicts the code, and no public surface is undocumented. A repository whose
documentation is in good shape is a normal outcome. Do not manufacture findings
to fill the report, and do not downgrade "healthy" into a list of stylistic
suggestions — style opinions belong in review, not in a drift audit.
