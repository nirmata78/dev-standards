# pragmatic-codewiki

Keeps documentation current without paying for it on every commit.

Google's CodeWiki idea — documentation as a living abstraction layer over the
code, single-source-of-truth, indexed from one entry point — is right about the
destination and silent about the cost. Synchronizing docs on every commit burns
context, clutters history, and rewrites the same page three times while a branch
is still moving.

This plugin keeps the CodeWiki model and moves the payment to the **pull request
boundary**: code freely during the loop, settle the documentation debt once
against the finished diff.

The second half is ownership. Documents that *describe* code get rewritten from
it. Documents that *constrain* code — ADRs, RFCs, architecture rationale — are
audited and reported on, never overwritten. Collapsing that distinction is how
an agent ends up summarizing an implementation on top of the decision that
implementation was supposed to follow.

## Install

```
/plugin marketplace add nirmata78/dev-standards
/plugin install pragmatic-codewiki@dev-standards
```

Then, once per repository:

```
/pragmatic-codewiki:codewiki-init
```

## Skills

| Skill | Invoke | Fires when | Writes |
|---|---|---|---|
| `codewiki-init` | `/pragmatic-codewiki:codewiki-init` | setting up a repository | yes |
| `doc-sync` | `/pragmatic-codewiki:doc-sync` | before opening a PR | yes |
| `doc-audit` | `/pragmatic-codewiki:doc-audit` | periodically, on demand | no |

### codewiki-init

One-time scaffold: `DOCUMENTATION.md`, a `docs/` subtree, an ADR index and
first ADR, and the documentation protocol appended to the repository's
`CLAUDE.md` or `AGENTS.md`.

It surveys the repository before writing and seeds the index from what is
actually there, rather than emitting a fixed template whose links point at files
that do not exist. It never overwrites an existing file — it merges and reports.
On a repository that already has a working docs structure, it declines and
suggests `doc-audit` instead.

### doc-sync

The pull request boundary. Resolves the real base branch, diffs
`base...HEAD`, classifies every changed path, updates only the derived docs the
change actually affects, and stages them.

It reports conflicts rather than resolving them — notably the case where a code
file and an ADR covering it changed on the same branch, which is either a
decision being implemented or a decision being quietly rewritten to match drift.
Only a human can tell those apart.

"No documentation impact" is a normal result. Most commits are refactors, tests,
and dependency bumps, and treating those as documentation events is how doc
noise starts.

### doc-audit

The sweep `doc-sync` cannot do. Diff-driven sync is blind to rot that no single
branch caused: an index entry pointing at a deleted page, a derived doc the code
moved past on another branch, public surface nobody ever documented, an ADR
stuck in `proposed` for a year.

It reports and makes no changes — auditing and fixing have different blast
radii, and merging them produces a skill that edits files when you asked a
question.

## Layout

```
pragmatic-codewiki/
├── .claude-plugin/
│   └── plugin.json               # manifest - the only file in this directory
├── README.md                     # this file
├── reference/
│   └── doc-taxonomy.md           # intent / derived / generated, written once
└── skills/
    ├── codewiki-init/
    │   ├── SKILL.md
    │   └── templates/            # DOCUMENTATION.md, ADR index, ADR-0001, protocol
    ├── doc-sync/SKILL.md
    └── doc-audit/SKILL.md
```

`reference/doc-taxonomy.md` is shared by `doc-sync` and `doc-audit`. The
classification rules are the one piece of judgment both depend on, so they are
written once and linked, not copied into each skill.

## Why there is no installer script

The original design paired this with a `doc-sync-install.sh` that injects
`.claude/commands/doc-sync.md` into any repository. That makes the skill's text
exist in two places — the script and the source — and they had already diverged
in the draft.

A plugin is the distribution mechanism. Install it once, use it everywhere; the
skills travel with it and update with it. What a repository still needs on disk
is only what belongs to that repository: its index, its docs, its protocol
section. That is exactly what `codewiki-init` writes, and those files are plain
Markdown with no runtime dependency on the plugin.

## Develop

```bash
claude --plugin-dir ./plugins/pragmatic-codewiki
```

Then run `/pragmatic-codewiki:doc-sync`. Use `/reload-plugins` to pick up edits
without restarting.

## Docs

Full page, including the integration guide and the automatic PR hook:
[docs/plugins/pragmatic-codewiki.md](../../docs/plugins/pragmatic-codewiki.md).
