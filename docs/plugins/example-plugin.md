---
title: example-plugin
---

# example-plugin

**Version** 0.1.0 · **License** MIT ·
[Source](https://github.com/nirmata78/dev-standards/tree/main/plugins/example-plugin)

Reference plugin demonstrating the expected layout. Copy it as a starting point
for a real plugin, or delete it once the marketplace has real ones.

It carries no behavior of its own. It exists so that the structure every other
plugin follows is available as something you can read, load, and run.

## Install

```
/plugin marketplace add nirmata78/dev-standards
/plugin install example-plugin@dev-standards
```

## Skills

### example-skill

**Invoke** `/example-plugin:example-skill` · **Model-invocable** no

Documents the skill format and proves the scaffold loads.

*When it fires:* only when invoked explicitly. The skill sets
`disable-model-invocation: true` so Claude never loads it on its own, which is
the right setting for a placeholder - it would otherwise consume context and
compete for attention during unrelated work.

*What it does:* explains how a skill directory maps to an invocation name, which
frontmatter fields matter, and where supporting files go.

*Output:* an explanation of the skill format. It makes no changes to the
repository.

## Verifying the scaffold

```bash
claude --plugin-dir ./plugins/example-plugin
```

Then run `/example-plugin:example-skill`. A response confirms the layout is
correct. Note that asking Claude whether the skill is *available* will report
that it is not - `disable-model-invocation` hides it from the model's skill
list by design. Invoke it directly instead.

## Replacing it

See [Authoring plugins](../authoring/plugins.md). Copy the directory, rename it
in all three places, then update `marketplace.json`, `docs/nav.json`, and the
plugin tables in `docs/index.md` and the repository README.
