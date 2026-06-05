## Question 12 [evidence]

> Does the cursor for windowed retrieval encode an absolute position into the materialized link list, or does it encode an I-address/tumbler boundary into the spanfilade search itself?

## KB Synthesis

The cursor encodes an identity into the **materialized link list**, not a boundary into the spanfilade search.

From [SS-PAGINATE-LINKS]: on every paginated call, the system **re-executes the full `findlinksfromtothreesp()` search** from scratch — no spanfilade shortcut. Only after the complete result list is materialized does cursor logic apply: if the cursor is zero-tumbler it returns from the head; otherwise it **linearly scans the list with `tumblereq()` for an exact ISA match**, then truncates at N items via `linkset->next = NULL`.

The cursor is a **link ISA tumbler** — an identity address, not a positional offset or an I-address range boundary. There is no mechanism to inject the cursor as a lower-bound restriction into the spanfilade retrieval path.

Consequence noted in [SS-PAGINATE-LINKS]: if the cursor link is deleted between calls, `tumblereq()` never matches, the scan falls off the end, and the call returns an empty set with count=0 — a stale-cursor invalidation that would be impossible if the cursor were a pure address boundary into the index.

---

## Code Exploration

I now have everything needed. Here is the complete answer, verified against the actual source.

---

## Cursor Encoding in Windowed Retrieval

**The cursor is a tumbler (I-address) that identifies the last returned link by its ISA, but it is consumed as a linear scan bookmark in a freshly re-materialized result list — it is NOT fed back as a tumbler boundary into the spanfilade search.**

---

### Call Chain

```
FEBE wire
  → fns.c:219  findnextnlinksfromtothree()
  → do1.c:362  dofindnextnlinksfromtothree()
  → spanf1.c:117  findnextnlinksfromtothreesp()
      ├── spanf1.c:124  findlinksfromtothreesp()   ← full re-traversal every time
      │     → sporglset2linkset()
      │     → retrieverestricted()   [retrie.c:56]
      │     → retrieveinarea()       [retrie.c:87]
      │     → findcbcinarea2d()      [retrie.c:229]  ← B-tree walk with tumbler boundaries
      └── spanf1.c:126–135  linear scan using cursor
```

---

### Step 1 — Cursor read off the wire as a raw tumbler

`get1fe.c:115–120`:
```c
bool getfindnextnlinksfromtothree(..., typeisa *lastlinkptr, INT *nptr)
{
    return
       getfindlinksfromtothree(...)
    && gettumbler(taskptr, lastlinkptr)   // line 119 — cursor is just a tumbler
    && getnumber(taskptr, nptr);
}
```

`typeisa` is `typedef tumbler typeisa` (`xanadu.h:23`). The cursor the client sends is the ISA (I-address) of the last link returned in the previous window.

---

### Step 2 — Do layer passes the cursor through unchanged

`do1.c:362–367`:
```c
bool dofindnextnlinksfromtothree(..., typeisa *lastlinkisaptr, ...)
{
    return findnextnlinksfromtothreesp(taskptr, fromvspecptr, tovspecptr,
               threevspecptr, orglrangeptr, lastlinkisaptr, ...);
}
```

The cursor is not transformed; it goes straight to the spanfilade layer.

---

### Step 3 — Spanfilade re-traverses from scratch every time

`spanf1.c:117–149` (full text verified):

```c
bool findnextnlinksfromtothreesp(..., typeisa *lastlinkisaptr,
                                  typelinkset *nextlinksetptr, INT *nptr)
{
    // line 124: full re-traversal — spanfilade walked from root every call
    if (!findlinksfromtothreesp(taskptr, spanf, fromvspecset, tovspecset,
                                threevspecset, orglrangeptr, &linkset))
        return (FALSE);

    // line 126: cursor applied AFTER full traversal
    if (iszerotumbler(lastlinkisaptr)) {
        *nextlinksetptr = linkset;              // first window: start from head
    } else {
        for (; linkset; linkset = linkset->next) {
            if (tumblereq(&linkset->address, lastlinkisaptr)) {  // line 130
                *nextlinksetptr = linkset->next;  // resume after match
                break;
            }
        }
    }
    // line 141: truncate to n items
    for (linkset = *nextlinksetptr; linkset; linkset = linkset->next) {
        if (++n >= *nptr) { linkset->next = NULL; break; }
    }
    *nptr = n;
    return (TRUE);
}
```

---

### Step 4 — What the spanfilade search *does* use tumblers for

Inside `findlinksfromtothreesp` → `retrieverestricted` → `findcbcinarea2d` (`retrie.c:229`), the B-tree walk uses tumbler boundaries (`span1start`/`span1end`, `span2start`/`span2end`) derived from the from/to/three specsets to prune nodes via `crumqualifies2d` (`retrie.c:270`) and `whereoncrum` (`retrie.c:345`). These boundaries come from the query specsets, **not from the cursor**. The cursor plays no role in the spanfilade traversal itself.

---

### Definitive Answer

| Question | Answer |
|---|---|
| What is the cursor? | A `typeisa` (= `tumbler`) holding the ISA of the last link returned |
| Where is it constructed? | By the client; read off the wire via `gettumbler()` (`get1fe.c:119`) |
| Where is it consumed? | As a linear scan target in `findnextnlinksfromtothreesp` after full re-traversal (`spanf1.c:130`) |
| Does it drive the spanfilade search? | **No.** The spanfilade is re-walked from root on every window request with the original specset boundaries. The cursor only selects the resume point in the newly materialized list. |
| What does drive the spanfilade? | The from/to/three V-specsets, converted to tumbler ranges via `retrieverestricted` → `findcbcinarea2d` |

**The cursor encodes an absolute identity (the ISA tumbler of the last returned link), not a positional index and not a spanfilade search boundary.** Pagination is O(n) at the list level — the spanfilade's B-tree efficiency is used only for the initial from/to/three span intersection, not for resuming windows.
