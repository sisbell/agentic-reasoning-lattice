## Question 18 [gregory]

> When INSERT at position V:1.3 in a document shifts text content rightward via `makegappm`, and a link L has source endset referencing I-addresses of that shifted content, does `FOLLOWLINK` on L resolve the endset to the new V-positions (post-shift) by performing a fresh I-to-V lookup through the POOM, or does it cache any V-position from link creation time?

## KB Synthesis

**FOLLOWLINK performs a fresh I-to-V lookup through the current POOM — it always resolves to post-shift V-positions, never cached creation-time positions.**

## Mechanism

The resolution chain is documented in [SS-FOLLOWLINK] (Finding 0048):

1. `link2sporglset()` extracts the endset's I-addresses from the link orgl in I-space — these are permanent and unchanged by any edit
2. `linksporglset2specset()` converts those I-addresses to V-addresses by looking them up in the **specified document's current POOM**

The POOM is not read-only; it is the sole mutable layer [SS-POOM-MUTABILITY]. After INSERT at V:1.3, `makegappm` shifts all POOM entries in `[1.3, 2.1)` rightward by the insertion width [ST-INSERT, Finding 0054] — so the entry that previously mapped V:1.5 → I_content now maps V:1.8 → I_content. When FOLLOWLINK later resolves I_content through that POOM, it finds V:1.8, not the stale V:1.5.

## Empirical Confirmation

[INV-LINK-CONTENT-TRACKING] (Finding 0019) provides direct evidence:

> **V-address shifts**: When content is inserted within or before a linked region, the endset V-addresses shift to reflect the new positions:
> - Before: link on "here" at V 1.7 width 0.4
> - Insert "right " at position 1.7
> - After: link reports **1.13 width 0.4**

## Why No Caching Is Possible

Three interlocking properties make any V-position cache incorrect:

| Property | Entry |
|----------|-------|
| I-addresses never change after allocation | [INV-IADDR-IMMUTABILITY] |
| INSERT shifts V-positions in current POOM, leaves I-addresses untouched | [FC-INSERT-IADDR] |
| I-to-V filtering always goes through current POOM | [INV-ITOV-FILTERING] |

The link orgl stores I-addresses as its permanent reference point. V-positions are strictly derived, always computed live from the current POOM state. If a link's endpoint I-addresses have no current POOM mapping (e.g., after deletion), FOLLOWLINK silently returns empty — demonstrating it consults the POOM at call time, not at creation time [EC-GHOST-LINK].

## Clarification on Finding 0028

[SS-LINK-ENDPOINT] (Finding 0028) says "link endpoints are immutable V-spans fixed at creation time" and "follow_link always returns the original VSpan." This describes the *stored link data structure* — the link orgl itself does not update. What [SS-FOLLOWLINK] shows is that FOLLOWLINK doesn't return the stored V-span directly; it re-derives V-positions from stored I-addresses through the current POOM. The stored I-addresses are immutable; the V-positions derived from them are not.

---

## Code Exploration

Now I have everything needed to trace the full execution path. Here is the complete answer.

---

## Does FOLLOWLINK cache V-positions or perform a fresh I-to-V lookup?

**Answer: FOLLOWLINK performs a completely fresh I-to-V lookup through the POOM at follow time. No V-position is ever cached in a link.**

The architecture has three phases. Here is each one traced to specific lines.

---

### Phase 1: Link Creation — I-Addresses Are What Gets Stored

`docreatelink` [do1.c:195–221] does:

```c
specset2sporglset (taskptr, fromspecset, &fromsporglset, NOBERTREQUIRED)   // do1.c:214
insertendsetsinorgl (taskptr, linkisaptr, link, &fromvsa, fromsporglset, ...)  // do1.c:218
insertendsetsinspanf (taskptr, spanf, linkisaptr, fromsporglset, ...)          // do1.c:219
```

`specset2sporglset` [sporgl.c:14–33] converts the client's specset. If the client sent V-spans (`VSPECID`), it calls `vspanset2sporglset` [sporgl.c:35–65], which converts them immediately to I-addresses at creation time:

```c
(void) vspanset2ispanset (taskptr, orgl, vspanset, &ispanset);   // sporgl.c:48
// then for each ispan:
movetumbler (docisa, &sporglset->sporgladdress);          // sporgl.c:53 — document ISA
movetumbler (&ispanset->stream, &sporglset->sporglorigin); // sporgl.c:54 — I-address
movetumbler (&ispanset->width, &sporglset->sporglwidth);   // sporgl.c:55 — I-width
```

`vspanset2ispanset` [orglinks.c:397–402] calls `permute(..., V, ..., I)` [orglinks.c:404–422], which calls `retrieverestricted` on the POOM to read the current V→I mapping. The returned I-addresses are what get stored.

**What is stored in the link's ORGL:** `sporglorigin` (I-address) and `sporglwidth` (I-width) per endset entry. The link's own virtual address space uses positions like `1.x` (from-end), `2.x` (to-end), `3.x` (three-end) on the V-axis. The I-axis holds the I-addresses of the referenced content. **No V-position of the target content is persisted.**

---

### Phase 2: INSERT and makegappm — What Changes

`insertnd` [insertnd.c:15–111], when the enfilade is a POOM, calls `makegappm` first [insertnd.c:54]:

```c
case POOM:
    makegappm (taskptr, fullcrumptr, origin, width);   // insertnd.c:54
    // ...
    bothertorecombine = doinsertnd(fullcrumptr, origin, width, infoptr, index);
```

`makegappm` [insertnd.c:124–172] makes two cuts at the insertion point, then walks the children:

```c
for (ptr = findleftson (father); ptr; ptr = findrightbro (ptr)) {
    i = insertcutsectionnd(ptr, &fgrasp, &knives);
    switch (i) {
      case 1:  /* crum is to the right of the cut — must shift */
        tumbleradd(&ptr->cdsp.dsas[V], &width->dsas[V], &ptr->cdsp.dsas[V]);  // insertnd.c:162
        ivemodified (ptr);
        break;
    }
}
```

Only `cdsp.dsas[V]` — the V-dimension displacement — is modified. `cdsp.dsas[I]` (the I-dimension) is **untouched**. I-addresses are permanent identifiers for content; they never shift. The POOM now reflects a new V→I mapping: the same I-addresses are reached by higher V-addresses than before.

---

### Phase 3: FOLLOWLINK — The Fresh Lookup

`followlink` [fns.c:114–127] calls `dofollowlink` [do2.c:223–232]:

```c
return (
   link2sporglset (taskptr, linkisaptr, &sporglset, whichend, NOBERTREQUIRED)
&& linksporglset2specset (taskptr, &((typesporgl*)sporglset)->sporgladdress, sporglset, specsetptr, NOBERTREQUIRED));
```

**Step 3a — `link2sporglset` [sporgl.c:67–95]:** Queries the link's own ORGL to recover the stored I-addresses:

```c
tumblerincrement (&zero, 0, whichend, &vspan.stream);   // sporgl.c:81 — select from/to/three
tumblerincrement (&zero, 0, 1, &vspan.width);           // sporgl.c:82
if (context = retrieverestricted((typecuc*)orgl, &vspan, V, (typespan*)NULL, I, (typeisa*)NULL))
    // sporgl.c:83
```

For each context result:

```c
contextintosporgl ((type2dcontext*)c, (tumbler*)NULL, sporglptr, I);  // sporgl.c:86
```

`contextintosporgl` [sporgl.c:205–220] extracts:
```c
movetumbler (&context->totaloffset.dsas[I], &sporglptr->sporglorigin);  // sporgl.c:211 — I-address
movetumbler (&context->contextwid.dsas[I], &sporglptr->sporglwidth);    // sporgl.c:219 — I-width
```

After this step: we have the same I-addresses that were stored at link creation time. Nothing else.

**Step 3b — `linksporglset2specset` [sporgl.c:97–123]:** For each sporgl with a non-zero `sporgladdress`, calls:

```c
linksporglset2vspec(taskptr, homedoc, &sporglset, (typevspec*)specset, type);  // sporgl.c:116
```

`linksporglset2vspec` [sporgl.c:127–137] → `sporglset2vspanset` [sporgl.c:141–176]:

```c
(void) findorgl (taskptr, granf, homedoc, &orgl, type);  // sporgl.c:152 — opens target doc's POOM
// builds ispan from sporglorigin/sporglwidth, then:
vspansetptr = ispan2vspanset (taskptr, orgl, &ispan, vspansetptr);  // sporgl.c:157
```

`ispan2vspanset` [orglinks.c:389–394]:
```c
return permute(taskptr, orgl, ispanptr, I, vspansetptr, V);  // orglinks.c:393
```

`permute` [orglinks.c:404–422] → `span2spanset` [orglinks.c:425–454]:
```c
context = retrieverestricted((typecuc*)orgl, restrictionspanset, I,
                              (typespan*)NULL, V, (typeisa*)NULL);  // orglinks.c:435
```

**This is a live query into the target document's POOM.** It asks: "given these I-addresses, what V-addresses do they correspond to right now?" Because `makegappm` has already updated `cdsp.dsas[V]` on the shifted crums, `retrieverestricted` will now return the **post-insertion V-positions**.

---

### Summary

| Phase | Operation | V stored? | I stored? |
|-------|-----------|-----------|-----------|
| `docreatelink` | `vspanset2ispanset` converts client V→I at creation time | No | Yes (`sporglorigin`, `sporglwidth`) |
| `makegappm` on INSERT | Shifts `cdsp.dsas[V]` in target POOM | POOM updated | Unchanged |
| `dofollowlink` | `link2sporglset` reads stored I-addresses; `ispan2vspanset` queries live POOM | Computed fresh | Read from link |

The link's endset stores **only I-addresses** (`sporglorigin`/`sporglwidth`) in its ORGL. V-positions are **never cached**. At follow time, `ispan2vspanset` → `permute` → `retrieverestricted` performs a completely fresh I→V lookup through the current state of the target document's POOM, so any shifts caused by `makegappm` are automatically reflected. The invariance of I-addresses is the mechanism that makes links stable across insertions: the content is always found by its permanent I-address, and the current V-position is always computed on demand.
