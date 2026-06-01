# Channel Assignment — ASN-0086 review-112

**Date:** 2026-05-31 21:31

## Issue 1: R0 cross-home freshness asserts a false intermediate — distinct documents are *not* generally prefix-incomparable
Reason: The fix is derivable from the ASN itself — R0a Case 1 already carries out the correct field-separator/zero-position cross-home argument (option b), and the alternative is a citation to a foundation lemma (ASN-0093), not a question about design intent or implementation behavior.

## Issue 2: Same scope-justification prose restated three times with a self-referential forward pointer
Reason: Purely editorial deduplication — consolidate the scope-choice statement at Definition — Emit_K and delete the two restatements. No external channel bears on this.

## Issue 3: Two full worked examples embedded inside the R7a proof body
Reason: Purely structural relocation/consolidation of existing content into the Worked Sketch section. No external channel bears on this.

## Issue 4: R7a leans on "substrate-conforming layer" / clause (b) frontier-emission as a definitional assumption
Reason: Derivable internally — the ASN's own Definition — Categorical reachability already exhibits a conforming-yet-non-contiguous counterexample showing the substrate does *not* force frontier-contiguity, so option (b) is foreclosed and only option (a) (qualifying the claim as clause-(b)-contingent in the table and at point of use) remains, a self-contained editorial fix.
