# Channel Assignment — ASN-0093 review-67

**Date:** 2026-05-31 12:09

## Issue 1: Properties Introduced table omits the four named chain disciplines that Scope promises it enumerates
Reason: The four disciplines (ChainElementT4Validity, ChainEnumerationInjectivity, DisjointSubAllocatorChains, ChainPrefixExtension) are already defined in the body with explicit ASN-0040 sources; adding table rows or weakening the Scope claim uses only material already present in the note.

## Issue 2: SD is verified in the base case but has no row in the inductive-step matrix, contradicting the note's own convention
Reason: Both remedies — adding an SD matrix row citing L0/C1/L1/StoreT4Validity, or declaring SD a pointwise consequence and removing it from the base-case list — are derivable from the note's own SD derivation and stated matrix convention, requiring no external input.
