# Channel Assignment — ASN-0051 review-62

**Date:** 2026-05-16 10:14

## Issue 1: SV11 attainment witness gap for (m ≥ 3, p = 2)
Reason: The fix is derivable from the ASN's own tumbler arithmetic, block-decomposition machinery, and the existing (m = 2, p = 2) construction. The reviewer even sketches the natural extension (single-element spans at non-adjacent offsets in both blocks, with the `min_k n_k ≥ 2m − 1` check) — verification uses only T1/TumblerAdd, S0 convexity, M7/M12 from ASN-0058, and the SV11 biconditional already established.

## Issue 2: Ambiguity in "intermediate state" terminology in Worked Example
Reason: Purely editorial — a rename (e.g., `M_after-step-1` or `M_after-reorder`) to reserve "intermediate" for the SV5-style elementary-stage state inside K.μ~. No external evidence required.

## Issue 3: SV11 attribution paragraph should acknowledge sharing's quantitative footprint more directly
Reason: The proposed identity `Σ_k |term_{j,k}| − |π_text| = Σ_a (m_a − 1) ⋅ |spans covering a|` is derivable directly from the SV11 decomposition cover formula and inclusion-exclusion on non-injective block I-extents. The supporting machinery (set-union idempotence, span coverage, block I-extents) is all in the ASN.

## Issue 4: SV11 attribution to "mechanism (b) only" risks overgeneralization
Reason: Editorial tightening of prose to scope the attribution to the specific witness rather than implying a global separation theorem. Derivable from the SV11 biconditional already stated.

## Issue 5: SV11 disjoint-pair T-interleaving sub-case verbosity has unaddressed clarity issues
Reason: Pure typo fix — replace `#f > #e ≥ #e` with `#f > #e`. No external evidence needed.

## Issue 6: SV13 omits a corollary for bilateral vitality
Reason: The bilateral vitality predicate is defined in the ASN, and its survival behavior under each transition is a one-line composition of SV2/SV3/SV4/SV5/SV5b applied per-slot. The wp framework for π extends to bilateral vitality by slotwise conjunction. No external channels needed.

## Issue 7: Worked Example's K.μ~ admissibility in Step 1 not fully discharged
Reason: The D-SEQ admissibility check for {v₃, v₄, v₅} as an upward tail of V_{s_C}(d) is mechanical from D-SEQ (ASN-0047, already cited) and mirrors the check the Worked Example performs at Step 2. No external evidence required.
