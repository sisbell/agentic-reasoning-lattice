# Review of ASN-0100

This is an unusually thorough and disciplined ASN. The three-effect decomposition (allocation/placement/shift), the substrate-composite realization under ValidComposite★, the explicit per-state vs. composite-boundary invariant verification, the careful disclaiming of ASN-0082's I3-V/I3-CS/I3-CX, and the three worked examples (interior with full projection trace, append, empty) together meet the depth standards (concrete examples, two non-trivial wp computations, derived corollaries, multi-step derivations). The boundary cases the review mandates — position 0, append, empty document — are all handled, and the K.μ⁻-omission case analysis (i.a forced-by-precondition, i.b forced-omission, ii canonical-choice) is correctly partitioned with the forced/choice distinction drawn precisely. I verified the interior worked example's projection arithmetic (`coverage(e_1) = [a_2, a_5)`, pre-projection `{[1,2],[1,3],[1,4]}`, post `{[1,2],[1,5],[1,6]}`) and the S8★ block-merge reasoning; both hold.

I found one concrete defect.

## REVISE

### Issue 1: OrdinalShiftBase misattributed to ASN-0034

**ASN-0100, §Verifying the Invariants → Arrangement functionality (S2), "Left ∩ Insertion = ∅" bullet**: "The component arithmetic splits on `k`, since `δ(k, m_C)` is defined only for `k ≥ 1` (OrdinalDisplacement, ASN-0034). For `k = 0`, OrdinalShiftBase (ASN-0034) gives `shift(p, 0) = p`..."

**Problem**: The `shift(t, 0) := t` convention is `OrdinalShiftBase`, which is an ASN-0058 convention (and is correctly cited as "(ASN-0058)" everywhere else in this ASN — the Notational convention paragraph, §Sequential text-subspace structure, §Post-state V-position well-formedness). ASN-0034's `OrdinalShift` is, by the ASN's own statement, "defined only for `n ≥ 1`." So this proof step appeals to ASN-0034 for a fact ASN-0034 does not contain; the `k = 0` final-component computation `(shift(p,0))_{m_C} = p_m` rests on an unsupported citation. The disjointness argument is the load-bearing step securing S2 functionality on the Insertion region, so the citation must be exact.

**Required**: Change "OrdinalShiftBase (ASN-0034)" to "OrdinalShiftBase (ASN-0058)" in this bullet. (The adjacent "OrdinalDisplacement, ASN-0034" and "OrdinalShift definition ... (ASN-0034)" citations are correct and need no change.)

## OUT_OF_SCOPE

None. The §Bounding the Scope exclusions (link-subspace insertion, COPY, DELETE, REARRANGE, version creation, BEBE) match the stated scope. The INSERT-vs-COPY section discusses COPY only to fix INSERT's identity character without specifying COPY mechanics, and the identity corollaries (INS.identity.crossdoc/.version/.tightsurv) are genuinely INSERT allocation properties rather than version or copy semantics, so they are in scope.

VERDICT: REVISE
