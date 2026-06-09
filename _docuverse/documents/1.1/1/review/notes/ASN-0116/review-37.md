# Review of ASN-0116

I checked the allocation/shift mechanics, the composite decomposition over the K-vocabulary, the coupling-constraint discharge, the boundary cases (empty, append, front-into-nonempty), and the wp derivation. The mathematical content is sound and the cases are complete — the block-disjointness partition, the I3-V/I3-CS exclusion attribution, the J1'★ "record only A_new, not the shifted suffix" point, and the P7a pre-state→post-state lift are all handled correctly, and the worked examples exercise each boundary. The findings below are the prose-accretion patterns the `review-mode.anti-bloat` classifier asks me to surface; the underlying argument does not need to change.

## REVISE

### Issue 1: Editorial framing around consultation answers
**ASN-0116, multiple sections**: "The consultation is unanimous and emphatic on a single point"; "The consultation is sharp on the relationship the displaced positions bear to the prior arrangement (Q2)"; "Two finer points the consultation insists on"; "The consultation's two-sense answer (Q6) is discharged by named claims"; "The consultation is emphatic that this coupling is not a separately-maintained relation".
**Problem**: These describe the consultation's *tone/stance* ("unanimous," "emphatic," "sharp," "insists") rather than advancing the claim. A precise reader skips the frame to reach the substantive content (identity is permanent; a V-position binds no content; provenance is minted with allocation). This is essay framing in structural slots.
**Required**: Keep the substantive claim and keep the citations — both the primary-source refs (4/66, 4/11, granf2.c) and the (Qxx) consultation pointers must survive. Drop only the editorializing frame, e.g. "The consultation is unanimous and emphatic on a single point: at the instant new content enters the document it acquires a permanent identity" → "At the instant new content enters the document it acquires a permanent identity (4/11, 4/30)."

### Issue 2: Provenance-coupling theme restated across four sites
**ASN-0116, intro / I-PROV / PROV / closing**: intro — "INSERT therefore carries an obligation to grow R in lockstep with allocation"; plus the rationale block around the `Σ.R` definition ("this coupling is not a separately-maintained relation but is established by the act of insertion itself"); restated again in I-PROV, named in PROV ("provenance is established atomically-with-allocation … not deferred"), and echoed in "What we have established."
**Problem**: The same point ("provenance is minted with allocation, not deferred") is asserted four times in different words. I-PROV is the formal clause and PROV the named claim; the intro motivation and the closing echo are redundant restatements.
**Required**: Let PROV/I-PROV carry the obligation. Trim the intro to introduce `Σ.R` as a state component without pre-stating the coupling conclusion, and drop the coupling restatement from the closing summary.

### Issue 3: Two sections defer coupling-constraint discharge to the same downstream location
**ASN-0116, Effect section and "INSERT as a valid composite" section**: the Effect lists J0/J1★/J1'★ as "mandatory" and says "we discharge each constraint directly" (in the provenance section); the composite section separately states "clause 2 (the coupling constraints J0, J1★, J1'★) discharged at the composite boundary in the provenance section below."
**Problem**: Two paragraphs in different sections point forward to the same downstream discharge. This is the forward-reference accretion pattern — the reader is told twice where the proof lives before reaching it.
**Required**: Make one forward pointer (the composite section is the natural home, since it owns the ValidComposite★ clause-1/clause-2 split) and remove the duplicate from the Effect.

## OUT_OF_SCOPE

The Open Questions (shared/transcluded insertion point, concurrent insertion freshness, provenance under transclusion, post-fragmentation contiguity) are correctly posed as questions, not as claims — no out-of-scope claim is asserted. IP4/IP6 concern INSERT's *preservation* of existing-link coverage/discoverability, which is part of specifying INSERT, not link discovery (FINDLINKS); they are in scope.

VERDICT: REVISE
