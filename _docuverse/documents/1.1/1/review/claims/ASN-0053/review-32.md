Tracing the dependency chains claim by claim.

**S6 (LevelConstraint):** The derivation `#reach(σ) = #(s ⊕ ℓ) = #ℓ = #s` via TumblerAdd's result-length identity is correctly instantiated; all four of TumblerAdd's preconditions are discharged by the well-formedness hypothesis. Sound.

**WF (WellFormedSpanFromEndpoints):** The equal-length exclusion of T1 case (ii) is correctly grounded — #s = #r forces #s + 1 ≤ #s, which NAT-addcompat rules out. Divergence uniqueness then identifies the T1 witness k with divergence(s,r) ≤ #s, discharging D1's final precondition. TumblerSub's equal-length postcondition #(r ⊖ s) = max(#r, #s) = #s closes the actionPoint bound and supplies level-uniformity. Sound.

**WR (WidthRecovery):** All nine of D2's preconditions are discharged: reach(σ) ∈ T from TumblerAdd on T12's well-formedness facts; #s ≤ #reach(σ) since both equal #s; divergence(s, reach(σ)) ≤ #s by the same equal-length T1-case-(ii) exclusion used in WF, with Divergence uniqueness identifying the witness. Sound.

**S3 (MergeEquivalence):** The WLOG elimination of the `reach(β) = start(α)` adjacency disjunct is valid (would give reach(β) ≤ start(β) < reach(β) by TA-strict). The Case 2 containment argument — t ≥ reach(α) and t < r imply r > reach(α), so r = reach(β), and the overlap condition delivers t ≥ start(β) — is correctly grounded. Level_compat and S6 together equate all four boundary lengths, discharging WF's #s = #r precondition. Sound.

**S4 (SplitPartition):** WF is correctly invoked twice: at (s, p) with #s = #p from level_compat, and at (p, reach(σ)) with #p = #reach(σ) via S6. Parts (a) and (b) follow from the endpoint definitions and T1 total order. Part (c) reads directly off WF's postcondition reach(λ) = p. Sound.

**S4a (SplitMergeInverse):** The proof is correct — S4 gives the split, adjacency is checked from level_compat(s, p) and reach(λ) = p = start(ρ), S3 merges to (s, reach(σ) ⊖ s), and WR closes the identity to (s, ℓ) = σ. But the Formal Contract has a structural error.

---

### S4a Formal Contract mislabels a proved theorem as an axiom
**Class**: REVISE
**Foundation**: WR (WidthRecovery) — proved in this ASN from D2, T12, TA-strict, TA0, T1, Divergence
**ASN**: S4a (SplitMergeInverse) Formal Contract — `*Axiom:* WR — for a level-uniform span, width = reach ⊖ start.`
**Issue**: WR is a proved theorem within ASN-0053, not an axiom. The Formal Contract lists WR correctly in `*Depends:*` (as a proved dependency with a rationale annotation), then redundantly re-declares it under an `*Axiom:*` slot — a slot that appears in no other claim in this ASN and that carries the formal meaning "assumed without proof." No other claim uses this slot. A verifier consuming the Formal Contract could treat WR as ground truth and skip its proof, leaving the WR→D2 precondition chain unverified. The label also conflicts with the Depends entry in the same contract.
**What needs resolving**: Remove the `*Axiom:* WR` slot from S4a's Formal Contract. WR is already correctly captured in `*Depends:*`; the axiom label is both incorrect and redundant. If the intent was to call out WR as the load-bearing lemma, that belongs in proof prose, not in a structural slot that denotes an unproved assumption.

---

VERDICT: REVISE