# Channel Assignment — ASN-0043 review-60

**Date:** 2026-05-14 14:51

## Issue 1: L3's formal statement admits empty type endsets despite prose claim of "tightening"
Reason: The fix depends on whether Nelson's design intent treats "every link carries a type endset" as requiring a non-empty endset or merely a present third slot. Gregory's short-circuit behavior is already documented in the prose; the open question is purely design intent.
Nelson question: Does the design requirement that "every link carries a type endset" mandate that the type endset be non-empty (referencing at least one span), or is it satisfied by the structural presence of a third slot that may be empty?

## Issue 2: L9 proof's conformance check awkwardly verifies model-level theorems as state invariants
Reason: Fix is purely internal restructure of the proof — partitioning state-local invariants (verified per state) from meta-theorems (proven once). Derivable from the ASN's own classification of its properties.

## Issue 3: L0's content-side universal silently strengthens ASN-0036
Reason: Fix is editorial — either flag the strengthening or cite a (non-existent) ASN-0036 invariant. The reviewer has already done the cross-ASN check confirming no S-invariant pins `s_C` globally. Gregory's `GRANTEXT = 1` constant is already cited in the prose as supporting evidence.

## Issue 4: L11b's "smallest i" construction relies on implicit T10a / AllocatedSet structure
Reason: Fix is purely internal — cite already-established properties (L1c, L12, AllocatedSet's initial-segment structure from ASN-0034). All needed lemmas exist in the lattice; the reviewer has identified them specifically.
