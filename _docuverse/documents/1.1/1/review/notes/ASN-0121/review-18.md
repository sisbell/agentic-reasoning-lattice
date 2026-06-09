# Review of ASN-0121

## REVISE

### Issue 1: Element-rooted home-set vacuity claim is false for wide spans
**ASN-0121, "What is being matched"**: "(An element-rooted `H` is admissible and simply vacuous: its coverage contains no document-level `home(a)`, so `athome` is uniformly `false` — the operation is total over the declared request type, with no ill-formed inputs to exclude.)"

**Problem**: The ASN explicitly admits *wide* spans for `H` ("A wider span `(p, ℓ)` rooted at the same `p` is equally admissible … its coverage is then the order-convex *range* `{t : p ≤ t < p ⊕ ℓ}`"). The vacuity argument only holds for the unit-depth **subtree** reading. For a wide span rooted at an element-level address, the coverage is a T1-range that *can* contain document-level tumblers. Concrete counterexample: let `p = [1,0,1,0,1,0,1,1]` (element-level, `zeros = 3`) and `ℓ = [0,0,0,0,1,1,1,1]` (action point 5 ≤ #p = 8, `Pos`, so T12-well-formed). Then `p ⊕ ℓ = [1,0,1,0,2,1,1,1]`, and the document tumbler `q = [1,0,1,0,2]` (`zeros = 2`) satisfies `p < q` (divergence at position 5: `1 < 2`) and `q < p ⊕ ℓ` (proper prefix, T1 case (ii)), so `q ∈ coverage((p, ℓ))`. If some link has `home(a) = q`, then `athome(a, H) = true` — not "uniformly false." The blanket claim conflates "element-rooted prefix span" with "element-rooted span," contradicting the wide-span admissibility the ASN states two sentences earlier.

**Required**: Restrict the vacuity claim to unit-depth (subtree) element-rooted spans, or drop it. The totality conclusion ("no ill-formed inputs to exclude") survives without it, since `athome` is well-defined as coverage membership regardless.

### Issue 2: FL-WP(b) increment formula over-attributed to R6b and mis-indexed
**ASN-0121, FL-WP(b) derivation**: "`nullified(Σ') = nullified(Σ) ∪ {t ∈ dom(Σ.L) : t ∈ coverage(G')}` (R6b)"

**Problem**: R6b (SingleDepthRetraction, ASN-0086) is a one-directional membership characterization at a single state (`… ∧ a ∈ coverage(G') ⟹ a ∈ nullified(Σ)`), not the across-transition set equality cited here. The equality additionally requires that the committed tuple is the *only* addition to `L_R` (`L_R^{Σ'} = L_R^Σ ∪ {(b,F',G')}`) to close the `⊆` direction. Separately, the index set should be `dom(Σ'.L)`, not `dom(Σ.L)`: the fresh retractor address `b ∈ dom(Σ'.L) \ dom(Σ.L)` could itself lie in `coverage(G')` (self-retraction), in which case the displayed formula undercounts. The conclusion drawn for *existing* `a ∈ dom(Σ.L)` is unaffected, but the formula as written is not exact and its single-citation derivation is compressed.

**Required**: Either state the increment formula over `dom(Σ'.L)` with the premise `L_R^{Σ'} = L_R^Σ ∪ {(b,F',G')}` named alongside R6b, or restrict the formula explicitly to the existing-link slice `dom(Σ.L)` it is actually used on and note the self-retraction case is excluded by scope.

## OUT_OF_SCOPE

### Topic 1: Visibility of retraction-tuple links in query results
**Why out of scope**: `addressable(Σ) = dom(Σ.L) \ nullified(Σ)` includes the retraction tuples of `L_R^Σ` themselves (a retractor `b` is not generally nullified), so a matching `q` — including the all-wildcard request — returns them. Whether the spec should filter retraction-mechanism links from ordinary `findlinks` results is a design question not settled by Nelson's text here; the retraction *mechanism* is ASN-0086's concern. This is a candidate refinement, not an error in the present matching rule.

VERDICT: REVISE
