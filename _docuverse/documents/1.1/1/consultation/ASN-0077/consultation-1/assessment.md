# Channel Assignment — ASN-0077 review-1

**Date:** 2026-05-25 11:48

## Issue 1: Citation typo for M16a
Reason: Pure citation correction; the correct lemma name "OriginInvarianceUnderShift" is given in the review itself and verifiable against ASN-0058's own labels. Internal.

## Issue 2: O1 is essentially tautological
Reason: Both offered fixes (strengthen to a partition statement or demote to a consequence) work from already-cited material — S7a and S7d of ASN-0036 are explicitly named in the ASN's prose and the partition structure follows from the prefix discipline. Internal.

## Issue 3: O4 reduces to a corollary of O3
Reason: The simpler offered fix — demoting O4 to a corollary of O3 — requires only restructuring within the ASN. The strengthening option is an alternative; choosing the demotion path needs no external input. Internal.

## Issue 4: Two formulations of `origins_V` without equivalence proof
Reason: The lemmas needed to chain the three forms (M2, M3, M16a of ASN-0058) are already cited; the work is making the derivation explicit using foundation content already in scope. Internal.

## Issue 5: Proofs are one-sentence appeals, not derivations
Reason: All premises invoked (P0 of ASN-0047, S7 family of ASN-0036, M2/M3/M16a of ASN-0058) are already named in the ASN; the revision expands the implicit steps into enumerated derivations. Internal.

## Issue 6: Edge cases not covered
Reason: Empty intersection, singleton, and empty-document cases derive from definitions and ASN-0058 preconditions. The cross-subspace case is already flagged in the ASN's Open Questions; the required fix is acknowledging the current silent-drop behaviour in the lift definition, not resolving the open question. Internal.

## Issue 7: Concrete example covers only the multi-block case
Reason: Extending the worked example to exercise O5–O10 uses only the operation spec, foundation transition rules already cited, and the existing example structure. Internal.

## Issue 8: O8 framing mismatch
Reason: Choosing between renaming to "Span union monotonicity" or strengthening to a uniformity statement (which O3 already covers pointwise) is an internal labelling decision over content already in the ASN. Internal.

## Issue 9: No weakest precondition analysis
Reason: The wp computations derive mechanically from the postconditions already specified for SHOWORIGIN_I and SHOWORIGIN_V; no new state semantics are needed. Internal.

## Issue 10: Operation precondition for V-span elides ASN-0058 conditions
Reason: The conjuncts of well-formed content reference are spelled out in ASN-0058 (subspace non-emptiness, T12, depth match, dom(M) inclusion); enumerating them inline is a transcription task against an already-cited foundation. Internal.
