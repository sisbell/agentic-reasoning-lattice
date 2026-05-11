# Review of ASN-0040

## REVISE

### Issue 1: B1 proof — sub-case (B) listing is incomplete and contradicts sub-case (C)

**ASN-0040, B1 proof, "All other namespaces" branch**: "(B) (p, d) violates B6 and every element of S(p, d) violates T4 — corresponding to p with a leading zero, p with adjacent zeros, p violating B6(iii) (zero budget), or d ≥ 3"

**Problem**: The listing enumerates four configurations under sub-case (B), but the parenthetical in sub-case (C) explicitly says: "When d = 2 with the same trailing-zero defect, all stream elements violate T4 and the configuration belongs to sub-case B above." So trailing-zero p combined with d = 2 also falls under (B) but is missing from the listing. This is precisely the case where the defect arises not from preserved-prefix propagation but from the union of p's trailing zero (at position #p) and TA5(d)'s separator (at position #p + 1) creating adjacent zeros in c₁ — a structurally distinct mechanism that deserves enumeration. The sub-case partition itself (whether stream contains T4-valid elements) remains correct, but the explanatory listing misleads readers about which configurations are dispatched where.

**Required**: Extend sub-case (B)'s "corresponding to" list to include "or p with trailing zero combined with d = 2", and note that the propagation mechanism here differs from TA5(b)-propagation (it arises from the conjunction of p's trailing zero and TA5(d)'s separator).

### Issue 2: Mutual forward references between B1 and B6 proofs

**ASN-0040, B1 proof**: "each of which the B6 necessity analysis below shows propagates a T4 defect to every stream element" and "which the B6 necessity analysis restricts to the trailing-zero case".

**ASN-0040, B6 proof, sub-case (b) for d = 1**: "(The stream identity is proved in B1's other-namespaces argument below.)"

**Problem**: B1's case structure for non-B6 namespaces relies on B6's necessity analysis to characterize the configurations and their propagation. B6's necessity sub-case (b) for d = 1 relies on B1's stream-identity argument S(p, 1) = S(p', 2). The proofs are not logically circular (the underlying arguments are independently grounded in TA5(b)–(d) and T4), but the textual presentation creates clumsy mutual forward references in opposite directions. A reader following B1 cannot verify its case structure without reading B6, and a reader following B6 cannot verify its sub-case (b) for d = 1 without reading B1.

**Required**: Either (a) promote the stream-identity argument S(p, 1) = S(p', 2) to a separate labeled property cited by both B1 and B6, or (b) inline the case-propagation argument (currently in B6 sub-case (a)/sub-case (ii)/sub-case (iii)) into B1's sub-case (B) so B1 is self-contained, or (c) reorder so B6 precedes B1, eliminating the forward reference from B1.

### Issue 3: TA5a restated two different ways within the same ASN

**ASN-0040, Bop correctness proof, B10 preservation**: "TA5a (IncrementPreservesT4, ASN-0034) states inc(t, k) satisfies T4 (for T4-valid t) iff `k = 0`, or `k = 1 ∧ zeros(t) ≤ 3`, or `k = 2 ∧ zeros(t) ≤ 2`."

**ASN-0040, B10 preservation proof, Case 1**: "TA5a (IncrementPreservesT4, ASN-0034) states that for any t satisfying T4, inc(t, k) satisfies T4 iff `k ∈ {0, 1}`, or `k = 2 ∧ zeros(t) ≤ 2`."

**Problem**: TA5a's actual statement (the second form) places `k ∈ {0, 1}` unconditionally for T4-valid t. The first restatement adds `zeros(t) ≤ 3` to the k = 1 case, which is redundant under T4-validity but misrepresents TA5a's structure — suggesting k = 1 has a zeros bound that it does not. The two restatements appear in adjacent proofs and create unnecessary inconsistency.

**Required**: Use the second form consistently — `k ∈ {0, 1}, or k = 2 ∧ zeros(t) ≤ 2` — matching TA5a's foundation statement.

## OUT_OF_SCOPE

No items. The Open Questions section already defers parent prerequisite, ownership, seed concretization, ghost-vs-structural distinction, bulk allocation, distributed coordination, and subspace partitioning appropriately; B3, Bridge1, and Bridge2 are explicitly framed as forward requirements; and the ASN otherwise stays within state/operations/invariants scope.

VERDICT: REVISE
