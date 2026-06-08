# Channel Assignment — ASN-0103 review-26

**Date:** 2026-06-08 08:30

## Issue 1: Off-chain branch re-derives a distinctness already established by freshness
Reason: Internal — the *Freshness* paragraph already proves `d ∉ E` for all of `E` via `d ∈ S(A,2) \ E`, so the off-chain branch is removable using reasoning already present in the ASN.

## Issue 2: Use-site justification and forward references in "A Note on Sub-Allocator Activation"
Reason: Internal — the activation effect is already correctly derived from SubAllocatorBundle/CND.subAlloc; deleting the use-site justification and INSERT/MAKELINK forward references is a pure editorial trim.

## Issue 3: Duplicate deferral to the registry-carrying ASN
Reason: Internal — both deferrals reference the same registry-coupling question already stated in Open Questions; consolidating to one location requires no external evidence.

## Issue 4: CND.A-act prose justifies why the assumption is needed rather than stating it
Reason: Internal — the assumption's content and single non-derivability note are already in the ASN; removing the duplicated rationale and use-site inventory is editorial.
