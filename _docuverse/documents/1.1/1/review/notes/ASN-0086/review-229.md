# Review of ASN-0086

## REVISE

### Issue 1: CoverageEqualityDecidable dismisses empty gaps without establishing indicator/set agreement
**ASN-0086, Lemma CoverageEqualityDecidable**: "Empty gaps need no special handling: an empty gap is `∅` in both coverages, so it contributes matching indicator entries automatically and never forces a spurious difference or a spurious match."

**Problem**: The decision procedure compares *structural indicator vectors* computed cell-by-cell, where each gap-cell indicator is "a finite disjunction over the spans of `e`, each disjunct a finite conjunction of T2 comparisons" — i.e., computed from endpoints, not from any interior tumbler. Empty gaps demonstrably exist in tumbler space (e.g., nothing lies strictly between `[2]` and `[2,0]` under T1). The leap from "is `∅` in both coverages" (a fact about the *sets*) to "contributes matching indicator entries automatically" (a claim about the *structural computation*) is exactly the step that needs proof: nothing shown forbids the endpoint-based disjunction from evaluating "in" for `e` and "out" for `e'` on an empty gap, which would report a spurious inequality despite both contributing `∅`. The procedure never detects emptiness.

**Required**: Either (a) restrict the comparison to cells that contain a representative tumbler (point-cells `{c_k}` plus provably-nonempty gaps), discharging the side-decidability "is there a tumbler strictly between `c_k` and `c_{k+1}`"; or (b) prove that the endpoint-based gap indicator coincides with actual set-membership of the gap region, so empty gaps cannot diverge. The one-sentence dismissal is a skip in a load-bearing lemma (TypeEquivalence `~`, `L_K` slicing, and `A_K` computability all rest on it).

### Issue 2: "Scope — retractors are standard-triple links only" re-derives an exclusion already forced by the carrier
**ASN-0086, Definition — Nullified, *Scope* sub-paragraph**: "A retractor must therefore be a standard-triple link; a higher-arity link (`|Σ.L(b)| > 3`) whose slot-3 coverage equals `coverage(R)` and whose slot-2 covers a target address has *no* nullifying effect. … For `N > 3` links the model fixes no canonical to-slot, so `coverage(G')` is undefined for them and they cannot serve as retractors within this layer."

**Problem**: The witnessing tuple `(b, F', G')` ranges over `L_R^Σ`, whose *Definition — TypedRelation* already carries the `|Σ.L(a)| = 3` conjunct. Higher-arity links are excluded by the carrier before this paragraph begins; the paragraph then spends four sentences imagining and refuting the `N>3` case the quantifier never admits. This is the flagged forward-reference-accretion pattern (a paragraph imagining a case the claim's carrier already excludes). The single clause "the existential ranges over `L_R^Σ`, which is triple-restricted" suffices.

**Required**: Cut the sub-paragraph to one clause noting the existential ranges over the triple-restricted `L_R^Σ`, or drop it entirely.

### Issue 3: The self-nullification boundary in WP Case 2 is stated three times before the worked example
**ASN-0086, Weakest-Precondition Analysis, Case 2**: the *Result* note ("The second conjunct is a *disjunction* … captures exactly the self-nullification boundary: the fresh emission self-nullifies precisely when …"), the standalone "*The disjunction is load-bearing.*" paragraph, and the *Derivation* each restate that `a ∈ nullified(Σ') ⟺ (K ~ R ∧ a_emit(Σ, d) ∈ coverage(G))`.

**Problem**: The *Result* note and the *load-bearing* paragraph say the same thing in different words (the disjunction is the negation of the self-nullification conjunction; the escape branch is required for weakestness). The *Derivation* proves it and the worked Step 4 instantiates it — those carry the weight. The two prose restatements ahead of the derivation are redundant meta-prose around the same claim.

**Required**: Keep the derivation (which proves the biconditional) and the worked instance; collapse the *Result* note and the *load-bearing* paragraph into a single sentence stating the disjunct is non-redundant, with the realizing witness (`K ~ R`, `G = ∅`) cited once.

## OUT_OF_SCOPE

### Topic 1: Whether the unit-depth retraction discipline should be a substrate K-operation
The note flags this itself in Open Questions. Introducing a designated retraction K-operation with a shape constraint is new substrate territory (ASN-0093 layer), not a defect here. The note's treatment of it as a layer convention — with the wp domain-restriction made explicit and the load-bearingness argued — is internally honest.

### Topic 2: Higher-arity typed relations `L_K^{(n)} ⊆ A_rel × ℘(A)^n`
The standard-triple restriction is a deliberate scoping choice; the `N > 3` relational structure is a future ASN, not a gap in this one.

VERDICT: REVISE
