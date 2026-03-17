# Review of ASN-0043

## REVISE

### Issue 1: L11 non-injectivity witness — abbreviated invariant verification

**ASN-0043, Link Distinctness and Permanence, L11 non-injectivity**: "The witness is immediate: allocate a' by forward allocation within the same document's link subspace, and set Σ'.L(a') = (F, G, Θ). All invariants L0–L14 are preserved (L0 by subspace, L1/L1a by allocation, L3–L5 by construction, L12 because existing entries are unchanged)."

**Problem**: The proof claims "All invariants L0–L14 are preserved" but verifies only L0, L1, L1a, L3–L5, and L12 — six of fifteen labeled properties. Missing from explicit verification: L2 (structural), L6 (same link value preserves slot distinction), L11 uniqueness for a' (forward allocation / GlobalUniqueness), L12a (corollary of L12), L14 (disjointness of extended domain), and S0–S3 (content store and arrangements unchanged). The L9 proof, for a structurally identical construction four paragraphs later, provides the expected level of completeness — it enumerates every remaining invariant with brief justification ("L2 holds structurally... L6 vacuously... L8, L10, L13 are lemmas... L12a follows from L12"). The L11 proof should match this standard set within the same ASN.

**Required**: Either enumerate the remaining invariants with one-line justifications (e.g., "L2 holds structurally; L6: same link value, same F ≠ G status; L11 uniqueness by GlobalUniqueness; L12a follows from L12; L14: a' is in subspace s_L, preserving disjointness; S0–S3: Σ'.C = Σ.C, Σ'.M = Σ.M, trivially preserved") or forward-reference the worked example's Step 1, which verifies the identical construction comprehensively.

## OUT_OF_SCOPE

### Topic 1: Compound link well-formedness constraints

The ASN establishes reflexive addressing (L13) enabling arbitrary link-to-link structures and notes Nelson's comparison to LISP cons cells. Whether compound link graphs require well-formedness constraints (acyclicity, finite depth, consistent typing across chains) is a natural follow-on question already captured in the open questions.

**Why out of scope**: The ASN correctly limits itself to establishing that link-to-link references are structurally valid and deriving the canonical span construction. Constraints on compound link graphs would require defining the graph structure and its invariants — new territory beyond the ontology of individual links.

VERDICT: REVISE
