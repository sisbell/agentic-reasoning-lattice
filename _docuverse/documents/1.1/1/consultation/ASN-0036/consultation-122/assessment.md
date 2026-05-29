# Channel Assignment — ASN-0036 review-122

**Date:** 2026-05-28 21:54

## Issue 1: Meta-prose claiming the document does not repeat itself
Reason: Pure deletion of a self-referential bookkeeping clause. The non-canonicality fact already stands on its own; no design intent or implementation evidence is needed to remove the promise-not-to-repeat sentence.

## Issue 2: Defensive prose explaining what is *not* invoked / *not* derived (S8a)
Reason: The positive derivation (zeros = 0 and positivity follow from the element-field commitment plus T0) is already present in the proof; removing the "without appeal to T4" and "(Note: ... not derived from S7b or S7c)" negations is internal editing.

## Issue 3: Parentheticals justifying why a precondition is omitted (OrdAddHom, OrdAddS8a)
Reason: The omitted bound follows trivially from ActionPoint's contract already cited in-document; dropping the defensive parentheticals and internal back-reference requires no external channel.

## Issue 4: Duplicated derivation of D-SEQ
Reason: Both passages restate the same argument already in the ASN; choosing to keep one and trim the other is an internal editorial decision.

## Issue 5: Repeated deferral of link-subspace contiguity to a future ASN
Reason: The load-bearing content (the `0` in `N.0.U.0.D.0.2.1` is a field separator, not a subspace identifier) is already established by T4 and stated in the Remark; consolidating the deferral into one statement and folding the separator note into S8a is internal.

## Issue 6: S9 trailing essay listing downstream guarantees "none is derived here"
Reason: Deletion of forward-looking essay that the ASN itself flags as underived; the directional-reading-of-S0 statement remains and carries all formal content.

## Issue 7: Redundant double-citation in subspace_I postcondition (b)
Reason: Determining which single clause delivers `E(a)₁ ≥ 1` is resolved from the ASN's own dependency structure (T4's positive-component constraint via S7b/T4b); whether T10a.4 discharges a distinct step is answerable from the existing proofs.

## Issue 8: ValidInsertionPosition precondition incomplete for its own postcondition
Reason: Postcondition (d) is derived from D-MIN and D-SEQ, which the ASN already lists in Depends; adding them to Preconditions (or weakening the postcondition) is an internal consistency fix.
