# Channel Assignment — ASN-0036 review-195

**Date:** 2026-05-29 23:43

## Issue 1: S8a abbreviation stated three times — residual meta-prose from the demotion
Reason: Purely editorial deduplication. Deciding which of the three S8a statements to keep and deleting the standalone Notation paragraph requires only the ASN's own text — no design intent or implementation evidence is at stake.

## Issue 2: ValidFirstInsertionPosition lists dependencies its derivation never uses
Reason: The empty-case definition is a constant tuple `[1,...,1]` of depth `m`; verifying that D-MIN, S8-depth, OrdinalShift, TumblerAdd, and T3 are not load-bearing is checkable directly against the definition and its postconditions in this ASN, so no channel is needed.
