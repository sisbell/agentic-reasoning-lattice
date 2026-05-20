# Channel Assignment — ASN-0094 review-17

**Date:** 2026-05-20 01:36

## Issue 1: "Content-side scaffolding" name covers more than content
Reason: Pure renaming issue with downstream citation updates. The scope mismatch is visible by inspection — four clauses are link-side, one is document-side — and the fix is editorial across the ASN's own self-references.

## Issue 2: Retraction catalog row's primary-consumption wording
Reason: The fix aligns with ASN-0086's R6b audit-slice commitment already cited in the framework. Rephrasing the parenthetical to reflect audit-slice semantics (rather than active-subset via `to_K`) is internal — both the framework's `to_K` definition and ASN-0086's R6b are already in scope.

## Issue 3: Retraction's pair_K signature departs from the other catalog rows without justification
Reason: This is a Sh5(b) discipline question entirely within the framework's own scope — whether the set-equality reading is mechanically forced or is a documented role-specific choice. Sh5 is hand-curated per the framework's META commitment, so the resolution is an internal design-discipline decision.

## Issue 4: Sh5(b) discipline statement is unfalsifiable as written
Reason: This is about precisifying the framework's own META criterion — what counts as "explicitly named" for templates that consume scaffolding clauses (like `chain_index` in `emission_order`). Internal precision fix; the catalog row's columns and the scaffolding listing are both already in the ASN.

## Issue 5: Sh-conf return-type extension creates an unfixed boundary with ASN-0086
Reason: The ASN already states the baseline R-registration requirement and that "Sh-conf admits every well-formed Nullify call" with R registered. The fix is choosing between two internal options (explicit exception or scope-restriction reframing); both are derivable from existing content.

## Issue 6: AllocatedAddressAntichain Sub-case 3 invokes Step 3.2's conclusion `E(x) ≼ E(a)` but uses only the first index
Reason: Pure proof-simplification — derive `E(x).1 = E(a).1` directly from componentwise agreement at position `n_3 + 1` plus T4b's index offset, both already cited in the proof. Internal.

## Issue 7: RetractionTargetNotOnChain Case II asserts "TA5(c) with k = 0 ... or equivalently, T10a.8" but the equivalence is not exact
Reason: Citation-precision fix between two ASN-0034 properties whose relationship is already known to the framework. Pick the per-step citation (TA5(c)) or the closure citation (T10a.8) consistent with what the proof actually consumes. Internal.

## Issue 8: "Layer commitment" is used to refer to four distinct things
Reason: Pure naming/terminology disambiguation across the document. All five commitments are introduced and defined within the ASN itself; the fix is consistent renaming throughout. Internal.

## Issue 9: Worked Example "Rejection case 4" example uses K_ghost ∈ T_admissible but example shape parameters not stated
Reason: Editorial fix to add an explicit `T_cat = {comment, K_res, R, …}` listing at the start of the worked example. Internal.

## Issue 10: Sh4 preservation proof's Case A residual scenario is dispatched but its enumeration is incomplete
Reason: Internal proof-structure choice between two options (drop residual analysis relying on case-equation, or prove uniqueness of the listed residual). Both options are self-contained within the framework's existing proof apparatus.

## Issue 11: SingleHomeCoverageDiscipline preservation is not separately proved
Reason: Structural-completeness question parallel to Sh4 and FDD, whose preservation-theorem templates (layer-discipline contract + inductive Case A/B/C structure) are already established in the ASN. Choice between adding a preservation theorem (using the existing pattern) or explicitly noting it as a non-inductive registration constraint is internal.
