# Review of ASN-0058

## REVISE

### Issue 1: Definition asserts an unproven uniqueness theorem for the empty arrangement
**ASN-0058, Definition (Block Decomposition)**: "The empty arrangement `M(d) = ∅` has `B = ∅` as its unique decomposition."
**Problem**: The definition slot asserts *uniqueness*, but no proof is given there, and M2 immediately afterward only discharges *existence* ("admits `B = ∅` ... B1, B2, B3 are vacuously satisfied"). M12 proves uniqueness only of the *maximally merged* decomposition, not of decompositions in general — so the unqualified "unique decomposition" claim has no supporting argument anywhere. The empty case is thus stated twice (definition + M2) with the definition carrying an unsupported theorem-claim.
**Required**: Drop "unique" from the definition (a definition slot should not assert an unproven uniqueness result), or, if uniqueness of the empty decomposition is wanted, give the one-line argument (any block has `n ≥ 1`, hence non-empty `V(β)`, forcing a domain point that `∅` lacks) and place it in M2, not the definition.

### Issue 2: M14's verification proves an unlabeled, strictly stronger result than M14 claims
**ASN-0058, M14 (IndependentOccurrences)**: M14 claims only that blocks "sharing their I-start and width (with `v₁ ≠ v₂`)" are unmergeable. The paragraph beginning "The same conclusion extends to any two distinct blocks `β₁ = (v₁, a₁, n₁)`, `β₂ = (v₂, a₂, n₂)` ... whose I-extents share at least one position" proves a different, more general statement (any shared I-extent position ⟹ I-adjacency unsatisfiable).
**Problem**: This is a labeled-claim-worth of content (shared-I-overlap ⟹ unmergeable) sitting as trailing proof-prose under a claim whose stated postcondition does not cover it. A reader checking M14 against its statement finds a second, unstated theorem appended. Per the review standard, content of this weight needs its own home, not an unlabeled coda.
**Required**: Either promote the generalization to its own labeled property (e.g., `M14a (SharedIExtentUnmergeable)`) with its own statement, or remove it and confine M14's verification to M14's stated claim.

## OUT_OF_SCOPE

### Topic 1: Lattice structure of the equivalent-decomposition poset
**Why out of scope**: Raised in Open Questions; characterizing the refinement lattice with the canonical decomposition as a distinguished element is genuinely new algebraic territory, not a gap in the present claims.

### Topic 2: Multi-source resolution ordering / reorderability
**Why out of scope**: The Open Question on whether an implementation may reorder source references is an operation-placement concern; C1b fixes the per-reference order, and the cross-reference policy belongs to a later operation-semantics ASN.

VERDICT: REVISE
