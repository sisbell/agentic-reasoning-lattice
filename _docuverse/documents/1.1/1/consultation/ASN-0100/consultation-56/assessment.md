# Channel Assignment — ASN-0100 review-56

**Date:** 2026-06-04 16:04

## Issue 1: Claims table carries near-duplicate rows
Reason: Purely editorial deduplication of claim rows; deciding which row subsumes which is derivable from the ASN's own claim statements, no design intent or implementation evidence needed.

## Issue 2: Statement column of the claims table embeds full proofs
Reason: The derivations already appear in the body sections cited; trimming the Statement cells to bare claims is an internal restructuring with no external dependency.

## Issue 3: Forward-looking aside in a claims-table entry
Reason: Removing a speculative sentence about downstream K.μ⁻ behaviour from INS.inv.depth's slot is a self-contained edit; the claim's correct scope is fixed by the ASN's own definition of INSERT.

## Issue 4: Multiple sections defer to the same downstream derivation
Reason: Consolidating two forward-pointers to one canonical derivation and citing claim labels is an internal cross-reference cleanup, fully determined by the ASN's existing structure.
