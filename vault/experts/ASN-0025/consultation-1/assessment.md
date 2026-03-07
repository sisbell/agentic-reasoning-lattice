# Revision Categorization — ASN-0025 review-1

**Date:** 2026-03-07 07:09

## Issue 1: J0 preservation never verified
Category: INTERNAL
Reason: The preservation arguments follow directly from each operation's already-stated postconditions (e.g., B ⊆ Σ'.A for INSERT, S ⊆ Σ.A for COPY, P0 for CREATE VERSION). The proofs are one-liners derivable from existing definitions.

## Issue 2: COPY V-space postcondition incomplete
Category: INTERNAL
Reason: COPY inserts content into a sequential V-space mapping at some position, which logically requires the same shift behavior as INSERT. The fix is to state this explicitly by analogy with INSERT's already-written V-space postcondition.

## Issue 3: No concrete worked example
Category: INTERNAL
Reason: A worked example applies the existing state model definitions (Σ.ι, Σ.A, Σ.v) and invariants (P0, P1, J0) to a specific scenario. All necessary definitions are already present in the ASN.

## Issue 4: P9 references state outside the model
Category: INTERNAL
Reason: The reviewer offers two clear options — add spanfilade to Σ or demarcate P9 as implementation commentary. Either option is executable from information already in the ASN. The cleaner fix (option b) requires only moving P9 out of the properties table.

## Issue 5: CREATE VERSION I-space effect is self-contradictory
Category: GREGORY
Reason: The Gregory evidence for CREATE VERSION covers only POOM (V-space) allocation. The parenthetical claim about an orgl entry in I-space is unsupported by any cited implementation evidence. We need confirmation of what `docreatenewversion` actually allocates in the granfilade.

Gregory question: Does `docreatenewversion` allocate any entry in the granfilade (I-space), such as an orgl record? If so, what I-address does it receive and in which subspace?

## Issue 6: P3 conflates two distinct claims under one label
Category: INTERNAL
Reason: The issue is purely logical — the prose says "never shrinks" (= P0) while the formal statement says "doesn't change at all for these operations" (stronger). Splitting or renaming requires only reorganizing claims already present in the ASN.

## Issue 7: Operation preconditions never stated
Category: INTERNAL
Reason: Preconditions follow from each operation's description and the state model (d ∈ Σ.D, valid position in dom(Σ.v(d)), S ⊆ Σ.A for COPY). All necessary constraints are implicit in existing postconditions and can be made explicit without external evidence.

## Issue 8: P6 presented as independent but is a direct consequence of UF-V
Category: INTERNAL
Reason: The derivation is immediate — UF-V applied across all operations yields P6. This is a logical observation about properties already defined in the ASN, requiring only a one-sentence restatement.

## Issue 9: P10 blurs the boundary between abstract model and implementation
Category: INTERNAL
Reason: The ASN itself states that a conforming implementation could satisfy P0 ∧ P1 directly without P10. The fix is editorial: move P10 to implementation commentary and remove it from the properties table. No external evidence needed.
