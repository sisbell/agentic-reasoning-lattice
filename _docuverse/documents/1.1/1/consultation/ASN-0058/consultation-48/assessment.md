# Channel Assignment — ASN-0058 review-48

**Date:** 2026-05-30 08:01

## Issue 1: Forward-reference accretion in the OrdinalShiftBase and "+" overloading paragraphs
Reason: Purely editorial pruning — the required change reduces prose to the definition plus disambiguation already stated in the ASN. No design-intent or implementation evidence is involved.

## Issue 2: M-int dependency/availability inventory header
Reason: Removing the dependency inventory and reusability assertion is internal cleanup; the proof itself already exhibits the dependencies, and any reuse justification relocates to C1a's existing text within the ASN.

## Issue 3: M-sub is a non-load-bearing lemma carrying use-site-inventory prose
Reason: Whether M-sub is consumed anywhere is determinable from the ASN's own proofs (C1a, C16a), which the review already traces. The decision to delete or wire it in is a formal-structure judgment internal to the note.

## Issue 4: M16a enumerates its downstream consumers
Reason: Editorial deletion of the consumer-enumeration clause while keeping the one-line summary; nothing requires external design intent or implementation evidence.

## Issue 5: M2 misattributes ASN-0036's S8 postcondition labels
Reason: The fix is a citation correction against sibling foundation note ASN-0036, whose actual S8 labels the review already states (lockstep = (a), partition/uniqueness = prose + (c)); neither Nelson's design intent nor Gregory's implementation bears on which label ASN-0036 assigns.
