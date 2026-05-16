# Channel Assignment — ASN-0047 review-43

**Date:** 2026-05-15 17:07

## Issue 1: K.λ allocation description has notation and operator errors
Reason: The notation/operator errors are derivable from ASN-0034's TA5 case definitions and L1's zeros-count constraint; the ASN's own worked example shows the correct address structure (ℓ = 1.0.1.0.1.0.2.1 with zeros = 3). Fix is internal — restate the inc chain with correct operators and component counts.

## Issue 2: "We include links in E_doc" contradicts formal definitions
Reason: The contradiction resolves from this ASN's own formal definitions — IsDocument requires zeros = 2 (ASN-0045), L1 requires links to have zeros = 3, so IsDocument(ℓ) is false and links cannot inhabit E_doc. The state model already places L as a distinct component. Fix is internal: align prose with the formal partition.

## Issue 3: K.μ~ definition does not explicitly require subspace-preserving bijection
Reason: Adding a subspace-preserving precondition is a formal strengthening that surfaces a constraint the ASN already derives indirectly through S3★, L14, and link-subspace fixity. Fix is internal.

## Issue 4: Foundation ASN amendments not properly identified
Reason: This is a presentation/labeling choice between marking modifications as foundation amendments versus introducing ★-named properties; the technical content is unchanged. Fix is internal.

## Issue 5: SC-NEQ stated as fact but not labeled as an axiom
Reason: Adding the "Axiom" label is a presentational alignment with existing foundation conventions (NoDeallocation, S0). Fix is internal.

## Issue 6: Permanence-from-frames lemma does not address L
Reason: Extending the lemma to L12 follows the existing P0/L12 frame-based derivation pattern already established in this ASN. Fix is internal.

## Issue 7: K.μ⁻ admissibility precondition references D-CTG★/D-SEQ★ defined later
Reason: This is a document-organization fix — either reorder sections or restate the precondition in self-contained terms using content already in the ASN. Fix is internal.

## Issue 8: K.λ does not verify L1b (#E(ℓ) ≥ 2)
Reason: L1b is an existing foundation invariant from ASN-0043; adding it to K.λ's precondition (or deriving via L1c) follows the standard precondition-listing convention used elsewhere in the ASN. Fix is internal.

## Issue 9: Link withdrawal restriction under D-CTG★ understated
Reason: The reviewer wants a body-level paragraph characterizing the conflict between D-CTG★/D-MIN★ and Nelson's tombstoning design (LM 4/9). The ASN already cites Nelson's "not currently addressable" status, but a substantive characterization of the withdrawal mechanism would help write the acknowledgment.
Nelson question: Does the design require that single-link withdrawal at arbitrary V-positions be supported, with the withdrawn link transitioning to "not currently addressable" status while retaining its arrangement position — or is tombstoning a separate state attribute orthogonal to V-position arrangement?

## Issue 10: K.δ for non-root entities — inc chain incomplete
Reason: The case distinction by k (sibling vs. descent) is derivable from ASN-0034's TA5 cases; the fix is to make the k-conditional roles of t explicit. Fix is internal.

## Issue 11: K.μ⁺ value-preservation under domain extension argument
Reason: The disjoint-domain consequence follows from K.μ⁺'s conjunctive postcondition (strict domain extension AND value preservation), which is already stated; the fix is to make the inference explicit. Fix is internal.

## Issue 12: SC-NEQ derivation from foundation is asserted but not shown
Reason: The correct derivation chain (L0 + SC-NEQ + T7 → L14) is already articulated in this ASN's L14 entry; the introductory citation needs alignment with that derivation. Fix is internal.
