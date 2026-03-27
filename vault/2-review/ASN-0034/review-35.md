# Proof Verification: T3

## Verification

**Checklist analysis:**

1. **Precondition completeness** — `a, b ∈ T` stated. ✓
2. **Case coverage** — Both directions of the biconditional proved (forward and reverse). ✓
3. **Postcondition establishment** — The proof establishes the claimed biconditional via extensional sequence equality (forward) and Leibniz's law (reverse). ✓
4. **All conjuncts addressed** — Both directions shown. ✓
5. **Dependency correctness** — The proof states: *"T3 is derived from T0's characterisation of the carrier set. By T0, T is the set of all finite sequences over ℕ."* T0 is explicitly used to establish that tumblers **are** their component sequences (no quotient, no normalization map), which is the entire basis of the extensionality argument. Without T0, you cannot rule out that T imposes additional identification on sequences. Yet the Dependencies section lists **(none)**.
6. **Formal contract** — Uses "Postconditions" for a derived property, which is consistent with the Axiom→Postconditions revision (commit `53b890e`). Content matches the narrative. ✓
7. **Missing guarantees** — Same as item 5; T0 supplies the needed guarantee. No other missing guarantees.

```
RESULT: FOUND

**Problem**: The proof explicitly depends on T0 ("T3 is derived from T0's characterisation of the carrier set. By T0, T is the set of all finite sequences over ℕ.") but the Dependencies section declares (none). T0's definition that T is the set of finite sequences over ℕ — with no quotient or normalization — is the premise that makes the extensionality argument valid. Without it, the proof has no basis for asserting that sequence equality is the only equality on T.

**Required**: Declare T0 (specifically T0(a), the carrier-set definition) as a dependency of T3 and include its statement in the Dependencies section so the proof's reasoning chain is grounded.
```
