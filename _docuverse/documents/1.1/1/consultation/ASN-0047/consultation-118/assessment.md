# Channel Assignment — ASN-0047 review-118

**Date:** 2026-05-19 15:31

## Issue 1: K.δ case (ii) k=2 sub-case A induction omits sub-case C as a base
Reason: The fix is internal — the ASN already defines sub-case C and NodeRegistryBootstrap; the induction prose just needs to name both B and C as valid bases.

## Issue 2: P7a proof uses dom(L) where dom(L') is required
Reason: The fix is internal — restating the proof to apply S3★ and L14 at Σ' directly uses invariants already present in the ASN; no design-intent or implementation question is involved.

## Issue 3: S7b matrix entry misattributes the zeros(a) = 3 source
Reason: The fix is internal — the ASN body already restates ASN-0093's K.α precondition `zeros(a) = 3` verbatim; the matrix entry just needs to cite it directly rather than derive it.

## Issue 4: P4a Class (b) matrix entry has muddled temporal language
Reason: The fix is internal — the correct elementary ordering is established by the worked example and the boundary-only framework already in the ASN; this is presentation cleanup.

## Issue 5: K.μ⁻ admissibility derivation circulates through D-SEQ★ at the post-state
Reason: The fix is internal — the D-SEQ★ derivation chain from D-CTG★ + D-MIN★ + S8-depth + S8-fin + S8a is already stated in the ASN; the prose just needs to make non-circularity visible.
