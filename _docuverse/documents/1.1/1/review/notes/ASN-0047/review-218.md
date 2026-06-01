# Review of ASN-0047

I checked the elementary-transition definitions, the coupling/isolation calculus, the K.δ allocator-dispatch discharge, the K.μ~ decomposition and its fixity lemmas, the D-SEQ★ derivation, and verified the worked-example tumbler arithmetic (b_C/b_L anchors, fork addresses, link emissions) against the foundation contracts. The technical content holds up under that scrutiny — the necessity/sufficiency proof of the K.μ~ precondition (with the explicit π_swap witness), the FrontierEquivalence biconditional, and the GlobalLineage(iii) inc-chain induction are all sound, and the Class (a)/Class (b) partition is handled consistently.

The findings below are prose-level (anti-bloat), which the note explicitly directs me to surface.

## REVISE

### Issue 1: K.μ~ S3★ discharge restates its non-circularity ~5 times
**ASN-0047, *Decomposition of K.μ~*, Steps (A)–(B)**: The single claim "S3★(Σ') is recovered from the decomposition, not assumed as a filter hypothesis" is asserted in the intro paragraph ("Step (A) below establishes subspace preservation from the decomposition's K.μ⁺ content-subspace precondition (realisability), *not* from the post-state package S3★(Σ')"), again at Step (A)'s opening ("with no appeal to the filter-stipulated S3★(Σ')"), again at Step (A)'s close ("the discharge rests on the decomposition rather than on assuming S3★(Σ')"), again at Step (B)'s framing, and again at Step (B.3) ("consistently with S3★(Σ')").

**Problem**: This is the "prose justifies non-circularity" pattern. After the regrounding recorded in the recent revision, the *argument* is the load-bearing content; the repeated disclaimer is meta-prose a reader must skip past to follow the actual chain (B.1 → B.2 → B.3). The duplication between Step (A)'s closing sentence and Step (B)'s opening sentence is the same statement in different words.

**Required**: State the non-circularity once (e.g., a single sentence at the head: "S3★(Σ') is established by Step (B), not assumed"), then let Steps (A)/(B) carry only their object-level content. Remove the four restatements.

### Issue 2: "Structurally sufficient" modification-mode enumeration duplicates downstream detail
**ASN-0047, *Elementary transitions*** (the paragraph "The seven elementary kinds … are *structurally sufficient* for the *catalogued* modification modes …"): the three replacement forms (prior-provenance two-step, first-time three-step, fresh-content four-step) are enumerated here in full, then re-enumerated in the *Decomposition of K.μ~* discussion and a third time across the two replacement worked examples.

**Problem**: A use-site inventory of replacement forms placed in the elementary-transitions overview restates content the worked examples already carry. The reader meets the same (in C, in R) / (in C, not in R) / (not in C, not in R) partition three times.

**Required**: Keep the partition statement at one site (the worked-example contrast paragraph already states it cleanly as the exhaustive case split) and reduce the elementary-transitions occurrence to a one-line pointer, or vice versa — but not both in expanded form.

## OUT_OF_SCOPE

### Topic 1: Interior deletion / tombstoning under D-CTG★
The consequence that K.μ⁻ admits only per-subspace suffix removal — so withdrawing an interior link/character requires withdrawing everything allocated after it — is a real limitation, but the ASN correctly identifies it in the Open Questions (the tombstoning reconciliation item) rather than papering over it. No revision needed; the limitation is a derived property, not an error.

### Topic 2: Concurrent allocation under a shared home document
The SequentialTransitionAxiom assumes totally-ordered atomic transitions; concurrent K.α/K.λ under one document is excluded by that axiom and flagged as future work in the Open Questions. This is appropriately deferred, not a gap in the present model.

META:

VERDICT: REVISE
