# Revision Categorization — ASN-0005 review-3

**Date:** 2026-03-06 21:15

## Issue 1: DEL7 conflates global and per-document discoverability; false contiguity claim
Category: INTERNAL
Reason: The fix restructures definitions already present in the ASN — DEL7's quantifier structure and DEL8's per-document resolution are both stated; the issue is their inconsistency and an unsupported bridge claim. All corrections are derivable from the existing formal machinery.

## Issue 2: "Three permanence commitments" but four listed
Category: INTERNAL
Reason: A counting error in prose; the four properties are already listed immediately below the incorrect count.

## Issue 3: Variable shadowing in wp analysis
Category: INTERNAL
Reason: A notational fix — renaming a bound variable to avoid shadowing the DELETE parameter. Purely mechanical, no external evidence needed.

## Issue 4: POOM entry positional correspondence unstated
Category: INTERNAL
Reason: The positional correspondence (v₁ + k ↦ i₁ + k) is implicit in the span model already used throughout the ASN and its vocabulary ("contiguous range specified by start tumbler and length"). The fix is making an existing implicit assumption explicit as a one-line premise.
