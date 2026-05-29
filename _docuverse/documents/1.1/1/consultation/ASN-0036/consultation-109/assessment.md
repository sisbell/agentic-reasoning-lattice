# Channel Assignment — ASN-0036 review-109

**Date:** 2026-05-28 19:27

## Issue 1: Cited foundation lemmas absent from the foundation
Reason: The fix is internal. The foundation extract lists exactly five ℕ axioms (NAT-addcompat, NAT-closure, NAT-discrete, NAT-order, NAT-wellorder); whether NAT-sub/NAT-cancel/NAT-zero are real ASN-0034 claims is a foundation-document question, but the ASN can resolve it itself by rederiving the position-arithmetic and injection steps from the five available axioms already cited.

## Issue 2: Use-site inventories around definition promotions
Reason: Internal editorial fix — delete the consumer enumerations; no design intent or implementation evidence is involved.

## Issue 3: Prose justifying document ordering / non-circularity
Reason: Internal — the non-circularity is already encoded in the Depends dependency graph; removing the defensive narrative requires no external channel.

## Issue 4: Depends fields duplicate proof-body arithmetic verbatim
Reason: Internal editorial condensation; the arithmetic is already present in the proof body and the Depends entries need only name the cited claim and its role.

## Issue 5: Multiple paragraphs deferring to the same downstream location
Reason: Internal restructuring — state the subspace-preservation fact once at ShiftPreservation and replace the three framing paragraphs with bare citations; no external input needed.

## Issue 6: Reindexing bookkeeping in the S8 corollary
Reason: Internal editorial — renumber the conclusions inline and delete the index-correspondence bookkeeping.

## Issue 7: S5 Frame is a defensive scope essay
Reason: Internal — the scope reduction to a single sentence follows from the proof's own stated S0–S3 range; no channel required.

## Issue 8: Duplicated caveat text in S8 Depends
Reason: Internal editorial — collapse the two near-identical S7b/S7c entries into one joint entry.

## Issue 9: Self-referential consultation citation
Reason: Nelson is needed to ground the claim that S3 must hold at every observable state (not just quiescent states) with a proper Literary Machines source, replacing the procedural "consultation answer ASN-0036" tag with quotable design intent.
Nelson question: Is referential integrity (every V-reference resolves) intended to hold at every observable state including mid-operation, or only at quiescent states between operations — and what is the Literary Machines basis for that intent?
