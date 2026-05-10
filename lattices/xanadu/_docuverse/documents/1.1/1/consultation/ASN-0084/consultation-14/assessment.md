# Revision Categorization — ASN-0084 review-14

**Date:** 2026-04-10 12:33

## Issue 1: "Canonical decomposition" used without definition
Category: INTERNAL
Reason: The fix is entirely derivable from definitions already present in the ASN — Block, BlockDecomposition (B1–B3), and Merge are all defined, so "canonical" just means "maximally merged under the stated Merge condition," and uniqueness follows from the arrangement being a function. No external design intent or implementation evidence is needed.
