# Channel Assignment — ASN-0047 review-274

**Date:** 2026-06-01 18:27

## Issue 1: "K.μ~ range-invariance" jumps from content-range equality to full-range equality without the link step
Reason: The fix re-wires an existing derivation using facts already present in the ASN — content-range equality (shown inline) plus the link-subspace functional identity `M'(d)|_{dom_L} = M(d)|_{dom_L}` from sub-step (3) of the link-subspace fixity proof. No design intent or implementation evidence is needed.

## Issue 2: Worked-example slot carries proof-architecture essay rather than verification
Reason: Purely editorial deletion — remove the per-state/composite-boundary classification essay (already stated in the preamble) and retain the concrete checks plus one sentence on P4★ restoration. Fully internal to the ASN.
