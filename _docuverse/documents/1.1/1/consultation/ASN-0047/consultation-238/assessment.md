# Channel Assignment — ASN-0047 review-238

**Date:** 2026-06-01 11:14

## Issue 1: K.μ~ admissibility is defined by clauses (i)–(iii), but the proof relies on subspace-preservation, which those clauses do not entail when two subspaces share a depth
Reason: The fix is internal — adding subspace-preservation as explicit admissibility clause (iv) (or folding S3★/S3★-aux into the hypotheses) is fully derivable from the ASN's own S3★ definition, L14, and the coinciding-depth counterexample already present in the worked examples; no design intent or implementation evidence is required to repair the admissible/realisable gap.

## Issue 2: P4★/K.μ~ cell misdescribes what K.μ~ preserves
Reason: The fix is internal — K.μ~'s bijection equation `M'(d)(π(v)) = M(d)(v)` is defined in the ASN, so replacing "values preserved" with the range/set-equality justification follows directly from the operation's stated semantics.

## Issue 3: Duplicated section header restated verbatim as its own first sentence
Reason: The fix is internal — deleting the redundant announcing sentence and run-in header is a purely editorial correction requiring no external input.
