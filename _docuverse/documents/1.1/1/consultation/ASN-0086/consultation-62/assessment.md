# Channel Assignment — ASN-0086 review-62

**Date:** 2026-05-19 11:09

## Issue 1: Worked Sketch inline correction breaks formal tone
Reason: Pure editorial cleanup — the correct concrete value (`1.0.1.0.1.0.2.1`) is already present in the text; the fix is to remove the false start and present the corrected derivation directly. No design intent or implementation evidence needed.

## Issue 2: "Case A walkthrough" terminology undefined
Reason: Internal terminology cleanup. The ASN never establishes a Case A/B taxonomy elsewhere, so the simplest fix is to drop the label; if a taxonomy is wanted, K.λ's own first/subsequent emission rule (already cited) supplies the case structure. Derivable from the ASN.

## Issue 3: R7a substrate-conformance precondition under-specifies
Reason: The proof's invariant dependencies (L0, L1, L1a, L1b, L1c, L3, L14, L14a, L-fin) are already enumerated in ASN-0043/ASN-0036, which R7a's proof cites in full. The fix is a precondition-statement edit (expand the list or use a blanket abbreviation) — purely a precision question within the ASN's own substrate vocabulary.

## Issue 4: Observe_K signature ambiguous about address domain
Reason: The ASN's own semantics dictate the answer: `coverage(F)` ranges over `T` (including ghosts per L9, TypeGhostPermission), so pattern arguments must range over `℘_fin(T)` for `F̂ ⊆ coverage(F)` to be a meaningful subset relation when ghost addresses are in play. Resolvable from L9 + the rationale paragraph already in the Definition.
