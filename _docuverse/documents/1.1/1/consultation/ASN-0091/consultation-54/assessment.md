# Channel Assignment — ASN-0091 review-54

**Date:** 2026-06-03 23:58

## Issue 1: The collapse/non-trivial case split is stated three times in different words
Reason: Pure prose-deduplication; the case split, the S5 witness, and the realiser selection are all already present in the ASN. Consolidating restatements requires no design intent or implementation evidence.

## Issue 2: Duplicate frame-inherited invariant inventory
Reason: Both enumerations are already in the ASN; the fix is to keep one and have the Worked Example cite it. No external channel needed.

## Issue 3: Prose-and-table redundancy in clause correspondence
Reason: The RA-reg discharge appears in both prose and table within the ASN; choosing one form is an internal editorial decision derivable from existing content.

## Issue 4: Essay-flavored parenthetical restating RE-origin
Reason: The parenthetical restates the preceding sentence's established content; deletion is purely internal with no dependency on design intent or code.
