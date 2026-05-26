# Channel Assignment — ASN-0091 review-7

**Date:** 2026-05-26 15:43

## Issue 1: Empty arrangement boundary case is implicit, not explicit
Reason: The fix is internal. The ASN already states `|dom_C(M(d))| ≥ 2` is forced by R-PRE(iv) ∧ CS2; extending this to explicitly note the empty case follows from RA-π's vacuous behavior on an empty domain plus the existing cardinality argument.

## Issue 2: "Transclusion-bearing arrangement" phrasing is potentially misleading
Reason: The fix is internal. Fragmentation depends only on breaking I-address-chain adjacency under π; this is derivable from the existing definitions of maximal runs and the construction. The reviewer has supplied the replacement phrasing directly.

## Issue 3: Per-state foundation invariant verification missing from worked examples
Reason: The fix is internal. The relevant invariants (S8a, S8-depth, S3★, D-CTG★, D-MIN★, D-SEQ★) are formal definitions in the project's own foundation specs (ASN-0036/ASN-0047), not external knowledge requiring Nelson's design intent or Gregory's implementation evidence — the author can apply them to the concrete arrangements exhibited in each worked example.
