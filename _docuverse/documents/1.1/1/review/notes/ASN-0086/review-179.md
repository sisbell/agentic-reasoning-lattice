# Review of ASN-0086

## REVISE

### Issue 1: CoverageEqualityDecidable proof omits the empty-endset boundary

**ASN-0086, Lemma — CoverageEqualityDecidable**: "For any two endsets `e, e' ∈ Endset`, the predicate `coverage(e) = coverage(e')` is decidable... Let `P = {...} ∪ {...}`, a finite endpoint set; sort it under T1 via T2... into the distinct values `c₁ < … < c_m`... Both coverages lie within `[c₁, c_m)`..."

**Problem**: The lemma is stated for *any* `e, e' ∈ Endset`, and ASN-0043 explicitly admits the empty endset (`∅ ∈ Endset`). When `e = e' = ∅`, `P = ∅` and `m = 0`: there are no cells, and the references to `[c₁, c_m)`, the cell partition `{c₁}, (c₁,c₂), …`, and the "exterior cells" are undefined. The result (trivially equal, both coverages `∅`) is correct, but the proof's machinery does not reach it. This is the named "empty" boundary the review standard requires. (Any *non-empty* endset has `m ≥ 2`, since a span `(s, ℓ)` with `ℓ > 0` contributes distinct endpoints `s < s ⊕ ℓ` by TA-strict; so `m = 0` is the only uncovered case, but it is reachable.)

**Required**: Either dispatch `m = 0` (both coverages empty, equal) as a base case before the cell construction, or restrict the lemma's stated domain to the inputs it is actually applied to (`T_admissible`, where coverage is always non-empty and `m ≥ 2`).

### Issue 2: Retraction-stability consequences for conforming `↝`-steps not derived

**ASN-0086, R6a/R6c**: "`(A Σ → Σ', a : a ∈ nullified(Σ) :: a ∈ nullified(Σ'))`" and R6c "`(A Σ' : Σ →* Σ' :: (a, F, G) ∉ A_K^{Σ'})`".

**Problem**: R6a and R6c are proved only against `→` (and `→*`), via R3 and R2 (= L12/L12a), which themselves hold only across `→`. But the substrate's operational evolution is `↝`, and the note builds substantial machinery (R7a, *Definition — substrate-conforming layer*, K-Step Conformance Preservation) precisely to relate conforming `↝`-steps to `→`. The natural derived guarantee — that retraction stability holds across the `↝`-steps of any substrate-conforming layer (clause (a) preserves L12/L12a, so R6a's proof transfers verbatim; or via R7a, since `nullified` is a pure function of `Σ.L`) — is never stated. As written, a reader cannot tell whether a higher layer's conforming operation can un-nullify a tuple, even though the apparatus to answer it is present. This is a postcondition whose consequence is left unexplored.

**Required**: State and prove (it is a one-line corollary of R7a or of clause (a) + R6a) that retraction stability and R6c extend to `↝`-steps issued by a substrate-conforming layer; or make explicit that R6a/R6c are deliberately scoped to `→` and that no `↝`-level guarantee is claimed.

### Issue 3 (anti-bloat): The "arity-independence / non-gating arity" point is restated across four sites

**ASN-0086, Definition — Nullify / R-Scope / wp Case 1**: e.g. Definition — Nullify: "single-tuple scope holds regardless of it (R-Scope, arity-independent)"; R-Scope statement: "The result is *arity-independent*"; R-Scope proof: "the conclusion is arity-independent — it holds equally when `a` is a higher-arity address"; wp Case 1: "The scope condition P2 (`|Σ.L(a)| = 3`) is consequently absent from the wp: single-tuple scope is arity-independent, as established in R-Scope."

**Problem**: The same claim — that `|Σ.L(a)| = 3` is not load-bearing for single-tuple scope — is asserted in four places, and within *Definition — Nullify* it is explained twice (the gating-conditions paragraph and the trailing "arity-3 scope remark" paragraph). This is the "two paragraphs say the same thing in different words" / forward-reference-accretion pattern the classifier targets: R-Scope's `arity-independent` postcondition is the single load-bearing statement, and the other sites should cite it without re-arguing it.

**Required**: Prove and label arity-independence once (in R-Scope). Reduce the Definition — Nullify and wp Case 1 mentions to a bare citation, and delete the duplicate explanation inside Definition — Nullify.

## OUT_OF_SCOPE

### Topic 1: Higher-arity active subsets
The note restricts `L_K` and `A_K` to standard-triple (`|Σ.L(a)| = 3`) links and acknowledges higher-arity links exist in `dom(Σ.L)` without a typed-relation home. The construction of higher-arity typed relations `L_K^{(n)}` is correctly deferred (it appears in Open Questions); this is new territory, not a defect in the present development.

VERDICT: REVISE
