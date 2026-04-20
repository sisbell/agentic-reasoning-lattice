# Proof Verification: TumblerSub

I'll work through the verification checklist systematically for the proofs in the TumblerSub property section.

**1. Precondition completeness** — All required inputs and conditions are stated for TA1/TA1-strict (a < b, w > 0, k ≤ min(#a, #b)), TA3/TA3-strict (a < b, a ≥ w, b ≥ w, plus #a = #b for strict), and TA4 (k = #a, #w = k, zero prefix). TA4 implicitly requires w > 0 through the existence of an action point, which is acceptable.

**2. Case coverage** — TA1/TA1-strict: three cases (k < j, k = j, k > j) are exhaustive; the prefix sub-case of T1(ii) forces k < j and falls into Case 1. TA3: Case 0 (prefix), Case 0a (component divergence + zero-padded equality with w), Cases 1–3 (component divergence + divergence with w) are exhaustive and correctly partitioned. Case 2 impossibility is valid. TA3-strict: eliminating Case 0 via #a = #b is sound; the remaining cases all produce strict inequality. TA4: two sub-cases on a_k cover all possibilities.

**3. Postcondition establishment** — Each case of TA1 establishes ≤ (via equality or strict). TA1-strict establishes strict inequality in Cases 2 and 3. Every TA3 case establishes ≤. TA3-strict's remaining cases all establish strict. TA4 reconstructs a in both sub-cases.

**4. All conjuncts addressed** — Each property has a single postcondition and each is proved.

**5. Dependency correctness** — The proofs use T1 (order definition/comparison), TumblerAdd constructive definition and TA0 (via TA1's dependency), TA2 (well-definedness of subtraction), TumblerSub (the definition under verification), and the inline derivation (†) from T1 alone. No undeclared dependencies are used. The Divergence definition is correctly applied in the transition to Cases 1–3 and in TA1-strict.

**6. Formal contract** — TumblerSub definition has a correct formal contract. TA3 and TA3-strict have correct formal contracts matching their narrative claims. TA1 and TA1-strict are formally contracted in the dependencies section. However, **TA4 has no formal contract anywhere** — neither in the property section nor in the dependencies. The claim is stated in prose but lacks the required `*Formal Contract:*` block.

**7. Missing guarantees** — The TA3 proof's inline derivation (†) is fully established from T1. The TA4 proof implicitly verifies r ≥ w (needed for TumblerSub to apply) via construction. No missing external guarantees.

---

```
RESULT: FOUND

**Problem**: The TA4 verification (cancellation: `(a ⊕ w) ⊖ w = a`) has no `*Formal Contract:*` block. It is the only property in the section that is both defined and proved here (not inherited from the dependencies) yet lacks a formal contract. The claim text states preconditions in prose ("under the full precondition: k = #a, #w = k, (A i : 1 ≤ i < k : aᵢ = 0)") but does not formalize them.

**Required**: Add a formal contract after the TA4 proof, e.g.:

    *Formal Contract:*
    - *Preconditions:* a ∈ T, w ∈ T, w > 0, actionPoint(w) = #a, #w = #a, (A i : 1 ≤ i < #a : aᵢ = 0)
    - *Postconditions:* (a ⊕ w) ⊖ w = a
```
