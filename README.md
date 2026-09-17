# dev-standards

A Claude Code plugin marketplace. This repository is the skeleton - it defines
the layout and the marketplace index; the plugins themselves get added over
time.

It currently ships one placeholder plugin, `example-plugin`, whose only job is
to prove the structure loads. Copy it to start a real plugin, or delete it once
there are real ones.

## Two names, on purpose

The repository is `nirmata78/dev-standards`. The marketplace it publishes is
named **`eng-pack`**. These are different identifiers and both are needed:

- You **add** the marketplace by its repository: `nirmata78/dev-standards`
- You **install** from it by its marketplace name: `<plugin>@eng-pack`

The marketplace name comes from the `name` field in
`.claude-plugin/marketplace.json` and is independent of the repository name.
If you would rather they match, change that one field - nothing else in the
repo depends on it, though anyone who has already added the marketplace would
need to re-add it.

Plugin names, by contrast, are kept identical across the three places they
appear (directory name, `plugin.json` `name`, and the `marketplace.json`
entry). Claude Code permits the marketplace entry's name to differ from the
plugin's own manifest, but that only creates confusion about which name to
install by.

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

At install you choose a scope: **user** (all your projects), **project**
(shared with collaborators via `.claude/settings.json`), or **local** (just you,
just this repo). Claude Code activates the plugin in the current session; if the
install summary says `Run /reload-plugins to activate.`, it runs that for you.

A plugin's skills are namespaced by the plugin name, so a skill directory
`skills/foo/` inside `example-plugin` is invoked as `/example-plugin:foo`.

### Other ways to add the marketplace

```
/plugin marketplace add https://github.com/nirmata78/dev-standards.git   # full git URL
/plugin marketplace add git@github.com:nirmata78/dev-standards.git       # SSH
/plugin marketplace add ./dev-standards                                  # a local clone
```

Append `#<ref>` to a git URL to pin a branch or tag.

### Managing it

```
/plugin marketplace list             # marketplaces you have added
/plugin marketplace update eng-pack  # pull the latest plugin versions
/plugin marketplace remove eng-pack  # remove it (uninstalls its plugins)
/plugin list                         # installed plugins
/plugin disable <plugin-name>@eng-pack
/plugin uninstall <plugin-name>@eng-pack
```

## Team-wide installation

To register this marketplace automatically for everyone working in a repo,
commit this to that repo's `.claude/settings.json`:

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

Adding the marketplace this way does not install the plugins - each team member
still runs the install once, and Claude Code shows them the command to run.

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
├── LICENSE
└── README.md
```

Layout rules this repo follows:

- `.claude-plugin/marketplace.json` sits at the repo root - that path is what
  makes the repo addable as a marketplace.
- Each `source` in `marketplace.json` is relative to the repo root
  (`./plugins/<name>`).
- Each plugin's manifest is at `<plugin>/.claude-plugin/plugin.json`.
- Component directories (`skills/`, and optionally `commands/`, `agents/`,
  `hooks/`) sit at the plugin root, **beside** `.claude-plugin/`, never inside
  it. Only `plugin.json` goes inside `.claude-plugin/`.
- A skill is a directory containing `SKILL.md`, so it can carry supporting files
  next to it. The directory name becomes the skill's invocation name.
- In `SKILL.md` frontmatter, `description` is the field that matters - Claude
  reads it to decide when to load the skill, so write it as a trigger
  condition. Add `disable-model-invocation: true` for a skill that should only
  run when invoked explicitly.
- Both manifests carry a `$schema` pointing at the published JSON Schema, so
  editors autocomplete the fields and flag typos.

## Adding a plugin

1. Copy `plugins/example-plugin/` to `plugins/<your-name>/`.
2. Update `.claude-plugin/plugin.json` - `name` must match the directory.
3. Replace the contents of `skills/` (and add `commands/`, `agents/`, or
   `hooks/` if the plugin needs them).
4. Add an entry to `.claude-plugin/marketplace.json` with
   `"source": "./plugins/<your-name>"` and the same `name`.

Develop against it without installing anything:

```
claude --plugin-dir ./plugins/<your-name>
```

Run `/reload-plugins` to pick up edits without restarting the session.

Validate before publishing - `--strict` turns warnings into errors, which is
what you want in CI:

```
claude plugin validate . --strict                       # the marketplace index
claude plugin validate ./plugins/<your-name> --strict    # one plugin manifest
```

Note that validation does not reject unknown fields, so a misspelled key can
pass. The `$schema` reference in each manifest is what catches those in an
editor.

Bump the plugin's `version` in both its `plugin.json` and its
`marketplace.json` entry whenever its behavior changes - users only receive
updates when that field moves.

## License

MIT - see [LICENSE](LICENSE).
