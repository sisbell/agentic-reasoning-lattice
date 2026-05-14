# Channel Assignment — ASN-0042 review-31

**Date:** 2026-05-14 01:14

## Issue 1: O10 trajectory uses arithmetically incorrect baptism semantics
Reason: TA5(d) from ASN-0034 already fixes `inc(t, 2) = t.0.1` (terminal value always `1`), and TA5(c) gives sibling increment semantics. The fix is a mathematical reconstruction of the trajectory using these already-cited postconditions — fully internal to the ASN.

## Issue 2: O10 step count k = 3 - zeros(pfx(π)) is incorrect for u > 1
Reason: The corrected step count follows directly from the trajectory rebuild in Issue 1, distinguishing field-descending `inc(·, 2)` from lateral `inc(·, 0)` steps — both operations have postconditions already cited from ASN-0034.

## Issue 3: O10 does not address baptismal sequencing when sub-delegate domains contain intermediate siblings
Reason: The proof depends on ASN-0040's `next(B, p, d)` semantics — specifically whether the allocator forces sequential sibling generation or permits skipping. Gregory's implementation evidence determines which of the review's options (a/b/c) is required.
Gregory question: Does the udanax-green allocator's `next(B, p, d)` operation require all preceding sibling values `1, 2, ..., u-1` to be baptized before `u` can be produced at a given (parent, depth), or can it baptize `u` independently of intermediate siblings?

## Issue 4: O10's "u-selection" assumes the sub-delegate set is fully known but doesn't ground baptismal authority for intermediates
Reason: Same baptism-mechanism question as Issue 3 — whether `π` can reach a non-colliding sub-position without traversing sub-delegate-owned intermediates depends on the allocator's sequencing behavior. One Gregory consultation resolves both.
Gregory question: When a principal `π` requests baptism of a sub-account position and the lower-numbered siblings under `pfx(π)` have been delegated to other principals (so are not in `π`'s effective ownership), what does `docreatenewdocument`/`getnewtumbler` do — proceed to the next available value, fail, or require those sub-delegates' participation?
