# Cross-cutting Review — ASN-0034 (cycle 3)

*2026-04-17 02:05*

Reviewing the ASN as a system for cross-cutting issues not already captured in Previous Findings.

### ℕ addition associativity used in proofs but not axiomatized

**Foundation**: (internal consistency — ASN defines NAT-* axioms to carry ℕ facts)
**ASN**: TS3 (ShiftComposition) concludes the round-trip at position m with: *"(vₘ + n₁) + n₂ = vₘ + (n₁ + n₂). These are equal by the associativity of addition in ℕ."* TA-assoc (AdditionAssociative) does the same in Case 2: *"both sides produce `a_k + b_k + c_k` at `k` (natural-number addition is associative)"* and the formal Case 2 analysis cites *"associativity of addition on ℕ"*. The five NAT-* axioms collectively state closure, additive identity, strict total order, discreteness, order-compatibility of addition, strict successor inequality, and well-ordering — none of them states associativity of `+` on ℕ.
**Issue**: Both TS3's and TA-assoc's proofs turn on a property of ℕ that has no axiomatic basis in the ASN. The ASN's stated convention is "Each proof cites only the ℕ facts it actually uses" (T0), and other proofs are careful to route every discreteness, order-compat, or well-ordering step through an explicit NAT-* citation; associativity is used the same way but isn't available to cite.
**What needs resolving**: Either extend NAT-closure (or add a new NAT-* axiom) to include associativity — and then update TS3 and TA-assoc to cite it in their Depends — or accept associativity as background arithmetic and remove the other NAT-* axioms on the same principle. As stated, the citation policy for ℕ facts is applied inconsistently between the axiomatized facts and associativity.

### TA1/TA1-strict, TA3/TA3-strict, TA4 each have two separate statements and two independent proofs

**Foundation**: (internal consistency)
**ASN**: The ASN contains "Verification" blocks that state and prove claims, followed much later by formal properties that re-state and re-prove the same claims. Specifically:
- *"Verification of TA1 and TA1-strict"* ("**Claim:** (TA1, weak form)..." + proof by case analysis on `k` vs. `divergence(a,b)`) and later *"TA1 (OrderPreservationUnderAddition)"* + *"TA1-strict (StrictOrderPreservation)"* as distinct formal properties with their own proofs.
- *"Verification of TA3"* ("**Claim:** (TA3, weak form)..." + proof with Cases 0, 0a, 1–3 and its own Formal Contract) and later *"TA3 (OrderPreservationUnderSubtractionWeak)"* with a structurally different proof organized as Cases A (sub-cases A1–A3) and B (sub-cases B1–B4) and its own Formal Contract + Depends.
- *"Verification of TA4"* ("**Claim.** `(a ⊕ w) ⊖ w = a` under the full precondition..." + proof with Sub-cases (i) and (ii)) and later *"TA4 (PartialInverse)"* with a different proof organization (Steps 1–2, Cases 1 and 2) and its own Formal Contract.

In each pair the claim is identical but the proof narrative differs — different case labels, different ordering, and in TA3's case the "Verification" contract has no Depends while the formal property's contract does.
**Issue**: The same claim has two authoritative-looking statements in the document. A reviser who tightens preconditions or repairs a proof step in one version has no mechanism to propagate the change to the other. The TA3 pair is the starkest: the two proofs enumerate cases differently, so verifying that they establish the same postcondition is a non-trivial reading exercise.
**What needs resolving**: The ASN must collapse each duplicated pair to a single authoritative statement with a single proof and a single formal contract, with the other occurrence either removed or explicitly marked as an informal sketch that defers to the formal property.
