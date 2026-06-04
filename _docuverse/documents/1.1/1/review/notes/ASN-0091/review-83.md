# Review of ASN-0091

The mathematical core is sound. I checked the abstract Vstream-only class definition, the REARRANGE_K realisation (the K.μ~ clause (i)–(v) discharges, the net-effect split, the reachability route to RA-adm), and every RE-* derivation. The five worked examples are arithmetically correct (I recomputed the 3-cut pivot, 4-cut swap, interior-cut, coalescence, and collapse traces against R-P1/R-P2 and R-S1/R-S2/R-S3). L-chain is correctly applied in the run-cardinality witnesses, and the bijection-non-uniqueness example correctly establishes that RE-proj's set image is witness-independent. Boundary cases (empty arrangement, single-value collapse, non-empty in-S exterior) are each instantiated. The findings below are confined to meta-prose, per the `review-mode.anti-bloat` classifier.

## REVISE

### Issue 1: Defensive non-claim prose imagining an excluded case
**ASN-0091, "Reachability scope of the realisation"**: "The abstract RA-adm clause as defined quantifies over arbitrary Σ; for a Σ that satisfies every per-state invariant but is not reachable, the reachability route supplies nothing, and the realiser's admissibility is not claimed there."
**Problem**: The preceding two sentences already scope the realisation theorem to reachable Σ ("we scope the realisation theorem accordingly — REARRANGE_K realises ... on every Σ reachable from Σ₀ ..."). The quoted sentence then conjures a non-reachable-but-invariant-satisfying Σ solely to state what is *not* proved there. This is a defensive justification about a case the stated scope already excludes — the anti-bloat pattern "a paragraph imagines a case the claim's precondition already excludes." A reader following the realiser proof must skip past it.
**Required**: Delete the final sentence; the scoping is fully carried by the prior sentence naming reachable Σ as the theorem's domain.

### Issue 2: Collapse-case explanation dispersed across sections
**ASN-0091, "Transclusion Preservation" (iii)**: "it may nonetheless hold, as in the net-effect collapse and identity cases where Σ' = Σ leaves every arrangement unchanged."
**Problem**: The collapse mechanism is introduced and proved in the net-effect split, given a dedicated worked example ("Net-Effect Collapse"), and referenced again here as a side remark. The conclusion (iii) only needs to state that it carries the hypothesis `origin(a) ≠ d`; the parenthetical speculation that (iii) "may nonetheless hold" in the collapse case is a cross-reference to the collapse concept that does not advance the guarantee being stated, and the following sentence ("The transclusion premise origin(a) ≠ d_view does not imply (iii)'s condition origin(a) ≠ d") restates the same logical-independence point a second time.
**Required**: State (iii)'s hypothesis once; drop the "may nonetheless hold" aside and the redundant restatement of condition-independence.

## OUT_OF_SCOPE

### Topic 1: Link-subspace rearrangement semantics
**Why out of scope**: CS3 fixes the cut subspace at `s_C`; what an analogous link-subspace operation would preserve is correctly deferred to the Open Questions and belongs in a future ASN.

### Topic 2: Reconstitution of a same-source span split by a cut
**Why out of scope**: The note explicitly declines to establish whether two fragments jointly reconstitute a transcluded span (RE-trans closing remark). This is genuinely new territory, correctly listed as an open question rather than asserted.

VERDICT: REVISE
