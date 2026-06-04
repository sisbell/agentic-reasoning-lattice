# Channel Assignment — ASN-0101 review-74

**Date:** 2026-06-04 15:55

## Issue 1: P4a discharge in the D11 boundary derivation relies on a single-step argument at a multi-step composite boundary
Reason: The fix restructures an internal proof step using J1'★ — already part of ValidComposite★'s clause (2) in this ASN — to witness composite-added provenance pairs at the endpoint boundary. No design intent or implementation evidence is needed; the argument is fully derivable from the ASN's own validity conditions and N2/P4a definitions.

## Issue 2: Wrong claim reference in the worked-example verification of D10
Reason: A pure textual cross-reference correction ("D11 wp" → "D10 wp"); the ASN itself establishes that D10 introduces the wps and D11 introduces no wp.

## Issue 3 (anti-bloat): Defensive vocabulary-provenance prose in D11
Reason: A deletion of one redundant sentence; the vocabulary list and "The operation" section already carry the information, so the fix is internal.
