---
name: codewiki-init
description: Scaffold the Pragmatic CodeWiki structure into a repository - DOCUMENTATION.md index, /docs subtree, ADR template, and the agent protocol section in CLAUDE.md or AGENTS.md. Use when the user asks to "set up documentation", "install codewiki", "scaffold the docs", "add ADRs", or when doc-sync reports that no DOCUMENTATION.md exists.
---

# codewiki-init

One-time setup. It installs the structure the other two skills operate on, then
gets out of the way.

Seed the index from what the repository **actually contains**. A template full
of links to files that were never created is broken from the first minute, and
the first `doc-audit` run will spend its whole report saying so.

## Phase 1 — Survey before writing

```bash
ls DOCUMENTATION.md AGENTS.md CLAUDE.md 2>/dev/null
find . -maxdepth 2 -name '*.md' -not -path './node_modules/*' | head -50
ls docs 2>/dev/null
```

Establish three things:

1. **Is there already a docs structure?** A repository with `docs/` populated
   needs its existing files indexed, not a parallel empty tree beside them.
2. **What are the real top-level components?** The architecture entry should
   name them.
3. **Which agent file does this repo use?** Claude Code reads `CLAUDE.md`;
   `AGENTS.md` is the cross-tool convention. Use whichever exists. If both
   exist, put the protocol in `CLAUDE.md` and leave `AGENTS.md` a pointer to
   it — the same fact in two files is the duplication this framework is against.
   If neither exists, create `CLAUDE.md`.

**Never overwrite an existing file.** If `DOCUMENTATION.md` is already there,
merge missing sections into it and report what you added. If an agent file
exists, append the protocol section; do not replace the file. Report every path
touched.

## Phase 2 — Create the structure

Only create directories you will immediately populate. An empty `docs/api/`
tells a future reader that API docs exist somewhere, which is worse than its
absence.

```
DOCUMENTATION.md          # the index — every doc under /docs is registered here
docs/
├── architecture/
│   └── overview.md       # seeded from the real component survey
├── adr/
│   ├── README.md         # ADR index
│   └── 0001-record-architecture-decisions.md
└── setup.md              # seeded from real config keys and scripts
```

Templates are in [`templates/`](templates/) beside this file:

| Template | Becomes |
|---|---|
| [`DOCUMENTATION.md`](templates/DOCUMENTATION.md) | the root index |
| [`adr-index.md`](templates/adr-index.md) | `docs/adr/README.md` |
| [`adr-0001.md`](templates/adr-0001.md) | the first ADR, which records the ADR practice itself |
| [`agent-protocol.md`](templates/agent-protocol.md) | a section appended to `CLAUDE.md` or `AGENTS.md` |

Substitute real content for every `<placeholder>`. A placeholder committed as-is
is worse than an empty file, because it reads as documentation.

## Phase 3 — Index what already exists

Register every pre-existing doc found in Phase 1 under the right heading, with a
one-line summary, and a tier marker where the tier is clear:

```markdown
- [Public API Reference](docs/api/overview.md) `derived` — Endpoint contracts.
- [ADR Index](docs/adr/README.md) `intent` — Architectural Decision Records.
```

Markers are optional but worth adding: they let `doc-sync` skip classification
entirely, which is both faster and not a guess. See
[`reference/doc-taxonomy.md`](../../reference/doc-taxonomy.md).

## Phase 4 — Install the protocol

Append the contents of `templates/agent-protocol.md` to the repository's agent
file. This is what makes the workflow automatic: it tells the agent to defer
doc work during feature loops and to run `doc-sync` before opening a PR.

Without it, the plugin's skills exist but nothing triggers them at the right
moment, and the deferred-sync model silently degrades into "documentation when
someone remembers".

## Phase 5 — Verify

```bash
grep -o '](\([^)]*\)' DOCUMENTATION.md | cut -d'(' -f2 | while read -r f; do
  [ -e "$f" ] || echo "broken link: $f"
done
```

Every link must resolve. Then report:

```
codewiki-init — initialized

Created   DOCUMENTATION.md, docs/architecture/overview.md, docs/adr/README.md,
          docs/adr/0001-record-architecture-decisions.md, docs/setup.md
Modified  CLAUDE.md (appended CodeWiki protocol section)
Indexed   4 pre-existing docs found under docs/
Skipped   docs/legacy/ — 11 files, unclear ownership, left unregistered

Next: review the placeholders in docs/architecture/overview.md, then commit.
```

## When to stop

If the repository already has a `DOCUMENTATION.md` and a populated `docs/`
tree, there is nothing to initialize. Say so, suggest
`/pragmatic-codewiki:doc-audit` to check its health, and stop. Do not
restructure a working documentation setup into this one's shape — a convention
already in use beats a better convention imposed.
