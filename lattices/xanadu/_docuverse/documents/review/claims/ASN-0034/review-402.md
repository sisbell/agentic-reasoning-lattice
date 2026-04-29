# Regional Review — ASN-0034/T4a (cycle 4)

*2026-04-23 00:49*

### T4a setup cites `zeros(t) ∈ {0, 1, 2, 3}` under weaker preconditions than T4's Consequence
**Class**: OBSERVE
**Foundation**: T4 (HierarchicalParsing), T4a (SyntacticEquivalence)
**ASN**: T4a's preconditions are "`t ∈ T` with `zeros(t) ≤ 3`" without the full field-segment constraint. The proof opens with "Set `k = zeros(t) ∈ {0, 1, 2, 3}`". T4's exported Consequence is stated as "`zeros(t) ∈ {0, 1, 2, 3}` for every **T4-valid** tumbler `t`" — i.e., under the full Axiom, including field-segment constraint.
**Issue**: T4a's annotation `k ∈ {0, 1, 2, 3}` can't be sourced from T4's Consequence as written, because the Consequence's stated scope is T4-validity, which T4a does not assume. In fact T4's Exhaustion proof only uses `zeros(t) ≤ 3` (plus NAT-card/NAT-zero/NAT-order/NAT-discrete), so the Consequence is actually provable under T4a's weaker precondition, but that's not what the Consequence slot states. The mismatch is latent: T4a's proof does not actually need `k ≤ 3` — it case-splits only on `k = 0` vs `k ≥ 1` — so the annotation is ornamental, but it is nonetheless a forward citation that doesn't type-check. Either T4's Consequence could be broadened to `zeros(t) ≤ 3` (the scope its proof actually establishes), or T4a could drop the annotation in favor of the minimal `k ∈ ℕ` it actually uses.

### T4a re-derives `#t ≥ 1` as "local unpacking" when T0's Axiom states it directly
**Class**: OBSERVE
**Foundation**: T0 (CarrierSetDefinition), T4a
**ASN**: T0's Axiom contains "`(A a ∈ T :: 1 ≤ #a)`" explicitly, exported as axiomatic content. T4a's proof says: "T0 declares every `t ∈ T` to be a nonempty finite sequence over ℕ; a nonempty sequence has at least one component, so by the definition of length `#t ≥ 1` — this is a local unpacking performed here, not a postcondition cited from T0".
**Issue**: The disclaimer is inverted from the foundation it cites. T0's Axiom explicitly posits `1 ≤ #a` for every `a ∈ T`; instantiating at `a := t` is direct axiom use, not a "local unpacking" of "nonempty finite sequence" semantics. The narrative invents a derivation path that doesn't need to exist, and the closing clause "not a postcondition cited from T0" misdescribes what T0 exports. This is reviser-drift prose: a justification explaining why a step is safe instead of stating the step.

### Base case of Exhaustion skips NAT-zero's Consequence
**Class**: OBSERVE
**Foundation**: NAT-zero (NatZeroMinimum), T4 (HierarchicalParsing)
**ASN**: NAT-zero's formal contract exports a Consequence `(A n ∈ ℕ :: ¬(n < 0))`. T4's Exhaustion, at the base step `m = 0`, derives `¬(zeros(t) < 0)` via the "exactly-one route": "the case `zeros(t) < 0` is excluded by `0 ≤ zeros(t)` via the exactly-one route just described".
**Issue**: The elaborate route (unfold `0 ≤ zeros(t)` to a disjunction, identify a trichotomy alternative, apply exactly-one) duplicates what NAT-zero's Consequence `¬(n < 0)` already gives in one step at `n := zeros(t)`. NAT-zero is declared in T4's Depends, so the Consequence is in scope. Using the uniform mechanism at all four `m ∈ {0, 1, 2, 3}` is consistent, but only three of those four levels lack a pre-exported lower-bound Consequence; citing NAT-zero's Consequence at the base would shorten the argument and exercise the foundation slot the review in the prior cycle introduced it for.

### Field-separator definition sits inside T4's Axiom slot
**Class**: OBSERVE
**Foundation**: T4 (HierarchicalParsing)
**ASN**: T4's Formal Contract Axiom bullet contains: "T4 stipulates that a position `i` of `t` is a *field separator* iff `tᵢ = 0`."
**Issue**: This is a definitional stipulation (a name for a decidable condition), not an axiomatic constraint on T4-valid tumblers. Sibling foundations separate these: NAT-order has a dedicated Definition slot for `≤`, `≥`, `>`. Placing a definition in the Axiom slot blurs what the axiom claims about validity versus what is mere naming. A Definition slot (or an inline definitional aside outside the Axiom bullet) would separate the two.

VERDICT: OBSERVE

## Result

Regional review converged after 4 cycles.

*Elapsed: 1684s*
