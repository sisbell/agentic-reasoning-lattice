# Channel Assignment — ASN-0099 review-77

**Date:** 2026-06-04 14:46

## Issue 1: Silent-projection fact stated twice in different words
Reason: Purely editorial deletion of a redundant restatement; the Phase 1 sentence and F12's `defined when` clause already establish both facts within the ASN. No design or implementation evidence needed.

## Issue 2: "coverage(∅)=∅ / empty slot is never a witness" repeated across four locations
Reason: Deleting a standalone paragraph that verbatim repeats F4's own preamble and material in the Endset Filtering and Empty Query sections. Fully internal to the ASN.

## Issue 3: Definition section enumerates its downstream consumers
Reason: Removing a non-load-bearing forward pointer ("a distinction F9 and F11 turn on") that previews downstream consumers; F9 and F11 re-establish the facts at their own sites. Derivable from the ASN alone.
