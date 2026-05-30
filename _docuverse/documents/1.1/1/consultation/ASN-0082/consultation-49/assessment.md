# Channel Assignment — ASN-0082 review-49

**Date:** 2026-05-30 09:36

## Issue 1: D-SEQ-post cites D-SEP(b) for `|X| = c` outside D-SEP(b)'s stated precondition
Reason: Internal. The fix re-derives `|X| = c` from the containment precondition (`p₂ + w₂ − 1 ≤ N`) and pre-state D-SEQ (`V_1(d) = {[1,k] : 1 ≤ k ≤ N}`), both already stated in the ASN and both R-independent — no design intent or implementation evidence required.

## Issue 2: "mathematically forced" overstates the depth restriction
Reason: Internal. The ASN's own Open Question already concedes contraction may generalize past depth 1; scoping the claim to the TA4-based proof route is a self-contained rewording.

## Issue 3: NAT-CA introduction carries non-derivability essay (meta-prose around an axiom)
Reason: Internal. Stating commutativity/associativity of ℕ addition as a one-line carrier fact and dropping the model-theoretic narrative is pure prose trimming.

## Issue 4: I3-S and D-S close with duplicated summary prose
Reason: Internal. Consolidating two near-identical commutativity-with-shift summaries into one referenced statement is editorial deduplication.

## Issue 5: Meta-summary inventorying which clauses the worked examples "exercise"
Reason: Internal. Removing the exhaustiveness-inventory sentence and trimming the redundant second example to its one novel fact is prose cleanup against content already present.
