# Channel Assignment — ASN-0102 review-13

**Date:** 2026-06-03 14:38

## Issue 1: The "uniqueness" characterization of COPY is false
Reason: Internal fix. The note already states K.μ⁺'s semantics (frame `C'=C`, precondition `a ∈ dom(C)`) in its own "Definition of COPY" section, so the corrected taxonomy and the displacement-based essence are derivable from the ASN's own content plus the already-cited ASN-0047. No design-intent or implementation evidence is at stake — the false claim is a formal over-statement, not a question about what the system meant or does.

## Issue 2: "k = number of maximal contiguous I-runs the source occupies" is imprecise for multi-reference sequences
Reason: Internal fix. The precise picture already lives in X8 (canonical count `≤ k`, equality iff no inter-reference boundary is I-adjacent), and resolution-as-concatenation is ASN-0058 machinery the note already invokes; reconciling the early sentence with X8 is pure self-consistency. No channel needed.
