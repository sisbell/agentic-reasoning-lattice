# Channel Assignment — ASN-0099 review-10

**Date:** 2026-05-26 19:11

## Issue 1: F4 missing from numbering
Reason: Pure bookkeeping/labeling within the ASN. The author chooses between restoring an F4 claim (which Issue 4 may absorb) or renumbering F5–F20; no external evidence or design intent is required.

## Issue 2: Worked example does not exercise cross-document T1 case (ii)
Reason: The version-extension case is already derived in F10's prose using K.δ at k=1 and T1 case (ii). Extending the example with `d_c = inc(d_a, 1)` or adding prose justification draws on material already in the ASN and cited axioms (T1, ASN-0034; K.δ, ASN-0047).

## Issue 3: F9-cor's coverage of K.δ-IsDocument is not made explicit
Reason: The fix is an explicit one-sentence note that `findlinks` (without V-prefix) consults only `Σ.L`, which is F8's own structure. The K.δ frame from ASN-0047 and LP8 from ASN-0098 are already cited; no further evidence is needed.

## Issue 4: F1's "design constraint on conforming implementations" is normative content without numbered status
Reason: The substantive content (no strengthening of the match predicate) is already justified in the ASN via the reader's promise and L13 (links attach to bytes). Elevating to a labeled claim or folding into F2/F3 is a structural reorganization derivable from existing prose.

## Issue 5: A1's vocabulary-closure clause is brittle under future revision
Reason: The contradiction between A1's temporal closure clause and its propagation clause is an internal wording problem. Resolving it requires only that the author choose between removing the temporal qualifier or strengthening the propagation clause to override it.

## Issue 6: F11's value-equality vs. tuple-component step is glossed
Reason: The fix adds one sentence grounded in L3 of ASN-0043 (Link as a finite sequence with arity = tuple length), an axiom already cited extensively in F11's derivation. No external input needed.
