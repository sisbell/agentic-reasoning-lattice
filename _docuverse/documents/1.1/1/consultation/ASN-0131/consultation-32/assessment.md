# Channel Assignment — ASN-0131 review-32

**Date:** 2026-06-13 21:25

## Issue 1: Path-not-taken justification in the insert/delete paragraph
Reason: Pure anti-bloat prose trim. The load-bearing fact (insert/delete displace content through the region's fixed positions per I3/D-SHIFT, so the image of a fixed `W` swings and RE tracks it non-monotonically, with RE-IDENT holding spans fixed) is already stated in the note; the fix only removes the "not competing descriptions" reconciliation and the decomposition parenthetical. Derivable from the ASN alone — no channel needed.

## Issue 2: "Freshly inserted content" is not delivered by the cited displacement primitive
Reason: Internal consistency with a sibling formalization note. The reviewer has already established what ASN-0082's I3/D-SHIFT primitive delivers (I3-V vacates the gap, I3-CS leaves no slot for fresh content; displaced-in content from lower positions *is* delivered), and both offered remedies are checkable against that already-cited foundation. The choice between "acknowledge the composite" and "restrict the cited source" is a modeling/exposition decision the author can make against the lattice's own content, not a question of Nelson's design intent or udanax-green's behavior.
