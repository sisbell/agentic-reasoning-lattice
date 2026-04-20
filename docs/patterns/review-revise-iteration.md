# Review/Revise Iteration

## Pattern

An agent reviews a body of work against criteria, produces findings, and a second pass (or agent) revises the work to address each finding. The revised work is reviewed again. The cycle repeats until no new findings emerge.

The cycle has a natural convergence property: each revision reduces the number of issues, and no revision introduces issues outside its scope. When the reviewer finds nothing, the work satisfies the criteria.

## Forces

- **Agents are imperfect reviewers.** A single review pass may miss issues. Iteration catches what individual passes miss.
- **Agents are imperfect revisers.** A fix may introduce new issues or incompletely address the finding. Re-review catches these.
- **Findings must be specific.** The reviewer tells the reviser what to fix — not general quality complaints, but actionable findings. The reviser follows the finding precisely.
- **Scope must be bounded.** The reviser only changes what the finding requires. Without this discipline, each revision creates unbounded side effects and the cycle diverges.

## Structure

```
review → findings → revise → commit → review → findings → ...
         │                                       │
         └── if none: converged ─────────────────┘
```

The review and revise steps may be the same agent or different agents. The reviewer needs read access to the work. The reviser needs write access. Separating them enforces the discipline that the reviewer identifies and the reviser acts.

## Why it needs multiple cycles

Surface issues mask deeper ones. A reviewer looking at wrong citations can't see the logical gap beneath them. Once the citations are fixed, the gap becomes visible. Once the logic is fixed, the mathematical imprecision becomes visible. Each layer masks the next.

This means the cycle doesn't fix a flat list of known issues. It excavates — each pass clears a layer and reveals the next. The depth is unknown in advance. You discover it as you dig.

The findings progress through predictable stages:

1. **Citation accuracy** — wrong references, missing preconditions in contracts. Surface errors that are immediately visible.
2. **Completeness** — missing axioms, undeclared dependencies, boundary guards. Gaps in what's stated.
3. **Structural coherence** — axioms scoped too narrowly, proof structure mismatched to claims, narrative and formal content inconsistent.
4. **Mathematical precision** — unstated domain assumptions, claims asserted when derivable, proofs claiming specific scope when argument is general.
5. **Structural organization** — phantom dependencies, redundant claims, edge-case insights.

This progression was observed independently in ASN-0034 discovery (reviews 14-31), ASN-0036 discovery (reviews 1-26), and ASN-0036 formalization regional reviews. The same stages, same order, across different notes and different pipeline stages.

## When it converges

- Each finding is addressed in one revision
- Revisions don't create new issues outside their scope
- The reviewer is consistent — it doesn't flag something it previously accepted
- All layers have been excavated — the reviewer finds nothing new

## When it stalls

- Revisions create side effects that generate new findings (oscillation)
- The reviewer contradicts itself across cycles
- The work is tightly coupled — fixing one part shifts another (see [dependency cone](dependency-cone.md))

## Applications

### Local review

**Scope**: one claim at a time, dependencies as fixed context.
**Review criteria**: 7-point checklist — logical gaps, unjustified steps, missing cases, dependency correctness, formal contract completeness.
**Reviser**: agent with Edit tools, operates on the claim's `.md` file.
**Convergence**: typically 2-5 cycles per claim.

### Contract review

**Scope**: one claim at a time.
**Review criteria**: formal contract matches what the proof establishes. Preconditions, postconditions, invariants, frame conditions.
**Reviser**: contract rewriter — regenerates the contract section.
**Convergence**: typically 1-3 cycles. Mechanical — less LLM judgment involved.

### Full review

**Scope**: entire note + foundation statements.
**Review criteria**: cross-claim consistency — carrier-set conflation, precondition chain gaps, scope mismatches, undeclared dependencies.
**Reviser**: agent with Edit/Write tools, can modify multiple claims per finding.
**Convergence**: slow — broad context means noisy findings. May stall on [dependency cones](dependency-cone.md).

### Regional review

**Scope**: one claim + its same-note dependencies, narrowed foundation.
**Review criteria**: same as full-review, but focused on the constraint system around one high-dependency claim.
**Reviser**: same as full-review.
**Convergence**: faster than full-review — narrower context produces more precise findings. Typically 1-3 cycles per cone.

## Origin

The review/revise cycle was the first pattern to emerge. Initial formalization attempts used single-pass LLM rewriting — produce a contract, move on. Quality was inconsistent. Adding a review step that checked the output and fed findings back to a reviser transformed the process. The cycle became the fundamental unit of all pipeline stages.
