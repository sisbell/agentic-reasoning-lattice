## Question 13 [evidence]

> During the I→V conversion of a read endset, are unreferenced I-addresses (those in no current POOM) silently filtered, and does this produce a partial or empty endset for ghost links?

## KB Synthesis

Yes, on both counts. The filtering is universal and the result can be partial or empty.

## Mechanism

The silent filtering is implemented in the shared I→V conversion path, not in any operation-specific code [INV-ITOV-FILTERING]. The chain is:

```
linksporglset2specset() → sporglset2vspanset() → ispan2vspanset()
  → permute() → span2spanset() → retrieverestricted()
```

At `span2spanset()` (`orglinks.c:425-449`), `retrieverestricted()` searches the target document's POOM for each I-address. When it returns NULL (no V-position mapping exists), the I-address is dropped without error or notification. Both FOLLOWLINK and RETRIEVEENDSETS share this same path [SS-FOLLOWLINK, SS-RETRIEVE-ENDSETS].

## Result for Ghost Links

Three observable states [EC-GHOST-LINK]:

1. **All I-addresses live** → full endset returned
2. **Some unreferenced** → partial endset (only I-addresses with current POOM mappings survive)
3. **All unreferenced** → empty result `[]`, operation returns success (`works: true`)

The operation never errors — an empty result is a valid successful outcome, not a failure [PRE-FOLLOWLINK]. This is by design: the permanent layer holds the I-addresses eternally [INV-IADDR-IMMUTABILITY], and the POOM is the mutable layer that determines current V-position resolvability [SS-POOM-MUTABILITY].

## Why This Matters

The filtering is a **universal invariant of I→V conversion**, not an operation-level guard: `∀ op returning V-addresses: v ∈ result(op) → ∃ d, i : poom.d(v) = i` [INV-ITOV-FILTERING]. Consequently, a caller cannot distinguish "link has no endpoint content" from "link endpoint I-addresses are simply not in this document's POOM" — both produce the same empty result.

---

## Code Exploration

I now have everything I need. Here is the complete answer.

---

## I→V Conversion of Read Endsets: Ghost Link Behavior

### Short Answer

**Yes. Unreferenced I-addresses are silently filtered.** An endset whose I-addresses map to no POOM crum returns as a reduced or empty V-spanset — no error, no signal, no record of what was lost.

---

### The Conversion Path

Following a link calls `dofollowlink` [do1.c:223-232]:

```c
bool dofollowlink(typetask *taskptr, typeisa *linkisaptr, typespecset *specsetptr, INT whichend)
{
  typesporglset sporglset;
  return (
     link2sporglset (taskptr, linkisaptr, &sporglset, whichend, NOBERTREQUIRED)
  && linksporglset2specset (taskptr, &((typesporgl *)sporglset)->sporgladdress,
                            sporglset, specsetptr, NOBERTREQUIRED));
}
```

The endsets come back as I-address spans (sporgls). When these are subsequently converted to V-addresses — e.g., via `ispan2vspanset` to prepare the specset for retrieval — the path is:

**`ispan2vspanset`** → **`permute`** → **`span2spanset`** → **`retrieverestricted`** → **`findcbcinarea2d`** (applies `crumqualifies2d`) → either a context list or nothing

---

### The Silent Filter: `span2spanset` [orglinks.c:425–454]

```c
typespanset *span2spanset(typetask *taskptr, typeorgl orgl, typespanset restrictionspanptr,
                           INT restrictionindex, typespanset *targspansetptr, INT targindex)
{
  typecontext *context, *c, *retrieverestricted();
  ...
  context = retrieverestricted((typecuc*)orgl, restrictionspanptr, restrictionindex,
                               (typespan*)NULL, targindex, (typeisa*)NULL);  // line 435
  for (c = context; c; c = c->nextcontext) {
      context2span (c, restrictionspanptr, restrictionindex, &foundspan, targindex);
      nextptr = (typespan *)onitemlist (taskptr, (typeitem*)&foundspan,
                                        (typeitemset*)targspansetptr);
  }
  if(!context){
      return(targspansetptr);  // line 446–448: SILENT DROP — returns unchanged pointer
  }
  contextfree (context);
  return (&nextptr->next);
}
```

When `retrieverestricted` returns NULL (no POOM crum covers the I-address), the `if(!context)` branch fires at line 446 and **returns `targspansetptr` unmodified** — the I-span contributes nothing to the output V-spanset. There is no error code, no logged warning, no flag set.

---

### Why Retrieval Returns NULL for Ghost Addresses

`retrieverestricted` [retrie.c:56–85] calls `retrieveinarea`, which calls `findcbcinarea2d` [retrie.c:229–268]:

```c
for (; crumptr; crumptr = getrightbro (crumptr)) {
    if (!crumqualifies2d (crumptr, offsetptr, span1start, span1end, index1,
                          span2start, span2end, index2, (type2dbottomcruminfo*)infoptr)){
        continue;  // line 253–254: skip the crum
    }
    if (crumptr->height != 0) {
        ...
        findcbcinarea2d (findleftson ((typecuc*)crumptr), ...);
    } else {
        context = makecontextfromcbc ((typecbc*)crumptr, (typewid*)offsetptr);
        incontextlistnd (headptr, context, index1);  // only reaches here if qualified
    }
}
```

`crumqualifies2d` [retrie.c:270–305] rejects a crum when the I-space span does not intersect:

```c
// line 282–290: index1 (I-space) overlap check
endcmp = iszerotumbler (span1end) ? TOMYRIGHT : whereoncrum (crumptr, offset, span1end, index1);
if ( endcmp <= ONMYLEFTBORDER){
    return(FALSE);
}
startcmp = whereoncrum (crumptr, offset, span1start, index1);
if( (startcmp > THRUME)){
    return (FALSE);
}
```

If the I-address in the endset corresponds to no living POOM crum — i.e., the content was deleted or never existed in this POOM — then every crum in the tree will fail one of these interval tests. The tree is traversed completely, no context is built, and `retrieverestricted` returns NULL.

---

### Effect on Ghost Links

A **ghost link** is one whose endsets contain I-addresses that are no longer covered by any POOM entry (e.g., the content at those addresses was deleted, the document it referenced is gone, or the link was stored with stale I-coords).

When such an endset passes through I→V conversion:

| Scenario | Result |
|---|---|
| All I-addresses are live | Full V-spanset returned — normal behavior |
| Some I-addresses are unreferenced | Those spans silently vanish — **partial endset** |
| All I-addresses are unreferenced | Empty V-spanset — **empty endset** |

The caller in all three cases sees a valid data structure. There is nothing in the return value or call chain that distinguishes "no content" from "ghost." The `permute` loop at orglinks.c:414 simply continues to the next span regardless:

```c
for (; restrictionspanset; restrictionspanset = restrictionspanset->next) {
    targspansetptr = span2spanset(taskptr, orgl, restrictionspanset, restrictionindex,
                                   targspansetptr, targindex);
}
return (save);  // returns the original head — may be unchanged from before the loop
```

If `save` pointed to a NULL V-spanset going in, and every `span2spanset` call silently returned early, `save` still points to NULL on the way out. The caller gets NULL back and has no way to distinguish that from "this link genuinely has no endset content."

---

### Code Citations

| Claim | Location |
|---|---|
| `ispan2vspanset` entry | `orglinks.c:389–394` |
| `permute` iteration loop | `orglinks.c:414` |
| Silent early return when no context | `orglinks.c:446–448` |
| `retrieverestricted` delegates to `retrieveinarea` | `retrie.c:83` |
| `findcbcinarea2d` skips non-qualifying crums | `retrie.c:253–254` |
| `crumqualifies2d` I-space interval filter | `retrie.c:282–290` |
| `dofollowlink` endset retrieval | `do1.c:223–232` |
