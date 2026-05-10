# Review of ASN-0084

## REVISE

### Issue 1: ArrangementRearrangement definition omits other-document frame condition
**ASN-0084, State and Vocabulary**: "An *arrangement rearrangement* is a state transition Σ → Σ' in which dom(M'(d)) = dom(M(d)), C' = C (S0, ASN-0036), and there exists a bijection π..."
**Problem**: The definition constrains only document d and the content store. It says nothing about M'(d') for d' ≠ d. The subsequent paragraph then claims "every ASN-0036 invariant is maintained by an arrangement rearrangement." But S2 and S3 are universally quantified over all documents — an arrangement rearrangement as defined could arbitrarily corrupt M'(d') for d' ≠ d, violating S3 for those documents. The specific postconditions do include the frame condition (R-FRAME-P(b)/R-FRAME-S(b): M'(d') = M(d') for d' ≠ d), but the general definition and its invariant-preservation claim stand independently. A future ASN building on "arrangement rearrangements preserve all invariants" without the frame condition would inherit a false guarantee.
**Required**: Add `M'(d') = M(d') for all d' ≠ d` to the ArrangementRearrangement definition, or qualify the invariant preservation claim as applying to document d and C only, with other-document preservation requiring the frame condition stated in the specific postconditions.

### Issue 2: R-PPERM/R-SPERM proofs incomplete on non-S subspace positions
**ASN-0084, R-PPERM proof**: "For exterior v: π(v) = v, and M'(d)(v) = M(d)(v) by R-EXT."
**Problem**: R-EXT applies only to V_S(d) positions ("For v ∈ V_S(d) with v < c₀ or v ≥ c₂"). For v ∈ dom(M(d)) with subspace(v) ≠ S, the justification is R-FRAME-P(a), not R-EXT. The formula itself is correct — non-S positions do satisfy `v < c₀` or `v ≥ c₂` under T1 (their subspace identifier differs from S, so the first component comparison resolves before any cut position) — but the proof cites the wrong clause.

The same gap appears in the surjectivity argument: "the three image sets cover V_S(d), also shown in R-PIV." The bijection is claimed on dom(M(d)) → dom(M'(d)), but surjectivity is only argued for V_S(d). Non-S positions contribute {v ∈ dom(M(d)) : subspace(v) ≠ S} to the image under the identity; this set is disjoint from the three V_S(d) image sets and together they cover dom(M(d)). The step is trivial but absent.

The same issues apply to R-SPERM.

**Required**: In R-PPERM (and R-SPERM), the exterior verification should cite both R-EXT and R-FRAME-P(a)/R-FRAME-S(a). The surjectivity paragraph should note that non-S positions map to themselves, and the union of all image sets covers dom(M(d)), not just V_S(d).

### Issue 3: Properties table — Block DEF attributes decomposition properties to individual blocks
**ASN-0084, Properties table**: "Block | DEF | Correspondence run (v, a, n) with M(d)(v + k) = a + k for 0 ≤ k < n, satisfying B1–B3"
**Problem**: B1 (coverage), B2 (disjointness), and B3 (consistency) are properties of a *block decomposition* — a set of blocks — not of an individual block. An individual block satisfies only the correspondence-run condition M(d)(v + k) = a + k. The body text distinguishes these correctly (Block is defined separately from block decomposition), but the table conflates them. A reader consulting the table alone would misunderstand what "Block" means.
**Required**: The Block DEF entry should state only the correspondence-run condition. B1–B3 belong to a separate "BlockDecomposition" concept, or should be noted as decomposition properties in the table.

### Issue 4: Properties table — PermutationDisplacement DEF includes derived property
**ASN-0084, Properties table**: "PermutationDisplacement | DEF | Δ(v) = ord(π(v)) − ord(v): uniform within each region, determined by region widths alone"
**Problem**: The definition is Δ(v) = ord(π(v)) − ord(v). The uniformity within regions is a consequence derived from R-PPERM/R-SPERM in the body text, not part of the definition itself. Conflating definition with derived property in the table makes the DEF entry do double duty — it simultaneously defines a quantity and states a theorem about it.
**Required**: Either split into a DEF (the formula) and a separate lemma entry (the uniformity), or annotate the table entry to distinguish the definition from its derived property.

## OUT_OF_SCOPE

### Topic 1: Canonical (maximally-merged) block decomposition uniqueness
**Why out of scope**: The ASN uses "canonical decomposition" in worked examples without formally defining it or proving uniqueness. R-BLK works with any block decomposition satisfying B1–B3, so the formal results are independent of canonicality. A formal treatment of maximal merging and its uniqueness would belong in a future ASN on block decomposition theory.

### Topic 2: Generalization to V-position depth > 2
**Why out of scope**: The ASN explicitly restricts to depth-2 V-positions and notes that generalization is "structurally identical" by D-CTG-depth. A formal treatment of the general case — where ordinals are multi-component tumblers and displacement analysis requires tumbler arithmetic rather than integer subtraction — would be a separate extension.

VERDICT: REVISE
