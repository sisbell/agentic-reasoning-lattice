# Review of ASN-0071

I read this as Dijkstra would: hunting for the skipped case, the checkmark masquerading as a proof, the invariant conjunct left unaddressed. I did not find one. Below is what I checked and why each holds.

## Proofs verified

**Prefix confinement (PC) — the load-bearing argument.** The totality sub-argument (`#t ≥ #u` for every `t ∈ ⟦σ⟧`) is correctly separated from the componentwise argument, and its two sub-cases (proper-prefix via T1 case (ii); first-disagreement at `p ≤ #t < #u` via case (i)) are exhaustive and each reaches contradiction. The prefix-copy fact `(u⊕ℓ)_j = u_j` for `j < actionPoint(ℓ) = #u` is applied only where `j < #u`, where it is valid. The position-1 instance (subspace confinement) follows and is correctly reused for S3★ routing.

**The `actionPoint(ℓ) = #u` tightening.** The interior-action-point over-collection (`σ' = ([s_C,1,2], [0,1,0])` capturing positions 2..n) is computed correctly — reach `[s_C,2,2]`, intersection `{[s_C,1,2],...,[s_C,1,n]}` — and the precondition rejects it (`2 ≠ 3`). The contrast with cross-depth subtree capture (depth-wise vs sideways) is principled, not hand-waved: PC pins the prefix, so only component `#u` and below vary.

**Resolve-equivalence.** The reduction to ASN-0058 C1a/B1/B3 is shown step by step, and set-flattening dedup is exercised concretely by the three-block `σ_D` example where `β₁, β₃` both carry `a₁` (M16 cross-origin blocks the merge). This is the multi-block case the singleton query could not reach.

**Boundary cases.** Empty query (`find(∅) = ∅`, vacuous wp-defined), infinite span filtered to finite intersection (F-FILT), exclusion against a concrete non-containing `d_C` (F-SOUND negative direction), currency under K.μ⁻ contraction (F-CUR), and finiteness via `Σ₀.E_doc = ∅` + K.δ-adds-≤1 + finite composite ancestry — all present and correct.

**Foundation discipline.** Every numbered cross-reference is to ASN-0047/0053/0058. Tumbler primitives (TumblerAdd, T0, T1, δ, actionPoint) are used by name, not by foreign ASN number. No reinvented notation.

**Currency derivation.** `find` is correctly shown to read only `E_doc` and `M`, never `dom(C)` or content values; the permanence/currency reconciliation honestly flags versioning as convention, not structural guarantee, and defers history to `R`.

## OUT_OF_SCOPE

The deep-vspec direction `#u > m` is not given a worked example, but it is benignly handled by F-FILT (every `t ∈ ⟦σ⟧` has depth `≥ #u > m`, so the intersection with `dom(M(d_s))` is empty). This is covered by the general mechanism, not a gap. The historical-`R` query, visibility filtering, replica freshness, and the cross-transition contraction invariant are correctly deferred to the Open Questions.

META: not applicable — the ASN defines an abstract query as a pure function of state with completeness/soundness as conformance obligations, squarely a system guarantee rather than implementation mechanics.

VERDICT: CONVERGED
