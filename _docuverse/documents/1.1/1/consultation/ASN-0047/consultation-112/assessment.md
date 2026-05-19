# Channel Assignment — ASN-0047 review-112

**Date:** 2026-05-19 09:38

```
## Issue 1: K.α and K.λ precondition framing inconsistency
Reason: Fix is derivable from the ASN's own framing — the Notation section's totality convention (`M(d) = ∅` for `d ∉ E_doc`) makes `d ∈ dom(M)` vacuous, and K.μ⁺/K.μ⁺_L/worked examples already use `d ∈ E_doc`. Pure terminological alignment, no external evidence or design intent at stake.
```

```
## Issue 2: K.σ subsumption implicit
Reason: Fix is derivable from the ASN's own content — the *Allocator hierarchy under documents* section already identifies K.δ-for-documents as the "joint T2-spawn step" activating A_C(d) and A_L(d), which is exactly the K.σ role. The fix is to make the subsumption explicit at K.δ's definition; no design intent or implementation evidence is needed beyond what ASN-0093 and ASN-0047 already say.
```

```
## Issue 3: "Amendment postcondition" terminology in verification matrix
Reason: Fix is internal to the ASN — the K.μ⁺ amendment section explicitly states only the `subspace(v) = s_C` clause as added; D-CTG★/D-MIN★ are inherited preconditions from the original K.μ⁺ definition. Pure naming correction in the matrix.
```

```
## Issue 4: "By inheritance" wording for K.α frame
Reason: Fix is derivable from the ASN's own content — ASN-0093's state model has no E or R components (per ASN-0093 itself), so the `E' = E` and `R' = R` conjuncts are necessarily added by ASN-0047, not inherited. Pure wording correction.
```

```
## Issue 5: A_doc vs A_↓ notation interchange
Reason: Fix is purely notational — both names denote the same allocator (when `t` is an account, `A_↓(t) = A_doc(t)`); unification is a stylistic choice with no semantic or evidence question.
```

```
## Issue 6: K.μ~ existence-condition discharge obligation
Reason: Fix is derivable from the ASN's own framing — the *Decomposition of K.μ~* section already derives `|dom_C(M(d))| ≥ 2` as the necessary-and-sufficient existence condition for admissibility clause (iii). The choice between precondition vs. sufficiency obligation is a structural framing decision internal to the ASN's transition discipline, with both readings already supported by the existing derivation.
```
