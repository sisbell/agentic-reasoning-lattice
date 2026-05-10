# Review of ASN-0081

## REVISE

(none)

## OUT_OF_SCOPE

### Topic 1: Generalization to ordinal depth greater than one
**Why out of scope**: The ASN honestly restricts to depth 2 via an explicit scoping axiom and lists the generalization as an open question. At depth > 1, TA4's zero-prefix condition (`(A i : 1 ≤ i < k : aᵢ = 0)`) conflicts with ordinals in S (all-positive components), so the round-trip `(ord(p) ⊕ w_ord) ⊖ w_ord = ord(p)` fails for displacements acting above the deepest level. This is genuine new territory requiring a different algebraic approach.

### Topic 2: Composition of sequential contractions
**Why out of scope**: Since all invariants (D-CTG, D-MIN, S8-depth, S8a, S8-fin, S2, S3) are verified in the post-state, a second contraction's preconditions are satisfiable — but the ASN doesn't address whether composed contractions commute or how cumulative shifts interact. This belongs in a future operations ASN.

### Topic 3: Interaction between contraction and link-subspace references
**Why out of scope**: The contraction removes V-positions from a single subspace. Content referenced by those positions persists in the Istream (D-I), but links in subspace 2 that reference the now-unreferenced I-addresses are unaffected at the arrangement level. The semantic consequences (link dangling, endset integrity) belong in a link operations ASN.

---

**Commentary.** This ASN is clean. The ordinal extraction functions (ord, vpos, w\_ord) correctly implement the ordinal-only formulation from TA7a, separating subspace structure from within-subspace arithmetic. The shift σ is defined algebraically and the three key properties — order-preservation/injectivity (D-BJ via TA3-strict), gap closure (D-SEP via TA4), and dense partition (D-DP combining the first two) — are fully derived with all foundation preconditions verified. The invariant preservation section covers every ASN-0036 invariant systematically, and the four worked examples (standard case, L=∅, R=∅, full deletion) verify all postconditions against concrete state. The depth-2 scoping is honest about what it buys (vacuous TA4 zero-prefix, trivial TA3-strict equal-length) and what it costs (the open question is real, not cosmetic). The D-DOM formulation correctly handles the subtle case where shifted Q₃ positions coincide with former X positions — the worked example explicitly verifies this. The cross-subspace and cross-document frame conditions (D-CS, D-CD) are stated with both domain equality and mapping equality conjuncts, which the invariant proofs correctly rely on.

VERDICT: CONVERGED
