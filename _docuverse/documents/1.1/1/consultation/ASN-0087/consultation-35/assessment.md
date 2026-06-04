# Channel Assignment — ASN-0087 review-35

**Date:** 2026-06-03 23:23

## Issue 1: Definition introduced by its downstream consumers
Reason: Pure editorial deletion — remove the use-site preamble and open with the predicate already stated verbatim in the ASN. No design intent or implementation evidence needed.

## Issue 2: Two sections defer to the same downstream argument
Reason: Consolidation of a forward pointer; the S2 two-part argument is already present in full in the ASN. Choosing where it lives is internal restructuring.

## Issue 3: Redundant restatement of the decomposition rationale
Reason: Folding one non-redundant clause (links live in V-space, L14a) into the prior paragraph and deleting the restatement is purely internal — the content is already in the ASN.

## Issue 4: Frame re-enumeration in the "No Permission Check" preamble
Reason: Deleting the parenthetical re-listing of the frame is pure prose cleanup; the permission-check statement stands on its own within the ASN.

## Issue 5: Housekeeping aside that does not advance MAKELINK's reasoning
Reason: Deleting the meta-commentary clause about ASN-0047's precondition phrasing is editorial; the retained `dom(M) = E_doc` identity is already cited.
