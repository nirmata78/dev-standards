---
name: example-skill
description: Placeholder skill used to verify that this marketplace's layout loads correctly. Use only when someone explicitly asks to test or verify the eng-pack plugin scaffold.
---

# Example Skill

This skill exists to prove the scaffold works. It carries no real behavior -
replace it, or delete the plugin, before publishing anything meaningful.

## Structure of a skill

A skill is a directory containing `SKILL.md`. The frontmatter has two required
keys:

- `name` - must match the containing directory name.
- `description` - written so Claude can decide *when* to load this skill. State
  the trigger conditions, not just the topic.

Everything below the frontmatter is the prompt Claude receives when the skill
loads. Supporting files (references, scripts, templates) go beside `SKILL.md`
in the same directory and are referenced by relative path.

## Verifying the scaffold

If the marketplace is wired up correctly, `/plugin` lists `example-plugin`
under `eng-pack`, and after installing it this skill appears in the session's
available skills.
