I read the foundation statements, then the full ASN — both the prose note and the per-claim Formal Contracts — tracing every cross-claim precondition chain to its callee.

The core algebra is sound. I verified the load-bearing chains explicitly:

- **WF** discharges all five D1 preconditions (including `divergence(s,r) ≤ #s` via the equal-length exclusion of T1 case (ii)), and routes the width `r ⊖ s` through TumblerSub's positive branch correctly (zpd defined via Divergence-symmetry + ZPD Relationship-to-Divergence). **WR** discharges D2 identically. Both are rigorous.
- **S5**'s TA-assoc application uses the correct precondition direction (`k_d ≤ #s`, `k_{d'} ≤ #d`), and the TA-LC discharge (Pos, action-point bounds, the `s ⊕ (d⊕d') = s ⊕ ℓ` chain) is complete.
- The **S8 → S9 → S10** normalization chain is well-grounded: S8's emitted spans are WF-certified well-formed level-uniform (so S9's well-formedness precondition holds), S9 correctly needs no inter-set level-compatibility (its TA-LC fires only at shared starts), and S10's level hypotheses are genuinely preserved under union.
- **S11** and **S11a–d** cover all five SC cases plus the reverse-containment orientation; the tightness argument's S0 invocation supplies `q ∈ T` and discharges the `start(α) ≤ t ≤ reach(β)` bracket. **SC**'s five-case split is exhaustive and the disjoint/overlap partition is proved per case.
- **S7**'s infinitude argument (trailing-zero extensions `s.0ⁿ ∈ ⟦σ⟧` via T1 case (ii)/(i), all in T by T0 comprehension) is correct, and `actionPoint([0,…,0,1]) = #t ≤ #t` checks out.

The S0/S11d/SC ≤-composition derivations are *not* noise — T1 exports only strict transitivity (c) for tumblers (it does not re-export ≤-transitivity the way NAT-order does), so each case-split on the `≤` abbreviation is load-bearing.

The findings below are observations, not correctness defects.

### D0 listed as "cited" but never cited
**Class**: OBSERVE
**Foundation**: D0 (DisplacementWellDefined)
**ASN**: Properties Introduced table — `| D0 | Displacement well-definedness: a < b and divergence(a, b) ≤ #a (DisplacementWellDefined, ASN-0034) | cited |`
**Issue**: D0 appears nowhere in any proof or prose body — the round-trip discharges all go through D1, D2, WF, and WR. Its sole appearance is this table row marking it "cited." D1 and D2 are genuinely cited; D0 is not. The status label is inaccurate (the displacement triple is listed for narrative completeness, but only two of the three are used).
**What needs resolving**: Mark D0's status as unused/background, or drop the row — keep the table's "cited" column truthful so a downstream dependency audit isn't misled.

### Defensive type-coherence prose in S2 precondition
**Class**: OBSERVE
**Foundation**: T12 (SpanWellDefinedness)
**ASN**: S2 (EmptyDistinction), Preconditions — "The last is a comparison of natural numbers (actionPoint(ℓ) ∈ ℕ), not the type-incoherent comparison of the tumbler s ⊕ ℓ against #s" (and the parallel sentence in the body).
**Issue**: The precondition is `actionPoint(ℓ) ≤ #s`. Nothing in it invites a reading as "`s ⊕ ℓ` against `#s`" — that phantom comparison is not in the claim. The prose refutes a misreading the precondition already excludes, which matches the reviser-drift pattern (a paragraph imagining/defending against a case the precondition rules out; likely a prior finding's content relocated rather than removed). It is text the precise reader must skip to reach the actual hypothesis.

### Use-site inventory in S6 Depends (TumblerAdd entry)
**Class**: OBSERVE
**Foundation**: TumblerAdd; S6 (LevelConstraint)
**ASN**: S6 Depends, TumblerAdd entry — "This is the sole source of the addition result-length: the in-scope foundations supply only the subtraction length (TumblerSub: #(a ⊖ w) = L) and the round-trip identity (D1: a ⊕ (b ⊖ a) = b), neither of which yields #(s ⊕ ℓ) = #ℓ for a general width ℓ."
**Issue**: The preceding sentences already establish *what* TumblerAdd supplies (`#(a⊕w) = #w`) and how it closes `#reach(σ) = #s`. This trailing sentence is a use-site inventory enumerating which other foundations *don't* supply the identity — it explains why the dependency was chosen rather than what it says, the named drift pattern for axiom-surrounding prose. It does not advance the contract.

I also note (not as a separate finding) that the verbatim "We discharge it as S11 does: each span σ ∈ {α, β} is well-formed … TumblerAdd's carrier postcondition a ⊕ w ∈ T gives reach(σ) ∈ T" block recurs identically across S1, S3, S4, S8, S11, and S11c. Each instance is load-bearing (it places a reach endpoint in T for WF), so it is not noise — but `reach(σ) ∈ T` is also immediate from T12 postcondition (a) for any well-formed span, so the longer TumblerAdd path is a stylistic choice, not a gap.

VERDICT: OBSERVE