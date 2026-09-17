# Contributing

## Setup

Nothing to install. The structural checks run on a bare `python3`; manifest
validation needs the Claude Code CLI, which you already have if you use it.

## The one rule

Documentation changes in the same commit as the code it describes. Not the next
commit, not a follow-up issue. CI fails rather than warns, so a PR that adds a
skill without documenting it does not merge.

The reasoning is in [docs/codewiki.md](docs/codewiki.md); the short version is
that this repository is maintained mostly by agents that start every session
with no context, and undocumented code costs them a full-repo scan to
re-derive.

## Adding a plugin

Follow [docs/authoring/plugins.md](docs/authoring/plugins.md). Six files change:

1. `plugins/<name>/.claude-plugin/plugin.json`
2. `plugins/<name>/skills/<skill>/SKILL.md`
3. `plugins/<name>/README.md`
4. `docs/plugins/<name>.md`
5. `.claude-plugin/marketplace.json`
6. `docs/nav.json`

Plus the plugin tables in `docs/index.md` and `README.md`.

## Adding a skill

Follow [docs/authoring/skills.md](docs/authoring/skills.md). The `description`
frontmatter field is load-bearing: Claude reads it to decide when to load the
skill, so write it as a trigger condition. CI requires at least 40 characters.

## Before you push

```bash
python3 scripts/check_repo.py
claude plugin validate . --strict
claude --plugin-dir ./plugins/<name>    # load it and invoke the skill for real
```

The last one matters most. Validation checks structure; only loading proves
Claude can see the skills.

## Pull requests

`main` is protected: CI must pass, and force-pushes and deletions are blocked.
The PR template lists the documentation requirements as a checklist.

## Versioning

Bump `version` in both `plugin.json` and the `marketplace.json` entry whenever
a plugin's behavior changes. Users receive an update only when that field moves,
and CI requires the two to agree.
