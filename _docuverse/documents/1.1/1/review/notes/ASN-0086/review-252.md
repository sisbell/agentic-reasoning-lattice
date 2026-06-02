# Review of ASN-0086

I checked every proof (R0, R0a, R1–R6c, R-Scope), the two wp cases, and the worked sketch. The core is sound: R0a's antichain split (cross-home zero-counting, same-home equal-length) is exhaustive and correct; R-Scope handles both P-tgt branches (P1 and self-emit) including the fresh-key case via R0a-at-Σ'; the worked-sketch tumbler arithmetic checks out (a₁…a₃ on `A_L(d)`); coverage half-open intervals match PrefixSpanCoverage; all cross-ASN references are to foundations (0034/0036/0040/0043/0093). The findings below are clarity/bloat, not correctness.

## REVISE

### Issue 1: ActiveSubset computability paragraph re-derives a lemma already proven
**ASN-0086, Definition — ActiveSubset**: "This test has two decidable layers: selecting the slice member `(b, F', G') ∈ L_R^Σ` requires deciding `coverage(Σ.L(b).e₃) = coverage(R)` for each `b ∈ dom(Σ.L)`, decidable by Lemma CoverageEqualityDecidable **exactly as for the `L_K^Σ` selection above**..."

**Problem**: The phrase "exactly as for the `L_K^Σ` selection above" is a self-flagged duplication. CoverageEqualityDecidable already establishes the decision procedure; restating its two-layer application inside a definition slot is the use-site re-explanation pattern. A reader following the definition of `A_K` must skip past a proof gloss to reach "`A_K^Σ` is then the finite slice `L_K^Σ` with `nullified(Σ)` excluded."

**Required**: Collapse to one line — "`A_K^Σ` is a finite, computable set: `L_K^Σ` is selected by CoverageEqualityDecidable, `nullified(Σ)` by CoverageEqualityDecidable and T2 span-membership, and `A_K^Σ = L_K^Σ \ nullified(Σ)`."

### Issue 2: Domain co-extensiveness stated twice in different words
**ASN-0086, R-Scope statement**: "The domain is co-extensive with the operation: every legal `Nullify` call (one satisfying P0 ∧ P-tgt) falls under the lemma."
**ASN-0086, WP Case 1**: "...the weakest precondition `P0 ∧ (P1 ∨ a = a_emit)` *coincides* with the operation's own precondition `P0 ∧ P-tgt`: every legal Nullify call attains single-tuple scope, and no legal call fails to."

**Problem**: Both passages assert the same fact — the lemma/wp domain equals Nullify's precondition. The "two paragraphs saying the same thing in different words" pattern. The R-Scope statement should state the formal claim and its hypotheses only; the co-extensiveness observation belongs once, in the wp where it is actually derived.

**Required**: Drop the "domain is co-extensive" sentence from the R-Scope statement (keep the arity-independence note, which the proof earns); retain the single statement in WP Case 1.

## OUT_OF_SCOPE

### Topic 1: Concurrency/atomicity model for Emit vs. Observe
**Why out of scope**: ASN-0093's SequentialAtomicTransitions gives serial atomicity; a consistency model for concurrent Observe against in-flight `A_K` transitions is new territory (the note's own open question), not a defect here.

### Topic 2: Ordering guarantees on Observe results, multi-arity typed relations `L_K^(n)`, and cardinality bounds on `nullified(Σ)`
**Why out of scope**: These are the note's stated open questions; each defines new state/operation structure beyond the standard-triple relational layer and belongs in a successor ASN.

### Topic 3: Cross-layer type-address collision under dynamic `T_admissible`
**Why out of scope**: Coordination semantics for independently-chosen ghost type addresses (L9) is a higher-layer protocol concern, not an invariant this substrate-adjacent note must establish.

VERDICT: REVISE
