# Review of ASN-0125

I reviewed this as a derived-composite operation note: two allocations (successor + claim) standing in for an impossible in-place mutation. I checked the impossibility argument, the carrier-necessity derivation, both operation contracts, the discipline induction, the discoverability characterizations, and the worked example. I traced the example against concrete addresses, and I checked boundary cases (empty store, first/last listing position, value-identical edit, revert, mutual-supersession standoff, fork).

## What I verified

**EL0 / EL1 (the negative core).** `wp(S, R_mut) = false` at Σ₀ is L12 closed under `→*` (= LP13) instantiated at `a`, with `J ⟹ ¬R_mut`. Sound. EL1's collapse of "edit" and "create" to one transition instance (hence one post-state) correctly grounds the need for explicit assertion — intent is not a state component.

**EL2 (carrier closures).** (c) is the load-bearing one: every allocated link address has `#E = 2` (FirstEmission + `inc(·,0)` length-preservation, TA5(c)), a version-of-link address needs `#E ≥ 3`, and R0a makes `dom(Σ.L)` an antichain — so address structure encodes only same-home and emission order. Checked. (a),(b),(d) follow from L12, L14, and the K.ρ/SD exclusion of link targets.

**EL6 / EL7 (the contracts).** The frame conjuncts are complete (both ops are pure `K.λ`; C, M, E, R framed; L extended at fresh keys; prior entries fixed by L12). The active-at-birth conclusions correctly invoke ASN-0086 wp Case 2 under the disciplined simplification (`K_sup ≁ R` discharges the self-nullification guard; unit-depth discipline + R0a-at-Σ′ discharges the third conjunct because the fresh emitter is prefix-incomparable to every existing retraction target). EL7's two-step `nullified(Σ₂) = nullified(Σ)` argument and the EL7(vi) discipline induction (both the claim case via `DC`'s schema clause and the non-claim case via vacuity over `S^{Σ₁}` + `DC`'s leading conjunct) are airtight; I confirmed the (iv)→(vi) dependency is non-circular ((vi) rests on `DC` and EL6(v), not (iv)).

**EL4 / Df-SUCC.** The per-claim totality of `old`/`new`/`addr` on `Ŝ^Σ` correctly rests on schema-conformance of the single claim plus R0a (a state property holding at every reachable state, not edit-discipline), which is exactly what lets Df-SUCC be total at non-disciplined reachable states. The `Ŝ^Σ` vs `S^Σ` distinction is genuinely needed under full-vocabulary reachability and is handled cleanly.

**EL9 / EL10 / EL11.** EL9(2)'s de-listing construction is correct including the `j=1` first-position branch and the `j=n` empty-suffix boundary; survivors land one position below and D-SEQ★ reshapes to `{[s_L,k] : 1 ≤ k ≤ n−1}`. EL10's position-reuse construction checks out (K.μ⁻ then K.μ⁺_L reassigns the vacated tail position). EL11(a)'s biconditional proof correctly excludes content addresses (zeros/subspace argument via C1, L0, SC-NEQ) and link addresses (R0a), reducing the projection to `{old(e)} ∩ ran(M(d))`. EL11(b)'s coincidence with `Observe` is correctly qualified to `y,x ∈ dom(Σ.L)`.

**EL14(e).** The activity-agnostic-membership result — `z ∈ current(y,Σ)` not implying `active(z,Σ)` because `succ_o` filters only on *claim* addresses — is subtle and correct, and the in-layer reachability witness (editlink then `Nullify` the successor) holds.

**Worked example.** Traced fully: the H/P chain addresses (`ℓ₁=H.0.s_L.2`, `c₁=H.0.s_L.3`, `r₁=H.0.s_L.4`, `c₃=H.0.s_L.5`, `r₂=H.0.s_L.6`; `ℓ₂=P.0.s_L.1`, `c₂=P.0.s_L.2`), the fork, the demotion, the `current(ℓ₀)=∅` standoff and its repair, and the registry-churn position reuse all compute as stated.

**Composite validity.** Both ops are `K.λ`-only sequences; J0/J1★/J1'★ are vacuous, and there is no link analogue forcing fresh links into arrangements (consistent with LP17 / "born unlisted"). Output states are reachable.

## REVISE

None. I could not find a correctness error, an uncovered boundary case, a "by similar reasoning" hand-wave (the one "symmetrically" in EL11 covers a structurally identical from/to case), or an unproven derived claim. Cross-ASN references are all to foundations (0034, 0036, 0042, 0043, 0047, 0086, 0093, 0098).

Anti-bloat check (per the attached classifier): I looked specifically for forward-reference accretion, defensive justification, use-site inventories, and reviser drift. "Vocabulary fact V" is an enumeration but it *is* the proof of a load-bearing lemma, not a use-site inventory. The EL7(iv)→EL7(vi) forward step and the Df-DISC commentary are the deliberate product of the most recent revision (`tighten Df-DISC commentary, forward key steps to EL7(vi)`) and are correct as written; re-raising them would re-litigate a just-made choice. The remaining framing clauses (EL-DM's "non-vacuous domain" / "what makes a disciplined state reachable") are brief orienting sentences, not impediments. The three EL7 remarks and the implementation notes are statements of what the operation does / concrete grounding, which the guidance explicitly excludes from meta-prose. Nothing rises to a finding.

## OUT_OF_SCOPE

None. The discoverability material (EL11/EL14/EL15) is intrinsic to the problem statement's "must a reader recognize the edit / identify the current successor," not general link discovery; it uses foundation primitives (`project`, `Observe`) rather than defining FINDLINKS/READLINK/FOLLOWLINK. The Open Questions correctly defer authority-of-retraction, meta-claim stratification, span-level endset correspondence, and registry-coupling to future ASNs rather than claiming them here.

VERDICT: CONVERGED
