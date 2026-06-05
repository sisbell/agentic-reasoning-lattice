# Channel Assignment — ASN-0100 review-88

**Date:** 2026-06-05 06:18

## Issue 1: Citation to a nonexistent postcondition
Reason: The corrected reference (ValidFirstInsertionPosition's definition fixing `v = [s_C, 1, …, 1]`) is already stated within ASN-0100's own precondition discussion; swapping the spurious label for the definition is a self-contained edit.

## Issue 2: Redundant restatement of the uniqueness conclusion
Reason: Purely editorial — folding the duplicate Nelson-quote paragraph into the opening requires no external design intent or implementation evidence, only consolidating text already present.

## Issue 3: Implementation-mechanics tangent in an abstract verification slot
Reason: The abstract isolation property is already discharged by `INS.frame.subspace` in the same paragraph; removing the knife aside is internal, since the verification stands on the frame alone without implementation evidence.

## Issue 4: Forward-reference accretion in the worked example
Reason: Restructuring (deferring the INS.proj instantiation and dropping the imagined-`e_1'` case) is reorganization of content already in the ASN; no design intent or implementation fact is in question.
