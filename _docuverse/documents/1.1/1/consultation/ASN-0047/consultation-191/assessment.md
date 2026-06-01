# Channel Assignment — ASN-0047 review-191

**Date:** 2026-06-01 00:43

## Issue 1: Foundation citation "SubAllocatorAxiom / ContentLinkSubAllocatorExistence" cannot be reconciled with ASN-0093's claim set
Reason: Internal citation hygiene. The review already supplies the actual ASN-0093 claim names (FirstEmission, FirstEmissionFreshness, DisjointSubAllocatorChains, ChainElementT4Validity, ChainDiscipline) and their derivation from ASN-0040's SiblingStream; the fix is to rename the citations or mark "SubAllocatorAxiom" as introduced-here and prove it from those lemmas — no design-intent or implementation evidence is required.

## Issue 2: Verification matrix and per-invariant prose triple-state the trivial rows
Reason: Pure editorial deduplication. Deleting the restating prose for frame/precondition-only invariants requires no external input — it is a presentation fix derivable from the ASN's own content.

## Issue 3: Defensive justification and use-site inventory around the M-totality override and foundation provenance
Reason: Editorial trimming internal to the ASN. Keeping the override identity and M2 carve-out while dropping the verbatim-carryover inventory and collapsing repeated provenance annotations needs no design or implementation evidence.
