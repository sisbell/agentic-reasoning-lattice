# Channel Assignment — ASN-0043 review-160

**Date:** 2026-05-31 01:20

## Issue 1: L9's formal statement drops the conformance conjunct that its prose, its proof, and its sibling lemma L11b all carry
Reason: Internal. The fix mechanically copies the conformance conjunct already present in L9's prose, its proof ("By FSP, `Σ'` satisfies every state-local L- and S-invariant"), and L11b's existential body into L9's formal statement. No design intent or implementation evidence is in question.

## Issue 2: L7 worked-example "illustration" is essay content in a verification slot, restating the body
Reason: Internal. Deleting or reducing a non-checkable illustration that restates the body's L7 is an editorial decision derivable from the ASN's own structure; no external evidence bears on it.

## Issue 3: Coverage's lossy-projection note duplicates what Step 6 establishes, with a back-reference closing the loop
Reason: Internal. Trimming the Coverage definition to the bare lossy-projection sentence while Step 6 carries the demonstration is a deduplication within this ASN's own content; neither channel is implicated.
