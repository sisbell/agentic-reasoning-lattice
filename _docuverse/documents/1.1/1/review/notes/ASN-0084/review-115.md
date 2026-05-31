# Review of ASN-0084

I performed a full correctness pass (every postcondition, every region/well-definedness case, the boundary configurations exercised by the six worked examples) and a separate anti-bloat pass per the `review-mode.anti-bloat` classifier. The mathematics is sound: because REARRANGE permutes the *mapping* M(d) over a *fixed* domain (`dom(M'(d)) = dom(M(d))`), every domain-shape invariant (D-CTG, D-MIN, D-SEQ, S8-fin, S8a, S8-depth) is preserved automatically, and the two invariants that need real work — S2 (functionality, via R-PIV/R-SWP) and S3 (referential integrity, via R-RI) — are discharged correctly. Well-definedness, the π bijections, R-COMM, R-BLK, and R-CANON all hold; the boundary edges (empty exteriors, minimum widths, all three μ-displacement sub-cases, non-S pass-through) are concretely verified. The findings below are confined to accreted prose.

## REVISE

### Issue 1: Foundation formula restated inline rather than cited
**ASN-0084, "Correspondence-Run Decomposition Transformation," I-address `+` preamble**: "...applied to a deeper tumbler (valid at any depth, OrdinalShift, ASN-0034: `shift(v, n) = v ⊕ δ(n, #v) ∈ T` with `shift(v, n)ᵢ = vᵢ` for `i < #v` and `shift(v, n)_{#v} = v_{#v} + n`)."
**Problem**: This restates OrdinalShift's full component definition from the foundation. The only content the preamble actually needs to add is that S8's `+` denotes a last-component shift applied at I-address depth (zeros = 3, S7b) — the foundation already supplies the formula by reference. Restating it is length without advancement.
**Required**: Reduce to the citation plus the one new fact ("`+` on I-addresses is `shift(a_s, k)`, valid at the I-address's depth per OrdinalShift, ASN-0034"); drop the inlined component equations.

### Issue 2: Orientation/essay prose in a structural slot
**ASN-0084, after the ArrangementRearrangement definition and R-RI**: "Any bijection qualifies; a rearrangement determined by cut points is one where the regions to exchange are identified by a tuple of cut positions. The properties in this ASN characterize this specific class of permutations."
**Problem**: This restates the ASN's thesis without advancing any claim — it sits between the rearrangement machinery and the cut-sequence definition as connective essay. A reader following the derivation skips past it.
**Required**: Delete, or fold the single load-bearing clause (cut-point rearrangements are the bijections induced by a cut tuple) into the CutSequence definition where it is actually used.

## OUT_OF_SCOPE

### Topic 1: k-cut rearrangements for k > 4
**Why out of scope**: The ASN is explicitly the 3-cut/4-cut class (CS1). Generalizing the permutation family is new territory, correctly left to the Open Questions.

### Topic 2: Composition of multiple rearrangements
**Why out of scope**: Whether two REARRANGEs compose to a single one is a property of sequences of operations, not of the single operation specified here.

### Topic 3: Weakest precondition for the post-state invariant suite
**Why out of scope**: The operation is fully specified with pre/postconditions and its invariant audit is complete; a wp characterization is a distinct analysis, appropriately deferred to the Open Questions.

VERDICT: REVISE
