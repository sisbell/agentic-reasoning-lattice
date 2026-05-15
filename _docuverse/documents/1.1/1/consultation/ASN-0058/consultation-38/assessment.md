# Channel Assignment — ASN-0058 review-38

**Date:** 2026-05-15 04:51

## Issue 1: M-int's "Prefix agreement" leaves implicit a witness identification
Reason: This is a proof-exposition gap entirely internal to M-int. The required witness identification (`j' = j₀`) is derivable from T1's structure, the minimality of `j₀`, and the prefix agreement already established — all ASN-0034/ASN-0058 content. No design intent or implementation evidence is needed.

## Issue 2: C0a case (b) repeats the same implicit witness identification
Reason: Same shape as Issue 1 — purely a proof-exposition gap. The witness identification follows from T1(i)'s least-divergence semantics, the minimality of `j₀`, and the prefix agreement `tᵢ = uᵢ` for `i < j₀` already in the proof. Fix is internal.

## Issue 3: C2's enumeration argument elides an inclusion chain
Reason: All three facts needed (well-formedness inclusion, C0a's prefix confinement, S8-depth's depth pinning) are already cited in the existing argument — the fix is to make the two-sided inclusion chain explicit, not to introduce new content. Derivable from the ASN itself.

## Issue 4: M12 (⟸) condenses a multi-step derivation
Reason: Expanding the disjunction of condition 3 requires only conditions 1 and 3 of "maximal run" (already defined in M12) plus B3-style chaining — all internal. Neither design intent nor implementation evidence is needed; this is a proof-writing clarification.
