# Channel Assignment — ASN-0130 review-16

**Date:** 2026-06-13 01:41

## Issue 1: The wp formula for referenceability gates the already-registered branch under VALID
Reason: Pure formal correction. The fix turns entirely on machinery already in the note and its dependencies — rejection-as-skip (`Σ' = Σ`, stated in PR0), I6's attainability convention (ASN-0128), and the fact that `POST-ref`/`POST-cert` are state predicates a *pre-existing* tuple can satisfy. The reviewer even supplies the corrected wp. No design intent or implementation behavior bears on a predicate-transformer derivation.

## Issue 2: PR-DISC carries a use-site inventory and a full seal preview that duplicates "Standard registrations"
Reason: Editorial / anti-bloat restructuring internal to the note — drop the downstream-consumer enumeration and the duplicated seal preview, stating the seal once in "Standard registrations." Nothing depends on what Nelson intended or what the implementation does.

## Issue 3: Defensive meta-prose around the encoding discipline
Reason: Editorial / anti-bloat deletion internal to the note — remove the PR-ENC-uniq robustness sentence (state-independence already follows from "properties of the value sequence alone") and the PR3-consumer rationale in PR-ENC, keeping the bare constraint. No external channel bears on prose pruning.
