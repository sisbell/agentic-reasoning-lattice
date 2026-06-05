# Review of ASN-0100

This is a thorough, mathematically careful specification. The three-effect decomposition (allocate / place / shift) is sound, the substrate composite is correctly typed under ValidComposite★, every invariant conjunct is touched, and the boundary cases (j=0, j=N append, empty-document first insertion) are each verified rather than waved through. The S4/S2 disjointness argument, the SubsequentEmissionFreshness chaining across intermediate states, and the per-state vs. composite-boundary invariant split are all handled correctly. I found no skipped proofs or missing edge cases in the core mathematics.

The findings below are redundancy/clarity issues, which the note's anti-bloat classifier asks to be surfaced.

## REVISE

### Issue 1: Position Constraints section restates already-established precondition material

**ASN-0100, §Position Constraints**: "For non-empty `V_{s_C}(d)` with cardinality `N`, the `N + 1` valid positions correspond to … `j = 0`: insertion at the very beginning … `j = N`: insertion at the end (append) … The non-empty case's depth parameter is fixed by S8-depth … For empty `V_{s_C}(d)`, the unique valid position is `[s_C, 1, …, 1]` of depth `m := #p ≥ 2`. … The precondition is the *ternary* predicate … K.μ⁻ is omitted from the composite …"

**Problem**: This section re-derives, in different words, content already fixed in three earlier places: the empty/non-empty predicate distinction and `m := #p` binding (§The Operation's Inputs and the **State Preconditions** bullet of §Formal Contract), and the K.μ⁻-omission for the empty case ((INS.μ⁻-fires) in the Substrate Decomposition). This is the "two paragraphs in the same document say the same thing in different words" pattern. The only genuinely new content is the mapping of `j ∈ {0, N, interior}` to Left/Shifted-right emptiness.

**Required**: Trim to the new content (the region-emptiness mapping across `j`), and cite the precondition predicates rather than restating their operational character a second time.

### Issue 2: INS.proj is deferred to from multiple sections to the same downstream location

**ASN-0100, §Cross-document independence and §A Worked Example**: "This is the `d' ≠ d` branch of INS.proj (§Coverage and link discoverability), derived there." / "Projection-shift correspondence — numeric instantiation of INS.proj."

**Problem**: The cross-document projection invariance is stated in the frame conditions (INS.frame.doc), re-asserted in §Cross-document independence with a forward deferral to §Coverage, instantiated numerically in the worked example, and finally derived in §Coverage. This is the "multiple paragraphs in different sections defer to the same downstream location" pattern. A reader following the cross-document claim must skip forward to §Coverage to find the actual argument.

**Required**: State the `d' ≠ d` branch once, where it is derived (it is a one-line LP4 composition); replace the upstream deferrals with the bare result so each site is self-contained.

### Issue 3: ActivatedEmission preservation is stated twice in the same breath

**ASN-0100, §Atomicity, entity-set invariants bullet**: "Each invariant is a predicate over E … and so holds at every intermediate by inheritance from the pre-state. ActivatedEmission in particular is preserved by the frame `E' = E` (INS.frame.E): INSERT fires no K.δ, so no new entity enters E, and the pre-state witness … survives unchanged for every `e ∈ E`."

**Problem**: The group sentence already discharges all four entity-set invariants (P8, NodeLineage, ActivatedEmission, M0) by the `E' = E` frame. The trailing "ActivatedEmission in particular…" sentence repeats the identical argument (no K.δ → no new entity → pre-state witness survives) for one member of the group with no added content.

**Required**: Drop the redundant restatement, or if ActivatedEmission's witness structure warrants singling out, replace the repetition with the one fact that distinguishes it.

## OUT_OF_SCOPE

(none — the bounded scope statements at §Bounding the Scope and the Open Questions correctly defer DELETE/COPY/REARRANGE, link-subspace insertion, version derivation, concurrency, and replication.)

VERDICT: REVISE
