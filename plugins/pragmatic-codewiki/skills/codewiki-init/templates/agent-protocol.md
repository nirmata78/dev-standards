## Documentation protocol (Pragmatic CodeWiki)

<!-- Appended by /pragmatic-codewiki:codewiki-init. Edit freely; this is now a
     normal part of this repository's agent instructions. -->

### Architecture

- **Entry point:** `DOCUMENTATION.md` is the index. Read it before reading
  anything under `docs/`; read only the pages it maps to the work at hand.
- **Modular storage:** documents live under `docs/` — `docs/architecture/`,
  `docs/adr/`, `docs/api/`.
- **Ownership tiers:**
  - *Intent* (ADRs, RFCs, architecture rationale) — human-authored. These
    constrain the code. Never rewrite them from the implementation.
  - *Derived* (API reference, schemas, config keys) — mirror the code. Rewrite
    them freely to match it.
  - *Generated* (OpenAPI dumps, typedoc) — build output. Never hand-edit.

### When documentation is written

Do **not** update `docs/` or `DOCUMENTATION.md` during feature iteration,
refactoring, or debugging loops. Code moves during a branch; a doc written
mid-loop is written twice.

Reading is not writing. Intent docs are an *input* — read the relevant ADR
before implementing something it governs. The deferral applies to updates only.

### Pull request boundary (required)

Before creating, opening, or submitting a pull request — including when asked
to "create a PR", "open a PR", or "submit this for review" — run
`/pragmatic-codewiki:doc-sync` and include the resulting documentation changes
in the branch.

It diffs the branch against its merge base, updates the derived docs the change
actually affects, audits intent docs without rewriting them, and reports
conflicts for a human. "No documentation impact" is a normal and complete
result for most branches.

### Periodic

`/pragmatic-codewiki:doc-audit` reports drift that no single branch introduced:
broken index links, derived docs the code has moved past, undocumented public
surface, ADRs stuck in `proposed`. It reports only; it makes no changes.
