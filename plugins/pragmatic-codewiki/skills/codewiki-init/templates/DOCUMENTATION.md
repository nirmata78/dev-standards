# <Project> Documentation Index

> **Agent instruction:** this file is the documentation entry point. Read it
> before reading anything under `docs/`. Every document created under `docs/`
> must be registered below, with a one-line summary.
>
> Tier markers — `intent` (human-authored, never rewrite from code), `derived`
> (mirrors code state, rewrite freely), `generated` (build output, never edit
> by hand).

## 1. System architecture

- [Architecture Overview](docs/architecture/overview.md) `intent` — <System topology, component boundaries, and why they sit where they do.>

## 2. Decision records

- [ADR Index](docs/adr/README.md) `intent` — Architectural Decision Records: what was decided, when, and why.

## 3. API and interfaces

<!-- Add derived docs here as public surface appears. Delete this section if the
     project exposes no public interface. -->

## 4. Developer and operational guides

- [Setup & Environment](docs/setup.md) `derived` — <Local development setup, required config keys, and how to run the tests.>

---

**Keeping this current:** documentation is synchronized at pull request
boundaries, not on every commit. Run `/pragmatic-codewiki:doc-sync` before
opening a PR. Run `/pragmatic-codewiki:doc-audit` periodically to catch drift
that no single branch introduced.
