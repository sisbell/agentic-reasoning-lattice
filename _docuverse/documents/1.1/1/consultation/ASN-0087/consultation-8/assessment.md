# Channel Assignment — ASN-0087 review-8

**Date:** 2026-05-26 13:24

## Issue 1: Notation drift between substrate (ASN-0093) and transition model (ASN-0047)
Reason: Both ASN-0093 (`dom(M)`) and ASN-0047 (`E_doc`) are available; the equivalence is structural (K.δ IsDocument / K.σ register `d` into both simultaneously) and the bridging note is composable from existing definitions in those ASNs.

## Issue 2: S2 verification omits cross-subspace exclusion argument
Reason: The missing argument uses S3★-aux (ASN-0047), SC-NEQ (ASN-0093), and subspace decomposition — all already cited elsewhere in the ASN. Purely mechanical expansion of the existing reasoning.

## Issue 3: Boundary case — empty non-type endset not addressed
Reason: L3 (ASN-0043) settles permission (only `e₃ ≠ ∅` required), and `coverage(∅) = ∅` plus LP12 mechanically determine the degradation. The fix is either an example variant or a clarifying paragraph — both derivable from the ASN's own framework.

## Issue 4: L1c chain step k₃ admissibility threshold not flagged as tight
Reason: The saturation observation follows directly from TA5a's bounds (cited in the chain table) against the per-step zero-counts already computed. Adding the uniqueness remark requires only re-reading the existing table.
