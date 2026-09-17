# eng-pack

A Claude Code plugin marketplace of engineering-standards plugins: keep
documentation current, keep work aligned to its backlog, and keep integrations
honest to their contracts.

## Plugins

| Plugin | What it does |
|---|---|
| **pragmatic-codewiki** | Maintains a pragmatic, always-current code wiki. Detects drift between code and docs and updates only the pages a change actually invalidated. |
| **scrum-master** | Turns vague requests into well-formed backlog items with testable acceptance criteria, and flags work that has drifted outside sprint scope. |
| **contract-masterplan** | Drives contract-first delivery: pins the API/schema contract before implementation, then verifies producers and consumers against it. |

## Install

Add the marketplace once:

```
/plugin marketplace add nirmata78/dev-standards
```

Then install whichever plugins you want:

```
/plugin install pragmatic-codewiki@eng-pack
/plugin install scrum-master@eng-pack
/plugin install contract-masterplan@eng-pack
```

Or browse and install interactively:

```
/plugin
```

Plugins installed this way are available in **all** your projects. Restart
Claude Code (or start a new session) after installing so the skills load.

### Other ways to add the marketplace

```
/plugin marketplace add https://github.com/nirmata78/dev-standards.git   # full git URL
/plugin marketplace add ./dev-standards                                  # a local clone, for development
```

### Managing it

```
/plugin marketplace list             # marketplaces you have added
/plugin marketplace update eng-pack  # pull the latest plugin versions
/plugin marketplace remove eng-pack  # remove it (uninstalls its plugins)
/plugin uninstall scrum-master@eng-pack
```

## Using the plugins

Each plugin ships a skill that Claude invokes on its own when the work matches.
You do not call anything explicitly - just describe the task:

- *"Update the docs for the change I just made"* → **pragmatic-codewiki**
- *"Turn this request into a story with acceptance criteria"* → **scrum-master**
- *"Does this endpoint still match the OpenAPI spec?"* → **contract-masterplan**

Each skill adopts the conventions already in your repo (doc layout, ticket ID
format, schema location) rather than imposing its own.

## Team-wide installation

To make these plugins load automatically for everyone working in a repo, commit
this to that repo's `.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "eng-pack": {
      "source": {
        "source": "github",
        "repo": "nirmata78/dev-standards"
      }
    }
  },
  "enabledPlugins": {
    "pragmatic-codewiki@eng-pack": true,
    "scrum-master@eng-pack": true,
    "contract-masterplan@eng-pack": true
  }
}
```

## Repository layout

```
.
├── .claude-plugin/
│   └── marketplace.json          # marketplace index; `source` paths are repo-relative
├── plugins/
│   ├── pragmatic-codewiki/
│   │   ├── .claude-plugin/
│   │   │   └── plugin.json       # plugin manifest
│   │   └── skills/
│   │       └── pragmatic-codewiki/
│   │           └── SKILL.md      # each skill lives in its own named directory
│   ├── scrum-master/
│   │   ├── .claude-plugin/plugin.json
│   │   └── skills/scrum-master/SKILL.md
│   └── contract-masterplan/
│       ├── .claude-plugin/plugin.json
│       └── skills/contract-masterplan/SKILL.md
└── README.md
```

Layout rules this repo follows:

- `.claude-plugin/marketplace.json` sits at the repo root - that path is what
  makes the repo addable as a marketplace.
- Each `source` in `marketplace.json` is relative to the repo root (`./plugins/<name>`).
- Each plugin's manifest is at `<plugin>/.claude-plugin/plugin.json`, and its
  `name` matches both its directory name and its `marketplace.json` entry.
- Component directories (`skills/`, and optionally `commands/`, `agents/`,
  `hooks/`) sit at the plugin root, **beside** `.claude-plugin/`, not inside it.
- A skill is a directory containing `SKILL.md`, so it can carry supporting files
  next to it. A bare `skills/SKILL.md` is not discovered.
- `SKILL.md` frontmatter needs `name` (matching its directory) and a
  `description` written so Claude can tell from it when to invoke the skill.

## Contributing

To add a plugin: create `plugins/<name>/` with a `.claude-plugin/plugin.json`
and at least one component directory, then add an entry to
`.claude-plugin/marketplace.json` with `"source": "./plugins/<name>"`.

Test locally before publishing:

```
/plugin marketplace add /path/to/your/clone
/plugin install <name>@eng-pack
```

Bump the plugin's `version` in both its `plugin.json` and its `marketplace.json`
entry whenever its behavior changes.

## License

MIT
