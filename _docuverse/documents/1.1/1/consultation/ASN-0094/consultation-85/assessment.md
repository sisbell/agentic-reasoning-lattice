# Channel Assignment — ASN-0094 review-85

**Date:** 2026-05-25 19:23

## Issue 1: Sh-conf admission's "biconditional" wording explains why the axiom is structured rather than stating what it says
Reason: Pure prose restructuring — replace meta-justification with direct biconditional statement. The axiom's content is already present; the fix is internal reformulation.

## Issue 2: RetractionSelfFreshness Precondition 3 mixes precondition with consequence
Reason: Internal cleanup — relocate the Sh4-contract discharge from precondition to proof body. All cited facts and their justifications already exist in the ASN; the fix is structural.

## Issue 3: "Gate 5" mislabels the K.λ emission step
Reason: Internal terminology fix — the framework's actual structure (5 gates plus emission) is clear from the content; reword "gate 5" references to "K.λ emission after gate 4 admits."

## Issue 4: Sh-conf Rejection Patterns omits d ∉ dom(Σ.M)
Reason: Documentation gap — gate 0's two-conjunct structure is already specified in the Gate Ordering; the fix is adding the missing pattern entry or expanding Pattern 4 to cover both conjuncts.

## Issue 5: Case A enumeration duplicated across Sh4, FDD, and SHCD preservation proofs
Reason: Refactoring — lift the shared A_K-closure / L_K-side-stable case enumeration into a shared lemma (extending CaseAClosureForLK or adding a sibling). All content already exists; the fix is consolidation.

## Issue 6: Forward-reference accretion around EffectiveWpSimplification
Reason: Internal cleanup — concentrate wp-simplification machinery in the corollary, replace preambles with label-only citations. The technical content lives in EffectiveWpSimplification and LinkAddressNotPrefixOfEmit; the fix removes redundant scaffolding.

## Issue 7: Per-walkthrough convention reiterated in every walkthrough
Reason: Pure repetition removal — convention is already stated once at Initial-State Baseline. Drop per-walkthrough citations; this is purely editorial.

## Issue 8: AllocatedAddressAntichain Step 3.2 contains apologetic meta-prose
Reason: Internal prose hygiene — strip the parenthetical defending against a stronger-bound comparison. The proof itself works at the bound used; the meta-justification adds nothing.

## Issue 9: Tuple-Classifier's "single-letter substitution" misdescribes the change from Classifier
Reason: Internal description fix — the formal template bodies are correct in the ASN; only the explanatory phrase needs to either accurately describe the rename+capture-avoidance or be dropped entirely.

## Issue 10: Properties Introduced table duplicates body content
Reason: Internal editorial decision — reduce to navigation aid or drop entirely. All claims and their statements are in the body; the table's classification is the only added content.
