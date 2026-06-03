# Review of ASN-0070

## REVISE

### Issue 1: M-int cited with a precondition it does not supply

**ASN-0070, "Computation via Decomposition"**: "By M-int (TumblerIntervalCharacterization, ASN-0058), whose subspace-agreement postcondition gives `subspace(y) = subspace(v)` for every `y` with `v ≤ y < v + n`, every V-position of β shares the V-subspace of `v`, so each block lives in exactly one V-subspace."

**Problem**: M-int (ASN-0058) requires *both* operands in `dom(M(d))`: "Let `x, y ∈ dom(M(d))` and `n ≥ 1`. If `x ≤ y < x + n`, then ... `subspace(y) = subspace(x)`." The note applies its subspace-agreement clause to "every `y` with `v ≤ y < v + n`," but an arbitrary tumbler in the lexicographic interval `[v, v+n)` need not be a V-position of `d` (deeper-depth tumblers inhabit the interval and are not in `dom(M(d))`). The justification therefore overreaches M-int's precondition. The conclusion is sound only because the relevant `y` are the block's V-positions `v + k`, which lie in `dom(M(d))` by B3 (Consistency, ASN-0058) — not because M-int speaks about all interval points.

**Required**: Restrict the quantifier to `V(β) = {v + k : 0 ≤ k < n} ⊆ dom(M(d))` (B3), then apply M-int to each `y = v + k ∈ dom(M(d))`. State the `V(β) ⊆ dom(M(d))` step explicitly so the M-int precondition is discharged rather than silently widened.

### Issue 2: Verbatim coverage-membership caveat repeated across worked configurations

**ASN-0070, "A Worked Example"**: the same disambiguating clause — "the only depth-`m_a` members of [coverage] are ...; since the block I-extents are depth-`m_a`, the intersections meet coverage only at {...}, and we write that finite set where the intersections are computed" — recurs nearly verbatim in Configuration 1, Configuration 2, Configuration 3, and Configuration 5.

**Problem**: This note carries `review-mode.anti-bloat`. The caveat (coverage is an infinite half-open interval but only its depth-`m_a` members can meet the depth-`m_a` block I-extents) is a single structural fact about how intersections are computed. Restating it once per configuration is the "two paragraphs say the same thing in different words" accretion pattern; a precise reader must re-read identical boilerplate four times.

**Required**: State the depth-`m_a` reduction once (e.g., as a remark preceding the configurations or in F-contig's neighborhood), then cite it per configuration rather than re-deriving it inline each time.

## OUT_OF_SCOPE

### Topic 1: Concurrency semantics of `follow` against a concurrently-modified document
The note's third Open Question raises this; it belongs to a future transition-interleaving ASN, not this query-definition note.

### Topic 2: Resolution relationships across documents with shared transclusion lineage
Raised in the Open Questions; this is new territory (cross-version correspondence under FOLLOWLINK), not a defect in F0–F-multidoc.

META: (none — the ASN defines a state-pure query operation via the inverse-image relation, with abstract postconditions an alternative implementation must also satisfy; it has not drifted into implementation mechanics.)

VERDICT: REVISE
