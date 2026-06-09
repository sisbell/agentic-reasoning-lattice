## Question 13 [evidence]

> When an endset's V-span maps to non-contiguous I-addresses, does CREATELINK automatically split it into multiple sporgl entries, and does this splitting happen for all three endsets uniformly?

## KB Synthesis

Yes on both counts.

**Automatic splitting for non-contiguous V-spans**

When `domakelink` processes a V-span that maps to non-contiguous I-addresses (e.g., a span covering transcluded content from two sources), `vspanset2sporglset` (`sporgl.c:35-65`) automatically decomposes it. The inner loop at `sporgl.c:49-58` iterates over every I-span returned by `vspanset2ispanset` and creates a separate sporgl per contiguous I-address region. The front end passes a single V-span; the backend produces N sporgls. [ST-LINK-CREATE / Finding 0037]

The postcondition: `link.source_endset = { sporgl(origin=i.start, width=i.width, doc=d) | i ∈ V_to_ISpans(d, vspan) }` — cardinality is determined by the I-space fragmentation of the V-span, not the number of V-spans provided. [SS-LINK-ENDPOINT / Finding 0037]

**Uniform application to all three endsets**

All three endsets (FROM, TO, THREE) go through the same `vspanset2sporglset` conversion before being passed to `insertendsetsinspanf()`, which indexes each sporglset tagged with `LINKFROMSPAN=1`, `LINKTOSPAN=2`, `LINKTHREESPAN=3` respectively. [INT-SPORGL-LINK-INDEX / Finding 0013]

There is no special handling for any particular endset — the splitting is a property of `vspanset2sporglset` itself, which `domakelink` calls uniformly for each endpoint specset. [SS-RETRIEVE-ENDSETS / Finding 0035]

The one caveat: the concrete example in Finding 0037 specifically tests the source endset. The THREE endset (type endpoint) typically references the bootstrap document's type registry at contiguous addresses, so it rarely triggers multi-sporgl splitting in practice — but the code path is identical.

---

## Code Exploration

All citations verified. Here is the complete answer.

---

## Does CREATELINK Split Non-Contiguous I-Addresses into Multiple Sporgl Entries?

**Yes.** When an endset's V-span maps to non-contiguous I-addresses, `CREATELINK` automatically splits it into multiple sporgl entries — one per contiguous I-address range. This splitting is **structurally uniform** across all three endsets, with one minor asymmetry for endset 3 at insertion time.

---

### Complete Call Chain

```
fns.c:100          createlink()
  → do1.c:195      docreatelink()
      → do1.c:214  specset2sporglset()   [for endset 1: from]
      → do1.c:215  specset2sporglset()   [for endset 2: to]
      → do1.c:216  specset2sporglset()   [for endset 3: three]
          → sporgl.c:25  vspanset2sporglset()
              → orglinks.c:401  vspanset2ispanset()
                  → orglinks.c:404  permute()
                      → orglinks.c:435  retrieverestricted()   ← finds all contexts
                      → orglinks.c:439  loop over contexts     ← one I-span per context
      → do1.c:219  insertendsetsinspanf()
          → do2.c:119  insertspanf()  [LINKFROMSPAN]
          → do2.c:120  insertspanf()  [LINKTOSPAN]
          → do2.c:123  insertspanf()  [LINKTHREESPAN, conditional]
```

---

### Stage 1: V→I Conversion and Non-Contiguity Detection

The splitting is determined in `span2spanset()` [orglinks.c:425]:

```c
context = retrieverestricted((typecuc*)orgl, restrictionspanptr, restrictionindex,
                             (typespan*)NULL, targindex, (typeisa*)NULL);
for (c = context; c; c = c->nextcontext) {           /* [orglinks.c:439] */
    context2span (c, restrictionspanptr, restrictionindex, &foundspan, targindex);
    nextptr = (typespan *)onitemlist (taskptr, (typeitem*)&foundspan, (typeitemset*)targspansetptr);
}
```

`retrieverestricted()` [orglinks.c:435] walks the granfilade/enfilade tree and returns **one context record per contiguous mapped region**. A V-span that covers two non-adjacent I-address ranges produces two context records. The `for` loop at line 439 converts each context into a separate I-span, giving one I-span per contiguous region.

---

### Stage 2: One Sporgl per I-span

In `vspanset2sporglset()` [sporgl.c:35]:

```c
for (; vspanset; vspanset = vspanset->next) {
    (void) vspanset2ispanset (taskptr, orgl, vspanset, &ispanset);
    for (; ispanset; ispanset = ispanset->next) {       /* [sporgl.c:49] */
        sporglset = (typesporgl *) taskalloc (taskptr, sizeof(typesporgl));
        sporglset->itemid = SPORGLID;
        sporglset->next = NULL;
        movetumbler (docisa, &sporglset->sporgladdress);
        movetumbler(&ispanset->stream, &sporglset->sporglorigin);   /* I-start */
        movetumbler (&ispanset->width, &sporglset->sporglwidth);    /* I-width */
        *sporglsetptr = (typesporglset)sporglset;
        sporglsetptr = (typesporglset *)&sporglset->next;
    }
}
```

The inner loop at [sporgl.c:49] allocates a fresh `typesporgl` for **every I-span** returned by `vspanset2ispanset`. A V-span with two non-contiguous I-regions exits `vspanset2ispanset` as two I-spans, and exits `vspanset2sporglset` as two chained sporgl entries.

---

### Stage 3: All Three Endsets Use the Same Path

`docreatelink()` [do1.c:214–216] calls `specset2sporglset()` three times with identical arguments:

```c
specset2sporglset (taskptr, fromspecset,   &fromsporglset,   NOBERTREQUIRED)  /* do1.c:214 */
specset2sporglset (taskptr, tospecset,     &tosporglset,     NOBERTREQUIRED)  /* do1.c:215 */
specset2sporglset (taskptr, threespecset,  &threesporglset,  NOBERTREQUIRED)  /* do1.c:216 */
```

No code path distinguishes endset 1 from endset 2 from endset 3 during V→I conversion or sporgl creation. The same `specset2sporglset` → `vspanset2sporglset` → `vspanset2ispanset` → `permute` → `span2spanset` chain runs for all three.

---

### The One Asymmetry: Endset 3 is Optional at Insertion

In `insertendsetsinspanf()` [do2.c:116–128]:

```c
if (!(insertspanf(taskptr, spanfptr, linkisaptr, fromsporglset, LINKFROMSPAN)
      && insertspanf(taskptr, spanfptr, linkisaptr, tosporglset,  LINKTOSPAN)))
    return (FALSE);
if (threesporglset) {                                            /* do2.c:122 */
    if (!insertspanf(taskptr, spanfptr, linkisaptr, threesporglset, LINKTHREESPAN))
        return (FALSE);
}
```

Endsets 1 and 2 are unconditional. Endset 3 is guarded by `if (threesporglset)` — it is skipped if null. The same guard appears in `insertendsetsinorgl()` [do2.c:136]: `if (threevsa && threesporglset)`.

This is not asymmetry in the **splitting** behavior. It is simply that endset 3 is an optional endset. When it is present and non-null, `insertspanf()` processes its sporgl list with the same inner loop [spanf1.c:25–52] that handles endsets 1 and 2.

---

### Summary

| Question | Answer |
|---|---|
| Does CREATELINK split non-contiguous I-ranges into multiple sporgls? | **Yes** — one sporgl per contiguous I-region, via the context loop at [sporgl.c:49] |
| Where is non-contiguity detected? | `retrieverestricted()` at [orglinks.c:435], which returns one context per region |
| Is splitting uniform across all three endsets? | **Yes** — identical code path for all three via [do1.c:214–216] |
| Is there any endset asymmetry? | **Yes, one**: endset 3 has a null-guard at [do2.c:122] making it optional; when present it is treated identically |
