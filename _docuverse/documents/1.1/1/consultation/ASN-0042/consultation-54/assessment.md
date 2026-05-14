# Channel Assignment — ASN-0042 review-54

**Date:** 2026-05-14 10:20

## Issue 1: Worked example — `a₃` invoked in the Fork scenario without provenance in Σ.B
Reason: Bookkeeping fix internal to the worked example. Either option (seeding `a₃` in `Σ_0.B` or inserting a `π_N` baptism step) is mechanically derivable from the ASN's own B6/B1/O5 obligations — no design intent or implementation evidence at issue.

## Issue 2: AccountField postcondition (a) — "satisfying T4 and T4a" is malformed
Reason: The ASN itself states T4a as a Consequence (derived equivalence) of T4 in its references to ASN-0034, so dropping "and T4a" is internal terminological cleanup.

## Issue 3: OwnershipDomainPermanence Step 4 is structurally redundant
Reason: Step 2 of the same proof already establishes `pfx(π) ≺ pfx(π')`; eliminating or folding Step 4 is pure proof-structure editing within the ASN.

## Issue 4: "By the same reasoning" in acct(a) Case zeros = 3
Reason: The reviewer supplies the replacement sentences explicitly; reusing T4a + T4 invariants already cited in the Case `zeros = 2` paragraph is internal.
