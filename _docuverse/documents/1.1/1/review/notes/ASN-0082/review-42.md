# Review of ASN-0082

## REVISE

No substantive REVISE items found.

The ASN is rigorous throughout:
- All foundation invariants (S0, S2, S3, S7a-d, S8-depth, S8a, S8-fin) have explicit preservation lemmas with derivations through cited foundation axioms.
- All eight insertion postconditions and six contraction postconditions undergo consistency analysis (pairwise disjointness of assignment regions, domain closure consistency).
- The NAT-sub chains for `n + ℓₘ = ℓₘ + n` and `c + c' = c' + c` are derived from foundation axioms without assuming commutativity — appropriate given that ASN-0034 omits a commutativity-of-`+` axiom.
- The TA4 necessity argument for the `#p = 2` scoping is structurally explicit: constraints (i), (ii) jointly force actionPoint(w_ord) = m − 1; constraint (iv) then requires zero prefix that collides with S8a's componentwise positivity at any depth > 2.
- Boundary cases covered: empty document, insert at start, insert past end, L = ∅, R = ∅, full deletion, cross-subspace (text active with link spectator, and link active with text spectator).
- The wp analyses for I3-VP and S8a-post surface specific foundation lemmas (TS2, TS4, subspace preservation, TA2, PositiveOffsetExceeds) as precise discharged obligations, confirming preconditions are exactly the wp-derived constraints.
- I3-V is correctly identified as a corollary of I3-CS but retained for readability — the author's defense (operational mapping clarity) is reasonable.
- D-CTG-post derives the closed form V_1(d') = {[1, k] : 1 ≤ k ≤ N − c} and verifies D-CTG's quantifier directly rather than re-citing the foundation's text-only D-CTG proof on the post-state.

## OUT_OF_SCOPE

### Topic 1: Full INSERT operation with content placement
**Why out of scope**: I3 is explicitly the shift sub-operation; the composing INSERT ASN must allocate fresh I-addresses for the gap positions and re-establish D-CTG, D-MIN, D-SEQ. The scope decision is stated at the top of the Post-Insertion Shift section and the frame I3-C correctly anticipates the weaker S0 form the composition will require.

### Topic 2: Deeper-depth contraction (#p > 2)
**Why out of scope**: The TA4 zero-prefix collision with S8a is mathematical, not a proof gap. The author identifies two paths forward (strengthened TA4 admitting non-zero prefixes when k = #a, or derivation from TumblerAdd/TumblerSub directly) — both legitimate future analysis.

### Topic 3: Link-subspace contraction
**Why out of scope**: The S = 1 scoping axiom defers link-subspace mutation (tombstoning rather than gap-closure) to a future ASN. The foundation's text-only D-CTG/D-MIN/D-SEQ supports this scoping.

### Topic 4: External-state synchronization
**Why out of scope**: Open Question 1 — when external references record V-positions, what updates does the system provide after a shift? Genuinely future work.

### Topic 5: COPY, MAKELINK, MERGE
**Why out of scope**: Other operations not covered; each merits its own arrangement-transformation analysis.

VERDICT: CONVERGED
