# Channel Assignment — ASN-0123 review-14

**Date:** 2026-06-13 01:59

## Issue 1: The headline guarantee — link carry-through — is never demonstrated against a concrete scenario
Reason: The required trace only instantiates claims the note already proves (V2's transcription, V13's `R' = R ∪ A×{v}`, V9w's dual rows, V10's LP12 biconditional) on concrete addresses; the coverage computation it needs is already in hand (PrefixSpanCoverage for the unit-depth span, SA to force `coverage(ℓ) ∩ A = {a₁}` from the antichain property), and `project`'s value comes from the already-cited link-projection foundation. No design intent or implementation evidence beyond what the note already imports is required.
