# Review of ASN-0120

This is a strong, mature ASN. The central thesis — MAKELINK is a V→I coordinate conversion, and survivability/immutability/residence-independent discoverability all fall out of recording at the identity level — is well-argued, with the confinement step (ordinal-displacement ⟹ T5 ⟹ `t₁ = s_C`), the `#E = 2` exactness argument, an explicit wp derivation, and a worked example all present. The issues below are precision/rigor nits in load-bearing proofs, not structural defects.

## REVISE

### Issue 1: `subspace_I` asserted where it is undefined
**ASN-0120, ML9 Fact (a) / Fact (b)**: "every covered tumbler carries `subspace_I = s_C`" and "coverage(eᵢ) and its surplus lie in content subtrees (subspace s_C) … so every covered tumbler carries `subspace_I = s_C`".
**Problem**: `coverage(eᵢ) = ∪{t : aₖ ≼ t}` includes surplus descendants formed by extending a resolved address with a *zero* component, giving `zeros(t) = 4` — not T4-valid. The foundation defines `subspace_I` (ASN-0043) only on T4-valid tumblers with `zeros = 3`, so `subspace_I` is undefined on those covered tumblers. The proof asserts a partial function's value across a set where it does not apply.
**Required**: Re-route the conclusion through store membership rather than `subspace_I` over all covered tumblers. The fact actually needed is `coverage(eᵢ) ∩ (dom(Σ.C) ∪ dom(Σ.L)) = ρ(R_i, Σ)`: the content part is `ρ` by ML2, and `coverage(eᵢ) ∩ dom(Σ.L) = ∅` because any link `ℓ` with `aₖ ≼ ℓ` would inherit `E(ℓ)₁ = E(aₖ)₁ = s_C ≠ s_L`. Both halves use only facts already established; state them over store membership, not over `subspace_I` of arbitrary covered tumblers.

### Issue 2: K.μ⁺_L preconditions not discharged
**ASN-0120, "Residence" section**: "the link *reference* enters the home document's arrangement in the link subspace, via `K.μ⁺_L` (ASN-0047): a fresh link-subspace V-position `v_a` of `d` is bound to `a`".
**Problem**: MAKELINK is the composite `K.λ` then `K.μ⁺_L`, yet the ASN invokes K.μ⁺_L without showing its elementary precondition holds at the intermediate state — specifically `ℓ ∈ dom(L)`, `origin(ℓ) = d`, `ℓ ∉ ran(M(d))`, and a well-formed `v_ℓ` (ASN-0047, K.μ⁺_L). Operations are where specifications fail, and a composite whose second step's precondition is never discharged is incomplete.
**Required**: Add a sentence discharging these: post-`K.λ`, `a ∈ dom(Σ.L)` and `origin(a) = home(a) = d` (ML0); `a ∉ ran(M(d))` follows from freshness (`a ∉ dom(Σ.L)` and the link-subspace range lies in `dom(Σ.L)` by S3★/CL-OWN); the V-position is selected by K.μ⁺_L's own `ValidFirstLinkPosition`/`shift(max(V_{s_L}(d)),1)` clause. One line closes it.

### Issue 3: Open Question 3 is already answered by the ASN
**ASN-0120, Open Questions**: "What invariant must hold so that two MAKELINK calls supplying identical endset arguments and identical home necessarily produce distinct link identities rather than coalescing?"
**Problem**: ML0 (fresh, never-reused address from `A_L(d)`) together with SubsequentEmissionFreshness (ASN-0093) and the R2 consequence (ASN-0086 — identical `(F,G)` under identical `K` produce distinct addresses) already guarantee this. Posing it as open suggests a gap the ASN has in fact closed.
**Required**: Either remove the question or convert it to a stated consequence ("distinct identities are guaranteed by ML0 freshness; value-coincidence is permitted by L11b but address-coincidence is excluded").

## OUT_OF_SCOPE

### Topic 1: Type-as-content modeling commitment
ML6 forces the type argument to `ρ`-resolve into `dom(Σ.C)` (active content), so MAKELINK never exercises L9's ghost-type permission. Whether types should instead inhabit a dedicated type space — and an operation that mints ghost-type references — is a separate question the ASN deliberately and consistently sets aside. The Open Question on link-subspace endsets partially anticipates it.

VERDICT: REVISE
