# Channel Assignment — ASN-0094 review-59

**Date:** 2026-05-24 07:55

## Issue 1: NAT-card additivity proof uses subtraction before NAT-sub is derived
Reason: The fix is derivable from the ASN's own content — step (γ) already establishes `|S₁'| + 1 = |S₁|`, and the required reformulation uses only ℕ-assoc, ℕ-comm, and that identity. No design intent or implementation evidence is needed; this is a mechanical rearrangement of arithmetic already present in the proof.

## Issue 2: Stratified proof order omits NAT-sub from LinkAddressNotPrefixOfEmit's consumed inputs
Reason: The fix is a bookkeeping reconciliation — the proof body explicitly cites NAT-sub at Steps II.0 and II.1, so the stratification metadata simply needs to be updated to match what the proof actually consumes. No external consultation required.
