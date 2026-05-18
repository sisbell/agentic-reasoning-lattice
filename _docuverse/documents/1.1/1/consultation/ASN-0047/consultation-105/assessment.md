# Channel Assignment — ASN-0047 review-105

**Date:** 2026-05-18 05:33

## Issue 1: NodeUniqueAllocation clause (c) — structural mismatch
Reason: Pure structural reformulation — splitting an event-based universal from an initial-state existential is derivable from the ASN's own structure; no external evidence needed.

## Issue 2: SubAllocatorAxiom — T10a-membership of A_C(d), A_L(d) not committed
Reason: The L1c paragraph already asserts T10a-conformance of subsequent emissions as a side remark; elevating it to an axiom sub-clause is a formal commitment internal to the ASN.

## Issue 3: K.μ⁻ admissibility clause (2) — internal contradiction
Reason: Either remove from precondition list or commit as precondition — purely a clarity decision derivable from the operation's own semantics.

## Issue 4: K.δ case (ii) k = 0 — frontier requirement implicit
Reason: T10a's per-(t, k') uniqueness clause already precludes non-frontier sibling allocation; the fix is either elevating this as an explicit precondition or making the T10a discharge argument explicit. Derivable from the foundation.

## Issue 5: K.δ k = 1 — parent-allocator relationship not stated
Reason: The parent-allocator structure (parent_allocator(A_v(t)) = A_doc(parent(t))) is derivable from the *Allocator hierarchy under documents* section combined with T10a's spawn rules; the fix is to make the relationship explicit at the discharge site.

## Issue 6: K.μ⁺ amendment frame omits L' = L
Reason: Pure structural fix — adding the L' = L conjunct to the extended-state frame is a notational completion derivable from the ASN's own state-component enumeration.

## Issue 7: Worked example: interior content replacement — composite definition unclear
Reason: The two-step (transcluded) vs four-step (fresh) replacement distinction is derivable from K.α's role under J0 — the elementary transitions already determine which steps are needed in each case.

## Issue 8: D-SEQ★ forward reference in K.μ⁻ amendment
Reason: Document-organization fix — reordering paragraphs so that defining sites precede consuming sites. Internal.

## Issue 9: ExtendedReachableStateInvariants — summary verification
Reason: Proof restructuring (verification matrix or per-transition completeness) is internal organization — every preservation argument already lives somewhere in the ASN; the issue is presentation, not new content.

## Issue 10: Accretion meta-prose
Reason: Editorial cleanup — removing meta-prose, defensive justifications, and "see X below" cross-references is internal to the ASN's prose.

## Issue 11: K.μ~ "bijectively into"
Reason: Typo fix — "into" → "onto." No external input needed.

## Issue 12: SequentialTransitionAxiom — composite-boundary invariants and intermediate-state observability
Reason: This is a design-intent question (is the docuverse semantics intended to expose intermediate states between elementary steps?) coupled with an implementation-evidence question (does udanax-green commit compound operations atomically?). Both channels needed.
Nelson question: Did the design intend compound operations like create-document-with-initial-content or fork-with-population to be atomic from the docuverse's external semantics, or are the intermediate states between elementary steps conceptually observable to other agents in the system?
Gregory question: Do udanax-green's compound document operations (e.g., `docreatenewversion` followed by content insertion and provenance recording, or `docreatelink` which combines link allocation with placement) execute as transactional atoms with no externally-observable intermediate state, or can concurrent operations observe states where allocation has occurred but placement or provenance recording has not?
