# Working in this repository

This is a Claude Code plugin marketplace. The repository and the marketplace
share one name: `dev-standards`.

Read [`docs/nav.json`](docs/nav.json) first. It is the canonical index of every
doc page, plugin, and skill, with paths and summaries. It is validated against
the filesystem in CI, so it is safe to trust - read it instead of scanning the
repository.

## The rules

Documentation is a constraint here, not a follow-up. CI fails, not warns, when
it is missing. The three rules are in [`docs/codewiki.md`](docs/codewiki.md):

1. **Atomic docs near code** - concepts in `/docs`, component detail beside the
   component. Write each fact once, closest to what it describes; link rather
   than restate.
2. **Doc-as-a-constraint** - docs change in the same commit as the code.
3. **Explicit navigation tree** - `docs/nav.json` must describe the repository
   exactly, in both directions.

## Before you commit

```bash
python3 scripts/check_repo.py
```

Dependency-free and fast. It prints every broken rule with its file. Also run
`claude plugin validate . --strict` when a manifest changed.

## Adding a plugin

Follow [`docs/authoring/plugins.md`](docs/authoring/plugins.md). Six files
change; the guide lists them in order. Summary:

1. `plugins/<name>/.claude-plugin/plugin.json`
2. `plugins/<name>/skills/<skill>/SKILL.md`
3. `plugins/<name>/README.md`
4. `docs/plugins/<name>.md` - needs a `### <skill>` heading per skill
5. `.claude-plugin/marketplace.json` - `version` must match the manifest
6. `docs/nav.json` - plus the tables in `docs/index.md` and `README.md`

## Adding a skill

Follow [`docs/authoring/skills.md`](docs/authoring/skills.md). The description
is the load-bearing field: it states *when* the skill fires, and CI requires at
least 40 characters. Update the plugin README, the plugin docs page, and
`docs/nav.json` in the same commit.

## Things that silently break

- A component directory (`skills/`, `agents/`, `hooks/`) placed inside
  `.claude-plugin/` loads nothing. Only `plugin.json` goes in there.
- A plugin name that differs between the directory, `plugin.json`, and
  `marketplace.json` leaves users with no reliable install name.
- A `version` bumped in one manifest but not the other means users never
  receive the update.
- `claude plugin validate` does not reject unknown fields - neither published
  schema sets `additionalProperties: false`. A misspelled key passes. The
  `$schema` reference in each manifest catches it in an editor instead.

## Verifying a plugin actually works

Structural checks prove the layout. Only loading proves Claude can see the
skills:

```bash
claude --plugin-dir ./plugins/<name>
```

Then invoke `/<name>:<skill>`. A skill with `disable-model-invocation: true` is
hidden from the model's skill list by design - asking whether it is available
reports that it is not. Invoke it directly.
