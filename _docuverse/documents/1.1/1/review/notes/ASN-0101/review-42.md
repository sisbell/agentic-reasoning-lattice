# Review of ASN-0101

The formal content is sound. I checked D0's precondition reduction, D1's gap-closure bijection, the D8 invariant-preservation cases (including the S8★(c) split between content and link subspaces via M12 vs. D6), the D9 projection characterisation, and the D11 weakest-precondition derivations (including the partial-command negation equivalence and the four discoverability/cardinality wps) against the three worked examples — the arithmetic and case analysis hold throughout. Boundary cases (empty post-state, start/end/interior deletion, singleton subspace) are covered uniformly. My findings are confined to the bloat patterns the `review-mode.anti-bloat` classifier directs me to surface.

## REVISE

### Issue 1: Redundant double-deferral to D10 in "The operation"
**ASN-0101, "The operation"**: "The vacuity at the one-step level does not extend automatically to multi-step composites containing both DEL and allocation-or-placement steps; D10 below records the precise statement and its scope. The formal extension of ValidComposite★ to admit DEL is recorded there."
**Problem**: Two adjacent sentences defer to the same downstream location (D10). The second sentence ("The formal extension … is recorded there") adds nothing the first sentence's deferral did not already carry. Moreover this whole paragraph previews the J0/J1★/J1'★ vacuity argument that D10 then states in full — pre-statement plus double pointer is exactly the forward-reference accretion the classifier flags.
**Required**: Collapse to a single deferral, or state the vacuity once (here or in D10) and have the other site merely name it. Drop the redundant second sentence.

### Issue 2: D8 Group (ii) per-invariant rationale duplicates the uniform frame observation
**ASN-0101, D8 Group (ii) and "Justification (Groups (ii) and (iii))"**: the Group (ii) catalogue attaches an individualized "*X* predicates over [component(s)], preserved by [frame fact]" clause to roughly twenty-five invariants (M0, C1, C1b, C1c, C2, S7a, S7b, S7d, S4, L0, L1, L1a–c, L3, L12, SD, L-fin, C-fin, NodeLineage, ActivatedEmission, plus eight chain-discipline lemmas), then the justification states the single principle that subsumes every one of them: "every invariant in these groups is either (a) a predicate over `(C, L, E, R, dom(M))` … pointwise preserved by D0's frame; or (b) a transition predicate … reduces to the equality case."
**Problem**: The per-item rationale clauses are twenty-five restatements of one uniform fact. Once the uniform observation is stated, each bullet's "predicates over … preserved by …" gloss advances no reasoning — it is a use-site inventory the precise reader must skim past. The list of *names* establishes completeness; the repeated per-name justification is noise.
**Required**: Keep the enumeration of invariant names (completeness has value) but discharge them collectively through the uniform observation, removing the individualized rationale clause from each bullet. Retain individualized argument only where an invariant does *not* fall under the uniform principle (there appear to be none in Group (ii)).

### Issue 3: Claims-Introduced table rows carry justification-level prose
**ASN-0101, "Claims Introduced" table, rows D8 and D10**: the D8 cell enumerates the full Group (i)/(ii)/(iii) invariant breakdown with discharge mechanisms; the D10 cell embeds the entire LP-family extension catalogue ("LP2★, LP3★, LP13 extend to DEL via D3; LP4, LP5 via D5; LP6, LP7, LP8, LP14, LP9, LP10, LP11 are vocabulary-disjoint … LP12a, LP12b are supplanted … LP-Sub … LP-Fin …").
**Problem**: A summary table should state each claim tersely. These two cells reproduce paragraph-length content already present in the body (D8's three-group justification; the "LP-family extension under DELETE" paragraph), so the table duplicates rather than summarizes. The D10 cell's per-lemma LP inventory is the use-site-inventory pattern relocated into a table slot.
**Required**: Reduce the D8 and D10 rows to one-line statements of the guarantee, leaving the per-invariant and per-lemma detail to the body sections that already carry it.

## OUT_OF_SCOPE

### Topic 1: Full historical reconstruction of arbitrary prior states
The recoverability section correctly scopes this to a versioning mechanism (J4 ForkComposite) outside DEL, and the Open Questions defer it. No revision needed — flagging only to confirm the boundary is drawn appropriately, not as an error.

VERDICT: REVISE
