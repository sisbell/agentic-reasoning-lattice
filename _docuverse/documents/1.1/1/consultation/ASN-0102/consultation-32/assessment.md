# Channel Assignment — ASN-0102 review-32

**Date:** 2026-06-07 22:03

## Issue 1: The discriminating merge behavior (X8, X12) is stated but never exercised by any worked example
Reason: Internal. Constructing a worked example where an inter-reference boundary coalesces and a leading/trailing boundary absorbs requires only the merge predicates (M7/M16) and absorption conditions already stated in X8/X12, instantiated with concrete I-adjacent same-origin addresses. No design intent or implementation evidence is needed — the firing conditions are fully specified in the note.

## Issue 2: X8's within-reference non-coalescence re-derives a guarantee `resolve` already supplies
Reason: Internal. The note already cites ASN-0058 C1a/M12 as defining `resolve` to return the maximally-merged decomposition; replacing the re-derivation with a one-line citation to that established fact draws entirely on references the ASN already invokes.
