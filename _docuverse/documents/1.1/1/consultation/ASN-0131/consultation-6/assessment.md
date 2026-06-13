# Channel Assignment — ASN-0131 review-6

**Date:** 2026-06-13 07:17

## Issue 1: Worked instance asserts an exact result that depends on two unspecified endsets
Reason: The fix is internal — it requires only specifying `e₂′` and `e₃′` so their coverage misses `{a₂}` (exactly as the note already constructed `e₂` and `e₃` via PrefixSpanCoverage disjoint from the image) and extending the "only slot 1 appears" read-off to `L₂`'s two slots. This is example construction governed by the note's own definitions (RE-DEF, `touch_W`), with no appeal to design intent or implementation behavior.

## Issue 2: The adopted convention RE-WHOLE is never exercised by a concrete scenario
Reason: The fix is internal — RE-WHOLE is already adopted and defined in the note (return all spans of a touching endset), so the task is purely to construct a discontiguous endset spanning one in-region and one out-of-region address and read off the result under RE-DEF/RE-WHOLE. It does not ask to *resolve* OQ1 (which would need Nelson's design intent), only to illustrate the already-stated provisional convention.
