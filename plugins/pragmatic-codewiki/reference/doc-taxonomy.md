# Documentation taxonomy

The one judgment every CodeWiki operation depends on: **who owns this file?**
Get it wrong in the safe direction and docs go stale. Get it wrong in the unsafe
direction and an agent overwrites a human's architectural decision with a
summary of the code that decision was meant to constrain.

Three tiers, in order of who wins when they disagree.

## Tier 1 - Intent docs (human-owned)

Documents that *drive* code. They state what should be true and why.

| Typically at | Examples |
|---|---|
| `docs/adr/`, `docs/rfc/` | Architecture Decision Records, RFCs |
| `docs/architecture/` | System topology, boundaries, design rationale |
| `docs/vision.md`, `docs/roadmap.md` | Product intent |
| `README.md` prose sections | Positioning, motivation |

**Rule: never rewrite from code.** An agent may fix a broken link, a stale path
reference, or a heading level. It may *report* that the implementation has
diverged. It may not reconcile the divergence by editing the ADR — that is a
human decision, and quietly rewriting it destroys the record of what was
decided.

An ADR is immutable once accepted. Superseding one means adding a new ADR that
references it, not editing the old one.

## Tier 2 - Derived docs (code-owned)

Documents that *describe* code. They mirror state and carry no independent
authority.

| Typically at | Examples |
|---|---|
| `docs/api/` | Endpoint and interface reference |
| `docs/schemas/` | Data models, database schemas, event payloads |
| `docs/setup.md` | Config keys, environment variables |
| Module-level `README.md` | What a package contains and exposes |

**Rule: rewrite to match the code.** When code and a derived doc disagree, the
code is right by definition. Update the doc; do not open a discussion.

## Tier 3 - Generated docs (tool-owned)

Output of a generator: OpenAPI dumps, typedoc/javadoc/sphinx HTML, coverage
reports, dependency graphs.

**Rule: never hand-edit.** Hand edits are lost on the next build, and an agent
editing them produces a diff that looks like progress and isn't. If generated
output is stale, the correct action is to run the generator or report that the
generation step is missing from CI.

Detect these by: a `DO NOT EDIT` banner, a path under `build/`, `dist/`,
`site/`, or `generated/`, or a `.gitattributes` entry marking them
`linguist-generated`.

## Classifying an unfamiliar file

In order — first match wins:

1. Generator banner, or a path under a build/output directory → **Generated**.
2. Path under `adr/`, `rfc/`, `decisions/`, or `architecture/` → **Intent**.
3. Filename matches `ADR-*`, `RFC-*`, or frontmatter has a `status:` field with
   a value like `proposed` / `accepted` / `superseded` → **Intent**.
4. Content is predominantly signatures, tables of fields, config keys, or
   endpoint lists → **Derived**.
5. Content is predominantly prose explaining a choice, with words like
   "we decided", "instead of", "trade-off", "because" → **Intent**.
6. Still unclear → **treat as Intent** and report it.

Rule 6 is deliberate. The failure modes are not symmetric: a derived doc
mistakenly left alone is stale for one more cycle, while an intent doc
mistakenly rewritten is a decision silently erased. When unsure, do the
reversible thing.

## Where the tiers are recorded

A repository can state the mapping explicitly instead of relying on inference.
`DOCUMENTATION.md` supports a tier marker per entry:

```markdown
- [Public API Reference](docs/api/overview.md) `derived` — Endpoint contracts.
- [ADR Index](docs/adr/README.md) `intent` — Architectural Decision Records.
- [Generated SDK docs](docs/sdk/index.html) `generated` — Built by `npm run docs`.
```

An explicit marker always wins over inference. Repositories that add markers get
faster and more reliable syncs, because no classification step is needed.
