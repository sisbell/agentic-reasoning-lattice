# Review of ASN-0047

I reviewed the transition model for proof rigor and, per the active `review-mode.anti-bloat` classifier, for meta-prose and reviser drift around the forward-referenced machinery. The technical core (the per-elementary verification matrix, the K.μ~ decomposition with its filter-then-realize structure, the D-SEQ★ derivation, the GlobalLineage induction) is internally consistent and carefully guards against the obvious circularities (e.g., S8-fin(Σ') deliberately discharged independently of K.μ~-FIX). My findings are confined to accreted justification prose in structural slots.

## REVISE

### Issue 1: Rationale-as-statement drift in the FrontierEquivalence index entry
**ASN-0047, *Properties Introduced* → FrontierEquivalence row**: "A T4b parse of `t` alone cannot discharge the operational check: whether `inc(t, 0) ∈ Σ.E` turns on prior K.δ emission history ... so the frontier predicate must be evaluated against the reachable state rather than read off a structural identification of `t`."
**Problem**: A Properties-Introduced table cell exists to state *what* a property is. This cell instead argues *why the lemma is needed* (why a structural parse is insufficient) — the flagged "explains why ... is needed rather than what it says" pattern. The lemma statement and proof already appear in full in the body; the table duplicates the motivation.
**Required**: Reduce the cell to the lemma statement (biconditional + its discharge sources). If the why-not-structural observation is load-bearing, keep it once at the lemma's proof site, not in the index.

### Issue 2: K.σ subsumption explained in two places
**ASN-0047, *Typing note (M total)* bullet vs. *K.δ definition → Subsumption of ASN-0093's K.σ***: The typing note states "ASN-0047 subsumes K.σ into K.δ ... stated and justified at *Subsumption of ASN-0093's K.σ* (K.δ definition)," and the K.δ definition then restates the same subsumption ("ASN-0047 has no separate K.σ primitive: when `IsDocument(e)`, K.δ carries document registration...").
**Problem**: Two paragraphs convey the same fact (K.σ ⊆ K.δ for documents, M'(e)=∅ by totality) in different words — the "two paragraphs say the same thing" pattern, compounded by a deferral pointer between them.
**Required**: State the subsumption once at the K.δ definition; have the typing-note bullet reference it without re-explaining the routing.

### Issue 3: Open Question essay imagining a precondition-excluded case
**ASN-0047, *Open Questions* (final item, account-level depth-1)**: "The structural form `[N, 0, U, 1]` is itself well-typed (still `IsAccount`) under T4b, and admitting it would not violate any per-state invariant of the present model (the k = 1 harmlessness verification for documents would carry across); but no role for such an entity is documented..."
**Problem**: Every other Open Question is a one-line future-topic pointer. This one is a multi-sentence analysis of a case the K.δ k=1 precondition (`t ∈ E_doc`) already excludes — the flagged "imagines a case the precondition already excludes" + essay-content pattern. The harmlessness verification and design-evidence citation are argument, not a question.
**Required**: Reduce to a one-line open question (e.g., "Should the discipline admit account-level depth-1 extension for future use cases such as account renaming?"). Drop or relocate the harmlessness analysis.

## OUT_OF_SCOPE

### Topic 1: Link inheritance under forking
**Why out of scope**: The ASN explicitly defers a K.μ⁺_L-based link-inheritance mechanism for forked documents to a future ASN, and the fork composite correctly starts the forked document's link subspace empty. This is new territory, not a defect in the present transition model.

VERDICT: REVISE
