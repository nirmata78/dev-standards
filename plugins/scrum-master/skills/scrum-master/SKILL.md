---
name: scrum-master
description: Keep engineering work aligned to its agile artifacts. Use when a request needs to become a well-formed backlog item, when a story needs acceptance criteria or splitting, when work in progress may have drifted outside sprint scope, or when the user mentions a sprint, backlog, standup, story points, epic, or ticket.
---

# Scrum Master

Most delivery failures are not coding failures. They are a request that was
never pinned down, a story that quietly grew, or work that no one can tell is
finished. This skill closes those gaps before code is written, and catches them
while it is.

## Principles

1. **A story is a contract, not a title.** If two people can read it and build
   different things, it is not ready.
2. **Done is defined before started.** Acceptance criteria are written first,
   or they will be written to match whatever got built.
3. **Vertical slices only.** A story delivers observable value end to end. "The
   backend half" is a task, not a story.
4. **Scope creep is detected, not prevented.** Assume it happens; make it
   visible the moment it does and let a human decide.
5. **Estimate uncertainty, not effort.** When a number is hard to give, the
   missing thing is information - name it instead.

## Workflow

### Step 1 - Read the board

Find the existing agile context before inventing any. Check issue trackers via
available tooling (`gh issue`, `gh project`, Jira/Linear MCP servers if present),
then in-repo artifacts: `BACKLOG.md`, `ROADMAP.md`, `docs/sprint*`, issue and PR
templates under `.github/`. Adopt the conventions in use - ID format, label
taxonomy, estimation scale, column names, definition of done. Never introduce a
competing scheme.

### Step 2 - Classify the request

| Type | Signal | Shape |
|---|---|---|
| `EPIC` | Spans several sprints or several stories | Split before estimating |
| `STORY` | One vertical slice of user-visible value | Full template below |
| `TASK` | Technical step with no standalone user value | Attach to a parent |
| `BUG` | Behavior diverges from an agreed expectation | Repro + expected vs actual |
| `SPIKE` | The answer is unknown; the output is knowledge | Time-box + question |
| `CHORE` | Maintenance with no behavior change | Minimal record |

State the classification and why. If a request is really two items, split it
rather than writing one item with "and" in the title.

### Step 3 - Write the item

```
Title:    <verb> <object> so that <outcome>

As a      <specific role - never "user" if a narrower role fits>
I want    <capability>
So that   <the value; if this cannot be stated, the item may not be worth doing>

Context
  - Why now, and what changes if this is not done.
  - Links: parent epic, related items, prior art, relevant docs.

Acceptance criteria
  - [ ] Given <state>, when <action>, then <observable result>
  - [ ] Given <edge case>, when <action>, then <handled result>
  - [ ] <non-functional bar: latency, permissions, telemetry, a11y>

Out of scope
  - <the adjacent thing a reader will assume is included, named explicitly>

Dependencies
  - <blocking item, decision, access, or external team>

Estimate: <scale in use>   Confidence: high | medium | low
Open questions
  - <question> -> needs answer from <who> before <which criterion> is testable
```

Every criterion must be observable by someone who did not write the code. Reject
criteria phrased as implementation ("uses a queue") in favor of behavior
("submissions survive a restart with no duplicates").

### Step 4 - Readiness check

An item is sprint-ready only when all hold:

- [ ] Value stated, and stated for a specific role.
- [ ] Criteria are testable and cover at least one edge case.
- [ ] Vertical - it can ship on its own.
- [ ] Dependencies named and either resolved or tracked.
- [ ] Estimated, or explicitly converted to a spike.
- [ ] Out-of-scope boundary drawn.

Report the failing boxes plainly. Do not mark an item ready by softening the
criteria.

### Step 5 - Alignment check on work in progress

When work is already underway, compare what is being built to the item that
authorized it:

- **On track** - changes map to stated criteria.
- **Scope creep** - changes serve no criterion. Name the file/change and the
  missing criterion; propose a follow-up item rather than deleting the work.
- **Scope gap** - a criterion has no corresponding change yet.
- **Contradiction** - a change violates a stated criterion or an out-of-scope line.

Surface this; never silently re-plan around it.

### Step 6 - Splitting

When an item is too large, split along a dimension that keeps each piece
shippable: workflow step, happy path vs edge cases, one data type first, one
platform or surface first, read before write, manual before automated. Do not
split by architectural layer - that produces tasks that cannot ship.

## Ceremonies

- **Standup** - per stream: what moved, what is next, what is blocked and on
  whom. No status theater; a blocker without an owner is not reported.
- **Planning** - readiness check every candidate; flag anything unready before
  capacity is discussed.
- **Review** - walk the acceptance criteria one by one against the built
  behavior; unmet criterion means unmet story.
- **Retro** - separate what the process caused from what circumstance caused,
  and produce at most a couple of owned actions.

## Output

Report as:

1. **Classification** - type and rationale.
2. **The item(s)** - in the template above, using the repo's own conventions.
3. **Readiness** - the checklist with failures called out.
4. **Alignment** - for in-flight work: on track, creep, gaps, contradictions.
5. **Questions** - what a human must answer, and what it blocks.
