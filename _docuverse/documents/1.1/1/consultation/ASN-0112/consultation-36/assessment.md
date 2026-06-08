# Channel Assignment — ASN-0112 review-36

**Date:** 2026-06-08 11:04

## Issue 1: V0's codomain conflates two distinct ASN-0053 types
Reason: This is a type-design choice between three named options (uniform span-set, span-option, or justified asymmetry), all resolvable from the ASN's own reasoning plus ASN-0053's span/span-set definitions already cited in-note. No design intent or implementation evidence is at stake — the implementation's zeros-sentinel is already recorded (V11), and Nelson's "span-set is a series of spans" (4/25) is already quoted; the fix is picking a representation and stating why.

## Issue 2: V-frame is over-justified — prose explains why the frame matters rather than what it asserts
Reason: Pure prose-trimming of an already-stated claim (`Σ' = Σ`); reducing the frame to its assertion and removing the V16-distinction parenthetical requires nothing beyond the note's own content.
