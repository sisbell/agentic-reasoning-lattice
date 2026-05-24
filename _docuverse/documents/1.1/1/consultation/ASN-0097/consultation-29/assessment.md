# Channel Assignment — ASN-0051 review-29

**Date:** 2026-05-15 22:54

## Issue 1: SV0 inconsistently labeled as both an SV claim and not a theorem
Reason: This is a labeling/organization decision derivable from the ASN's own content — the author needs to choose between proving SV0 as a derivation or recategorizing it as a Schema Observation.

## Issue 2: Same-origin coverage growth has no formal claim or explicit exclusion
Reason: Determining whether to make a formal claim requires design intent (was coverage growth at the byte level meant to be closed?) and implementation evidence (what does the allocator actually enforce?).
Nelson question: At the byte level within a document, was the "strap between bytes" intended to be closed against future same-origin allocations (including child-depth), or is span coverage open by design at all levels?
Gregory question: Does the udanax-green allocator ever produce child-depth tumblers (TA5(d) with k' > 0) for text content, or is sibling increment the exclusive allocation mode for byte-level text?

## Issue 3: SV7 transclusion corollary conflates fixed-A with document-derived A
Reason: The fix is a formal restatement derivable entirely from the ASN's existing discover_s definition and SV7's statement.

## Issue 4: SV13(e) "dual character" framing for K.λ is unclear
Reason: This is an editorial rewording derivable from the K.λ frame condition already established in the ASN.

## Issue 5: Bilateral vitality vacuous-case discussion is excessive
Reason: This is an editorial compression task derivable from the ASN's own definitions.

## Issue 6: Broader-level spans (k ≤ p₃) survivability not addressed
Reason: Characterizing broader-level span survivability requires design intent (how does coverage growth work for cross-document/account/node spans?) and may benefit from implementation evidence on whether such spans are realized.
Nelson question: For spans with action-points in the document-prefix region (server, account, document fields), did the design intend their coverage to grow monotonically as new nodes/accounts/documents are allocated within their reach, and is this growth bounded by any allocator discipline?
Gregory question: Does udanax-green implement broader-level spans (action-points at field positions ≤ p₃), and if so, what survivability or growth behavior does the implementation exhibit when new allocations occur within such spans' reach?

## Issue 7: Decomposition term vs maximal fragment count statements
Reason: The clarification follows directly from the ASN's own definitions of decomposition term (exactly m·p by construction) and maximal fragment (after coalescence).

## Issue 8: Worked example - K.μ~ + K.μ⁻ composite description awkward
Reason: This is an editorial presentation choice derivable from D-SEQ already cited in the ASN — either show the intermediate state or restructure the example.
