# example-plugin

Reference plugin demonstrating the expected layout. Copy it as a starting point
for a real plugin, or delete it once the marketplace has real ones.

It carries no behavior of its own. Its purpose is to be a working, validated
example of the structure every other plugin in this repository follows.

## Install

```
/plugin marketplace add nirmata78/dev-standards
/plugin install example-plugin@dev-standards
```

## Skills

| Skill | Invoke | Model-invocable |
|---|---|---|
| `example-skill` | `/example-plugin:example-skill` | No |

### example-skill

Documents the skill format and proves the scaffold loads. It sets
`disable-model-invocation: true`, so Claude never loads it on its own - a
placeholder should not compete for attention with real skills. Invoke it
explicitly to confirm the plugin is wired up correctly.

## Layout

```
example-plugin/
├── .claude-plugin/
│   └── plugin.json          # manifest - the only file in this directory
├── README.md                # this file
└── skills/
    └── example-skill/
        └── SKILL.md         # directory name becomes the skill name
```

## Develop

```bash
claude --plugin-dir ./plugins/example-plugin
```

Then run `/example-plugin:example-skill`. Use `/reload-plugins` to pick up edits
without restarting.

## Docs

Full page: [docs/plugins/example-plugin.md](../../docs/plugins/example-plugin.md).
Conventions this plugin follows: [docs/architecture.md](../../docs/architecture.md).
