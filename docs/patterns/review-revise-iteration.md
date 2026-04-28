# Review/Revise Iteration

## Pattern

An agent reviews a body of work against criteria, produces findings, and a second agent revises the work to address each finding. The revised work is reviewed again. The cycle repeats until every concern raised has been addressed — by edit or by reasoned rejection.

This pattern is formally specified as the [convergence protocol](../protocols/convergence-protocol.md). The pattern describes the observed behavior. The protocol specifies the properties that must hold: every `comment.revise` has a `resolution`, resolved comments stay resolved, no work is lost between invocations.

## Forces

- **Agents are imperfect reviewers.** A single review pass may miss issues. Iteration catches what individual passes miss.
- **Agents are imperfect revisers.** A fix may introduce new issues or incompletely address the finding. Re-review catches these.
- **Findings must be specific.** The reviewer tells the reviser what to fix — not general quality complaints, but actionable findings. The reviser follows the finding precisely.
- **Scope must be bounded.** The reviser only changes what the finding requires. Without this discipline, each revision creates unbounded side effects and the cycle diverges.
- **The reviser can refuse.** If a finding is incorrect, the reviser creates a rejection rationale rather than applying a harmful fix. Refusal is a valid resolution — it closes the comment without changing the document.

## Structure

```
review → findings → revise → review → findings → ...
         │                             │
         └── if none: converged ───────┘
```

The reviewer reads and produces findings. The reviser reads findings and edits (or rejects). The convergence predicate — every `comment.revise` has a `resolution` — determines when the cycle is done. Neither the reviewer's verdict nor the cycle count decides convergence; the state of the link graph does.

## Why it needs multiple cycles

Surface issues mask deeper ones. A reviewer looking at wrong citations can't see the logical gap beneath them. Once the citations are fixed, the gap becomes visible. Once the logic is fixed, the mathematical imprecision becomes visible. Each layer masks the next.

This means the cycle doesn't fix a flat list of known issues. It excavates — each pass clears a layer and reveals the next. The depth is unknown in advance. You discover it as you dig.

### Excavation stages

The findings progress through predictable stages:

1. **Citation accuracy** — wrong references, missing preconditions in contracts. Surface errors that are immediately visible.
2. **Completeness** — missing axioms, undeclared dependencies, boundary guards. Gaps in what's stated.
3. **Structural coherence** — axioms scoped too narrowly, proof structure mismatched to claims, narrative and formal content inconsistent.
4. **Mathematical precision** — unstated domain assumptions, claims asserted when derivable, proofs claiming specific scope when argument is general.
5. **Structural organization** — phantom dependencies, redundant claims, edge-case insights.

This progression was observed independently in ASN-0034 discovery (reviews 14–31), ASN-0036 discovery (reviews 1–26), and ASN-0036 claim convergence regional reviews. The same stages, same order, across different notes and different protocol stages. The convergence protocol deliberately does not prescribe finding order — this ordering is an empirical regularity, not a protocol property.

## When it converges

- Each finding is addressed in one revision — by edit or by rejection
- Revisions don't create new issues outside their scope
- The reviewer is consistent — it doesn't flag something it previously accepted
- All layers have been excavated — the reviewer files zero new `comment.revise` links

## When it stalls

- Revisions create side effects that generate new findings — [reverse-course oscillation](../equilibrium/reverse-course-oscillation.md)
- The reviewer contradicts itself across cycles
- The work is tightly coupled — fixing one part shifts another (see [dependency cone](dependency-cone.md))
- The reviser rejects findings that the reviewer re-files — reject cycling

Detecting stalls is a choreography and monitoring concern, not a protocol property. See [Claim Convergence](../claim-convergence.md) for detection strategies.

## Finding classification

The reviewer classifies each finding by whether it requires action:

- **`comment.revise`** — the document is wrong, incomplete, or ungrounded. Requires resolution.
- **`comment.observe`** — the document is correct but the reviewer noticed something. Recorded, no resolution required.

OBSERVE is the off-ramp for the [production drive](../design-notes/production-drive.md) — the LLM's tendency to generate findings and push them toward action. Without it, every observation becomes a mandatory revision and the cycle over-revises. The convergence predicate tracks only REVISE comments; OBSERVE accumulates as audit trail.

At discovery scale, the classification is REVISE / OUT_OF_SCOPE rather than REVISE / OBSERVE. OUT_OF_SCOPE channels the production drive into [scope promotion](scope-promotion.md) — engagement with adjacent material becomes a new inquiry rather than a mandatory fix to the current note.

## Applications

The pattern applies wherever an LLM reviews and revises content iteratively. The [convergence protocol](../protocols/convergence-protocol.md) is the general specification. Domain-specific protocols extend it:

**[Claim convergence](../protocols/claim-convergence-protocol.md).** The convergence protocol applied to per-claim files in the lattice. Adds structural validation (validate-before-review), lattice structure (`claim`, `contract`, `citation` links), scope strategies (adaptive and comprehensive as choreography), and the Dijkstra voice for both reviewer and reviser.

**[Discovery review](../protocols/note-convergence-protocol.md).** The convergence protocol applied to notes. Adds OUT_OF_SCOPE as the off-ramp (instead of OBSERVE). No structural validation — notes have no claim file contract. Convergence signals readiness for [claim derivation](../claim-derivation.md).

## Origin

The review/revise cycle was the first pattern to emerge. Initial attempts used single-pass LLM rewriting — produce a contract, move on. Quality was inconsistent. Adding a review step that checked the output and fed findings back to a reviser transformed the process. The cycle became the fundamental unit of all protocol stages.

## Related

- [Convergence Protocol](../protocols/convergence-protocol.md) — the formal specification of this pattern. The predicate, link types, safety and liveness properties.
- [Note Convergence Protocol](../protocols/note-convergence-protocol.md) — the convergence protocol applied to notes, with OUT_OF_SCOPE routing and lattice growth signals.
- [Claim Convergence Protocol](../protocols/claim-convergence-protocol.md) — the convergence protocol applied to claims, with lattice structure and a specific algorithm.
- [Dependency Cone](dependency-cone.md) — when tightly coupled documents stall single-document review, the cone is reviewed as a unit.
- [Validate Before Review](validate-before-review.md) — structural validation before each review cycle clears noise from the reviewer's path.
- [Reverse-Course Oscillation](../equilibrium/reverse-course-oscillation.md) — a failure mode of the review/revise cycle where findings alternate without converging.
- [Production Drive](../design-notes/production-drive.md) — the LLM behavioral force that OBSERVE and OUT_OF_SCOPE channel safely.