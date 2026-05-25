# Channel Assignment — ASN-0051 review-46

**Date:** 2026-05-16 04:55

## Issue 1: SV5's π-invariance claim is asserted, not derived
Reason: Pure editorial fix — the derivation uses L12 (coverage invariance) and K.μ~'s ran-preservation, both already established in the ASN. No external input needed.

## Issue 2: `discover_s(A)` state-dependency notation is inconsistent
Reason: Notation convention choice internal to the ASN. Picking one form and applying uniformly is a mechanical edit; no design intent or implementation evidence bears on the choice.

## Issue 3: TransclusionCouplingAbsence headline overstates the absence
Reason: The K.ρ coupling requirement comes from ASN-0047's J1★, already cited in the body's closing paragraph. Lifting it into the headline is internal restructuring.

## Issue 4: SV13(g) is missing the state-dependence qualifier in the headline
Reason: SV11's body already contains the "m · p is state-dependent" caveat; SV13(g) just needs the qualifier propagated into its headline. Pure synthesis-consistency edit.

## Issue 5: SV6's scope not summarised in SV13(f)
Reason: SV6's body already carefully delimits scope to element-level b with deferral of broader-level spans to ASN-0034. The fix is to mirror that scope in SV13(f)'s headline — internal cross-reference cleanup.
