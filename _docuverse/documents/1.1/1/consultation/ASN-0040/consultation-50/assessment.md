# Channel Assignment — ASN-0040 review-50

**Date:** 2026-05-28 21:33

## Issue 1: Bop's preservation paragraphs duplicate the dedicated invariant proofs
Reason: Purely structural deduplication — §B1/§B10/§B_fin already carry the full inductive proofs, and the fix is to drop or one-line the restated Bop paragraphs. Derivable from the ASN's own layout.

## Issue 2: Bop FRAME duplicates the Formal Contract Frame line with a within-document pointer
Reason: Editorial removal of a redundant within-document pointer; both statements are present in the ASN and the fix is to state the frame once. No external channel needed.

## Issue 3: hwm "Justification" anticipates and duplicates B2
Reason: The hwm justification and B2's proof are adjacent and say the same thing; trimming to the maximum-identification claim is an internal text edit grounded in the ASN's own definitions.

## Issue 4: B1 sub-case C and B6 necessity sub-case (b) duplicate the (p′, 2) validity check
Reason: Both verifications already exist in the ASN with identical content; consolidating into B6 and citing from §B1 is an internal cross-reference fix requiring no design or implementation input.

## Issue 5: B0a closes with a restated partition / exhaustiveness claim
Reason: The opening sentence plus bullets already define and name both classes; deleting the redundant closing sentence is a self-contained editorial cut.

## Issue 6: The allocated-set aside duplicates an Open Question
Reason: The aside and the Open Question carry the same deferral; reducing the aside to its factual line is derivable from the ASN's own content without external channels.
