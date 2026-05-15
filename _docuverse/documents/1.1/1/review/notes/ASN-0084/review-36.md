# Review of ASN-0084

## REVISE

### Issue 1: REARRANGE operation not explicitly defined

**ASN-0084, R-WP**: "wp(REARRANGE_C, Q) ⇐ R-PRE(C) ∧ ASN-0036-invariants(Σ, d) ∧ (B is a correspondence-run partition of dom(M(d)) under M(d))"

**Problem**: R-WP uses wp(REARRANGE_C, Q) but the ASN never defines REARRANGE_C as a state-transition operator with explicit pre/postcondition contract. The intro to "Rearrangement Postconditions" says the postcondition clauses "define the rearrangement operation," but there is no explicit OPERATION block tying R-PRE, the postcondition clauses, and frame conditions together as "REARRANGE_C : Σ → Σ' is the operation that...". The Properties Introduced table lists PivotPostcondition and SwapPostcondition as separate DEFs but no REARRANGE operation. The wp() notation requires a formal operation referent.

**Required**: Add an explicit Operation specification: "REARRANGE_C(Σ, d) is the state transition with precondition R-PRE(C) that produces Σ' satisfying PivotPostcondition (when n=3) or SwapPostcondition (when n=4)." Add this as a row in Properties Introduced.

### Issue 2: S8 corollary preservation not addressed in R-WP

**ASN-0084, R-WP**: discharges "S8(a) (uniqueness of containing run)" and "S8(b) (consistency under M'(d)) via B' = R-BLK(B)"

**Problem**: ASN-0036's S8 has a "Corollary — subspace and field-structure preservation across a run" that asserts subspace_I, zeros, and #E preservation across each run. R-WP audits S8(a) and S8(b) but never mentions this corollary. While it follows from S7b/S7c being preserved on dom(C') and ShiftPreservation (since aⱼ values are unchanged), the audit should explicitly close it.

**Required**: Add a sentence to the S8 discharge in R-WP explicitly noting that S8's corollary properties (i)–(iii) are preserved because the I-addresses {aⱼ} in B' equal those in B, and S7b/S7c hold on dom(C') = dom(C); cite ShiftPreservation.

### Issue 3: R-PPERM/R-SPERM surjectivity citation is imprecise

**ASN-0084, R-PPERM proof**: "Surjectivity: non-S positions map to themselves under the identity, and the three V_S(d) image sets cover V_S(d) (shown in R-PIV)"

**Problem**: R-PIV showed coverage of V_S(d) by the *domain clauses* of the postconditions (R-EXT, R-P1, R-P2). The image sets in R-PPERM ({v < c₀ or v ≥ c₂}, {c₀ + w_β + j : 0 ≤ j < w_α}, {c₀ + j : 0 ≤ j < w_β}) are not the same as those domain clauses; they happen to cover the same range, but this requires its own argument. R-SPERM has the analogous citation issue with R-SWP.

**Required**: Either spell out the image-coverage argument explicitly (the three subspace-S image sets equal V_S(d) \ [c₀, c₂), [c₀ + w_β, c₂), and [c₀, c₀ + w_β), whose union is V_S(d)), or recognize that surjectivity follows from injectivity on a finite set of equal cardinality.

### Issue 4: R-BLK as both lemma and function

**ASN-0084, R-WP**: "B' = R-BLK(B)"; **R-BLK header**: "R-BLK — RunDecompositionTransformation (LEMMA)"

**Problem**: R-BLK is labeled as a LEMMA but R-WP uses functional application notation R-BLK(B), treating it as a procedure. The Phases 1–3 description is constructive (split, classify, reassemble), so it does define a function from input partitions to output partitions. The dual usage should be acknowledged so readers understand that R-BLK both *proves* a transformation is valid and *names* the constructive procedure.

**Required**: At R-BLK's header, add a sentence: "R-BLK names both the lemma below and the constructive transformation (B, C, M(d), M'(d)) ↦ B' it specifies; R-WP invokes the latter via R-BLK(B)."

### Issue 5: ArrangementRearrangement definition not labeled

**ASN-0084, State and Vocabulary**: "An *arrangement rearrangement* is a state transition Σ → Σ' in which..."

**Problem**: The Properties Introduced table lists "ArrangementRearrangement DEF" but the body presents the definition as prose, without a "Definition — ArrangementRearrangement" header matching the style of CutSequence, RegionPartition, PivotPostcondition, etc. Inconsistent labeling makes the index harder to use.

**Required**: Add a "Definition — ArrangementRearrangement" header to the prose paragraph.

### Issue 6: Multiplicity preservation derivation terse

**ASN-0084, State and Vocabulary**: "the multiset of I-addresses is also preserved: since π is a bijection, for each I-address a, the preimage {v : M(d)(v) = a} is in bijection with {π(v) : M(d)(v) = a} = {u : M'(d)(u) = a}"

**Problem**: The middle set equality {π(v) : M(d)(v) = a} = {u : M'(d)(u) = a} requires both inclusions, neither of which is shown. The forward inclusion needs π(v) → satisfies M'(d)(π(v)) = M(d)(v) = a; the backward inclusion needs surjectivity of π plus the defining property. This is invoked in R-WP's S5 discharge.

**Required**: Spell out both inclusions, or note that both follow from the defining property M'(d)(π(v)) = M(d)(v) combined with bijectivity.

### Issue 7: Phase 1 "outside" case explanation could be sharper

**ASN-0084, R-BLK Phase 1**: "Outside ⋃_k V(bₖ): no split is performed. This occurs only for the last cut c_{n−1}..."

**Problem**: The argument that c₀, ..., c_{n−2} all lie inside ⋃_k V(b_k) chains together CS2, R-PRE(iv), and S8 in one sentence. Given the importance of this case analysis for Phase 1's well-definedness, it warrants a clearer separation: (i) every cut except possibly c_{n−1} lies in [c₀, c_{n−1}); (ii) R-PRE(iv) places those positions in V_S(d); (iii) S8 places them in some run.

**Required**: Restructure as three explicit steps citing CS2, R-PRE(iv), and S8 of the pre-state respectively.

## OUT_OF_SCOPE

### Topic 1: Generalization to k > 4 cut points
**Why out of scope**: Listed in Open Questions. The ASN scopes to 3-cut pivot and 4-cut swap deliberately.

### Topic 2: Composition of multiple rearrangements
**Why out of scope**: Listed in Open Questions. Single-operation specification is sufficient at this layer.

### Topic 3: Run-count change bounds across a rearrangement
**Why out of scope**: Listed in Open Questions. R-BLK acknowledges it does not characterize which pre-state run pairs produce post-state mergeability.

### Topic 4: Constraints on cut points relative to canonical run boundaries
**Why out of scope**: Listed in Open Questions. R-PRE deliberately admits arbitrary cut positions within V-span.

### Topic 5: Cross-subspace rearrangement
**Why out of scope**: Explicitly excluded by CS3 (cuts in subspace S=1 only). Belongs in a follow-up ASN treating the link subspace and beyond.

### Topic 6: Documents with m_1 > 2
**Why out of scope**: Explicitly excluded by the depth-2 scope restriction. Generalization belongs in a separate ASN.

### Topic 7: Necessity (weakest precondition) in R-WP
**Why out of scope**: R-WP explicitly claims sufficiency only and notes "Computing the weakest precondition would demand a converse argument exhibiting failure of Q whenever any conjunct is dropped, and is beyond the scope of this ASN."

### Topic 8: Maximal-partition reachability post-rearrangement
**Why out of scope**: R-BLK acknowledges B' may not be maximal and that the canonical partition is recovered by re-running the merge process. A characterization of which merges occur is deferred.

VERDICT: REVISE
