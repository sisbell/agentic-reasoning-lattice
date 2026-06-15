# Channel Assignment — ASN-0134 review-55

**Date:** 2026-06-14 19:48

## Issue 1: A2's zero-step linearization clause is not reconciled with multi-access reads
Reason: Internal. The three pieces in tension (A1's classing of `stale` as one zero-step op, A2's single-index clause, §8's `N+1`-access finding) are all already in the note, and V0/V2 already supply the single-vs-multi-access distinction the fix needs; restricting A2 and pointing multi-access reads to V0/V2 uses only the note's own content.

## Issue 2: The §3 lead-in re-derives all of G0 before G0 states it
Reason: Internal. Pure deduplication — the lead-in previews claims G0 states in full immediately below; trimming it to the pipelining-client definition plus a pointer is editorial and needs nothing external.

## Issue 3: "A critical section buys only contiguity, not atomicity" is argued in both §1 and §6
Reason: Internal. The same conclusion is established at A5 (§1) and W2 (§6); choosing one carrier and citing it from the other is a structural consolidation derivable from the note alone.

## Issue 4: MIC clauses re-argue their source claims' justifications rather than invoking them
Reason: Internal. Clauses 4 and 6 reproduce V0's and V2's rationale verbatim; reducing them to obligation-plus-citation relocates existing text and requires no design or implementation input.

## Issue 5: The model-intrinsic-contiguity derivation appears in both A6's final paragraph and W1
Reason: Internal. A6 already proves hole-impossibility via `inc(max,·)`/`C0`/`L12`/cross-home framing; having W1 invoke A6 and keep only its collision-not-hole and uniqueness-not-contiguity content is an internal cite-don't-restate edit.

## Issue 6: §4 instance (i)'s `age` paragraph routes through an excluded case to reach a consequence no clause consumes
Reason: Internal. The facts in play (BH4's `idem = ⊥` precondition, `age` denominated in home link traffic) are ASN-0128 content already cited, and the note itself states instance (i)'s load-bearing conclusion is the surviving `idem=⊤` duplicate motivating clause 7; cutting the dead-end digression needs no further evidence.
