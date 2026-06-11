# Channel Assignment — ASN-0128 review-10

**Date:** 2026-06-11 01:53

## Issue 1: I0a is a named lemma with no block of its own, inside a definition grown into an essay
Reason: Pure restructuring — the proof is correct and complete in the ASN; extracting I0a into a labeled block and deduplicating the `t`/`t.x` example requires no new design intent or implementation evidence.

## Issue 2: The wrapper's both-branches-read-`d_retr` rationale is stated verbatim twice
Reason: Deletion of a duplicated sentence with a pointer left behind; the surviving DR statement already carries the full content. Internal fix.

## Issue 3: The RP-c trailing paragraph justifies the design instead of stating the claim, and duplicates I1
Reason: The commitment is already stated operationally in I1 and the commitments bullet; cutting the counterfactual paragraph and one R-VAL restatement is editorial consolidation of existing content. Internal fix.

## Issue 4: I6 and DR each announce the same Case-1/Case-2 correspondence, deferring to each other; DR narrates the review process
Reason: Choosing one home for the correspondence sentence and deleting the review-trail clause is derivable from the ASN's own structure; the technical dependency (I6's reduction on DR's C3 vacuity) is already stated. Internal fix.

## Issue 5: The reach-withholding rationale appears in full twice; the adjudication-to-the-reader point three times
Reason: Both rationales are fully stated in the ASN; the fix is selecting canonical sites and replacing the duplicates with citations. Internal fix.

## Issue 6: `stale(h)` compares ages denominated in different homes' traffic, and the consequence is unstated
Reason: The fix requires a committed design choice between home-relative expiry and per-home parameterization, and the right choice turns on whether any cross-document arrival ordering is actually recoverable from the implementation's structural state — evidence only Gregory can supply; the ASN's state model rules out a clock but not the question of what ordering the implementation itself preserves.
Gregory question: Does udanax-green preserve any global, cross-document ordering of link/event creation (a system-wide counter, log order, or granfilade structure recoverable at query time), or is arrival order recoverable only within a single document's link chain?
