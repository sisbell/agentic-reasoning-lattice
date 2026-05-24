# Channel Assignment — ASN-0051 review-27

**Date:** 2026-05-15 21:59

## Issue 1: SV10 witness violates S7c (foundation invariant)
Reason: Mechanical correction — choose addresses satisfying #E ≥ 2 and recompute the reach. All required machinery (S7c from ASN-0036, tumbler arithmetic, D0/D1) is already cited within the ASN.

## Issue 2: SV6 — T4-validity of generic t in span not explicitly established
Reason: The proof gap is filled using T4's no-adjacent-zeros, t₁ ≠ 0, t_#t ≠ 0 conjuncts (ASN-0034, already cited) and the existing agreement-with-s structure. Pure proof augmentation.

## Issue 3: SV6 sub-lemma — implicit #t ≥ j assumption
Reason: Inserts a prefix-exclusion argument using T1(ii), already cited within the proof. Internal logical patching.

## Issue 4: wp(K.μ⁺) assumes single mapping
Reason: The fix generalizes the wp formula based on K.μ⁺'s Effect specification in ASN-0047 (already cited). The reviewer provides the corrected form.

## Issue 5: wp(K.μ⁻) doesn't constrain V_rm to D-SEQ tail
Reason: Adds the D-SEQ constraint from K.μ⁻ in ASN-0047, already cited within this ASN's wp section. The constraint just needs explicit statement.

## Issue 6: SV0 — L-equality precondition extraneous, framing misleading
Reason: Reformulation references the state-space schema (ASN-0036), link value structure (ASN-0043), and operation set (ASN-0047) — all foundation ASNs already cited. The substantive meta-claim about admissible resolution functions is derivable from these definitions.

## Issue 7: SV2 proof attributes ran growth to "frame" instead of "effect"
Reason: Terminological correction citing the existing Frame/Effect distinction in ASN-0047.

## Issue 8: SV11 distributivity step implicit
Reason: Pure set-algebraic derivation (∩ distributes over ∪, plus coverage(e) = ⋃_j ⟦(sⱼ, ℓⱼ)⟧). No external evidence required.

## Issue 9: Title doesn't match content
Reason: Authorial choice between retitling to match the body's survivability framing or introducing a formal displacement concept. The body's SV2–SV13 content determines the appropriate title; no external channel needed.
