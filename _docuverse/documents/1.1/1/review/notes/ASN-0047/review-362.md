# Review of ASN-0047

The transition model is technically sound on the points I checked hardest: the K.δ case-(ii) freshness discharge (FrontierEquivalence / ChildSpawnFreshness via P1 + SSGU), the K.μ~ admissibility decomposition (Steps A/B, K.μ~-FIX, K.μ~-RANGE), the fork φ-bijection (order + multiplicity, verified against the duplicate-source and depth-rebasing examples), and the cross-layer inductions (P6–P8, P4★/P4a/P7a) all hold up under boundary cases I traced. My findings are confined to the meta-prose accretion the `review-mode.anti-bloat` classifier flags.

## REVISE

### Issue 1: Foundation axiom restated verbatim in the body
**ASN-0047, §The state model and Properties Introduced (Inherited table)**: SequentialTransitionAxiom is given a full in-body restatement ("The transition relation Σ → Σ' is single-event sequential: each transition is an atomic, uninterruptible event…") while the inherited-foundation table separately carries it with the pointer "full statement in §The state model."
**Problem**: ASN-0093 is a foundation ASN; foundation axioms may be referenced without restating. The full body restatement plus a table pointer that redirects *back* to that restatement is exactly the "explains the axiom rather than referencing it" accretion pattern. The double presence (body + table) advances no reasoning.
**Required**: Reference ASN-0093 for SequentialTransitionAxiom and reduce the body occurrence to a one-line pointer (the `Σ → Σ'` / `Σ →* Σ'` notation note is the only locally novel content and can stand alone).

### Issue 2: Justificatory necessity-prose in the K.μ~ admissibility definition
**ASN-0047, §Decomposition of K.μ~, "The conjuncts are mutually independent"**: A paragraph constructs a link-position transposition (to show clause (v) is independently load-bearing) and a content/link transposition at a coinciding depth (to show clause (iv) is independently load-bearing), each "yet it fails admissibility on clause (X) alone."
**Problem**: This is the flagged pattern "new prose explains why [each clause] is needed rather than what it says" — it imagines cases that admissibility already excludes, purely to argue the conjunct set is non-redundant. The two transpositions are concrete (so not meta-prose per se), but the surrounding necessity-of-each-clause framing is essay content sitting inside a definition. Clauses (iv)/(v) are already used at their points of consumption (Step (A), the S3★ discharge); their necessity does not require a standalone demonstration here.
**Required**: Drop the independence-of-conjuncts paragraph, or relocate the two example transpositions to the worked-examples material as illustrations rather than as a necessity argument embedded in the admissibility definition.

### Issue 3: Reinvented order notation for a foundation relation
**ASN-0047, §Amendments to existing transitions, "V-ordering on subspace S (definition)"**: "The V-ordering on subspace S is the restriction of T1 (LexicographicOrder, ASN-0034) to the depth-m_S positive-component tuples whose first component is S — equivalently, the standard lexicographic order…"
**Problem**: This names a new relation for what is, by the definition's own admission, T1 restricted to a slice. Per standard 7, an ASN should use the foundation relation rather than coin notation for it. The named "V-ordering" then recurs in D-CTG★, D-MIN★, and D-SEQ★ as if it were a distinct order, adding a layer the reader must unwind back to "T1 restricted to v₁ = S."
**Required**: State D-CTG★/D-MIN★/D-SEQ★ directly in terms of T1 on the fixed-depth, fixed-subspace slice, or demote "V-ordering on subspace S" to an inline abbreviation introduced at first use rather than a standalone definition propagated through three invariants.

## OUT_OF_SCOPE

### Topic 1: Interior link-arrangement contraction with renumbering
**Why out of scope**: Open Question 8 (renumbering-aware contraction modelling the implementation's interior `DELETEVSPAN`) is genuinely future territory — the present K.μ⁻ models suffix removal only, and interior compaction is a distinct operation. This belongs in a successor ASN, not a revision here.

### Topic 2: Link-subspace reordering
**Why out of scope**: K.μ~ clause (v) fixes the link subspace pointwise, so reordering links within a document is unmodeled. Whether a link-reordering primitive is warranted is a new-operation design question, not a defect in this ASN's stated scope.

VERDICT: REVISE
