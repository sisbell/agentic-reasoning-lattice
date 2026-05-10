# Proof Verification: TA0

**Checklist Analysis**

1. **Precondition completeness** — All inputs and conditions are stated: `a ∈ T`, `w ∈ T`, `w > 0`, `actionPoint(w) ≤ #a`. Complete.

2. **Case coverage** — Three regions (prefix, action point, tail) cover all indices `1..n`. Boundary cases (k=1 making prefix vacuous, k=n making tail vacuous) are handled by the length arithmetic. Complete.

3. **Postcondition establishment** — Both `a ⊕ w ∈ T` and `#(a ⊕ w) = #w` are explicitly shown. Complete.

4. **All conjuncts addressed** — Membership in T requires (a) finite length, (b) length ≥ 1, (c) all components ∈ ℕ. All three are verified. The length identity is separately established. Complete.

5. **Dependency correctness** — **Mismatch.** The proof's dependency block declares:

   > **T0(a) (Carrier-set definition):** T is the set of all finite sequences over ℕ with length ≥ 1.

   But the provided T0(a) is **"Unbounded component values"** — the property that for every tumbler, component position, and bound M, there exists a tumbler exceeding M at that position. The carrier-set definition ("T is the set of all finite sequences over ℕ with length ≥ 1") appears only as an *axiom* within T0(a)'s formal contract, not as T0(a) itself. The proof never uses the unboundedness property; it only uses the carrier-set axiom. So T0(a) is declared but not used for what it actually states, and the carrier-set axiom is used but cited under the wrong label.

6. **Formal contract** — Preconditions and postconditions match the narrative exactly. Complete.

7. **Missing guarantees** — The proof uses closure of ℕ under addition (at the action point). T0(a)'s axiom states closure under *successor*; closure under addition follows by induction but is not explicitly provided by any declared dependency. This is minor (standard mathematical background) but worth noting.

---

```
RESULT: FOUND

**Problem**: The dependency block cites "T0(a) (Carrier-set definition)" but the
actual T0(a) is "Unbounded component values" — a different property entirely. The
proof never uses T0(a)'s unboundedness claim; it only uses the carrier-set axiom
(T is the set of all finite sequences over ℕ with length ≥ 1), which is a
foundational axiom listed *within* T0(a)'s formal contract, not T0(a) itself.

**Required**: Replace the T0(a) dependency citation with the correct label for the
carrier-set axiom (likely T0 or whichever property/axiom actually defines T's
carrier set). If no such standalone axiom exists in the spec, one should be
introduced and cited here. T0(a) should be removed from TA0's dependency list
since its content (unbounded component values) is not used by this proof.
```
