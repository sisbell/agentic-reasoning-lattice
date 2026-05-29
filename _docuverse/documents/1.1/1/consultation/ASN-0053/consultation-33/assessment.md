# Channel Assignment — ASN-0053 review-33

**Date:** 2026-05-28 19:56

## Issue 1: WF introduced by its use-sites, not its meaning
Reason: Pure editorial deletion of a framing sentence; the lemma statement and proof are already self-contained. No design intent or implementation evidence needed.

## Issue 2: The a = b "degenerate case" is excluded and never handled
Reason: TA-strict on T12 already guarantees start(σ) < reach(σ) for every span, so a = b never arises — the fix follows from the ASN's own carrier precondition.

## Issue 3: Forward defer to S9 inside the S8 construction
Reason: S8's existence claim needs only N1/N2 and denotation equality, both proven internally; removing the S9 pointer is derivable from the ASN's own proof structure.

## Issue 4: Defensive justification of a notation choice in S7
Reason: The one-span-per-position construction already establishes |Σ| = |P|; deleting the defensive meta-commentary requires nothing beyond the existing proof.
