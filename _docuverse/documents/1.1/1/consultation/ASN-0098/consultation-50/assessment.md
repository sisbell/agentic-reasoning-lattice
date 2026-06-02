# Channel Assignment — ASN-0098 review-50

**Date:** 2026-06-02 16:07

## Issue 1: Redundant back-pointer parenthetical for LP14
Reason: Pure deletion of a cross-reference; the ASN already establishes LP14 in the arrangement-fixing template paragraph. No external channel needed.

## Issue 2: LP13 trailing paragraph restates its own proof conclusion
Reason: Editorial fold — merge the one new clause (holder reliance + LP9–LP11 pointer) into the proof's closing sentence. All content is already present in the ASN.

## Issue 3: "Remark on K.δ" is a use-site inventory
Reason: Editorial removal/relocation of a coverage roster; the K.δ sub-case framing is already internal to the ASN's LP4/LP8 discussion.

## Issue 4: Achievability argument uses chain contiguity without citing it
Reason: The fix asserts that "index ≤ m ⟹ allocated" because allocated addresses form a contiguous initial chain segment — this is a gap-freeness property of the allocator that must be confirmed as ChainMembershipForOrigin's actual conclusion (the implementation evidence), not merely chain membership.
Gregory question: Does the allocator guarantee that the set of emitted chain indices for a given origin sub-allocator is always a contiguous initial segment {1, …, m} with no gaps, so that m being the allocated maximum entails 1..m all allocated?
