# eng-pack

A Claude Code plugin marketplace. This repository is the skeleton - it defines
the layout and the marketplace index; the plugins themselves get added over
time.

It currently ships one placeholder plugin, `example-plugin`, whose only job is
to prove the structure loads. Copy it to start a real plugin, or delete it once
there are real ones.

## Install

Add the marketplace once:

```
/plugin marketplace add nirmata78/dev-standards
```

Then install a plugin from it:

```
/plugin install <plugin-name>@eng-pack
```

Or browse and install interactively:

```
/plugin
```

Plugins installed this way are available in **all** your projects. Restart
Claude Code (or start a new session) after installing so the plugin's
components load.

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
/plugin uninstall <plugin-name>@eng-pack
```

## Team-wide installation

To make plugins from this marketplace load automatically for everyone working
in a repo, commit this to that repo's `.claude/settings.json`:

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
    "example-plugin@eng-pack": true
  }
}
```

## Repository layout

```
.
├── .claude-plugin/
│   └── marketplace.json              # marketplace index; `source` paths are repo-relative
├── plugins/
│   └── example-plugin/
│       ├── .claude-plugin/
│       │   └── plugin.json           # plugin manifest
│       └── skills/
│           └── example-skill/
│               └── SKILL.md          # each skill lives in its own named directory
└── README.md
```

Layout rules this repo follows:

- `.claude-plugin/marketplace.json` sits at the repo root - that path is what
  makes the repo addable as a marketplace.
- Each `source` in `marketplace.json` is relative to the repo root
  (`./plugins/<name>`).
- Each plugin's manifest is at `<plugin>/.claude-plugin/plugin.json`, and its
  `name` matches both its directory name and its `marketplace.json` entry.
- Component directories (`skills/`, and optionally `commands/`, `agents/`,
  `hooks/`) sit at the plugin root, **beside** `.claude-plugin/`, not inside it.
- A skill is a directory containing `SKILL.md`, so it can carry supporting files
  next to it. A bare `skills/SKILL.md` is not discovered.
- `SKILL.md` frontmatter needs `name` (matching its directory) and a
  `description` written so Claude can tell from it when to invoke the skill.

## Adding a plugin

1. Copy `plugins/example-plugin/` to `plugins/<your-name>/`.
2. Update `.claude-plugin/plugin.json` - `name` must match the directory.
3. Replace the contents of `skills/` (and add `commands/`, `agents/`, or
   `hooks/` if the plugin needs them).
4. Add an entry to `.claude-plugin/marketplace.json` with
   `"source": "./plugins/<your-name>"`.

Validate and test locally before publishing:

```
claude plugin validate .
/plugin marketplace add /path/to/your/clone
/plugin install <your-name>@eng-pack
```

Bump the plugin's `version` in both its `plugin.json` and its
`marketplace.json` entry whenever its behavior changes.

## License

MIT
