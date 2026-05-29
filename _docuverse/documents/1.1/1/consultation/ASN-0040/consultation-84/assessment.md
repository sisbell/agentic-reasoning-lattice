# Channel Assignment — ASN-0040 review-84

**Date:** 2026-05-29 02:00

## Issue 1: S0 cites a foundation result whose precondition it does not discharge
Reason: Internal. The fix is to either restrict S0's postcondition to B6-valid `(p, d)` or re-prove S0 directly from TA5(a) and T1 transitivity/irreflexivity — both axioms already cited in the ASN, and the reviewer notes this is exactly what T10a.7's own proof uses. No design intent or implementation evidence is required.

## Issue 2: B7 imports an unstated co-tree hypothesis
Reason: Internal. Disjointness of two unrelated B6-valid parents' streams (e.g. `[5]` vs `[7]`) follows from T1 lexicographic disagreement and the prefix structure (S1, TA5, T3) already in the ASN; the author can either re-derive the prefix-incomparable case directly or read T10a.6's actual proof structure in the sibling foundation ASN-0034. Neither design intent nor implementation behavior bears on a structural lemma about address ordering.

## Issue 3: Meta-prose and reviser-drift residue (anti-bloat)
Reason: Internal. Purely editorial deletion of a use-site inventory sentence and a leftover reference to a prior revision's argument; no external information is needed.
