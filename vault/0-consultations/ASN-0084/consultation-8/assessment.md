# Revision Categorization — ASN-0084 review-8

**Date:** 2026-04-10 10:37



## Issue 1: V-extent of a block used without formal definition
Category: INTERNAL
Reason: The fix is explicitly stated — add a one-line definition of V-extent derived from B3, which is already present in the ASN. No external design intent or implementation evidence needed.

## Issue 2: `vpos` defined but never used
Category: INTERNAL
Reason: This is a dead definition identifiable purely from the ASN's own content. The fix (remove or use it) requires only inspecting whether any proof or property references `vpos`, which none does.
