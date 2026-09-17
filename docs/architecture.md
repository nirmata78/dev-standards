---
title: Architecture
---

# Architecture

## Layout

```
.
├── .claude-plugin/
│   └── marketplace.json          # the marketplace index; makes this repo addable
├── plugins/
│   └── <plugin-name>/
│       ├── .claude-plugin/
│       │   └── plugin.json       # plugin manifest - the ONLY file in here
│       ├── README.md             # atomic doc: what this plugin is
│       └── skills/
│           └── <skill-name>/
│               └── SKILL.md      # one directory per skill
├── docs/
│   ├── nav.json                  # canonical machine-readable index
│   ├── index.md                  # this site's entry point
│   ├── plugins/<plugin-name>.md  # one page per plugin
│   └── authoring/                # how-to guides
├── scripts/
│   └── check_repo.py             # structural + documentation checks
├── .github/workflows/            # CI and Pages deployment
└── CLAUDE.md                     # operating instructions for agents
```

## How Claude Code resolves this

**The marketplace.** `.claude-plugin/marketplace.json` must be at the
repository root. That exact path is what lets someone run
`/plugin marketplace add nirmata78/dev-standards`. The marketplace's name comes
from the `name` field inside that file, not from the repository name; we keep
them identical so there is one identifier rather than two.

**Plugin sources.** Each `source` in the index is a path relative to the
repository root: `./plugins/<name>`. Claude Code resolves it from there to find
the plugin directory.

**Plugin identity.** A plugin's name appears in three places - the directory
name, `plugin.json`'s `name`, and the `marketplace.json` entry. Claude Code
permits the marketplace entry to differ from the manifest, but then users have
two candidate names and no way to tell which one `/plugin install` wants. CI
requires all three to match.

**Components.** `skills/`, and optionally `commands/`, `agents/`, and `hooks/`,
sit at the **plugin root, beside `.claude-plugin/`**. Only `plugin.json` goes
inside `.claude-plugin/`. Putting a component directory in there is the most
common way to build a plugin that silently loads nothing, so CI checks for it
explicitly.

**Skills.** A skill is a directory containing `SKILL.md`. The directory name
becomes the skill's invocation name, namespaced by the plugin:
`plugins/foo/skills/bar/SKILL.md` is invoked as `/foo:bar`. The `skills/`
directory is always scanned - no manifest declaration is needed.

**Versions.** Users receive an update only when a plugin's `version` moves, so
it must be bumped in both `plugin.json` and the `marketplace.json` entry. CI
requires the two to agree.

## Schema validation

Both manifests carry a `$schema` pointing at the published JSON Schema:

- `https://json.schemastore.org/claude-code-marketplace.json`
- `https://json.schemastore.org/claude-code-plugin-manifest.json`

Neither schema sets `additionalProperties: false`, which means a misspelled key
is accepted rather than rejected - including by `claude plugin validate
--strict`. The `$schema` reference is what surfaces those typos, in the editor,
before they are committed. Treat an unexpected field highlighted by your editor
as an error even though the validator stays quiet.
