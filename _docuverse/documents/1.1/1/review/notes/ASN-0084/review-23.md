# Review of ASN-0084

## REVISE

### Issue 1: Step (c) of canonical decomposition uniqueness compresses a multi-step argument

**ASN-0084, "Correspondence-Run Decomposition Transformation," canonical decomposition proof step (c)**: "At termination, no mergeable pair remains — every run is maximal, since a non-maximal run would have a V-adjacent, I-adjacent neighbor forming a mergeable pair."

**Problem**: The implication "non-maximal ⟹ has a mergeable partition-neighbor" requires showing that the partition run containing the hypothetical extension's first new position is itself V-adjacent and I-adjacent. The argument involves: (a) if b = (v_b, a_b, n_b) is non-maximal, it extends to a valid b'' through some v_b + n_b ∈ dom(M(d)); (b) the partition run c containing v_b + n_b must have v_c = v_b + n_b — values v_c < v_b + n_b are ruled out because the candidate position would otherwise lie in V(b), contradicting partition disjointness via S8(a); (c) a_c = M(d)(v_b + n_b) = a_b + n_b by S8(b) of b''. Without these steps, the reader cannot tell whether the neighbor is in the current partition or only hypothetically constructible.

**Required**: Expand the one-sentence claim into the explicit argument above, naming the partition run c, deriving V-adjacency from partition disjointness, and deriving I-adjacency from b'''s validity.

### Issue 2: 3-cut worked example narrative omits the second Phase 1 split

**ASN-0084, "Worked Example: 3-Cut Pivot on a 5-Position Document," run partition after rearrangement**: "The cut at [1,2] (c₀, interior to b₁ at offset 1) split the original run b₁ into ([1,1], A, 1) and ([1,2], B, 2), and the rearrangement inserted the single-element run for D between them."

**Problem**: The example's stated canonical partition includes ([1,5], E, 1) as a separate single-element run. This singleton arises only because Phase 1 of R-BLK also splits b₂ = ([1,4], D, 2) at c₂ = [1,5] (which is interior to b₂ at offset 1, separating β from the right exterior). The narrative mentions only the c₀ split. Without splitting at c₂, b₂ would span both β and the right exterior, and Phase 2's region classification (which requires each post-split run to lie in exactly one region) would not apply. A careful reader who reconstructs Phase 1 step by step will notice the omission; a casual reader may miss that two splits are required.

**Required**: Augment the narrative to note that c₂ also bisects b₂ — e.g., "The cut at [1,2] split b₁ at offset 1; the cut at [1,5] split b₂ at offset 1, separating D (in β) from E (in the right exterior)."

## OUT_OF_SCOPE

(The ASN's "Open Questions" section already enumerates the appropriate future work — k-cut generalization, rearrangement composition, run-count bounds, cut/boundary alignment. No additional items.)

VERDICT: REVISE
