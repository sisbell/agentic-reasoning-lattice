# Channel Assignment — ASN-0086 review-31

**Date:** 2026-05-17 05:31

```
## Issue 1: SharedDepthOneAllocator's "element-field depth" terminology is used in two incompatible senses
Reason: The fix is terminological disambiguation between zeros-count depth (defined in Setup) and allocator-tree spawn-event distance. Both notions are already present in the ASN and its cited foundations (ASN-0034 TA5, T10a); the structural facts are correct, only the naming needs clarification. No external evidence or design-intent input required.
```

```
## Issue 2: R0 Step 4 dispatches seven L-invariants in a single bullet, breaking granularity with the rest of the proof
Reason: The fix is to either expand the bundled L4–L10 bullets to per-invariant granularity or shorten the elaborated ones for uniformity. Each L-invariant is defined in ASN-0043 (already cited), and verifying preservation under a class-(iii) emission with the stated Frame is mechanical from those definitions. Purely internal proof-style fix.
```

```
## Issue 3: Worked Sketch Step 3 cites T3 for prefix-incomparability, but T3 is about tumbler equality, not prefix relations
Reason: The fix is a citation correction — replace T3 (CanonicalRepresentation) with Prefix (PrefixRelation, ASN-0034) and exhibit the routine divergence-at-shared-position argument. Both T3 and the Prefix definition are in ASN-0034, already cited; the corrected argument requires no new content. Internal.
```
