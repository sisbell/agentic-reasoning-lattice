# Proof Verification: OrdinalShift

**Checking OrdinalShift…**

1. **Precondition completeness** — v ∈ T and n ≥ 1 are stated. The TA0 verification mentions the action-point precondition but does not explicitly verify δ(n, m) > 0 (required by TA0). It holds because n ≥ 1 makes the last component nonzero, but the check is elided. Minor.

2. **Case coverage** — m ≥ 2 and m = 1 cases are both handled for position-1 behavior. General component behavior covered.

3. **Postcondition establishment** — The narrative derives all claimed consequences (component identity, depth preservation, positivity) from TumblerAdd's constructive rule. Sound.

4. **All conjuncts addressed** — Yes.

5. **Dependency correctness** — The proof uses δ(n, m) and relies on its structure: that it equals [0, …, 0, n] of length m, that its action point is m, and that δ(n, m) ∈ T with δ(n, m) > 0. These facts come from the **OrdinalDisplacement** definition, which is **not declared as a dependency**. Both TA0 and TumblerAdd are declared and used correctly.

6. **Formal contract** — **Missing.** The property section has no `*Formal Contract:*` block.

7. **Missing guarantees** — The OrdinalDisplacement definition is needed to justify the action-point claim and the component structure of δ(n, m).

```
RESULT: FOUND

**Problem**: Two issues.
(a) The property section has no formal contract. OrdinalShift is a definition
    with derived postconditions; it needs a contract covering both.
(b) The proof uses δ(n, m) and asserts "the action point of δ(n, m) is m"
    and that its form is [0, …, 0, n], but OrdinalDisplacement is not listed
    as a dependency. Without it, the TA0 precondition check (δ(n, m) > 0,
    actionPoint = m) has no cited ground truth.

**Required**:
(a) Add a formal contract, e.g.:

    *Formal Contract:*
    - *Preconditions:* v ∈ T, n ≥ 1
    - *Definition:* shift(v, n) = v ⊕ δ(n, #v)
    - *Postconditions:* shift(v, n)ᵢ = vᵢ for i < #v,
      shift(v, n)_{#v} = v_{#v} + n, #shift(v, n) = #v,
      shift(v, n)_{#v} ≥ 1

(b) Add OrdinalDisplacement to the dependency list, citing its definition
    of δ(n, m) = [0, …, 0, n] with action point m and δ(n, m) > 0 when n ≥ 1.
```
