# Channel Assignment — ASN-0084 review-63

**Date:** 2026-05-30 14:16

## Issue 1: R-SP lemma duplicates the "Invariant preservation" audit; the wp claim is trivial
Reason: Derivable from the ASN alone — whether R-PRE(iv)'s bound on ord(c_{n−1}) is load-bearing is a mathematical question answerable from the definitions, postconditions, and D-SEQ already present in the document.

## Issue 2: Four sections defer to the same "Foundation-S8 transport" step
Reason: Pure structural deduplication — consolidating where post-state S8 is consumed is an editorial decision internal to the document, requiring no design-intent or implementation evidence.

## Issue 3: ℕ-addition cancellation is derived through shift lemmas where the NAT axioms suffice
Reason: Derivable from the foundation the ASN already cites — NAT-order and NAT-addcompat are formal axioms of ASN-0034, not facts about Nelson's design intent or the udanax-green implementation, so the substitution is internal.

## Issue 4: Forward-reference framing around "Width positivity"
Reason: Pure prose/structure cleanup — removing meta-justification and redundant forward pointers requires no external channel.
