# Channel Assignment — ASN-0047 review-54

**Date:** 2026-05-16 17:54

## Issue 1: K.δ case (ii) k=2 sub-case description contains a confused sentence
Reason: The contradiction is internal to the ASN — for k=2, `e = inc(t, 2)` mathematically forces `parent(e) = t`, so the "sibling of parent(e)" sentence directly contradicts the formal definition. Fix is a textual cleanup derivable from K.δ's own structure.

## Issue 2: SubAllocatorAxiom's relationship to T10a's allocator discipline is unclear
Reason: Clarifying whether b_C(d) and b_L(d) sit inside or outside T10a's tree requires both design intent (how the docuverse partitions subspaces) and implementation evidence (how sub-allocators are realized and whether T10a.6 applies to them).
Nelson question: How does the design conceive of content vs. link subspace allocation under a document — are they separate allocator structures established at document creation outside the usual inc-based hierarchy, or extensions of a single per-document allocator?
Gregory question: In udanax-green, are the content sub-allocator and link sub-allocator under a document realized as a single allocator emitting siblings differing in subspace prefix, or as two structurally distinct allocators with disjoint domains and independent frontiers?

## Issue 3: K.μ~ has dual definitional structure (contract + decomposition) without clear primacy
Reason: This is a specification design choice between primitive and composite characterization — the ASN has all information needed to commit either way without external input.

## Issue 4: K.μ~ link-subspace identity precondition is "overdetermined" but still stated
Reason: The ASN already proves the redundancy via S3★ + CL-UNIQ + K.μ⁺ amendment; the decision to drop or retain the precondition is internal cleanup.

## Issue 5: K.δ k=1 ghost-base prohibition lacks invariant-level justification
Reason: The strengthening claims to lift the implementation contract to the spec but the harmlessness verification supports the weaker form; we need design intent on whether ghost-base versioning is admissible and implementation evidence on whether the live-base requirement is essential.
Nelson question: Does the design admit creating a new version of a document whose base address has no live entity in the docuverse (ghost-base versioning), or does the ghost-element doctrine apply only to non-immediate ancestors and require the immediate version base to be a live document?
Gregory question: Does `docreatenewversion` strictly require the source document to be a live granfilade entity (e.g., via `doretrievedocvspanfoo`) before issuing a version address, or can a version be allocated against an address that was never instantiated or has been removed?

## Issue 6: K.μ⁻ admissibility precondition duplicates D-CTG★/D-MIN★ postcondition information
Reason: The equivalence between admissibility precondition and D-CTG★/D-MIN★ postcondition under D-SEQ★-shaped input is established in the ASN's own case analysis; choice between precondition and derived postcondition is internal.

## Issue 7: K.μ⁻ amendment forbids interior link withdrawal — structural defect deferred to open question
Reason: The fix is to scope the structural sufficiency claim to acknowledge the link-withdrawal gap — the ASN already documents the gap in open questions, so the relocation/qualification is internal.

## Issue 8: Forward references to CL-UNIQ and S3★-aux from K.μ~ section
Reason: This is a presentation order issue — the ASN's own disclaimer notes the fix (reorder sections).

## Issue 9: The verification of K.δ k=1 base-liveness is presented as exhaustive but conclusory
Reason: This is an exposition/compression issue with no underlying derivation question — the verification logic is sound, just over-elaborated.

## Issue 10: Properties Introduced table contains duplicate or near-duplicate entries
Reason: This is a cataloging/presentation issue — partitioning new vs. extension vs. restatement is bookkeeping derivable from each property's relationship to foundation ASNs.
