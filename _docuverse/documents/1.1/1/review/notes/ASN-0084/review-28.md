# Review of ASN-0084

## REVISE

### Issue 1: dom(M(d)) vs V_S(d) conflation in canonical decomposition

**ASN-0084, Correspondence-Run Decomposition Transformation, step (a)**: "By D-SEQ (ASN-0036), V_S(d) = {[S, 1], ..., [S, N]} for some N ∈ ℕ (the maximum ordinal in V_S(d), finite by S8-fin), and dom(M(d)) = V_S(d) under the text-subspace scope (S = 1)."

**Problem**: The ASN itself acknowledges in R-FRAME-P(a) and R-PIV that dom(M(d)) contains positions in subspaces other than S. The equation `dom(M(d)) = V_S(d)` is false in general — link-subspace positions inhabit dom(M(d)) per ASN-0036's S8a. The canonical-decomposition argument is about runs within V_S(d), not the whole dom(M(d)).

**Required**: Restate as "we analyze the maximal runs whose V-positions lie in V_S(d)" or similar. The argument then proceeds unchanged, since non-S runs are unaffected by REARRANGE.

### Issue 2: Existence-of-maximum hand-wave

**ASN-0084, canonical decomposition step (a)**: "existence of a maximum follows from NAT-wellorder (applied to its complement within the bound) — equivalently, every non-empty bounded subset of ℕ has a maximum."

**Problem**: NAT-wellorder gives least elements, not maxima. The aside "applied to its complement within the bound" is the correct intuition but is not a derivation. Reviewers and downstream consumers cannot reconstruct the proof from this remark.

**Required**: Make the derivation explicit, e.g., "For S ⊆ {0, ..., B} non-empty, the set T = {B − s : s ∈ S} is a non-empty subset of {0, ..., B}, so by NAT-wellorder T has a least element m ∈ ℕ. Then B − m ∈ S and B − m ≥ s for all s ∈ S, so max(S) = B − m exists." Apply this once and cite it for both f(v) and r(v).

### Issue 3: Partition property not shown maintained through merges

**ASN-0084, canonical decomposition step (c)**: "Partition disjointness... forces b = c. Under b = c, we have v_c = v_b and n_c = n_b..."

**Problem**: The merge process starts from a partition (S8) and merges pairs. The argument relies on the current state being a valid partition (pairwise disjoint V-extents covering dom(M(d))), but this is never derived. A single merge step replaces two adjacent runs with one; the resulting collection must still be a partition for the disjointness argument to apply.

**Required**: Add a one-paragraph invariant: "At each step of the merge process, the current collection is a partition of dom(M(d)) into valid runs. Initially this holds by S8. Each merge replaces two runs b₁, b₂ with a single run b₁₂ whose V-extent is V(b₁) ∪ V(b₂); validity of b₁₂ is by the Merge lemma, and disjointness from other runs is inherited because V(b₁), V(b₂) were already disjoint from them."

### Issue 4: "Strict extension" used without formal definition

**ASN-0084, canonical decomposition step (c)**: "Suppose, toward contradiction, that some run b ... is non-maximal. By the definition of maximality, b admits a strict extension as a valid correspondence run..."

**Problem**: "Strict extension" is referenced repeatedly and quoted once ("the definition of 'strict extension'"), but no formal definition is given. The reader must reconstruct it from context (V-extent strict containment plus validity).

**Required**: State the definition explicitly: "A *strict extension* of run b = (v_b, a_b, n_b) is a valid correspondence run b* = (v_s*, a_s*, n_s*) under M(d) with V(b*) ⊋ V(b)." Place this where the term first appears.

### Issue 5: Worked examples do not verify R-RI

**ASN-0084, Worked Example sections**: Both examples verify R-EXT/R-P1/R-P2 (or R-S*), the permutation, displacements, and run partitioning, but neither explicitly verifies R-RI.

**Problem**: R-RI is the load-bearing referential-integrity claim. The worked examples are the natural place to spot-check that ran(M'(d)) ⊆ dom(C') is preserved (e.g., that the post-rearrangement I-addresses A, B, C, D, E are all still in dom(C)).

**Required**: Add a one-line check per example: "R-RI: ran(M'(d)) = {A, B, C, D, E} = ran(M(d)) ⊆ dom(C) = dom(C')."

### Issue 6: Weakest-precondition analysis absent

**ASN-0084 (entire ASN)**: No formal wp analysis appears.

**Problem**: The ASN states preconditions (R-PRE) and postconditions (R-EXT, R-P*/R-S*, R-FRAME-*), and proves preservation of selected invariants (R-RI), but never formally computes wp(REARRANGE, Q) for a non-trivial post-condition Q. For Q = S8(b)-style consistency on M'(d), the wp computation is non-trivial — it requires tracking how the post-state runs decompose, which R-BLK does. Recasting this as an explicit wp would tighten the contract.

**Required**: Add a worked wp computation for one non-trivial post-condition, e.g., wp(3-cut pivot, "M'(d) admits a run partition"), showing that R-PRE plus M(d)'s having an S8 partition entails the post-state property.

### Issue 7: R-BLK's "valid but not necessarily maximal" lacks general characterization

**ASN-0084, R-BLK closing paragraph**: "The partition B' is valid but not necessarily maximal. After rearrangement, runs that were in different regions may become V-adjacent and I-adjacent, satisfying the merge condition."

**Problem**: This claim is illustrated by the second worked example (B and H merging into a width-3 run) but no general derivation characterizes *when* merges become possible. Two adjacent runs from different regions in the post-state are V-adjacent iff π lands their V-extents adjacent; they are I-adjacent iff their I-starts and widths align. The conditions on cut placement and pre-state I-addresses that produce post-state mergeability deserve explicit statement.

**Required**: Either characterize the merge conditions formally (which pre-state run pairs can become mergeable, expressed in terms of region assignment and I-address arithmetic), or scope the claim down to "B' may not be maximal; the maximal partition is recovered by applying the exhaustive-merge process to B'."

### Issue 8: Empty-exterior boundary case not traced through R-BLK Phase 1

**ASN-0084, R-BLK Phase 1**: "[The 'outside ⋃_k V(bₖ)' case] occurs only for the last cut c_{n−1} when c_{n−1} ∉ V_S(d)..."

**Problem**: The boundary configuration c_{n-1} = [S, N+1] (one past the last V-position) is admitted by R-PRE but is never traced through Phase 1. In particular: does the run containing [S, N] get split, and if so, by what? The intended answer (no split is needed because no run extends past [S, N] into a non-existent position) is correct but unstated.

**Required**: Add an explicit trace: "When c_{n−1} ∉ V_S(d), every run in V_S(d) has V-extent ⊆ {[S, 1], ..., [S, N]} ⊊ V_S(d) ∩ [c₀, c_{n−1}), so no run straddles c_{n−1}, and the 'outside ⋃_k V(bₖ)' case fires without splitting."

### Issue 9: Region-partition exhaustiveness only stated, not derived

**ASN-0084, RegionPartition definition**: "Exhaustiveness follows from every v ∈ A falling in exactly one inter-cut interval."

**Problem**: For the 4-cut case, this needs explicit case analysis on the position of v relative to c₁ and c₂. The half-open intervals [c₀, c₁), [c₁, c₂), [c₂, c₃) need to be shown both pairwise-disjoint and exhaustive on [c₀, c₃) by T1 trichotomy.

**Required**: One-paragraph derivation: "For v ∈ A = {v ∈ V_S(d) : c₀ ≤ v < c_{n−1}}, T1 trichotomy applied to (v, c₁) and (v, c₂) yields five sub-cases, all reducing to membership in exactly one of α, μ, β." This makes the exhaustiveness check inspectable.

### Issue 10: NAT-sub domain verification implicit for ordinal subtraction

**ASN-0084, Width-ordinal identities**: "w_α = ord(c₁) − ord(c₀); w_β = ord(c₂) − ord(c₁) for n = 3..."

**Problem**: NAT-sub is partial — `m − n` requires m ≥ n. The width definitions are subtractions; the ASN should explicitly discharge the m ≥ n precondition from CS2 (which gives c₀ < c₁ < c₂ < c_{n−1} under T1, hence ord(c_i) < ord(c_{i+1})).

**Required**: A single line: "By CS2 and T1, ord(c_i) < ord(c_{i+1}) for each i, so NAT-sub applies and each width is a positive natural number." This grounds the arithmetic and makes the singleton-tumbler identification more explicit at the point of use.

## OUT_OF_SCOPE

### Topic 1: Composition of multiple rearrangements
**Why out of scope**: The ASN raises this in Open Questions. Whether successive pivots/swaps compose into a single cut-point rearrangement is a legitimate downstream concern, not an error in defining a single rearrangement.

### Topic 2: k-cut generalization for k > 4
**Why out of scope**: Listed in Open Questions. The k = 3 and k = 4 cases are deliberately scoped; broader generalization is future work.

### Topic 3: Inverse operations
**Why out of scope**: A natural follow-up question (is every pivot/swap invertible by another pivot/swap?), but the ASN explicitly defines forward operations and is not undermined by deferring the inverse analysis.

### Topic 4: Cross-subspace transposition
**Why out of scope**: Explicitly excluded by the ASN's scope statement (CS3 restricts to subspace S = 1). Lifting this restriction is a separate operation.

### Topic 5: Run-count behavior under REARRANGE
**Why out of scope**: Listed in Open Questions. The upper bound on run-count change relative to cut-count is a quantitative refinement, not a correctness issue for the operation as specified.

VERDICT: REVISE
