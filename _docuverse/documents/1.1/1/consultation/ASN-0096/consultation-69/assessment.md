# Channel Assignment — ASN-0051 review-69

**Date:** 2026-05-17 19:52

## Issue 1: The (m=1, p ≥ 4) inductive lift recipe is broken against its stated base
Reason: The fix is mathematical/structural — either replace the (m=1, p=3) base witness with one whose blocks have interior positions, change the recipe, or state direct construction. All paths are derivable from the ASN's own decomposition machinery and ASN-0058's block algebra; no design intent or implementation evidence needed.

## Issue 2: SV11 W(m,p) "boundary lift" verifications under-specify the V-arena extension
Reason: The fix is to align the lift prose with the framing note (lifts are independent constructions, not state modifications) and discharge against D-SEQ from ASN-0036. Pure internal/foundation clarification.

## Issue 3: SV13(e) penultimate parenthetical conflates K.μ⁺ and K.μ⁺_L frames
Reason: Editorial cleanup — remove redundant parenthetical or relocate to SV4-isolation. Derivable from the ASN's own bullet structure and K.μ⁺_L's effect already cited from ASN-0047.

## Issue 4: SV10 witness implicitly requires K.λ adds Σ.L(a) consistently with L3's arity-3 floor
Reason: The fix adds T4-validity and T12 verification annotations to the existing witness components. All checks are direct applications of T4 (ASN-0034) and T12 (ASN-0034) already in scope; the W(2, 2) explicit-verification subsection supplies the model.

## Issue 5: NoStaleResolutionState — schema-closure argument under-specifies the "no auxiliary V-cache field" claim
Reason: The fix is a framing decision (present-state property vs. forward closure obligation), both options derivable from the ASN's own schema discussion of ASN-0047's Σ = (C, L, E, M, R).

## Issue 6: SV11 attainment witness W(2,2) — "corner case" claim lacks a lift mechanism justification
Reason: The fix is checking whether the (α_2) offset arithmetic ({5, 7, ..., 2m+3} in β₁, {0, 2, ..., 2m−2} in β₂) is degenerate at m=2, or re-parameterising W(2, 2) to fit the W(m, 2) template. Purely internal mathematical verification.

## Issue 7: Worked Example three-span variant cites unallocated tumbler existence without discharging T0(a) preconditions
Reason: The fix adds a one-line foundation citation chain (T0(a) + OrdinalShiftBase + TA5a/T4 preservation) from ASN-0034, all already cited elsewhere in this ASN. Pure foundational citation cleanup.
