# Channel Assignment — ASN-0042 review-87

**Date:** 2026-05-30 00:47

## Issue 1: Covering-chain lemma carries a use-site inventory instead of advancing the lemma
Reason: Purely structural deletion of a pre-enumeration paragraph; the general lemma and its downstream instantiations are already present in the ASN, so no design intent or implementation evidence is needed.

## Issue 2: O7(c) proof re-opens conditions it has just discharged
Reason: The Formal Contract for (c) already encodes the conditional cleanly; the fix removes proof-body scenarios redundant with that wording, derivable entirely from the ASN's own text.

## Issue 3: Trust-boundary claim stated twice in identical force
Reason: Deduplication of a proposition stated identically in two sections; the `validaccount` observation it rests on is already present, so the fix is internal.

## Issue 4: Triplicated boilerplate across the three Delegation preservation paragraphs
Reason: Factoring a verbatim-repeated induction scaffold into a single statement; the per-invariant discharges (conditions iv, v, length-contradiction) are all already in the ASN.
