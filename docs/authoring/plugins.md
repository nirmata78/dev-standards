---
title: Authoring plugins
---

# Authoring plugins

Adding a plugin touches six files. CI fails if any is missed, so work through
the list rather than from memory.

## 1. Create the plugin

```bash
cp -r plugins/example-plugin plugins/<your-name>
```

Plugin names are kebab-case and must be identical in all three places they
appear: the directory name, `plugin.json`, and the `marketplace.json` entry.

## 2. Update the manifest

`plugins/<your-name>/.claude-plugin/plugin.json`:

```json
{
  "$schema": "https://json.schemastore.org/claude-code-plugin-manifest.json",
  "name": "<your-name>",
  "version": "0.1.0",
  "description": "One sentence: what this plugin does.",
  "author": { "name": "nirmata78", "url": "https://github.com/nirmata78" },
  "homepage": "https://github.com/nirmata78/dev-standards/tree/main/plugins/<your-name>",
  "repository": "https://github.com/nirmata78/dev-standards",
  "license": "MIT",
  "keywords": ["..."]
}
```

Only `plugin.json` belongs inside `.claude-plugin/`. Everything else -
`skills/`, `commands/`, `agents/`, `hooks/`, `README.md` - sits at the plugin
root.

## 3. Write the skills

See [Authoring skills](skills.md). Each skill is a directory under `skills/`
containing a `SKILL.md`.

## 4. Register it in the marketplace

Add an entry to `.claude-plugin/marketplace.json`:

```json
{
  "name": "<your-name>",
  "source": "./plugins/<your-name>",
  "description": "Same sentence as the manifest.",
  "version": "0.1.0",
  "author": { "name": "nirmata78" },
  "homepage": "https://github.com/nirmata78/dev-standards/tree/main/plugins/<your-name>",
  "license": "MIT",
  "keywords": ["..."],
  "category": "..."
}
```

`version` must match `plugin.json` exactly - CI compares them.

## 5. Write the documentation

Two files, per [doc-as-a-constraint](../codewiki.md#2-doc-as-a-constraint):

**`plugins/<your-name>/README.md`** - the atomic doc beside the code. What the
plugin is, the skills it ships, how to install it. Every skill name must appear
here.

**`docs/plugins/<your-name>.md`** - the page on this site. Needs a
`### <skill-name>` heading for each skill; CI checks for exactly that string.

Copy `plugins/example-plugin/README.md` and `docs/plugins/example-plugin.md` as
the shape to follow.

## 6. Add it to the navigation tree

`docs/nav.json`, under `plugins`:

```json
"<your-name>": {
  "manifest": "plugins/<your-name>/.claude-plugin/plugin.json",
  "readme": "plugins/<your-name>/README.md",
  "doc": "docs/plugins/<your-name>.md",
  "summary": "One line.",
  "skills": {
    "<skill-name>": {
      "path": "plugins/<your-name>/skills/<skill-name>/SKILL.md",
      "summary": "One line.",
      "model_invocable": true
    }
  }
}
```

Also add a row to the plugin table in `docs/index.md` and in the repository
README.

## 7. Verify

```bash
python3 scripts/check_repo.py
claude plugin validate . --strict
claude plugin validate ./plugins/<your-name> --strict
claude --plugin-dir ./plugins/<your-name>     # load it for real
```

The last one matters most: validation checks structure, but only loading the
plugin proves Claude can see the skills. Inside that session, run
`/<your-name>:<skill-name>`.

## Releasing a change

Bump `version` in both `plugin.json` and the `marketplace.json` entry. Users
receive an update only when that field moves.
