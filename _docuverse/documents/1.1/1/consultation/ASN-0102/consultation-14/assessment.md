# Channel Assignment — ASN-0102 review-14

**Date:** 2026-06-03 14:44

## Issue 1: The symbol `p` is overloaded with two distinct meanings
Reason: Pure notational disambiguation — renaming the reference count vs. insertion-position component and auditing every occurrence is entirely internal to the ASN; no design intent or implementation evidence bears on a symbol choice.

## Issue 2: X10's name and table summary overstate the guarantee for the self-source case
Reason: The body already states the correctly scoped claim (`d' ≠ d` non-interference plus snapshot resolution for `d_s = d`); aligning the name and table entry to the body is internal bookkeeping requiring no external channel.

## Issue 3: `wp(COPY, S3★)` is called a "biconditional" but is a universal membership condition
Reason: The displayed formula and surrounding proof are already correct; only the descriptive word is wrong, so the fix is a self-contained wording correction derivable from the ASN's own reasoning.
