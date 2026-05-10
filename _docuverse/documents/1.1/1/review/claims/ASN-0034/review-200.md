# Cone Review — ASN-0034/TA0 (cycle 2)

*2026-04-17 21:14*

### Unused intermediate fact `wₖ > 0` in TumblerAdd's dominance proof

**Foundation**: TumblerAdd's dominance proof (`a ⊕ w ≥ w`), within the branch where `aᵢ = 0` for all `i < k`.

**ASN**: TumblerAdd, second branch of the dominance case split: "If instead `aᵢ = 0` for all `i < k`, then at position `k` we have `rₖ = aₖ + wₖ`, and ActionPoint's `wₖ ≥ 1` yields `wₖ > 0` via the chain `wₖ ≥ 1 > 0`: NAT-order's defining clause at `m = 1, n = wₖ` unfolds `wₖ ≥ 1` into `1 < wₖ ∨ 1 = wₖ`; NAT-addcompat's strict successor inequality at `n = 0`, together with NAT-closure's additive identity `0 + 1 = 1`, supplies `0 < 1`; NAT-order composes these … to yield `0 < wₖ`, i.e., `wₖ > 0`."

**Issue**: Tracing the inner case split that follows this derivation, neither sub-case consumes `wₖ > 0`. In sub-case `aₖ > 0`, the strict promotion runs through `0 ≤ aₖ` (NAT-zero) → `aₖ + wₖ ≥ 0 + wₖ` (NAT-addcompat right OC) → `aₖ + wₖ ≥ wₖ` (NAT-closure additive identity) → `aₖ + wₖ > wₖ` (NAT-order with NAT-cancel ruling out equality); `wₖ > 0` is not invoked. In sub-case `aₖ = 0`, `rₖ = aₖ + wₖ = 0 + wₖ = wₖ` directly via NAT-closure's additive identity; again `wₖ > 0` is unused. The follow-on text "The inner case split … is the same NAT-zero + NAT-order unfolding applied at `m = 0, n = aₖ`" refers only to the *form* of the unfolding (≥-into-disjunction), not to the specific `wₖ > 0` conclusion. Result: a four-step chain consuming NAT-order (twice), NAT-addcompat, and NAT-closure produces a fact the proof never uses, while inflating the per-step citation discipline that the Depends paragraph mirrors. A reviser tightening any of those NAT-* axioms would treat the chain as load-bearing because the proof prose says it is.

**What needs resolving**: Either identify a genuine downstream consumer of `wₖ > 0` inside the dominance argument and make that consumption explicit (e.g., a step `rₖ ≥ wₖ` derived from `wₖ > 0` rather than from `0 ≤ aₖ`), or excise the `wₖ ≥ 1 ⟹ wₖ > 0` chain from the proof so that the inner case split begins directly with the NAT-zero + NAT-order dichotomy on `aₖ`. The Depends paragraph's enumeration of NAT-* citations should then be re-checked: the `wₖ ≥ 1 ⟹ wₖ > 0` chain is the only site at which NAT-addcompat's strict successor inequality at `n = 0` and NAT-closure's additive identity `0 + 1 = 1` are jointly invoked in the dominance proof, so removing the chain would also remove those particular instantiations from the load-bearing set.

## Result

Cone converged after 3 cycles.

*Elapsed: 1817s*
