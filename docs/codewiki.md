---
title: CodeWiki principles
---

# CodeWiki principles

This repository is maintained largely by AI agents. Agents do not remember
yesterday's session, so anything not written down is re-derived - slowly,
and sometimes wrongly. These three rules exist to make the repository legible
to an agent that arrives with no context, and CI enforces all three.

## 1. Atomic docs near code

High-level concepts live in [`/docs`](index.md). Anything that describes a
specific component lives next to that component.

| Documentation | Lives at | Covers |
|---|---|---|
| Marketplace overview, conventions, how-to guides | `docs/` | Concepts spanning more than one plugin |
| Plugin purpose, its skills, its usage | `plugins/<name>/README.md` | One plugin |
| What a skill does and when it fires | `plugins/<name>/skills/<skill>/SKILL.md` | One skill |

The rule: **a fact is written once, in the place closest to what it describes.**
A `/docs` page that needs a plugin detail links to that plugin's README rather
than restating it. Restating is how two documents start disagreeing.

Enforced by `scripts/check_repo.py`: every plugin must have a `README.md`;
every skill must have a `SKILL.md` with a description of at least 40
characters, because a description too short to state a trigger is not a
description.

## 2. Doc-as-a-constraint

**Documentation changes in the same commit as the code it describes.** A
feature is not complete until its `/docs` counterpart reflects it.

This is a constraint rather than a convention, which means it fails the build:

- A plugin directory with no entry in `marketplace.json` fails.
- A plugin with no `docs/plugins/<name>.md` page fails.
- A skill with no `### <skill-name>` section in its plugin's docs page fails.
- A skill not mentioned in its plugin's `README.md` fails.
- A version bumped in `plugin.json` but not in `marketplace.json` fails.

There is deliberately no warning level. A warning is a note that documentation
may be added later, and later does not arrive. The
[pull request template](https://github.com/nirmata78/dev-standards/blob/main/.github/pull_request_template.md)
restates these as a checklist so the requirement is visible before CI runs.

## 3. Explicit navigation tree

[`docs/nav.json`](https://github.com/nirmata78/dev-standards/blob/main/docs/nav.json)
is the canonical index of this repository: every doc page, every plugin, every
skill, each with its path and a one-line summary.

It exists so that an agent can answer "what is in this repository and where" by
reading one small file, instead of scanning every directory at the start of
every session. That only works if the file is exactly right, so
`scripts/check_repo.py` cross-checks it against the filesystem in both
directions:

- Anything on disk that is missing from the tree fails.
- Anything in the tree that is missing from disk fails.
- Path fields that do not match the real location fail.
- Entries without a summary fail.

A stale index is worse than no index, because it is trusted. Keeping it correct
is what makes it worth reading.

## Working in this repository

If you are an agent, read
[`CLAUDE.md`](https://github.com/nirmata78/dev-standards/blob/main/CLAUDE.md)
at the repository root first: it states these rules operationally, as steps to
follow when adding a plugin or a skill.

Run the checks before you commit:

```bash
python3 scripts/check_repo.py
```
