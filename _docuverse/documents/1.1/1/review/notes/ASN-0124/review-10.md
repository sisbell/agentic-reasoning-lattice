# Review of ASN-0124

I checked every introduced claim against its derivation, the boundary cases, and the foundation citations. The mathematics is sound. FD-IMGC's (⊇) direction correctly forces `subspace(v) = s_C` via S3★ + SD; FD-FRESH's clear-then-rebuild composite is genuinely valid (the initial-to-final couplings J0/J1★/J1'★ are discharged, and the cleared intermediate state satisfies the per-state shape package vacuously); FD-VERS's `ran_C(d_new, Σ') = ran_C(d_op, Σ)` follows from J4's derived consequence; FD-VDYN(d)'s swing law and both absorption/non-absorption constructions check out; the FD-NEUT(c) and FD-LOSSY constructions are reachable and valid. Transition coverage is complete (all seven atomics plus K.μ~), and boundary cases (empty `Q`, empty `W`, fresh document, `Ret = ∅`, `I = ∅`, first-insertion, pure append) are handled. The historical companion (FD-HIST…FD-COINC) is internally correct, deriving locally from ASN-0047's provenance apparatus.

The findings below are anti-bloat trims, consistent with this note's `review-mode.anti-bloat` classifier. They are prose-accretion items, not rigor defects.

## REVISE

### Issue 1: The "document-side analogue of ASN-0127, derived independently" justification is restated at four sites
**ASN-0124, Introduction / Scope / Query Algebra preamble / Dynamics preamble**:
- Intro: "we do not rebuild ASN-0127's machinery — we cite its image primitive and its resolution-drift results where they apply."
- Scope: "we cite ASN-0127's image layer rather than re-deriving it."
- Query Algebra: "Each law below is the document-side analogue of an ASN-0127 Phase-2 law, derived independently because the predicate differs (arrangement ranges, not stored coverages)."
- Dynamics: "The methodology mirrors ASN-0127's existence lane..."

**Problem**: This is one defensive de-duplication claim — *we re-derive the document-side versions rather than citing ASN-0127, because the predicate differs* — repeated across four sections. The intro paragraph carries genuine content (the inversion: ASN-0127's link coverages are immutable so its fixed-`I` query only grows, whereas document arrangement ranges are mutable so the answer breathes); that insight is load-bearing and should stay. The three restatements add nothing the reader needs to follow FD-UDIST or FD-FRAME — they are preamble to skip past, and exactly the kind of forward-reference/de-dup justification that compounds across cycles.

**Required**: State the relationship once (in the inversion paragraph). Delete the cite-don't-rebuild restatement in the Scope paragraph, the "document-side analogue … derived independently because the predicate differs" preamble before FD-UDIST, and the "methodology mirrors ASN-0127's existence lane" clause in the Dynamics preamble. Where a specific result is reused, the inline citation (F-IMG-MONO, F-IMG-SWING, etc.) at the point of use already carries the relationship.

### Issue 2: Section-methodology self-narration in the Dynamics section
**ASN-0124, Dynamics preamble and FD-NONMONO**:
- Dynamics preamble: "…through resolution, which we take up at the end."
- FD-NONMONO: "The motion enters through the pointing, not through the containing — which is why this section fixed I first."
- FD-NONMONO table/prose: "composed per transition by FD-VDYN."

**Problem**: These narrate the document's own organization ("which we take up at the end," "which is why this section fixed I first," "composed per transition by FD-VDYN") rather than advancing any claim. Two of them are forward pointers to FD-VDYN from within the same section; one explains the section's ordering choice. None is needed to follow the non-monotonicity result.

**Required**: Remove the self-narration clauses. FD-NONMONO can state non-monotonicity and the resolution-drift motion (citing D-PRES) without explaining why the section fixed `I` first or pointing ahead to FD-VDYN; FD-VDYN stands on its own when reached.

## OUT_OF_SCOPE

None. The note's eight Open Questions correctly defer future territory (intra-composite coherence, temporal ordering of provenance, attribution-bearing answers, past-arrangement reach, distributed availability, authority, provenance compaction, multiplicity exposure), and the multi-server completeness gap is correctly scoped out as a refinement concern rather than treated as an error here.

VERDICT: REVISE
