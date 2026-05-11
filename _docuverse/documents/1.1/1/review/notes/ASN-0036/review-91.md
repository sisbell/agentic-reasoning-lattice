# Review of ASN-0036

## REVISE

### Issue 1: D-SEQ Step 3 does not explicitly verify that the constructed intermediate w satisfies S8a

**ASN-0036, D-SEQ proof, Step 3 (contiguity of k-values)**: "For any integer k with k₁ < k < k₂, the tuple w = [1, 1, …, 1, k] satisfies subspace(w) = 1, #w = m, and v₁ < w < v₂..."

**Problem**: The proof verifies subspace, depth, and order, but not S8a. Since D-CTG's conclusion places w ∈ V_1(d) ⊆ dom(M(d)), and every member of dom(M(d)) satisfies S8a, the proof's "by D-CTG, w ∈ V_1(d)" step needs w to satisfy S8a — otherwise the immediate contradiction is with S8a, not (as the proof intends) with S8-fin. The verification is straightforward (k > k₁ ≥ 1 forces every component of w ≥ 1, so zeros(w) = 0; #w = m ≥ 2 by S8a on v₁), but it is left implicit. D-CTG-depth's analogous construction explicitly verifies S8a; D-SEQ Step 3 should be parallel.

**Required**: Add one sentence verifying that w satisfies S8a — citing k > k₁ ≥ 1 for the last component and the leading 1's for the rest — before invoking D-CTG.

### Issue 2: D-SEQ Step 1 (m = 2 case) does not justify why component 1 equals 1

**ASN-0036, D-SEQ proof, Step 1, Case m = 2**: "Every position has exactly two components: the subspace identifier 1 at component 1, and a single ordinal at component 2."

**Problem**: The claim "subspace identifier 1 at component 1" relies on v₁ = 1 for every v ∈ V_1(d), which follows from the definition V_1(d) = {v ∈ dom(M(d)) : subspace(v) = 1} and subspace(v) = v₁ — but this routing is left implicit. The m ≥ 3 branch routes through D-MIN (which fixes the shared prefix at all-1s); the m = 2 branch should similarly cite either D-MIN or the definition of V_1(d) so the reader doesn't need to reconstruct the chain.

**Required**: Add a phrase noting that v₁ = 1 for every position in V_1(d) by the definition of subspace 1 (or, equivalently, by D-MIN evaluated at the m = 2 case).

VERDICT: REVISE
