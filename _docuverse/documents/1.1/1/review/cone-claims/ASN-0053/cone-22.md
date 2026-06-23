Reading the foundation statements, then each claim as a system.

**WR.** The proof re-derives the divergence bound divergence(s, reach(σ)) ≤ #s inline, mirroring WF's argument. The derivation uses two NAT-level facts: (1) NAT-addcompat's successor inequality `#s < #s + 1` to refute the case-(ii) bound `#s + 1 ≤ #s`, and (2) NAT-order's exactly-one trichotomy disjointness `¬(sₖ < reach(σ)ₖ ∧ sₖ = reach(σ)ₖ)` to lift `sₖ < reach(σ)ₖ` to `sₖ ≠ reach(σ)ₖ`. The proof text names both foundations explicitly ("impossible since #s < #s + 1"; "by NAT-order's exactly-one trichotomy disjointness clause"). Neither NAT-addcompat nor NAT-order appears in WR's depends list. WF correctly lists both; WR does not, despite reproducing the same argument.

The proof also says "Four discharge immediately" for D2's preconditions. D2 has nine preconditions; the enumerated four cover items (4) s < reach(σ), (7)+(8) Pos(ℓ)/actionPoint, (9) s ⊕ ℓ = reach(σ), and (6) #s ≤ #reach(σ). The carrier memberships s ∈ T, ℓ ∈ T, and reach(σ) ∈ T are not mentioned. The first two are immediate from span well-formedness; reach(σ) ∈ T requires TA0's carrier-membership postcondition (a ⊕ w ∈ T), which TA0 exports but WR's depends entry for TA0 describes only as supplying the length identity.

**S4, S3, WF, S6, S3b.** All proof steps account for their preconditions and the case analyses are complete. S6 is a one-step corollary of TumblerAdd's length postcondition and carries no unaccounted dependencies. WF correctly lists NAT-addcompat and NAT-order and walks the ≤-unfolding case analysis in full. S3's WLOG is valid (the merged-span formula is symmetric), and the converse inclusion correctly identifies max(reach(α), reach(β)) > reach(α) from t ≥ reach(α) ∧ t < r using T1's mixed ≤-< chaining. S3b's two cases both establish interiority of the split point using the (†) non-emptiness facts before invoking S4, and the WR invocations are correctly licensed. No issues found.

---

### WR: NAT-addcompat and NAT-order absent from depends
**Class**: REVISE
**Foundation**: NAT-addcompat (strict successor inequality `n < n + 1`); NAT-order (exactly-one trichotomy disjointness).
**ASN**: WR, divergence-bound subargument — "it would force #s + 1 ≤ #s, impossible since #s < #s + 1" and "whence sₖ ≠ reach(σ)ₖ by NAT-order's exactly-one trichotomy disjointness clause `¬(sₖ < rₖ ∧ sₖ = rₖ)`."
**Issue**: Both foundations are invoked by name in the proof body. Neither appears in WR's formal depends list. WF, which proves the identical sub-argument, correctly lists both. WR reproduces the argument without importing its dependencies.
**What needs resolving**: WR's depends must add NAT-addcompat (for the successor-inequality step that excludes T1 case (ii)) and NAT-order (for the trichotomy-disjointness step that converts sₖ < reach(σ)ₖ to sₖ ≠ reach(σ)ₖ).

---

### WR: reach(σ) ∈ T not articulated as a D2 precondition discharge
**Class**: OBSERVE
**Foundation**: TA0 (WellDefinedAddition) — postcondition a ⊕ w ∈ T.
**ASN**: WR proof — "Four discharge immediately" enumeration; WR depends entry for TA0 — "supplies the result-length identity `#(s ⊕ ℓ) = #ℓ = #s` … to confirm TA0's own preconditions."
**Issue**: D2 requires b ∈ T for b = reach(σ). The proof's "Four discharge immediately" does not mention reach(σ) ∈ T; it is available from TA0's carrier postcondition a ⊕ w ∈ T (TA0's preconditions hold by span well-formedness), but TA0's entry in the depends describes only the length-identity use and does not name the carrier-membership use. A consumer verifying the D2 precondition chain must independently locate this postcondition in TA0.

VERDICT: REVISE