# Revision Categorization — ASN-0027 review-2

**Date:** 2026-03-10 09:46

## Issue 1: A6 concrete example makes a false claim about COPY restoring identity
Category: INTERNAL
Reason: The formal proof of A6 is correct; the error is in the illustrative paragraph that misapplies COPY after INSERT instead of after DELETE alone. The fix requires only rearranging or correcting the example using A2, A4, and A7 already defined in the ASN.

## Issue 2: A3 precondition specifies no operation parameters
Category: GREGORY
Reason: The ASN already cites Gregory's evidence about REARRANGE's mechanism (modifying V-displacements) but lacks the operation's input signature. The implementation determines whether REARRANGE takes a cut-and-paste spec `(d, p_from, k, p_to)`, a full permutation, or another form.
Gregory question: What parameters does the rearrange operation accept in udanax-green — does it take a source position, width, and destination position (cut-and-paste), or some other input form?

## Issue 3: A7 claims full document restoration without derivation
Category: INTERNAL
Reason: The three-step derivation (left frame, right frame, length) uses only A2 and A4 properties already stated in the ASN. The review itself sketches the complete proof; the fix is adding it to the text.
