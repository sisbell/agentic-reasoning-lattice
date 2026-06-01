# Channel Assignment — ASN-0086 review-160

**Date:** 2026-06-01 05:35

## Issue 1: The "K.λ-step preserves substrate-conformance" fact is re-derived in four places instead of being stated once
Reason: Pure consolidation — the propagation fact and its justification already exist in the ASN (the K-op contracts plus the substrate-conforming-state clauses (a)–(c)); naming it once and citing it is derivable from the note's own content.

## Issue 2: Essay content in the "Properties Introduced" table slots
Reason: Editorial relocation — the rationale already lives in the corresponding body sections (Emit_K function-ness lemma, the `→` definition, Observe_K and unit-depth discipline definitions); trimming table cells to the property statement uses only material present in the ASN.

## Issue 3: The `state-local-conforming` domain carries an imprecise, proof-unused reachability conjunct
Reason: Derivable from the ASN — the R0 and Emit_K proofs are present and visibly discharge every conclusion from invariants holding *at* Σ, never from how Σ was reached, so the unused `↝*`-reachable conjunct can be dropped (or `↝` closed) by inspection of the note's own proofs.

## Issue 4: Forward pointer embedded in a lemma statement
Reason: Purely editorial — deleting the navigational pointer from R0's statement requires no external input; the proof subsection heading already serves the purpose.
