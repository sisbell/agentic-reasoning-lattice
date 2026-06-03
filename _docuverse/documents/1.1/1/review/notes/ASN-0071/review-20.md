# Review of ASN-0071

## REVISE

### Issue 1: PC proof omits the case where `t` is shorter than `#u`

**ASN-0071, "The query" (PC derivation)**: "Were `t` to first disagree with `u` at some prefix position `p < #u`, then since `u_p = (u ⊕ ℓ)_p`, T1 case (i) at `p` would force either `t < u` ... or `t > u ⊕ ℓ` ...; by NAT-order trichotomy (T0) no such `p` exists, so `t_j = u_j` throughout `1 ≤ j < #u`."

**Problem**: The argument only rules out componentwise disagreement (T1 case (i)). It never rules out the case where `t` is a *strict prefix* of `u` (depth `< #u`), where the components `t_j` for `j` near `#u` simply do not exist. The universal conclusion "`t_j = u_j` throughout `1 ≤ j < #u`" is not even well-defined for such a `t`. To make the prefix claim total over `1 ≤ j < #u`, you must first establish that every `t ∈ ⟦σ⟧` has depth `≥ #u`. This follows — a `t` shorter than `u`'s prefix is a proper prefix of `u`, hence `t < u` by T1 case (ii), contradicting `u ≤ t` — but it is the T1 *case (ii)* exclusion, which the proof skips entirely while invoking only case (i).

**Required**: Add the case-(ii) step: any `t ∈ ⟦σ⟧` with depth `< #u` would be a proper prefix of `u` (agreeing on its whole length), giving `t < u` and contradicting `u ≤ t`; therefore every `t ∈ ⟦σ⟧` has depth `≥ #u` and `t_j` is defined for all `1 ≤ j < #u`. Then the case-(i) argument discharges the claim.

### Issue 2: `find` typed as a total function but is partial

**ASN-0071, Claims Introduced table (F-find)**: "`find : VSpecSet × Σ → P(E_doc)` ... defined under the precondition `(A (d_s, σ) ∈ Q :: d_s ∈ Σ.E_doc)`"

**Problem**: The total arrow `→` contradicts both the companion definition F-iaddrs (correctly typed `⇀`, partial) and the body, which states "We make this explicit as the *domain of the partial function* `find`" and "`find(Q)(Σ)` is defined precisely when this precondition holds." A function that is undefined outside `wp-defined` is partial; typing it total is a precision error in a formal signature.

**Required**: Change the F-find signature to `find : VSpecSet × Σ ⇀ P(E_doc)`, matching F-iaddrs and the prose.

## OUT_OF_SCOPE

### Topic 1: Relationship between `find`'s current result and the provenance relation `R`
**Why out of scope**: The ASN correctly defers the currency-vs-history reconciliation to a future ASN (first Open Question); `R`-based "ever-containing" queries are new territory, not a defect here.

### Topic 2: Visibility filtering and distributed-replica completeness
**Why out of scope**: Explicitly listed under "What we do not specify" and the Open Questions; these are separable policy/consistency layers, not gaps in the present definition.

VERDICT: REVISE
