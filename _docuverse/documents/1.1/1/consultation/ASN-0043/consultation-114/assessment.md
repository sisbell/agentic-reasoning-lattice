# Channel Assignment — ASN-0043 review-114

**Date:** 2026-05-30 17:16

## Issue 1: Dangling forward reference in the Worked Example — promised L9 verification never appears
Reason: Purely internal — the fix adds or inlines a disjointness check (`g` against `c₁, c₂, a`) using T7 and subspace distinctness, all already present in the ASN's own Setup and L0/L9 machinery. No design intent or implementation evidence is at stake.

## Issue 2: DocVal carries a use-site inventory rather than content (anti-bloat)
Reason: Purely internal — deleting a trailing meta-prose sentence requires no external evidence; DocVal's claim and its S7d/T10a.4 derivation are self-contained.
