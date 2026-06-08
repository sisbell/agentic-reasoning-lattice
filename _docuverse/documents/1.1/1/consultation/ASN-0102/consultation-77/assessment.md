# Channel Assignment — ASN-0102 review-77

**Date:** 2026-06-08 03:13

## Issue 1: `k` mischaracterized as the M7-maximal block count of the concatenated region
Reason: The fix is internal — the ASN already defines `k` correctly (as `Σ kᵢ`, per-reference maximal-run counts) and X8 already derives that the concatenated/copied region merges to `≤ k` blocks. Scoping the M7-maximality clause to `kᵢ` (or dropping it) is settled entirely by the ASN's own definitions and X8; no design intent or implementation evidence is required.
