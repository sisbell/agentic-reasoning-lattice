## Question 11 [evidence]

> When COPY places a spec-set at V-position v in the target, does it create new POOM entries pointing to the SAME I-addresses as the source, leaving the granfilade entirely unmodified?

## KB Synthesis

Yes on the I-address reuse; no on "granfilade entirely unmodified." Here is the precise breakdown:

**COPY creates new POOM entries pointing to the same I-addresses** [ST-COPY (Finding 0064)]:

> "Unlike INSERT (which allocates fresh I-addresses), COPY shares the source's existing I-addresses in the target document's POOM via `insertpm`."

No call to `inserttextingranf` or `findisatoinsertgr` for content occurs. The permascroll portion of the granfilade — the I-address→byte mappings — is completely untouched.

**But the granfilade is not entirely unmodified.** The granfilade stores both permascroll content AND document POOM structures [SS-DUAL-ENFILADE (Finding 0012)]:

> "`granf` stores all content and document structure — the permascroll, document orgls, link orgls, and V→I mappings."

COPY calls `insertpm` [ST-VCOPY (Finding 0046)], which adds new crum entries to the target document's POOM tree — a subtree within the granfilade. So the granfilade's POOM section gains new V→I entries (pointing to the existing I-addresses), while its permascroll section is untouched.

**The spanfilade is also modified** [ST-COPY (Finding 0047)]:

> "COPY creates DOCISPAN entries proportional to the number of contiguous I-spans in the source content."

`docopy` calls `insertspanf(..., DOCISPAN)` [FC-CONTENT-SPANF-ISOLATION (Finding 0036)], making the copied I-addresses discoverable from the target document via FIND_DOCUMENTS.

**Summary:**

| Layer | Effect of COPY |
|-------|---------------|
| Permascroll (granf content) | **Unmodified** — same I-addresses, no new allocation |
| Target document POOM (granf structure) | **Modified** — new crum entries with existing I-addresses |
| Spanfilade DOCISPAN | **Modified** — new reverse-index entries |
| Source document POOM | **Unmodified** (frame condition) [FC-DELETE-CROSS-DOC] |

---

## Code Exploration

---

## Answer

**Yes.** COPY creates new POOM entries pointing to the **same I-addresses** as the source. The granfilade is entirely unmodified. Here is the complete proof from source.

---

### Entry point: `docopy` [`do1.c:45–65`]

```c
bool docopy(typetask *taskptr, typeisa *docisaptr, tumbler *vsaptr, typespecset specset)
{
  typeispanset ispanset;
  typeorgl docorgl;
  ...
  return (
     specset2ispanset (taskptr, specset, &ispanset, NOBERTREQUIRED)
  && findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
  && acceptablevsa (vsaptr, docorgl)
  && asserttreeisok(docorgl)

  /* the meat of docopy: */
  && insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset)

  &&  insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN)
  && asserttreeisok(docorgl)
  );
}
```

Three things happen:
1. **`specset2ispanset`** — converts the source V-spec to the underlying I-spans. This is a pure read/mapping: it walks the POOM to find what I-addresses the source V-positions currently map to. No data is written.
2. **`insertpm`** — the comment says "the meat of docopy." This is where the new POOM entries are created.
3. **`insertspanf`** — updates the spanfilade (for link retrieval indexing). Operates on `spanf`, not `granf`.

**There is no call to `inserttextingranf` or any granfilade-mutation function anywhere in `docopy`'s body.**

---

### The meat: `insertpm` [`orglinks.c:75–134`]

```c
bool insertpm(typetask *taskptr, tumbler *orglisa, typeorgl orgl, tumbler *vsaptr, typesporglset sporglset)
{
  tumbler lstream, lwidth;
  type2dbottomcruminfo linfo;
  typewid crumorigin, crumwidth;
  ...
  for (; sporglset; sporglset = (typesporglset) sporglset->xxxxsporgl.next) {
      unpacksporgl (sporglset, &lstream, &lwidth, &linfo);  // [line 101]

      movetumbler (&lstream, &crumorigin.dsas[I]);          // [line 105] — source I-address
      movetumbler (&lwidth,  &crumwidth.dsas[I]);           // [line 109] — source I-width
      movetumbler (vsaptr,   &crumorigin.dsas[V]);          // [line 113] — NEW target V-position
      shift = tumblerlength (vsaptr) - 1;
      inc   = tumblerintdiff (&lwidth, &zero);
      tumblerincrement (&zero, shift, inc, &crumwidth.dsas[V]);  // [line 117] — V-width

      insertnd (taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);  // [line 130]
      tumbleradd (vsaptr, &crumwidth.dsas[V], vsaptr);      // [line 131] — advance vsaptr
  }
  return (TRUE);
}
```

For each I-span in the ispanset, `insertpm`:
- Extracts **the existing I-address** (`lstream`) and I-width (`lwidth`) from the source span via `unpacksporgl` [`orglinks.c:101`]
- Places that I-address verbatim into `crumorigin.dsas[I]` [`orglinks.c:105`]
- Places the **target** V-position (`vsaptr`) into `crumorigin.dsas[V]` [`orglinks.c:113`]
- Inserts a new POOM crum via `insertnd` [`orglinks.c:130`]

The new POOM crum thus maps: *new V-position → same I-address as source*.

---

### What `unpacksporgl` extracts [`sporgl.c:178–202`]

```c
int unpacksporgl(typesporglset sporglptr, tumbler *streamptr, tumbler *widthptr, type2dbottomcruminfo *infoptr)
{
  if (((typeitemheader *)sporglptr)->itemid == ISPANID) {
      movetumbler (&((typeispan *)sporglptr)->stream, streamptr);  // I-address
      movetumbler (&((typeispan *)sporglptr)->width,  widthptr);   // I-width
      tumblerclear (&infoptr->homedoc);
  } else if (...SPORGLID...) {
      movetumbler (&((typesporgl *)sporglptr)->sporglorigin,  streamptr);  // I-address
      movetumbler (&((typesporgl *)sporglptr)->sporglwidth,   widthptr);   // I-width
      movetumbler (&((typesporgl *)sporglptr)->sporgladdress, &infoptr->homedoc);
  }
}
```

Both branches extract the **permascroll I-address** that already exists in the granfilade. Neither branch allocates new I-space.

---

### `insertspanf` [`spanf1.c:15–54`]

`insertspanf` inserts into `spanf` (the spanfilade, used for link-endpoint retrieval), not `granf`. It operates on the same I-addresses from `ispanset` — again, no new I-space is created.

---

### Contrast with `doinsert` [`do1.c:87–123`]

```c
bool doinsert(typetask *taskptr, typeisa *docisaptr, tumbler *vsaptr, typetextset textset)
{
  ...
  ret = (inserttextingranf(taskptr, granf, &hint, textset, &ispanset)  // allocates new I-space
      && docopy (taskptr, docisaptr, vsaptr, ispanset)                 // then adds POOM mapping
  );
  return(ret);
}
```

`doinsert` is the only path that mutates the granfilade — it calls `inserttextingranf` first (allocating new I-addresses on the permascroll), and then delegates to `docopy` to create the POOM mapping. `docopy` itself has no knowledge of granfilade allocation; it only wires up V→I mappings.

---

### Conclusion

When COPY places a spec-set at V-position *v* in the target:

1. The source V-spec is resolved to existing I-addresses via `specset2ispanset` (a pure read).
2. **`insertpm` creates new POOM crums** mapping the target V-positions to those **same I-addresses** — no new permascroll storage is allocated anywhere.
3. `insertspanf` records the I-spans in the spanfilade for link indexing — again no granfilade write.
4. **The granfilade is entirely unmodified.** The content already resident at those I-addresses is simply referenced by the new POOM entries.

This is the transclusion mechanism in action: multiple V-addresses in multiple documents can point to the same I-address, and COPY is the operation that creates that shared reference.
