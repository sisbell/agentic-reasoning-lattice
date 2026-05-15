# Review of ASN-0058

The proofs in this ASN are detailed and the structural arguments hold up under examination. I worked through each claim against its dependencies and the foundation ASNs. Below are my findings.

## REVISE

None.

I verified the key proofs in detail:

- **M-int (TumblerIntervalCharacterization)** correctly handles both `#t < m` (impossible via T1(ii) and divergence at j₀ ≤ #t < m) and `#t ≥ m` (prefix agreement via min-divergence argument). The Component-m reduction's case split on `k = 0` vs `k ≥ 1` properly handles TumblerAdd's positivity precondition via OrdinalShiftBase.
- **M2** translates S8(a) to B1+B2 via the V-extent ⟷ interval equivalence; both inclusions are explicit (forward via TumblerAdd direct, reverse via M-int) and the reverse does not invoke B1/B2 (no circularity).
- **M7-cov** correctly applies M-int to exclude V-overlap, with the `k = 0` case ruled out by the strict `v₁ < v₂` hypothesis.
- **M12a** Partition corollary's right-then-left extension preserves the necessary conditions; the unit-shift injectivity argument at the equal-component step is sound (matches TS2 with n=1).
- **M12b** No-right and no-left extension arguments correctly establish merge condition violations via M-aux re-bracketing.
- **M16a** Origin invariance is established via the action-point analysis: zeros of `a + k` at indices `< #a` coincide with zeros of `a`, the third separator stays at position `z₃ < #a`, and T3 closes the structural decomposition equality.
- **C0** rules out `k < m` via T0(a)'s unbounded last-component, contradicting S8-fin through the wⱼ family construction.
- **C0a** correctly handles both depth cases through divergence-position analysis at the j₀-position.
- **C1a** Generalization of M11/M12 to arbitrary finite partial functions with common depth ≥ 2 is correct: M-int applies under the dom(f) ⊆ dom(M(d_s)) inclusion, and the substitution of S8-depth by the common-depth assumption is local to one inferential step.
- **C2** Cardinality argument is correct via partition + M0 width coupling.

Edge cases (empty decomposition, singleton blocks, n=1 in M0, c=1 in M4, single-source content reference) are handled.

The bidirectional `M7` proof handles all three failure modes of merge (V-non-adjacency with gap, I-non-adjacency, and V-overlap via M7-cov). The frame conditions (M6f, M7f, M15(b)) are stated and verified at the right level.

## OUT_OF_SCOPE

None to add. The ASN's own Open Questions section appropriately defers:
- I-space discontinuity structure at canonical-decomposition boundaries
- Lattice structure of equivalent decompositions
- V-extent / block-count relations
- V-start vs I-start depth relations within a block (M0 depth coupling open question)
- Multi-source resolution ordering preservation

These are genuine future-ASN territory.

VERDICT: CONVERGED
