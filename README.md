# dev-standards

[![validate](https://github.com/nirmata78/dev-standards/actions/workflows/validate.yml/badge.svg)](https://github.com/nirmata78/dev-standards/actions/workflows/validate.yml)
[![pages](https://github.com/nirmata78/dev-standards/actions/workflows/pages.yml/badge.svg)](https://github.com/nirmata78/dev-standards/actions/workflows/pages.yml)
[![docs](https://img.shields.io/badge/docs-nirmata78.github.io-blue)](https://nirmata78.github.io/dev-standards/)
[![plugins](https://img.shields.io/badge/plugins-2-informational)](https://nirmata78.github.io/dev-standards/#plugins)
[![license](https://img.shields.io/badge/license-MIT-green)](LICENSE)

A Claude Code plugin marketplace for AI-managed repositories, plus the
documentation rules that keep it legible to the agents that maintain it.

The repository and the marketplace share one name - `dev-standards` - so you add
it and install from it using the same identifier.

**Documentation: [nirmata78.github.io/dev-standards](https://nirmata78.github.io/dev-standards/)**

## Install

```
/plugin marketplace add nirmata78/dev-standards
/plugin install <plugin-name>@dev-standards
```

Or run `/plugin` and browse the **Discover** tab.

At install you choose a scope: **user** (all your projects), **project** (shared
with collaborators via `.claude/settings.json`), or **local** (just you, just
this repo). Claude Code activates the plugin in the current session; if the
install summary says `Run /reload-plugins to activate.`, it runs that for you.

A plugin's skills are namespaced by the plugin name, so a skill directory
`skills/foo/` inside `example-plugin` is invoked as `/example-plugin:foo`.

### Other ways to add it

```
/plugin marketplace add https://github.com/nirmata78/dev-standards.git   # full git URL
/plugin marketplace add git@github.com:nirmata78/dev-standards.git       # SSH
/plugin marketplace add ./dev-standards                                  # a local clone
```

Append `#<ref>` to a git URL to pin a branch or tag.

### Managing it

```
/plugin marketplace list                  # marketplaces you have added
/plugin marketplace update dev-standards  # pull the latest plugin versions
/plugin marketplace remove dev-standards  # remove it (uninstalls its plugins)
/plugin list                              # installed plugins
/plugin disable <plugin-name>@dev-standards
/plugin uninstall <plugin-name>@dev-standards
```

## Plugins

| Plugin | Version | Description |
|---|---|---|
| [pragmatic-codewiki](plugins/pragmatic-codewiki) | 0.1.0 | Deferred documentation sync at pull request boundaries, with ownership tiers that keep human decisions from being overwritten by code state. |
| [example-plugin](plugins/example-plugin) | 0.1.0 | Reference plugin demonstrating the expected layout. Copy it to start a real plugin, or delete it. |

`example-plugin` is a placeholder that proves the structure loads. It can be
deleted once it stops being useful as a template.

## Team-wide installation

To register this marketplace automatically for everyone working in a repo,
commit this to that repo's `.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "dev-standards": {
      "source": {
        "source": "github",
        "repo": "nirmata78/dev-standards"
      }
    }
  },
  "enabledPlugins": {
    "pragmatic-codewiki@dev-standards": true
  }
}
```

Registering the marketplace this way does not install the plugins - each team
member still runs the install once, and Claude Code shows them the command.

## How this repository is organized

```
.
├── .claude-plugin/marketplace.json   # marketplace index; source paths are repo-relative
├── plugins/<name>/
│   ├── .claude-plugin/plugin.json    # manifest - the ONLY file in this directory
│   ├── README.md                     # atomic doc beside the code
│   └── skills/<skill>/SKILL.md       # directory name becomes the skill name
├── docs/                             # published site; nav.json is the canonical index
├── scripts/check_repo.py             # structural + documentation checks
├── CLAUDE.md                         # operating instructions for agents
└── .github/workflows/                # CI and Pages deployment
```

Full detail: [Architecture](https://nirmata78.github.io/dev-standards/architecture).

## Documentation is a constraint

This repository is maintained largely by AI agents, which arrive with no memory
of yesterday. Three rules keep it readable, and **CI fails rather than warns**
when they are broken:

1. **Atomic docs near code.** Concepts live in `/docs`; component detail lives
   beside the component. Each fact is written once, closest to what it
   describes.
2. **Doc-as-a-constraint.** Documentation changes in the same commit as the
   code. A plugin with no docs page, or a skill with no `### <skill>` section,
   fails the build.
3. **Explicit navigation tree.** [`docs/nav.json`](docs/nav.json) indexes every
   page, plugin, and skill so an agent can read one small file instead of
   scanning the repository each session. CI cross-checks it against the
   filesystem in both directions, because a stale index is worse than none.

Full rationale: [CodeWiki principles](https://nirmata78.github.io/dev-standards/codewiki).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md), or the authoring guides for
[plugins](https://nirmata78.github.io/dev-standards/authoring/plugins) and
[skills](https://nirmata78.github.io/dev-standards/authoring/skills).

Before pushing:

```bash
python3 scripts/check_repo.py      # structure and documentation
claude plugin validate . --strict  # manifest schema
```

## License

MIT - see [LICENSE](LICENSE).
