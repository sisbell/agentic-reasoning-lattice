# Channel Assignment — ASN-0042 review-39

**Date:** 2026-05-14 05:04

## Issue 1: NestingByDelegation derived in text but absent from Properties Introduced table
Reason: Purely a cataloging fix — the property is already derived in the text and the required table row's provenance is internal to the ASN. No channels needed.

## Issue 2: The cumulative invariant "every principal's prefix is in Σ.B" is used but not formally derived as a named property
Reason: All ingredients are present in the ASN — O14(vii) base case, O15 closure, O18 inductive step, T8 permanence. The fix is to name the cumulative invariant, prove it inline by induction on path length, and replace the bare "invoke O18" citations. No channels needed.

## Issue 3: Self-ownership at the prefix asserted as a general theorem but not catalogued
Reason: The theorem's proof (reflexivity of ≼, O1b for distinct prefixes, the prefix-baptism invariant from Issue 2) is entirely internal. Promotion to the table and provenance follow from already-stated properties. No channels needed.
