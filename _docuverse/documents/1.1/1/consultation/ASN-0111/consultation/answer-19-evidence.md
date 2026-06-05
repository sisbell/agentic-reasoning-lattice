## Question 19 [evidence]

> Is there an invariant that a link orgl always contains exactly three endsets, and does a direct read fail or return a partial structure if any endset's I-span is empty?

## KB Synthesis

## Link Orgl Endset Structure and Empty-Endset Behavior

**Three endsets are always present at creation.** Link creation (`docreatelink`) always calls `insertendsetsinspanf()` with all three sporglsets — FROM (LINKFROMSPAN=1), TO (LINKTOSPAN=2), THREE/type (LINKTHREESPAN=3) — and indexes them in the spanf simultaneously [ST-CREATE-LINK, Finding 0012]. The orgl positions 0.1, 0.2, and 0.3 correspond to the three endpoints accessed by `link2sporglset()` [SS-FOLLOWLINK, Finding 0048]. Zero-width endpoint spans crash at creation (Bug 0017) [PRE-LINK-CREATE, Finding 0028], so all three endsets must be non-empty when the orgl is first allocated.

**Direct reads do not fail on empty endsets — they silently return partial or empty structures.** FOLLOWLINK's call chain — `link2sporglset()` → `linksporglset2specset()` → `span2spanset()` → `retrieverestricted()` — drops any I-address with no current POOM mapping without error [SS-FOLLOWLINK, Finding 0048]. The precondition for FOLLOWLINK requires only that the link orgl exists; liveness of the endpoint content is not checked [PRE-FOLLOWLINK, Finding 0048]. This is captured as the universal I→V filtering invariant: no operation returning V-addresses ever errors on an unreferenced I-address [INV-ITOV-FILTERING, Finding 0048].

**One unresolved anomaly:** When both source and target endpoints are deleted, `follow_link(link, LINK_TYPE)` also returns empty — despite the type endset referencing the permanent bootstrap document, which was never deleted [EC-ORPHANED-LINK, Finding 0024]. The KB does not explain the mechanism; it is recorded as unexpected behavior, possibly indicating that type resolution depends on one of the other endpoints being resolvable, or that there is an undocumented dependency in the FOLLOWLINK execution path.

---

## Code Exploration

I now have all the source evidence needed to answer definitively.

---

## Answer

### Question 1: Is there an invariant that a link orgl always contains exactly three endsets?

**No. The invariant is that from and to are always present; the three-endset is optional.** The codebase has two distinct link-creation paths:

#### `domakelink` — creates a 2-endset link (do1.c:169-193)

```c
&& setlinkvsas (&fromvsa, &tovsa, NULL)                                  // do1.c:189
&& insertendsetsinorgl (taskptr, linkisaptr, link, &fromvsa, fromsporglset, &tovsa, tosporglset, NULL, NULL)  // do1.c:190
&& insertendsetsinspanf (taskptr, spanf, linkisaptr, fromsporglset, tosporglset, NULL)  // do1.c:191
```

The two `NULL` arguments mean no three-end VSA is set and no three-end data is written.

#### `docreatelink` — creates a 3-endset link (do1.c:195-221)

```c
&& setlinkvsas (&fromvsa, &tovsa, &threevsa)                             // do1.c:217
&& insertendsetsinorgl (taskptr, linkisaptr, link, &fromvsa, fromsporglset, &tovsa, tosporglset, &threevsa, threesporglset)  // do1.c:218
&& insertendsetsinspanf (taskptr, spanf, linkisaptr, fromsporglset, tosporglset, threesporglset)  // do1.c:219
```

The guards that enforce this optionality are explicit:

**`insertendsetsinorgl` (do2.c:136):**
```c
if (threevsa && threesporglset) {
    if (!insertpm (taskptr, linkisaptr, link, threevsa, threesporglset)){
        return (FALSE);
    }
} else {
    fprintf(stderr,"leaving INSERTENDSETSINORGL 4\n");   // debug: missing three-end
}
```

**`insertendsetsinspanf` (do2.c:122):**
```c
if (threesporglset) {
    if(!insertspanf(taskptr,spanfptr,linkisaptr,threesporglset,LINKTHREESPAN)){
        return (FALSE);
    }
}
```

**`setlinkvsas` (do2.c:169-183):**
```c
if (threevsaptr) {
    tumblerclear (threevsaptr);
    tumblerincrement (threevsaptr, 0, 3, threevsaptr);  // VSA = 3.1
    tumblerincrement (threevsaptr, 1, 1, threevsaptr);
}
```

The VSA layout for endsets (xanadu.h:36-38, do2.c:169-183):
- **From-end**: V = 1.1 (LINKFROMSPAN = 1)
- **To-end**: V = 2.1 (LINKTOSPAN = 2)
- **Three-end**: V = 3.1 (LINKTHREESPAN = 3) — only when `threevsaptr != NULL`

**Note on FEBE path:** The FEBE `createlink` handler (fns.c:100-112) calls only `docreatelink`, so all links created through the FEBE protocol carry three endsets. `domakelink` is an internal path. Still, the structure has no code that asserts or enforces exactly-three anywhere.

---

### Question 2: Does a direct read fail or return a partial structure if any endset's I-span is empty?

The answer differs depending on which read path is used.

---

#### Path A: `followlink` → `dofollowlink` → `link2sporglset` (reads from link's orgl)

**`link2sporglset` (sporgl.c:67-95):**
```c
tumblerincrement (&zero, 0, whichend, &vspan.stream);
tumblerincrement (&zero, 0/*1*/, 1, &vspan.width);
if (context = retrieverestricted((typecuc*)orgl, &vspan ,V, (typespan*)NULL, I, (typeisa*)NULL)) {
    for (c = context; c; c = c->nextcontext) {
        ...
    }
    return (TRUE);
} else {
    return (FALSE);     // ← hard failure if V-position has no data
}
```

If V-position `whichend` was never written (e.g., asking for endset 3 on a 2-endset link), `retrieverestricted` returns NULL and `link2sporglset` returns **FALSE**. `dofollowlink` propagates this FALSE (do1.c:228-231), and the FEBE layer sends `putrequestfailed` (fns.c:125-126). **No partial structure — hard failure.**

---

#### Path B: `retrieveendsets` → `doretrieveendsets` → `retrieveendsetsfromspanf` (reads from spanfilade)

**`retrievesporglsetinrange` (spanf1.c:237-267)** always returns TRUE, even if nothing is found:
```c
return (TRUE);   // spanf1.c:266 — always succeeds
```

**`linksporglset2specset` (sporgl.c:97-123)** with a NULL sporglset:
```c
*specsetptr = NULL;
for (; sporglset; ...) {   // loop body never executes if sporglset is NULL
    ...
}
return (TRUE);              // returns TRUE, *specsetptr remains NULL
```

**`retrieveendsetsfromspanf` (spanf1.c:190-235)** chains these calls, so if any endset is absent from the spanfilade, the function still returns TRUE with a NULL specset for the absent endset. The caller `retrieveendsets` (fns.c:350-362) then calls `putretrieveendsets` with these potentially-NULL specsets. **Partial structure — success return with NULL contents for missing endsets.**

---

#### Zero-width I-span: Process abort in either path

If a zero-width I-span is actually stored and retrieved, there are guards at two points that call `gerror` → `qerror` → `abort()` (genf.c:546-550):

**`contextintosporgl` (sporgl.c:212-216):**
```c
if (iszerotumbler (&context->contextwid.dsas[index])) {
    gerror ("zero wid in contextintosporgl");
}
```

**`linksporglset2specset` (sporgl.c:105-110):**
```c
if (iszerotumbler (&((typesporgl *)sporglset)->sporglwidth))
    gerror("zero wid I span in linksporglset2specset\n");
```

`gerror` is `#define gerror(s) qerror(s)` (common.h:119), and `qerror` is:
```c
INT qerror(char *message) {          // genf.c:546
    fprintf (stderr, "Error: %s\n",message);
    abort();
    return(1);
}
```

**A zero-width I-span at retrieval time crashes the process.** There is no graceful degradation or partial return — it is treated as a structural invariant violation that cannot be recovered from.

---

### Summary

| Scenario | Behavior |
|---|---|
| Link orgl always has 3 endsets | **No** — from+to required, three optional |
| `followlink` on absent endset (V-position empty) | **Returns FALSE** — hard failure, `putrequestfailed` sent |
| `retrieveendsets` on absent endset (not in spanfilade) | **Returns TRUE** with NULL specset — partial structure |
| Zero-width I-span anywhere in retrieval path | **`abort()`** — process crash |
