# Proof Verification: PositiveTumbler

Looking at the PositiveTumbler property section and its formal contract.

**Formal Contract:**
- *Definition:* `t > 0` iff `(E i : 1 ≤ i ≤ #t : tᵢ ≠ 0)` — stated.
- *Postconditions:* `t > 0 ∧ (A i : 1 ≤ i ≤ #z : zᵢ = 0) ⟹ z < t` under T1 — claimed but not formally proved.

The only argument for the postcondition is this inline sketch:

> "if `t` has a nonzero component at position `k`, then at position `k` either the zero tumbler has a smaller component (0 < tₖ) or has run out of components, either way placing it below `t`."

This sketch has a precision gap. T1 requires a witness `k` such that **(A i : 1 ≤ i < k : zᵢ = tᵢ)** — agreement at all positions before `k` — before either case (i) or (ii) applies. The sketch says "a nonzero component at position `k`" without specifying that `k` must be the **first** (least) nonzero component of `t`. If `k` is not the first nonzero component, the agreement condition can fail:

**Counterexample to the sketch's reasoning (not to the claim):** Let `t = [3, 5]`, `z = [0, 0]`. Picking `k = 2` (a nonzero component), T1 requires `z₁ = t₁` for agreement at position 1, but `0 ≠ 3` — so position 2 is not a valid T1 witness. The correct witness is `k = 1` (the *first* nonzero component), where `z₁ = 0 < 3 = t₁` gives T1 case (i).

A correct proof needs: let `k = min({i : 1 ≤ i ≤ #t ∧ tᵢ ≠ 0})`. By minimality, `tᵢ = 0` for all `i < k`, matching `zᵢ = 0`, so the T1 agreement condition holds. Then two sub-cases:
- If `k ≤ #z`: `zₖ = 0 < tₖ` (since `tₖ ∈ ℕ`, `tₖ ≠ 0` implies `tₖ > 0`), and `k ≤ min(#z, #t)`, giving `z < t` via T1 case (i).
- If `k > #z`: all shared positions `1..#z` agree (since `#z < k` means every `tᵢ = 0 = zᵢ` for `i ≤ #z`), and `#z + 1 ≤ #t` (since `k ≤ #t` and `k > #z`), giving `z < t` via T1 case (ii).

No such case analysis appears in the property section. The other properties with postconditions (T1, TA0, TA4) all have explicit `*Proof.*` blocks; PositiveTumbler does not.

```
RESULT: FOUND

**Problem**: The postcondition `t > 0 ∧ (∀i: zᵢ = 0) ⟹ z < t` has no formal proof.
The inline sketch says "if t has a nonzero component at position k" without
requiring k be the *first* nonzero component — which is necessary for the T1
prefix-agreement condition `(A i : 1 ≤ i < k : zᵢ = tᵢ)` to hold. The sketch
also does not distinguish the two T1 sub-cases (k ≤ #z vs k > #z).

**Required**: Add a *Proof.* section that (1) defines k as the least nonzero
position of t, (2) derives the agreement condition from minimality of k, and
(3) handles both T1 witness cases: case (i) when k ≤ #z giving zₖ = 0 < tₖ,
and case (ii) when k > #z giving z as a proper prefix of t.
```
