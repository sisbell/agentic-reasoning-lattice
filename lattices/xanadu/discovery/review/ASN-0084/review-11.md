# Review of ASN-0084

## REVISE

### Issue 1: Properties table label collision on PermutationDisplacement
**ASN-0084, Properties table**: Two entries share the label "PermutationDisplacement" — one DEF ("Δ(v) = ord(π(v)) − ord(v)") and one LEMMA ("Δ(v) is uniform within each region, determined by region widths alone").
**Problem**: Duplicate labels make the table ambiguous. A reader cannot cite "PermutationDisplacement" without specifying which entry they mean.
**Required**: Give the LEMMA a distinct label (e.g., "DisplacementUniformity" or "R-DISP").

### Issue 2: PermutationDisplacement uniformity — listed as LEMMA but not formally stated
**ASN-0084, Displacement Analysis section**: The displacement values are computed per region, and the text observes: "every position in the affected range shifts by a value determined solely by the region widths — the displacement does not depend on the position's location within its region."
**Problem**: The Properties table lists this as a LEMMA, but the body provides only a computation followed by an informal observation. There is no formal statement with preconditions/postconditions. For both the 3-cut and 4-cut forms, the claim that Δ is uniform within each region follows immediately from the explicit R-PPERM/R-SPERM formulas, but it should be stated once as a proper lemma that downstream work can cite.
**Required**: State the uniformity result as a formal lemma under its own label. Preconditions: a cut sequence C satisfying R-PRE and the permutation π from R-PPERM (3-cut) or R-SPERM (4-cut). Postcondition: for all v₁, v₂ in the same region, Δ(v₁) = Δ(v₂), with the common value given by the explicit formulas already present in the section.

### Issue 3: Split and Merge B3 proofs are stated for M(d) specifically
**ASN-0084, Block Decomposition Transformation section**: The Split B3 proof says "we need M(d)(v + k) = a + k"; the Merge B3 proof says "We verify B3 for the merged block — that M(d)(v₁ + k) = a₁ + k."
**Problem**: Both proofs reference M(d) in their B3 verification, but neither uses any property of M(d) beyond B3 of the constituent blocks and TS3 (shift composition). The proofs are arrangement-parametric — they work for any arrangement A under which the constituent blocks satisfy B3. The worked examples apply Merge to the post-rearrangement M'(d) without noting that the B3 proof transfers. At the 4-cut example's merge step, the text says "Merge: ([1,6], B, 3)" without justifying B3 for M'(d), relying on the reader to realize the earlier M(d)-specific proof generalizes.
**Required**: Either (a) state the B3 verifications over a generic arrangement A ("for any arrangement A satisfying B3 for blocks (v₁, a₁, n₁) and (v₂, a₂, n₂)..."), or (b) add a sentence after the Merge definition noting that the proof depends only on B3 of the constituent blocks and TS3, making it arrangement-independent. This would close the gap in the worked examples where Merge is applied to M'(d).

## OUT_OF_SCOPE

### Topic 1: Canonical decomposition — existence and uniqueness of maximally merged form
**Why out of scope**: The term "canonical decomposition" appears in the worked examples to describe the maximally merged block decomposition, but no formal definition, existence proof, or uniqueness proof is given. R-BLK produces a valid decomposition B' (before merging) and notes that further merging is possible. Formalizing the maximally merged form — showing that iterative merging terminates and yields a unique result regardless of merge order — would be new territory, not an error in this ASN.

### Topic 2: Explicit connection between Block Split/Merge and ASN-0053 span operations
**Why out of scope**: Block Split at offset c structurally mirrors S4 (SplitPartition) applied simultaneously to the V-span and I-span of a correspondence run, and Block Merge mirrors S3 (MergeEquivalence). Drawing these connections explicitly would ground the block operations in the span algebra foundation, but the current ASN is self-contained and correct without them. This belongs in a future bridge property or in ASN-0053 itself.

VERDICT: REVISE
