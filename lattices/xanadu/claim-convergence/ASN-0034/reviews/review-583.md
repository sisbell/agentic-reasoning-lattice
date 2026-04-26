# Cone Review — ASN-0034/TA-dom (cycle 1)

*2026-04-26 00:54*

Reading the ASN systematically — every dependency chain, every case split, every cited postcondition.

I walked the major proofs:

**TA0** — direct export of TumblerAdd's first two postconditions; preconditions match. ✓

**ActionPoint** — uniqueness via case analysis on `m₁ < m₂ ∨ m₁ = m₂` paired with the symmetric, dispatched against irreflexivity in each pairing. The `1 ≤ w_{actionPoint(w)}` derivation correctly uses T0's commitment that components are ℕ-valued, NAT-zero's disjunction, NAT-discrete, and NAT-closure's identity at `n := 1`. ✓

**T3** — both directions discharged from T0's extensionality and Leibniz. ✓

**T1** — irreflexivity, trichotomy, and transitivity proved with case analysis walked. Trichotomy's three cases partition `T × T`; uniqueness of the witness handled across `k < k'`, `k = k'`, `k' < k`. Transitivity's nine sub-cases addressed; `(ii, ii)` correctly derived as contradictory via NAT-cancel and NAT-addcompat. ✓

**TumblerAdd** — strict advancement via T1 case (i); dominance split on `(∃ j < k : aⱼ > 0)` then on `aₖ > 0 ∨ aₖ = 0`, with NAT-cancel's mirror form correctly ruling out the equality branch when `aₖ > 0`. Tested examples `[1,1]⊕[0,2]`, `[1,1,5]⊕[0,2]`, prefix/strict cases — all consistent. ✓

**TumblerSub** — precondition `a ≥ w` correctly drives `aₖ > wₖ` at `k = zpd(a, w)` via Divergence case split with T1 case (ii) eliminations under both component and prefix divergence. Membership `a ⊖ w ∈ T`, `Pos(a ⊖ w)` via the NAT-sub right-inverse contradiction, and `actionPoint(a ⊖ w) = zpd(a, w)` via ActionPoint's uniqueness all verified. Sub-case `k > #w` with zero-padded `wₖ = 0` handled. ✓

**Divergence, ZPD, TA-dom** — contracts internally consistent; TA-dom is direct re-export. ✓

Cross-checked many-to-one example via inverse: `[1,3] ⊖ [1,1] = [0,2]` recovers `w`; cited postconditions all present in dependent contracts.

No correctness gaps, missing cases, ungrounded symbols, broken precondition chains, or unresolved references.

VERDICT: CONVERGED

## Result

Cone review converged.

*Elapsed: 953s*
