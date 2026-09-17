---
title: Overview
---

# dev-standards

A Claude Code plugin marketplace for AI-managed repositories, plus the
documentation rules that keep it legible to the agents that maintain it.

The repository and the marketplace share one name - `dev-standards` - so there
is a single identifier to remember.

## Install

```
/plugin marketplace add nirmata78/dev-standards
/plugin install <plugin-name>@dev-standards
```

Or run `/plugin` and browse the **Discover** tab. See the
[repository README](https://github.com/nirmata78/dev-standards#install) for
scopes, team-wide setup, and management commands.

## Navigation

| Page | What it covers |
|---|---|
| [CodeWiki principles](codewiki.md) | The three documentation rules this repository enforces in CI |
| [Architecture](architecture.md) | Repository layout and how Claude Code resolves it |
| [Authoring plugins](authoring/plugins.md) | Add a plugin to the marketplace, end to end |
| [Authoring skills](authoring/skills.md) | Write a `SKILL.md` that Claude loads at the right time |
| [Validation](validation.md) | What CI checks, and how to run it locally |

The machine-readable version of this tree is
[`docs/nav.json`](https://github.com/nirmata78/dev-standards/blob/main/docs/nav.json).
Agents should read that file rather than scanning the repository.

## Plugins

| Plugin | Version | Description |
|---|---|---|
| [pragmatic-codewiki](plugins/pragmatic-codewiki.md) | 0.1.0 | Deferred documentation sync at pull request boundaries, with ownership tiers that keep human decisions from being overwritten by code state. |
| [example-plugin](plugins/example-plugin.md) | 0.1.0 | Reference plugin demonstrating the expected layout. Copy it to start a real plugin, or delete it. |

`example-plugin` is a placeholder that exists to prove the structure loads. It
can be deleted once it stops being useful as a template.
