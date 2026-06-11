# Channel Assignment — ASN-0118 review-27

**Date:** 2026-06-10 19:01

## Issue 1: Misstatement of what J1'★ forbids in the worked example
Reason: J1'★'s content (a constraint on the net new pairs `R' ∖ R`, not on individual K.ρ steps) is already fixed by ASN-0047 and correctly characterized in the review; the fix is rewording two passages to match that formal content. No design-intent or implementation question arises.

## Issue 2: Range equality and CP4 exactness cite only the lower-bound clauses; the closure clauses they need go uncited
Reason: The needed closure clauses (CP3c, CP6's domain-equality conjunct) already exist in the ASN; the fix is adding them as cited premises in two derivations. Purely an internal proof-citation repair.

## Issue 3: Garbled sentence in the entity-frame paragraph
Reason: Editorial — a mangled relocation of an existing sentence whose intended content the review reconstructs; rewriting it requires only the ASN's own text. No external consultation needed.

## Issue 4: The placement-position S8a/S8-depth discharge is stated twice, nearly verbatim
Reason: Deduplication of an internally derived discharge (ValidInsertionPosition + OrdShiftHom) into a single factored observation; both copies and all cited lemmas are already in the ASN. Internal restructuring only.

## Issue 5: The composite-validity proof interrupts the operation contract
Reason: Pure placement/organization — moving the existing composite exhibition into its own section and referencing it from CP8. No new content is required from either channel.
