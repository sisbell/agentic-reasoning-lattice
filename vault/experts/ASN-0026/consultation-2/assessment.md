# Revision Categorization — ASN-0026 review-2

**Date:** 2026-03-08 00:24

## Issue 1: P4 relies on undefined predicate `independent_creation`
Category: INTERNAL
Reason: The derivation from T9 (forward allocation) and T10 (partition independence) in ASN-0001 is already cited in the prose. The fix is to write the two-line formal derivation and recast P4 as a corollary, all from existing definitions.

## Issue 2: Σ.D has no structural properties
Category: NELSON
Reason: Part (a) — stating Σ.V(d) defined iff d ∈ Σ.D — is an internal formalization fix. But part (b) — whether Σ.D is monotonic or can shrink — is a design intent question. I-space is monotonic (P1); whether the document set shares this permanence property requires Nelson's architectural intent.
Nelson question: Is the set of documents permanent (monotonically growing, like I-space), or can documents be destroyed — and if so, what happens to their tumbler addresses and version history?

## Issue 3: P9 formalization is incomplete
Category: INTERNAL
Reason: The missing precondition on p, the formal clause for new positions, and the post-state length assertion are all derivable from the existing prose description and the worked example already in the ASN.

## Issue 4: I-Space Extension freshness is assumed, not derived
Category: INTERNAL
Reason: The reviewer identifies the exact derivation path (T9 + T10 → freshness) and notes it is a two-line argument. All premises are in ASN-0001; only the explicit derivation step is missing.

## Issue 5: Preservation Obligation misclassifies several properties
Category: INTERNAL
Reason: The distinction between state invariants, operation postconditions, and structural permissions is derivable from the definitions already present in the ASN. This is a taxonomy correction using only the ASN's own content.

## Issue 6: P11 is vacuous within the state model
Category: INTERNAL
Reason: The intent is already clearly captured in the Nelson quotes within the ASN. The fix is a formalization choice — reformulating P11 as a protocol signature constraint on RETRIEVE rather than a quantification over a phantom viewer type. No new evidence needed.

## Issue 7: Property numbering gaps
Category: INTERNAL
Reason: Editorial fix — either renumber properties to close gaps or add a note explaining the reserved/removed labels. The commit history already explains the cause.
