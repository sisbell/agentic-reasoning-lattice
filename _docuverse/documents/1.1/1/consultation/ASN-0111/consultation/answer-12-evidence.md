## Question 12 [evidence]

> Does direct read of the link orgl preserve the positional ordering of the three endsets (source, target, type), and is that ordering structurally fixed within the orgl?

## KB Synthesis

Yes, the ordering is structurally fixed. The KB provides consistent evidence from two independent code paths.

**At creation** (`docreatelink`): `insertendsetsinspanf()` stores each endset into the spanfilade tagged with distinct constants — `LINKFROMSPAN=1`, `LINKTOSPAN=2`, `LINKTHREESPAN=3` — which serve as ORGLRANGE positions within the link orgl's internal V-space. [INT-SPORGL-LINK-INDEX]

**At retrieval** (FOLLOWLINK): `link2sporglset()` reads the orgl at the requested endset position **0.1, 0.2, or 0.3** via `retrieverestricted()`, with `whichend` (1, 2, or 3) directly selecting the position. [SS-FOLLOWLINK]

**Cross-check via RETRIEVEENDSETS**: The spanfilade search uses the same three ORGLRANGE prefixes — `LINKFROMSPAN=1`, `LINKTOSPAN=2`, `LINKTHREESPAN=3` — to recover all three endsets independently. [SS-RETRIEVE-ENDSETS]

The mapping is:
| Position | Endset |
|----------|--------|
| 0.1 | FROM (source) |
| 0.2 | TO (target) |
| 0.3 | THREE (type) |

This ordering is baked into constants at both write and read sites. The KB does not describe the internal tree topology of the orgl further than these positional addresses, but the positional ordering itself is structurally fixed and not derived from any runtime state.

---

## Code Exploration

I have verified all key line numbers. Here is my complete answer.

---

## Answer: Link Orgl Endset Positional Ordering

**Yes — the link orgl preserves positional ordering of the three endsets, and that ordering is structurally fixed at compile time.**

---

### 1. The Constants (xanadu.h:36-38)

Three integer constants define endset slot positions in both the orgl (V-space) and the spanfilade:

```c
#define LINKFROMSPAN    1   /* source */
#define LINKTOSPAN      2   /* target */
#define LINKTHREESPAN   3   /* type   */
```

These are the only names used anywhere in the codebase to address endsets. There are no aliases, no dynamic slot assignments, no runtime permutation.

---

### 2. Write Path — V-Space Addresses Assigned in `setlinkvsas` (do2.c:169-183)

Before insertion, each endset is given a fixed V-space address (VSA):

```c
bool setlinkvsas(tumbler *fromvsaptr, tumbler *tovsaptr, tumbler *threevsaptr)
{
    tumblerclear(fromvsaptr);
    tumblerincrement(fromvsaptr, 0, 1, fromvsaptr);   // source → V-pos 1
    tumblerincrement(fromvsaptr, 1, 1, fromvsaptr);

    tumblerclear(tovsaptr);
    tumblerincrement(tovsaptr, 0, 2, tovsaptr);       // target → V-pos 2
    tumblerincrement(tovsaptr, 1, 1, tovsaptr);

    if (threevsaptr) {
        tumblerclear(threevsaptr);
        tumblerincrement(threevsaptr, 0, 3, threevsaptr); // type → V-pos 3
        tumblerincrement(threevsaptr, 1, 1, threevsaptr);
    }
    return(TRUE);
}
```

The first `tumblerincrement` argument is the component index (0 = major axis); the second is the value. So source is anchored at V-position 1, target at 2, type at 3. These are tumbler addresses in the orgl's V-dimension — they don't shift with content.

---

### 3. Write Path — Orgl Insertion in `insertendsetsinorgl` (do2.c:130-148)

```c
bool insertendsetsinorgl(... tumbler *fromvsa, ... tumbler *tovsa, ... tumbler *threevsa, ...)
{
    if (!(  insertpm(taskptr, linkisaptr, link, fromvsa, fromsporglset)   // source first
         && insertpm(taskptr, linkisaptr, link, tovsa,   tosporglset)))   // target second
        return(FALSE);
    if (threevsa && threesporglset) {
        if (!insertpm(taskptr, linkisaptr, link, threevsa, threesporglset)) // type third
            return(FALSE);
    }
    return(TRUE);
}
```

Each `insertpm` call places content at the VSA established by `setlinkvsas`. Insertion order mirrors address order: 1 → 2 → 3.

This is invoked from `docreatelink` (do1.c:217-218):

```c
&& setlinkvsas(&fromvsa, &tovsa, &threevsa)
&& insertendsetsinorgl(taskptr, linkisaptr, link,
                       &fromvsa, fromsporglset,
                       &tovsa, tosporglset,
                       &threevsa, threesporglset)
```

---

### 4. Write Path — Spanfilade Tagging in `insertendsetsinspanf` (do2.c:116-128)

The spanfilade (used for link lookup by content span) receives the same ordering:

```c
insertspanf(taskptr, spanfptr, linkisaptr, fromsporglset, LINKFROMSPAN)   // tag=1
  && insertspanf(taskptr, spanfptr, linkisaptr, tosporglset, LINKTOSPAN)  // tag=2
if (threesporglset)
    insertspanf(taskptr, spanfptr, linkisaptr, threesporglset, LINKTHREESPAN) // tag=3
```

The integer tag passed to `insertspanf` is exactly the `LINK*SPAN` constant — same scheme used in the orgl's V-addresses.

---

### 5. Read Path — Orgl Retrieval in `link2sporglset` (sporgl.c:67-95)

The follow path takes a `whichend` parameter (1, 2, or 3) and performs a V-space lookup directly at that position:

```c
tumblerclear(&zero);
tumblerincrement(&zero, 0, whichend, &vspan.stream);   // address = whichend
tumblerincrement(&zero, 0/*1*/, 1, &vspan.width);
if (context = retrieverestricted((typecuc*)orgl, &vspan, V, ...)) { ... }
```

`whichend` maps directly onto the V-positions established at write time: pass 1 to get source, 2 for target, 3 for type. There is no indirection, no lookup table, no reordering.

(Note: the commented-out `/*1*/` on line 82 records a past edit — the width's component index was changed from 1 to 0, meaning width is expressed in the same major dimension as stream rather than a separate component. This affects retrieval window geometry, not endset identity.)

The caller `dofollowlink` (do1.c:223-231) passes `whichend` straight from the FEBE protocol handler, which in turn validates it is 1, 2, or 3 (get1.c:68-74).

---

### 6. Read Path — Spanfilade Retrieval in `retrieveendsetsfromspanf` (spanf1.c:190-235)

The spanf-based retrieval path constructs the same three query spans from the same constants:

```c
fromspace.stream.mantissa[0]   = LINKFROMSPAN;    // 1
fromspace.width.mantissa[0]    = 1;

tospace.stream.mantissa[0]     = LINKTOSPAN;      // 2
tospace.width.mantissa[0]      = 1;

threespace.stream.mantissa[0]  = LINKTHREESPAN;   // 3
threespace.width.mantissa[0]   = 1;
```

Then retrieves them in that order via `retrievesporglsetinrange` + `linksporglset2specset`. Source, target, type — same sequence as write.

---

### Conclusion

The positional ordering is **structurally fixed** in three independent ways:

1. **Compile-time constants** in `xanadu.h:36-38` — `LINKFROMSPAN=1`, `LINKTOSPAN=2`, `LINKTHREESPAN=3` — are used unchanged by every write and read function.
2. **V-space addressing** — `setlinkvsas` encodes each endset at a tumbler address whose major component equals its slot number. The orgl retrieves by that same address; V-space is an ordered addressing space, not a bag.
3. **No permutation anywhere** — neither `insertendsetsinorgl`, `link2sporglset`, `retrieveendsetsfromspanf`, nor any intermediate function reorders, sorts, or remaps endsets. The path from `docreatelink` → `setlinkvsas` → `insertpm` → `retrieverestricted` → `link2sporglset` is positionally faithful end to end.

A direct read of the link orgl at V-position `n` returns exactly and only the endset written at V-position `n`. The source/target/type assignment is part of the data model, baked in at the level of the address scheme itself.
