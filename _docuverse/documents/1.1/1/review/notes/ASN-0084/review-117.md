# Review of ASN-0084

I checked the cut-point arithmetic, the two postcondition definitions, the well-definedness lemmas (R-PIV/R-SWP), the bijection proofs (R-PPERM/R-SPERM), R-COMM, R-BLK, R-CANON, and the six worked examples. The mathematics is sound: region partitioning is exhaustive and disjoint, the displacement formulas tile the affected range, the bijections are verified pointwise and closed under finiteness, and R-CANON's forward/backward extension arguments are rigorous. Boundary coverage is genuinely thorough — minimum `V_S(d)`, empty exteriors, equal/unequal/backward μ sub-cases, and a non-S pass-through are each traced concretely. My findings are confined to the forward-reference accretion this note is flagged to carry.

## REVISE

### Issue 1: Non-circularity reassurance lodged in the S8 discharge
**ASN-0084, "Invariant preservation" / Post-state S8 discharge**: "all of foundation S8's preconditions … are established in this audit (R-RI for S3), **and none of them references the pre-state run partition**, foundation S8 (ASN-0036) applies to M'(d) directly"

**Problem**: The clause "and none of them references the pre-state run partition" is a defensive non-circularity argument — exactly the "the forward pointer is non-circular by Y argument" pattern. S8 is a single-state theorem; it has no "pre-state partition" input, so the worry it preempts cannot arise. The reasoning that advances the claim is complete at "M'(d) satisfies S8's preconditions, so S8 applies." The reader must parse and discard the reassurance.

**Required**: Delete the non-circularity clause. State only that M'(d) satisfies S8's preconditions (R-RI supplying S3), so foundation S8 yields the post-state partition.

### Issue 2: R-BLK re-derives cases R-COMM already proves
**ASN-0084, R-BLK, "Same-region discharge of the commutation identity"**: "On non-S and subspace-S exterior runs the identity holds trivially (π is the identity there, so both sides equal vⱼ + k); on the displaced α/μ/β runs it is supplied by R-COMM."

**Problem**: R-COMM's statement and proof already cover *all five* region cases, including non-S and the subspace-S exterior (it proves the identity there from "π is the identity"). R-BLK re-splits the same case structure ("trivial here / R-COMM there") and re-states the exterior/non-S derivation that R-COMM owns. This duplicates R-COMM's case enumeration in different words. The same redundancy appears in the Phase-2 parenthetical "(`v < c₀` or `v ≥ c_{n−1}`, a single region as in the R-PPERM/R-SPERM formulas and R-COMM)," which re-justifies a point R-COMM already fixes.

**Required**: In the same-region discharge, cite R-COMM uniformly across all regions ("each post-split run lies in one region (Phase 2), so R-COMM gives π(vⱼ + k) = π(vⱼ) + k"). Drop the re-derivation of the trivial cases and the Phase-2 re-justification parenthetical.

## OUT_OF_SCOPE

### Topic 1: k-cut rearrangements (k > 4) and composition of rearrangements
**Why out of scope**: The note correctly fixes n ∈ {3, 4} (CS1) and lists generalization and composition as Open Questions. These are new operational territory, not defects in the pivot/swap specification.

### Topic 2: Depth m₁ > 2 in the text subspace
**Why out of scope**: The depth-2 restriction is an explicit, declared scope choice (singleton-ordinal arithmetic depends on it). Lifting it requires multi-component shift arithmetic — a separate ASN, not a gap here.

### Topic 3: Weakest precondition for the post-state invariant suite Q
**Why out of scope**: Listed as an Open Question; the invariant audit discharges each invariant directly, which is the obligation for this ASN. A wp analysis is future work.

VERDICT: REVISE
