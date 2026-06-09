# Channel Assignment — ASN-0126 review-34

**Date:** 2026-06-09 09:56

## Issue 1: The reachable-state conformance guarantee is asserted but absent from the property list
Reason: The closure invariant is derived purely from P4 plus the base case `Σ_init.L = ∅`, both already stated in the ASN; raising it to a numbered property with its inductive proof requires no external input.

## Issue 2: The attribution-via-home-document point is stated three times
Reason: Pure editorial consolidation — collapse three restatements of the `d_retr` attribution rationale into one. All content is internal to the section.

## Issue 3: "Binary is weaker than unit-depth discipline" is explained twice at length
Reason: Both passages restate a structural fact already proven from the note's own Binary/unit-depth definitions; deduplicating and cross-referencing is internal.

## Issue 4: "Domain-discharge ordering" is explained twice
Reason: The fix replaces a re-explanation with a named back-reference to a convention defined earlier in the same note — entirely internal.

## Issue 5: Projection-bridge paragraph carries defensive meta-prose
Reason: Removing self-justifying sentences while keeping the already-stated concrete consequences is a local editorial deletion requiring no external evidence or intent.

## Issue 6: "Properties established" re-derives rather than indexes
Reason: Compressing P5's body to statement-plus-pointer references the Registry-permanence derivation already present in the note; purely internal.

## Issue 7: Open-question item 4 contains essay content in a structural slot
Reason: The fix is to crisp the question and relocate or drop the Nelson aside; the rephrasing is structural and the claim is already in the note, so no fresh design-intent query is required.
