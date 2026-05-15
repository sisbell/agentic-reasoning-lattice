# Review of ASN-0082

## REVISE

### Issue 1: I3 lacks an explicit S7 preservation lemma

**ASN-0082, post-insertion shift section**: The structural-preservation lemmas for I3 cover S8-depth (I3-VD), S8a (I3-VP), S3 (I3-S3), S2 (I3-S2), and S8-fin (I3-fin), but no lemma addresses S7a/S7b/S7c preservation. The contraction section, by contrast, explicitly proves S7-post.

**Problem**: The invariant suite for I3 is incomplete relative to the contraction section, and the asymmetry obscures whether structural attribution (S7) is preserved under shifting. The substance is present in the I3-C frame clause ("dom(C') = dom(C)") plus the observation that S7a/S7b/S7c are predicates over dom(C), but the conclusion is not formalized.

**Required**: Add an I3-S7 lemma stating S7a, S7b, S7c preservation post-insertion. The proof is one paragraph (S7a/b/c are predicates over dom(C); by I3-C, dom(C) and per-address values are unchanged; the predicates hold identically). The parallel to S7-post will make the invariant coverage symmetric.

### Issue 2: OrdinalOrderEquivalence proof — "same positions with the same values"

**ASN-0082, Ordinal Extraction section**: "Since #v₁ = #v₂ implies #ord(v₁) = #ord(v₂), the comparison of the ordinals under T1 examines the same positions with the same values, giving an identical outcome."

**Problem**: The phrase "same positions" is ambiguous and technically misleading. The components of ord(v) at positions 1..m−1 correspond to v's components at positions 2..m — the indices are offset by 1. The divergence position k ≥ 2 in v's comparison maps to divergence position k − 1 in the ord comparison. The conclusion is correct but the wording suggests a literal index correspondence that does not hold.

**Required**: Rephrase to make the index shift explicit. Something like: "The T1 comparison of v₁ and v₂ examines positions 2..m (position 1 agrees by hypothesis), with divergence at some k ≥ 2 where (v₁)ₖ < (v₂)ₖ. The T1 comparison of ord(v₁) and ord(v₂) examines positions 1..m−1, which carry the same values (v₁)₂..(v₁)ₘ versus (v₂)₂..(v₂)ₘ. The divergence position in the ord comparison is k − 1, and the comparison outcome is identical to that of v."

### Issue 3: Proof ordering — D-SEQ-post forward-references S8-depth-post and S8a-post

**ASN-0082, invariant preservation section**: D-SEQ-post's proof cites S8-depth-post and S8a-post ("By S8-depth-post (below)..." and "By S8a-post (below)..."), but those lemmas appear later in the document.

**Problem**: Forward references in proof chains are not circular here, but they require the reader to skip ahead and verify dependencies. The current order (S2-post → S3-post → D-CTG-post → D-MIN-post → D-SEQ-post → S8-depth-post → S8a-post → S8-fin-post → S7-post) places dependents before their premises.

**Required**: Reorder so that S8-depth-post and S8a-post appear before D-SEQ-post. The dependency graph admits the order: S8-depth-post, S8a-post, D-CTG-post, D-MIN-post, D-SEQ-post, S8-fin-post, S2-post, S3-post, S7-post.

### Issue 4: D-CTG-post boundary argument — "adjacent ordinals" claim under-justified

**ASN-0082, D-CTG-post proof**: "L's maximum ordinal is p₂ − 1 and Q₃'s minimum ordinal is p₂ (D-SEP(b)), which are adjacent, so L ∪ Q₃ is contiguous."

**Problem**: "Adjacent ordinals" plus contiguity of L and contiguity of Q₃ does not by itself establish that L ∪ Q₃ satisfies the foundation's D-CTG predicate, which quantifies over arbitrary intermediate V-positions. The proof needs to verify D-CTG's quantifier directly: for any u, q ∈ L ∪ Q₃ with u < q at depth 2, any v with u < v < q at depth 2 in subspace 1 lies in L ∪ Q₃.

**Required**: Spell out the D-CTG verification: L = {[1, k] : 1 ≤ k < p₂}, Q₃ = {[1, k] : p₂ ≤ k ≤ N − c}, so L ∪ Q₃ = {[1, k] : 1 ≤ k ≤ N − c}. For any [1, kᵤ], [1, kq] ∈ L ∪ Q₃ with kᵤ < kq, any depth-2 subspace-1 position [1, k] with kᵤ < k < kq satisfies 1 ≤ k ≤ N − c, hence lies in L ∪ Q₃. The "adjacent ordinals" justification compresses this verification.

## OUT_OF_SCOPE

### Topic 1: Span-level lift for contraction (dual of I3-S)

**Why out of scope**: I3-S provides a span-level corollary for insertion, but no analog exists for contraction. A "D-SHIFT-S" would characterize how a level-uniform span σ wholly within R transforms to (σ(start(σ)), width(σ)). This is a natural symmetric extension but is not required for the operation's correctness — the point-level postconditions suffice. Deferring is appropriate; the omission could be noted in Open Questions.

### Topic 2: Generalization to ordinals of depth > 2 for contraction

**Why out of scope**: Already flagged in the Open Questions section. The TA4 dependency makes the generalization a substantive new derivation, and udanax-green / FEBE do not require it.

### Topic 3: Composition with content placement for the full INSERT/DELETE operations

**Why out of scope**: The ASN explicitly scopes itself to the shift sub-operations. The full INSERT (which extends dom(C) with new I-addresses at the gap positions and re-derives contiguity invariants over the complete post-state) and full DELETE (which composes contraction with optional cleanup of Istream references) belong in future operation ASNs that compose with this one.

VERDICT: REVISE
