# Revision Categorization — ASN-0085 review-5

**Date:** 2026-04-11 01:44

## Issue 1: OrdAddHom postcondition (c) invokes vpos outside its declared domain
Category: INTERNAL
Reason: The fix is entirely derivable from the ASN's own definitions. The sequence identity `[S, o₁, ..., oₖ]` stripped and reconstructed is a pure structural fact about tumblers; the overly restrictive precondition on vpos and the missing conditional on the S8a postcondition are internal contract errors that require no external evidence to correct.
