---
title: pragmatic-codewiki
---

# pragmatic-codewiki

**Version** 0.1.0 · **License** MIT ·
[Source](https://github.com/nirmata78/dev-standards/tree/main/plugins/pragmatic-codewiki)

Keeps documentation current without paying for it on every commit.

> **Not to be confused with** [CodeWiki principles](../codewiki.md), which are
> the three rules governing *this* repository. This page describes a plugin you
> install into *your* repositories. They share an ancestor and solve different
> problems: the rules here are enforced by CI on a marketplace; the plugin is a
> workflow for ordinary product code.

## The model

Google's CodeWiki idea — documentation as a living abstraction layer over code,
single source of truth, reachable from one entry point — is right about the
destination and silent about the cost. Applied literally to an AI-assisted
workflow it means regenerating documentation on every commit, which burns
context, clutters history, and rewrites the same page three times while the
branch is still moving.

Two adjustments make it survive contact with a real SDLC.

### 1. Deferred sync at pull request boundaries

Code freely during the feature loop. Settle the documentation debt **once**,
against the finished diff, immediately before the PR.

The saving is not mainly the writing. It is the *reading*: a doc update
mid-loop means loading the index and the affected pages into context, on every
iteration, to describe code that is about to change again. Deferring collapses
`n` partial updates into one correct one.

One clarification the original framing gets wrong by omission: **the deferral
applies to writing, not reading.** Intent docs are an input. An agent about to
implement something an ADR governs should read that ADR first. "Do not touch
`/docs` during iteration" is correct advice for updates and bad advice for
reads.

### 2. Ownership tiers

| Tier | Examples | Source of truth | On sync |
|---|---|---|---|
| **Intent** | ADRs, RFCs, architecture rationale | a human | audit, report, never rewrite |
| **Derived** | API reference, schemas, config keys | the code | rewrite to match |
| **Generated** | OpenAPI dumps, typedoc, coverage | a build tool | never hand-edit |

Without this split, a sync step eventually summarizes an implementation on top
of the decision that implementation was supposed to follow — and the record of
what was decided is gone, invisibly, inside a diff labelled "update docs".

When a file's tier is unclear, it is treated as **Intent**. The failure modes
are not symmetric: a stale derived doc costs one cycle, a rewritten ADR costs a
decision. Full rules:
[`reference/doc-taxonomy.md`](https://github.com/nirmata78/dev-standards/blob/main/plugins/pragmatic-codewiki/reference/doc-taxonomy.md).

## Install

```
/plugin marketplace add nirmata78/dev-standards
/plugin install pragmatic-codewiki@dev-standards
```

## Integration guide

### Step 1 — Initialize the repository

Once per repository:

```
/pragmatic-codewiki:codewiki-init
```

It surveys the repository first, then writes `DOCUMENTATION.md`, a `docs/`
subtree, an ADR index with a first ADR, and appends the documentation protocol
to `CLAUDE.md` or `AGENTS.md`. It never overwrites an existing file, and it
declines outright on a repository that already has a working docs structure.

Review the placeholders it leaves — they mark the places only you can fill —
then commit the result. Those files are plain Markdown and have no runtime
dependency on the plugin.

### Step 2 — Confirm the protocol landed

The appended section is what makes the workflow automatic. Without it the skills
exist but nothing invokes them at the right moment, and deferred sync degrades
into "documentation when someone remembers". Check that your agent file now
contains a **Documentation protocol** section naming `doc-sync` and the PR
boundary.

### Step 3 — Use it

```
/pragmatic-codewiki:doc-sync      # before opening a PR
/pragmatic-codewiki:doc-audit     # periodically, or before a release
```

In practice `doc-sync` mostly fires on its own: the protocol section tells the
agent to run it when you ask for a PR.

### Step 4 (optional) — Enforce the boundary with a hook

The protocol is an instruction, and instructions get skipped. To make the
boundary mechanical, add this to the repository's `.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          { "type": "command", "command": ".claude/hooks/require-doc-sync.sh" }
        ]
      }
    ]
  }
}
```

With `.claude/hooks/require-doc-sync.sh` (make it executable):

```bash
#!/usr/bin/env bash
# Intercepts `gh pr create` until the branch carries documentation changes.
command=$(python3 -c 'import json,sys; print(json.load(sys.stdin).get("tool_input",{}).get("command",""))')
case "$command" in *"gh pr create"*) ;; *) exit 0 ;; esac
[ -n "$DOC_SYNC_OK" ] && exit 0

base=$(git symbolic-ref --quiet refs/remotes/origin/HEAD 2>/dev/null | sed 's|refs/remotes/||')
[ -n "$base" ] || base=origin/main
git diff --name-only "$base"...HEAD | grep -qE '^(DOCUMENTATION\.md|docs/)' && exit 0

echo "Run /pragmatic-codewiki:doc-sync before opening this PR." >&2
exit 2
```

Exit code 2 returns the message to Claude rather than to you, so the agent runs
`doc-sync` and retries by itself.

**Its one failure mode, stated plainly:** "no documentation impact" is a
legitimate `doc-sync` outcome that changes no files, and this hook cannot
distinguish that from never having run. Those PRs need `DOC_SYNC_OK=1` to pass.
If that annoys you more than the occasional skipped sync, don't install the
hook — the protocol section alone covers the common case.

The hook is deliberately **not** shipped inside the plugin. A plugin-level
`PreToolUse` hook on `Bash` runs on every shell command in every repository
where the plugin is installed, including ones with no CodeWiki structure at all.
That is too much reach for a convenience.

### Step 5 (optional) — Check it in CI

A cheap guard that catches an index pointing at deleted pages:

```yaml
- name: Documentation index resolves
  run: |
    grep -o '](\([^)]*\)' DOCUMENTATION.md | cut -d'(' -f2 | while read -r f; do
      [ -e "$f" ] || { echo "broken link: $f"; exit 1; }
    done
```

Full drift detection needs judgment and belongs in `doc-audit`, not in a CI
grep.

## Skills

### codewiki-init

**Invoke** `/pragmatic-codewiki:codewiki-init` · **Model-invocable** yes ·
**Writes** yes

*When it fires:* setting up documentation in a repository for the first time —
"set up documentation", "install codewiki", "scaffold the docs", "add ADRs" —
or when `doc-sync` reports that no `DOCUMENTATION.md` exists.

*What it does:* surveys the repository, creates only the directories it
immediately populates, indexes pre-existing docs rather than ignoring them,
writes an ADR index and a first ADR recording the ADR practice itself, and
appends the protocol to the agent file the repository already uses. It never
overwrites; it merges and reports every path it touched.

*Output:* a list of files created, modified, indexed, and deliberately skipped,
plus the next manual step.

*Stop condition:* a repository with a populated `docs/` tree and an existing
index needs nothing initialized. It says so and suggests `doc-audit`, rather
than restructuring a working setup into this one's shape.

### doc-sync

**Invoke** `/pragmatic-codewiki:doc-sync` · **Model-invocable** yes ·
**Writes** yes

*When it fires:* before creating, opening, or submitting a pull request —
including on phrasings like "create a PR" or "submit this for review".

*What it does:* resolves the real base branch rather than assuming `main`,
diffs `base...HEAD` against the merge base, classifies every changed path by
ownership tier, updates only the derived docs the change actually affects,
registers any new doc in the index, verifies every index link resolves, and
stages the result.

It does **not** commit or open the PR unless asked, and it does not reconcile
conflicts. The case it exists to catch: a code file and an ADR covering it
changed on the same branch. That is either a decision being implemented or a
decision being edited to match drift after the fact — and only a human can tell
which.

*Output:* `Updated` / `Conflicts` / `Drift` / `No impact`, empty sections
omitted.

*Stop condition:* "no documentation impact", reported in one line. Most
branches are refactors, tests, and dependency bumps. A sync step that cannot
return nothing will invent work.

### doc-audit

**Invoke** `/pragmatic-codewiki:doc-audit` · **Model-invocable** yes ·
**Writes** no

*When it fires:* "are the docs stale", "check documentation drift", "is
anything undocumented", or ahead of a release, an onboarding, or an architecture
review.

*What it does:* the sweep a diff-driven sync structurally cannot do. `doc-sync`
sees only its own branch, so rot introduced elsewhere is invisible to it. This
checks index integrity (broken links, orphans, unregistered subtrees), verified
staleness in derived docs, undocumented public surface, and decision hygiene —
ADRs stuck in `proposed`, superseded ADRs with no forward link.

Staleness is *verified*, not inferred from timestamps. Code being newer than its
doc is a signal to check, not a finding to report; the report names the claim
that is actually wrong.

*Output:* findings ordered by cost of being wrong, ending with a one-line
statement of what was checked and found healthy — that line is what makes the
rest credible.

*Stop condition:* a clean bill of health is a normal outcome. It does not
downgrade "healthy" into a list of style suggestions.

## Review notes: what changed from the original framework

This plugin is an edit of an earlier draft, not a transcription. The
substantive changes, with reasons:

| Change | Why |
|---|---|
| Deferral applies to **writes only** | The draft said not to read `/docs` during iteration. Intent docs are an input to implementation; refusing to read an ADR before implementing what it governs is the opposite of the goal. |
| Base branch is **resolved**, not assumed | `git diff main...HEAD` fails on `master`, `develop`, release branches, and shallow CI clones. |
| Third tier: **Generated** | The draft's Derived/Intent split has no place for OpenAPI dumps and typedoc output. Hand-editing those produces a diff that looks like progress and is erased by the next build. |
| Explicit tie-break: **ambiguous → Intent** | A binary taxonomy with no rule for unclear cases resolves them inconsistently, in the direction that destroys decisions. |
| **Conflict detection** added | The draft's Case A / Case B split has no branch for "code *and* an ADR both changed" — which is the case most worth a human's attention. |
| **Stop conditions** added | The draft's sync always finds work. "No documentation impact" needed to be a stated, successful outcome or every PR grows a cosmetic doc commit. |
| **`doc-audit`** added | Diff-driven sync is blind to drift no branch caused. Nothing in the draft ever detected it. |
| Staleness must be **verified** | A timestamp comparison alone reports every refactor as drift, and a report that is mostly false positives gets ignored entirely. |
| Installer script **dropped** | It duplicated the skill text into a shell heredoc — and the two copies had already diverged in the draft, inside a framework whose premise is single-source-of-truth. A plugin already is the distribution mechanism. |
| Template links now **point at files that exist** | The draft's installer wrote an index linking to `docs/architecture/overview.md` and `docs/adr/README.md`, created the directories, and never created those files. Every fresh install started with broken links. |
| `codewiki-init` **never overwrites** | The draft's installer guarded `DOCUMENTATION.md` with `if [ ! -f ]` but clobbered `.claude/commands/doc-sync.md` unconditionally, destroying local customization. |
| Agent file is **detected**, not assumed | The draft writes `AGENTS.md`. Claude Code reads `CLAUDE.md`. Writing the protocol where the agent will not read it is a silent no-op. |

## Verify it loads

```bash
claude --plugin-dir ./plugins/pragmatic-codewiki
```

Then run `/pragmatic-codewiki:doc-sync` in a repository with a branch checked
out. Structural validation proves the layout; only loading proves Claude can
see the skills.
