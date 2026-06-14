# Channel Assignment — ASN-0133 review-27

**Date:** 2026-06-14 04:28

## Issue 1: Q0's heterogeneous-view rewrite is asserted but never exercised
Reason: The fix instantiates machinery the note already imports and describes in full — UV's default-view rewrite, PC3's fixed-view-base rebuild equations, and PC4 value-preservation, all cited from ASN-0129 — on a concrete two-rule registry, with value-preservation following from UV being a semantics-preserving rewrite. It is a self-contained exercise of cited results; the collections' view behavior (`stale`/`chain` filtered at default) is already committed via ASN-0129 and accepted by the reviewer, so no design intent or fresh implementation evidence is required.

## Issue 2: the pdef-trigger "link vs decidability" contrast is illusory
Reason: The fix is a reframing grounded in ASN-0130's lemma structure (PR3a delivering `expand(a) ∈ PL` under PR-DISC, via PR2 acyclicity), which the reviewer has already laid out and which lives in a dependency ASN — corpus-formal content owned by neither Nelson (design intent) nor Gregory (udanax-green C, where `register_pred`/`expand` do not exist). ASN-0133 already cites PR-DISC and how it is discharged, so the correction is derivable from content in hand.

## Issue 3: the H-RF / H-W / Q5a relationship is re-litigated section after section
Reason: Pure consolidation of a separation the note already establishes in four places into one statement (at H-RF) plus cross-references; entirely internal, no external fact needed.

## Issue 4: the H-SFAIR regime-form reduction is derived twice
Reason: De-duplication of a derivation already present in the note — derive once under H-SFAIR, have Q6 invoke the named result; entirely internal.

## Issue 5: defensive framing and forward-reference inventories in structural slots
Reason: Prose cleanup — the underlying distinctions (Q3's general-meta-level vs marker-pattern-effective; Q5a's open-model strict-strengthening) are already stated in the note, so the fix only removes scaffolding and the intro's Q3 preview, requiring no external input.
