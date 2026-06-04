# Review of ASN-0091

This ASN is mathematically sound. I traced all four worked examples (3-cut pivot, 4-cut swap, interior cuts, shared-address non-uniqueness) at the value level — the R-P1/R-P2/R-S1/R-S2/R-S3 computations, the π formulas from R-PPERM/R-SPERM, the run-decomposition cardinalities, and the ChainDisjointAdjacency applications all check out. The d-vs-d_tgt distinction in RE-trans is handled correctly, the abstract S2 and RE-subpres derivations are valid, and the shape-package/remaining-invariant split correctly keeps mapping-dependent S8★ out of the "from RA-dom alone" layer. No cross-ASN references outside the foundation set. The findings below are the meta-prose the `anti-bloat` classifier flags.

## REVISE

### Issue 1: RA-frame definition parenthetical duplicates the discharge table
**ASN-0091, "REARRANGE as Vstream-Only Operation"**: the RA-frame block closes with "(of which `Σ'.C = Σ.C` and the other-document clause … are inherited from ASN-0084's ArrangementRearrangement, while `Σ'.L = Σ.L`, `Σ'.E = Σ.E`, `Σ'.R = Σ.R`, and `dom(Σ'.M) = dom(Σ.M)` are the new clauses this ASN introduces)".
**Problem**: This inherited-vs-new inventory is provenance bookkeeping that does not advance the definition of RA-frame, and it is restated verbatim in substance by the RA-frame row of the "Abstract class clause ← REARRANGE_K source" table ("matches each conjunct explicitly except `dom(Σ'.M) = dom(Σ.M)`, which follows structurally…"). A reader must skip the parenthetical to read the frame itself.
**Required**: Delete the parenthetical; the realization table is the correct home for clause provenance.

### Issue 2: RE-R carries a defensive double-justification via J3
**ASN-0091, "Origin and Provenance Invariance"**: "For REARRANGE_K specifically, the same conclusion is independently supplied by ASN-0047's J3 (Reordering Isolation) … — confirming that K.μ~ realizes the abstract class's R-preservation property." Repeated in the worked example: "Σ'.R = Σ.R by RA-frame directly; equivalently, by ASN-0047's J3 … through K.μ~'s frame."
**Problem**: RA-frame already pins `Σ'.R = Σ.R`. The J3 "confirms/equivalently" cross-check adds no reasoning — it is belt-and-suspenders provenance appearing twice.
**Required**: State RE-R from RA-frame once; drop the J3 confirmation in both places (or fold a single mention into the provenance table, where RE-R already cites J3).

### Issue 3: Summary paragraph after RE-ext restates RE-sub and RE-ext
**ASN-0091, end of "In-Subspace Exterior Frame"**: "The pointwise-fixity strengthening — both RE-sub's fixity on non-S V-positions and RE-ext's fixity on in-subspace exterior V-positions — is the joint content of R-PPERM/R-SPERM … and R-FRAME-P/S(a)/R-EXT … : REARRANGE_K's cut sequence operates only on the affected range within a single subspace and leaves everything else verbatim."
**Problem**: This recapitulates the two preceding paragraphs (RE-sub and RE-ext, each already stating its π-fixity source and arrangement-preservation source) without adding content.
**Required**: Delete the summary paragraph.

### Issue 4: Contentless forward pointer
**ASN-0091, "What the Content Store Sees: Nothing"**: "The same observation applies symmetrically to the link store via RA-frame. We will exploit this when reasoning about links below."
**Problem**: "We will exploit this … below" is a forward pointer with no propositional content; the link-store fact is restated as RE-L where it is actually used.
**Required**: Drop the second sentence (keep the first if the symmetric link-store fact is wanted here).

### Issue 5: "Abstract class would permit X; REARRANGE_K pins it" repeated across sections
**ASN-0091, clause-correspondence section, RE-sub/RE-ext sections, and Interior Cuts example**: the same point recurs — "The abstract class alone — via RA-adm + RE-subpres — would permit a bijection that non-trivially permuted within each subspace; RE-sub and RE-ext together pin REARRANGE_K…"; and "The abstract class … would permit a bijection that moved `[1, 1]` and `[1, 5]`; R-EXT is what pins them."
**Problem**: The same claim (the abstract class is looser than REARRANGE_K, which the R-PPERM/R-SPERM branch structure tightens) is made in three different words across three locations.
**Required**: State it once — the Interior Cuts example is the natural site since it exhibits the non-empty exterior concretely — and remove the duplicates.

## OUT_OF_SCOPE

### Topic 1: Link-subspace rearrangement semantics
**Why out of scope**: The ASN fixes the cut subspace to s_C (CS3) and explicitly defers link-subspace reordering to an Open Question. This is new territory, correctly excluded.

### Topic 2: Reconstitution of a same-source span split across cuts
**Why out of scope**: RE-trans establishes per-byte origin survival; whether two fragments *jointly reconstitute* the original source span is correctly routed to the first Open Question rather than asserted.

META: (none — the ASN defines an abstract Vstream-only transition class with state, frame, and invariants stated implementation-independently; it has not drifted into mechanics.)

VERDICT: REVISE
