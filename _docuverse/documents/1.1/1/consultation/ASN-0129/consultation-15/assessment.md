# Channel Assignment — ASN-0129 review-15

**Date:** 2026-06-11 20:45

## Issue 1: The reserved symbol `S` is rebound twice after being globally declared
Reason: Pure notation hygiene — renaming PD2's type-set variable and PC6's `S_view` requires only consistent application of the note's own symbol reservation; no design intent or implementation fact bears on a variable name.

## Issue 2: The is_doc emit-surface provenance is stated three times; the PC5 instance is inert for the claim it decorates
Reason: Deduplication of an already-grounded fact — the full provenance stays at QD-audit and PC5's clause is trimmed to its termination-relevant content. The fix moves text, it does not need new evidence about what the emit surface does.

## Issue 3: Two sections close by deferring to C-reach; the PC6 pointer sentence carries no content
Reason: Deletion of a redundant forward pointer whose content is stated verbatim at C-reach. The fix is settled by the ASN's own cross-reference structure; neither channel is implicated.

## Issue 4: QD-audit buries a second topic inside a nested parenthetical of a ~110-word sentence
Reason: Sentence restructuring — the P-tgt accounting is already complete and correct in the ASN; the fix only promotes it from a nested parenthetical to its own sentence, with the review supplying the replacement text.
