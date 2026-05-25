# Channel Assignment — ASN-0070 review-4

**Date:** 2026-05-25 13:18

## Issue 1: F-canonical Step 1, case k = 1 — wrong exclusion reason
Reason: Internal fix. The exclusion mechanism (finiteness of V-restricted denotation under S8-fin) is already used for case 2 ≤ k < m_S(d) within the ASN; the fix is to extend that same argument to k = 1, derivable entirely from the V-restricted denotation definition (F0/F1) and S8-fin (ASN-0036, already cited).

## Issue 2: F-canonical Step 1, case 2 ≤ k < m_S(d) — construction wording inconsistent
Reason: Internal fix. The issue is purely about restating the witness construction unambiguously (fix tail to range only over t_m). No design intent or implementation evidence is involved — the corrected construction is mechanical from T1 ordering already in use.

## Issue 3: F-canonical Step 2 — "maximal contiguous runs" undefined; unique decomposition not derived
Reason: Internal fix. The required derivation uses only T1 ordering (ASN-0034), N1/N2 of normalised span-sets (ASN-0053), and the V-restricted denotation already defined in this ASN. The reviewer has supplied the proof skeleton; expansion is mechanical and self-contained.
