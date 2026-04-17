# Cone Review — ASN-0034/TA-Pos (cycle 3)

*2026-04-17 14:13*

### TA-Pos's step from `tₖ ≥ 1` to `zₖ = 0 < tₖ` is not discharged by the axioms its *Depends* cites
**Foundation**: TA-Pos's Case `#z ≥ k` claims `zₖ = 0 < tₖ` via the chain "tₖ ≠ 0 ⟹ tₖ ≥ 1 ⟹ 0 < tₖ". The *Depends* enumerates NAT-zero, NAT-discrete, NAT-order, NAT-wellorder; it does not list NAT-addcompat.
**ASN**: TA-Pos, postcondition proof, Case `#z ≥ k`: "whose contrapositive under the premises `0 ≤ tₖ` and `tₖ ≠ 0` forces `tₖ ≥ 1`, whence `zₖ = 0 < tₖ`." The *Depends* clause glosses the whole derivation as "the 'nonzero ⇒ `≥ 1`' inference is discharged from the combination NAT-zero + NAT-discrete".
**Issue**: The Depends accounts for the step *to* `tₖ ≥ 1` but not the step *from* `tₖ ≥ 1` to `0 < tₖ`. From `1 ≤ tₖ` (i.e., `1 < tₖ ∨ 1 = tₖ`), concluding `0 < tₖ` requires `0 < 1` — either as a direct fact or composed via NAT-order transitivity (`0 < 1 < tₖ`) and substitution (`0 < 1 = tₖ`). But `0 < 1` is not implied by NAT-zero (which only gives `0 ≤ 1`), by NAT-discrete (which at `m=0, n=0` gives `0 = 0`, not `0 < 1`), or by NAT-order or NAT-wellorder alone. The natural discharge is NAT-addcompat's strict successor inequality `n < n + 1` instantiated at `n = 0`, but NAT-addcompat is not in TA-Pos's Depends. (A simpler two-line route exists — `0 ≤ tₖ` by NAT-zero plus `tₖ ≠ 0` gives `0 < tₖ` directly via NAT-order's trichotomy, using only the non-strict/strict unfolding of `≤` — but the proof does not take that route, and the Depends gives no account of how the `tₖ ≥ 1 ⟹ 0 < tₖ` step it does take resolves.)
**What needs resolving**: Either (a) add NAT-addcompat (with `0 < 0 + 1`) to TA-Pos's Depends and have the prose explicitly compose it with NAT-order transitivity/substitution to close the gap; or (b) rewrite the Case `#z ≥ k` argument to derive `0 < tₖ` directly from NAT-zero's `0 ≤ tₖ` and the construction's `tₖ ≠ 0` via NAT-order's trichotomy, dropping the `tₖ ≥ 1` detour — along with NAT-discrete — from the citation entirely.

## Result

Cone converged after 4 cycles.

*Elapsed: 1828s*
