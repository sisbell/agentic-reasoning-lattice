# Cone Review — ASN-0034/T10a-N (cycle 6)

*2026-04-16 20:56*

### TA5 Case `k > 0` verification of (a) uses T0 discreteness and order-compatibility without citation
**Foundation**: N/A (internal)
**ASN**: TA5 (HierarchicalIncrement), proof Case `k > 0` of postcondition (a) — "T1 case (ii) applies with witness `m + 1 = #t + 1 ≤ #t' = m + k`: `t` is a proper prefix of `t'`, giving `t < t'`."
**Issue**: The step "`m + 1 ≤ m + k`" is load-bearing for invoking T1 case (ii) (which requires the prefix-witness to satisfy `k ≤ #t'`). Reducing to `1 ≤ k` needs T0's discreteness (for `k ∈ ℕ`, `k > 0 ⟹ k ≥ 1` — no natural lies strictly between `0` and `1`); lifting `1 ≤ k` to `m + 1 ≤ m + k` needs T0's order-compatibility of addition. TA5's Depends for T0 itemizes several ℕ appeals ("closure of ℕ under successor…", "designated components `0` and `1`…", "verification of (a) in Case `k = 0` invokes T0's strict successor inequality…") but enumerates nothing for Case `k > 0`. T10a-N's Depends cites exactly these two T0 facts (discreteness at `m = 0`; order-compatibility at `m = #t₁`, `p = 1`, `n = k`) for the structurally identical step — the convention is already in force one property over.
**What needs resolving**: Either extend TA5's T0 entry to cite discreteness and order-compatibility of addition at the Case `k > 0` step where `k > 0` is sharpened to `k ≥ 1` and lifted to `#t + 1 ≤ #t + k` for T1 case (ii), or justify why this step may remain implicit in TA5 while T10a-N cites the same two T0 facts for the same pattern.
