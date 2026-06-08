# Review of ASN-0100

This ASN is technically strong: the substrate decomposition is sound, the composite-boundary vs. per-state invariant distinction is handled correctly (P4★/P4a/P7a/J0 are properly deferred to the boundary while P6/P7 are discharged per-intermediate), the closed-interval reduction for D-CTG★ at m ≥ 3 checks out, and the worked examples exercise the genuinely hard cases (forced full shrinkage at j=0, off-prefix exclusion at m_C=3). I found no skipped proof step or missing edge case. The findings below are anti-bloat / redundancy issues, consistent with this note's `review-mode.anti-bloat` classifier.

## REVISE

### Issue 1: The "identity by allocation, not value" theme is stated three times in different words
**ASN-0100, Effect One / Identity Through Allocation / claim INS.identity**:
- Effect One: "INSERT creates *new* content with *fresh* I-addresses: the operation does not reuse, alias, or identify with any pre-existing I-address … content identity is based on creation, not value."
- Identity Through Allocation: "INSERT confers fresh content identity … The system tracks identity by allocation event, not by value — if two allocations carry coinciding bytes, that coincidence is observable but produces no shared identity."
- INS.identity row: "INSERT cannot identify new content with any pre-existing I-address regardless of value coincidence."

**Problem**: Effect One and the Identity Through Allocation section say substantially the same thing — the pattern "two paragraphs in the same document say the same thing in different words." The claim-table row is the legitimate summary; the prose should state the point once.
**Required**: Keep the formal treatment (the section, which uniquely carries the INS.identity.crossdoc corollary) and the claim row; remove the redundant restatement in Effect One, or reduce Effect One to the allocation mechanics it actually needs.

### Issue 2: "What is *not* allocated" restates the Frame Conditions
**ASN-0100, "What is not allocated"**: "INSERT does *not* allocate new documents (`dom(M') = dom(M)`), does *not* allocate new links (`L' = L`) … every `a_k` has `subspace_I(a_k) = s_C`."

**Problem**: `dom(M') = dom(M)` and `L' = L` are already stated verbatim in Frame Conditions and again in INS.frame.L / INS.frame.E. The subsection adds no new content beyond a re-description of the frame — a "statement of what the operation does not do" relocated into a dedicated structural slot where it duplicates the contract.
**Required**: Fold the one genuinely new fact (allocation footprint is exactly `n` content-subspace I-addresses, `subspace_I(a_k) = s_C`) into INS.C or INS.alloc and delete the standalone subsection.

### Issue 3: Forward-reference deferral for INS.proj
**ASN-0100, Cross-document independence**: "…gives `project(ℓ, i, d', Σ') = project(ℓ, i, d', Σ)` by INS.proj's `d' ≠ d` case (proved below)."

**Problem**: This paragraph asserts a projection result and defers its justification to INS.proj, stated and proved later in the Coverage section — a forward reference whose `d' ≠ d` case is trivially the cross-document frame already established two sentences earlier ("the cross-document frame `M'(d') = M(d')` established above"). The deferral adds an indirection the reader must chase for a result already in hand.
**Required**: Either derive the one-line `d' ≠ d` consequence directly here from the frame (no forward reference needed), or drop the sentence and let INS.proj carry it where it is proved.

## OUT_OF_SCOPE

### Topic 1: Failure-recovery / canonical-order restoration after partial composite failure
**Why out of scope**: Raised in Open Questions; it is an implementation-realization concern, correctly deferred, not a defect in this ASN.

### Topic 2: Link-subspace insertion (K.μ⁺_L) semantics
**Why out of scope**: The ASN explicitly bounds itself to the content subspace; link-subspace insertion is a structurally distinct operation.

VERDICT: REVISE
