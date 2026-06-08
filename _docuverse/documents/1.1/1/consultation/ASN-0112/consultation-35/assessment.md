# Channel Assignment — ASN-0112 review-35

**Date:** 2026-06-08 10:57

## Issue 1: Purity asserted in prose but never recorded as a claim
Reason: The no-mutation guarantee is already stated in the ASN's prose ("observes the state and returns a value, changing nothing") and follows directly from the operation being typed as a pure query over `Σ`; formalizing it as `V-frame: Σ' = Σ` is internal bookkeeping, not a new fact requiring design intent or implementation evidence.

## Issue 2: V14 re-derives V6 inline rather than citing it
Reason: This is a purely editorial fix — replacing a restatement of V6's conclusion with a bare pointer to V6 — derivable from the ASN's own claim structure with no external input.
