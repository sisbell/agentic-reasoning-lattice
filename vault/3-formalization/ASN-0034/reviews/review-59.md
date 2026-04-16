# Cone Review — ASN-0034/T8 (cycle 5)

*2026-04-15 23:00*

I've reviewed the entire ASN systematically, tracing every dependency chain, quantifier scope, and case analysis. Most cross-property relationships are sound, and many issues from previous cycles have been addressed in the current text (T1 now has `Depends: T3`, T4 now has T4a–T4c postconditions, TumblerSub now exports strict `aₖ > wₖ`, T8 Frame now includes `inc via TA5`, TA5 now has `t' ∈ T` postcondition).

One new finding:

---

### TA5 (HierarchicalIncrement) formal contract has no Depends clause, despite the proof invoking T1 by name in both case analyses for postcondition (a)

**Foundation**: T1 (LexicographicOrder) — case (i) for component divergence, case (ii) for proper prefix
**ASN**: TA5 (HierarchicalIncrement) proof: case `k = 0` — "By T1 case (i) with divergence position `j`, the agreement on positions `1, ..., j − 1` and the strict inequality `t_j < t'_j` yield `t < t'`"; case `k > 0` — "T1 case (ii) applies with witness `m + 1 = #t + 1 ≤ #t' = m + k`: `t` is a proper prefix of `t'`, giving `t < t'`." Formal contract contains Preconditions, Definition, and Postconditions but no Depends clause. YAML metadata declares `depends: [T1]`.
**Issue**: The proof establishes postcondition (a) `t' > t` by explicitly invoking T1's case structure — case (i) for `k = 0` and case (ii) for `k > 0`. The YAML metadata correctly records `depends: [T1]`, but the prose contract has no Depends field at all. A contract reader sees the postcondition annotation "under T1" but cannot trace that T1's case-level structure was actually invoked as a proof tool without reading the proof body. This is the same class of gap that was identified and fixed for T1 (`Depends: T3`), T2 (`Depends: T3`), and TumblerAdd (`Depends: T1, T3`) — each of those properties now has a Depends clause in the prose contract bridging the postcondition annotation to the proof's actual dependency. TA5 was reviewed in cycle 1 but only the missing `t' ∈ T` postcondition was caught; the missing Depends clause was not.
**What needs resolving**: TA5's formal contract must include a Depends clause declaring T1 (LexicographicOrder), consistent with the pattern established by T1, T2, and TumblerAdd contracts in the same ASN. Specifically: postcondition (a) for `k = 0` invokes T1 case (i) at divergence position `sig(t)`, and postcondition (a) for `k > 0` invokes T1 case (ii) with the proper-prefix condition.
