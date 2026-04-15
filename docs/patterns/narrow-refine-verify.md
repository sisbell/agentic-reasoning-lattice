# Narrow → Refine → Verify

## Lineage

This is the scientific method operationalized for autonomous agents.

In science: form a specific hypothesis (narrow), test and revise through experiment (refine), submit to peer review and replication (verify). The cycle repeats — each pass tightens the knowledge. The body of published, peer-reviewed literature is the trace of repeated cycles.

In agentic reasoning: scope a question (narrow), iteratively improve through review and revision (refine), check coherence against everything else (verify). The cycle repeats. The reasoning lattice is the trace.

The pattern language documented here is not a new method. It is the set of practical discoveries about what happens when autonomous agents operationalize the scientific method on structured reasoning — the failure modes they encounter, the adjustments they make, and the structures that emerge.

## Pattern

Every process in the system follows the same three-phase rhythm:

1. **Narrow** — reduce scope until the problem is tractable. Break a broad question into targeted sub-questions. Break a document into properties. Focus on a cluster instead of the whole.

2. **Refine** — within the narrowed scope, iteratively improve. Find issues, fix them, re-check. The scope is small enough to converge — changes don't cascade beyond the boundary.

3. **Verify** — step back to the original width and check that the refined pieces cohere. The narrowing created seams. Verification finds them.

This is one cycle, not three separate activities. Narrowing without refinement produces nothing. Refinement without narrowing can't converge. Verification without both has nothing to check. The three phases are inseparable.

## Forces

- **Broad scope can't refine.** Too much context, too many moving parts. Refinement stalls because each change affects everything else.
- **Narrow scope can converge.** Small enough to hold in focus, bounded enough that changes don't cascade. But narrow scope hides cross-boundary issues.
- **Verification reconnects.** The pieces were refined independently. Verification checks that they still fit — that the narrowing didn't create inconsistencies at the seams.
- **The cycle repeats.** Verification may find issues. Those issues feed the next cycle — narrow to the affected area, refine, verify again. Each pass tightens.

## The cycle everywhere

### Discovery

Narrow a broad question into targeted sub-questions scoped to each authority ([scoped inquiry](scoped-inquiry.md)). Refine the responses through [review/revise iteration](review-revise-iteration.md). Verify the whole consultation coheres through synthesis.

### Formalization

Narrow the ASN into per-property scope. Refine each property's proof and contract through review/revise iteration. [Verify the whole](verify-the-whole.md) ASN through cross-review.

### Extract/absorb

Narrow to a shared concept found across documents. Refine the extracted definition into a single authoritative version. Verify that consuming documents cohere with the shared version.

### Cone review

Narrow to a dependency cluster ([scope narrowing](scope-narrowing.md) to the cone). Refine the apex and its relationships through focused review/revise. Verify the cluster coheres before returning to wider scope.

### Scope promotion

An out-of-scope finding is promoted to its own investigation. That investigation follows the same cycle — narrow the new question, refine through review/revise, verify the new node coheres with the lattice.

## Relationship to other patterns

The three-phase cycle is the primitive. The other patterns either participate in it or adjust it:

- [Scope narrowing](scope-narrowing.md) — the first phase. How you narrow and when to widen.
- [Review/revise iteration](review-revise-iteration.md) — the second phase. The review/revise loop within the narrowed scope.
- [Verify the whole](verify-the-whole.md) — the third phase. Checking coherence at the original width.
- [Dependency cone](dependency-cone.md) — a signal that the narrowing in phase 1 overshot. The scope is too narrow for the coupling. Widen to the cluster and re-enter the cycle.
- [Scoped inquiry](scoped-inquiry.md) — narrowing applied to questions rather than documents.
- [Two data authorities](two-data-authorities.md) — the architecture that scoped inquiry operates within.
- [Scope promotion](scope-promotion.md) — findings at the boundary that seed new cycles.
- [Reasoning lattice](reasoning-lattice.md) — the structure that accumulates the output of repeated cycles.
- Extract/absorb — a cycle that restructures the lattice when shared concepts emerge.

## Origin

Discovered in this conversation. Scope narrowing, review/revise iteration, and verify the whole were documented as separate patterns. Each was observed independently at different times — review/revise from the first formalization runs, scope narrowing from the blueprinting redesign, verify the whole from cross-review.

The insight that they are one rhythm came from listing every process in the system and seeing the same three phases in each: discovery, formalization, extract/absorb, cone review, scope promotion. Three steps, same order, everywhere. The patterns we documented separately are phases of a single cycle.
