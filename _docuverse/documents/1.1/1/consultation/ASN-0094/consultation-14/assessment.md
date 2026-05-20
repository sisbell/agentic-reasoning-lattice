# Channel Assignment — ASN-0094 review-14

**Date:** 2026-05-20 00:27

## Issue 1: T4-validity dependency for content addresses is implicit
Reason: The fix is internal — either strengthen the scaffolding clause to assert T4-validity for content addresses, or derive it from the existing scaffolding clauses (`zeros(a) = 3` and `#E(a) ≥ 2` already presuppose T4-validity via T4b's well-definedness of `#E`). Both options are framework-internal documentation choices.

## Issue 2: R3 overgeneralization in Sh0–Sh3 proofs
Reason: The fix is internal — ASN-0086's R3 scope (`→`-transitions only) is established, and LinkStoreInvarianceUnderArrangement already supplies the arrangement-step case in the proofs' Case A. The correction is mechanical: replace the opening claim with the disjunction "strict under `→` by R3, equal under `↦ \ →` by LinkStoreInvarianceUnderArrangement."

## Issue 3: Imprecise R-numbering reference in introduction
Reason: The fix is internal — ASN-0086's actual lemma roster (R0–R7a with intermediate corollaries) is known to the framework; the correction updates the prose reference to match.

## Issue 4: Sh4 base case relies on initial-state baseline that appears later in the text
Reason: The fix is internal — the initial-state baseline paragraph in Sh-conf already establishes `Σ_0 = Σ_init` with `L_K^{Σ_init} = ∅`; the correction adds explicit citation at each Sh0–Sh4 base case site.

## Issue 5: Stratification of inductive proofs is implicit
Reason: The fix is internal — Sh0–Sh3 are proved independently of Sh4 in the existing text, and FDD's preservation symmetrically consumes them. The correction adds a brief stratification note before Sh4 and FDD's preservation proofs.

## Issue 6: Sh-conf's effective-wp derivation has forward dependency
Reason: The fix is internal — both options (reordering RetractionTargetNotOnChain before the derivation, or hoisting the simplification into a labeled Consequence) are document-structural choices using material already present.

## Issue 7: Atomicity scope for Sh4 contract is described inconsistently
Reason: The fix is internal — FDD's "emission and retraction events" phrasing already exists in the document; the correction propagates that phrasing to Sh4's contract for consistency.

## Issue 8: The `slot_addrs(F)` as set-valued function should clarify well-definedness
Reason: The fix is internal — the equivalence follows directly from the canonical-slot form's definition `F = {(x, δ(1, #x)) : x ∈ X_F}`; the correction adds one sentence verifying the comprehension recovers `X_F`.
