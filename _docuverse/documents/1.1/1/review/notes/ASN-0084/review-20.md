# Review of ASN-0084

## REVISE

### Issue 1: Integer-valued displacement Δ extends foundation without formalization
**ASN-0084, PermutationDisplacement / R-DISP**: "Δ(v) = ord(π(v)) − ord(v) (an integer, possibly negative)"
**Problem**: The foundation (ASN-0034) provides NAT-sub as a *partial* operation defined only when `m ≥ n`. The β displacement `−(w_α + w_μ)` is always negative, and the μ displacement `w_β − w_α` is negative whenever `w_β < w_α`. The ASN tacitly extends to ℤ without defining the integer carrier or its operations. The R-DISP proof for "4-cut β" computes `ord(c₀) − ord(c₂)` where `ord(c₀) < ord(c₂)`, which NAT-sub cannot discharge.
**Required**: Either restate Δ as a signed magnitude pair `(±, n) ∈ {+,−} × ℕ` definable over the foundation, or explicitly introduce ℤ with an "extends-NAT" lemma. Each negative case in R-DISP must be re-derived against whatever the chosen formalization licenses.

### Issue 2: "Block" reinvents "correspondence run" from foundation
**ASN-0084, Block definition**: "A *block* is a correspondence run (v, a, n) with n ≥ 1"
**Problem**: ASN-0036 S8 already names this concept "correspondence run" and exports it as the unit of S8's decomposition. The ASN's BlockDecomposition (B1, B2, B3) likewise restates S8(a) (which combines B1+B2 via E! quantification) and S8(b) (B3) under new labels. Per the standards, "if an ASN invents its own notation for something a foundation already defines, flag it as a REVISE item." The ASN should use the foundation vocabulary, not parallel it.
**Required**: Replace "block" with "correspondence run" throughout, and discharge B1/B2/B3 into S8's existing (a)/(b) clauses. Split, Merge, and CanonicalBlockDecomposition can stand as new operations layered on the existing concept.

### Issue 3: R-PRE(vi) categorization confused
**ASN-0084, R-PRE(vi)**: "Subspace confinement: all cuts and all resulting positions remain within subspace S. At depth 2, this is satisfied automatically when all cut ordinals are positive..."
**Problem**: A precondition that holds automatically given the other clauses is not a precondition — it is a consequence. As written, it is unclear what (vi) constrains beyond CS3+CS4+S8a, and a reader cannot tell whether they have a verification obligation. This conflates derived facts with assumptions.
**Required**: Either remove (vi) and add a separate "Consequences of R-PRE" paragraph deriving subspace confinement from CS3+CS4+S8a, or replace (vi) with the actual non-derivable obligation it intends to capture.

### Issue 4: ord(v) at depth 2 implicitly identified with a natural number
**ASN-0084, State and Vocabulary**: "We write c₀ + j for the V-position [S, ord(c₀) + j]"
**Problem**: ASN-0036's OrdinalExtraction returns ord(v) = [v₂] — a single-component tumbler, not a natural number. The expressions "ord(c₀) + j", "ord(v) − k", "ord(c₁) = ord(c₀) + w_α" used throughout the ASN treat ord(·) as ℕ-valued. This identification is never formalized, yet it is the foundation on which every displacement computation rests.
**Required**: State explicitly that at depth 2 the ASN identifies the singleton tumbler [n] with n ∈ ℕ, with a one-line justification (e.g., a singleton tumbler is determined by its single component, and addition/subtraction on these singletons coincides with NAT-* via TumblerAdd's action-point machinery), and either prove or cite the equivalence.

### Issue 5: Maximal block construction (step a) implicitly uses D-CTG
**ASN-0084, CanonicalBlockDecomposition step (a)**: "r(v) = max{k ≥ 0 : [S, ord(v) − k] ∈ V_S(d) ∧ (A i : 0 ≤ i ≤ k : M(d)([S, ord(v) − k + i]) = shift(M(d)([S, ord(v) − k]), i))}"
**Problem**: For the inner conjunct to be well-formed, M(d) must be defined at every [S, ord(v) − k + i] for 0 ≤ i ≤ k. The membership clause checks only [S, ord(v) − k] ∈ V_S(d). The intermediate positions are in V_S(d) only because D-CTG/D-SEQ guarantees the contiguous range from ord(v) − k to ord(v) is fully populated. This is invoked nowhere in the construction.
**Required**: Add an explicit step: "[S, ord(v) − k] ∈ V_S(d) and v ∈ V_S(d), with D-SEQ giving V_S(d) = {[S, j] : 1 ≤ j ≤ N}, so all intermediate [S, ord(v) − k + i] ∈ V_S(d) for 0 ≤ i ≤ k." Without this, the predicate inside max is not licensed.

### Issue 6: Phase 1 of R-BLK does not handle c_{n−1} ∉ V_S(d)
**ASN-0084, R-BLK Phase 1**: "For each cut position cᵢ, if cᵢ falls in the interior of some block bₖ ... split bₖ at the offset c = ord(cᵢ) − ord(vₖ)."
**Problem**: The ASN explicitly permits c_{n−1} to lie outside V_S(d) ("the last cut c_{n−1} serves as an exclusive upper bound and need not belong to V_S(d)"). When c_{n−1} > max(V_S(d)), it falls in no block and the conditional is silently false. The proof never states that this is intentional or how it interacts with subsequent classification — Phase 2 classifies blocks "lying entirely within one region" and the right-exterior region {v : v ≥ c_{n−1}} is empty in this case. A reader cannot tell whether this falls under Phase 2 by vacuous reasoning or whether it requires a separate case.
**Required**: Add an explicit case-split in Phase 1: "if cᵢ ∉ ⋃_k V(bₖ), no split is performed; this can occur only for c_{n−1} when c_{n−1} > max(V_S(d)), and in that case the right-exterior region is empty." Verify Phase 2 classification handles the empty right-exterior consistently.

### Issue 7: "Structurally identical" generalization to depth > 2 is hand-waved
**ASN-0084, State and Vocabulary**: "generalization to deeper ordinals is structurally identical by D-CTG-depth (ASN-0036), which reduces contiguity at any depth m ≥ 3 to contiguity of the last component alone."
**Problem**: D-CTG-depth establishes that components 2 through m−1 are shared within V_1(d) at depth m. It does not establish that the cut-point algebra, the displacement formulas, or R-COMM and R-BLK transfer wholesale. In particular, link subspace V_2(d) is exempt from D-CTG entirely (per D-CTG's frame). "Structurally identical" is precisely the kind of one-line claim the standards forbid.
**Required**: Either (a) restate the depth-2 restriction as a strict scope boundary with no claim of generalization, leaving deeper depths to a future ASN, or (b) carry out the reduction explicitly for at least one non-text subspace and depth m = 3, showing that each lemma transfers.

### Issue 8: "FiniteSpanDecomposition" is not the foundation label
**ASN-0084, Block Decomposition Transformation section**: "We recall from S8 (FiniteSpanDecomposition, ASN-0036) that the arrangement M(d) admits a finite decomposition into correspondence runs."
**Problem**: ASN-0036's S8 is labeled "SpanDecomposition", not "FiniteSpanDecomposition". Foundation references must match the actual labels.
**Required**: Correct to "S8 (SpanDecomposition, ASN-0036)".

### Issue 9: Title does not reflect content
**ASN-0084, title**: "Bundle Projection Displacement"
**Problem**: The phrases "bundle" and "projection" appear nowhere in the body; the only relevant noun is "displacement" via R-DISP. The actual content is cut-point rearrangements and their effect on correspondence-run decomposition. The introductory paragraph likewise frames the ASN as extending ASN-0053 (Span Algebra), but the proofs rely almost exclusively on ASN-0036 (Strand Model) and ASN-0034 (Tumbler Algebra). A reader seeking properties about spans will find none.
**Required**: Rename to something accurate (e.g., "Cut-Point Rearrangements" or "Arrangement Permutation by Cut Points") and rework the introduction to position the ASN against ASN-0036, not ASN-0053.

## OUT_OF_SCOPE

### Topic 1: Composition of rearrangements
**Why out of scope**: The ASN treats single rearrangements. Whether the composition of two rearrangements is itself a rearrangement (and what its cut sequence is) is genuinely new territory and warrants its own ASN. The Open Questions section already flags this.

### Topic 2: Generalization to k-cut for k > 4
**Why out of scope**: Open Questions explicitly leaves this as future work. The 3-cut and 4-cut cases are sufficient as a beachhead.

### Topic 3: Connection to user-level editing operations (INSERT, DELETE, COPY)
**Why out of scope**: The ASN defines pivot/swap as primitives. Mapping to user-level editing operations belongs in a separate ASN that bridges the operations layer to the rearrangement primitives.

### Topic 4: Behavior under links (subspace 2)
**Why out of scope**: The ASN restricts attention to text subspace S = 1 implicitly throughout most arguments. Link subspace handling — particularly under D-CTG's exemption — is non-trivial and orthogonal to the cut-point algebra established here.

VERDICT: REVISE
