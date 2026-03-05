# Review of ASN-0001

## REVISE

### Issue 1: Definition of sig(t) contradicts its own example

**ASN-0001, Increment for allocation**: "Define the *last significant position* of a tumbler `t` as `sig(t) = max({i : 1 ≤ i ≤ #t ∧ tᵢ ≠ 0} ∪ {#t})`" followed by "For `[1, 0, 3, 0]`, `sig = 3` (position of the 3)."

**Problem**: The definition gives `sig([1, 0, 3, 0]) = max({1, 3} ∪ {4}) = max({1, 3, 4}) = 4`, not 3. The union with `{#t}` is intended to handle the all-zero fallback, but it dominates the result for any tumbler with trailing zeros. The subsequent claim that `[1, 0, 3, 0]` and `[1, 0, 3]` share the same `sig` value is false under the stated definition: `sig([1, 0, 3, 0]) = 4` while `sig([1, 0, 3]) = 3`.

The error is confined to non-T4-compliant tumblers (valid I-space addresses have their last component nonzero, so `max({i : tᵢ ≠ 0}) = #t` and the union changes nothing). The downstream proof that `inc(t, 0)` acts on a field component for valid addresses is correct because it depends on `sig(t) = #t`, which holds independently of the union. But the definition as written is inconsistent with its illustration, and any reader checking the definition against the example will find a contradiction.

**Required**: Fix the definition to a conditional form: `sig(t) = max({i : 1 ≤ i ≤ #t ∧ tᵢ ≠ 0})` when the set is non-empty, `sig(t) = #t` when every component is zero. Alternatively, drop the `∪ {#t}` and handle the all-zero case explicitly. Update the example to be consistent.

---

### Issue 2: TA4 verification assumes aₖ > 0 without covering aₖ = 0

**ASN-0001, Verification of TA4**: "Since `aₖ > 0` (by T4's positive-component constraint for valid addresses, or by the precondition `w > 0` when `k = 1 = #a`), we have `rₖ = aₖ + wₖ > wₖ`, and the first divergence is at position `k`."

**Problem**: The second disjunct is a non-sequitur — `w > 0` establishes `wₖ > 0`, not `aₖ > 0`. Under the stated preconditions (`k = #a`, `#w = k`, all components of `a` before `k` zero), the value `aₖ = 0` is permitted: `a` may be a zero tumbler, and the zero-prefix condition is satisfied vacuously when `k = 1`. When `aₖ = 0`: `r = a ⊕ w = [0, ..., 0, wₖ]`, and `r = w` (since both have length `k`, both have zeros before `k`, and `rₖ = 0 + wₖ = wₖ`). The subtraction `r ⊖ w` then follows the equal-operand path — no divergence exists, result is the zero tumbler of length `k`, which equals `a`. TA4 holds, but through a path the proof does not trace.

**Required**: Split the verification at the divergence step into two sub-cases: (i) `aₖ > 0`, where the current argument applies, and (ii) `aₖ = 0`, where `r = w` and the subtraction's equal-operand rule produces the zero tumbler, recovering `a`.

---

### Issue 3: TA3 proof does not cover the prefix case of a < b

**ASN-0001, Verification of TA3**: "Let `j = divergence(a, b)` — the first position where `a` and `b` differ (`aⱼ < bⱼ` since `a < b`)."

**Problem**: When `a < b` by T1 case (ii) — `a` is a proper prefix of `b` — no divergence position exists. The three-case analysis (on the relationship between `dₐ` and `d_b`) assumes throughout that `j` is a well-defined position where `aⱼ < bⱼ`. The conclusion is correct: `a ⊖ w` has length `max(#a, #w)`, `b ⊖ w` has length `max(#b, #w) ≥ max(#a, #w)`, and the results agree through their shared prefix and differ in length, so `a ⊖ w < b ⊖ w` by the T1 prefix rule. But this argument is nowhere in the proof.

The gap is benign for the editing use case (V-space ordinals are single-component tumblers that cannot stand in prefix relationship), but TA3 is stated for all tumblers in T. The claim requires a proof for all cases of its precondition.

**Required**: Add a fourth case (or a preliminary lemma) handling `a < b` by the prefix rule: when `#a < #b` and `aᵢ = bᵢ` for all `i ≤ #a`, show that `#(a ⊖ w) ≤ #(b ⊖ w)` and the results agree through the shorter length, so the T1 prefix rule gives `a ⊖ w < b ⊖ w`. Alternatively, define `divergence(a, b)` to handle the prefix case (e.g., `j = #a + 1` with the convention that `aⱼ = 0 < bⱼ`) and show the existing case analysis still applies.

---

## OUT_OF_SCOPE

### Topic 1: Crash recovery for allocation monotonicity
**Why defer**: Already identified as an open question. T9 is a pure-state property; the recovery protocol that restores it after failure is a separate system-level concern, not an error in the algebra.

### Topic 2: Span intersection computability from POOM structure
**Why defer**: Already identified as an open question. This requires the POOM's structure (a future ASN's territory), not just the tumbler algebra.

### Topic 3: Multi-component span lengths across hierarchical boundaries
**Why defer**: T12 admits multi-component lengths, and the ASN notes spans can cover "all content in multiple documents under a user." The well-definedness of such spans depends on TA0's precondition (`k ≤ #s`), which is always satisfied when the span's start address is at least as deep as the displacement's action point. A future ASN on span operations should verify this for each hierarchical span construction.

VERDICT: REVISE
