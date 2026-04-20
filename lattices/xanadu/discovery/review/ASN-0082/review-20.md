# Review of ASN-0082

## REVISE

### Issue 1: D-SEQ-post not derived for contraction
**ASN-0082, Post-Contraction Shift — Invariant preservation**: The contraction proves D-CTG-post, D-MIN-post, S8-depth-post, S8a-post, S8-fin-post, S2-post, S3-post, and S7-post, but does not derive D-SEQ-post.
**Problem**: The insertion shift section explicitly identifies D-SEQ as violated ("D-SEQ (SequentialPositions) is likewise violated, since V_S(d) is no longer {[S, 1, ..., 1, k] : 1 ≤ k ≤ n} for any n"). The contraction restores the sequential structure — the proof of D-CTG-post demonstrates that L ∪ Q₃ = {[S, k] : 1 ≤ k ≤ N − c}, which is exactly the D-SEQ form — but this is never stated as a lemma. The asymmetry leaves the reader wondering whether D-SEQ is also broken by contraction. Moreover, the statement registry has no D-SEQ-post entry, leaving a gap in the invariant preservation story.
**Required**: Add a D-SEQ-post lemma: "When the post-state V_S(d) is non-empty, V_S(d) = {[S, k] : 1 ≤ k ≤ N − c}." The derivation is immediate from D-CTG-post (contiguity), D-MIN-post (minimum at [S, 1]), and S8-depth-post (depth 2), following the same reasoning as the original D-SEQ in ASN-0036. Add the corresponding entry to the statement registry.

### Issue 2: OrdinalAdditiveCompatibility stated for general depth, proved only at depth 2
**ASN-0082, Ordinal Extraction**: "**Lemma — OrdinalAdditiveCompatibility.** For a V-position p with #p = m ≥ 2 and a displacement w with w₁ = 0, #w = m, and w > 0: ord(p ⊕ w) = ord(p) ⊕ w_ord"
**Problem**: The statement quantifies over all m ≥ 2, but the proof header says "Proof at depth m = 2" and only the m = 2 case is shown. A "Lemma" conventionally carries a complete proof. The general case does hold — the same TumblerAdd component analysis (prefix copy below the action point, advance at the action point, tail copy from the displacement) yields ord(p ⊕ w) = [p₂, ..., p_{k−1}, p_k + w_k, w_{k+1}, ..., w_m] = ord(p) ⊕ w_ord for arbitrary k ≥ 2 — but this argument is not present.
**Required**: Either (a) provide the general proof (a short component-wise argument showing the result for arbitrary action point k ≥ 2 within an m-component tumbler), or (b) restrict the lemma statement to m = 2 to match the proof, noting the general case as a remark or open question. Option (a) is preferred since the argument is brief and the general result strengthens the ASN.

## OUT_OF_SCOPE

### Topic 1: Span-level contraction property (analog of I3-S)
**Why out of scope**: The insertion shift has I3-S (SpanShiftPreservation), which lifts the point-level shift to a span-level width-preservation result connecting to ASN-0053. The contraction has no corresponding span-level property. Deriving one — e.g., that a span σ = (s, ℓ) entirely within R transforms to (σ(s), ℓ) with preserved width — would strengthen the connection to the span algebra framework and complete the symmetry between the two operations. However, the contraction's point-level specification (D-SHIFT, D-BJ, D-SEP, D-DP) is complete and correct as stated; the span-level lifting is new territory.

### Topic 2: Composition and inverse properties of shift and contraction
**Why out of scope**: Insertion shift opens a gap; contraction closes one. The natural question is whether they compose to identity under appropriate conditions (shift by n at p followed by contraction of n at p recovers the original arrangement). This would formalize the inverse relationship implicit in the ASN's structure. This is new work beyond the current scope of specifying each operation independently.

VERDICT: REVISE
