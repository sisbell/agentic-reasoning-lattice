# Cone Review — ASN-0034/TA5a (cycle 4)

*2026-04-17 18:57*

### TA5 uses NAT-discrete to sharpen `k > 0` to `k ≥ 1` but omits NAT-zero
**Foundation**: NAT-discrete (NatDiscreteness) — `(A m, n ∈ ℕ :: m ≤ n < m + 1 ⟹ n = m)`. Instantiating at `m = 0` to conclude `k ≥ 1` from `k > 0 ∧ k ∈ ℕ` requires the premise `0 ≤ k`, which is supplied by NAT-zero (`0 ≤ n` on ℕ). T0 alone fixes the carrier but does not license the lower-bound step.
**ASN**: TA5's proof, Verification of (a), Case `k > 0`:
> "NAT-discrete (instantiated at `m = 0`: no natural lies strictly between `0` and `0 + 1`) sharpens the hypothesis `k > 0` in ℕ to `k ≥ 1`, since any `k ∈ ℕ` with `0 < k < 1` is ruled out."

TA5's Depends list cites T0, NAT-closure, NAT-addcompat, NAT-discrete, T1, TA5-SIG — no NAT-zero.
**Issue**: The "`0 < k < 1` ruled out" step ranges `k` over ℕ and instantiates NAT-discrete at `m = 0`; the antecedent `m ≤ n < m + 1 = 0 ≤ k < 1` requires `0 ≤ k`, which NAT-zero supplies. Elsewhere in this ASN — T4a's opening, T4c's exhaustion step, TA5-SigValid, and the current revision's per-step citation convention for the structurally identical "non-zero ⇒ strictly positive on ℕ" inference — the trio T0 + NAT-zero + NAT-discrete is cited jointly at exactly this kind of step. TA5 performs the same lower-bound-plus-discreteness move but cites only NAT-discrete, so the `0 ≤ k` premise it consumes is unsourced under the convention the ASN has set for itself.
**What needs resolving**: TA5's Depends list must either surface NAT-zero as a distinct citation at the Case `k > 0` step (matching the per-step convention used in T4a, T4c, TA5-SigValid, and TA5a for the analogous inference), or restate the step so that the `0 ≤ k` premise is not required (e.g., by consuming `k ≥ 1` directly from a prior clause rather than sharpening from `k > 0`).

### TA5a case `k = 1` cites a TA5-SigValid fact that is not in TA5-SigValid's exported Guarantee
**Foundation**: TA5-SigValid (SigOnValidAddresses) — Guarantee: "`sig(t) = #t`". The strict-positivity fact `t_{#t} > 0` appears as an intermediate step inside TA5-SigValid's proof but is not part of its exported contract; the exported contract carries only the equality of indices.
**ASN**: TA5a's proof, Case `k = 1`:
> "The last component of `t` is positive — by TA5-SigValid, `t_{#t} > 0` — so the new component is not adjacent to a zero."

TA5a's Depends entry reinforces this:
> "TA5-SigValid (SigOnValidAddresses) — ... Also invoked at case `k = 1` to license the non-zero last component ('by TA5-SigValid, `t_{#t} > 0`') against which the appended `1` is checked for non-adjacency."

**Issue**: Two inconsistencies between property contracts.
(1) TA5-SigValid's Guarantee exports only `sig(t) = #t`; `t_{#t} > 0` is a proof-internal derivation routed through T4 + NAT-zero + NAT-discrete. Citing "by TA5-SigValid, `t_{#t} > 0`" treats an internal step as a foundation-level guarantee, breaking the contract boundary between the two properties.
(2) Case `k = 0` sources the same underlying fact — `t_{sig(t)} ≠ 0` — by the explicit chain "TA5-SigValid → T4: by TA5-SigValid, `sig(t) = #t`; by T4's boundary clause, `t_{#t} ≠ 0`". Case `k = 1` short-circuits that chain and additionally strengthens `≠ 0` to `> 0` with no NAT-* citation, even though the non-adjacency check in that case needs only `t_{#t} ≠ 0`, which T4's boundary clause supplies directly (as it does in case `k = 2`). The two cases of the same proof therefore route structurally identical sourcing through inconsistent chains.
**What needs resolving**: TA5a's case `k = 1` must either (a) source the non-adjacency premise through the same chain case `k = 0` uses (TA5-SigValid for `sig(t) = #t` if needed, and T4's boundary clause `t_{#t} ≠ 0` for the non-zero fact — as already done in case `k = 2`), eliminating the mis-attribution to TA5-SigValid of a fact it does not export; or (b) coordinate with TA5-SigValid to promote `t_{#t} > 0` into its exported Guarantee, so the citation resolves to a contracted fact. Either path also requires TA5a's Depends entry for case `k = 1` to be updated to match.
