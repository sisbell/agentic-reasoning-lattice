# Review of ASN-0081

## REVISE

### Issue 1: Registry Contraction entry lists D-SHIFT as a precondition
**ASN-0081, Statement registry**: "Contraction | operation | ... preconditions: D-SHIFT; postconditions: D-SHIFT, D-DOM; frame: D-L, D-CS, D-CD, D-I"
**Problem**: D-SHIFT is a postcondition, not a precondition. The entry says "preconditions: D-SHIFT" which creates a circular reference: D-SHIFT's own preconditions section says "As stated in the contraction formal contract," pointing back to the Contraction Setup section. The registry should state the actual preconditions directly.
**Required**: Replace "preconditions: D-SHIFT" with the contraction formal contract preconditions: `p ∈ V_S(d), w > 0, #w = #p, w₁ = 0, #p = 2, containment (p₂ + w₂ − 1 ≤ N)`.

### Issue 2: S8-fin preservation missing from invariant verification
**ASN-0081, Invariant Preservation section**: "We now verify that the post-state satisfies the system invariants established in ASN-0036."
**Problem**: S8-fin (FiniteArrangement) — `dom(M(d))` is finite — is an ASN-0036 invariant that is not stated or verified. The section verifies S2-post, S3-post, D-CTG-post, D-MIN-post, S8-depth-post, and S8a-post, but omits S8-fin-post. The proof is trivial (L ⊆ V_S(d) and R ⊆ V_S(d) are subsets of a finite set; |L ∪ Q₃| ≤ |V_S(d)|; D-CS and D-CD preserve other subspaces and documents) but should be stated for completeness alongside the other invariant preservation lemmas.
**Required**: Add S8-fin-post as a lemma with the one-line argument, and add it to the statement registry.

## OUT_OF_SCOPE

*None beyond the open question the ASN already identifies (depth generalization).*

VERDICT: REVISE
