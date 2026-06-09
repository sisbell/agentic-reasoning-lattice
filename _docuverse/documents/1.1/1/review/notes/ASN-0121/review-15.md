# Review of ASN-0121

## REVISE

### Issue 1: FL-WP(a) discharges addressability with an invalid inference

**ASN-0121, FL-WP part (a)**: "The addressability conjunct is discharged by freshness: `ℓ ∉ dom(Σ.L)`, and an ordinary K.λ does not emit a retraction tuple targeting `ℓ`, so `ℓ ∉ nullified(Σ')` and hence `ℓ ∈ addressable(Σ')` unconditionally."

**Problem**: The inference from "`ℓ` is fresh" + "the *new* tuple does not target `ℓ`" to "`ℓ ∉ nullified(Σ')`" is invalid. `nullified(Σ')` is defined (ASN-0086) over *all* retraction tuples in `L_R^{Σ'}`, and for an ordinary K.λ, `L_R^{Σ'} = L_R^Σ`. So

  `nullified(Σ') = nullified(Σ) ∪ ({ℓ} if (E (b, F', G') ∈ L_R^Σ :: ℓ ∈ coverage(G')))`.

Because endset coverage may name ghost addresses (ASN-0086 L4/L9 EndsetGenerality, R5, and the orphan/resurrection regime of ASN-0098 LP17/LP18), a *pre-existing* retraction tuple's to-coverage `coverage(G')` can already contain the future address `ℓ`. Freshness against `dom(Σ.L)` does not exclude this. In that case `ℓ ∈ dom(Σ'.L)` and `ℓ ∈ coverage(G')`, so `ℓ ∈ nullified(Σ')` and `ℓ ∉ findlinks(q, Σ')` *even though* `sat(ℓ, q, Σ')` holds. The wp is then not the bare four-way conjunction displayed.

This is precisely the concern the foundation already carries: ASN-0086's wp Case 2 (EmitKWeakestPrecondition) includes the third conjunct `¬(E (b, F', G') ∈ L_R^Σ :: a_emit(Σ, d) ∈ coverage(G'))` for exactly this reason. FL-WP(a) is the direct analogue and drops it.

**Required**: Add the addressability conjunct to FL-WP(a):

  `wp(K.λ, ℓ ∈ findlinks(q, ·)) ≡ ℓ ∉ nullified(Σ') ∧ liftH_d(q.H) ∧ lift(F, q.F) ∧ lift(G, q.G) ∧ lift(Θ, q.Θ)`,

where `ℓ ∉ nullified(Σ') ≡ ¬(E (b, F', G') ∈ L_R^Σ :: ℓ ∈ coverage(G'))`. Either keep this conjunct explicitly, or invoke a stated discipline (as ASN-0086's "disciplined-domain simplification" does) under which no pre-existing retraction tuple covers the freshly allocated address, and show that discipline holds here — but it cannot simply be asserted to "drop out unconditionally."

## OUT_OF_SCOPE

(none)

VERDICT: REVISE
