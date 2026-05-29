# Channel Assignment — ASN-0036 review-118

**Date:** 2026-05-28 21:03

## Issue 1: S1 says the same thing twice
Reason: Pure editorial deduplication — the fix removes one of two sentences that both state S1 is the domain conjunct of S0. No design intent or implementation evidence is needed; the surviving sentence is already in the ASN.

## Issue 2: S5 previews and forward-references its own proof
Reason: Deleting a preview sentence and a forward-pointer to the proof that follows is purely structural; the proof body already discharges both constructions. Derivable from the ASN alone.

## Issue 3: Definition Depends clauses end with redundant use-site inventories
Reason: Removing two trailing sentences that restate their own Depends lists is internal cleanup; nothing about design or implementation is in question.

## Issue 4: Text-subspace-only scoping is restated five-plus times
Reason: Consolidating a scoping caveat that is already encoded by the formal `V_1(d)`/`S = 1` bindings is an editorial trim. The text-subspace restriction itself is already settled in the ASN, so no channel is needed.

## Issue 5: S8-depth carries a forward-reference meta-sentence
Reason: Removing a sentence that only announces later results exist is internal; the later results cite their own preconditions. No external input required.

## Issue 6: S9 restates its own (non-)content
Reason: Trimming a triplicated characterization and an enumeration of guarantees not derived in this section is editorial. S9's non-content status is fixed by the ASN's own S0 corollary structure, so no design or implementation evidence is needed.
