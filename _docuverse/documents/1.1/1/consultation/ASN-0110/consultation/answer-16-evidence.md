## Question 16 [evidence]

> Are unreferenced I-addresses (DEL5 ghosts) within a matching endset silently filtered during the I→V conversion of the result, yielding partial or empty endset reports?

## KB Synthesis

Yes, confirmed. Unreferenced I-addresses are silently filtered during I→V conversion, yielding partial or empty endset reports.

## Mechanism

[INV-ITOV-FILTERING] establishes this as a **universal invariant** of all operations that convert I-addresses to V-addresses. The conversion path is shared:

```
linksporglset2specset() → sporglset2vspanset() → ispan2vspanset()
  → permute() → span2spanset() → retrieverestricted()
```

At `span2spanset()` (`orglinks.c:446-448`), if `retrieverestricted()` finds no POOM mapping for an I-address, it returns NULL. The I-address is **silently dropped** — no V-span added, no error raised.

## Three Observable Cases

[EC-GHOST-LINK] (Finding 0048) documents the three result states:

| Endset I-addresses | Result |
|---|---|
| All referenced in POOM | Full endset V-spans |
| Some unreferenced | Partial endset — only live addresses converted |
| All unreferenced | Empty `[]`, operation still returns success |

## Applies to Both Operations

[SS-FOLLOWLINK] and [SS-RETRIEVE-ENDSETS] both route through `linksporglset2specset()` — the same filtering applies to FOLLOWLINK and RETRIEVEENDSETS identically.

## Precondition Implication

[PRE-FOLLOWLINK] is explicit: the precondition for FOLLOWLINK does NOT require endset I-addresses to be currently referenced in any POOM. An empty result is a valid successful outcome, not an error. The operation answers "what current V-positions correspond to this endset?" — if the answer is none, it returns `[]`.

## Concrete Confirmation

[EC-GHOST-LINK-ENDPOINT] (Finding 0067) shows the specific case: DELETE from document A removes I-address mappings from A's POOM. A link in document B referencing those I-addresses then has its endset silently filtered to empty on FOLLOWLINK, even though the link structure in B is completely unchanged and the I-addresses persist permanently in I-space.

---

## Code Exploration

I now have all the code and findings needed. Here is the complete answer.

---

## Answer: DEL5 Ghost Filtering During I→V Conversion of Endsets

**Yes.** Unreferenced I-addresses (DEL5 ghosts) within a matching endset are silently filtered during I→V conversion. The filter is implicit and structural, not an explicit liveness check. The operation succeeds, but DEL5 ghosts simply contribute nothing to the output, yielding a partial or empty endset report.

---

### What is a DEL5 Ghost

Per EWD-030:

> (DEL5) unreferenced(a) ≡ a ∈ dom.ispace ∧ ¬(∃d, v : poom.d(v) = a)

An I-address becomes unreferenced when `deletevspanpm` removes its V→I mapping from the POOM via `deletend(V)` [`orglinks.c:149`], but no corresponding cleanup occurs in the spanfilade or link orgl. Those structures reference the I-address permanently.

From `do1.c:158-167` (`dodeletevspan`):

```c
bool dodeletevspan(typetask *taskptr, typeisa *docisaptr, typevspan *vspanptr)
{
    typeorgl docorgl;
    return (
       findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
    && deletevspanpm (taskptr, docisaptr, docorgl, vspanptr)
    );
}
```

And `orglinks.c:145-152`:

```c
bool deletevspanpm(typetask *taskptr, tumbler *docisaptr, typeorgl docorgl, typevspan *vspanptr)
{
    if (iszerotumbler(&vspanptr->width))
        return (FALSE);
    deletend((typecuc*)docorgl, &vspanptr->stream, &vspanptr->width, V);  // removes V→I from POOM only
    logbertmodified(docisaptr, user);
    return (TRUE);
}
```

There is no call to remove the spanfilade entry. No `deletespanf` function exists anywhere in `spanf1.c` or `spanf2.c` (Finding 0057). Link orgl entries referencing the deleted I-addresses persist in I-space permanently (P0).

---

### The Filter: Where It Happens

Both endset query operations go through the same I→V conversion funnel.

#### Path 1: FOLLOWLINK

`do1.c:223-231` → `sporgl.c:link2sporglset` → `sporgl.c:linksporglset2specset`

`link2sporglset` [`sporgl.c:67-95`] extracts I-addresses from the link orgl with **no POOM check**:

```c
// Step 2: read endset at V-position whichend (0.1 / 0.2 / 0.3)
tumblerincrement (&zero, 0, whichend, &vspan.stream);
tumblerincrement (&zero, 0/*1*/, 1, &vspan.width);

// Step 3: retrieve I-addresses — NO LIVENESS CHECK
if (context = retrieverestricted((typecuc*)orgl, &vspan, V,
                                  (typespan*)NULL, I, (typeisa*)NULL)) {
    for (c = context; c; c = c->nextcontext) {
        contextintosporgl ((type2dcontext*)c, (tumbler*)NULL, sporglptr, I);
        ...
    }
    return (TRUE);
}
```

The I-addresses extracted here may be DEL5 ghosts. The function does not know and does not care.

#### Path 2: RETRIEVEENDSETS

`do1.c:369-374` → `spanf1.c:retrieveendsetsfromspanf` → `spanf1.c:retrievesporglsetinrange` → `sporgl.c:linksporglset2specset`

`retrievesporglsetinrange` [`spanf1.c:237-267`] pulls I-addresses from the spanfilade via `retrieverestricted`. Again, no liveness check: the spanfilade is a historical record, not a live index.

#### Shared Convergence Point: `ispan2vspanset`

Both paths converge at `sporglset2vspanset` [`sporgl.c:141-176`], which calls:

```c
vspansetptr = ispan2vspanset (taskptr, orgl, &ispan, vspansetptr);
```

`ispan2vspanset` [`orglinks.c:389-394`]:

```c
typevspanset *ispan2vspanset(typetask *taskptr, typeorgl orgl, typeispan *ispanptr, typevspanset *vspansetptr)
{
    return permute(taskptr, orgl, ispanptr, I, vspansetptr, V);
}
```

`permute` [`orglinks.c:404-422`] iterates over I-spans and calls `span2spanset` for each:

```c
for (; restrictionspanset; restrictionspanset = restrictionspanset->next) {
    targspansetptr = span2spanset(taskptr, orgl, restrictionspanset,
                                   restrictionindex, targspansetptr, targindex);
}
```

---

### The Silent Drop in `span2spanset`

`span2spanset` [`orglinks.c:425-453`] is where the filtering actually occurs:

```c
context = retrieverestricted((typecuc*)orgl, restrictionspanptr,
                              restrictionindex, (typespan*)NULL,
                              targindex, (typeisa*)NULL);

for (c = context; c; c = c->nextcontext) {
    context2span (c, restrictionspanptr, restrictionindex, &foundspan, targindex);
    nextptr = (typespan *)onitemlist (taskptr, (typeitem*)&foundspan,
                                      (typeitemset*)targspansetptr);
}

// orglinks.c:446-448 — the silent drop:
if(!context){
    return(targspansetptr);   // return unchanged — nothing added
}
```

For a DEL5 ghost I-address, `retrieverestricted` searches the home document's POOM (`orgl`) and finds **no crums** whose I-range covers that address, because `deletend` already removed them. It returns `NULL`. The `for` loop body never executes. Control falls to `if(!context)` and returns `targspansetptr` with nothing added.

No error. No log message. The I-address is simply absent from the output.

---

### No Liveness Check in `crumqualifies2d`

One might ask whether `crumqualifies2d` [`retrie.c:270-305`] performs a DEL5 check. It does not. Its qualification tests are purely geometric:

```c
// retrie.c:274 — homedoc check; only active when infoptr != NULL
if ((crumptr->height == 0) && infoptr &&
    !tumblereq (&infoptr->homedoc, &(((type2dcbc *)crumptr)->c2dinfo.homedoc))){
    return (FALSE);
}
// retrie.c:282-300 — range intersection checks only
endcmp = iszerotumbler (span1end) ? TOMYRIGHT : whereoncrum (...);
startcmp = whereoncrum (...);
```

The `homedoc` check at line 274 is skipped because `retrieverestricted` is called with `docisaptr = NULL` from `span2spanset` [`orglinks.c:435`]:

```c
context = retrieverestricted((typecuc*)orgl, restrictionspanptr, restrictionindex,
                              (typespan*)NULL, targindex, (typeisa*)NULL);
                              //                            ^^^^^^^^^^^^^^^
                              //                  NULL → infoptr = NULL → line 274 skipped
```

So the only reason context is NULL for a DEL5 ghost is that no crums covering that I-range exist in the POOM — they were structurally removed by `deletend`. There is no separate ghost marker or DEL flag in any crum field.

---

### Behavior Table

| Endset I-address state | POOM contains crum? | `retrieverestricted` | `span2spanset` result | Final endset |
|------------------------|---------------------|----------------------|-----------------------|--------------|
| Live (currently in POOM) | Yes | Returns context | Adds V-span to output | Included |
| DEL5 ghost (removed from POOM) | No | Returns NULL | Returns unchanged | Silently dropped |

---

### Consequence: Partial or Empty Reports

- **Partial endset**: If an endset contains some live I-addresses and some DEL5 ghosts, `permute` accumulates V-spans only for the live ones. The ghosts are dropped silently. The caller receives fewer spans than the endset logically contains.

- **Empty endset**: If ALL I-addresses in the endset are DEL5 ghosts, `permute` returns an empty V-span set. The operation succeeds (`return TRUE`) but the result is `[]`.

This is confirmed by the golden test `golden/links/orphaned_link_target_all_deleted.json`:

```json
{
    "op": "follow_link",
    "label": "after_delete",
    "end": "target",
    "result": [],
    "works": true
}
```

The operation returns success (`"works": true`) with an empty result — not an error.

---

### Spanfilade Stale References Compound the Problem

Because the spanfilade is write-only (no `deletespanf` exists — Finding 0057), I-addresses appear in endset queries even after the content that wrote them was deleted. When `retrieveendsetsfromspanf` finds an endset in the spanfilade and converts its sporgl I-addresses via `linksporglset2specset` → `sporglset2vspanset` → `ispan2vspanset`, every DEL5 ghost in that endset silently contributes nothing. The query returns a V-span set that is a strict subset of what the stored endset contains.

The two enfilades are in perpetually divergent states:
- **spanf**: Append-only; retains all I-address-to-document associations ever made
- **granf POOM**: Mutable; reflects only what is currently mapped in V-space

The I→V conversion is the only reconciliation step, and it is silent.

---

### Summary

**DEL5 ghosts within a matching endset are silently filtered during I→V conversion.** The mechanism is structural: `span2spanset` [`orglinks.c:446-448`] returns `targspansetptr` unchanged when `retrieverestricted` finds no POOM crums for an I-address. There is no explicit liveness check anywhere in the chain — `crumqualifies2d` performs only geometric tests, and the `homedoc` filter is not activated. The result is that endset reports are partial (only live I-addresses produce V-spans) or empty (all-ghost endsets). The operation always reports success; the caller receives no indication that addresses were dropped.
