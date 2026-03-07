# Revision Categorization — ASN-0025 review-2

**Date:** 2026-03-07 07:32

## Issue 1: P3 exhaustiveness claim is ungrounded
Category: GREGORY
Reason: The preferred fix (adding CREATE DOCUMENT as a seventh operation) requires implementation evidence for `docreatenewdocument`'s exact I-space and V-space effects, parallel to the Gregory confirmations provided for every other operation.
Gregory question: What does `docreatenewdocument` allocate in I-space — just a single orgl address via `findisatoinsertnonmolecule`, or additional entries? Is the initial V-space empty, or does it contain a structural entry?

## Issue 2: P7 asserted as axiom but is derivable
Category: INTERNAL
Reason: The derivation uses only properties already present in the ASN and ASN-0001 (T9, T10, GlobalUniqueness, P3). No external evidence is needed — the fix is a matter of writing out the logical steps from existing definitions.

## Issue 3: Correspondence derivation cites wrong premise
Category: INTERNAL
Reason: The correct premise (CREATE VERSION's V-space mirroring postcondition) is already stated in the ASN's own CREATE VERSION section. The fix is a citation correction within existing content.

## Issue 4: P8 is not a property of the abstract model
Category: INTERNAL
Reason: Both fix options draw on material already in the ASN — the tumbler structure from ASN-0001 and the ASN's own statement that "the node field records provenance, not current location." No new design intent or implementation evidence is needed.

## Issue 5: P2 mislabeled in properties table
Category: INTERNAL
Reason: The derivation is already written and correct in the ASN text. The fix is a one-word change in the properties table from "introduced" to "derived."
