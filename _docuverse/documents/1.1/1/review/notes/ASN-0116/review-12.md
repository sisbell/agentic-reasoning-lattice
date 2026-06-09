# Review of ASN-0116

## REVISE

### Issue 1: The arrangement step is not exhibited as an ASN-0047 atomic transition, yet ValidComposite is relied upon

**ASN-0116, "What is allocated…" / INSERT Effect**: "INSERT is the composite of `n` content allocations (K.α, ASN-0093), one arrangement transition realising the post-insertion shift of ASN-0082's I3 family, and `n` provenance recordings (K.ρ, ASN-0047)."

**Problem**: ASN-0047's `ValidComposite★` admits only the atomic vocabulary `{K.α, K.δ, K.λ, K.μ⁺, K.μ⁺_L, K.μ⁻, K.ρ}` (K.μ~ as a named K.μ⁻+K.μ⁺ composite). There is no "I3 transition" in that vocabulary. K.α and K.ρ are genuine atomics, but the I3 shift is not a single ASN-0047 atomic, and as a single transition it matches none of them:

- It changes the value at *existing* positions — `M(d)(q_J) = a_J` becomes `M'(d)(q_J) = a` (the content `a_J` moves to `q_{J+n}`). K.μ⁺ explicitly forbids this: `(A v : v ∈ dom(M(d)) : M'(d)(v) = M(d)(v))`. The ASN itself concedes this in P6 ("INSERT is not a pure extension… I-SHIFT violates [prior-domain agreement] by vacating every suffix position `v ≥ p`").
- It strictly grows the domain (`{q_1,…,q_N} → {q_1,…,q_{N+n}}`), so it is neither K.μ⁻ nor K.μ~ (the latter requires `dom(M'(d)) = dom(M(d))` by K.μ~-FIX).

Because the ASN nonetheless invokes ASN-0047's machinery wholesale — `ExtendedReachableStateInvariants` for the post-state, the coupling constraints J0/J1★/J1'★ "for the composite," and ValidComposite clause (2) to argue PROV — the central soundness claim depends on INSERT actually being a valid composite over the K-vocabulary. That decomposition is never shown. Citing ASN-0082's I3 (a displacement *postcondition* spec, not a K-transition) does not place INSERT inside ASN-0047's reachable-state machinery.

A corollary gap: ValidComposite clause (1) requires each atomic step's precondition to hold at the *intermediate* state (e.g., a K.μ⁺ installing I-NEW requires the referenced `A_new` addresses to already be in `dom(C)`; each K.ρ requires its target in `dom(C')`). The ASN never fixes a sub-step ordering or discharges these intermediate preconditions.

**Required**: Exhibit the arrangement change as an explicit finite sequence of ASN-0047 atomics — e.g. `K.α(×n)` → `K.μ⁻` (contract to the prefix `{q_1,…,q_{J-1}}`) → `K.μ⁺` (re-extend with the shifted suffix and the new block referencing `A_new`) → `K.ρ(×n)`, or `K.α(×n)` → `K.μ⁺` (append `n` top slots → `A_new`) → `K.μ~` (permute) → `K.ρ(×n)`. State the ordering, verify each intermediate precondition (clause 1), and confirm the coupling constraints (clause 2) only at the composite boundary — which the existing range-new = `A_new` argument already supports. Until the K-vocabulary decomposition is given, the appeal to ExtendedReachableStateInvariants and to ValidComposite is not established.

## OUT_OF_SCOPE

(none beyond the Open Questions, which are appropriately posed as questions rather than claims)

VERDICT: REVISE
