# Review of ASN-0125

I reviewed this as an editing-under-immutability specification: an impossibility result (EL0–EL2), a forced-architecture derivation (RQ1–RQ7, EL3), two operations (assert_sup, editlink), and their contracts/consequences (EL4–EL16). I checked the proofs, the boundary cases, the foundation usages, and the worked example arithmetic. I also applied the `review-mode.anti-bloat` lens to the forward-reference structure. My conclusion is that the formal content is sound and complete, scope is respected, and the prose — recently tightened — does not contain obstructive accretion. Details below.

## REVISE

None.

What I verified, including the load-bearing and subtle steps:

- **EL0** is correctly the weakest-precondition reading of L12/LP13: `J` holds at every state of every schedule from `Σ₀`, `[J ⟹ ¬R_mut]` since `Σ.L` is a partial function and `w ≠ ℓ₀`, so `wp(S, R_mut) = false`. The dual ("readable at its address forever") is exact.
- **EL1**'s collapse is right — each transition and `a_emit` are functions of pre-state, so "edit" and "independent creation" with the same parameters are the *same transition*; no state predicate separates them.
- **EL2(c)** correctly forecloses address-nesting: `FirstEmission`/`ChainDiscipline` give `#E = 2` for every allocated link address, a version-of address needs `#E ≥ 3`, and R0a (antichain) blocks prefixing — so the address relation carries only same-home and per-home-order, neither semantic.
- **EL4** is per-claim (PrefixSpanCoverage + R0a), correctly noted as needing no whole-state hypothesis; `new`/`old`/`addr` total on `Ŝ^Σ`.
- **EL6(iv)** — the hardest frame argument — is correct in both halves: unconditionally `nullified(Σ') ∩ dom(Σ.L) = nullified(Σ)` because the new tuple is class `K_sup ≠ R` (no `[R]`-growth); and under discipline the fresh `b` escapes every pre-existing unit-depth `[R]` to-coverage because `t ≼ b` with `t ∈ dom(Σ.L)`, `b ∉ dom(Σ.L)` violates R0a — exactly wp Case 2's third conjunct.
- **EL7(vi)** correctly transfers `DC(ℓ')`'s witnesses across the step-1 emission via `dom(Σ.L) ⊆ dom(Σ₁.L)`, and rightly observes the fresh `a'` is neither witness (so the new claim never self-references). The retraction-valued-`ℓ'` case is handled coherently.
- **EL11(a)**'s content-address exclusion is rigorous: a `t ≽ old(e)` inherits `old(e)`'s three zeros, so if `zeros(t)=3` its element field starts at the same position with `E(t)₁ = s_L`, contradicting `E(t)₁ = s_C` (SC-NEQ); link extensions collapse by R0a; intersection reduces to `{old(e)} ∩ ran(M(d))`.
- **EL13**'s commutation holds because `a_emit(Σ,d)` consults only the `d`-homed subset, unchanged by a `d'≠d` emission; the per-home vs. per-asserter "latest" caveat is precise.
- **EL14(c)** standoff (`current = ∅`) is correctly reachable and `reach_o` stays computable under cycles (finite closure, no sink).
- **Worked example** address arithmetic is correct end-to-end: `ℓ₁ = H.0.s_L.2`, `c₁ = H.0.s_L.3`, `ℓ₂ = P.0.s_L.1`, `c₂ = P.0.s_L.2`, `r₁ = …4`, `c₃ = …5`, `r₂ = …6`; `shift([s_L,1],1) = [s_L,2]` (EL10) checks; the demotion/revert/standoff/repair currency transitions are all correct.
- Foundation usages (L12, LP13, R0a, a_emit, wp Case 2, R3, R6a, PrefixSpanCoverage, LP12, S3★, CL-OWN, K.μ⁻/K.μ⁺_L retention shapes, T7/SC-NEQ) are consistent with the cited contracts. The **Layer-transfer** argument is sound: every invoked ASN-0086 fact depends only on `(dom(L), L, dom(M))`, which evolve identically under the full ASN-0047 vocabulary (links only by K.λ — Vocabulary fact V; `dom(M)` monotone — M1).

On anti-bloat specifically: I examined the candidates. EL6(iv) ("independence of axes") and EL7(ii) ("archivally present / contextually dark," citing EL11a/b) do use the EL9/EL11 vocabulary ahead of those claims, but each states genuine contract content (the operation's frame on the original; the successor's discoverability status post-edit) and grounds it by forward citation — the normal contract-then-formalize structure, not vacuous accretion. The EL3 remarks are the *negative* elimination dual to the positive construction (value-space and address-space failures by RQ), not a restatement. The implementation-note blocks and the worked example are required concrete evidence. I did not find prose I had to skip to follow a claim.

## OUT_OF_SCOPE

Nothing to flag. Scope is respected: the `in`/`out` and `Observe_{K_sup}` queries (EL11b) are supersession-record reads, not general link discovery (FINDLINKSFROMTOTHREE); the K.μ⁻/K.μ⁺_L uses (EL9, EL10) characterize the original's listing aftermath using existing substrate operations rather than defining new document operations.

VERDICT: CONVERGED
