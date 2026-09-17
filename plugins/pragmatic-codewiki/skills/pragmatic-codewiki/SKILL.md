---
name: pragmatic-codewiki
description: Maintain a pragmatic, always-current code wiki. Use when documentation needs to be written, refreshed, or checked for drift after a code change - when the user asks to "document this", "update the docs/wiki", "write an ADR", "onboard someone to this module", or when a change alters public behavior, setup steps, or architecture.
---

# Pragmatic CodeWiki

Documentation is a cache of the codebase. Like any cache, it is only worth
keeping if it is invalidated when the source changes. This skill maintains that
cache: small, current, and derived from the code as it actually is.

## Principles

1. **The code is the source of truth.** Never describe intended behavior. Read
   the implementation and describe what it does today.
2. **Document what cannot be re-derived cheaply.** Why a tradeoff was made,
   what invariant must hold, which failure modes are load-bearing. Do not
   restate what a reader gets in ten seconds from a type signature.
3. **Touch the smallest surface.** Update the pages the change invalidated.
   Do not rewrite adjacent pages because they could be better.
4. **A stale page is worse than a missing one.** If a page describes something
   that no longer exists, delete it or fix it - do not leave it annotated.
5. **Every claim is anchored.** A page that names behavior cites the file (and
   ideally the symbol) it came from, so the next drift check is mechanical.

## Workflow

### Step 1 - Locate the wiki

Find where documentation already lives before creating a new home for it.
Check, in order: `docs/`, `wiki/`, `.github/`, `README.md`, any `CONTRIBUTING.md`,
and any docs config (`mkdocs.yml`, `docusaurus.config.*`, `mdbook.toml`).
Adopt the conventions you find - directory layout, file naming, heading depth,
link style, front matter. If no wiki exists, propose the smallest structure
that fits the repo and confirm before creating it.

### Step 2 - Determine the change surface

Establish what actually changed and what it invalidates:

- Diff scope: uncommitted changes, the branch against its base, or the range
  the user named.
- Public surface touched: exported functions, routes, CLI flags, env vars,
  config keys, schemas, migrations.
- Behavioral surface touched: defaults, error handling, retry/timeout policy,
  permissions, ordering guarantees.
- Operational surface touched: build, run, deploy, or test commands.

If none of these moved, say so and stop. An internal refactor with an unchanged
surface usually needs no documentation change.

### Step 3 - Drift check

For each candidate page, compare its claims against the current code and
classify every mismatch:

| Class | Meaning | Action |
|---|---|---|
| `STALE` | Page describes behavior that changed | Rewrite the claim |
| `ORPHANED` | Page describes something that no longer exists | Delete the section |
| `MISSING` | New public surface has no page | Add the minimum page |
| `THIN` | Page exists but omits a load-bearing constraint | Extend in place |
| `CURRENT` | Page matches the code | Leave untouched |

Report the classification before editing. Do not fix `THIN` items opportunistically
in an unrelated change - list them instead.

### Step 4 - Write

Each page carries only the sections it needs:

- **Purpose** - one or two sentences: what this exists to do, and for whom.
- **How it works** - the actual mechanism, in the order a reader traverses it.
  Name the real entry point (`path/to/file.ext:symbol`).
- **Interface** - the surface a caller touches: signatures, routes, flags,
  config keys, with required/optional and defaults.
- **Invariants and constraints** - what must remain true. These are the lines
  that prevent future bugs; they are the reason the page exists.
- **Failure modes** - what breaks, what the reader sees, what to do about it.
- **Decisions** - non-obvious tradeoffs and what was rejected. Link an ADR
  rather than relitigating the decision inline.
- **Related** - links to neighboring pages, no more than a handful.

Omit any section with nothing real to put in it. An empty heading is drift
waiting to happen.

### Step 5 - Verify

Before reporting done:

- Every code path, symbol, and command named in the edited pages exists.
- Every internal link resolves.
- Every command shown was run, or is explicitly marked as unverified.
- No section was left as a placeholder.

## ADRs

Record a decision when it was expensive to make and will be expensive to
revisit: storage engines, sync vs async boundaries, auth models, public API
shapes, dependencies that are hard to remove. Use a short, dated record:
context, the decision, the alternatives rejected and why, and the consequences
accepted. Never edit an accepted ADR's decision - supersede it with a new one
that links back.

## Output

Report as:

1. **Change surface** - what moved.
2. **Drift table** - each page with its classification.
3. **Edits made** - each file with a one-line summary.
4. **Deferred** - drift found but deliberately not fixed in this pass, so the
   next run can pick it up.
