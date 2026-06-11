# Channel Assignment — ASN-0121 review-36

**Date:** 2026-06-11 16:29

## Issue 1: Trace 4 asserts a nullification with no witness in the store, and its conclusion depends on the missing witness
Reason: The fix is internal — the ASN already contains every ingredient for the explicit construction: the retraction-type representative `ρ` and retractor-building pattern from Trace 7, the `nullified`/`L_R^Σ` definition, the frontier-allocation discipline from FL-WP's scope note, and FL-EMP's link-side rule that excludes the unattributed retractor from the from-constrained query. The review's required repair is a computation over these existing definitions, with no design-intent or implementation question outstanding.

## Issue 2: The snapshot reading is stated twice, the second time as a relocated stub, with a meta-disclaimer
Reason: This is a prose-structure defect — duplication and a meta-disclaimer — fixable by deleting the restated paragraph and disclaimer sentence and opening the section with the stability facts. No semantic content is in question, so neither channel is needed.

## Issue 3: FL-LOC re-derives the nullified-locality argument given two paragraphs earlier
Reason: Pure deduplication: the structural argument is already correctly derived in "The answer is forced," and the fix is to cite that derivation from FL-LOC's proof and trim the claims-table row. No new fact from design intent or the implementation is required.

## Issue 4: FL-REACH opens and closes with the same assertion
Reason: Editorial redundancy — the fix is to cut the closing paragraph or fold its one novel clause into consequence (a), with all substantive content already carried by consequences (a)–(d). Derivable entirely from the ASN's own text.
