# Review of ASN-0065

## REVISE

### Issue 1: Body text contradicts Open Questions on depth generalization

**ASN-0065, State and Vocabulary**: "This restriction simplifies the displacement arithmetic considerably; generalization to deeper ordinals is an open question."

**ASN-0065, Open Questions**: "The depth-2 restriction [...] is a presentational simplification, not a technical limitation [...] generalization to arbitrary depth is immediate."

**Problem**: The body text calls depth generalization "an open question," while the Open Questions section calls it "immediate" by D-CTG-depth. These characterizations are in tension. A reader encountering the body text first is led to believe the generalization is unsettled; the Open Questions section then contradicts this by resolving it in a sentence. If it is immediate, do not call it open; if it is open, do not call it immediate.

**Required**: Align the two passages. Either (a) change the body to "generalization to deeper ordinals is structurally identical by D-CTG-depth (ASN-0036); see Open Questions" and keep the Open Questions note as-is, or (b) remove the Open Questions note and keep the body's "open question" framing, acknowledging that the formal treatment at arbitrary depth has not been carried out in this ASN. Pick one story and tell it consistently.

---

No other issues found. The ASN is technically rigorous and I verified the following in detail:

**Postconditions fully specified.** R-P1/R-P2/R-EXT (3-cut) and R-S1/R-S2/R-S3/R-EXT (4-cut) define M'(d) on all of dom(M(d)) via partitioning into subspace-S affected/exterior ranges (plus R-XS for other subspaces). The tiling argument — that the clause ranges [c₀, c₀+w_β), [c₀+w_β, c₀+w_β+w_μ), [c₀+w_β+w_μ, c₃) cover [c₀, c₃) without overlap — is verified by width arithmetic (w_β + w_μ + w_α = w_α + w_μ + w_β).

**Permutation proofs correct.** R-PPERM and R-SPERM define explicit bijections π, verified against the postconditions clause by clause. Injectivity holds within each case (distinct j → distinct image) and across cases (image sets are the disjoint partition established by R-PIV/R-SWP). Surjectivity follows from the image sets covering dom(M'(d)) = dom(M(d)).

**Content preservation (R-CP).** Multiset equality ran(M'(d)) = ran(M(d)) follows from π being a bijection with M'(d)(π(v)) = M(d)(v). The multiplicity argument (|{v : M'(d)(v) = a}| = |{π(u) : M(d)(u) = a}| = |{u : M(d)(u) = a}|) is correct.

**Frame conditions (R-CF).** C' = C, E' = E by K.μ~ not touching these components. R' = R by J3 (ReorderingIsolation). Coupling constraints J0, J1, J1' vacuously satisfied: J0 vacuous because dom(C') \ dom(C) = ∅; J1 vacuous because ran(M'(d)) \ ran(M(d)) = ∅ by R-CP; J1' vacuous because R' \ R = ∅.

**Invariant preservation.** S2 (functionality) by R-PIV/R-SWP establishing totality. S3 (referential integrity) by ran(M'(d)) = ran(M(d)) ⊆ dom(C) = dom(C'). S8a, S8-depth, S8-fin by dom(M'(d)) = dom(M(d)). D-CTG by V_S'(d) = V_S(d) as sets. K.μ~ preconditions verified in R-KMU.

**R-BLK commutativity.** The claim π(vⱼ + k) = π(vⱼ) + k holds because at depth 2, the displacement is uniform within each region and ordinal increment is natural number addition (associative and commutative). Verified explicitly for α, β, μ, and exterior.

**Worked examples verified.** Both the 3-cut pivot (5-position document, mixed origins) and the 4-cut swap (8-position document, w_α ≠ w_β) confirmed: postconditions match position-by-position computation, permutations satisfy M'(d)(π(v)) = M(d)(v), displacements sum to zero, and block decompositions are correct including the merge of B+C+H in the 4-cut example.

**Displacement analysis consistent.** Total displacement zero in both cases: w_α·(w_β) + w_β·(−w_α) = 0 for 3-cut; w_α·(w_β+w_μ) + w_μ·(w_β−w_α) + w_β·(−(w_α+w_μ)) = 0 for 4-cut.

**R-PRE(v) redundancy noted but acceptable.** CS2 (strict ordering of cuts) at depth 2 already implies w_α ≥ 1 and w_β ≥ 1, so R-PRE(v) is derivable. Stating it explicitly is a defensible clarity choice.

## OUT_OF_SCOPE

None.

VERDICT: REVISE
