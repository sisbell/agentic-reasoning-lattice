# Review of ASN-0091

## REVISE

### Issue 1: First Worked Example re-verifies the entire foundation-invariant package that RA-adm already discharged abstractly
**ASN-0091, "Worked Example" → Admissibility (RA-adm) bullet**: the bullet walks S2, S8a, S8-depth, S3★, D-CTG★, D-MIN★, D-SEQ★, S3★-aux, CL-OWN, CL-UNIQ, and S8★ concretely against `Σ'.M(d)`.
**Problem**: RA-adm is already established abstractly for every reachable `Σ` (the realiser section), and the concrete-example mandate asks the example to verify the *key postconditions* — the RE-* claims, which the preceding bullets already do. Re-deriving each per-state invariant by hand is an exhaustiveness/use-site inventory that the reader must skip to reach the headline checks. The four later worked examples then each carry an "Admissibility (RA-adm)" note that defers back to "the first Worked Example's pattern" — the same-location deferral pattern compounding the accretion.
**Required**: Drop the per-invariant concrete sweep (RA-adm is proven once, abstractly); keep only the RE-* postcondition checks in the example. Remove the repeated "discharge as in the first Worked Example" admissibility notes from the 4-cut, Interior-Cuts, and Collapse examples — each should state only its delta.

### Issue 2: RE-sub is derived twice
**ASN-0091, K.μ~ admissibility table clause (v)** vs **"Subspace Frame (REARRANGE_K-specific)"**: clause (v) discharges "RE-sub: by CS3 the cut subspace is S = s_C, so every subspace(v) = s_L V-position lies on R-PPERM/R-SPERM's non-S branch, which sets π(v) = v pointwise." The dedicated section then re-establishes the same pointwise fixity (S = s_C means non-S = s_L, so the scopes coincide).
**Problem**: Two paragraphs in different sections prove the same statement. Clause (v)'s job is to discharge a K.μ~ admissibility requirement; once the standalone RE-sub section exists, clause (v) should cite it rather than re-prove it.
**Required**: Have clause (v) cite RE-sub; or fold the standalone derivation into clause (v). One derivation, one site.

### Issue 3: RE-sub and RE-ext sections are parallel boilerplate
**ASN-0091, "Subspace Frame" and "In-Subspace Exterior Frame"**: both run the identical template — "ASN-0084's R-PPERM and R-SPERM ... define π directly as the identity on [X] ... R-FRAME/R-EXT records the resulting arrangement preservation ... Together these supply RE-X in its full pointwise form."
**Problem**: The two cover different position sets (non-cut-subspace vs in-subspace exterior), so they are not redundant, but the framing prose is copied verbatim with one substitution. The boilerplate is noise.
**Required**: State both pointwise-fixity facts once with a single shared sentence and the two position-set predicates, rather than duplicating the four-line template.

### Issue 4: Repeated Nelson-paraphrase framing lines
**ASN-0091, multiple sections**: "This is the formal content of Nelson's...", "This is the formal precipitate of Nelson's 'links between bytes can survive rearrangements'", "This is Nelson's 'arrive at the same content...'", "This is the formal precipitate of Nelson's 'REARRANGE is document-scoped'", "This is the formal account of Nelson's 'the endset becomes a discontiguous set of bytes'".
**Problem**: Five near-identical interpretive framings, none advancing the proof. One grounding line per source idea is fine; the recurring template is essay accretion.
**Required**: Keep grounding where it does work; collapse the repeated "this is the formal precipitate of Nelson's X" framing to at most one or two load-bearing instances.

## OUT_OF_SCOPE

None — the Open Questions (same-source span splitting, link-subspace rearrangement semantics, observational equivalence, run-cardinality bounds, bijection realizability) are correctly deferred rather than half-answered.

VERDICT: REVISE
