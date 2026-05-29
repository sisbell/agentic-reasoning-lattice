# Channel Assignment — ASN-0040 review-104

**Date:** 2026-05-29 04:24

## Issue 1: s.B-frame dispatch carries forward-looking proof-method prose
Reason: Purely a prose deletion within B0a — removing use-site rationale while keeping the named shorthand. No design intent or implementation evidence is involved; the proofs already state the load-bearing claim where used.

## Issue 2: B8 silently weakens the foundation's global uniqueness without motivating the restriction
Reason: The fix adds a one-sentence acknowledgment that co-reachability coincides with global uniqueness under linear history, pointing to the cross-replica open question already present in this ASN. Both the proof's reliance on single-path linearity and the deferral target are internal content.

## Issue 3: forward reference to B₀ conf. in the registry definition
Reason: Removing a forward pointer and relocating the conformance statement to B₀ conf. is a self-contained editorial move; both the s.B definition and B₀ conf. are present in the ASN.
