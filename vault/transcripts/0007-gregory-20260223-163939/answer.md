## KB Synthesis

# Answer

Based on the knowledge base, `insertendsetsinspanf` creates **one spanfilade entry per I-span within each endset**, not one entry per endset.

## Key Evidence

From [SS-DOCISPAN] Finding 0047, which documents the same `insertspanf` mechanism used by `insertendsetsinspanf`:

> "When `insertspanf` is called, it iterates over the `ispanset` linked list and makes one `insertnd` call per `typeispan` struct. Each `typeispan` represents a contiguous range of I-addresses (with a `stream` start and `width` size), so inserting 10 contiguous bytes creates 1 DOCISPAN entry, not 10."

The code structure is:
```c
for (; sporglset; sporglset = next) { 
    ... 
    insertnd(...); 
}
```

## Concrete Example

From [ST-LINK-CREATE] Finding 0037:

> "When document C transcludes 'AA' from A and 'BB' from B, the contiguous V-span 1.1..1.4 in C maps to two disjoint I-address regions. The link subsystem handles this transparently: `vspanset2sporglset` calls `vspanset2ispanset` which walks the POOM (permutation matrix) to discover all I-address regions, producing one I-span per contiguous region."

If a link is created with source endset covering this content:
- **Input**: One V-span `[1.1, 1.4)` covering "AABB" in document C
- **Conversion**: Produces two I-spans (one for "AA" from doc A, one for "BB" from doc B)
- **Spanfilade entries**: **Two entries** — one per I-span

The granularity is per-contiguous-I-range, not per-endset. This means links with fragmented content (transcluded from multiple sources) create multiple spanfilade entries for a single endset.

## Code Exploration

Now I have traced the complete execution path. Let me provide the answer with all code citations:

---

## Answer

**`insertendsetsinspanf` creates one spanfilade entry per I-span within each endset.**

If a source endset contains two non-contiguous I-ranges, **two spanfilade entries result** (one per I-span).

### Code Evidence

**1. `insertendsetsinspanf` calls `insertspanf` once per endset** [do2.c:116-128]:

```c
bool insertendsetsinspanf(..., typesporglset fromsporglset, typesporglset tosporglset, typesporglset threesporglset)
{
  if (!(insertspanf(taskptr,spanfptr,linkisaptr,fromsporglset,LINKFROMSPAN)
      &&insertspanf(taskptr,spanfptr,linkisaptr,tosporglset,LINKTOSPAN)))
    return (FALSE);
  if (threesporglset) {
    if(!insertspanf(taskptr,spanfptr,linkisaptr,threesporglset,LINKTHREESPAN))
      return (FALSE);
  }
  return(TRUE);
}
```

**2. `insertspanf` iterates through each I-span in the sporglset** [spanf1.c:25-51]:

```c
for (; sporglset; sporglset = (typesporglset)((typeitemheader *)sporglset)->next) {
  if (((typeitemheader *)sporglset)->itemid == ISPANID) {
    movetumbler (&((typeispan *)sporglset)->stream, &lstream);
    movetumbler (&((typeispan *)sporglset)->width, &lwidth);
    ...
  } else if (((typeitemheader *)sporglset)->itemid == SPORGLID) {
    movetumbler (&((typesporgl *)sporglset)->sporglorigin, &lstream);
    movetumbler (&((typesporgl *)sporglset)->sporglwidth, &lwidth);
    ...
  }
  movetumbler (&lstream, &crumorigin.dsas[SPANRANGE]);
  movetumbler (&lwidth, &crumwidth.dsas[SPANRANGE]);
  insertnd(taskptr,(typecuc*)spanfptr,&crumorigin,&crumwidth,&linfo,SPANRANGE);
}
```

The critical line is [spanf1.c:51]: **`insertnd` is called once per iteration**, creating one spanfilade entry per sporglset item.

**3. Each sporglset item represents one contiguous I-span** [sporgl.c:49-57]:

When V-spans are converted to I-spans, each resulting I-span becomes a separate sporgl:

```c
for (; ispanset; ispanset = ispanset->next) {
  sporglset = (typesporgl *) taskalloc (taskptr, sizeof(typesporgl));
  sporglset->itemid = SPORGLID;
  sporglset->next = NULL;
  movetumbler (docisa, &sporglset->sporgladdress);
  movetumbler(&ispanset->stream,&sporglset->sporglorigin);
  movetumbler (&ispanset->width, &sporglset->sporglwidth);
  *sporglsetptr = (typesporglset)sporglset;
  sporglsetptr = (typesporglset *)&sporglset->next;
}
```

### Execution Flow

For a link with a source endset containing two non-contiguous I-ranges `[1.1.1, 2)` and `[10.1.1, 2)`:

1. `specset2sporglset` converts the endset to a sporglset with **two items** (one per I-range) [sporgl.c:14-33, 35-65]
2. `insertendsetsinspanf` calls `insertspanf` with this two-item sporglset [do2.c:119]
3. `insertspanf` iterates twice, calling `insertnd` **twice** [spanf1.c:25, 51]
4. Result: **Two spanfilade entries**, one indexing `[1.1.1, 2)` and one indexing `[10.1.1, 2)`

This design allows the spanfilade to efficiently retrieve links by any I-span fragment within an endset, not just complete endsets.
