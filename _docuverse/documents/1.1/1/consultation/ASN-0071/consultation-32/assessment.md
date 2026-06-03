# Channel Assignment — ASN-0071 review-32

**Date:** 2026-06-03 08:06

## Issue 1: Completeness/soundness restated within the same section
Reason: Pure deletion of a redundant paragraph; both conformance obligations are already named by the subset/superset framing. No design intent or implementation evidence needed.

## Issue 2: Defensive "load-bearing" justification prose in *The query*
Reason: Trimming rationale essay to bare precondition-constraint statements and relocating the interior-action-point argument to its concrete exhibit. The precondition semantics and the over-collection consequence are already derived within the ASN.

## Issue 3: Abstract-then-concrete duplication with structural narration
Reason: Consolidating two existing treatments (abstract + concrete) into the concrete home and removing cross-section narration. Both derivations already exist in the ASN; this is a placement decision.

## Issue 4: vspec/ContentReference relationship stated twice
Reason: Trimming the prose inventory in *The query* to the single fact (subspace confinement retained) that the Resolution resolve-equivalence derivation needs. Both statements are present; the fix is internal deduplication.

## Issue 5: `find`-vs-`R` distinction stated in three places, plus out-of-scope drift
Reason: Consolidating the find-vs-R point to Currency and cutting the versioning-convention reconciliation, which the ASN's own scope list excludes and which it already concedes is non-structural. Internal scoping decision.

## Issue 6: Origin-recovery recipe stated twice then deferred to
Reason: Stating the `origin(a)`-comparison recipe once and letting the worked bullet exhibit a concrete value. All content already present; the fix is removing repetition.
