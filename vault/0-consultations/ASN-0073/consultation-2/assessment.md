# Revision Categorization — ASN-0073 review-2

**Date:** 2026-03-22 14:52

## Issue 1: Exactness of N+1 count asserted without distinctness argument
Category: INTERNAL
Reason: Distinctness follows from TS4, TS5, or equivalently from the explicit OrdinalShift computation and T3 — all already-defined foundation properties. The review itself sketches both proof paths.

## Issue 2: Lower bound m ≥ 2 in the empty case stated without derivation
Category: INTERNAL
Reason: The review provides the complete argument: at m=1 the action point of δ(1,1) is k=1, so TumblerAdd increments component 1 (the subspace identifier), violating subspace preservation. The derivation uses only OrdinalShift and TumblerAdd, both already defined.

## Issue 3: Structural properties of valid positions claimed without verification
Category: INTERNAL
Reason: All three sub-properties (depth preservation, subspace identity, S8a consistency) are derivable from OrdinalShift's result-length identity, TumblerAdd's copy behavior for components before the action point, and the explicit form of shift — all present in the foundation ASNs.
