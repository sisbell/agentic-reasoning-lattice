# Channel Assignment — ASN-0087 review-64

**Date:** 2026-06-04 02:40

## Issue 1: D-CTG★ discharge rests on an unsupported global reachability claim
Reason: The fix is internal — the corrected contiguity argument is a direct T1 consequence of the D-SEQ★ initial-segment structure already present in the ASN, holding at any depth `m_L(d) ≥ 2`; no design intent or implementation evidence is needed, and the required change is to delete the unsupported global-reachability detour.

## Issue 2: Reviser-drift / accretion around the freshness derivation
Reason: The fix is internal — collapsing a section into an existing citation and stripping meta-prose are editorial changes that rely only on foundation lemmas (FirstEmissionFreshness, SubsequentEmissionFreshness, Store Monotonicity★) already cited in the ASN.

## Issue 3: Duplicated sentence in the claims table
Reason: The fix is internal — removing a verbatim duplicated notation sentence from the claims table is purely editorial.
