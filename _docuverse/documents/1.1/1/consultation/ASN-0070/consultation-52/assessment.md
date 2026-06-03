# Channel Assignment — ASN-0070 review-52

**Date:** 2026-06-03 01:01

## Issue 1: Existence proof interleaved inside the uniqueness argument; theorem mislabeled
Reason: Pure proof-restructuring — rename the theorem and relocate Step 2a so existence is not embedded in the uniqueness chain. No design intent or implementation evidence is needed; the content already exists in the ASN.

## Issue 2: F-subspace's Consequence re-derives a chain its own postcondition already encapsulates
Reason: The fix trims a redundant re-invocation of S3★-aux/S3★ and starts from the already-established postcondition equality, keeping only the L0+L14 step. Entirely internal bookkeeping.

## Issue 3: Repeated "System reading" template across the derived-property catalogue
Reason: The fix consolidates existing Nelson-design-intent commentary into one preamble remark — the design content is already written in the ASN, so this is a restructuring of present material, not a request for new intent. Internal.

## Issue 4: Forward-reference gestures justifying representability before it is needed
Reason: The fix removes premature representability justifications from F0 and the inline forward pointer in F-canon-form, leaving the argument where F-canonical proves it. No external input required.
