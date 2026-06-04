# Review of ASN-0087

I checked the decomposition, preconditions, the wp derivation, every invariant conjunct against ASN-0047's `ExtendedReachableStateInvariants` list, the boundary cases, and the worked example's tumbler arithmetic.

**Invariant coverage is complete.** Every conjunct of the per-state list (S2, S3★, S3★-aux, S4, S7a, S7b, C1b, C1c, S7d, S8a, S8-fin, S8-depth, S8★, C-fin, D-CTG★, D-MIN★, D-SEQ★, P6, P7, P8, NodeLineage, ActivatedEmission, L0–L1c, L3, L14, L-fin, CL-OWN, CL-UNIQ), the composite-boundary properties (P4★, P4a, P7a with J0/J1★/J1'★), and the transition invariants (M1, L12, P0–P3) is addressed — either proved directly or frame-inherited with explicit justification.

**The hard discharges hold up.** S2's two-part exclusion (within- and cross-subspace) correctly proves `v_ℓ ∉ dom(Σ.M(d))` rather than the weaker `v_ℓ ∉ V_{s_L}(d)`. D-CTG★ is proved over the full depth-`m` slice for arbitrary `m ≥ 2` (not assuming `m = 2`), which is the right move. D-MIN★ and D-SEQ★ split the empty/non-empty cases correctly.

**Boundaries are handled.** Empty endsets for `i ≠ 3` (coverage `∅`), reflexive endsets (M-Reflexive + worked-example variant), home document with no prior links vs. prior links with cleared V-subspace (the address `ℓ` and V-position `v_ℓ` are correctly decoupled — `ℓ = inc(ℓ_prev,0)` while `v_ℓ = [s_L,1]`), and `d_target ∉ dom(M)` (membership clause). The wp has a genuinely non-trivial case (Case 2's reflexive disjunct) and collapses correctly under standard authoring via M-FreshExcl.

**Worked-example arithmetic checks out.** `a₁ = [1,0,1,0,1,0,1,1]` and `ℓ = [1,0,1,0,1,0,2,1]` diverge at position 7 (`1 ≠ 2`); `a₁/a₂` diverge at position 8. Prefix tests and the `d`/`d'` discoverability split are correct.

**Derived claims carry derivations.** M-DiscSymmetry, M-PriorLinkDisc (full LP9/LP18 specialization), M-Reflexive, M-WP, and M-Perm each have explicit chains, not bare assertions.

All cross-ASN references are to foundation ASNs (34, 36, 43, 47, 53, 58, 93, 98); no non-foundation references. No notation reinvented that a foundation already supplies.

On the anti-bloat pass: the Σ_mid/protocol-layer theme is touched by the Atomicity section, the M-CompAtomicity table row, and Open Question 4, but this is prose + summary-table + forward-pointer rather than prose-prose duplication, and the Atomicity section carries a substantive argument (K.λ contributes no discoverability change). It does not rise to a flaggable accretion. The "No Permission Check" section is a one-sentence statement of what the operation does not do — explicitly not meta-prose per the guidance.

## OUT_OF_SCOPE

The four Open Questions (forward-reaching endset well-formedness, identical-endset distinctness, deferred-consistency, Σ_mid visibility bound) are correctly deferred as future territory rather than gaps in this note.

VERDICT: CONVERGED
