# Revision Categorization — ASN-0042 review-11

**Date:** 2026-03-15 23:19

## Issue 1: O14 does not provide the base case for O1a and O1b invariants
Category: INTERNAL
Reason: The prose already states initial principals are "node-level" (zeros = 0), which satisfies both constraints. The fix is adding explicit formal constraints to O14 that are already implied by the existing text — no external evidence needed.

## Issue 2: O6 biconditional forward direction compresses the field-alignment argument
Category: INTERNAL
Reason: The ASN already contains the two-case field-alignment argument in step (3) of the "effective owner's prefix is embedded" derivation. The fix is inlining or forward-referencing existing reasoning into the biconditional's forward direction — purely a structural reorganization of material already present.

## Issue 3: O10 does not establish existence of a suitable fork address
Category: INTERNAL
Reason: The review itself sketches the complete argument from finite Π (O15), O1a, and T0a/T0b (from ASN-0034). All premises are already established in the ASN or its dependencies — the fix is assembling an existence proof from existing properties.
