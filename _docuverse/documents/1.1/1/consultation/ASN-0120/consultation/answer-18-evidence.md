## Question 18 [evidence]

> Does the type endset (third endset) get stored structurally identical to source and target endsets as an I-address span, with the link type itself registered at `1.0.2.x` in the global type namespace, distinguishing a typed relation from an untyped from→to connection?

## KB Synthesis

Yes, but with an important distinction in what the I-address span *refers to*.

**Structural storage: identical to source/target**

The type ("three") endset is indexed in the spanfilade under `LINKTHREESPAN=3`, parallel to `LINKFROMSPAN=1` and `LINKTOSPAN=2` [SS-RETRIEVE-ENDSETS]. `insertendsetsinspanf()` receives sporglsets for all three endpoint types and inserts each into the spanf index tagged by endpoint type [INT-SPORGL-LINK-INDEX]. The POOM uses a dedicated third subspace at `3.x` for type endpoints — the same V-space partitioning that puts link orgls at `2.x` and text at `1.x` [SS-DUAL-ENFILADE, Finding 0038].

So mechanically: yes, an I-address span, stored and indexed identically.

**Content: a reference into the bootstrap type registry**

The I-addresses in the type endset point into the bootstrap document's type subspace at `1.0.2.x`, not into arbitrary user content [SS-LINK-ENDPOINT, Finding 0024]:

| Type | Bootstrap address |
|------|-------------------|
| JUMP | `1.0.2.2` |
| QUOTE | `1.0.2.3` |
| FOOTNOTE | `1.0.2.6` |
| MARGIN | `1.0.2.6.2` |

Tumbler containment encodes the type hierarchy — `1.0.2.6.2` is a subtype of `1.0.2.6` — enabling range queries like "find all footnote-family links."

**Distinguishing typed from untyped**

The KB documents `FINDLINKSFROMTOTHREE` accepting `NOSPECS` for any of the three parameters [SS-FIND-LINKS, SS-PAGINATE-LINKS], so type is optional for *querying*. Whether passing `NOSPECS` (or zero-width, which crashes for source/target per [PRE-ZERO-WIDTH]) at *creation* time produces a valid typeless link is not answerable from the KB — the creation preconditions for the three-endset are not explicitly documented.

---

## Code Exploration

I have everything I need. Here is the full answer.

---

## Third Endset Storage: Structure, V-Space, and ISA Allocation

### The Short Answer

The type endset (third endset, called `threespecset` in the code) **is stored structurally identical** to the from and to endsets as a `typesporgl` — an I-address span plus home document reference. The link object itself gets an ISA at `<docISA>.0.2.x` relative to its home document (because `LINKATOM = 2`), but **there is no global type namespace at `1.0.2.x`**. The third endset's content is an arbitrary I-address span; the backend applies no type semantics to it.

---

### The Data Structures

**I-span** (`xanadu.h:65-70`):

```c
typedef struct structtypespan{
    struct structtypespan *next;
    typeitemid      itemid;
    tumbler stream;       // address (V or I)
    tumbler width;
} typespan;
typedef typespan typeispan;
```

**Sporgl** — the endset storage unit (`xanadu.h:115-121`):

```c
typedef struct structsporgl{
    struct structsporgl *next;
    typeitemid	itemid;
    tumbler sporglorigin;    // I-space start address
    tumbler sporglwidth;     // I-space width
    typeisa sporgladdress;   // home document ISA
} typesporgl;
```

A sporgl **is** an I-span with a document reference appended. `sporglorigin`/`sporglwidth` directly parallel `stream`/`width`. Every endset — from, to, and three — resolves to this same structure.

---

### Link Creation: All Three Endsets Follow Identical Paths

`createlink` in `fns.c:100-112` dispatches to `docreatelink` in `do1.c:195-221`:

```c
bool docreatelink(typetask *taskptr, typeisa *docisaptr,
                  typespecset fromspecset, typespecset tospecset,
                  typespecset threespecset, typeisa *linkisaptr)
{
    ...
    && specset2sporglset(taskptr, fromspecset,   &fromsporglset, NOBERTREQUIRED)  // do1.c:214
    && specset2sporglset(taskptr, tospecset,     &tosporglset,   NOBERTREQUIRED)  // do1.c:215
    && specset2sporglset(taskptr, threespecset,  &threesporglset,NOBERTREQUIRED)  // do1.c:216
    && setlinkvsas(&fromvsa, &tovsa, &threevsa)                                   // do1.c:217
    && insertendsetsinorgl(taskptr, linkisaptr, link,
                           &fromvsa, fromsporglset,
                           &tovsa,   tosporglset,
                           &threevsa,threesporglset)                              // do1.c:218
    && insertendsetsinspanf(taskptr, spanf, linkisaptr,
                            fromsporglset, tosporglset, threesporglset)           // do1.c:219
```

All three endsets go through the exact same conversion function (`specset2sporglset`) and the exact same storage functions (`insertpm` via `insertendsetsinorgl`, `insertspanf` via `insertendsetsinspanf`). The sporgl type (`SPORGLID = 6`, `xanadu.h:32`) is identical for all three.

---

### The V-Space Positions: 1.1, 2.1, 3.1

`setlinkvsas` in `do2.c:169-183` assigns the endsets their V-space slots **within the link's own orgl**:

```c
bool setlinkvsas(tumbler *fromvsaptr, tumbler *tovsaptr, tumbler *threevsaptr)
{
    tumblerclear(fromvsaptr);
    tumblerincrement(fromvsaptr, 0, 1, fromvsaptr);   // mantissa[0] = 1
    tumblerincrement(fromvsaptr, 1, 1, fromvsaptr);   // mantissa[1] = 1 → 1.1

    tumblerclear(tovsaptr);
    tumblerincrement(tovsaptr, 0, 2, tovsaptr);       // mantissa[0] = 2
    tumblerincrement(tovsaptr, 1, 1, tovsaptr);       // mantissa[1] = 1 → 2.1

    if (threevsaptr) {
        tumblerclear(threevsaptr);
        tumblerincrement(threevsaptr, 0, 3, threevsaptr);   // mantissa[0] = 3
        tumblerincrement(threevsaptr, 1, 1, threevsaptr);   // mantissa[1] = 1 → 3.1
    }
    return(TRUE);
}
```

`tumblerincrement(ptr, rightshift, bint, dst)` from `tumble.c:599-623`: when incrementing from zero it sets `exp = -rightshift, mantissa[0] = bint`; when incrementing a nonzero tumbler it finds the rightmost nonzero mantissa position `idx` and adds `bint` at `mantissa[idx + rightshift]`. So `1.1`, `2.1`, `3.1` are three two-digit tumblers — endset V-addresses within the link's private permutation matrix.

The spanfilade uses the corresponding type constants (`xanadu.h:36-38`):

```c
#define LINKFROMSPAN    1
#define LINKTOSPAN      2
#define LINKTHREESPAN   3
```

`insertspanf` in `spanf1.c:22` does `prefixtumbler(isaptr, spantype, &crumorigin.dsas[ORGLRANGE])` — the link's ISA prefixed with 1, 2, or 3 forms the ORGL key for the two-dimensional spanfilade lookup. This is the only way the three endsets are distinguished.

---

### Link ISA Allocation: `<docISA>.0.2.x`, Not a Global `1.0.2.x`

`LINKATOM = 2` is defined at `xanadu.h:146`. The hint is built at `do1.c:207`:

```c
makehint(DOCUMENT, ATOM, LINKATOM, docisaptr, &hint);
```

This triggers `findisatoinsertmolecule` in `granf2.c:158-176`:

```c
} else if (hintptr->atomtype == LINKATOM) {
    tumblerincrement(&hintptr->hintisa, 2, 2, isaptr);   // granf2.c:171
    if (tumblercmp(&lowerbound, isaptr) == LESS)
        tumblerincrement(isaptr, 1, 1, isaptr);
    else
        tumblerincrement(&lowerbound, 0, 1, isaptr);
}
```

Line 171: `tumblerincrement(&hintptr->hintisa, 2, 2, isaptr)` finds the rightmost nonzero mantissa position `idx` of the document's ISA, then adds `2` at `mantissa[idx + 2]`. This is appending `.0.2` (two levels deeper, with value 2) to the document's ISA. First link: `tumblerincrement(isaptr, 1, 1, isaptr)` adds one more level → `<docISA>.0.2.0.1`.

If the document lives at ISA `D`, then:
- First link → `D.0.2.0.1`
- Second link → `D.0.2.0.2`
- …

The `1.0.2.x` pattern is not a global namespace. It would only appear if the home document's ISA happened to be `1` — a trivially simple address that no real document would have. Documents have multi-component ISAs like `1.0.1.0.1.0.1`. The `.0.2` suffix is **per-document**, not global.

Nowhere in `fns.c`, `do1.c`, `do2.c`, or any header does the code define or reference a global type namespace. `LINKATOM = 2` is an atom-type discriminator (vs. `TEXTATOM = 1`), used only to drive the ISA allocation formula above.

---

### Two-Endset vs. Three-Endset Links

There is also `domakelink` in `do1.c:169-193` — a two-endset variant that passes `NULL` for the third:

```c
&& setlinkvsas(&fromvsa, &tovsa, NULL)
&& insertendsetsinorgl(taskptr, linkisaptr, link,
                       &fromvsa, fromsporglset,
                       &tovsa,   tosporglset,
                       NULL,     NULL)
&& insertendsetsinspanf(taskptr, spanf, linkisaptr,
                        fromsporglset, tosporglset, NULL)
```

The guards in `insertendsetsinorgl` (`if (threevsa && threesporglset)` at `do2.c:136`) and `insertendsetsinspanf` (`if (threesporglset)` at `do2.c:122`) mean that a link with no third endset simply lacks slot 3 in both storage structures. However, `domakelink` is not exposed through the FEBE interface — only `docreatelink` (via `createlink` at `fns.c:100`) is public. The public API always takes a `threespecset` argument, which callers may pass empty.

---

### Summary

| Claim | Finding |
|---|---|
| Third endset structurally identical to from/to? | **Yes.** All three are `typesporgl` items, stored via the same `specset2sporglset` → `insertpm` + `insertspanf` pipeline. |
| Distinguishing feature of third endset? | V-position `3.1` in link orgl; spanfilade type tag `LINKTHREESPAN=3`. No other structural difference. |
| Link type registered at `1.0.2.x` globally? | **No.** Links get ISAs at `<docISA>.0.2.x` within their home document's namespace. No global `1.0.2.x` type namespace exists in the code. |
| Third endset carries type semantics? | **No.** The backend treats it as an arbitrary I-address span. Semantic meaning of "type" is imposed by convention at a higher layer, not enforced in the storage code. |
