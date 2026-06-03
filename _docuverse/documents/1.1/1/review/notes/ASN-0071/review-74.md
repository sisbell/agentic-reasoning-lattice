# Review of ASN-0071

## REVISE

### Issue 1: vspec definition contradicts its own precondition list and the empty-source resolution case

**ASN-0071, *The query***: "A vspec is exactly ASN-0058's ContentReference `(d_s, σ)` minus two of its clauses: we drop well-formedness ... and the depth-pinning clause (iii) `#ℓ = #u = m`."

**Problem**: ASN-0058's ContentReference has clause (i) `V_{u₁}(d_s) ≠ ∅` (the source subspace is non-empty). The "minus two clauses" wording keeps clause (i). But:

- The explicit vspec precondition list (`subspace(u) = s_C`, `Pos(ℓ)`, `actionPoint(ℓ) = #u`, `#ℓ = #u`, `actionPoint(ℓ) ≥ 2`) does **not** include `V_{s_C}(d_s) ≠ ∅`.
- *Resolution* then treats `V_{s_C}(d_s) = ∅` as a live case ("If `V_{s_C}(d_s) = ∅` the source carries no content-subspace position ... the intersection is empty"), and **F-DEEP**'s claims-table entry asserts "the companion empty-source case `V_{s_C}(d_s) = ∅ ⟹ iaddrs_one = ∅` holds trivially."

If clause (i) is kept, the empty-source handling and the F-DEEP companion case are dead code (vacuously unreachable). If the empty-source case is genuinely admissible — as Resolution and F-DEEP assume — then clause (i) is dropped, making it **three** clauses dropped, not two, and the precondition list is the authoritative (correct) version while the prose is wrong.

**Required**: Pick one. Either (a) correct the prose to "minus three clauses," explicitly state clause (i) `V_{s_C}(d_s) ≠ ∅` is dropped, and keep the empty-source treatment; or (b) keep clause (i), add `V_{s_C}(d_s) ≠ ∅` to the precondition list, and remove the now-vacuous empty-source branch and the F-DEEP companion case. As written the definition is internally inconsistent.

## OUT_OF_SCOPE

### Topic 1: relationship to provenance relation R and rejection-vs-filter policy
**Why out of scope**: The three Open Questions (currency-vs-`R` guarantee, when to reject unresolvable vspecs, contraction-boundary invariant) are genuinely new territory — operations/invariants this query ASN need not settle. Correctly parked.

VERDICT: REVISE
