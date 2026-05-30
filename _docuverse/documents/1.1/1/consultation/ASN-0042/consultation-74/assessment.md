# Channel Assignment — ASN-0042 review-74

**Date:** 2026-05-29 22:31

## Issue 1: O6 and O9 invoke O1a but omit the reachability precondition O1a requires
Reason: Internal — O1a is established within this ASN as a reachability-dependent derived invariant, and the fix is to align O6/O9 preconditions with the neighboring properties (O2, O4, O10) that already carry "Σ reachable from Σ₀." No design intent or implementation evidence is needed.

## Issue 2: O14's post-formula paragraph is a downstream-consumer inventory of an axiom
Reason: Internal — the consuming derivations (FiniteRegistry, O1a, O1b, T4, O18) already name their base cases within the ASN, so deleting the forward-advertising enumeration is purely editorial and self-contained.

## Issue 3: Document-organization meta-prose around the delegation predicate
Reason: Internal — removing cross-reference bookkeeping sentences is a pure document-organization edit with no dependence on design intent or implementation.

## Issue 4: Duplicated scope-note and near-duplicate open questions
Reason: Internal — collapsing the doubled out-of-scope statement and merging two overlapping open questions is editorial deduplication derivable from the ASN's own text.
