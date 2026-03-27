### [REVIEW-32] [FOUND] T3
Looking at T3's proof against the verification checklist:

**1. Precondition completeness** — Fine. Requires a, b ∈ T.

**2. Case coverage** — Both directions of the biconditional are addressed.

**3. Postcondition establishment** — Both directions are explicitly shown with clear reasoning.

**4. All conjuncts addressed** — Forward and reverse both proved. ✓

**5. Dependency correctness** — The proof explicitly states: "By T0, T is the set of all finite sequences over ℕ." This is the load-bearing premise — the entire argument rests on the carrier set definition from T0. Yet the dependency list declares **(none)**.

Furthermore, the formal contract labels T3 as an **Axiom**, but the proof itself *derives* T3 from T0: "T3 is not derived from other properties; it holds by the definition of the carrier set. By T0, T is the set of all finite sequences over ℕ." These two claims are in tension — the proof simultaneously says it is not derived and then derives it from T0. Either T3 is an axiom (needing no justification from T0) or it is a consequence of T0 (making it derived, not axiomatic, and requiring T0 as a declared dependency).

**6. Formal contract** — The formal contract content accurately captures the property statement. The biconditional matches. However, the **Axiom** label is inconsistent with the proof's own derivation from T0.

**7. Missing guarantees** — No guarantees are assumed beyond T0.

```
RESULT: FOUND

**Problem**: The proof invokes T0 ("By T0, T is the set of all finite sequences over ℕ") as its central justification, but declares no dependencies. The formal contract labels T3 as an *Axiom*, which contradicts the proof body's own derivation from T0. The proof cannot simultaneously claim "not derived from other properties" and then cite T0 as the ground on which it stands.

**Required**: Either (a) declare T0 as a dependency, change the formal contract from *Axiom* to a derived form (e.g., *Postconditions* or a simple theorem statement), and remove the claim "T3 is not derived from other properties"; or (b) if T3 is genuinely intended as an axiom that stands independently, remove the appeal to T0 from the proof and state that sequence extensionality is adopted as a primitive design commitment, not derived from the carrier-set definition.
```

### [REVIEW-33] [FOUND] T3
## Verification

**Checklist walkthrough:**

1. **Precondition completeness** — The proof requires `a, b ∈ T` and that T is the set of finite sequences over ℕ (from T0). Complete.

2. **Case coverage** — Both directions of the biconditional are proved. Empty sequences (length 0) are handled: forward direction holds vacuously (no components to compare, lengths both 0), reverse direction trivially. Fine.

3. **Postcondition establishment** — Forward direction: extensional sequence equality. Reverse direction: Leibniz's law. Both sound and explicitly shown. The "no quotient/normalization" design commitment is addressed in the concluding paragraph. Matches the formal contract.

4. **All conjuncts addressed** — Two directions of the biconditional, both proved. ✓

5. **Dependency correctness** — The proof explicitly states: *"T3 is derived from T0's characterisation of the carrier set. By T0, T is the set of all finite sequences over ℕ."* Yet the dependency list declares **(none)**. T0 is used but not declared.

6. **Formal contract** — The postcondition `a = b ⟺ #a = #b ∧ (∀ i : 1 ≤ i ≤ #a : aᵢ = bᵢ)` matches the property statement. The "Postconditions" label is reasonable for a derived property (consistent with the recent Axiom→Postconditions revision). Contract matches narrative.

7. **Missing guarantees** — The proof's correctness depends entirely on T0 defining T as bare finite sequences over ℕ with no quotient structure. Without T0 declared, this cannot be verified against the actual statement.

---

```
RESULT: FOUND

**Problem**: The proof explicitly derives T3 from T0 — "T3 is derived from T0's
characterisation of the carrier set. By T0, T is the set of all finite sequences
over ℕ" — but the dependency list declares (none). T0 is the sole load-bearing
dependency and is undeclared.

**Required**: Add T0 (carrier set definition) as a declared dependency of T3.
```

### [REVIEW-34] [FOUND] T3
**Checking dependency correctness.**

The proof opens with: *"T3 is derived from T0's characterisation of the carrier set. By T0, T is the set of all finite sequences over ℕ."* It then relies on T0 throughout both directions — the forward direction appeals to extensional sequence equality on T0's carrier set, and the reverse direction applies Leibniz's law to elements of that same carrier set.

Yet the declared dependencies section states: **(none)**.

```
RESULT: FOUND

**Problem**: T0 is used but not declared as a dependency. The proof explicitly states "T3 is derived from T0's characterisation of the carrier set" and relies on T0's definition of T as the set of all finite sequences over ℕ for both directions of the biconditional. The dependencies section lists "(none)".

**Required**: Declare T0 as a dependency of T3.
```

### [REVIEW-35] [FOUND] T3
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

### [REVIEW-36] [VERIFIED] T3

### [REVIEW-36] [RESOLVED] T3

### [REVIEW-36] [VERIFIED] T1

### [REVIEW-36] [VERIFIED] TA1

### [REVIEW-36] [FOUND] Divergence
Looking at the Divergence definition section against the checklist:

**1. Precondition completeness** — `a, b ∈ T`, `a ≠ b` are stated. Complete.

**2. Case coverage** — The two cases are mutually exclusive (case (i) requires a disagreement within the shared range; case (ii) requires full agreement) and exhaustive for `a ≠ b` (if no shared-position disagreement exists, T3 forces `#a ≠ #b` to avoid `a = b`). The uniqueness of `k` in case (i) follows from the universal agreement prefix `(A i : 1 ≤ i < k : aᵢ = bᵢ)` combined with `aₖ ≠ bₖ`. Sound.

**3–4. Postcondition / conjuncts** — The "exactly one case applies" claim is asserted with adequate informal justification via T1's case structure. Acceptable for a definition.

**5. Dependency correctness** — T1 is used (the two divergence cases mirror T1's two ordering cases). TA0 and TA1-strict are referenced in the motivating paragraph about unsatisfiability. These are correctly listed. T3 is used implicitly for exhaustiveness (same-length + all-components-equal ⟹ equal) but is available transitively through T1's proof.

**6. Formal contract** — The Divergence section has no `*Formal Contract:*` block. Every other property in the dependencies (T1, TA0, TA1, TA1-strict) has one. A definition should have at minimum:

```
*Formal Contract:*
- *Preconditions:* a ∈ T, b ∈ T, a ≠ b
- *Definition:* divergence(a, b) = k where (i) k = min({i : 1 ≤ i ≤ min(#a, #b) ∧ aᵢ ≠ bᵢ}) if such i exists, or (ii) k = min(#a, #b) + 1 otherwise
```

**7. Missing guarantees** — No external guarantees assumed beyond what dependencies provide.

```
RESULT: FOUND

**Problem**: The Divergence definition section has no `*Formal Contract:*` block. All other properties in the ASN (T1, TA0, TA1, TA1-strict) include one. Per the specification's own convention, each property section must end with a formal contract summarizing its interface.

**Required**: Append a formal contract to the Divergence definition, e.g.:

*Formal Contract:*
- *Preconditions:* a ∈ T, b ∈ T, a ≠ b
- *Definition:* divergence(a, b) = k, where (i) if ∃ i with 1 ≤ i ≤ min(#a, #b) and aᵢ ≠ bᵢ, then k = min({i : 1 ≤ i ≤ min(#a, #b) ∧ aᵢ ≠ bᵢ}); (ii) otherwise k = min(#a, #b) + 1
```

### [REVIEW-37] [VERIFIED] Divergence

### [REVIEW-37] [RESOLVED] Divergence

### [REVIEW-37] [VERIFIED] TA1-strict

### [REVIEW-37] [VERIFIED] T4

### [REVIEW-37] [VERIFIED] TA6

### [REVIEW-37] [VERIFIED] TA2

### [REVIEW-37] [VERIFIED] TA3

### [REVIEW-37] [FOUND] TumblerSub
## Verification

I need to check the proofs of TA1/TA1-strict, TA3/TA3-strict, and TA4 within the TumblerSub property section against the provided dependencies.

**Checklist items 1–4 (Preconditions, Case coverage, Postcondition establishment, Conjuncts):** The proofs are thorough. TA1 local proof correctly handles three cases on the relationship between action point `k` and divergence `j`. TA3 exhaustively partitions into prefix (Case 0) and component-divergence (Cases 0a, 1–3), with appropriate sub-cases for the relationship between operands and `w`. TA3-strict correctly eliminates Case 0 via the equal-length precondition, and the remaining cases all yield strict inequality. TA4's restricted preconditions (`k = #a`, `#w = k`, zero-prefix) are necessary — general cancellation fails (e.g., `a = [1,5]`, `w = [2]` gives `(a ⊕ w) ⊖ w = [1] ≠ a`).

**Checklist item 5 (Dependency correctness):** The TA3 proof references **TA6** by name in three locations:

1. Case 0, sub-case `a = w`: *"every zero tumbler is less than every positive tumbler (TA6)"*
2. Case 0, sub-case `a > w` without divergence: *"a ⊖ w (all zeros) is strictly less by TA6"*
3. Case 0a: *"By TA6, a ⊖ w < b ⊖ w"*

**TA6 does not appear in the listed dependencies** (Divergence, T1, TA1, TA1-strict, TA2, TA3). While TA6's content is derivable from T1 — a zero tumbler `z` compared to a positive tumbler `p` with first nonzero at position `j`: if `j ≤ #z`, T1 case (i) gives `z < p`; if `j > #z`, T1 case (ii) gives `z < p` as a proper prefix — it is cited as a named, standalone property rather than derived inline. A dependency used but not declared.

```
RESULT: FOUND

**Problem**: The TA3 proof invokes "TA6" (every zero tumbler is strictly less than every positive tumbler) in three separate cases, but TA6 is not listed in the dependency section. The dependency list contains only: Divergence, T1, TA1, TA1-strict, TA2, TA3.

**Required**: Add TA6 to the dependency list with its statement and formal contract, or replace each TA6 citation with an inline derivation from T1 (which is already a declared dependency).
```
