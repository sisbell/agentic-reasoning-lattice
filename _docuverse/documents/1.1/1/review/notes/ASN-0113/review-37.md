# Review of ASN-0113

The mathematical core is sound. W4's ExactCoverage proof correctly invokes T5 on the shared prefix `[S,1,…,1]` of length `m_S − 1`, the half-open bounds pin the last component to `1..n_S`, and the depth-3 instance genuinely exercises prefix-confinement where `m_S = 2` leaves it vacuous. W10/W11/W16/W19/W20 all carry explicit derivations, the worked instances check the load-bearing postconditions, and the wp analysis (W19) is non-trivial. The findings below are anti-bloat, per this note's `review-mode.anti-bloat` classifier.

## REVISE

### Issue 1: Open question Q2 is meta-prose mapping the open-question structure and duplicating the final open question
**ASN-0113, Open Questions (second item)**: "(This is the consumer-side reading; the operation-side counterpart — what the operation must guarantee so the kind-list stays fixed and reports stay comparable when the convention is extended — is the final open question below.)"
**Problem**: The parenthetical does not pose or advance a question — it explains how Q2 relates to the final open question and previews the final question's content in full. The final open question then restates exactly that content ("Should the subspace convention be extended beyond text and links, what must the operation guarantee so that the kind-list remains fixed and the report stays comparable across documents of different vintages?"). This is two slots saying the same thing plus essay-content navigation in a structural slot — the forward-reference accretion the classifier targets.
**Required**: Delete the parenthetical. Let Q2 stand as the consumer-side question and the final item as the operation-side question; the reader does not need a map between them.

### Issue 2: W14 prose defers to an open question that re-defers back, triangulating the same topic across three locations
**ASN-0113, "Comparing reports across documents" (W14)**: "What a consumer must do when that provision fails — reports of differing vintages whose kind-lists may themselves differ — is the subject of an open question below."
**Problem**: This forward pointer defers the cross-vintage case from W14's prose to Q2; Q2 then back-references the final open question (Issue 1). Three passages in different sections circle the same unresolved topic, each pointing at another. Per the flagged pattern ("multiple paragraphs in different sections defer to the same downstream location"), the deferral chain is noise the reader must trace.
**Required**: Drop the forward-pointer sentence from W14. The claim that per-kind comparison is well-defined "provided both reports range over the same kind-list" already names the precondition; the failure case lives in the Open Questions section without needing to be announced from inside W14.

## OUT_OF_SCOPE

(none — the open questions on version forks, transclusion, and the single-overall-extent relationship are forward-looking deferrals appropriate to future ASNs, not claims defined in this note.)

VERDICT: REVISE
