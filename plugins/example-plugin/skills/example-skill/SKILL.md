---
name: example-skill
description: Placeholder skill that documents the skill format for this marketplace. Invoke explicitly as /example-plugin:example-skill to verify the scaffold loads.
disable-model-invocation: true
---

# Example Skill

This skill exists to prove the scaffold works. It carries no real behavior -
replace it, or delete the plugin, before publishing anything meaningful.

It sets `disable-model-invocation: true` so Claude never loads it on its own.
A placeholder should not compete for attention with real skills. Drop that line
in a real skill, and write a `description` that states *when* to use it.

## Structure of a skill

A skill is a directory containing `SKILL.md`. The directory name becomes the
skill's invocation name, namespaced by the plugin:

```
plugins/example-plugin/skills/example-skill/SKILL.md
        └── plugin name        └── skill name      ->  /example-plugin:example-skill
```

In the frontmatter, `description` is the field that matters: Claude reads it to
decide whether to load the skill, so write it as a trigger condition ("Use
when...") rather than a topic label. `name` is optional in this layout because
the directory already supplies it; it is included here for readability.

Everything below the frontmatter is the prompt Claude receives when the skill
loads. Supporting files - references, scripts, templates - go beside `SKILL.md`
in the same directory and are referenced by relative path.

## Verifying the scaffold

```
claude --plugin-dir ./plugins/example-plugin
```

Then run `/example-plugin:example-skill`. If it responds, the layout is correct.
