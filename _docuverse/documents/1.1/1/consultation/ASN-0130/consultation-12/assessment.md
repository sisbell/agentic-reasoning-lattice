# Channel Assignment — ASN-0130 review-12

**Date:** 2026-06-13 00:14

## Issue 1: Duplicated "overlapping runs are harmless"
Reason: Pure within-note deduplication — drop the PR-ENC-uniq parenthetical and retain the start-anchoring statement in PR3. The start-anchored-resolution property is already established by the ASN's own content (PR3's resolution clause, PR-ENC-uniq's prefix-freeness argument); no design intent or implementation evidence is in play.

## Issue 2: PS1 re-derives PR0's dynamics and inventories the Multi shape's consumers
Reason: Editorial deduplication internal to the note — replace PS1's idempotency dynamics with a pointer to PR0's already-stated contract, keep the merged-span rationale (already present in PS1), and drop the use-site inventory. PR0's hit/miss/rejection semantics and the AD unit-depth rationale are both already in the ASN.

## Issue 3: Certification's Boolean-result-sort boundary is not stated
Reason: The boundary is forced by content already in the note and its cited dependency — ST/PD0 is a class of Boolean state-predicates (ASN-0129, already imported by PR5), `sig(a) = (Γ_D, C_D)` supplies the result sort (PR-SIG), and PR0 admits any `C_D ∈ Codom`. Adding condition (0) `sig(a) = (Γ_D, Bool)`, splitting out the non-predicate rejection category, and reconciling "predicate" with the general-term mechanism all clarify content the ASN already commits to; no new design intent or implementation evidence is required.
