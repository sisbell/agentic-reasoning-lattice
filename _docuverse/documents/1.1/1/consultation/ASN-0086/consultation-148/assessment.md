# Channel Assignment — ASN-0086 review-148

**Date:** 2026-06-01 03:41

## Issue 1: L-ContiguousPrefix duplicates the foundation lemma ASN-0093 ChainMembershipForOrigin, and the two are cited interchangeably for the same fact
Reason: The fix is a restructuring decision — cite ChainMembershipForOrigin for the reachable case and recast L-ContiguousPrefix as its extension to substrate-conforming states. Both lemmas are already referenced in the note, and the extension is justified from this note's own conformance clauses (b)–(c), so the reconciliation is derivable from ASN content alone.

## Issue 2: Meta-prose justifying proof ordering / non-circularity in R7a
Reason: Pure deletion of meta-prose; the substantive content ("Σ' is substrate-conforming") is already stated in the preceding sentence. Internal.

## Issue 3: Orientation meta-prose and duplicated alias boilerplate
Reason: Pure deletion of orientation prose and verbatim boilerplate already carried by the Properties table. Internal.

## Issue 4: R6b label inconsistency
Reason: Reconciling the heading to match the table's "DEF-Consequence" is a self-contained editorial fix; the body's one-line definitional unfolding confirms the correct classification. Internal.
