# Channel Assignment — ASN-0042 review-115

**Date:** 2026-05-30 04:32

## Issue 1: O1a's boxed statement omits the reachable-state quantification that O1b carries
Reason: Pure notational alignment — the ASN's own proof already establishes O1a as a reachable-state invariant (base O14(iii), delegate condition (iii)) and every citation reads it that way; restating the boxed formula to match O1b is derivable from the ASN alone.

## Issue 2: The shared-induction bookkeeping is described three times
Reason: Internal deduplication of proof-management prose; the induction structure and per-invariant delegation-step split are all present in the ASN, so consolidating to one statement plus one-line discharges needs no external input.

## Issue 3: O10(c) prose is defensive justification plus forward-deferral, not derivation
Reason: The load-bearing zero-count derivation (B5a, `inc` field-opening) already lives in the construction; deleting the strategy-justification and namespace-essay sentences is a self-contained edit derivable from the ASN.

## Issue 4: Repeated full parenthetical re-citation of the covering-chain lemma
Reason: Citation-style cleanup — the lemma is named and proved in-document, so shortening later references is purely internal.
