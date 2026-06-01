# Channel Assignment — ASN-0086 review-120

**Date:** 2026-05-31 23:08

## Issue 1: R0's formal statement quantifies over all states but the proof requires state-local-conformance
Reason: Internal fix. The proof already restricts its discharge to state-local-conforming states and Emit_K/function-ness already scope Σ to that sub-space; aligning R0's (and R5's) quantifier with the conformance hypothesis the proof consumes is derivable from the ASN's own definitions.

## Issue 2: R7a discharge (4)(iii) "Subsequent occurrences" is a case the precondition excludes
Reason: Internal fix. The ASN's own Definition — substrate-conforming state fixes the at-most-one-key-per-home discipline, so Δ holds at most one address per home and no `d_k` repeats; removing the dead subcase is derivable from the ASN alone without consulting design intent or implementation.

## Issue 3: state-local-conforming definition states its witness twice
Reason: Internal fix. Pure editorial deduplication — the witness construction already establishes the separation, so dropping the restatement requires nothing beyond the ASN's own text.
