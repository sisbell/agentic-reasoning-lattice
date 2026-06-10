# Review of ASN-0126

I checked the proof obligations carefully. The core mathematics is sound: P1 (registry invariance) follows from the framed step conditions; P3/P6 (conformance) follow from the gate preconditions and induction; P5 (realizability) correctly lifts ASN-0086's `Emit_K` through the projection bridge; the three-move R-Scope transfer for `Nullify_Binary` is airtight (the `dom(π(Σ').L) = dom(Ψ.L)` framing genuinely holds because `a_emit` is F-blind); and the born-nullified witness in the worked illustration computes correctly (`g ∈ coverage(G_rng)` at the half-open lower endpoint, so C3 fails). Boundary cases are covered: empty registry (link-inert), `G = ∅` for Multi, `F = ∅` rejected, arity > 3 with no `→_sh` image, ghost targets, self-nullification. Both ASN-0043 and ASN-0086 are foundations, so the cross-references are in-bounds, and `|e|` is set cardinality grounded in `Endset = 𝒫_fin(Span)`, not reinvented notation.

One anti-bloat finding remains.

## REVISE

### Issue 1: Shape-conformance treads "span count ≠ coverage" three times; the closing recap is fully redundant
**ASN-0126, Shape-conformance**: The section establishes the same measurement point across three passes.

- Para 1: "The span-count and coverage measures diverge sharply… Span-count, not coverage, is the measure."
- Para 2: "The divergence cuts both ways. Types are keyed by *coverage class*… yet F-conformance counts spans…"
- Closing: "The predicate therefore depends only on the tuple's span counts `|F|`, `|G|` and the shape recorded for K in the registry."

**Problem**: The closing recap adds nothing — it restates the Sh-conf bullet definition immediately above it (which already reads exactly `|F|`, `|G|`, and `shape(K)`), and the same fact is re-derived where it is actually used, in the P4 proof: "It respects `~` because… it reads only the span counts `|F|`, `|G|` and `shape(K) = shape(K')`." So the dependency is stated three times (definition, recap, P4) and used once. Separately, Para 2's lead-in "The divergence cuts both ways" re-opens Para 1's divergence theme before delivering its genuinely novel content (decomposition-sensitivity: two abutting spans fail every shape despite coverage-equal F; and the coverage-keyed-types-vs-span-counted-F tension). The novel content is worth keeping; the repeated "the measures diverge / span-count is the measure" framing is not.

**Required**: State "the gate measures span count, not coverage" once. Fold both illustrations under it — the unit-depth-span magnitude case (Para 1: one span, infinite coverage) and the abutting-spans decomposition case (Para 2: two spans, coverage equal to a one-span F) — and keep the coverage-keyed/span-counted tension as the section's distinctive point. Delete the closing recap sentence; P4 re-derives the dependency at its point of use. Retain the Multi-permissive paragraph and the no-residence-check (ghost) paragraph — those carry distinct content.

## OUT_OF_SCOPE

### Topic 1: A state-aware retraction discipline that re-internalizes single-tuple-scope
**Why out of scope**: The note correctly demotes ASN-0086's single-tuple-scope from a substrate guarantee to an app obligation (Retraction as an attributed Binary), and is explicit that the second gap — the P-tgt requirement on the target — "the gate cannot see at all," because P-tgt (target is a leaf link address) is a state-dependent runtime fact a *static* shape gate cannot evaluate. Restoring a substrate-level single-tuple-scope guarantee would therefore require a state-aware retraction check beyond the shape catalog, which is genuinely new machinery and not a defect in this framework's static-gate design. The Open Questions cover idempotence, behaviors, predicates, and arity but not this; it belongs to a successor note that layers operational semantics.

VERDICT: REVISE
