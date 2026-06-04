# Review of ASN-0087

## REVISE

### Issue 1: LP-Sub miscited to establish `ℓ ∈ F` for the fresh address

**ASN-0087, *Inputs* (Fresh-address exclusion, M-FreshExcl)**: "The fresh link address `ℓ ∈ F` (it is an `A_L(d)` emission of the form `[d, 0, s_L, k]`, LP-Sub)."

**Problem**: LP-Sub (ASN-0098) states `dom(Σ.C) ∪ dom(Σ.L) ⊆ F` — its quantifier ranges over addresses *already in the stores*. But `ℓ` is fresh by construction: `ℓ ∉ dom(Σ.C) ∪ dom(Σ.L)`. LP-Sub therefore says nothing about `ℓ`, and cannot supply either the structural form `[d, 0, s_L, k]` or membership in `F` for a non-stored address. M-FreshExcl is the keystone of the standard-authoring exclusion; it is re-invoked downstream (the *Side Effects* backward-freshness-transfer argument applies M-FreshExcl at `Σ_{ℓ'}`), so the miscitation propagates.

**Required**: Justify `ℓ ∈ F` from the correct premises: `ℓ` is an `A_L(d)` emission, so FirstEmission / ChainDiscipline (ASN-0093) fix its form `[d, 0, s_L, k]`; `origin(ℓ) = d` with `d` T4-valid and `zeros(d) = 2` by M0 (ASN-0093); F's definition then yields `ℓ ∈ F`. Replace the LP-Sub tag with these citations.

### Issue 2: Scope mismatch when M-FreshExcl is reused on a prior link

**ASN-0087, *Side Effects on Prior Links' Discoverability***: "M-FreshExcl (*Inputs*), applied at `Σ_{ℓ'}` with this transferred freshness, then gives `ℓ ∉ coverage(Σ.L(ℓ').eᵢ)`."

**Problem**: M-FreshExcl as stated in *Inputs* is phrased specifically about "the fresh link address `ℓ`" of the *current* operation and its *own* endsets `eᵢ`. Here it is applied to a *prior* link `ℓ'`'s endsets at an *earlier* authoring state `Σ_{ℓ'}`, with `ℓ` playing the role of the fresh F-address against a different endset. The underlying logic is general, but the lemma's stated carrier is operation-specific, so the application is a silent generalization.

**Required**: State M-FreshExcl generically — for any `x ∈ F` with `x ∉ dom(Σ.C) ∪ dom(Σ.L)` and any endset `e` with `StandardAuthoring(e, Σ)`, `x ∉ coverage(e)` — so both the home-link use and the prior-link reuse are instances of the same stated form.

## OUT_OF_SCOPE

The Open Questions appropriately defer endset well-formedness for unallocated targets, value-equal-link distinctness, deferred-consistency, and protocol-layer atomicity bounds — all genuinely future territory, not gaps in this ASN.

VERDICT: REVISE
