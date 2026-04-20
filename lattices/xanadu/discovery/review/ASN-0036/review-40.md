# Proof Verification: S7b

**Analysis of S7b**

S7b is a design requirement (axiom): every Istream address has exactly three zeros, meaning all four tumbler fields are present. It uses T4's field correspondence to interpret `zeros(a) = 3`. S7a appears only in the forward-looking sentence "With S7a and S7b established, we can state structural attribution" — it is not used to establish S7b itself.

**Checklist:**

1. **Precondition completeness** — OK. The domain `dom(Σ.C)` is the only input.
2. **Case coverage** — N/A (axiom, not a case-based proof).
3. **Postcondition establishment** — OK. Design requirement, asserted not derived.
4. **All conjuncts addressed** — OK. Single conjunct `zeros(a) = 3`.
5. **Dependency correctness** — S7a is declared as a dependency but never used to establish S7b. It is a co-requisite for downstream properties, not a dependency of this one. T4 is correctly used (field correspondence interpretation).
6. **Formal contract** — **Missing.** The property section has no `*Formal Contract:*` block. As a design axiom, it should have one.
7. **Missing guarantees** — None.

```
RESULT: FOUND

**Problem**: (a) No formal contract. S7b is a design axiom and needs a formal contract block. 
(b) S7a is listed as a dependency but is not used to establish S7b — it appears only in a forward-looking statement about downstream consequences.

**Required**: 
(a) Add a formal contract:
   *Formal Contract:*
   - *Axiom:* (A a ∈ dom(Σ.C) :: zeros(a) = 3)

(b) Remove S7a from S7b's dependency list. S7a is a co-requisite for the downstream "structural attribution" statement, not a dependency of S7b itself. If the downstream property needs both, it should declare both as its own dependencies.
```
