# Review of ASN-0084

## REVISE

(none)

## OUT_OF_SCOPE

### Topic 1: Generalization to k-cut rearrangements for k > 4
**Why out of scope**: The ASN scopes to n ∈ {3, 4} per CS1 and explicitly identifies this generalization as an open question. The natural class of permutations expressible by k-cut sequences for k > 4 (and the necessary refinements to RegionPartition, R-PPERM/R-SPERM analogues, and R-BLK Phase 2 classification) belongs in a follow-on ASN.

### Topic 2: Composition of multiple rearrangements
**Why out of scope**: Already named as an open question. Whether REARRANGE_{K₁} ∘ REARRANGE_{K₂} can be expressed as a single REARRANGE_{K₃} — and what the closure of the rearrangement family under composition looks like — requires analysis tying π-composition to cut-sequence arithmetic, which is future work.

### Topic 3: Cross-subspace rearrangements
**Why out of scope**: Explicitly scoped out via CS3. Rearrangements that move content from the text subspace to the link subspace (or vice versa) require new operational semantics — different field-correspondence, different invariants (D-CTG does not extend to the link subspace), and different ordinal arithmetic. This is a distinct operation, not a missing case of REARRANGE_K.

### Topic 4: Full weakest-precondition derivation for R-SP
**Why out of scope**: The lemma is declared sufficiency-only. The necessity sketches isolate R-PRE(iii)-CS3 (as a well-typedness guard) and R-PRE(iv) (as a semantic precondition with an exhibited counterexample), but the converse "wp(REARRANGE_K, Q) = R-PRE(K) ∧ ASN-0036-invariants" is acknowledged as open. The well-typedness/semantic distinction would itself need formalization.

### Topic 5: Characterization of post-rearrangement mergeability
**Why out of scope**: R-BLK's closing remark acknowledges that B' is valid but not necessarily canonical. Characterizing exactly which pre-state run pairs (under what cut-sequence/region-assignment conditions) produce post-state mergeability — and tying this to I-address arithmetic from the pre-state — is identified as beyond R-BLK's scope.

### Topic 6: Multi-subspace worked example
**Why out of scope**: R-NS proves non-S subspace invariance with three explicit clauses (NS-π, NS-run, NS-inv); the mechanism is sound. A worked example exhibiting REARRANGE_K on a document with concrete link-subspace V-positions would be a pedagogical addition rather than a correctness fix. The five existing examples cover the operational edge cases that matter for the text-subspace contract this ASN establishes.

### Topic 7: Constraint between cut points and run boundaries
**Why out of scope**: The fourth open question asks whether cuts must align with canonical-partition run boundaries. The current ASN allows arbitrary cut positions within the affected range; characterizing the implications of cut placement (e.g., minimizing post-rearrangement splits, optimizing partition cardinality) is future work.

VERDICT: CONVERGED
