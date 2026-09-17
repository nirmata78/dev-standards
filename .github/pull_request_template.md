## What changed

<!-- One or two sentences. -->

## Documentation

This repository treats documentation as a constraint, not a follow-up: docs
change in the same PR as the code. See [docs/codewiki.md](../blob/main/docs/codewiki.md).

If this PR adds or changes a **plugin**:

- [ ] `plugins/<name>/README.md` written or updated
- [ ] `docs/plugins/<name>.md` written or updated
- [ ] Entry added to `.claude-plugin/marketplace.json`, with `version` matching `plugin.json`
- [ ] Entry added to `docs/nav.json`
- [ ] Row added to the plugin tables in `docs/index.md` and `README.md`

If this PR adds or changes a **skill**:

- [ ] `SKILL.md` has a `description` that states *when* the skill should fire
- [ ] Skill named in its plugin's `README.md`
- [ ] `### <skill-name>` section added to `docs/plugins/<plugin>.md`
- [ ] Skill listed in `docs/nav.json` with `path`, `summary`, and `model_invocable`
- [ ] Loaded and invoked for real: `claude --plugin-dir ./plugins/<name>`

If this PR changes **behavior of an existing plugin**:

- [ ] `version` bumped in both `plugin.json` and `marketplace.json`

## Checks

- [ ] `python3 scripts/check_repo.py` passes
- [ ] `claude plugin validate . --strict` passes
