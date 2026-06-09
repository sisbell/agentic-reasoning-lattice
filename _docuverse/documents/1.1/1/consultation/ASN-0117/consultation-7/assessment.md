# Channel Assignment — ASN-0117 review-7

**Date:** 2026-06-08 22:41

## Issue 1: Cross-document isolation (P5) is never exercised concretely
Reason: The fix only adds a worked scenario instantiating claims already proven in the ASN (P5, DEL-FDOC, P0, C'=C). No design intent or implementation evidence is needed — the required machinery and the expected result are fully present in the ASN's own clauses.

## Issue 2: DELETE is not pinned to a foundation transition kind, and the entity/provenance frame is unstated
Reason: This is a bookkeeping/derivation fix against the spec's own foundation model — identifying DELETE as K.μ⁻ and adding the E'=E, R'=R frames plus the P4★/P7a one-liner. The reviewer already supplies the bridge (`Contains_C` shrinks, `dom(C')=dom(C)`, so both hold with `R'=R`), and K.μ⁻'s frame requirements live in the cited foundation ASNs, not in Nelson's intent or Gregory's code.
