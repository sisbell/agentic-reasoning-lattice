# Channel Assignment — ASN-0036 review-131

**Date:** 2026-05-28 23:34

## Issue 1: The entire "V-position ordinal decomposition" section has no consumer in this ASN
Reason: The fix is a scoping decision — either wire the homomorphism machinery into an in-ASN consumer or remove it as premature infrastructure. Both options are resolvable from the ASN's own dependency structure (no claim here invokes `OrdAddHom`/`OrdShiftHom`; only Open Questions reference them). No design intent or implementation evidence is at stake.

## Issue 2: S8 proves only the trivial singleton decomposition; the run identity for n > 1 is never exercised
Reason: This is a proof/prose-honesty fix — either narrow the postcondition to the existence claim or construct a non-singleton run exercising conjunct (b) at k ≥ 1. The ASN already supplies the machinery (the worked example checks the displacement identity at k=3), so the fix is internal.

## Issue 3: Out-of-scope operations prose accreting in invariant sections
Reason: Pure trimming of operation-specific meta-prose (INSERT/DELETE/COPY/REARRANGE) back to the state-level invariants S3 and S9 already state. No external input needed to cut scope.

## Issue 4: S7 "two mechanisms for origin lookup" adds nothing to the abstract guarantee
Reason: The fix is to remove an implementation inventory the ASN itself disclaims as irrelevant to the abstract `origin(a)` claim; the prefix-encodes-origin point already corroborates S7a and is retained on the ASN's own terms. Editorial removal, derivable internally.

## Issue 5: subspace_I and subspace definitions carry redundant restatement
Reason: Purely internal cross-reference cleanup — point the projection definitions at S7c/S8a for positivity instead of re-deriving the same T0/T4/NAT chain. No external channel involved.
