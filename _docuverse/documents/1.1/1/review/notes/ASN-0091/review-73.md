# Review of ASN-0091

This ASN carries the `review-mode.anti-bloat` classifier. I checked the proofs and edge cases first (no correctness error found — the abstract/concrete split, the net-effect collapse case, the ChainDisjointAdjacency lemma, and the four worked examples all hold up), then swept for accreted meta-prose and forward-reference noise. The findings below are the latter.

## REVISE

### Issue 1: Redundant deferrals to the Provenance column
**ASN-0091, "REARRANGE_K Realises the Abstract Class" and "Composition Across Multi-Step…"**: "The REARRANGE_K realisation sources for the remaining abstract clauses (RA-π, RA-dom, RA-frame, RA-adm) are recorded in the Provenance column of the Claims Introduced table." … and later: "The ★ table's *Provenance* and *Composition Conditions* columns carry these bare-equality cases; we do not restate each here."
**Problem**: Two paragraphs in different sections defer the reader to the same downstream table columns rather than advancing the argument. The first sentence is a pure pointer — it states nothing the table does not, and the clause-by-clause discharges that follow it (RA-reg, then the per-invariant table) are where the actual work happens. This is the "multiple paragraphs defer to the same downstream location" pattern.
**Required**: Drop the pointer sentences. The Provenance column is self-describing; the prose only forces a jump.

### Issue 2: Preview sentence restated as full sections
**ASN-0091, "Clause Correspondences and Per-Invariant Discharges"**: "The cut sequence further restricts the bijection beyond what the abstract class requires — π acts as identity on V-positions outside the affected range and on V-positions in subspaces other than the cut subspace S, supplying RE-sub (subspace frame) and RE-ext (in-subspace exterior frame) below."
**Problem**: This previews content that the dedicated "Subspace Frame" and "In-Subspace Exterior Frame" sections then derive in full from R-PPERM/R-SPERM and R-FRAME-P/S(a)/R-EXT. The preview adds no premise the later sections lack; it is a forward pointer that the standalone sections make redundant.
**Required**: Remove the preview clause; let RE-sub/RE-ext be introduced where they are derived.

### Issue 3: Frame-definition prose justifies provenance instead of stating the clause
**ASN-0091, "REARRANGE as Vstream-Only Operation"**: "the genuinely new frame conjuncts — fixing the link store `L`, the entity set `E`, the provenance relation `R`, and the document registry, components on which ASN-0084 imposes nothing — collected with the inherited conjuncts into the full frame (RA-frame)".
**Problem**: "genuinely new … components on which ASN-0084 imposes nothing" is provenance rationale (why these conjuncts are listed apart from inherited ones) embedded in a definition that should simply state RA-frame. The which-clauses-came-from-where bookkeeping already lives in the Provenance column (Issue 1's target).
**Required**: State RA-frame's conjuncts directly; move any inherited-vs-new attribution to the table if it is wanted at all.

## OUT_OF_SCOPE

### Topic 1: Same-source span reconstitution after a splitting cut
**Why out of scope**: The RE-trans section correctly flags that whether two fragments of a same-source transclusion "jointly reconstitute" the original span "is not established here," and the Open Questions list it. This is genuinely new territory (a reconstitution semantics), not a gap in REARRANGE's invariants — properly deferred.

### Topic 2: Link-subspace rearrangement semantics
**Why out of scope**: CS3 confines cuts to the content subspace; a REARRANGE acting on the link subspace would be a distinct operation with its own invariants (CL-OWN, CL-UNIQ preservation). The ASN's Open Questions raise it appropriately.

VERDICT: REVISE
