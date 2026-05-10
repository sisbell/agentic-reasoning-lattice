# Review of ASN-0001

## REVISE

### Issue 1: TA-strict not verified against the constructive definition
**ASN-0001, Tumbler arithmetic / TA-strict**: "Adding a positive displacement strictly advances: a ⊕ w > a for w > 0"
**Problem**: Every other axiom (TA1, TA1-strict, TA3, TA4) receives an explicit verification section showing it follows from the constructive definition of ⊕ and ⊖. TA-strict receives only a degenerate-model motivation (why it's needed) but no verification that the constructive definition satisfies it. The ASN establishes a pattern — state the axiom, give the constructive definition, verify the axiom against the definition — and then breaks it for the one axiom that T12 (span non-emptiness) depends on directly.
**Required**: Add a verification. The proof is one paragraph: let k be the action point of w. By the constructive definition, (a ⊕ w)\_i = a\_i for i < k, and (a ⊕ w)\_k = a\_k + w\_k > a\_k (since w\_k > 0, being the first nonzero component). Positions 1 through k−1 agree; position k is strictly larger. By T1 case (i), a ⊕ w > a.

### Issue 2: Constructive definition of ⊖ undefined for prefix-related operands of different lengths
**ASN-0001, Constructive definition of ⊖**: "let k be the first position where a and w differ"
**Problem**: The axiom TA2 promises well-definedness for all a ≥ w. But the constructive definition locates the divergence point as "the first position where a and w differ" — a component-wise scan. When w is a proper prefix of a and all trailing components of a beyond #w are zero (e.g., a = [1, 0, 3, 0], w = [1, 0, 3]), the tumblers are distinct by T3 (different lengths) and ordered a > w by T1 case (ii), so the precondition a ≥ w is satisfied. Yet the component-wise scan finds no divergence: positions 1–3 agree, and position 4 of a is 0, matching a zero-padded w. The constructive definition does not specify the result.

The ASN handles the a = w case explicitly ("the result is the zero tumbler of length #a") but not the a > w prefix case where components agree under zero-padding. Gregory's implementation sidesteps this because `strongsub` operates on fixed-length mantissa arrays (implicit zero-padding with a definite length), but the abstract definition has no such padding convention.

No current use of ⊖ in the ASN exercises this case — V-space shifts use same-length operands, and TA4's preconditions prevent it — but the gap between TA2's promise and the constructive definition's coverage should be closed.
**Required**: Either (a) extend the constructive definition with an explicit convention for different-length operands (e.g., zero-pad the shorter to the length of the longer), or (b) add a precondition #a = #w to the constructive definition and note that TA2's well-definedness for different-length prefix-related operands is guaranteed by the axiom but not exhibited by the constructive algorithm as given.

### Issue 3: "Action point" used before defined
**ASN-0001, TA0**: "the action point k of w satisfies k ≤ #a"
**Problem**: TA0, TA1, and TA1-strict all reference "the action point k of w." The formal definition — k = min({i : 1 ≤ i ≤ n ∧ w\_i ≠ 0}) — appears much later, in the "Constructive definition" section. A reader encountering the axioms must infer the meaning from context. The ASN is self-contained; forward references to not-yet-defined terms undermine that.
**Required**: Move the definition of "action point" to immediately before TA0 (where it is first used), or state the definition inline in TA0.

### Issue 4: Global Uniqueness Case 3 — derivation compressed to assertion
**ASN-0001, Theorem (Global uniqueness), Case 3**: "addresses with different zero counts necessarily differ in at least one component, giving a ≠ b"
**Problem**: The claim is true but the derivation is suppressed. The chain is: if #a = #b, then identical components would give identical zero counts (contrapositive: different zero counts with same length implies some component differs), so a ≠ b by T3. If #a ≠ #b, then a ≠ b by T3 directly. This is two sentences, not zero.
**Required**: Show the two cases (same length / different length) explicitly, citing T3 in each.

### Issue 5: TA7a not verified from the constructive definition
**ASN-0001, TA7a (Subspace closure)**: "the shift operations are closed within each subspace"
**Problem**: The ASN provides a structural characterization of element-local displacements and a detailed discussion of INSERT/DELETE implementation strategies, but never formally derives TA7a from the constructive definition of ⊕. The argument is: for an element-local displacement w with action point k strictly after the subspace-identifier position, positions i < k are copied from a (preserving the subspace identifier), and the addition at position k and tail replacement at positions > k affect only the element field. This is straightforward from the constructive definition but not shown.
**Required**: Add a short derivation: identify the subspace-identifier position in the address structure, confirm that element-local displacements have k strictly after that position, and conclude from the constructive definition's "copy from start" rule that the subspace identifier is preserved.

## OUT_OF_SCOPE

### Topic 1: Crash recovery and allocation counter monotonicity
**Why defer**: The ASN's fourth open question (allocation counter durability across crashes) is a system-level concern about implementation correctness, not a property of the tumbler algebra. T9 states what must hold; how a crashed implementation restores monotonicity is operational recovery, not algebraic specification.

### Topic 2: Version-derivation graph structure
**Why defer**: T6(d) correctly notes that structural subordination in the address does not capture derivation history. The minimal auxiliary structure for version-derivation reconstruction (the ASN's third open question) requires specifying the version graph, which is a distinct topic — document state and operations, not tumbler algebra.

### Topic 3: Zero sentinel interaction with span intersection
**Why defer**: The fourth open question (zero sentinel behavior in span arithmetic) matters for span operations, which are operational concerns for a future ASN on span algebra or enfilade structure. The tumbler algebra ASN correctly defines zero tumblers (TA6) and spans (T12); the question of what happens at the boundary is a span-operations question.

### Topic 4: Span intersection computability from the POOM
**Why defer**: The first open question (algebraic property of the POOM for span intersection) belongs in an ASN on enfilade structure or V-space operations.

VERDICT: REVISE
