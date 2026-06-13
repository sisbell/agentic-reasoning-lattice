## Question 11 [evidence]

> Does FINDNUMOFLINKSFROMTOTHREE obtain its number by calling the same `findlinksfromtothreesp` spanfilade search as enumeration and fully materializing the matching link list into a transient structure before taking its length, so that asking for a count costs the same as retrieving every match?

## KB Synthesis

Yes. [SS-FIND-LINKS] (Finding 0035) states this explicitly:

> FINDNUMOFLINKSFROMTOTHREE (opcode 29) is a trivial wrapper around FINDLINKSFROMTOTHREE. It calls `findlinksfromtothreesp()` to materialize the complete linked list of matching links, then walks the list counting elements. There is no count-only optimization — the full search executes (V-to-I translation, spanfilade search per endset, intersection of result sets), then the list is linearly counted.

The implementation is at `backend/spanf1.c:105-115`. The count operation shares the identical work profile as full enumeration: V-to-I address translation on the query specset, spanfilade search per endset type (FROM, TO, THREE), intersection of result sets via `intersectlinksets()`, and then a linear walk to tally the materialized list. Asking "how many?" costs exactly as much as asking "which ones?"

---

## Code Exploration

I have everything needed for a complete answer.

---

## Answer

**Yes — asking for the count costs exactly as much as full retrieval.** `FINDNUMOFLINKSFROMTOTHREE` obtains its number by calling `findlinksfromtothreesp` verbatim, waiting for it to fully materialise every matching link into a heap-allocated linked list, and then walking that list with a bare pointer-chase loop to count nodes.

---

### The complete call chain

**Dispatch** — `requests.h:38`
```c
#define FINDNUMOFLINKSFROMTOTHREE 29
```

**FEBE handler** — `fns.c:204–217`
```c
void findnumoflinksfromtothree(typetask *taskptr)
{
  ...
  if (
     getfindnumoflinksfromtothree (taskptr, &fromvspecset, &tovspecset, &threevspecset, &homeset)
  && dofindnumoflinksfromtothree (taskptr, fromvspecset, tovspecset, threevspecset, homeset, &numberoflinks))
        putfindnumoflinksfromtothree (taskptr, numberoflinks);
  else
        putrequestfailed (taskptr);
}
```

**Thin wrapper** — `do1.c:355–360`
```c
bool dofindnumoflinksfromtothree(typetask *taskptr, typespecset *fromvspecset, ...)
{
  bool findnumoflinksfromtothreesp();
  return findnumoflinksfromtothreesp (taskptr, spanf, fromvspecset, tovspecset, threevspecset, orglrangeptr, numptr);
}
```

**The counting function** — `spanf1.c:105–115`
```c
bool findnumoflinksfromtothreesp(typetask *taskptr, typespanf spanfptr,
    typespecset fromvspecset, typespecset tovspecset, typespecset threevspecset,
    typeispan *orglrange, INT *numptr)
{
  typelinkset linkset;
  INT n;

  if (!findlinksfromtothreesp (taskptr, spanfptr, fromvspecset, tovspecset, threevspecset, orglrange, &linkset))
          return(FALSE);
  for (n = 0; linkset; linkset = linkset->next, ++n);
  *numptr = n;
  return (TRUE);
}
```

There is no early exit, no counter maintained during retrieval, no shortcut through the enfilade. The call to `findlinksfromtothreesp` at `spanf1.c:110` is the identical function used by `FINDLINKSFROMTOTHREE` (`do1.c:348–353`). Once it returns the full materialised list, `findnumoflinksfromtothreesp` traverses every `->next` pointer and increments `n`.

---

### What `findlinksfromtothreesp` does (the expensive part)

`spanf1.c:56–103` — three-phase full materialisation:

1. **Virtual→internal address translation** (lines 70–75): for each non-null endpoint specset, calls `specset2sporglset`, which traverses the granfilade and/or version graph to convert virtual spans to internal (sporgl) coordinates.

2. **Spanfilade retrieval per endpoint** (lines 76–99): for each of from/to/three, calls `sporglset2linkset` (`sporgl.c:222`), which in turn calls `sporglset2linksetinrange` → `retrieverestricted` (full enfilade traversal) → `onlinklist` to build a heap-allocated `typelinkset`. If any endpoint returns an empty set the function returns immediately with `NULL` (lines 78–83, 86–90, 93–97).

3. **Intersection** (line 100): calls `intersectlinksets` (`spanf2.c:46–120`), which allocates a **new** `typelink` node via `makelinkitem`/`taskalloc` (line 130) for every address that survives the intersection. With all three endpoints supplied this is an O(|from| × |to| × |three|) nested loop (`spanf2.c:106–117`).

The list produced by step 3 is what `findnumoflinksfromtothreesp` receives at `spanf1.c:110`. It holds one `typelink` struct per matching link, each allocated from the task arena. The counting loop at line 112 then walks every node — the memory is already allocated, the retrieval work is already done.

---

### Summary

| Operation | Code path |
|---|---|
| `FINDLINKSFROMTOTHREE` | `fns.c:196–199` → `do1.c:348` → `findlinksfromtothreesp` → return list |
| `FINDNUMOFLINKSFROMTOTHREE` | `fns.c:211–214` → `do1.c:355` → `findnumoflinksfromtothreesp` → **same `findlinksfromtothreesp`** → count list → discard |

The count is taken by a `for` loop over the already-materialised list (`spanf1.c:112`). There is no dedicated counting path through the enfilade. Asking "how many?" costs exactly the same as asking "give me all of them."
