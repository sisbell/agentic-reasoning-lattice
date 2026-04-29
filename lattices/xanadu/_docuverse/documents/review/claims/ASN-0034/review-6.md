# Contract Review — ASN-0034 (cycle 1)

*2026-04-08 09:44*

### D0

`

- `MISSING_POSTCONDITION: #(b ⊖ a) = max(#a, #b) — the proof explicitly computes and states the length of the displacement as max(#a, #b) from TumblerSub; this result is absent from the contract`
- `MISSING_POSTCONDITION: #a > #b → a ⊕ (b ⊖ a) ≠ b — the proof explicitly derives and names the round-trip boundary condition: when #a > #b, the result length max(#a,#b) = #a > #b, so T3 gives inequality; the contract omits this proven failure mode entirely`

### T4

- `INACCURATE: T4a conflates two separate constraints. The proof distinguishes: (1) the positive-component constraint — "every non-separator component is strictly positive" — stated as a standalone conjunct of the axiom T4; and (2) the non-empty field constraint — "each present field has at least one component" — which T4a proves equivalent to the three syntactic conditions. The contract's T4a bundles both into one statement: "each present field has ≥ 1 component with all components strictly positive" ↔ syntactic conditions. This misrepresents what T4a specifically establishes: T4a's proven equivalence is between the non-empty field constraint alone and the syntactic conditions. The positive-component constraint is an independent axiom conjunct, not part of the equivalence T4a proves.`

### TA-RC

- `INACCURATE: The contract uses precondition/postcondition format, which implies universal quantification (for all a, b, w satisfying the preconditions, the postcondition holds). But TA-RC is an existence property — the proof exhibits specific witnesses. As a universal claim the contract is false: a = b = [1,3,5] with w = [0,2,4] satisfies all listed preconditions yet a = b, contradicting the postcondition a ≠ b. The contract should be stated existentially: ∃ a, b, w ∈ T : w > 0 ∧ actionPoint(w) ≤ #a ∧ actionPoint(w) ≤ #b ∧ a ≠ b ∧ a ⊕ w = b ⊕ w.`

### TA5

- `INACCURATE: Postcondition (b) uses the undefined term "increment point" — `(A i : 1 ≤ i < increment point : t'ᵢ = tᵢ)`. The proof's verification section establishes two distinct bounds: for `k = 0`, agreement holds for `1 ≤ i < sig(t)`; for `k > 0`, agreement holds for `1 ≤ i ≤ #t`. The term "increment point" is never formally defined in the contract, making (b) unverifiable mechanically. The contract should either define "increment point" explicitly as `sig(t)` when `k = 0` and `#t + 1` when `k > 0`, or split postcondition (b) into two case-guarded claims mirroring the proof's structure.`

4 mismatches.
