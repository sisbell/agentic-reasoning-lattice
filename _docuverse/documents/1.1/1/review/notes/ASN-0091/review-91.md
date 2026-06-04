# Review of ASN-0091

## REVISE

### Issue 1: Composite-boundary necessity stated in three places
**ASN-0091, "Composite-Boundary Properties" + RA-bndy table row**: the section opens "ASN-0047's three composite-boundary properties P4★ ∧ P4a ∧ P7a are not of this kind... establishing these three only at composite boundaries — not at states interior to a composite still in progress," and the RA-bndy provenance cell repeats "required because ASN-0047's P4★ ∧ P4a ∧ P7a hold only at composite boundaries, not at composite-interior states."
**Problem**: The table cell restates the section's opening paragraph nearly verbatim. The claims-table is an index; carrying the full motivating justification in a cell duplicates load-bearing prose that lives in the section. This is the accretion pattern of essay content in a structural slot.
**Required**: Reduce the RA-bndy cell to a bare statement of the precondition plus a pointer to the section; keep the rationale in one location.

### Issue 2: Repeated deferral to "the net-effect split"
**ASN-0091, clause-(ii) discharge cell, "Worked Example — Net-Effect Collapse" setup (twice), RA-adm paragraph**: clause (ii) reads "holds by hypothesis in the non-trivial case of the net-effect split established above"; the collapse example cites "(net-effect split, above)" and "the shared-image licence (net-effect split, above)."
**Problem**: Multiple paragraphs in different sections each defer back to the same established split, a flagged forward/back-reference accretion pattern. Each deferral re-anchors the reader to the same upstream paragraph rather than advancing local reasoning.
**Required**: State the split once as a named fact; let later sites invoke it by name without re-narrating "established above / net-effect split, above" each time.

### Issue 3: Shared-image licence justifies rather than states
**ASN-0091, "Net-effect split" paragraph**: "S2 (ArrangementFunctionality) imposes only functionality on M(d) — at most one image per V-position — and never a single-image (injectivity) constraint, while S5 (UnrestrictedSharing) explicitly admits a single I-address at several V-positions."
**Problem**: This is justificatory prose explaining why sharing is permitted (re-deriving the content of foundation S2/S5) rather than advancing the construction. The split needs only the citation "non-singleton pre-image blocks are admissible (S2, S5)."
**Required**: Compress to the foundation citation; drop the re-explanation of what S2 and S5 already say.

## OUT_OF_SCOPE

### Topic 1: Same-source span reconstitution after a cut
**Why out of scope**: Whether two fragments of a same-source transcluded span jointly reconstitute the original (raised in "Cross-Document Transclusion Preserved" and the first Open Question) is genuinely new territory — a bundle-reassembly guarantee, not a REARRANGE invariant. Correctly deferred.

### Topic 2: Link-subspace rearrangement semantics
**Why out of scope**: The second Open Question (what invariants a link-subspace reordering must preserve) is future work; this ASN's cuts are content-subspace only (CS3), and RE-sub correctly freezes the link subspace.

Technical content checked: L-chain (disjoint-adjacency), the fragmentation/coalescence/equality witnesses, the bijection non-uniqueness and collapse traces, and the RE-proj/RE-disc derivations are sound, including the collapse-case consistency where π ≠ id yet fixes the projection set. No correctness defects found; the REVISE items are accretion, not error.

VERDICT: REVISE
