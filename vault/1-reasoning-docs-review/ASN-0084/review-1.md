# Review of ASN-0084

## REVISE

### Issue 1: Pervasive cross-ASN references to non-foundation ASNs
**ASN-0084, State and Vocabulary; postconditions; R-BLK**: References include "Σ = (C, E, M, R) per ASN-0047", "K.μ~ admits a bijection", "B1–B3 (ASN-0058)", "M4 (SplitDefinition, ASN-0058)", "M5 (SplitPartition)", "M6f (SplitFrame)", "M7 (MergeCondition, ASN-0058)", "M12", "M16", "M-aux convention (ASN-0058)".
**Problem**: ASN-0047 and ASN-0058 are not foundation ASNs. The ASN references them at least twelve times for state definitions, the M-aux arithmetic convention used in every postcondition clause, and the entire block decomposition vocabulary on which R-BLK depends. The ASN is not self-contained.
**Required**: (a) Drop ASN-0047: C and M(d) are defined in ASN-0036 (foundation). E appears only in R-PRE(i) "d ∈ E\_doc" — reformulate as "M(d) is well-defined" or "V\_S(d) is non-empty" (already R-PRE(ii)). R (provenance) is never used. K.μ\~ is motivational context — the postconditions define M'(d) directly. (b) Drop ASN-0058: define the ordinal increment convention directly — at depth 2, `c₀ + j = [S, p + j]` where `c₀ = [S, p]`, via repeated TA5(c) (ASN-0034), with `c₀ + 0 = c₀` by identity. For R-BLK, either restate the needed block decomposition definitions (B1–B3, split, merge) or defer R-BLK to a future ASN that can cite ASN-0058 as a foundation.

### Issue 2: Postconditions undefined outside the target subspace; frame conditions missing
**ASN-0084, PivotPostcondition / SwapPostcondition**: "dom(M'(d)) = dom(M(d))"
**Problem**: R-EXT covers "v ∈ V\_S(d) with v < c₀ or v ≥ c₂" — positions in subspace S only. R-P1/P2 (or R-S1/S2/S3) cover the affected range, also in subspace S. Together these define M'(d) on V\_S(d) but not on dom(M(d)) \ V\_S(d). If the document has positions in other subspaces (e.g., subspace 2 for links), M'(d) is undefined there, yet the postcondition claims `dom(M'(d)) = dom(M(d))`. Additionally, no frame conditions are stated for other documents or the content store.
**Required**: (a) Extend R-EXT or add a frame clause: "For v ∈ dom(M(d)) with subspace(v) ≠ S: M'(d)(v) = M(d)(v)." (b) State the remaining frame: "For all d' ≠ d: M'(d') = M(d')." and "C' = C" (S0, ASN-0036).

### Issue 3: R-SWP proof deferred to R-PIV without showing work
**ASN-0084, R-SWP**: "Identical in structure to R-PIV."
**Problem**: R-PIV explicitly computes ordinal ranges for R-P1 and R-P2, verifies their disjointness (w\_β ≥ 1 separates them), and shows their union tiles [c₀, c₂). R-SWP has three clause ranges instead of two but offers no parallel argument — just "identical in structure." The tiling is sketched above R-SWP (in the swap postcondition section), but part (a) of R-SWP — that every v ∈ V\_S(d) falls under exactly one clause — is never established with explicit ordinal ranges and disjointness checks.
**Required**: Show the partition of V\_S(d) into the four clause domains (R-EXT, R-S1, R-S2, R-S3) with ordinal ranges and pairwise disjointness, paralleling R-PIV's treatment.

### Issue 4: R-BLK commutativity proof — missing premise and dismissed cases
**ASN-0084, R-BLK Phase 3**: "The argument is identical for β, μ, and exterior regions."
**Problem**: Two gaps. First, the commutativity claim π(vⱼ + k) = π(vⱼ) + k requires that vⱼ + k lies in the same region as vⱼ, so that π applies the same displacement formula. This follows from Phase 1's guarantee that no post-split block straddles a cut boundary, but that guarantee is never stated as a premise of the commutativity argument. Second, only the α case (3-cut) is shown; β (displacement −w\_α) and μ (displacement w\_β − w\_α) are dismissed as "identical." The β case involves a negative ordinal displacement, which is integer subtraction — distinct from the addition in the α case and worth one line.
**Required**: (a) State the premise explicitly: "After Phase 1, every block lies in a single region, so for each block (vⱼ, aⱼ, nⱼ) and 0 ≤ k < nⱼ, positions vⱼ and vⱼ + k are in the same region and receive the same displacement." (b) Show at least the β case: π(c₁ + j + k) = c₀ + (j + k) = (c₀ + j) + k = π(c₁ + j) + k.

### Issue 5: R-BLK Phase 1 — split processing order unspecified
**ASN-0084, R-BLK Phase 1**: "For each cut position cᵢ, if cᵢ falls in the interior of some block βₖ — split βₖ..."
**Problem**: When two cut positions fall in the same block (e.g., a wide block spanning multiple regions), the first split modifies the decomposition and subsequent cuts must reference the updated blocks. The text iterates over cut positions without specifying the order or acknowledging that earlier splits affect later ones. The correctness relies on processing cuts in index order (ascending by CS2), so each split refines exactly one block and later cuts fall in a resulting piece or at a new boundary.
**Required**: State that cuts are processed in index order against the progressively updated decomposition. Note that CS2's strict ordering guarantees each later cut falls in the right-hand piece (or at a boundary) of an earlier split, so the process is well-defined.

### Issue 6: R-BLK — reassembled block contiguity not established
**ASN-0084, R-BLK Phase 3**: "Coverage (B1) and disjointness (B2) follow from π being a bijection."
**Problem**: This one-liner establishes that image positions are disjoint and covering but does not establish that each reassembled block (π(vⱼ), aⱼ, nⱼ) occupies a *contiguous* V-position range — needed for these objects to be blocks, not arbitrary position sets. Contiguity follows from the uniform-displacement property (π shifts all positions in a region by the same ordinal constant, so consecutive positions map to consecutive positions), but this step is implicit.
**Required**: Add: "Within each region, π applies a uniform ordinal displacement. By the commutativity π(vⱼ + k) = π(vⱼ) + k, consecutive V-positions in the original block map to consecutive V-positions, so each reassembled block is a contiguous range."

## OUT_OF_SCOPE

### Topic 1: Generalization beyond depth-2 V-positions
**Why out of scope**: The ASN explicitly restricts to depth-2 and notes that D-CTG-depth (ASN-0036) makes generalization structurally identical. The deeper case is a presentation extension, not an error in this ASN.

### Topic 2: k-cut rearrangements for k > 4, and rearrangement composition
**Why out of scope**: Both are listed as open questions in the ASN. The 3- and 4-cut cases are the primitives defined here; generalization is new territory.

VERDICT: REVISE
