# Review of ASN-0084

## REVISE

### Issue 1: R-CS3 proves redundancy, not necessity

**ASN-0084, "Necessity of CS3" / R-CS3**: "the same-subspace clause CS3 cannot be dropped without leaving the precondition unsatisfiable... the precondition is then unsatisfiable, so REARRANGE_K has no well-formed instance."

**Problem**: The lemma's own proof undercuts its necessity claim. It constructs a CS3-violating K and shows R-PRE(iv) is *unsatisfiable* for it. But an unsatisfiable precondition is benign — REARRANGE_K is partial (stated explicitly under "Partiality"), so it simply does not fire. No invariant breaks, no postcondition is violated. This is the opposite of necessity: it demonstrates that **R-PRE(iv) already rejects every CS3-violating K**, so CS3 is *redundant* for soundness, not necessary.

The proof in fact shows this is exhaustive: by CS2 any cut in a higher subspace must be the maximal cut c_{n−1} (a subspace-2 position exceeds all subspace-1 positions under T1), and then R-PRE(iv)'s range `c₀ ≤ v < c_{n−1}` swallows infinitely many subspace-1 positions against finite V_S(d). So *no* CS3-violating K can satisfy R-PRE — meaning a genuine necessity witness (a K satisfying R-PRE but breaking a postcondition) cannot exist. The section therefore cannot establish what it claims.

This also matches the reviser-drift pattern: R-CS3 reasons about a configuration that another precondition clause (R-PRE(iv), combined with CS2) already excludes. The comparison to a real necessity result (the foundation's T10a-N, which *falsifies an invariant*) is misleading — the two are not analogous.

**Required**: Either (a) cut the section, since it documents a redundancy rather than a necessity; or (b) reframe honestly — "CS3 is redundant with CS2 + R-PRE(iv): every CS3 violation is already caught as an unsatisfiable precondition" — and drop the "necessity"/"cannot be dropped" language and the T10a-N analogy.

### Issue 2: R-NS(NS-run) is stated in terms of a construction defined later

**ASN-0084, R-NS (NS-run)**: "the same triple (v_b, a_b, n_b) appears unchanged in B' = R-BLK(B)... Phase 1 of R-BLK never splits b... R-BLK carries b into B' as the unchanged triple."

**Problem**: NS-run is placed before R-BLK but its statement and proof depend on R-BLK's internal phases (B', Phase 1, the split sub-cases). To follow NS-run the reader must jump forward to a lemma that has not yet been introduced; R-BLK's Phase 2/Phase 3 then cite NS-run back, producing a forward/backward entanglement around the same downstream location. This is forward-reference accretion: the non-S handling of R-BLK has been hoisted into a prior lemma that can only refer to R-BLK by anticipation.

**Required**: Fold the non-S-run reasoning into R-BLK where B' and the phases exist (R-NS can retain the genuinely standalone NS-π pointwise-identity claim), so each claim is readable in place without a forward jump.

### Issue 3: Redundant restatement of the operation's frame/postconditions

**ASN-0084, "Operation — REARRANGE_K" (second paragraph)**: "REARRANGE_K has precondition R-PRE(K) and runtime signature (Σ, d) ↦ Σ'. The intra-document arrangement Σ.M(d) is the only mutated component: Σ.C, all other documents' arrangements Σ.M(d') for d' ≠ d, and the within-d non-S subspace portion of Σ.M(d) are preserved by the frame conditions; dom(M'(d)) = dom(M(d)) is asserted by the postconditions."

**Problem**: This paragraph re-summarizes the precondition (already given one paragraph above), the signature, and the frame conditions R-FRAME-P/R-FRAME-S(a)–(c) (C preserved, other documents preserved, non-S preserved) plus dom equality — all already stated normatively. It adds no new content; it is the "two paragraphs saying the same thing" / use-site-summary pattern.

**Required**: Delete the paragraph; the frame conditions and postconditions are already normative.

## OUT_OF_SCOPE

### Topic 1: Operational recovery of the maximal (canonical) partition from B′

R-BLK correctly produces a *valid* (non-maximal) partition and defers the merge-reduction to the S8-unique maximal decomposition, with Open Question 6 asking for the recovery process and its confluence. This is appropriately deferred — the existence/uniqueness of the maximal partition is borrowed from foundation S8, and the constructive reduction belongs in a future ASN. Not a defect.

### Topic 2: k-cut rearrangements for k > 4 and composition of rearrangements

Open Questions 1–2 raise generalization beyond 4 cuts and whether composed rearrangements stay within the class. These are new territory, not gaps in the present three-/four-cut treatment.

VERDICT: REVISE
