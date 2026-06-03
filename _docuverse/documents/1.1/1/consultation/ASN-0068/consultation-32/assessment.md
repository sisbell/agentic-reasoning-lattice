# Channel Assignment — ASN-0068 review-32

**Date:** 2026-06-03 00:10

## Issue 1: Trivial exhaustiveness prose duplicated in CV-SELF claim and justification
Reason: Purely editorial deduplication — removing a trivially-true parenthetical and a restated closing sentence. The `D ∪ X` decomposition and its case-discriminator are already fully present in the claim; no design intent or implementation evidence bears on the wording.

## Issue 2: CV-PRED's closing "convention" restates the left-maximality disjunct
Reason: The fix is a deletion justified entirely by internal redundancy — the existence clause plus the Left-maximal disjunction already carry the fact. No external channel is needed to confirm a self-contained restatement.

## Issue 3: CV-PRED "Dual inverse" clause has no use site
Reason: Whether `(v + j) − j = v` is invoked anywhere is a question about this ASN's own proofs and examples, which are all present in the text. Checking for a use site is internal; no Nelson or Gregory input required.
