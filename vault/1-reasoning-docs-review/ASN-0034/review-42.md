# Proof Verification: TumblerAdd

I need to verify the TumblerAdd definition against the checklist.

**1. Precondition completeness** — The preamble states `w > 0` and the explicit precondition states `k ≤ m`. Together these are complete for the definition. ✓

**2. Case coverage** — The piecewise definition covers `i < k`, `i = k`, `i > k` — exhaustive over all positions in the result. ✓

**3. Postcondition establishment** — The result-length identity derivation:
- `p = max(k-1, 0) + (n - k + 1)` counts prefix (`k-1` positions), action point (1 position), and tail (`n - k` positions). Correct.
- `w > 0` implies `k ≥ 1`, so `max(k-1, 0) = k-1`, giving `p = (k-1) + (n-k+1) = n = #w`. Correct. ✓

**4. All conjuncts addressed** — The three named properties (no carry propagation, tail replacement, many-to-one) are all stated and illustrated. ✓

**5. Dependency correctness** — TumblerAdd is a standalone constructive definition. It does not reference any of the listed dependencies (which serve TA4's proof). No undeclared dependencies are used. ✓

**6. Formal contract** — The property section ends with the many-to-one examples. There is **no `*Formal Contract:*` section**.

**7. Missing guarantees** — N/A for a self-contained definition.

```
RESULT: FOUND

**Problem**: The TumblerAdd property section has no formal contract. The definition
establishes preconditions (w > 0, actionPoint(w) ≤ #a), a constructive rule
(the piecewise formula), and a derived postcondition (the result-length identity
#(a ⊕ w) = #w), but none of these are collected into a formal contract block.

**Required**: Append a formal contract to the end of the TumblerAdd property section:

*Formal Contract:*
- *Preconditions:* a ∈ T, w ∈ T, w > 0, actionPoint(w) ≤ #a
- *Definition:* (a ⊕ w)ᵢ = aᵢ for i < k, (a ⊕ w)ₖ = aₖ + wₖ, (a ⊕ w)ᵢ = wᵢ for i > k, where k = actionPoint(w)
- *Postconditions:* #(a ⊕ w) = #w
```
