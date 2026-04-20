## Question 14 [gregory]

> When two logically distinct COPY operations produce I-address-adjacent mappings in a target POOM and `isanextensionnd` silently merges them into one crum, is there any residual record that the crum originated from two separate operations, or is the merge information-destroying?

## KB Synthesis

The merge is **information-destroying** with respect to operation count and per-operation boundaries.

## What the crum retains after merging

From [SS-POOM-BOTTOM-CRUM] (Finding 0076), a POOM bottom crum has exactly four fields:

```
BottomCrum = {
  origin: { dsas[I]: Tumbler, dsas[V]: Tumbler },
  width:  { dsas[I]: Tumbler, dsas[V]: Tumbler }
}
```

No operation count, no timestamp, no list of contributing spans. When [ST-VCOPY] Finding 0046 describes the extension path — `isanextensionnd` matches, `crum.width` is widened in place at `insertnd.c:243` — the prior boundary simply vanishes. There is no residual record that the region was assembled from two operations versus one.

[INV-VSPAN-CONSOLIDATION] (Finding 0028) confirms this explicitly: after 100 separate single-character inserts, `retrieve_vspanset` returns `span_count: 1`. The enfilade makes no distinction between a single bulk operation and N sequential ones that happen to coalesce.

## What is partially preserved

The one discriminating field is `homedoc`. From [PRE-COPY] Finding 0046:

> The extension check's `homedoc` condition means crums from different source documents are never merged.

Two COPYs from **different** home documents cannot coalesce — they always produce separate crums, preserving the fact that they originated from distinct sources. But two COPYs from the **same** home document with I-address-adjacent, V-address-adjacent results are indistinguishable from a single COPY of the combined range after the merge.

## The granfilade is not affected

The underlying I-addresses allocated by each COPY remain permanently and individually in the granfilade ([INV-IADDR-IMMUTABILITY], [FC-GRANF-ON-DELETE]). What is lost is only the POOM-level record of how those I-addresses were placed — the cut point between the two operations' contributions is erased. You can still address individual bytes through the granfilade, but you cannot reconstruct from the POOM alone that two separate operations were responsible.

**Summary:** The merge loses all information about operation boundaries and count. Only cross-document provenance (via `homedoc`) survives. Same-document multi-COPY history is not preserved.

---

## Code Exploration

I now have all the source I need. Let me compile the full answer.

---

## Answer: Is the `isanextensionnd` Merge Information-Destroying?

**Yes, unconditionally. The merge destroys the boundary information. No residual record is kept.**

Here is the full trace.

---

### 1. The Bottom-Crum Data Structure Has Exactly One Identity Field

The 2D bottom crum (`type2dcbc`) is defined in `enf.h:109-131`:

```c
struct struct2dcbc {
    ...
    typewid cwid;          /* combined width in both I and V */
    typedsp cdsp;          /* displacement: origin in both I and V */
    type2dbottomcruminfo  c2dinfo;   /* ← the sole identity payload */
};
```

And `type2dbottomcruminfo` is defined in `wisp.h:107-109`:

```c
typedef struct struct2dbottomcruminfo {
    tumbler homedoc;
} type2dbottomcruminfo;
```

**`homedoc` is the entire identity record for a POOM bottom crum.** It is a single tumbler — the ISA of the source document. There is no `origin_count`, no sub-span list, no operation log, no boundary marker.

---

### 2. What `isanextensionnd` Actually Tests

`insertnd.c:301-309`:

```c
bool isanextensionnd(typecbc *ptr, typedsp *offsetptr, typedsp *originptr,
                     type2dbottomcruminfo *infoptr)
{
  typedsp grasp, reach;
  bool lockeq();
    if (!tumblereq (&infoptr->homedoc, &((type2dcbc *)ptr)->c2dinfo.homedoc))
        return (FALSE);
    prologuend ((typecorecrum*)ptr, offsetptr, &grasp, &reach);
    return (lockeq (reach.dsas, originptr->dsas, (unsigned)dspsize(ptr->cenftype)));
}
```

Two conditions must both hold:

1. **Same `homedoc`** — the new crum's source document ISA equals the existing crum's `c2dinfo.homedoc` (line 305).
2. **Exact adjacency in ALL dimensions** — `lockeq` compares `reach.dsas[0..dspsize-1]` to `originptr->dsas[0..dspsize-1]`. For POOM, `dspsize(POOM) == DSPSIZEPM == 2` (`wisp.h:27`), so both the I and V right-edges of the existing crum must exactly equal the I-V origin of the new insertion.

This is a stricter condition than I-adjacency alone: the two COPY operations must land contiguously in **both** I-space and V-space simultaneously.

---

### 3. The Merge Operation

When `isanextensionnd` returns `TRUE`, `insertcbcnd` (insertnd.c:249-258) does exactly this:

```c
for (ptr = findleftson (father); ptr; ptr = findrightbro (ptr)) {
    if (isanextensionnd ((typecbc*)ptr, grasp, origin, infoptr)) {
        dspadd (&ptr->cwid, width, &ptr->cwid, (INT)father->cenftype);  /* line 251 */
        ivemodified (ptr);
        setwispupwards (father,1);
        ...
        return(FALSE);
    }
}
```

**Only one field is mutated**: `ptr->cwid` is incremented by `width` via `dspadd`. This is integer addition on the tumbler — a write-only, non-invertible operation.

| Field | Before merge | After merge |
|---|---|---|
| `cdsp.dsas[I]` | I-origin of op1 | **unchanged** |
| `cdsp.dsas[V]` | V-origin of op1 | **unchanged** |
| `cwid.dsas[I]` | width1_I | **width1_I + width2_I** |
| `cwid.dsas[V]` | width1_V | **width1_V + width2_V** |
| `c2dinfo.homedoc` | source doc ISA | **unchanged** |

No new crum is created (`createcrum` at line 260 is in the `else` branch that is skipped). The `infoptr` for the second operation — which carries the second copy's origin and width — is used only to compute the merged `cwid`, then discarded. The internal I/V boundary between the two operations is arithmetically summed away.

---

### 4. The Path That Creates the Crum in the First Place

For comparison: when no merge occurs, `insertcbcnd` creates a fresh crum at lines 260-267:

```c
new = createcrum (0, (INT)father->cenftype);
reserve (new);
adopt (new, SON, (typecorecrum*)father);
dspsub (origin, grasp, &new->cdsp, (INT)father->cenftype);   /* sets cdsp */
movewisp (width, &new->cwid);                                  /* sets cwid */
move2dinfo (infoptr, &((type2dcbc *)new)->c2dinfo);            /* sets homedoc */
```

All three fields (`cdsp`, `cwid`, `c2dinfo`) are set from the incoming operation data. When the merge path fires instead, only `cwid` is updated; the other two carry over from op1, and op2's origin/info is gone.

---

### 5. How `homedoc` Is Populated per COPY Call

The chain from `docopy` → `insertpm` → `unpacksporgl` in `sporgl.c:178-187`:

```c
int unpacksporgl(typesporglset sporglptr, tumbler *streamptr,
                 tumbler *widthptr, type2dbottomcruminfo *infoptr)
{
    ...
    } else if (((typeitemheader *)sporglptr)->itemid == SPORGLID) {
        movetumbler (&((typesporgl *)sporglptr)->sporglorigin, streamptr);
        movetumbler (&((typesporgl *)sporglptr)->sporglwidth, widthptr);
        movetumbler (&((typesporgl *)sporglptr)->sporgladdress, &infoptr->homedoc);
    }
```

`sporgladdress` is the ISA of the source document. This is the only identity datum passed down through `insertpm` → `insertnd` → `insertcbcnd` → `isanextensionnd`. **There is no field for "I-origin within source"** or any other per-operation annotation beyond `homedoc`.

---

### 6. No Secondary Record Survives

`docopy` (do1.c:53-65) also calls `insertspanf`:

```c
&& insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset)
&&  insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN)
```

The spanfilade records which I-spans belong to a document — the *inverse* mapping. But if the two COPY operations draw on I-adjacent spans from the same source, `putvspaninlist` in `orglinks.c:346-347` coalesces them too:

```c
if (!spancmp) {
    tumbleradd (&ptr->width, &spanptr->width, &ptr->width);   /* merge adjacent */
    return(0);
}
```

So the spanfilade also loses the inter-operation boundary for adjacent I-spans from the same source document.

The granfilade records raw content and has no knowledge of COPY operation identity at all.

---

### Summary

The merge performed by `isanextensionnd` + `insertcbcnd:251` is **fully and irrecoverably information-destroying**:

- The merged crum records only: (I-start of op1, V-start of op1, combined I-width, combined V-width, shared homedoc).
- The internal I/V boundary between op1 and op2 is gone.
- The fact that two distinct operations contributed is gone.
- The `type2dbottomcruminfo` structure has a single field (`homedoc`), providing no space for boundary or count metadata.
- The `dspadd` at `insertnd.c:251` is scalar addition on tumblers — not annotated, not logged, and not reversible without out-of-band knowledge of the original widths.
- No other data structure (spanfilade, granfilade) preserves per-COPY-operation provenance.

The design treats the merged span as if it were always a single contiguous copy. From the perspective of the enfilade, it is indistinguishable from having issued one COPY that covered the combined I-span in the first place.
