# Review of ASN-0125

I verified the load-bearing proofs against the foundation contracts, with particular attention to operation frames, boundary cases in the arrangement constructions, the discipline induction, and the recently-added `|ℓ'| = 3` gate.

**Checked and sound:**

- **EL0** — `wp(S, R_mut) = false` is L12/LP13 read as an impossibility result; `J ⟹ ¬R_mut` (partial function, `w ≠ ℓ₀`), `J` persists across `→*`, so no closed-vocabulary program establishes `R_mut`. Genuinely non-trivial wp, correctly argued.
- **EL6/EL7 frames** — the unconditional/conditional split on `nullified` is precise. Unconditional `nullified(Σ') ∩ dom(Σ.L) = nullified(Σ)` follows from no `[R]`-slice growth; the full frame under discipline discharges wp Case 2's third conjunct via unit-depth retraction + R0a antichain (fresh `b` prefix-incomparable to every existing retraction target). The two-emission chain in EL7(iv) correctly routes through the EL7(vi)-disciplined intermediate `Σ₁`. No circularity (EL7(vi) is independent of EL7(iv); EL-DM uses EL6(v)/EL7(vi), not EL6(iii)).
- **EL9(2) de-listing construction** — boundary cases `j = 1` (first-position branch re-pins at `[s_L,1]`), `j = n` (last/only), and interior all verified against K.μ⁻ per-subspace retention (prefix-only) and K.μ⁺_L re-seating; D-SEQ★ shape `{[s_L,k] : 1 ≤ k ≤ n−1}` holds.
- **EL10/EL13/EL14** — position re-binding (`shift(max,1)` reusing a vacated tail), cross-home emission commutation (`a_emit` depends only on the home-local subset; distinct fresh keys), and currency cardinalities 1/≥2/0 (the 2-cycle standoff `reach_o` with no sink) all check. EL14(e)'s activity-agnostic-membership demonstration (`Nullify` an endpoint leaves the claim active, so `a' ∈ current(a)` yet `¬active(a')`) correctly isolates the two axes.
- **EL11(a)** — the `project ≠ ∅ ⟺ listed(old(e), d, Σ)` biconditional: the "no content address extends `y`" step (three-zero coincidence forcing `E(t)₁ = s_L` against `s_C`) and R0a collapsing link-extension to equality are correct; "symmetrically for the from-side" is genuinely symmetric (both endpoints are link addresses).
- **DC gate** — gating the schema clause on `|ℓ'| = 3` exactly matches `S^Σ = L_{K_sup}^Σ`'s arity-3 restriction, so an arity-`>3` `[K_sup]`-typed successor is correctly left unconstrained (no claim) while clause (ii) is preserved vacuously. The revision is correct.
- **Worked example** — all six episodes traced (addresses `H.0.s_L.{2..6}`, `P.0.s_L.{1,2}`); the standoff/repair sequence and the registry-churn epoch-reuse reproduce EL10/EL13/EL14 faithfully.

The note stays in spec territory (state, operations, invariants stated abstractly), references only foundation ASNs, reinvents no foundation notation, and the implementation notes are correctly marked as evidence. The anti-bloat survey found the forward-reference scaffolding (Vocabulary fact V, Layer transfer, the bare-vs-internal `K.λ` distinction, the Df-SUCC totality parenthetical) to be load-bearing exhaustive checks and totality justifications, not skippable meta-prose.

## REVISE

None.

## OUT_OF_SCOPE

### Topic 1: Span-level correspondence between old and new endsets
**Why out of scope**: The composite treats the successor's value `ℓ'` as opaque — it never relates the old endsets' spans to the new ones. Whether a narrowed/reshaped endset must carry span-level correspondence (and in what space that lives) is genuinely new territory, correctly deferred to the ASN's own Open Question 7.

### Topic 2: Principal-level authority for asserting/retracting claims
**Why out of scope**: EL8(b) correctly scopes attribution to the home document and defers named-principal resolution to the ASN-0042 ownership overlay; `Σ = (C,L,E,M,R)` carries no principal set. The authority invariant governing retraction-by-non-asserter (Open Question 1) belongs to that overlay, not here.

VERDICT: CONVERGED
