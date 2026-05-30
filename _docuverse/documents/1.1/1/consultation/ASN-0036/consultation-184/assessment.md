# Channel Assignment — ASN-0036 review-184

**Date:** 2026-05-29 22:06

## Issue 1: S8 was not restored to the correspondence-run form — the central instruction of the patch
Reason: The correspondence-run decomposition is a mathematical restructuring of S8 using machinery already present in the ASN (ord/vpos/w_ord, OrdAddHom, OrdShiftHom, ShiftPreservation) and the displacement identity stated in the section intro and Open Questions. Constructing maximal runs by forward/backward extension and proving partition/uniqueness is derivable from the ASN's own definitions — no design intent or implementation evidence is needed.

## Issue 2: Section intro asserts run structure that S8 does not deliver
Reason: Once S8 is restored (Issue 1), the prose and the maximal-decomposition Open Question are reconciled by internal consistency alone. This is editorial alignment derivable from the ASN's own content.

## Issue 3: Worked example does not exercise conjunct (b) at `k ≥ 1`
Reason: Exhibiting the displacement identity `M(d)(shift(vⱼ, k)) = shift(aⱼ, k)` on the existing "hello" run and the Σ₂ transclusion/append boundary is a direct computation on tumblers already tabulated in the example — fully internal.

## Issue 4: Newly added claims are absent from the Properties Introduced registry
Reason: Adding registry rows (with types and dependency notes) for S7c, ShiftPreservation, ord, vpos, w_ord, OrdAddHom, OrdAddS8a, OrdShiftHom, subspace_I is a mechanical bookkeeping task derivable from the definitions already in the document.

## Issue 5: Ordinal-decomposition lemmas are orphaned (no downstream consumer)
Reason: Whether the restored S8 proof cites OrdShiftHom (lockstep displacement) and ShiftPreservation (structural inheritance along a run) is determined entirely by the proof construction in Issue 1 — an internal dependency-wiring question with no need for external channels.
