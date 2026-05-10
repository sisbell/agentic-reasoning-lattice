# Revision Categorization — ASN-0051 review-15

**Date:** 2026-03-23 01:34

## Issue 1: SV6 proof contains a false intermediate claim
Category: INTERNAL
Reason: The fix is purely proof-mechanical — replace `#t ≥ #s` with `#t ≥ k` and adjust the two-case argument. All definitions and properties needed are already present in the ASN.

## Issue 2: SV2 proof covers only K.μ⁺, not K.μ⁺_L as claimed
Category: INTERNAL
Reason: The fix is adding explicit reference to K.μ⁺_L's frame conditions in the proof parentheticals. The argument is trivially parallel and all needed properties are already stated in the ASN's own preamble to SV2.
