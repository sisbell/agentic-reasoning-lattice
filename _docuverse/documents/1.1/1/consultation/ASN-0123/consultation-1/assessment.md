# Channel Assignment — ASN-0123 review-1

**Date:** 2026-06-12 16:53

## Issue 1: The necessity half of G2 has an unproven step
Reason: The missing prefix-antichain lemma is derivable from LP-Sub's structural form and T4-validity, both already cited in the ASN, and the review sketches the proof itself. Internal proof-writing; no design intent or implementation evidence is needed.

## Issue 2: The ownership-model bridge is asserted, not established — ω may be undefined at the guard
Reason: Choosing between the standing totality assumption and a definedness precondition turns on whether a document can exist without an owning account — a design-intent question — and the assumption should be grounded in what the implementation's creation paths actually enforce.
Nelson question: Is every document intended to be created under an existing account, making ownership total over all allocated documents, or does the design admit documents with no owning account?
Gregory question: Do udanax-green's document- and version-creation paths enforce that every new document tumbler lies under an existing account (e.g., session or account checks at creation), or is there any code path that can create a document not covered by an account?

## Issue 3: Contiguity of the version namespace (the B1-analog) is proved by parenthesis
Reason: The fix is a preservation induction over the K.δ vocabulary using tumbler arithmetic (inc, zeros, stream membership) already in the ASN's apparatus, or routing through ASN-0034's AllocatedSet structure — cross-ASN formal work with no external fact required.

## Issue 4: V3 is cited and tabled but never stated or proved
Reason: V3's discharge follows from the per-step frame conditions of K.δ, K.μ⁺, and K.ρ already cited from ASN-0047 and the Effect clause's stipulations. Pure proof-writing internal to the ASN.

## Issue 5: V5(a) conflates "k-th fork" with "k-th namespace allocation"
Reason: The review fully specifies both acceptable restatements (namespace-relative form, or explicit conditioning on VD), and VD is already defined in the ASN; the deeper enforcement question is deliberately deferred to Open Question 1. Internal.

## Issue 6: V11(a) fails at the boundaries
Reason: The corrected statement is supplied verbatim by the review and follows from the enabling conditions of K.μ⁺, K.μ⁻, and K.μ~ already present in the foundation. Internal.

## Issue 7: V10 corollary (ii) states its key sentence backwards
Reason: A sentence-direction fix plus a cross-reference to corollary (iii)'s standing-arrangement condition; all needed content is already on the page. Internal.

## Issue 8: The atomicity remark claims more than the foundations supply
Reason: The conservative boundary-level restatement is internal, but the review's alternative — stating a composite-isolation convention — requires evidence of what isolation the implementation actually provides between the steps of a request.
Gregory question: Does the backend serialize request processing such that no other operation can observe an intermediate state of docreatenewversion — for example, the new version document existing in the granfilade before its POOM has been populated?
