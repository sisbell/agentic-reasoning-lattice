# Regional Review — ASN-0034/TA5 (cycle 3)

*2026-04-23 01:33*

### "m ≥ 2 ≥ 1" overspecified in TA5-SIG max derivation
**Class**: OBSERVE
**ASN**: TA5-SIG, contradiction branch within the max derivation: *"Fixing any `i₀ ∈ S` — `S ≠ ∅` supplies such a witness — we have `i₀ ≥ 1` (since `S ⊆ {1, …, #t}`), and `i₀ + 1 ≤ m` then yields `m ≥ 2 ≥ 1`"*
**Issue**: Only `m ≥ 1` is subsequently used (as the precondition for NAT-sub's conditional closure). The claim `m ≥ 2` requires NAT-addcompat's right order compatibility at `(1, i₀, 1)` to lift `1 ≤ i₀` to `1 + 1 ≤ i₀ + 1`, plus a convention for the numeral `2` (which NAT-closure does not posit). The derivation of `m ≥ 1` is cleaner via `1 ≤ i₀ < i₀ + 1 ≤ m` (strict successor + mixed transitivity). The "≥ 2" step is stronger than required and its derivation unstated.

### "Mirrored argument" in T1 Trichotomy Case 3
**Class**: OBSERVE
**ASN**: T1 trichotomy Case 3, closing of the case split: *"If `n < m`, the mirrored argument gives `b < a`."*
**Issue**: Symmetric by construction, but the review discipline asks that proofs walk every case. The "mirrored argument" must re-establish: (1) `k = n + 1 ≤ m` witnesses `b < a` via T1(ii), and (2) no reverse witness for `a < b` exists — where the sub-argument for (2) uses `aⱼ = bⱼ` at shared positions and the `n < m` direction of trichotomy. The mirror is legitimate, but spelling out the shape (particularly that no reverse witness exists) would match the rigor applied to the `m < n` branch.

### TA5 postcondition uses `k − 1` without NAT-sub in Depends
**Class**: OBSERVE
**ASN**: TA5 statement (d) and *Postconditions* bullet: *"the `k - 1` intermediate positions `#t + 1, ..., #t + k - 1` are set to `0`"*; *"(d) When `k > 0`: `#t' = #t + k`, positions `#t + 1 ... #t + k - 1` are `0`"*
**Issue**: The expressions `k − 1` and `#t + k − 1` presuppose subtraction on ℕ. TA5's Depends slot does not cite NAT-sub (it is available transitively through TA5-SIG, but not declared here). The postcondition is equivalently expressible without subtraction as the range `{i : #t + 1 ≤ i < #t + k}`, which requires no operator beyond those already cited. The current wording uses subtraction as informal notation while the postcondition slot is the place where operator grounding is auditable.

### Existence-of-`cₖ₁` inference in T1 Transitivity Case `k₁ < k₂`
**Class**: OBSERVE
**ASN**: T1 part (c), Case `k₁ < k₂`: *"If `a < b` via T1(i): `aₖ₁ < bₖ₁ = cₖ₁` with `k₁ ≤ m`, and the existence of `cₖ₁` gives `k₁ ≤ p`"*
**Issue**: "The existence of `cₖ₁` gives `k₁ ≤ p`" runs the inference backwards: `k₁ ≤ p` is what justifies `cₖ₁` being a well-formed projection, not a consequence of it. The step is sound by other means — from `k₁ < k₂` and either `k₂ ≤ p` (b < c via (i)) or `k₂ = n + 1 ≤ p` (b < c via (ii), then NAT-discrete + mixed transitivity) — but the phrasing as given presents the conclusion as its own justification.

VERDICT: OBSERVE

## Result

Regional review converged after 3 cycles.

*Elapsed: 1702s*
