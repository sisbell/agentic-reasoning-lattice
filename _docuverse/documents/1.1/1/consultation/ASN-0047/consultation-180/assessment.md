# Channel Assignment — ASN-0047 review-180

**Date:** 2026-05-31 22:45

## Issue 1: Vestigial `J1`/`J1'` and the first `ValidComposite` definition are superseded before they are ever used
Reason: This is a purely editorial deduplication — collapsing obsolete J1/J1' stubs and the first ValidComposite into the operative J1★/J1'★/ValidComposite★ forms. No design intent or implementation evidence is needed; the link-free fragment is already established as a special case within the ASN's own state model.

## Issue 2: Cross-ASN lineage narration in the property tables
Reason: Reducing each cell to property-plus-citation and dropping inter-ASN genealogy prose is internal editing against the ASN's own tables; the foundation sources (ASN-0093, ASN-0043) are already named, so no channel is required to determine what to keep.

## Issue 3: Definition entries enumerate their downstream consumers
Reason: Stripping use-site forward-references from TrackedEmission and FrontierEquivalence entries is a self-contained editorial fix; the definitions' assertions are already stated in the ASN, so no external channel is needed.
