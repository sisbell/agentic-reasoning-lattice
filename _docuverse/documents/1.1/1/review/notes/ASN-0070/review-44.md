# Review of ASN-0070

The mathematics is sound and unusually thorough — the F-canonical existence/uniqueness proof (maximal-run partition, the consecutivity characterisation with its induction, left/right closure) holds up, the five worked configurations exercise the genuine boundary cases (empty, multiplicity, cross-subspace straddle, state-dependence), the wp analysis is appropriate for a pure query, and the I/O subspace biconditional is correctly discharged via S3★ + S3★-aux + L14. No correctness defect found. The remaining issues are the accreted prose the anti-bloat classifier targets.

## REVISE

### Issue 1: Discussion section re-narrates already-stated derived properties

**ASN-0070, "Discussion: System Guarantees"**: "*Determinism (F-det).* Nelson's commitment ... is the structural consequence of working with functions ... *Origin symmetry (F-origin)* ... *State dependence (F-state)* ... *No preferred document (F-multidoc)* ..."

**Problem**: Each of these four paragraphs restates a derived property already fully specified above (F-det, F-origin, F-state, F-multidoc) and re-dresses it in interpretive prose. This is the "two paragraphs say the same thing in different words" pattern — a recap section that adds no formal content, only a Nelson gloss already available at each property's own site. It is the kind of essay accretion that compounds across cycles.

**Required**: Fold the one genuinely-new motivational sentence per item (if any) into the corresponding property's statement, and delete the standalone recap. The properties should carry their own system reading; a separate narration is redundant.

### Issue 2: Defensive reassurance prose not advancing a claim

**ASN-0070, F-subspace, "Derived guarantee (lookup totality)"**: "... so a `C`-lookup does not apply by design — the appropriate access is the link store. Both branches are determined by the foundations; there is no resolution outcome that references absent content."

**ASN-0070, "Computation via Decomposition" (closing paragraph)**: "No special logic handles fragmentation; the decomposition delivers it automatically. The same observation explains multiplicity ..."

**Problem**: Both passages explain *why the design is safe / why no special handling is needed* rather than stating a claim or a step. The lookup-totality derivation is complete once `M(d)(v) ∈ dom(C)` (resp. `dom(L)`) is established; the trailing "determined by the foundations / no resolution outcome references absent content" is reassurance. Likewise "No special logic handles fragmentation; the decomposition delivers it automatically" is implementation-reassurance sitting in a section already qualified as merely "one admissible computation."

**Required**: Trim to the load-bearing fact (the two store-membership consequences; that fragmentation/multiplicity are the per-block image of non-adjacent or shared I-extents). Cut the "by design / determined by the foundations / no special logic" reassurance.

## OUT_OF_SCOPE

### Topic 1: Cross-home, concurrency, and shared-lineage resolution relationships
**Why out of scope**: The three Open Questions (multi-home endset resolution across documents transcluding different home subsets; concurrency semantics under concurrent modification; the relationship between `follow(ℓ, d, i)` and `follow(ℓ, d', i)` under shared transclusion lineage) are new territory requiring their own operations/invariants, not gaps in this query's specification.

VERDICT: REVISE
