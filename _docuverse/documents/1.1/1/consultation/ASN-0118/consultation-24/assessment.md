# Channel Assignment — ASN-0118 review-24

**Date:** 2026-06-10 08:25

## Issue 1: No-gap half of the tiling relies on an uncited multi-step shift identity
Reason: Internal — the missing step is the shift-composition identity `(min+i)+W = min+(i+W)`, which is part of the tumbler arithmetic the ASN already builds on, and the reviewer names the exact lemma to cite (TS3 ShiftComposition / Extended Associativity in ASN-0034/ASN-0084). No design intent or implementation behavior is in question; it is a mechanical citation within the formal model.

## Issue 2: The I3-scope caveat is stated and then recapped verbatim
Reason: Internal — pure prose deduplication. The substantive I3-VP/I3-VD vs. OrdShiftHom distinction is already worked out in the displacing-case composite; the fix is to state the scope once there and drop the two redundant framings, requiring no design or implementation input.

## Issue 3: Content-residence and `act ⊆ V_{s_C}(d_s)` are forward-referenced twice in the resolution section
Reason: Internal — the single-subspace/single-depth consequence is already established from content-residence and S8-depth within the ASN; the fix only removes a duplicated forward reference, which is derivable from the ASN's own structure.

## Issue 4: CP0's grounding is wrapped in defensive meta-framing
Reason: Internal — the interior-address derivation (each `aⱼ+k` is `M(d_s)(vⱼ+k)` via S8 lockstep) is already present and self-sufficient; the fix is to delete the meta-commentary sentence, with no bearing on design intent or implementation.

## Issue 5: CP3c's role ("dischargeable from the postconditions alone") is restated within adjacent sentences
Reason: Internal — pure prose deduplication. CP3c's domain equation and its S2-discharge role are fully specified in the ASN; collapsing the repeated phrasing requires no external evidence.
