# Channel Assignment — ASN-0069 review-40

**Date:** 2026-05-27 15:56

## Issue 1: V4's introduction wording conflates design commitment with derivation
Reason: The fix is purely an editorial reordering — the ASN already acknowledges V4's design-commitment status explicitly later in the same section. No external channel adds information; the revision just moves existing text forward or rewords the introduction.

## Issue 2: V11 does not explicitly state that k ≥ 1
Reason: The fix is a formalism repair derivable from V11's own proof structure (the base case is k = 1, and the "step 0's post-state denotes Σ" convention applies only for k ≥ 1). Adding the explicit quantifier constraint requires no design or implementation evidence.

## Issue 3: V11a's "sibling-stream index" phrasing is ambiguous
Reason: The math is acknowledged correct in either interpretation; the fix is to either pick an indexing convention (resolvable by reading ASN-0034's T10a directly) or rephrase constructively via the inc(·, 0) operation. Neither design intent nor implementation evidence is needed — the foundation ASN content is directly accessible to the reviser.
