## Question 16 [gregory]

> Does DELETE on a span that covers the entire document content (full-width delete) leave the POOM in a state where subsequent retrieval returns an empty specset, and does the tree height remain at whatever level it grew to during prior insertions since `levelpull` is disabled?

## KB Synthesis

Yes to both.

**Full-width delete → empty retrieval**

When DELETE covers the entire document, `deletend` Case 1 (`disown` + `subtreefree`) removes all height-0 bottom crums. After the operation, the POOM tree has no bottom nodes and maps no V-addresses to I-addresses. `retrieve_vspanset` returns zero-width content — functionally empty. [ST-DELETE, Finding 0058]

**Tree height persists**

`recombinend` is called during rebalancing and invokes `levelpull` on the apex, but `levelpull` is disabled — it immediately returns 0 without executing the collapse logic. Height increases via `levelpush` are permanent; they are never reversed. [INV-ENFILADE-MINIMALITY, SS-ENFILADE-TREE, Finding 0058]

Concrete outcome: a document grown to height 3 that has all content deleted ends up with:
```
Fullcrum (height=3, numberofsons=2)    ← height unchanged
  ├─ Height-2 node (numberofsons=0)    ← empty, not freed
  └─ Height-2 node (numberofsons=0)    ← empty, not freed
```

**Additional consequence**

This post-delete empty state is structurally distinct from the never-filled state produced by `createenf` (height=1, one zero-width bottom crum). The never-filled state satisfies the implicit precondition `has_bottom_node(enf(doc))` required by `firstinsertionnd`. The delete-everything state does not — it has empty intermediate nodes but no bottom crums. Attempting INSERT or VCOPY into a delete-everything document crashes with a null pointer dereference (Bug 0019). [EC-EMPTY-DOC, Finding 0058, Finding 0064]

---

## Code Exploration

I now have the full picture from the source. Here is the complete answer:

---

## Full-Width Delete: POOM State and Tree Height After `deletend`

### 1. Does the POOM become logically empty after a full-width delete, causing subsequent retrieval to return an empty specset?

**Yes — and the specific mechanism that enforces it is an explicit NULL-children guard in `setwispnd`.**

#### Call chain

```
dodeletevspan          [do1.c:158–167]
  → deletevspanpm      [orglinks.c:145–152]
    → deletend         [edit.c:31–76]
      → setwispupwards [wisp.c:83–111]
        → setwispnd    [wisp.c:171–228]
```

**`dodeletevspan`** [`do1.c:158–167`] simply acquires the document's POOM orgl and delegates:

```c
bool dodeletevspan(typetask *taskptr, typeisa *docisaptr, typevspan *vspanptr)
{
    return (
       findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
    && deletevspanpm (taskptr, docisaptr, docorgl, vspanptr));
}
```

**`deletevspanpm`** [`orglinks.c:145–152`] forwards directly to `deletend` on the POOM, using the V-dimension index:

```c
bool deletevspanpm(typetask *taskptr, tumbler *docisaptr, typeorgl docorgl, typevspan *vspanptr)
{
    if (iszerotumbler(&vspanptr->width))
        return (FALSE);
    deletend((typecuc*)docorgl, &vspanptr->stream, &vspanptr->width, V);
    logbertmodified(docisaptr, user);
    return (TRUE);
}
```

**`deletend`** [`edit.c:31–76`] sets up two knife cuts (`origin` and `origin+width`), finds the covering node via `newfindintersectionnd`, then walks its children and classifies each:

```c
for (ptr = (typecuc *) findleftson (father); ptr; ptr = next) {
    next = (typecuc *) findrightbro((typecorecrum*)ptr);
    switch (deletecutsectionnd ((typecorecrum*)ptr, &fgrasp, &knives)) {
      case 1:
        disown ((typecorecrum*)ptr);      // edit.c:59
        subtreefree ((typecorecrum*)ptr); // edit.c:60
        break;
      case 2:
        tumblersub (&ptr->cdsp.dsas[index], width, &ptr->cdsp.dsas[index]); // edit.c:63
        break;
    }
}
setwispupwards (father,1); // edit.c:74
recombine (father);        // edit.c:75
```

For a **full-width delete** (the span covers the entire V-extent of the document), every crum bottom-node is classified `case 1` — completely inside the deletion interval — so every crum is `disown`ed and recursively freed via `subtreefree`. The covering `father` node is left with **no children** (`leftson == NULL`).

#### The zero-propagation guarantee

`setwispupwards` walks upward calling `setwisp` → `setwispnd` on each ancestor. **`setwispnd`** [`wisp.c:171–228`] has an explicit early branch for the no-children case:

```c
if ((ptr = findleftson (father)) == NULL) {
    /* All children deleted - clear width and mark modified */
    clear (&father->cdsp, sizeof(father->cdsp)); // wisp.c:187
    clear (&father->cwid, sizeof(father->cwid)); // wisp.c:188
    ivemodified((typecorecrum*)father);           // wisp.c:189
    return (TRUE);
}
```

This clears **both** `cdsp` (displacement) and `cwid` (width) on the node, marks it modified, and returns `TRUE` to continue propagating upward. For a full-width delete, this eventually reaches the POOM apex (fullcrum), whose `cwid` and `cdsp` are both zeroed.

#### Retrieval sees empty

`isemptyorgl` [`orglinks.c:539–544`] tests exactly those two fields on the apex:

```c
bool isemptyorgl(typeorgl fullcrumptr)
{
    return (
       iszerolock ((tumbler*)&((typecuc*)fullcrumptr)->cwid, widsize(POOM))
    && iszerolock ((tumbler*)&((typecuc*)fullcrumptr)->cdsp, dspsize(POOM)));
}
```

After the full-width delete, both are zero → `isemptyorgl` returns `TRUE`.

`doretrievedocvspanset` [`do1.c:322–336`] uses this directly:

```c
if (isemptyorgl (docorgl)) {
    *vspansetptr = NULL;  /* Empty document returns empty vspanset */
    return TRUE;
}
```

For the content-retrieval path (`doretrievev` → `specset2ispanset` → `permute` → `span2spanset` → `retrieverestricted` → `findcbcinarea2d`), the empty POOM means `findcbcinarea2d` [`retrie.c:229–268`] finds no qualifying crums, the context list remains NULL, no ispanset entries are produced, and `ispanset2vstuffset` returns an empty vstuffset.

**Conclusion:** A full-width delete leaves the POOM apex with `cwid = 0` and `cdsp = 0`. Both retrieval paths (`doretrievedocvspanset` and `doretrievev`) return empty results.

---

### 2. Does the tree height remain at whatever level it grew to during prior insertions, since `levelpull` is disabled?

**Yes — `levelpull` is unconditionally disabled; the height field can only ever grow.**

#### `levelpull` is a stub

`genf.c:318–342`:

```c
int levelpull(typecuc *fullcrumptr)
{
/*  typecuc *ptr; */
return(0);
/*
    if (!isfullcrum (fullcrumptr))
        ...
    if (fullcrumptr->numberofsons > 1)
        return;
    if (fullcrumptr->height <= 1)
        return;
    ptr = (typecuc *) findleftson (fullcrumptr);
    dspadd (&fullcrumptr->cdsp, &ptr->cdsp, &fullcrumptr->cdsp, ...);
    disown (ptr);
    fullcrumptr->height--;
    transferloaf (ptr, fullcrumptr);
    setwispupwards (fullcrumptr,1);
    freecrum (ptr);
*/
}
```

The entire body — including `fullcrumptr->height--` — is commented out. The function returns `0` immediately.

#### `levelpull` is called from both recombine paths

`recombineseq` (for GRANfilades) [`recombine.c:66–68`]:

```c
if (father->isapex)
    levelpull (father);   // no-op
```

`recombinend` (for POOM and SPAN) [`recombine.c:129–131`]:

```c
if (father->isapex)
    levelpull (father);   // no-op
```

Both `recombine` callsites in `deletend` [`edit.c:75`] and `insertnd` [`insertnd.c:76`] dispatch to `recombinend` for POOM enfilades [`recombine.c:31–33`]. Neither path can ever reduce the height.

#### `levelpush` is fully active and increases height

`genf.c:263–294` (abbreviated):

```c
int levelpush(typecuc *fullcrumptr)
{
    new = (typecuc *)createcrum ((INT)fullcrumptr->height, ...);
    new->isleftmost = TRUE;
    transferloaf (fullcrumptr, new);
    fullcrumptr->height++;           // genf.c:285 — increments height
    adopt ((typecorecrum*)new, SON, (typecorecrum*)fullcrumptr);
    ...
}
```

`levelpush` is called from `splitcrumupwards` (invoked from `insertcbcnd` [`insertnd.c:272`] and `rearrangend` [`edit.c:141`]) whenever too many sons accumulate at a level. Each push bumps `height` by 1. There is no corresponding decrement anywhere in live code.

#### Post-delete state of the height field

After a full-width delete:

1. `deletend` removes all crums → `setwispnd` zeros `cwid`/`cdsp` on the apex
2. `recombine(father)` → `recombinend(father)` [`recombine.c:112–113`]:
   ```c
   if (father->height < 2  || !father->modified)
       return(0);
   ```
   If the apex height is 1, early return — nothing changes. If height ≥ 2, the take-nephew loop runs over an empty sons array (n=0), does nothing, then calls `levelpull(father)` — which is a no-op.
3. **The `height` field on the apex is not touched.** It retains whatever value was accumulated during prior insertions.

**Conclusion:** The tree height is permanently frozen at its high-water mark. A document that received N insertions forcing K `levelpush` calls will have `height == K` on the POOM apex forever. Subsequent full-width deletes leave the tree structurally hollow — zero width, no bottom crums — but at its original height. Re-insertion into this "empty tall tree" will follow the `isemptyenfilade` branch in `doinsertnd` [`insertnd.c:191–194`]:

```c
if (isemptyenfilade (father)) {
    firstinsertionnd (father, origin, width, infoptr);
    return(FALSE);
}
```

`firstinsertionnd` [`insertnd.c:199–218`] handles the case where `findleftson(father) == NULL` (the original bottom crum was freed by `subtreefree`) by creating a fresh bottom crum and adopting it under the apex — so re-insertion works correctly despite the orphaned height.
