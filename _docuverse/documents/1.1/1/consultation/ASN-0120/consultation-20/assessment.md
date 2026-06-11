# Channel Assignment — ASN-0120 review-20

**Date:** 2026-06-11 05:01

## Issue 1: "never exact equality" fails at the empty-resolution boundary
Reason: The fix is internal — the boundary case follows directly from the ASN's own definitions (`wf` admits specs capturing no active position, the span-shape clause forces `e_j = ∅` when `ρ = ∅`, and `coverage(∅) = ∅`). Adding the qualifier and stating the boundary explicitly requires no design intent or implementation evidence.

## Issue 2: ML4's coverage description contradicts the ASN's own coverage/store-trace distinction
Reason: The fix is internal — the correct statement (resolved sets are finite subsets of `dom(Σ.C)` with no constraint relating them to `d`) is already established by ML1's recovery equation and the post-ML6 restriction paragraph; the issue is a self-contradiction to be resolved in favor of content the ASN already proves.

## Issue 3: the degenerate one-sided-link sentence is incoherent and pre-empts Open Question 1
Reason: Deleting is internal, but choosing between deletion and a corrected replacement depends on whether the design actually specifies a one-sided link convention — the sentence appears to paraphrase a Nelson claim, and getting the slot/role assignment right requires his intent. No implementation evidence is needed since the connection-semantics stays deferred to Open Question 1 either way.
Nelson question: When a link is one-sided — there is no meaningful second region — does the design specify which endset slot (from or to) is populated and which is left empty, or is the one-sided case not a designed configuration at all?
