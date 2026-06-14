# Review of ASN-0125

I read this as a single self-contained argument: link mutation is impossible (EL0), so EDITLINK must be allocation-plus-assertion, and the assertion must be a fresh typed link-to-link claim (EL2/EL3), formalized as the supersession class with `assert_sup`/`editlink` and the `succ_h`/`succ_o`/`current` query family. I checked the proofs case by case, ran the boundary scenarios, and verified the worked example arithmetically.

## What I verified

**EL0–EL1 (the impossibility core).** The wp argument is sound: `J ≡ a ∈ dom(L) ∧ L(a) = ℓ₀` is exactly LP13 closed under `→*`, `[J ⟹ ¬R_mut]` since a partial function is single-valued and `w ≠ ℓ₀`, so `wp(S, R_mut)` at `Σ₀` is `false` for every program. EL1's "same transition instance, same post-state" collapse is correct — intent is not a component of `Σ`.

**EL2(c) (address-relation closure).** Checked the structural claim: `inc(a, 1)` does preserve T4 (`zeros = 3 ≤ 3`, TA5a) and yields `#E = 3`, while every allocated link address has `#E = 2` (FirstEmission + `inc(·,0)` length preservation) and `dom(L)` is an R0a antichain — both independently block version-of-link nesting. The implementation notes (Q11–Q19) are evidence, not spec, and correctly placed.

**EL4 / EL6 / EL7 (the contracts).** EL4's `coverage(F) ∩ dom(L) = {x}` via PrefixSpanCoverage + R0a is genuinely per-claim (no whole-state hypothesis), and the totality of `old/new/addr` on `Ŝ^Σ` is right. EL6(iv)'s split — `nullified(Σ') ∩ dom(Σ.L) = nullified(Σ)` unconditionally (no `[R]` growth) versus full `nullified(Σ') = nullified(Σ)` only under discipline (fresh `b` escapes every unit-depth retraction coverage by R0a) — is exactly the distinction wp Case 2 needs, and EL7(iv) chains it correctly through the disciplined intermediate `Σ₁`. The "born unlisted" derivation (`a'` fresh against `dom(C) ∪ dom(L) ⊇ ran(M(d))`) holds.

**EL7(vi) (the bare-`K.λ` distinction).** The case split is complete: if `ℓ'` is `[K_sup]`/arity-3 it is a claim at `Σ₁` and `DC` forces schema-conformance (clause ii); otherwise `a' ∉ S^{Σ₁}` so clause (ii) is vacuous on it and `DC`'s leading conjunct keeps it out of `[R]` (clause i). The internal-`K.λ`-vs-bare-`K.λ` separation is load-bearing, not redundant.

**EL-DM (induction).** Base at `Σ₀` (`L₀ = ∅`) is the right empty-store boundary; the step correctly factors `assert_sup`→EL6(v), `editlink`→EL7(vi) without circularity (EL6/EL7 are per-transition conditionals; EL-DM discharges the condition).

**Boundary scenarios.** Empty store (EL-DM base), first/last/only listed position (EL9(2) `j = n` and `j = 1` branches), fork (EL12), mutual-supersession standoff `current = ∅` (EL14c), and activity-agnostic membership `z ∈ current(y) ∧ ¬active(z)` (EL14e) all check out. I reran EL9(2)'s de-list/re-seat (`K.μ⁻` retains the prefix, survivors slide down one via `shift(max, 1)`), EL10's position re-binding (`shift([s_L,1],1) = [s_L,2]`), EL13's cross-home commutation (`a_emit` reads only the home's own subset), and the full worked example (`c₁=H.0.s_L.3`, `r₁=H.0.s_L.4`, `c₃=H.0.s_L.5`, `r₂=H.0.s_L.6`; `current(ℓ₀)` walks `{ℓ₁} → {ℓ₁,ℓ₂} → {ℓ₁} → ∅ → {ℓ₀}`) — all consistent.

**EL11(a) (discoverability biconditional).** The "no content address extends `old(e)`" step is correct: a `t ≽ y` with `zeros(t) = 3` inherits `y`'s three zeros, fixing `E(t)₁ = E(y)₁ = s_L`, contradicting `E(t)₁ = s_C`; the link side collapses to `{y}` by R0a; so the intersection is `{y} ∩ ran(M(d))`, nonempty iff listed, and only at `home(y)` by Df-LISTED. The "symmetrically for the from-side" is justified because `new(e)` is structurally identical to `old(e)`, not a hidden distinct case.

**Self-containment.** Every cross-ASN reference is to a foundation (0034, 0036, 0040, 0042, 0043, 0045, 0047, 0053, 0058, 0086, 0093, 0098); no reinvented notation. The Open Questions correctly defer genuinely new territory (retraction-of-claim authority, span-level endset correspondence, meta-claim stratification). No claim addresses a Scope-excluded topic.

**Anti-bloat pass.** I looked specifically for relocated findings, axiom-justification prose, repeated paragraphs, use-site inventories in definitions, and deferral chains. Vocabulary fact V is a genuine load-bearing inventory (consumed by EL-DM and EL7(vi)), not padding. The dense passages (EL7(vi), EL14(d)) are argument, not meta-prose — I followed each claim through its proof without having to skip past filler. The recent revision targeting §vi and Df-LAY appears to have removed the prior accretion the classifier flagged.

## REVISE

(none)

VERDICT: CONVERGED
