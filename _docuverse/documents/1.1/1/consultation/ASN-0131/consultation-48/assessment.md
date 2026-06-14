# Channel Assignment — ASN-0131 review-48

**Date:** 2026-06-14 01:53

## Issue 1: The RE-UDIST-∩ counterexample omits two of its required witnesses
Reason: The fix completes a counterexample using machinery the ASN already has on the table — K.λ emission producing an addressable link, the unit-endset coverage `{t : a ≼ t}` (PrefixSpanCoverage), and image construction over sibling content addresses. Pinning the arrangement so `coverage(e) ∩ image(W₁∩W₂) = ∅` (rather than just `a ∉` it) is internal construction, requiring neither design intent nor implementation evidence.

## Issue 2: RE-EDIT's shift-insert/delete coverage rests on an undischarged, foreign assumption — flagged in prose but not in the claim's status, and surrounded by meta-prose
Reason: The required fix is presentational — either excise the shift cases (a scoping choice deferring to a future ASN) or mark RE-EDIT's shift coverage conditional in the Claims table as RE-WHOLE already is, plus trim the meta-prose. The assumption is meant to stay an assumption in this note, not be discharged, so no implementation evidence or design intent is needed; the labeling and trimming are derivable from the note's own structure.
