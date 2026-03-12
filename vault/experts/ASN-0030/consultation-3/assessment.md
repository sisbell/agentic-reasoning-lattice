# Revision Categorization — ASN-0030 review-3

**Date:** 2026-03-12 00:23

## Issue 1: Ghost permanence — PrefixOrderingExtension misapplied, conclusion overstated
Category: INTERNAL
Reason: The error is in the ASN's own logical argument. PrefixOrderingExtension, T1, TA5, and T9 are all defined in ASN-0001; the fix is correcting the direction of implication and restricting the conclusion using those existing definitions.

## Issue 2: A2 partition — fourth case silently excluded
Category: INTERNAL
Reason: The missing step cites P2 (ReferentiallyComplete, ASN-0026), which is already a stated foundation. The fix is adding one line of reasoning from an existing property.

## Issue 3: A4 — DELETE has no V-space postcondition
Category: INTERNAL
Reason: The review specifies exactly what to write (precondition, length, left-unchanged, right-shifted, cross-document frame), paralleling A4a/A5. The semantics are already understood from the INSERT postconditions and Gregory's implementation evidence already cited in the ASN.

## Issue 4: A5 — COPY target frame conditions absent
Category: INTERNAL
Reason: The review identifies the missing conditions and the ASN already cites Gregory's `insertpm` evidence establishing insert semantics. The fix is formalizing frame conditions already implicit in the existing specification and implementation evidence.

## Issue 5: Worked example forward-references A4
Category: INTERNAL
Reason: Structural ordering issue within the document. The fix is substituting A0 and +_ext (both already defined before the worked example) for the forward reference to A4.
