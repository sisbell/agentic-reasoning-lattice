# Channel Assignment — ASN-0133 review-63

**Date:** 2026-06-15 01:53

## Issue 1: Structural meta-prose previewing the proof and regime list
Reason: Neither channel is needed — the fix is a pure deletion of structural narration and a forward-pointer, derivable from the ASN alone. Removing meta-prose about what the Proof and regime list do (and the "every regime hypothesis below" pointer) requires no design intent and no implementation evidence; the Q6 statement's substantive claim (registry-side absorption guarantee) is already present and unchanged.

## Issue 2: Use-site inventory previewing Q5a's mechanism
Reason: Neither channel is needed — trimming to the scoping fact and dropping the Q5a-mechanism preview is internal prose hygiene. The retained claim (Q5 needs no extinction discipline) and the downstream contrast (Q5a "supplies H-RF by a route disjoint from Q5") both already exist in the ASN, so the deletion is fully derivable without design intent or implementation evidence.
