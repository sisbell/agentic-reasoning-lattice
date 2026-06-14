# Review of ASN-0131

This note is mathematically sound. I checked the inline proofs (RE-NCD's prefix-agreement argument, RE-ADDR's antichain argument, RE-RET's forward/backward directions, RE-UDIST-∩'s injective and non-injective counterexamples and its necessary-and-sufficient condition, the RE-CWP boundary collapse, and the worked instance) and found no logical errors. Depth is adequate: a concrete worked instance exercises the postconditions, and RE-CWP/RE-RET supply non-trivial weakest-precondition analyses.

The findings are all of the kind the `review-mode.anti-bloat` classifier targets: meta-prose accretion around forward references, use-site inventories, and essay content in structural slots.

## REVISE

### Issue 1: The `RE_clip` alternative operation is forward-reference accretion around Open Question 1
**ASN-0131, §Extent and §Composing regions**: The note materializes a full second operation — the selector `clip_W(e)` and the operation `RE_clip(W, d, Σ)` — and carries it through two sections, four claim-table entries, and Open Question 1.
**Problem**: The note has *adopted* whole-endset surfacing (RE-WHOLE). It then spends most of §Extent and a counterexample-laden block of §Composing regions building out the rejected alternative and threading it to OQ1: "That choice — RE-DEF's return value or `RE_clip`'s — is exactly what Open Question 1 reopens"; "a consideration bearing on Open Question 1 that the algebra makes sharp, and a more decisive one than §Extent's faithfulness appeal." This last sentence is pure argument-ranking — it compares two arguments for the same already-made decision and grades one "more decisive." A reader following "what does RE return at a touching slot?" must process an entire alternative operation and its composition-failure proofs to learn the answer is "the whole endset (provisionally)." This is the named pattern "multiple paragraphs in different sections defer to the same downstream location": OQ1 is deferred to from §Extent (twice), §Composing regions (twice), and the RE-WHOLE / RE-UDIST / RE-UDIST-∩ table entries.
**Required**: Keep RE-WHOLE as the adopted convention and state in one sentence that the touching-spans reading would forfeit RE-UDIST (its return value is region-dependent), with the choice left to OQ1. The concrete counterexamples may stay (they are examples, not meta-prose), but `RE_clip` should not be carried as a co-equal named operation, and the argument-ranking ("more decisive than §Extent's faithfulness appeal") should go. RE-UDIST and RE-UDIST-∩ are real claims about `RE` and stand without the rejected-reading foil.

### Issue 2: RE-NCD's claim entry carries a use-site inventory
**ASN-0131, Claims table, RE-NCD**: "...Cited by the worked instance (type endset `e₃`, `s_type`) and the retraction analysis (withdrawal to-set, `ℓ`, `s_L`)."
**Problem**: This is exactly the flagged pattern — a definition's entry enumerating its downstream consumers rather than advancing the claim's meaning. The places that use RE-NCD already cite it at the point of use; the table does not need to inventory them.
**Required**: Delete the "Cited by..." clause.

### Issue 3: Claims-table entries have grown essay tails
**ASN-0131, Claims table, RE-UDIST-∩ / RE-EDIT / RE-RET**: The RE-UDIST-∩ cell is a full paragraph — counterexample descriptions, the necessary-and-sufficient condition, an OQ4 deferral ("its weakest structurally-restricted sufficient form is Open Question 4"), and the reading-dependence note. RE-EDIT crams the entire stability theorem (every transition kind, the conservative-lift assumption, the link-subspace-confined cases) into one cell; RE-RET packs all its conditions and the sole-bearer iff into another.
**Problem**: Essay content in a structural slot. The table is supposed to be a one-line index of each claim; these cells reproduce the section prose, so the reader gains nothing by consulting the table over the body, and the OQ4/OQ1 deferrals compound the cross-reference threading of Issue 1.
**Required**: Reduce each cell to the claim statement plus its status, moving the case analysis, counterexample narration, and OQ deferrals to the proving sections (where most already appear).

### Issue 4: Redundant "two senses of permanence" recap
**ASN-0131, §Stability, "Under retraction"**: "Two senses of permanence must therefore be kept apart. The *specific retracted link's* membership in `addressable` is gone forever... But the *pair value* `(i, e)` is not permanently gone..."
**Problem**: This paragraph restates the distinction the preceding paragraph already established (the "sole addressable bearer" iff and the `ℓ₁`/`ℓ₂` worked-instance recap), in different words — the named pattern "two paragraphs in the same document say the same thing." Its only new content is the citation of R6c (restoration by re-emission).
**Required**: Fold the R6c point (an identical pair value re-enters when any live link bears `e` and touches) into the preceding paragraph and drop the recap.

## OUT_OF_SCOPE

The seven Open Questions correctly defer their topics (touching-spans reading, multiplicity preservation, V-rendered answers, the weakest structural sufficient condition for intersection-equality, non-co-resident link stores, type-slot/content matches, link-subspace regions) to future work. No new out-of-scope topic is needed; the issue is that OQ1 in particular is over-elaborated in the body (Issue 1), not that it is wrongly raised.

VERDICT: REVISE
