---
title: Validation
---

# Validation

Every push and pull request to `main` runs three checks. All three run locally
with the same commands.

## 1. Structure and documentation

```bash
python3 scripts/check_repo.py
```

Dependency-free; runs on a bare `python3`. It enforces the
[CodeWiki principles](codewiki.md):

- Plugin sets agree across the filesystem, `marketplace.json`, and `docs/nav.json`.
- Names match across directory, manifest, and marketplace entry; all kebab-case.
- Versions agree between `plugin.json` and the marketplace entry.
- `source` fields resolve to `./plugins/<name>`.
- No component directory hides inside `.claude-plugin/`.
- Every plugin has a `README.md` and a `docs/plugins/<name>.md` page.
- Every skill has a `SKILL.md` with a 40-1024 character description and a body.
- Every skill is named in its plugin README and has a `### <skill>` docs section.
- Every nav path exists; every nav entry has a summary; no orphans either way.
- Every `reference` entry a plugin declares in `docs/nav.json` resolves to a
  real file and carries a summary.

Failures print as a list with the file and the rule that was broken.

## 2. Manifest validation

```bash
claude plugin validate . --strict
claude plugin validate ./plugins/<name> --strict
```

`--strict` turns warnings into errors. Note the gap this does **not** close:
neither published schema sets `additionalProperties: false`, so a misspelled
field passes validation. The `$schema` reference in each manifest is what
catches typos in an editor. `scripts/check_repo.py` covers the specific fields
this repository depends on.

## 3. JSON syntax

Every `.json` file must parse. This runs first so a broken file produces a
clear error rather than a confusing downstream failure.

## Running everything

```bash
python3 scripts/check_repo.py && claude plugin validate . --strict
```

## The pull request checklist

`.github/pull_request_template.md` restates the documentation requirements as a
checklist, so they are visible while writing the change rather than after CI
rejects it.
