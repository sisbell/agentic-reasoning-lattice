# Channel Assignment — ASN-0051 review-58

**Date:** 2026-05-16 08:46

## Issue 1: SV6 worked example uses inconsistent subspace conventions
Reason: Pure prose clarification about the meaning of "first component" — the ASN already contains the correct structural definitions via the K.α amendment reference. No external consultation needed; the fix is to disambiguate "first of whole tumbler" vs "first of element field" in the existing prose.

## Issue 2: SV13(e) link-subspace extension classification
Reason: Internal terminological consistency choice — both K.μ⁺_L and K.δ extend dom(M) without modifying existing values, and the ASN must adopt one consistent rule. The classification framework is fully present in the ASN's own treatment of K.μ⁺/K.μ⁺_L and the K.δ caveat.

## Issue 3: OrdinalShiftBase description wording
Reason: The reviewer cites ASN-0034's `shift(v, n) = v ⊕ δ(n, #v)` definition directly, and the rephrase is mechanical. ASN-0034 is the canonical formalization already referenced; the fix is to lead with the structural "position #a" reading and demote the "last nonzero" reading to a T4-validity consequence.

## Issue 4: dom_C terminology used without local definition
Reason: Notation gloss against ASN-0047/ASN-0036's existing V_S(d) definition, which is already in the shared vocabulary scope. No external consultation; just add a local gloss `dom_C(M(d)) = V_{s_C}(d)` at first use.

## Issue 5: SV14(d) witness — F' coverage interval boundary
Reason: Expand the D0 / T12 discharge to match the explicit pattern already used in the SV10 witness within this same ASN. The full discharge logic is present and cited elsewhere in the note.

## Issue 6: SV11 multi-block attainment witness — p ≥ 3 case only gestured
Reason: Construction is a mathematical exercise within the ASN's own block-decomposition and span-coverage machinery (M11/M12, S0, S5). Either construct a concrete p = 3 witness or downgrade to a conjectural admission — both options are internal to the existing framework.

## Issue 7: Empty-arrangement boundary for SV11
Reason: Trivial boundary case directly readable off the SV11 formula and biconditional. The p = 0 reading (empty union, vacuous attainment) follows from set algebra and the existing C1a citation.
