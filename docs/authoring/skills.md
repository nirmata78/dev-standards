---
title: Authoring skills
---

# Authoring skills

A skill is a directory containing `SKILL.md`:

```
plugins/<plugin>/skills/<skill>/SKILL.md
```

The directory name becomes the invocation name, namespaced by the plugin:
`plugins/foo/skills/bar/` is invoked as `/foo:bar`. Supporting files -
references, scripts, templates - sit beside `SKILL.md` and are referenced by
relative path.

## Frontmatter

```yaml
---
name: <skill-name>            # optional; the directory already supplies it
description: <trigger>        # required, and the field that matters
disable-model-invocation: true  # optional; explicit invocation only
---
```

`description` is what Claude reads to decide whether to load the skill. It is a
trigger condition, not a topic label. Write when to use the skill, including
the words a user would actually say:

> Maintain a pragmatic, always-current code wiki. Use when documentation needs
> to be written or checked for drift after a code change - when the user asks
> to "document this", "update the docs", or "write an ADR".

not:

> Documentation helper.

CI requires at least 40 characters, because a description shorter than that
cannot state a trigger. The ceiling is 1024.

Set `disable-model-invocation: true` for a skill that should only run when
someone types it. A placeholder or a destructive operation should not compete
for Claude's attention during unrelated work.

## Body

Everything below the frontmatter is the prompt Claude receives when the skill
loads. It is read by a model with no other context, so:

- **State the workflow as steps.** Numbered phases beat prose.
- **Give the output shape.** Say what the report should contain; otherwise each
  run produces a different format.
- **Encode judgment as tables.** A classification table turns a vague call into
  a lookup.
- **Say when to stop.** A skill that never concludes "nothing to do here" will
  invent work.
- **Prefer specifics.** Name real paths, real commands, real file patterns.

Keep it focused. A skill covering three unrelated jobs fires at the wrong time
for two of them; split it instead.

## Documenting a new skill

A skill is not finished when it works. Before it merges:

1. `SKILL.md` exists with a description of 40+ characters.
2. The skill name appears in `plugins/<plugin>/README.md`.
3. `docs/plugins/<plugin>.md` has a `### <skill-name>` section covering what it
   does, when it fires, and what it outputs.
4. `docs/nav.json` lists it under the plugin's `skills`, with `path`, `summary`,
   and `model_invocable`.

CI checks all four. See [CodeWiki principles](../codewiki.md).

## Testing

```bash
claude --plugin-dir ./plugins/<plugin>
```

Then invoke `/<plugin>:<skill>`. Run `/reload-plugins` after edits instead of
restarting.

Loading proves the skill is visible. To find out whether Claude actually reaches
for it on a realistic prompt - and whether the description is pulling its weight
- run it against test prompts with `claude plugin eval`.
