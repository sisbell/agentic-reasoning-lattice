# Channel Assignment — ASN-0069 review-13

**Date:** 2026-05-25 16:43

## Issue 1: V11 stated with a stronger premise than the derivation requires
Reason: The fix is internal — promoting an already-stated tightened premise (present in the existing Remark) to be V11's primary form. The derivation already reads only content-subspace state, so the looser premise is established by the existing proof; no design-intent or implementation question is involved.

## Issue 2: V8b non-monotonicity discussion does not justify exhaustiveness
Reason: The fix is internal — the frame conditions of K.α, K.λ, K.μ⁺_L, K.ρ, K.δ on `M` are defined in ASN-0047, which this ASN already cites extensively. Exhaustiveness follows mechanically from those frame conditions; no design intent or implementation evidence is needed.

## Issue 3: V0 Effects-table annotation for the R' set equality uses awkward notation
Reason: Pure notation/presentation fix. The verification section already establishes the set equality with proper sequential composition; only the table annotation needs rephrasing. No external channels needed.

## Issue 4: V4b's derivation forward-references V0
Reason: Pure presentation/ordering choice between two internally consistent formulations (V4b as derived from V0, or V4b as primary with V0 restating it). Either presentation uses content already in the ASN; no design or implementation question is involved.
