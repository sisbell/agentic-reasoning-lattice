# Review of ASN-0001

## REVISE

### Issue 1: TA-strict not verified against the constructive definition
**ASN-0001, Tumbler arithmetic / TA-strict**: "Adding a positive displacement strictly advances: a ⊕ w > a for w > 0"
**Problem**: Every other axiom (TA1, TA1-strict, TA3, TA4) receives an explicit verification section showing it follows from the constructive definition of ⊕ and ⊖. TA-strict receives only a degenerate-model motivation (why it's needed) but no verification that the constructive definition satisfies it. The ASN establishes a pattern — state the axiom, give the constructive definition, verify the axiom against the definition — and then breaks it for the one axiom that T12 (span non-emptiness) depends on directly.
**Required**: Add a verification. The proof is one paragraph: let k be the action point of w. By the constructive definition, (a ⊕ w)\_i = a\_i for i < k, and (a ⊕ w)\_k = a\_k + w\_k > a\_k (since w\_k > 0, being the first nonzero component). Positions 1 through k−1 agree; position k is strictly larger. By T1 case (i), a ⊕ w > a.
**Resolution**: Already addressed. The verification paragraph exists at line 259 of the current ASN, with exactly the requested derivation.

### Issue 2: Constructive definition of ⊖ undefined for prefix-related operands of different lengths
**ASN-0001, Constructive definition of ⊖**: "let k be the first position where a and w differ"
**Problem**: The axiom TA2 promises well-definedness for all a ≥ w. But the constructive definition locates the divergence point as "the first position where a and w differ" — a component-wise scan. When w is a proper prefix of a and all trailing components of a beyond #w are zero, the tumblers are distinct by T3 but the component-wise scan finds no divergence under zero-padding.
**Required**: Either extend the constructive definition with an explicit zero-padding convention, or add a precondition.
**Resolution**: Already addressed. The constructive definition explicitly states: "When the operands have different lengths, we conceptually zero-pad the shorter to the length of the longer before scanning for divergence." The a = w case (after padding) is handled with: "the result is the zero tumbler of length max(#a, #w)." An explicit example covers the prefix case.

### Issue 3: "Action point" used before defined
**ASN-0001, TA0**: "the action point k of w satisfies k ≤ #a"
**Problem**: TA0, TA1, and TA1-strict reference "the action point k of w." The formal definition appears much later, in the "Constructive definition" section.
**Required**: Move the definition of "action point" to immediately before TA0.
**Resolution**: Already addressed. The definition appears at line 237, immediately before TA0 at line 239: "define the *action point* as k = min({i : 1 ≤ i ≤ n ∧ wᵢ ≠ 0})."

### Issue 4: Global Uniqueness Case 3 — derivation compressed to assertion
**ASN-0001, Theorem (Global uniqueness), Case 3**: "addresses with different zero counts necessarily differ in at least one component, giving a ≠ b"
**Problem**: The claim is true but the derivation is suppressed.
**Required**: Show the two cases (same length / different length) explicitly, citing T3 in each.
**Resolution**: Already addressed. Lines 212–214 show both sub-cases explicitly: "#a ≠ #b → a ≠ b by T3 directly" and "#a = #b → contradiction via zero-set equality → a ≠ b by T3."

### Issue 5: TA7a not verified from the constructive definition
**ASN-0001, TA7a (Subspace closure)**: "the shift operations are closed within each subspace"
**Problem**: The ASN provides a structural characterization of element-local displacements but never formally derives TA7a from the constructive definition of ⊕.
**Required**: Add a short derivation: identify the subspace-identifier position, confirm element-local displacements have k strictly after that position, conclude from the copy-from-start rule that the subspace identifier is preserved.
**Resolution**: Revised. The verification now begins with the 2-component V-position perspective: element-local displacement has action point k = 2, strictly after the subspace-identifier position 1; by the copy-from-start rule, (a ⊕ w)₁ = a₁ = N, preserving the subspace identifier. The ordinal-only formulation follows as the operational realization.

## DEFER

### Topic 1: Crash recovery and allocation counter monotonicity
**Why defer**: The ASN's fourth open question (allocation counter durability across crashes) is a system-level concern about implementation correctness, not a property of the tumbler algebra. T9 states what must hold; how a crashed implementation restores monotonicity is operational recovery, not algebraic specification.

### Topic 2: Version-derivation graph structure
**Why defer**: T6(d) correctly notes that structural subordination in the address does not capture derivation history. The minimal auxiliary structure for version-derivation reconstruction (the ASN's third open question) requires specifying the version graph, which is a distinct topic — document state and operations, not tumbler algebra.

### Topic 3: Zero sentinel interaction with span intersection
**Why defer**: The fourth open question (zero sentinel behavior in span arithmetic) matters for span operations, which are operational concerns for a future ASN on span algebra or enfilade structure. The tumbler algebra ASN correctly defines zero tumblers (TA6) and spans (T12); the question of what happens at the boundary is a span-operations question.

### Topic 4: Span intersection computability from the POOM
**Why defer**: The first open question (algebraic property of the POOM for span intersection) belongs in an ASN on enfilade structure or V-space operations.

VERDICT: CONVERGED
