# Review of ASN-0091

The technical core is sound: I checked all four worked examples (3-cut pivot, 4-cut swap, interior cuts, shared-address non-uniqueness) against R-P1/R-P2/R-S1–S3 and they compute correctly; the empty-case exclusion via R-PRE(iv)+CS2 holds (c₀ ∈ V_S(d) is forced); the ChainDisjointAdjacency inline lemma is valid; the net-effect split correctly routes collapse vs. non-trivial cases; and the d/d_tgt distinction in RE-trans is handled precisely. No cross-ASN-reference violations (all references are to foundations). The findings below are precision and accreted-prose issues, consistent with the anti-bloat classifier.

## REVISE

### Issue 1: Clause (v) discharge cites the wrong mechanism
**ASN-0091, "Clause Correspondences and Per-Invariant Discharges," admissibility table row (v)**: "(v) link-subspace fixing π(v) = v on the link subspace | RE-sub: by CS3 the cut subspace is S = s_C, so R-FRAME-P/S(a) fixes every subspace(v) = s_L V-position pointwise"
**Problem**: Clause (v) is a statement about the bijection — `π(v) = v`. R-FRAME-P/S(a) asserts `Σ'.M(d)(v) = Σ.M(d)(v)` (arrangement preservation), which does not entail `π(v) = v`. The π-fixity comes from R-PPERM/R-SPERM's non-S branch — exactly as the RE-sub row of the Claims table correctly records ("π-fixity from R-PPERM/R-SPERM non-S branch; arrangement preservation from R-FRAME-P/S(a)"). The explanatory clause picks the arrangement source to discharge a π-level obligation.
**Required**: Cite R-PPERM/R-SPERM's non-S branch (the source of `π(v) = v`) for clause (v), not R-FRAME-P/S(a).

### Issue 2: Triplicated construction of the shared-I-address distinction
**ASN-0091, "Clause Correspondences," Net-effect split paragraph**: the inline concrete witness `{[1, 1] ↦ a, [1, 2] ↦ b, [1, 3] ↦ a, [1, 4] ↦ b}` with cuts `([1,1],[1,3],[1,5])`.
**Problem**: The same shared-address phenomenon (π ≠ id while M'(d) = M(d)) is constructed three times: here as an inline example, again in the "collapse case" sentence of the realiser paragraph, and a fourth/fifth time in the dedicated "Bijection Non-Uniqueness Under Shared I-Addresses" worked example. A concrete value-level witness embedded in a clause-discharge slot is essay content relocated into a structural slot — the reviser-drift pattern. The split itself (which realiser per case) is what this slot needs; the witness belongs in the dedicated example.
**Required**: State the net-effect split abstractly in the discharge slot; keep one concrete witness, in the dedicated worked example.

### Issue 3: Document-ordering / non-circularity justification prose
**ASN-0091, "Domain Stability and Range Invariance" parenthetical**: "(For REARRANGE_K specifically, this equality is asserted directly as the domain clause of ASN-0084's PivotPostcondition/SwapPostcondition, independent of K.μ~-FIX and D-SEQ★.)"
**Problem**: This justifies *which* foundation clause is cited and that the route does not depend on K.μ~-FIX/D-SEQ★ — derivation-route bookkeeping ("non-circular by Y"), not advancement of RE-dom. The reader following RE-dom does not need to be told which alternative derivations were avoided.
**Required**: Drop the route-justification; cite the source clause without the independence apologetics.

### Issue 4: Reachability argument deferred and back-referenced across paragraphs
**ASN-0091, "Per-Invariant Discharges" (RA-adm paragraph) and following reachability paragraph**: "Σ' is reachable (established below), so RA-adm holds." … later: "the one-step discharge above establishes RA-adm for the REARRANGE_K realiser."
**Problem**: RA-adm defers downstream ("established below"), and the reachability paragraph reaches back ("the one-step discharge above"). The reader must bounce between the two to assemble a single argument. This is the "multiple paragraphs defer to the same downstream location" pattern.
**Required**: Consolidate the reachability establishment and the RA-adm conclusion into one location so the argument reads forward once.

## OUT_OF_SCOPE

### Topic 1: Joint reconstitution of a same-source span split across two fragments
The ASN explicitly declines this ("Whether the two fragments *jointly reconstitute* the original source span … is not established here") and routes it to the Open Questions. This is correctly deferred — it concerns a reconstitution guarantee not derivable from RE-frag/RE-origin alone, and belongs in a future ASN.

### Topic 2: Link-subspace rearrangement semantics
RE-sub fixes the link subspace pointwise under content-subspace cuts; an operation that *reorders* the link subspace is correctly listed as an Open Question, not an omission here.

VERDICT: REVISE
