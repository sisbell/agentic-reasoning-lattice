## Question 1 [evidence]

> Does udanax-green's link allocation (docreatelink and the link-orgl structure) fix the endset count at three, or does it support N ≥ 3, and does it require the type-endset to be non-empty?

## KB Synthesis

## Endset Count and Type-Endset Requirements

### Endset count is fixed at exactly three

The link orgl structure has exactly three endset slots — FROM, TO, and THREE — hardwired at every level of the system:

**Internal V-positions in the home document:** `setlinkvsas()` hardcodes digit-0 values of 1, 2, and 3, placing FROM at `2.x`, TO at `2.x` (sequential), and the type endpoint at `3.x`. There is no loop or count parameter — three positions, always. [SS-DUAL-ENFILADE] Finding 0038

**Link orgl access:** `link2sporglset()` retrieves endsets by tumbler position 0.1, 0.2, or 0.3 within the orgl's V-space. The access paths are positional constants, not a variable-length structure. [SS-FOLLOWLINK] Finding 0048

**Spanfilade indexing:** `insertendsetsinspanf()` receives exactly three sporglsets tagged `LINKFROMSPAN=1`, `LINKTOSPAN=2`, `LINKTHREESPAN=3`. [INT-SPORGL-LINK-INDEX] Finding 0013

**Query interface:** `RETRIEVEENDSETS` returns three specsets simultaneously; `FINDLINKSFROMTOTHREE` takes three separate constraint parameters. [SS-RETRIEVE-ENDSETS] Finding 0035

N > 3 endsets have no representation in the orgl structure, the POOM layout, the spanfilade index, or any query path.

---

### Type-endset is architecturally expected to be non-empty

Link types are VSpec references into the bootstrap document's type registry at `1.0.2.x` — they are content-identity references, not metadata flags. The KB records JUMP (`1.0.2.2`), QUOTE (`1.0.2.3`), FOOTNOTE (`1.0.2.6`), MARGIN (`1.0.2.6.2`). The type hierarchy is encoded by tumbler containment, enabling range queries over type families. [SS-LINK-ENDPOINT] Finding 0024

The KB does **not** contain direct evidence of what happens when a zero-width type specset is passed. `PRE-ZERO-WIDTH` establishes that zero-width spans crash link creation (Bug 0017), and the concrete example uses `create_link(home, source=Span(1.1, 0.0), target=Span(1.12, 0.0), type=T)` — the type `T` is non-zero in the crash test. Whether a zero-width type specset independently crashes is not tested in the recorded findings. [PRE-LINK-CREATE] Finding 0028, [PRE-ZERO-WIDTH] Finding 0028

One anomaly is recorded: when both source and target content are fully deleted, `follow_link(link_id, LINK_TYPE)` returns empty — even though the bootstrap document was never deleted. This unexplained behavior suggests type resolution depends on the same I-to-V filtering path as source/target (`INV-ITOV-FILTERING`), but the KB offers no mechanistic explanation. [EC-ORPHANED-LINK] Finding 0024

**Bottom line:** The count is three, fixed structurally. The type endset is required by design (bootstrap doc reference), but the KB is silent on whether an empty type specset is a hard crash or a silent failure at creation time.

---

## Code Exploration

I now have all the evidence. Here is my full answer.

---

## Link Endset Count and Type-Endset Requirements in udanax-green

### 1. Endset count is fixed at exactly three — no N ≥ 3

The system supports precisely three endset positions, defined as integer constants in `backend/xanadu.h:36-39`:

```c
#define LINKFROMSPAN    1
#define LINKTOSPAN      2
#define LINKTHREESPAN   3
#define DOCISPAN        4
```

There is no provision for a fourth endset. These constants are the only span-type identifiers ever passed to the spanfilade for link entries. `DOCISPAN = 4` is the document-content span type — it is not a link endset.

The constraint is structural: `setlinkvsas` (`backend/do2.c:169-183`) assigns fixed tumbler addresses to exactly three positions:

```c
bool setlinkvsas(tumbler *fromvsaptr, tumbler *tovsaptr, tumbler *threevsaptr)
{
    tumblerclear(fromvsaptr);
    tumblerincrement(fromvsaptr, 0, 1, fromvsaptr);  // FROM → 1.1
    tumblerincrement(fromvsaptr, 1, 1, fromvsaptr);
    tumblerclear(tovsaptr);
    tumblerincrement(tovsaptr, 0, 2, tovsaptr);      // TO → 2.1
    tumblerincrement(tovsaptr, 1, 1, tovsaptr);
    if (threevsaptr) {
        tumblerclear(threevsaptr);
        tumblerincrement(threevsaptr, 0, 3, threevsaptr); // THREE → 3.1
        tumblerincrement(threevsaptr, 1, 1, threevsaptr);
    }
    return (TRUE);
}
```

There is no loop, no count parameter, no extensible structure. FROM is always at V-address 1, TO at 2, THREE at 3. No other positions are ever set.

The protocol-level `getfollowlink` (`backend/get1.c:63-74`) further confirms this ceiling:

```c
if (!(
   getnumber(taskptr, whichendptr)
&& (*whichendptr == 1 || *whichendptr == 2 || *whichendptr == 3)))
    return(FALSE);
```

A request to follow endset 4 is a protocol error.

---

### 2. There are two link-creation entry points, not one

`backend/do1.c` defines two distinct link-creation operations:

**`domakelink` (`do1.c:169-193`)** — binary link (FROM + TO only):
```c
bool domakelink(typetask *taskptr, typeisa *docisaptr, typespecset fromspecset, typespecset tospecset, typeisa *linkisaptr)
{
    ...
    && setlinkvsas(&fromvsa, &tovsa, NULL)             // do1.c:189
    && insertendsetsinorgl(taskptr, linkisaptr, link,
         &fromvsa, fromsporglset, &tovsa, tosporglset,
         NULL, NULL)                                   // do1.c:190
    && insertendsetsinspanf(taskptr, spanf, linkisaptr,
         fromsporglset, tosporglset, NULL)             // do1.c:191
}
```

`NULL` is passed explicitly for the third endset parameters. No three-endset is allocated, no position 3 is written.

**`docreatelink` (`do1.c:195-221`)** — ternary link (FROM + TO + THREE):
```c
bool docreatelink(typetask *taskptr, typeisa *docisaptr, typespecset fromspecset, typespecset tospecset, typespecset threespecset, typeisa *linkisaptr)
{
    ...
    && specset2sporglset(taskptr, threespecset, &threesporglset, NOBERTREQUIRED)  // do1.c:216
    && setlinkvsas(&fromvsa, &tovsa, &threevsa)                                   // do1.c:217
    && insertendsetsinorgl(taskptr, linkisaptr, link,
         &fromvsa, fromsporglset, &tovsa, tosporglset,
         &threevsa, threesporglset)                                               // do1.c:218
    && insertendsetsinspanf(taskptr, spanf, linkisaptr,
         fromsporglset, tosporglset, threesporglset)                              // do1.c:219
}
```

The FEBE protocol layer exclusively calls `docreatelink`. `createlink` in `backend/fns.c:100-112` reads three specsets from the wire via `getcreatelink` and passes all three down:

```c
void createlink(typetask *taskptr)
{
    ...
    getcreatelink(taskptr, &docisa, &fromspecset, &tospecset, &threespecset)
    && docreatelink(taskptr, &docisa, fromspecset, tospecset, threespecset, &linkisa)
    ...
}
```

`getcreatelink` in `backend/get1fe.c:75-84` always reads exactly three specsets — `fromset`, `toset`, `threeset` — in that order. The client is required to send all three.

---

### 3. The type-endset (THREE) is not required to be non-empty — but emptiness is silently absorbed

`getspecset` (`backend/get2fe.c:147-180`) reads a specset from the wire. When the client sends `0` as the item count, it returns `TRUE` immediately with `*specsetptr = NULL` (`get2fe.c:158-159`):

```c
if (num == 0)
    return(TRUE);  // *specsetptr stays NULL
```

`specset2sporglset` (`backend/sporgl.c:14-33`) then receives that NULL as `specset`. Its loop does not execute, and `*sporglsetptr` remains NULL:

```c
*sporglsetptr = NULL;                     // sporgl.c:18
for (; specset; ...)  { ... }             // loop body skipped — specset is NULL
*sporglsetptr = NULL;                     // sporgl.c:30
return(TRUE);
```

The result is `threesporglset = NULL`.

`insertendsetsinorgl` (`backend/do2.c:130-149`) then guards on both pointers:

```c
if (threevsa && threesporglset) {          // do2.c:136
    insertpm(taskptr, linkisaptr, link, threevsa, threesporglset);
} else {
    fprintf(stderr, "leaving INSERTENDSETSINORGL 4\n");  // debug only
}
```

With `threesporglset = NULL`, the condition is false. The three-endset write into the orgl is silently skipped (with a debug-only stderr trace in non-DISTRIBUTION builds).

`insertendsetsinspanf` (`backend/do2.c:116-128`) guards the same way:

```c
if (threesporglset) {                      // do2.c:122
    insertspanf(taskptr, spanf, linkisaptr, threesporglset, LINKTHREESPAN);
}
```

Again, skipped.

Note that `threevsa` itself is NOT NULL — `setlinkvsas` was given `&threevsa` and wrote position 3.1 into it (`do2.c:177-181`). Only `threesporglset` is NULL. The guard requires both to be truthy, so even with a valid VSA the absence of content prevents any write. An empty three-endset `docreatelink` is therefore functionally equivalent to `domakelink`.

---

### Conclusions

| Question | Answer |
|---|---|
| Is the endset count fixed at 3 or N ≥ 3? | **Fixed at three.** FROM=1, TO=2, THREE=3 are hardcoded positions. No mechanism exists for a 4th endset. |
| Does it support N ≥ 3? | **No.** There is no loop, count parameter, or extensible allocation path. |
| Is the type-endset (THREE) required to be non-empty? | **No.** An empty specset (client sends `0` items) results in `threesporglset = NULL`, which is silently treated as "no third endset" in both `insertendsetsinorgl` and `insertendsetsinspanf`. |
| Are untyped (two-endset) links possible via `docreatelink`? | **Yes**, by sending an empty threespecset. The result is a link with only FROM and TO entries in the orgl and spanfilade. |
| What is `domakelink` then? | An older or internal convenience that hard-codes NULL for the three parameters rather than reading an empty specset from the wire. The protocol layer does not use it — `createlink` always calls `docreatelink`. |
