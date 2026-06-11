# Channel Assignment — ASN-0128 review-16

**Date:** 2026-06-11 03:56

## Issue 1: S2 ships `supersedes` without fixing the direction convention its own tip-semantics depends on
Reason: The slot convention must be grounded in the design intent of the whole-document supersession metalink (LM 4/52–4/53), which the ASN already cites as the pattern's source — the choice between F=superseder and F=superseded is Nelson's to settle, not derivable from the note's own content. The example scenario and reconciliation prose are then internal.
Nelson question: In Literary Machines' whole-document supersession metalink (LM 4/52–4/53), which endpoint carries the newer (superseding) document and which the older (superseded) — i.e., does the link assert "this supersedes that" from new to old, or point from an old version toward its replacement?

## Issue 2: DR's closing scope characterization under-describes what surface-discipline excludes
Reason: The fix is internal — the review supplies the full counterexample construction, and both failure modes (RangeSterilization for range-G tuples, the spurious dedup hit against the self-emit branch) are derivable from machinery already in the ASN (I0/I1 dedup, P-tgt's disjuncts, FrontierUnification). Restating the exclusion as "any `L_R` tuple not wrapper-deposited" requires no design intent or implementation evidence.

## Issue 3: The C3-under-discipline fact is stated four times, twice in full
Reason: Purely editorial consolidation — moving the lemma's single statement and proof to DR and replacing the restatements in SD, I4, and I6 with citations changes no semantics and needs no external input.

## Issue 4: Duplicated normative sentences
Reason: Editorial de-duplication of facts whose normative homes (BH1's Rewrite scope, BH2's Effect) are already identified by the review; replacing restatements with citations is fully internal to the ASN.
