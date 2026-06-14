# Channel Assignment — ASN-0134 review-33

**Date:** 2026-06-14 08:37

## Issue 1: The nesting-homes justification for the origin argument is a red herring
Reason: Internal. The fix is a logical correction fully derivable from the ASN's own content — the zeros arithmetic (`zeros(d')=zeros(d)+zeros(x)=2 ⟹ zeros(x)=0 ⟹ x₁≠0`) and anchor structure are already in the ASN, and the review's own example shows nesting anchors are prefix-incomparable. The genuine reason to prefer origin (cross-subspace generality) is already stated in H1 and W1; nothing about design intent or implementation behavior is at issue.

## Issue 2: §9 MIC clauses and §5 W-claims re-derive their source claims instead of citing them
Reason: Internal. Pure structural deduplication — replacing re-derivations with citations to V0/V2/H1/H2/ChainMembershipForOrigin, all of which are already present in the ASN. No external evidence or intent is needed to collapse a restatement into "claim + delta."

## Issue 3: The literal-vs-operative `I1a` argument is developed three times
Reason: Internal. Editorial deduplication — the argument is fully developed in §4 instance (i) from ASN-0128 I1a; clause 8 and SAFE(b)(ii) need only assert the conclusion "by §4 instance (i)." No new reasoning, intent, or implementation fact is required.

## Issue 4: "regardless of home" is asserted at six sites
Reason: Internal. Accreted-emphasis cleanup — the same-home derivation (clause 2's `φ, φ+1` slot-spacing) lives at §4 instance (i); the remaining five sites become citations. Entirely within the ASN's own content.

## Issue 5: A1's rejection sub-list reads exhaustive but omits two causes
Reason: Internal. The recommended fix — mark the sub-list illustrative ("e.g.") or drop it — preserves the exhaustiveness of the five zero-step *cases* and requires no verification of the omitted causes; the supporting facts (ASN-0128 I6, P-reg) live in an already-cited dependency, not in the implementation or design intent.
