# Channel Assignment — ASN-0075 review-50

**Date:** 2026-06-03 08:50

## Issue 1: Directional mismatch in "Distinguishing Deletions from Additions"
Reason: Purely internal consistency fix — the correct disambiguator and matching half are both defined within the ASN; align the example and the disambiguation paragraph to the same half.

## Issue 2: Mislabeled cross-reference to D-IDENT
Reason: Internal — D-IDENT's actual content (identity preservation) and the witness condition are both stated in the ASN; correcting the attribution needs no external input.

## Issue 3: D-ACT justification restates itself
Reason: Internal editorial collapse of three redundant sentences into one; no design intent or implementation evidence required.

## Issue 4: Protocol-rationale accretion in the D-DISCR notational convention
Reason: Internal — the per-composite annotations already discharge J0/J1★ at point of use, so removing the upfront rationale and forward pointer is derivable from the ASN's own structure.
