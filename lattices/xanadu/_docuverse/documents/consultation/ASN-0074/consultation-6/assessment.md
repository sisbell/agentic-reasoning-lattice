# Revision Categorization — ASN-0074 review-6

**Date:** 2026-03-22 16:14



## Issue 1: C0a proof has an unacknowledged sequential dependency
Category: INTERNAL
Reason: The fix is purely proof-structural — the mathematical content is correct but the presentation incorrectly claims independence across j. Both proposed fixes (induction or smallest-counterexample) use only definitions and properties already present in the ASN.

## Issue 2: w(resolve(d_s, σ)) is a type mismatch in C2
Category: INTERNAL
Reason: This is a notational/definitional inconsistency within the ASN itself — w is defined on reference sequences but applied to I-address sequences. Both proposed fixes (redefine w on I-address sequences, or inline the sum in C2) require only rearranging definitions already present in the document.
