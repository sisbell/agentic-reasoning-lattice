# Channel Assignment — ASN-0111 review-11

**Date:** 2026-06-07 23:48

## Issue 1: Two "Open Questions" restate guarantees the ASN already proves
Reason: The diagnosis (Q2 = RL7's `readlink(a, Σ') = readlink(a, Σ)`; Q3 answered "never" via L12 immutability plus the combinatorial nature of `coverage`) is established entirely within this ASN's own proofs. Removing the two questions, or replacing them with the forward-looking concerns RL7/RL8/immutability do *not* settle, is derivable from the ASN's existing content.

## Issue 2: The `N > 3` case of RL2 is verified only hypothetically
Reason: The clean fix is the reviewer's second branch — state that the arity-3 instance stands in for the general case because RL1/RL2's componentwise equality is arity-agnostic — which is fully internal. A concrete `N = 4` instance would instead need confirmation that arity-4 links are reachable, since the ASN itself says udanax-green caps links at three endsets, making the standing-precondition legitimacy of such an instance an implementation question.
Gregory question: Does udanax-green permit a link to carry more than three endsets, or is the three-endset cap enforced such that no reachable state contains an `N > 3` link?
