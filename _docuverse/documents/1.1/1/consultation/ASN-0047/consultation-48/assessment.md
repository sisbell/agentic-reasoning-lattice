# Channel Assignment — ASN-0047 review-48

**Date:** 2026-05-15 20:19

## Issue 1: K.λ first-link case lacks rigorous T10a-conformance
Reason: The fix requires understanding whether the link sub-allocator is a distinct T10a allocator (and how it's seeded) or shares an allocator with content. Both the design's conception of allocator structure and the implementation's realization are evidence for whether to construct b_L(d) via a concrete inc chain or to axiomatize it.
Nelson question: In the design, are content and link addresses produced by a single allocator under each document, or by two distinct sibling allocators — and if distinct, what spawning mechanism establishes the link allocator?
Gregory question: In udanax-green, how is the link allocator under a document seeded — is there a real ISA allocation that produces the link-prefix base, or does the implementation treat the link subspace as having a virtual starting point?

## Issue 2: Foundation-update proposal misplaced
Reason: Editorial fix — remove the "foundation should be updated" language and treat amendments as local to this ASN. Derivable from the ASN's own scope mandate.

## Issue 3: NodeUniqueAllocation axiom scope is ambiguous
Reason: The two cited mechanisms (Nelson's hierarchical baptism, Gregory's global granfilade) are already documented in the axiom's surrounding prose; the fix is editorial — clarify n₀'s status as a state-initial parameter and restate the axiom's mechanism non-circularly. Derivable from the ASN's own content.

## Issue 4: "Replacement decomposes into K.μ⁻ + K.μ⁺" claim is overly broad
Reason: Internal fix — qualify the claim by reference to K.μ⁻'s own admissibility precondition (suffix or full clearance), which is already established in this ASN.

## Issue 5: K.δ k=1 sub-case admits version-shaped addresses without version semantics
Reason: The fix requires deciding whether to constrain k=1-from-document, reject it, or prove omission harmless. Nelson's design intent on version lineage and Gregory's implementation of version creation both inform whether base-document existence must be enforced now or can be deferred.
Nelson question: In the design, does a version address [N,0,U,0,D,k] require the base document [N,0,U,0,D] (or prior versions) to exist, or can versions be allocated independently of the base's existence?
Gregory question: What does docreatenewversion (do1.c:271) require of the base document — must the base ISA exist in storage, and does the implementation enforce sequential version numbers?

## Issue 6: K.μ~ decomposition for non-trivial bijections is scattered
Reason: Editorial — consolidate the decomposition argument into one subsection at K.μ~'s definition site. The argument's components already exist in the ASN; only assembly is needed.

## Issue 7: Worked example does not verify P7a, P3★, or several link invariants
Reason: Internal verification completeness — add the missing invariant checks at each step using the ASN's already-stated invariants and frame conditions.

## Issue 8: ShiftPreservation for link-subspace V-positions is invoked but not derived
Reason: Citation fix — reference OrdShiftHom and ShiftPreservation from ASN-0036, verifying their subspace-independence by inspection of their statements. Derivable from the foundation as cited.

## Issue 9: ExtendedReachableStateInvariants proof's composite invariants treatment conflates J0 sequencing
Reason: Internal proof clarification — distinguish coupling constraints (initial-to-final) from intra-composite sequencing (preconditions at each intermediate state). The distinction is implicit in ValidComposite★'s definition; the fix is to make it explicit in the proof.

## Issue 10: Self-containment gaps — `subspace_I`, `subspace`, `origin`, `home`, `fields`, `parent`
Reason: Editorial — add a notation subsection citing each projection's source ASN and standardize on one notation per concept. No new content needed.
