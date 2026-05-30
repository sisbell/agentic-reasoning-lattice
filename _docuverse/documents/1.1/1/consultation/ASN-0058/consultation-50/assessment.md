# Channel Assignment — ASN-0058 review-50

**Date:** 2026-05-30 08:51

## Issue 1: Use-site inventory in the Content References preamble
Reason: Purely editorial deletion of a redundant advance-inventory sentence; the inline citations already carry every dependency at its point of use. No design intent or implementation evidence is needed.

## Issue 2: The `m ≥ 2` justification is scattered, and C1a's back-reference mis-points
Reason: This is a relocation-and-pointer fix entirely within the ASN — consolidate the `m ≥ 2` derivation at the ContentReference definition, delete the duplicate in C0a, and correct C1a's back-reference. All cited material (precondition (i), S8a, S8-depth) already lives in the note.

## Issue 3: M0 and M1 reproduce the same strict-monotonicity proof
Reason: De-duplicating two verbatim strict-monotonicity proofs and redirecting the M5(b)/M12b back-references is an internal restructuring; the underlying facts (TS4, TS5) and their use are already fully present in the ASN.
