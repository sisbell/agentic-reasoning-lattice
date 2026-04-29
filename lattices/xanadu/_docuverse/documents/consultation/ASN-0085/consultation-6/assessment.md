# Revision Categorization — ASN-0085 review-6

**Date:** 2026-04-11 01:56



## Issue 1: OrdAddHom precondition includes S8a, which the proof does not use
Category: INTERNAL
Reason: The review correctly identifies that the proof uses only TumblerAdd mechanics and never references S8a. The fix — weakening the precondition to `v ∈ T, #v ≥ 2` — is fully derivable from the existing proof structure and definitions within the ASN.
