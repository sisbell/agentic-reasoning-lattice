# Channel Assignment — ASN-0086 review-121

**Date:** 2026-05-31 23:16

## Issue 1: The K.λ first/subsequent emission rule is restated in full at five sites
Reason: Purely editorial restructuring — introduce `a_emit(Σ, d)` once in Allocator Structure and reference it. The rule's content is already fully specified in the ASN (inherited from ASN-0093's K.λ contract); no design intent or implementation evidence is needed to relocate a definition.

## Issue 2: R0a-Cor2's statement forward-references a Worked-Sketch object that does not yet exist
Reason: The fix substitutes an in-scope expression (`E(t_1) = [s_L, 1]`, already used in R0a-Cor2's own proof) or drops the parenthetical. Entirely internal to the note.

## Issue 3: Meta-prose justifying why prose/hypotheses are present
Reason: Both sentences are removable bookkeeping; the underlying facts (local-antichain weakening, conformance load-bearingness) are already demonstrated elsewhere in the ASN via counterexample. Deletion/compression needs nothing external.

## Issue 4: R6b's formal statement carries an unused antecedent conjunct
Reason: The proof itself states the fourth hypothesis is never consulted, so the three-hypothesis strength is derivable directly from the ASN's own proof; recasting the statement or adding a remark is a logical-form edit requiring no external channel.
