# Review of ASN-0112

I verified the span construction (V2's two covering cases, the TumblerSub/TumblerAdd component computations, V5's prefix-pinning and discreteness steps, V6's witness, the worked examples including the depth-divergent variant) against the foundation contracts — these all check out. Two issues remain.

## REVISE

### Issue 1: V9's biconditional has an unproven direction
**ASN-0112, "The origin is permanent; the extent is a function of the extremes" (V9), and the V9 table entry**: "A composition change — adding or removing occupied positions — moves the span *iff* it moves an extreme, and it need not."

**Problem**: Only one direction of the "iff" is discharged in general. The direction *span moves ⟹ extreme moved* follows from the function-of-extremes claim (contrapositive: extremes fixed ⟹ span identical), and the section establishes this. The converse — *an extreme moves ⟹ the span moves* — is demonstrated only in the single-subspace regime, via the dense-run identity (any change to `n_s` moves `max O(d)` and with it the final component of `extent_d`). In the cross-subspace regime the section exhibits only the negative examples (extremes standing, span fixed). A cross-subspace change that *does* move an extreme — say a link-side extension moving `max O(d)` from `[s_L,…,n_L]` to `[s_L,…,n_L+1]` — is claimed to move the span, but this requires injectivity of the map `(min O(d), max O(d)) ↦ (origin_d, extent_d)`, which is never argued. The min component is immediate (`origin_d = min O(d)`), but recovering `max O(d)` from `(origin_d, extent_d)` at fixed origin is a genuine multi-step argument: `shift(·, 1)` is injective within a depth (TS2) and depth-preserving, so distinct maxima give distinct reaches; then distinct reaches must give distinct extents, which needs a case split — when `#origin_d ≤ #reach_d` the D1 round-trip recovers `reach_d` from `origin_d ⊕ extent_d`, but when `#origin_d > #reach_d` the round-trip fails (D0) and recovery must go componentwise through TumblerSub's formula, using zero-freeness of `reach_d = shift(max O(d), 1)` (S8a) to rule out zero-padded-equal collisions across different reach depths. "X follows from Y" is a claim, not a proof; here the claim isn't even stated — the direction is silently absorbed into "iff."

**Required**: Either (a) prove the converse direction: show the extremes-to-span map is injective, with the depth case split above (the statement is true — the argument closes), or (b) weaken the claim to the directions actually established: extremes fixed ⟹ span identical (unconditional), and in the single-subspace regime every composition change moves the span (via the `n_s` identity), leaving the cross-subspace converse unasserted.

### Issue 2: V12 cites V8 for a fact V8 does not state
**ASN-0112, "What the caller learns beyond the name" (V12)**: "because `d` is fixed for the life of the document (V8) while the result is recomputed against the present state"

**Problem**: V8 is origin permanence — `origin_d = [s_C,1,…,1]` while the content subspace is non-empty. It says nothing about the fixity of the document identity `d`. The permanence of `d` itself is an entity-model fact (document addresses persist across all transitions — P1, EntityPermanence, ASN-0047), not a consequence of this ASN's V8. As written, the citation makes V12's information-gain contrast rest on the wrong premise.

**Required**: Cite P1 (ASN-0047) for the fixity of `d`, or drop the parenthetical and let `d`'s invariance stand as the trivial observation that it is the query's fixed argument.

## OUT_OF_SCOPE

### Topic 1: Composition of the whole-document span from per-run bounding spans
**Why out of scope**: The ASN correctly lists this in Open Questions; relating the global extent to correspondence-run-local spans is new territory (a future ASN over S8★'s run decomposition), not a defect in this boundary-query specification.

VERDICT: REVISE
