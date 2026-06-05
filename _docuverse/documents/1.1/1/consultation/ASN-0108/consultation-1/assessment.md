# Channel Assignment — ASN-0108 review-1

**Date:** 2026-06-04 20:06

## Issue 1: The content-position key violates the injectivity that W0 and W1 require
Reason: The logical contradiction is internal, but accurately correcting the "satisfies W0–W5" claim depends on whether the udanax-green insertion-sort actually breaks ties by link address or leaves equal-boundary matches tied — that is implementation evidence.
Gregory question: When the insertion-sort builds the result list, does it break ties between two links matching the same content-endpoint boundary (e.g. by link address), or can two distinct links land at the same sort position?

## Issue 2: W5's necessity claim ("only if state-stable") is too strong
Reason: The correction follows from the ASN's own model — `After` uses `κ(c)` recomputed at Σ', so only relative-order preservation among survivors is necessary while absolute invariance is sufficient. Fully derivable internally.

## Issue 3: W9's exhaustion signal is stated unconditionally but W8 identifies a counterexample
Reason: This is an internal inconsistency between W8 and W9; conditioning W9 on cursor-key recoverability with a cross-reference to W8 resolves it using only the ASN's content.

## Issue 4: No concrete worked example, and W4's termination clause misdescribes the non-divisible case
Reason: The worked examples and the termination-clause correction are pure arithmetic against the ASN's own definitions and W9a formula. No external evidence needed.

## Issue 5: W6's biconditional asserts a backward direction it does not justify
Reason: The ASN only uses and only argues the forward direction; deciding to weaken to that implication (or scope the quantifiers) is a logical fix internal to the note.
