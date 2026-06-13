# Channel Assignment — ASN-0133 review-8

**Date:** 2026-06-13 13:45

## Issue 1: The fire-sequence model is closed, which trivializes Q5a's "route" and the worked example's conditionality
Reason: This is a formal-modeling decision — whether `σ` admits non-registry `→_sh` steps — about the substrate's own transition relation (ASN-0128) and how it relates to the registry's fire sequence, not Xanadu design intent or udanax-green behavior. The reviewer has fully derived both branches (open re-statement vs. closed model with `bounded-domain-growth ⟺ H-RF` and an unconditional worked example), so the fix is internal: pick the model the substrate's own `→_sh` semantics support and align Q5/Q5a/Q6 and the example accordingly.

## Issue 2: H-FIN is stated as an existential where the operative reading is universal
Reason: Pure formalization error internal to the note — H-FIN's "admits (∃) a finite emission set" contradicts the universal-over-choices reading RG states one sentence later ("terminates iff *every* `Post_ρ`-satisfying fire sequence it can produce does"). The correction (restate H-FIN as ∀) is fully determined by the note's own content; no external channel is needed.
