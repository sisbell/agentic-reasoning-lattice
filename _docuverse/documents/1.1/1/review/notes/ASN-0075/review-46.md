# Review of ASN-0075

## REVISE

### Issue 1: Duplicated negative-scope prose about the disjointness argument
**ASN-0075, "The SHOWDELETIONS Operation" and "Edge Cases / Same document compared against itself"**: The definition section states "the disjointness is unconditional — it needs neither D-EXH nor any composite-boundary hypothesis," and the same-document edge case repeats "it needs neither D-EXH nor the composite-boundary hypothesis."
**Problem**: The identical negative-scope claim (what the argument does *not* need) is asserted in two separate sections. The edge case already says it is "the unconditional disjointness argument … specialised to a single document," so the repeated disclaimer adds nothing.
**Required**: State the unconditionality once (at the definition) and let the edge case cite it without re-litigating the absence of D-EXH/boundary dependence.

### Issue 2: Negative-scope meta-prose in D-IDENT (Transclusion integrity)
**ASN-0075, "Identity Preservation," Transclusion-integrity bullet**: "The link clause of S3★ targets dom(L) rather than dom(C) and is not invoked here; SHOWDELETIONS is restricted to the content subspace (D-SUBSP), so only the content clause is load-bearing for transclusion integrity."
**Problem**: This sentence explains which foundation clause is *not* used. It does not advance the transclusion-integrity argument; a reader following the claim must skip past it. The content-clause citation already suffices.
**Required**: Delete the "not invoked here" sentence; cite the content clause of S3★ directly without inventorying the unused clause.

### Issue 3: "Origin attribution" bullet is an empty forward reference
**ASN-0075, "Identity Preservation," third guarantee**: "Origin attribution. Origin survives recovery — the chain of provenance is not severed (origin determinacy and invariance via S7 are established in D-ORIG)."
**Problem**: The bullet states no substance of its own — it defers entirely to D-ORIG, which proves origin determinacy/invariance. It duplicates D-ORIG while contributing nothing to the identity-preservation argument, and it forward-points to a downstream claim in a structural slot.
**Required**: Either remove the bullet (origin is covered by D-ORIG) or have it carry an actual identity-preservation consequence rather than pointing forward.

### Issue 4: Claims-table D-DISCR overstates the body's labeled lemma
**ASN-0075, "Claims Introduced," D-DISCR row vs. "Why the Provenance Relation Is Load-Bearing"**: The table's D-DISCR reads "No function of (C, L, E, M) alone can distinguish … ; any system supporting SHOWDELETIONS must maintain state components C* beyond the four …"
**Problem**: In the body, Lemma D-DISCR proves only the indistinguishability claim. The "must maintain C*" necessity conclusion is derived in a separate, *unlabeled* paragraph ("The discrimination obligation follows in one step …"). The table attributes both to one label, so the table's D-DISCR is broader than the body's D-DISCR.
**Required**: Either label the necessity obligation as its own claim and reference it in the table, or narrow the table's D-DISCR entry to match the lemma it labels.

## OUT_OF_SCOPE

### Topic 1: Reporting content deleted from both compared documents but current in a third
**Why out of scope**: This is the n-ary / third-witness generalization the ASN itself defers to Open Questions; it is new territory (families of >2 documents), not an error in the binary operation specified here.

### Topic 2: Span-based finite presentation of the deletion set
**Why out of scope**: Compacting output into contiguous I-address spans is a presentation/representation concern (D-ACT explicitly leaves packaging to the implementation); it belongs to a future arrangement-presentation ASN.

VERDICT: REVISE
