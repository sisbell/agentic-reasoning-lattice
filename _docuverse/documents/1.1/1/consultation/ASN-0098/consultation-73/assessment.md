# Channel Assignment — ASN-0098 review-73

**Date:** 2026-06-03 06:40

## Issue 1: Forward/backward reference loop between LP-Fin and the `tight` definition
Reason: Purely an editorial reorganization — either reordering the `tight` definition above LP-Fin or deleting a parenthetical cross-link. No design intent or implementation evidence bears on prose placement; the fix is fully internal.

## Issue 2: Claims-table entries carry derivation prose instead of statements
Reason: A structural cleanup that moves derivation/scope prose out of the table's Statement column into the existing lemma bodies. Both the bare statements and the relocated prose already exist in the ASN; the fix is internal.
