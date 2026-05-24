# Channel Assignment — ASN-0094 review-53

**Date:** 2026-05-24 02:00

## Issue 1: Sh5(b) discipline's category (i) literal wording excludes the derived slot accessors the audit table treats as category (i)
Reason: Internal — the framework defines its own discipline and audit categories; updating category (i) wording or extending category (vi)'s enumeration is a definitional fix derivable from the ASN's own content.

## Issue 2: Sh4 Case D's "Step D.0" derivation of `τ_new ∈ A_R^{Σ'}` is load-bearing but its placement within Case D is unconventional
Reason: Internal — structural reorganization of an existing proof; promoting D.0 to a named sub-lemma is a presentation choice derivable from the ASN's own proof content.

## Issue 3: The "audit-slice multiplicity is not preserved" commitment in NullifyActiveSubsetCompatibility shifts ASN-0086's Nullify postcondition in a way downstream consumers may not anticipate from ASN-0086's text alone
Reason: Nelson needed — the migration-discipline question turns on whether retraction was designed as audit-event recording (multiset, distinguishable per call) or as state-flag (set, one bit per target). That design intent informs whether attributed-retraction is the right migration pattern and what the attribution slot should carry.
Nelson question: Was the retraction operation intended to record each retraction call as a distinguishable audit event (multiset semantics, with duplicates preserved for event reconstruction), or as a state-level flag setting `a ∈ nullified` (set semantics, with duplicates collapsing)?
