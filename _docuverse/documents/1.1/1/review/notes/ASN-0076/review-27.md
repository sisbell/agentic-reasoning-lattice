# Review of ASN-0076

I read the ASN as a self-contained operation specification and checked each of E0–E10, the composite-validity discharge, and the worked example against the foundation contracts (ASN-0034/0036/0043/0047/0098).

## REVISE

(none)

I attempted to break the proofs at the usual failure points and each held:

- **E0 freshness at the correct state.** The proof does not lazily inherit "first-emission freshness" from the earlier entity-allocation event; it re-derives `ℓ_new ∉ dom(Σ.L) ∪ dom(Σ.C)` *at the firing state* `Σ` (sub-case (a) via the empty-set sub-case condition; sub-case (b) via L11a + the `s_C ≠ s_L` subspace argument). The case split (`{ℓ' : origin = d_new}` empty / non-empty) is exhaustive. Both `ℓ_new` and `ℓ_sup` are discharged separately, the latter from the intermediate state `Σ_1`.
- **E0 depth bound `#E ≥ 2`.** This is the one place SubAllocatorBundle does not give the result directly for subsequent emissions, and the ASN supplies the induction itself: TA5(c) (length) + TA5(b) (modification confined to `sig`) + TA5-SigValid (`sig = #t` on T4-valid inputs) ⟹ zeros and field boundaries preserved ⟹ `#E` preserved. No circularity (T4-validity comes from T10a.4/SubAllocatorBundle independently of `#E`).
- **E0 max-identification for the supersession step.** The initial-segment argument plus T10a.7 (strictly increasing enumeration) correctly pins `ℓ_sup = inc(ℓ_new, 0)` whether `d_new` had prior links or not, and the adjacency assumption is explicitly tied to SequentialTransitionAxiom + ValidComposite★.
- **E5 induction.** Reachability is correctly propagated (concatenation of the path to `Σ` with `k−1` ValidComposite★ steps), all four post-state conjuncts (prior-link persistence via LP13, new references via E4, pairwise distinctness of all `2k` addresses via L11a) are discharged, and the base case `k=0` is genuinely vacuous. A single fixed `d_new = home(ℓ_old)` is correctly justified.
- **E7 / discoverability reconciliation.** The `covers(Σ, ·)` (inverse, store-only) vs. ASN-0098 `discoverable_from` (arrangement-conditional) distinction is the right hazard to flag, and the ASN handles it: since EDITLINK performs no `K.μ⁺_L` (E10), `ℓ_sup` is orphaned per LP17 until referents are arranged, with LP18 governing resurrection. This is the non-trivial discoverability case, addressed rather than skipped.
- **Worked example** verifies E0–E10 against concrete tumblers; the arithmetic (`zeros`, field decomposition, `inc(·,0)` last-component bump, `δ(1,8)`) checks out.
- **Cross-ASN discipline (#7).** All citations route through foundation ASNs (0034/0036/0043/0047/0098); ASN-0093 machinery is reached only via ASN-0047's lemmas, which is permitted.

## OUT_OF_SCOPE

The deferrals are correctly identified and parked in Open Questions, not smuggled in as claims:

- **Supersession-type convention for `τ_sup`** — semantic identification of `ℓ_sup` *as* a supersession needs an external type-endset registry; E4/E7 correctly limit themselves to structural-witness claims.
- **Authorization/ownership model** — E6's "who may select `d_new`" discussion is explicitly informal; the abstract K.λ has no executor field.
- **Cycle invariants / termination of lineage walks** — the appendix is marked illustrative and disclaims termination; admitting cyclic supersession is left open.

These are new territory, not errors in this ASN.

VERDICT: CONVERGED
