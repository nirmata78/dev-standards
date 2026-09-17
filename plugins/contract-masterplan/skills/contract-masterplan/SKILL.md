---
name: contract-masterplan
description: Drive contract-first delivery and verify implementations against the agreed contract. Use before building or changing an API, event, or schema boundary, and when checking a producer or consumer for conformance - triggers include OpenAPI/AsyncAPI/GraphQL/protobuf/JSON Schema work, "breaking change", "API versioning", "contract test", and cross-service integration.
---

# Contract Masterplan

An integration bug is almost always a disagreement that was never written down.
This skill writes it down first, then holds both sides to it. The contract is
the plan; the implementation is a detail that must conform.

## Principles

1. **The contract precedes the implementation.** If code shipped first, the
   contract is reverse-engineered from it and reviewed as a contract - not
   rubber-stamped.
2. **One artifact is normative.** Exactly one file defines the boundary.
   Everything else - types, clients, docs, mocks - is generated from or
   validated against it. Two hand-maintained definitions will diverge.
3. **Errors are part of the contract.** Status codes, error shapes, and codes
   are specified as precisely as the success path, because consumers branch on
   them.
4. **Compatibility is a property you check, not a promise you make.** Every
   change to a published contract gets a mechanical breaking-change analysis.
5. **Conformance is tested at both ends.** Producer verified against the
   contract, consumer verified against the contract - never against each other's
   live behavior.

## Workflow

### Step 1 - Identify the boundary and its artifact

Determine what kind of boundary this is and where its contract lives:

| Boundary | Normative artifact |
|---|---|
| HTTP/REST | OpenAPI (`openapi.yaml`, `*.openapi.json`) |
| GraphQL | SDL schema (`schema.graphql`) |
| gRPC | Protobuf (`*.proto`) |
| Async / events | AsyncAPI, or a versioned JSON Schema per event |
| Data at rest | Migration + schema definition |
| Library / module | Exported type declarations |

Search for an existing artifact before creating one; check for a schema
registry, a `contracts/` or `api/` directory, and generator config
(`openapi-generator`, `buf`, `graphql-codegen`, `quicktype`). If several
definitions exist, identify which is normative and flag the rest as derived.

### Step 2 - Draft or extract the contract

For each operation, pin down every element below. An unanswered row is an
integration bug scheduled for later.

```
Operation:      <name / method + path / topic / message type>
Purpose:        <what the caller achieves - one sentence>

Request
  Shape:        <fields: name, type, required?, constraints, default>
  Identity:     <auth scheme, scopes/permissions required>
  Idempotency:  <safe to retry? key mechanism?>

Response - success
  Status/shape: <code(s) and body schema>
  Nullability:  <which fields are guaranteed present>
  Pagination:   <cursor/offset, page size limits, ordering guarantee>

Response - failure
  <code> <error code/shape> : <cause> : <consumer's correct reaction>
  ... one row per failure the consumer must branch on

Semantics
  Consistency:  <read-after-write? eventual? bounded staleness?>
  Ordering:     <guaranteed? per key? none?>
  Side effects: <what else changes; at-least-once vs exactly-once>
  Limits:       <rate limits, payload size, timeout, expected latency>

Versioning
  Version:      <current>
  Stability:    experimental | stable | deprecated
  Deprecation:  <sunset date and replacement, if deprecated>
```

Prefer the boundary's own specification language over prose. Prose is where
ambiguity survives.

### Step 3 - Compatibility analysis

Classify every change against the currently published contract:

| Change | Class |
|---|---|
| Add optional request field with a default | Compatible |
| Add response field | Compatible (consumers must tolerate unknowns) |
| Add a new operation or a new enum value on input | Compatible |
| Loosen an input constraint | Compatible |
| Add required request field, or remove a default | **Breaking** |
| Remove or rename any response field | **Breaking** |
| Narrow a type, tighten a constraint, or change nullability | **Breaking** |
| Add an enum value the consumer must handle on output | **Breaking** |
| Change status code, error code, or error shape | **Breaking** |
| Change ordering, consistency, or idempotency semantics | **Breaking** (invisible to schema diff - state it explicitly) |

For anything breaking, do not proceed silently. Present the options: version the
boundary, add alongside and deprecate with a sunset date, or coordinate a
lockstep release - and name the known consumers each would affect.

### Step 4 - Verify both sides

**Producer conformance**
- [ ] Every operation in the contract is implemented.
- [ ] No undocumented operation, field, or status code is exposed.
- [ ] Responses validate against the schema, including error responses.
- [ ] Required/nullable and constraint enforcement matches the contract.
- [ ] Auth, limits, and idempotency behave as specified.

**Consumer conformance**
- [ ] Only documented fields and operations are relied on.
- [ ] Every failure row in the contract has a handling path.
- [ ] Unknown response fields are tolerated.
- [ ] Timeout and retry behavior respects the stated idempotency.
- [ ] Assumptions about ordering or consistency are ones the contract grants.

Report violations as `producer|consumer : <file:line> : <contract clause> :
<observed> vs <specified>`.

### Step 5 - Lock it in

Make conformance mechanical rather than remembered:

- Generate clients, server stubs, and types from the normative artifact; never
  hand-maintain a second copy.
- Add schema validation to the test suite for request and response bodies.
- Add contract tests at both ends, pinned to the contract file rather than to a
  live environment.
- Add a CI breaking-change diff against the published contract.
- Use contract-derived fixtures for mocks so mocks cannot drift.

## Output

Report as:

1. **Boundary** - what it is, and which artifact is normative.
2. **Contract** - the specification, in the boundary's own language.
3. **Compatibility** - change classification, with breaking items and options.
4. **Conformance** - producer and consumer findings, each anchored to a clause.
5. **Enforcement** - what was added to keep this checked automatically, and what
   remains manual.
