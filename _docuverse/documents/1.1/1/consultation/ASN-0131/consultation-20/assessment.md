# Channel Assignment — ASN-0131 review-20

**Date:** 2026-06-13 17:13

## Issue 1: "insertion"/"deletion" glosses misdescribe the frontier-restricted atomics they label
Reason: The fix re-characterizes the formal atomics using foundation facts already cited in the note — K.μ⁺/K.μ⁻ semantics and the D-CTG/D-SEQ canonical form (ASN-0047), the weak `⊆` of F-IMG-MONO/CONTR (ASN-0127), and the shift-based displacement as an ASN-0082 composite (I3/D-SHIFT). This is correcting the prose to match the spec's own transition model, not a question of design intent or implementation behaviour.

## Issue 2: the Open-Question-6 deferral and its conditional are restated multiple times (anti-bloat)
Reason: Pure editorial deduplication — collapsing the thrice-stated OQ6 deferral and the twice-stated under-it/absent-it conditional to a single telling. Entirely internal to the note's prose; no design intent or implementation evidence bears on it.
