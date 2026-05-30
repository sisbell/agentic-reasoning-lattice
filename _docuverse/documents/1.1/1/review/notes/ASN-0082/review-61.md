# Review of ASN-0082

## REVISE

### Issue 1: Near-verbatim duplicate framing across the two wp-analysis sections
**ASN-0082, "Weakest-precondition analysis (I3-VP...)" and "Weakest-precondition analysis (S8a-post...)"**: The insertion section opens "We illustrate the wp method on one of the preservation lemmas — I3-VP, which asserts S8a for the post-state — to expose the constraints that the assignment statement ... imposes on the pre-state ... Reading these obligations against the I3 contract makes explicit which preconditions the contract supplies and which it does not need to state because they are entailed by foundation invariants." The contraction section opens "We illustrate the wp method on the contraction's analogue of I3-VP — S8a-post ... Reading these obligations against the contraction contract makes explicit which preconditions the contract supplies ... entailed by foundation invariants." Both also close with the identical "no slack / contract's preconditions are exactly the wp-derived constraints" sentence.
**Problem**: Two paragraphs say the same thing in different words — the anti-bloat duplication pattern. The second preamble even labels itself "the contraction's analogue of I3-VP," confirming it is a transcription of the first. The wp computations themselves differ (different assignment, different conjuncts) and must stay; the surrounding boilerplate does not.
**Required**: Keep both wp computations, but state the shared method/framing once (or by one-line back-reference from the contraction section). Drop the duplicated opener and the duplicated "no slack" closer.

### Issue 2: Prose inventory restating the frame clauses
**ASN-0082, I3 explanatory paragraph**: "The left-region frame (I3-L) ensures that content before the insertion point is undisturbed. The cross-subspace frame (I3-X) ensures that link subspaces and other subspaces are unaffected by a text-subspace insertion. The cross-document frame (I3-D) ensures that other documents are unchanged. The content-store frame (I3-C) makes explicit that the shift is arrangement-only..."
**Problem**: This is a use-site inventory — each sentence re-narrates in English what the corresponding formal frame clause already states verbatim immediately above. It advances no reasoning; a precise reader skips it to reach the I3-V corollary and the domain-closure point that do carry content.
**Required**: Delete the clause-by-clause restatement. The Nelson grounding sentence and the I3-V-from-I3-CS derivation in the same paragraph are object-level and should stay.

### Issue 3: NAT-CA introduced as a primitive ℕ axiom, and placed away from its use
**ASN-0082, "The Ordinal Shift"**: "**NAT-CA** — *CarrierAdditionCommutativityAssociativity* (introduced locally). For all m, n, k ∈ ℕ: `m + n = n + m` ... and `(m + n) + k = m + (n + k)`."
**Problem**: A primitive ℕ-arithmetic axiom is introduced ad hoc inside the ordinal-shift discussion, but its only uses are in the span-width derivations (I3-S, D-S) much later. ASN-0034's NAT-* family (addcompat, closure, discrete, order, wellorder) is the established home for such axioms; commutativity/associativity belongs there, not freshly minted in an arrangement-displacement ASN. Its placement also strands it far from the only sites that consume it.
**Required**: Either route the ℕ-addition commutativity/associativity through a foundation citation (flagging the foundation gap if genuinely absent), or — if it must remain local — move it adjacent to its first use in the span sections rather than mid-way through "The Ordinal Shift."

## OUT_OF_SCOPE

### Topic 1: Contraction at ordinal depth > 1 and link-subspace contraction
**Why out of scope**: The depth-2 / S = 1 scoping axioms are deliberate, and the Open Questions already flag the TA4 zero-prefix collision with S8a positivity at intermediate components. Generalizing the gap-closure round-trip to deeper ordinals, and defining contraction on the (tombstone-permitting) link subspace, are genuinely new territory for a future ASN, not defects here.

The core mathematics is sound: the displacement round-trips (D-SEP via TA4, ord(r) ⊖ w_ord = ord(p)), the order-preserving bijection σ (D-BJ), the cardinality chain in D-SEQ-post (|L ∪ Q₃| = N − c), and the span-width identity (s₂+c′)−c = (s₂−c)+c′ discharged through ReverseInverse + TA4 + NAT-CA all check out, and the boundary cases (L=∅, R=∅, full deletion, cross-subspace) are exercised concretely.

VERDICT: REVISE
