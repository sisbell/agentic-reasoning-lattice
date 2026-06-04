# Review of ASN-0091

I checked the abstract Vstream-only definition, the REARRANGE_K realisation argument (clause-by-clause discharge of K.μ~ admissibility, reachability scoping of RA-adm), every RE-* derivation, the L-chain lemma, all five worked examples (verifying the cut arithmetic, π construction, and run-cardinality counts against R-P1/R-P2/R-S1–3), and the multi-step ★ closure. The mathematics is sound throughout — the worked examples compute correctly, L-chain's `x+1 = inc(x,0)` identification is valid for T4-valid chain elements, the net-effect collapse and bijection-non-uniqueness cases are handled honestly, and the composite-boundary discharge (P4★/P4a/P7a) holds. No cross-ASN reference violations: every citation is to a foundation ASN.

The remaining issues are precision and accreted meta-prose, consistent with the `review-mode.anti-bloat` classifier.

## REVISE

### Issue 1: Imprecise collapse condition in the net-effect split

**ASN-0091, "REARRANGE_K Realises the Abstract Class" (net-effect split)**: "when the affected range carries a repeating I-address pattern whose period matches the permutation's displacement, R-P1/R-P2 may yield `M'(d) = M(d)` although π is the non-identity rotation."

**Problem**: "period matches the permutation's displacement" is a loose heuristic presented in the slot where the precise condition belongs. It is not the actual collapse condition — the all-equal arrangement (period 1) in the very own "Net-Effect Collapse" worked example collapses under a pivot whose displacements are 1 and 2, so no "period = displacement" alignment holds. The precise condition is stated correctly in the next sentence ("a permutation that maps each shared-image V-position to another V-position carrying the same image leaves the map pointwise unchanged"). The "period matches displacement" clause adds nothing exact and misdirects a careful reader.

**Required**: Delete the "period matches displacement" gloss and let the precise pointwise condition stand, or replace it with the precise characterisation (π fixes the value at every affected position: `M(d)(π(v)) = M(d)(v)` for all affected `v`).

### Issue 2: Provenance-column entries restate body derivations

**ASN-0091, "Claims Introduced" tables (Provenance column)**: e.g. RA-adm's entry — "REARRANGE_K realisation *scoped to reachable Σ*: the K.μ~-validity / empty-composite argument makes Σ' reachable, whence the per-state foundation invariants follow at Σ' (the realiser's admissibility is not claimed at non-reachable invariant-satisfying Σ)."

**Problem**: Several Provenance entries are full sentences with parenthetical disclaimers that duplicate prose already carried in the body ("Reachability scope of the realisation" paragraph here, and the RA-π/RA-frame discharge paragraphs for others). This is the "two paragraphs say the same thing in different words" pattern in a structural slot — the table is meant to index where a claim comes from, not re-argue it. When the index restates the derivation, the reader must reconcile two phrasings of the same content.

**Required**: Reduce Provenance entries to a terse source pointer (e.g., RA-adm → "abstract definition; REARRANGE_K realiser, reachable Σ"), letting the body carry the argument and the disclaimers.

### Issue 3: Parenthetical "what-if" remark in the fragmentation witness

**ASN-0091, "Run Decomposition Is Not Invariant" (Direct witness, fragmentation)**: "The transclusion in this arrangement is incidental: the same fragmentation occurs whenever chain-adjacent I-addresses are rearranged to V-non-adjacent positions, regardless of origin (e.g., a pre-state with `a₁, a₂, b₁` all owned by `d` would fragment identically under the same cut sequence)."

**Problem**: This sentence imagines an alternative arrangement the witness does not use, to disclaim a property (origin-dependence) the witness never claimed. It does not advance the fragmentation argument — the witness already establishes RE-frag. It is the "paragraph imagines a case the claim already excludes / defensive aside" pattern.

**Required**: Remove the parenthetical; the witness stands on its own. If the origin-independence of fragmentation is worth a claim, it belongs as a stated property, not an aside.

## OUT_OF_SCOPE

### Topic 1: Joint reconstitution of a span split across two fragments

The RE-trans body correctly notes that when a cut splits a same-source transcluded span, "Whether the two fragments *jointly reconstitute* the original source span ... is not established here," and the first Open Question records it.

**Why out of scope**: This concerns span-reconstitution semantics over fragmented projections — a new property about how fragmented endsets relate to their source span, not an invariant of the REARRANGE transition itself. Correctly deferred.

### Topic 2: Link-subspace rearrangement semantics

The second Open Question asks what semantics rearrangement should carry on the link subspace. REARRANGE_K fixes `S = s_C` (CS3), so the link subspace is only ever framed here.

**Why out of scope**: A link-subspace rearrangement operation is a distinct operation needing its own preconditions and invariants; its absence is not an error in this content-subspace ASN.

VERDICT: REVISE
