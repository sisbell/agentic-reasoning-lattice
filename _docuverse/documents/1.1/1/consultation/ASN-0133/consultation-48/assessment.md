# Channel Assignment — ASN-0133 review-48

**Date:** 2026-06-14 16:37

## Issue 1: Q0's behavior-collection rebuild uses a single `is_filtered_J` where UV's `filtered` (a disjunction) is required
Reason: Internal. The same paragraph already treats `members`/`targets_of` with UV's full `filtered` disjunction (`{· : ¬filtered(·)}`, citing ASN-0129), so the fix is to apply that identical `¬filtered` body uniformly to the behavior collections — pure internal consistency with the disjunction the note already uses and cites.

## Issue 2: RG states Post_ρ's meta-level nature redundantly
Reason: Internal. This is prose compression of the note's own triplicated restatement; the type distinction (`Post_ρ` meta-level, `T_ρ` the PL part) is already fully present and needs only to be collapsed.

## Issue 3: Decorative capability list in the Triggers paragraph
Reason: Internal. Whether "linkable, versioned, and certified" support any claim is settled by inspecting the note itself, which uses only evaluability and Q0-recognizability; cutting or re-tying the list is an editorial decision derivable from the note's own content.
