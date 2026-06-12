# Review of ASN-0120

## REVISE

No REVISE items. The load-bearing chains were checked individually rather than taken on trust; recording what was verified so the verdict is earned, not asserted:

- **Subspace confinement of ρ.** `wf`'s `m ≥ 2` is exactly what makes the length-`(m−1)` prefix non-empty; OrdinalShift fixes both interval endpoints on positions `1..m−1`, T5's preconditions (`#p ≥ 1`, `p ≼ u_j`, `p ≼ u_j ⊕ ℓ_j`, `u_j ≤ t ≤ u_j ⊕ ℓ_j`) are all discharged, and S3★ is applied only on the `s_C` branch it covers. `ρ(R, Σ) ⊆ dom(Σ.C)` is sound, including for depth-mismatched specs (the `[1,1] ≤ [1,1,1] < [1,2]` example is correct under T1).
- **Recovery equation.** The reference decomposition satisfies it (LP-Fin Corollary at `n = 1`, applicability via LP-Sub checked); the merge of a chain run is legal exactly when all chain members are resolved (one frontier or skipped member violates the `F`-trace — the frontier counterexample distinguishing the `F`-trace from a store-trace condition is genuine, not decorative). The extensional form was verified in both directions, including the step the right-to-left reading needs: trace members in `dom(Σ.C)` are T4-valid (StoreT4Validity), so `sig = #` (TA5-SigValid) identifies the shift-form trace as an `inc(·,0)` run before ASN-0053's S3 is invoked. The TS3 composition correctly avoids the `n₁ = 0` boundary by treating `k = 1, 2` separately.
- **Tightness and stability.** The stored record matches ASN-0098's `Tight` clause-for-clause (canonical spans, start in store, all interior `F`-candidates in store), so LP19a applies; `coverage(e_j) ∩ dom(Σ''.C) = ρ(R_j, Σ)` at every later state follows because K.α is the vocabulary's only content-extending transition.
- **ML6.** Necessity (empty resolution forces `e₃ = ∅`, violating L3) and sufficiency (`ρ(R₃,Σ) ≠ ∅ ⟹ coverage(e₃) ≠ ∅ ⟹ e₃ ≠ ∅`) both check.
- **Composite validity.** K.λ's value precondition is fully discharged (arity 3, endset finiteness from S8-fin, `e₃ ≠ ∅` from ML6); K.μ⁺_L's precondition is discharged at the intermediate state, and the `a ∉ ran(M(d))` argument correctly applies S3★/S3★-aux/CL-OWN at the *pre*-state where freshness holds, sidestepping the trap that `a ∈ dom(L)` at the intermediate state. J0/J1★/J1'★ vacuity matches the K.λ/K.μ⁺_L frames (`E' = E ∧ R' = R`).
- **ML9.** Fact (a)'s two halves check (store-trace exactness for content; subspace exclusion `s_C` vs `s_L` for links, disposing of the fresh `a` and all pre-existing link addresses uniformly). Fact (b)'s `d' = d` boundary is handled correctly — the added point `a` is inert on both sides because `a ∉ coverage(eᵢ)` was already established. The wp correctly conjoins enabledness and the postcondition's definedness (`d' ∈ dom(Σ.M)`, which equals `dom(Σ'.M)` since neither step extends `dom(M)`). The future-state extension rests on two state-uniform premises, both verified.
- **MLop branch decoupling.** The one-directional forcing (empty homed set ⟹ `V_{s_L}(d) = ∅` via CL-OWN) and the contracted-home counterexample (`K.μ⁻` with `n'_{s_L} = 0`, links unseated but persistent under P3/L12) are both correct, and the mixed case's three contract checks go through.
- **Worked example.** All arithmetic verified: the interval `[s_C,1] ≤ t < [s_C,3]`, the chain identity `a₂ = inc(a₁, 0) = shift(a₁, 1)`, the depth-2 retention set `{[s_C, 1]}`, and the post-edit checks (i)–(iv) against K.μ⁻'s frame. The example exercises the boundary the ASN's own convention introduces (first seating at `m = 2` against D-MIN★/D-SEQ★) — the one branch not fixed by the substrate.

On the anti-bloat directive: I scanned for the listed patterns. The two deferrals point at *distinct* Open Questions, not one downstream location; the motivational passages ("what if MAKELINK stored V-positions," "why the trace is on `F`") each carry a derivation or counterexample, not defensive justification; the resolve-correspondence paragraph's brief recall of what `wf` declines to impose is cross-reference, not duplication. Nothing rises to a finding.

## OUT_OF_SCOPE

### Topic 1: Higher-arity MAKELINK (N > 3)
**Why out of scope**: The substrate's K.λ and the Link type admit `N ≥ 3` (and Nelson's LM 4/79 calls for n-sets), but `makelink(d, R₁, R₂, R₃)` deliberately fixes arity 3. An n-ary creation operation is a distinct contract — slot semantics beyond from/to/type would need their own resolution and discoverability story — and belongs in a future ASN, not in this one.

### Topic 2: Direct I-address endset arguments (ghost and foreign endsets)
**Why out of scope**: The ASN proves MAKELINK-via-V-specs produces only content-backed endsets and explicitly marks the I-address argument shape (which L4/L9 generality permits at the store level) as a distinct operation. Specifying that operation — including ghost-type creation — is new territory.

### Topic 3: Link-subspace endset resolution and empty-endset semantics
**Why out of scope**: Both are already recorded as the ASN's Open Questions, correctly: resolving a spec that reaches the link subspace requires deciding what `ρ` means over `V_{s_L}`, and the *meaning* of an empty non-type endset is a semantic question beyond the definedness/legality/inertness this ASN settles.

VERDICT: CONVERGED
