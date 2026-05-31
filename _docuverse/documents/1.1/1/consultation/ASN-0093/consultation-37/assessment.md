# Channel Assignment — ASN-0093 review-37

**Date:** 2026-05-31 07:34

## Issue 1: Definition enumerates downstream consumers
Reason: Pure editorial deletion of a use-site inventory clause; the state-independence fact and its consequence remain in the note and require no design intent or implementation evidence.

## Issue 2: C-fin restates a downstream use-site already established at K.α
Reason: Removing a duplicated well-definedness sentence already stated at K.α's precondition is internal bookkeeping derivable from the ASN's own text.

## Issue 3: Forward reference to the discharge matrix inside an invariant statement
Reason: Deleting a parenthetical pointer to a downstream section is purely editorial; the L14 derivation and its T7 dependency remain stated elsewhere in the note.

## Issue 4: L14 derivation restated a third time in the Cross-document section
Reason: Reducing or dropping a triplicated derivation is internal; L14's premises (L0 + SC-NEQ + T7) are already fixed in the invariant body and Properties table.

## Issue 5: ChainMembershipForOrigin enumerates which form downstream consumers will cite
Reason: Dropping the meta-prose clause while keeping the corollary is editorial; the corollary's content is self-contained within the lemma.

## Issue 6: Unexplained symbol in the Properties Introduced table
Reason: The cleanest fix is removing the undefined `E_doc` parenthetical, which is internal — but confirming whether `E_doc` was a genuine prior structural notion (vs. a typo) draws on the link-store model's history.
Gregory question: Does the udanax-green link allocator (or ASN-0043's link-store model it synthesizes) carry any `E_doc` notion distinct from `dom(M)` for scoping link home documents, or has document scope always been keyed on the arrangement-function domain?
