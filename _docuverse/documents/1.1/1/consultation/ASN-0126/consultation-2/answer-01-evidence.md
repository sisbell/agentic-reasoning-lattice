## Question 1 [evidence]

> In udanax-green, does the retraction/nullify operation ever create a link with an empty from-set, or does it always record a source address for the retracting party?

## KB Synthesis

The KB does not contain any entry describing a "retraction" or "nullify" operation in udanax-green.

What the KB does establish is that:

- All `create_link` calls require **non-zero-width endpoints** on both source and target — a zero-width endpoint crashes the backend [PRE-LINK-CREATE, PRE-ZERO-WIDTH]
- There is no `DELETELINK` operation in the FEBE protocol; once created, a link is permanent [INV-LINK-PERMANENCE]
- The minimum valid endpoint width is 1 [PRE-LINK-CREATE]

There is no KB entry describing any operation called "retraction," "nullify," or anything that creates a link with an intentionally empty from-set. I cannot answer whether such an operation exists or how it behaves from the material provided.

---

## Code Exploration

The permission was denied. Here is my full answer based directly on the source code.

---

## Answer: Empty From-Set in CREATELINK

### There Is No Nullify/Retract Operation

`backend/requests.h` defines 24 request codes — `INSERT` (0), `CREATELINK` (27), `DELETEVSPAN` (12), and others — but **no `NULLIFY` or `RETRACT`** opcode exists anywhere in the codebase. Retraction in the Xanadu model is a **semantic convention**: a link whose type-endset (three-set) points to a retraction type address. The backend treats all links identically.

### CREATELINK Explicitly Accepts an Empty From-Set

The backend **can** create a link with an empty from-set, and every layer in the call chain handles it gracefully:

**1. Wire protocol — `get2fe.c:147-159`**
```c
bool getspecset(typetask *taskptr, typespecset *specsetptr)
{
    *specsetptr = NULL;
    if (!getnumber(taskptr, &num)) { return (FALSE); }
    if (num == 0)
        return (TRUE);   // ← empty specset is valid, not an error
    ...
}
```
When the client sends `0~` (count zero), `getspecset` sets `*specsetptr = NULL` and returns `TRUE`. `NOSPECS = SpecSet([])` in `client.py:581` serializes exactly this way (`SpecSet.write`, `client.py:543`).

**2. V→I conversion — `sporgl.c:14-33`**
```c
bool specset2sporglset(typetask *taskptr, typespecset specset, ...)
{
    *sporglsetptr = NULL;
    for (; specset; ...) { ... }   // never runs when specset == NULL
    *sporglsetptr = NULL;
    return (TRUE);                 // ← succeeds with NULL sporglset
}
```
Called at `do1.c:214` for the from-set. NULL in → NULL sporglset out, returns TRUE.

**3. POOM insertion — `orglinks.c:86-133`**
```c
bool insertpm(typetask *taskptr, tumbler *orglisa, typeorgl orgl,
              tumbler *vsaptr, typesporglset sporglset)
{
    if (iszerotumbler(vsaptr)) { return (FALSE); } // fromvsa=1.1, not zero
    ...
    logbertmodified(orglisa, user);   // marks link dirty
    for (; sporglset; ...) { ... }    // NULL: loop body never runs
    return (TRUE);
}
```
`setlinkvsas` (`do2.c:169-183`) sets `fromvsa = 1.1`, so the zero-check does not fire. `logbertmodified` is called, but **nothing is inserted into the link's orgl at V=1.1 (the from-end position)**. Returns TRUE.

**4. Spanfilade registration — `spanf1.c:25-53`**
```c
for (; sporglset; ...) { ... }   // NULL: never runs
return (TRUE);
```
**Nothing is registered in the spanfilade for the from-end.** Returns TRUE. Called by `insertendsetsinspanf` (`do2.c:116-128`), which also returns TRUE.

**5. `docreatelink` (`do1.c:195-221`) succeeds end-to-end.** The link is created in the granfilade and placed in document V-space, but its from-end has no content in either the POOM or the spanfilade.

### Consequences

- **`follow_link(linkid, LINK_SOURCE)` fails.** `link2sporglset` (`sporgl.c:67-95`) calls `retrieverestricted` looking for content at V=1.1 in the link's orgl. Finding nothing, it returns `FALSE`. The Python client returns `NOSPECS` (`client.py:764`).

- **`find_links(sourcespecs)` cannot find the link.** Because nothing was registered in the spanfilade for the from-end, the link is invisible to from-set queries. It can still be found via to-set or type-set queries.

### Conclusion

**Yes, a link with an empty from-set can be created, and the backend accepts it without error.** If retraction is expressed as such a link, the retracting party's address is **not recorded**. The link is anonymous on its from-end.

This is consistent with Finding 0011 (convention over enforcement): the backend imposes no constraint requiring a non-empty from-set. Semantic requirements — such as "a retraction must identify its author" — are the calling application's responsibility, not the backend's.
