# Review of ASN-0091

## REVISE

### Issue 1: Four worked examples re-run the full verification machinery
**ASN-0091, "Worked Example" through "Worked Example — Bijection Non-Uniqueness"**: Examples 2–4 each open by deferring to the first — "every other RE-* claim and every RA-adm clause discharge as in the first Worked Example, with R-SPERM in place of R-PPERM"; "everything else discharges as in the first Worked Example's pattern."
**Problem**: This is the anti-bloat pattern of multiple sections deferring to the same location. The genuine *deltas* each example adds are small and identifiable: Example 2 = the μ-region displacement (4-cut), Example 3 = R-EXT firing on a non-empty exterior, Example 4 = within-block bijection freedom. But each restages a full concrete arrangement, a full RA-adm sweep, and full RE-* verification that duplicate Example 1 verbatim in shape. The precise reader must skip the duplicated machinery to reach the one new fact.
**Required**: Keep Example 1 as the comprehensive trace. Reduce Examples 2–4 to their stated deltas (the displacement, the exterior fixity, the two-witness uniformity) without re-deriving the shared claims.

### Issue 2: Rationale prose explaining proof strategy rather than advancing it
**ASN-0091, "REARRANGE_K Realises the Abstract Class" (arrangement-dependent invariants paragraph)**: "care is required about exactly which theorem ASN-0047 supplies. ASN-0047's only single-step preservation theorem, ExtendedTransitionInvariants, covers P3 alone — not this package. Its ExtendedReachableStateInvariants is keyed to *reachability* … We therefore cannot conclude these invariants at Σ' merely from their holding at an arbitrary invariant-satisfying Σ."
**Problem**: This is meta-prose narrating the author's deliberation about which lemma to cite, rather than the argument itself. The load-bearing content is one sentence: discharge S3★/S3★-aux/CL-OWN/CL-UNIQ/S8★ by extending reachability across the step and applying ExtendedReachableStateInvariants at Σ'. The surrounding "care is required / we therefore cannot" framing is rationale about the presentation.
**Required**: Collapse to the operative step (extend the reachability trace by the K.μ~ composite, apply ExtendedReachableStateInvariants at the now-reachable Σ'). Drop the narration of why a naive reading fails.

### Issue 3: Defensive typing essay in "State-Component-Only Invariants"
**ASN-0091, "State-Component-Only Invariants"**: "Two logically distinct categories are gathered here, and they discharge by different routes; conflating them under a single 'holds at Σ' iff at Σ' is ill-typed, because a binary transition invariant has no truth value 'at Σ'' — it is a relation on the pair Σ → Σ'."
**Problem**: This paragraph justifies the author's *organizational choice* to split single-state predicates from binary transition invariants. The split itself is fine; the meta-justification ("conflating … is ill-typed") advances nothing about REARRANGE. The two discharge routes (frame inheritance; transition-satisfaction) can be stated directly without the apologia.
**Required**: State the two routes and their member invariants; remove the "ill-typed / no truth value at Σ'" justification.

### Issue 4: RE-proj provenance over-claims dependence on RE-cov
**ASN-0091, Claims table, RE-proj row**: Provenance "target case from RA-π + RE-cov."
**Problem**: RE-proj quantifies over an *arbitrary* endset `e`, not over stored-link endsets. The body's own derivation grounds the middle step correctly: "coverage(e) is a fixed function of the endset's spans, identical at Σ and Σ'" — i.e., coverage state-independence (ASN-0098 Definition). RE-cov is the narrower fact `coverage(Σ'.L(a).eᵢ) = coverage(Σ.L(a).eᵢ)` for `a ∈ dom(Σ.L)`, which does not apply to an arbitrary `e`. The table cites a premise the body does not (and cannot) use here.
**Required**: Change the provenance to cite coverage state-independence (ASN-0098), not RE-cov. (RE-disc's citation of RE-cov is correct — it is scoped to stored links.)

### Issue 5: Collapse-case realiser asserted without discharging its decomposition preconditions
**ASN-0091, "REARRANGE_K Realises the Abstract Class" (net-effect split / reachability paragraph)**: "In the collapse case the realiser is K.μ⁻ + K.μ⁺ with `Σ' = Σ`; reachability of Σ' is immediate from reachability of Σ (the witnessing trace is unchanged), and every invariant holds at Σ' = Σ trivially."
**Problem**: K.μ~ admissibility clause (ii) excludes the collapse case (`M'(d) = M(d)`), so K.μ~ is unavailable and the realiser falls back to a bare K.μ⁻ + K.μ⁺ pair. But K.μ⁻ *strictly contracts* and K.μ⁺ *strictly extends*; the claim that this pair can be sequenced to return `Σ' = Σ` while each elementary step meets its precondition at the intermediate contracted state is asserted, not shown. "The witnessing trace is unchanged" presumes the conclusion (that a valid `Σ → Σ` step exists).
**Required**: Either show the collapse-case K.μ⁻ + K.μ⁺ decomposition satisfies each elementary precondition at the intermediate state (yielding `Σ' = Σ`), or argue the collapse case is unreachable/excluded by REARRANGE_K's own preconditions so no realiser is owed.

## OUT_OF_SCOPE

### Topic 1: Link-subspace rearrangement semantics
**Why out of scope**: The ASN restricts REARRANGE_K to the content subspace (CS3, `S = s_C`) and correctly defers link-subspace reordering to an Open Question. This is future territory, not an error here.

### Topic 2: Reconstitution of a same-source span split across a cut
**Why out of scope**: RE-trans explicitly notes it does not establish whether two fragments *jointly reconstitute* the source span, only that each carries its origin. Flagging this as an Open Question is the correct disposition; it is a future ASN.

VERDICT: REVISE
