# Proof Verification: S8-depth

## Verification of S8-depth

Working through the checklist against the provided property and dependencies.

**Checklist items 1–5, 7 — the k = 0 boundary in δ and the correspondence run:**

The definition states `δ(k, m) = [0, …, 0, k]` of length `m`, with `actionPoint(δ(k, m)) = m`. When `k = 0`, `δ(0, m) = [0, …, 0]` — the zero tumbler of length `m`. This has **no nonzero component**, so `actionPoint` is undefined. The claim `actionPoint(δ(k, m)) = m` is false at `k = 0`.

The correspondence run quantifies `(A k : 0 ≤ k < n : …)`, and the narrative explicitly invokes the base case:

> At `k = 0`, `δ(0, m) = [0, …, 0]` — the zero tumbler of length `m` — so `v ⊕ δ(0, mᵥ) = v` and `a ⊕ δ(0, mₐ) = a` **by TumblerAdd**

But TumblerAdd's precondition requires **`w > 0`**, and `δ(0, m)` is the zero tumbler, which is not `> 0`. TA0 has the same precondition. The operation `v ⊕ δ(0, m)` is **undefined** under the provided dependencies.

The "What tumbler arithmetic is NOT" section in the dependencies states this explicitly:

> There is no additive identity — the zero tumbler is a sentinel, not a neutral element for addition.

The narrative treats `δ(0, m)` as an identity element while the algebra it depends on explicitly denies one exists.

**Checklist item 6 — formal contract:** The definition field claims `actionPoint(δ(k, m)) = m` unconditionally, which fails at `k = 0` as shown above.

---

```
RESULT: FOUND

**Problem**: The correspondence run definition quantifies from k = 0, but δ(0, m) is 
the zero tumbler, for which (a) actionPoint is undefined (no nonzero component), and 
(b) TumblerAdd's precondition w > 0 is violated. The narrative claims 
"v ⊕ δ(0, mᵥ) = v by TumblerAdd" but TumblerAdd explicitly requires w > 0, and the 
dependencies state "the zero tumbler is a sentinel, not a neutral element for addition."

**Required**: Either (1) split the correspondence run into a separate base case and 
an inductive step — e.g., M(d)(v) = a ∧ (A k : 1 ≤ k < n : M(d)(v ⊕ δ(k, mᵥ)) = 
a ⊕ δ(k, mₐ)) — so that ⊕ is never invoked with the zero tumbler; or (2) introduce 
a convention extending ⊕ so that t ⊕ 0_m = t for any zero tumbler of matching length, 
stated as a separate stipulation (not derived from TumblerAdd). In either case, the 
definition's unconditional claim "actionPoint(δ(k, m)) = m" must be restricted to k > 0.
```
