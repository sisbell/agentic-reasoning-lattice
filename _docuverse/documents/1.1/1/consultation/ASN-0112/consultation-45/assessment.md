# Channel Assignment — ASN-0112 review-45

**Date:** 2026-06-08 12:21

## Issue 1: V18's "two transitions" dichotomy omits the emptiness transitions
Reason: Internal fix. The partition is already governed by the ASN's own claims — V11 handles the to-empty/from-empty transitions, V18 the migrations-between-defined-origins. Scoping V18 to defined-origin migrations (or adding the emptiness rows) is a logical correction derivable from V8/V11/V18 as written; no design intent or implementation evidence is at issue.

## Issue 2: Defensive meta-prose in the "Implementation conformance" remark on V2
Reason: Internal fix. Pure prose trim — drop the "theorem … merely conforms" framing and keep the conformance observation, which already cites consultation Q18. The load-bearing evidence is present in the ASN; no new question to either channel.

## Issue 3: V14 defends a case its own carrier already excludes
Reason: Internal fix. Removing a defensive sentence about positions excluded by V14's own `O(d)` quantifier is an editorial deletion; the quantifier and V6 are already in the ASN.

## Issue 4: V14's "The split is forced" justifies the citation rather than the claim
Reason: Internal fix. Deleting the meta-justification leaves the two-clause statement (content→`dom(C)` by S0/P0; link→`dom(L)` by L12) intact, all citations already present in the ASN.
