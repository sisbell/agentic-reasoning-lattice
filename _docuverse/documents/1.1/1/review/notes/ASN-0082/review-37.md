# Review of ASN-0082

## REVISE

(none)

## OUT_OF_SCOPE

### Topic 1: Full INSERT operation (gap content placement)
**Why out of scope**: This ASN explicitly scopes I3 to the shift sub-operation and acknowledges that a composing INSERT must extend `dom(C)` with fresh I-addresses, fill gap positions, and re-establish D-CTG/D-MIN/D-SEQ for the text subspace. The text frames this directly and motivates the I3-C → S0 weakening cleanly.

### Topic 2: Contraction at depth #p > 2
**Why out of scope**: The "Necessity from TA4" discussion derives the mathematical obstruction — TA4's zero-prefix condition (iv) at k = m − 1 > 1 collides with S8a's componentwise positivity on `ord(p)`. The Open Question correctly defers generalization, and the depth-2 restriction is justified, not arbitrary.

### Topic 3: Link-subspace contraction (tombstoning)
**Why out of scope**: The subspace scoping axiom (S = 1) explicitly defers non-text contraction to a future ASN that handles tombstone semantics, since shift-to-close-gap is not the right mutation for sparse, tombstone-bearing V_2(d).

### Topic 4: Span-level results for non-ordinal-level widths (actionPoint(ℓ) < m)
**Why out of scope**: I3-S and D-S restrict to ordinal-level widths. The text justifies this: a width with actionPoint < m operates on a different axis than the shift's δₙ, and the commutativity arguments that drive both proofs no longer apply. Span-level preservation in this regime is genuinely different mathematics.

### Topic 5: External V-position reference synchronization
**Why out of scope**: Listed in Open Questions. Concerns the interface between system state and external clients (cursors, selections, citations) holding V-position references that shift relocates.

### Topic 6: Other operations (REARRANGE, COPY, MAKELINK)
**Why out of scope**: This ASN is scoped to the displacement arithmetic of INSERT's shift sub-operation and DELETE's contraction. Other operations belong in separate ASNs that compose this displacement work with their own state mutations.

VERDICT: CONVERGED

The ASN is exceptionally rigorous. Every contract conjunct (I3, I3-V, I3-L, I3-X, I3-D, I3-C, I3-CS, I3-CX for insertion; D-SHIFT, D-L, D-DOM, D-CS, D-CD, D-I for contraction) has its consistency checked pairwise, its derived invariant lemmas worked, and its boundary cases (L = ∅, R = ∅, both empty, empty subspace, insert at start/end, cross-subspace) exercised in worked examples. The wp analyses for I3-VP, I3-S2, S8a-post, and S2-post are non-trivial multi-case derivations that surface exactly the foundation lemmas (TS2, TS4, OrdAddS8a, TA4 obstruction, D-BJ, D-DP) the contract is built to discharge. The TA-assoc preconditions, NAT-sub commutativity instances, and TumblerSub divergence-point arithmetic in I3-S(a) and D-S(a) are derived step-by-step with no appeal to unjustified commutativity. The asymmetry between insertion (general depth, general subspace) and contraction (depth 2, text only) is mathematically forced by TA4 and explained explicitly. The lemma ordering (typing → contiguity → finiteness → functionality → integrity → allocation) is internally consistent, with each lemma citing only previously-established results. Foundation references are exclusively to ASN-0034, ASN-0036, and ASN-0053.
