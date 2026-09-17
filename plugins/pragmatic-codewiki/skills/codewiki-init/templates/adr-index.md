# Architectural Decision Records

An ADR records a decision that was expensive to make and would be expensive to
revisit: why this approach, what was rejected, and what it costs.

**These are intent documents.** They constrain the code rather than describe it.
An agent may not rewrite an ADR to match an implementation that drifted — it
reports the divergence and leaves the record intact.

## Status values

| Status | Meaning |
|---|---|
| `proposed` | Written, not yet agreed. |
| `accepted` | In force. The implementation is expected to follow it. |
| `superseded` | Replaced. Must link to the ADR that replaced it. |
| `deprecated` | No longer applies, and nothing replaced it. |

An accepted ADR is immutable. Changing your mind means writing a new ADR that
supersedes it, so the history of the decision survives.

## Index

| # | Title | Status | Date |
|---|---|---|---|
| [0001](0001-record-architecture-decisions.md) | Record architecture decisions | accepted | <YYYY-MM-DD> |

## Adding one

Copy the most recent ADR, take the next number, and add a row above. Keep it to
one decision per record — a document deciding three things cannot be superseded
without disturbing the other two.
