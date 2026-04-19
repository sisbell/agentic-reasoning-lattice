# Proof Verification

You are verifying a single claim's proof in an Abstract Specification Note
(ASN) for the Xanadu hypertext system.

## Claim to Verify

**Label**: {{label}}

### Claim Section

{{claim_section}}

### Dependencies

The following claims and definitions are referenced by this proof.
Use them as ground truth when checking the proof's reasoning.

{{dependency_sections}}

## Verification Checklist

1. **Precondition completeness** — Are all required inputs and conditions stated?
   What is assumed? Is anything missing?

2. **Case coverage** — Are all cases handled? Boundaries: empty inputs, zero values,
   equal operands, prefix pairs, maximum/minimum values. If the proof says "three
   cases arise," are there really only three?

3. **Postcondition establishment** — Does the proof actually establish what the
   claim claims? Or does it say "by similar reasoning" or "follows similarly"
   without showing work?

4. **All conjuncts addressed** — If the claim has multiple parts (a), (b), (c),
   is each one proved? Are any skipped?

5. **Dependency correctness** — Does the proof use the dependencies it claims?
   Are there dependencies used but not declared, or declared but not used?

6. **Formal contract** — Does the claim section end with a `*Formal Contract:*`
   section listing the applicable fields? Choose the fields that match what the
   claim actually is. Examples:

   For an operation with preconditions and postconditions:
   ```
   *Formal Contract:*
   - *Preconditions:* w > 0, actionPoint(w) ≤ #a
   - *Postconditions:* a ⊕ w ∈ T, #(a ⊕ w) = #w
   ```

   For a state invariant:
   ```
   *Formal Contract:*
   - *Invariant:* allocated(s) ⊆ allocated(s') for every transition s → s'
   ```

   For an axiom (holds by definition/design, not derived):
   ```
   *Formal Contract:*
   - *Axiom:* (a₁ = b₁ ∧ ... ∧ aₙ = bₙ ∧ #a = #b) ≡ (a = b)
   ```

   For a claim that preserves something:
   ```
   *Formal Contract:*
   - *Preconditions:* o ∈ S, w > 0, k ≤ #o
   - *Postconditions:* o ⊕ w ∈ T
   - *Frame:* subspace identifier unchanged
   ```

   For a definition:
   ```
   *Formal Contract:*
   - *Definition:* δ(n, m) = [0, ..., 0, n] of length m, action point m
   ```

   The fields are:
   - **Preconditions**: what must hold before (requires)
   - **Postconditions**: what is guaranteed after (ensures)
   - **Invariant**: what holds across all state transitions (for every s → s')
   - **Frame**: what is preserved / not changed
   - **Axiom**: fundamental assertion by definition or design, not derived
   - **Definition**: the construction or computation rule
   Only include fields that apply. A claim may have multiple fields
   (e.g., Preconditions + Postconditions + Frame).
   If the formal contract is missing or incomplete, flag as FOUND.
   If the formal contract does not match the conditions stated in the
   claim's narrative — simplified, expanded, or with added implicit
   type constraints — flag as FOUND.

7. **Missing guarantees** — Does the proof assume a guarantee that no existing
   claim in the provided dependencies establishes? If so, flag as FOUND and
   describe the missing claim that should be created.

## Output

If the proof is sound and complete:

```
RESULT: VERIFIED
```

If there is an issue:

```
RESULT: FOUND

**Problem**: [specific description of the gap, with concrete example if possible]
**Required**: [what would fix it]
```

Be specific. Cite the exact text that is wrong or missing. Construct a
counterexample if the proof misses a case.

Work only with the claim section and dependencies provided above.
Do not search for additional files or attempt tool calls.
