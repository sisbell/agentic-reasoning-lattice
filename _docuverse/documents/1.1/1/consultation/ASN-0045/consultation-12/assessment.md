# Channel Assignment — ASN-0045 review-12

**Date:** 2026-05-28 19:41

## Issue 1: Partition's Depends omits NAT-closure, which its proof uses directly
Reason: Neither channel is needed. The fix is a citation-consistency correction fully derivable from the ASN itself — the Well-Definedness prose already invokes NAT-closure (`0 + 1`, `m + 1`, `2 := 1 + 1`, `3 := 2 + 1`), so adding it to Partition's Depends is a mechanical alignment of the formal slot with the proof text.

## Issue 2: Document and Element over-attribute NAT-addcompat to the predicate
Reason: Neither channel is needed. The fix follows from the ASN's own definitions — each predicate's sole postcondition is the biconditional `⟺ T4-valid(t) ∧ zeros(t) = k`, whose statement needs only the numeral's existence (NAT-closure), while numeral distinctness (NAT-addcompat) is consumed exclusively by Partition's at-most-one argument, as the annotation itself concedes.
