# Channel Assignment — ASN-0102 review-2

**Date:** 2026-05-28 14:17

## Issue 1: Operation effect on state components L, E, R is unspecified
Reason: Internal. The frame is derivable from COPY's own model — it touches neither the link store nor `Σ.E`, so `Σ'.L = Σ.L` and `Σ'.E = Σ.E` follow from the definition's content/arrangement-only effect; the `Σ.R` effect is settled under Issue 2.

## Issue 2: The coupling invariant J1★ is never discharged
Reason: Internal. J1★ (ASN-0047) is a coupling invariant binding *every* valid composite that extends the content-subspace range, so COPY is not exempt; the required K.ρ effect and discharge are forced by the foundation, and the matching implementation evidence (spanfilade recorded against destination) is already cited at X14 (Gregory Q18/Q19).

## Issue 3: COPY's transition status (elementary vs. composite) is left undeclared
Reason: Internal. The classification is a modeling decision over ASN-0047/0093's transition vocabulary: K.μ⁺'s old-position-fixity rules out a single ArrangementExtension, and the note already states the displacement is identical to INSERT's, so COPY inherits whatever transition shape INSERT is given in the foundation — resolvable from the foundation without external input.

## Issue 4: X8's claim that distinct references carry distinct origins is false
Reason: Gregory needed. Correcting the constructed-count claim requires confirming exactly when `docopy`/`isanextensionnd` coalesces across a reference boundary — specifically the shared-origin, I-adjacent case the reviewer flags — so the revised text states the implementation's agreement only where it actually holds.
Gregory question: When two consecutive content references in a single COPY resolve to content sharing one origin (equal `homedoc`) and abutting in I-space across the boundary, does `docopy`/`insertspanf` (via `isanextensionnd`) coalesce them into one crum, or still emit a separate crum per reference?

## Issue 5: First Open Question appears already answered by X10/X15
Reason: Internal. This is a self-consistency fix: X10 and X15 already pin `resolve_Σ(R)` to the frozen pre-state for the target-inside-source case, so the question is either removed or narrowed to a residual guarantee — entirely a judgment over the note's own content.
