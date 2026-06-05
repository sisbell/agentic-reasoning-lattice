## Question 12 [evidence]

> How is the end selector encoded — as a fixed index into the three stored endsets (source/from, target/to, type), and what happens if a selector value outside that range is supplied?

## KB Synthesis

## End Selector Encoding in FOLLOWLINK

### Encoding as Orgl Sub-position

The `whichend` parameter selects one of three positions within the link orgl structure using integer constants that map to tumbler sub-positions [SS-FOLLOWLINK]:

| Selector | Constant | Orgl Sub-position | Endset |
|----------|----------|-------------------|--------|
| 1 | LINKFROMSPAN | 0.1 | Source/from endpoint |
| 2 | LINKTOSPAN | 0.2 | Target/to endpoint |
| 3 | LINKTHREESPAN | 0.3 | Type endpoint |

`link2sporglset()` passes the selector to `retrieverestricted()`, which searches the link orgl restricted to the specified sub-position range [SS-FOLLOWLINK]. The same three constants appear in RETRIEVEENDSETS, where they partition the ORGLRANGE dimension of the spanfilade [SS-RETRIEVE-ENDSETS].

### Out-of-Range Behavior

The KB does not document explicit out-of-range handling. However, the general INV-ITOV-FILTERING invariant applies [INV-ITOV-FILTERING]: `retrieverestricted()` returns NULL when no content is found at the queried range, and `span2spanset()` silently drops unreferenced I-addresses rather than raising an error. An out-of-range selector would cause `retrieverestricted()` to search a sub-position with no stored endset data, yielding an empty sporglset and an empty V-span result — the same outcome as a ghost link [EC-GHOST-LINK]. The operation would succeed with an empty result, not error.

The KB does not confirm this with an explicit test; it is inferred from the silent-drop mechanism.

---

## Code Exploration

I now have the complete picture. Here is the full answer:

---

## How the End Selector Is Encoded

### The Constants

`xanadu.h:36-38` defines the three span types as a fixed numeric sequence:

```c
/* spanfilade span types */
#define LINKFROMSPAN    1
#define LINKTOSPAN      2
#define LINKTHREESPAN   3
#define DOCISPAN        4
```

The selector is not a symbolic enum with an offset — it **is** the literal integer 1, 2, or 3, used directly as a virtual-address coordinate in the link's POOM and as a spanfilade type tag.

---

### Storage: How the Three Endsets Are Written

When a link is created, `docreatelink` (`do1.c:195-221`) calls `setlinkvsas` to assign a virtual address to each endset slot:

**`setlinkvsas` (`do2.c:169-183`):**
```c
bool setlinkvsas(tumbler *fromvsaptr, tumbler *tovsaptr, tumbler *threevsaptr)
{
    tumblerclear (fromvsaptr);
    tumblerincrement (fromvsaptr, 0, 1, fromvsaptr);   // V = 1 = LINKFROMSPAN
    tumblerincrement (fromvsaptr, 1, 1, fromvsaptr);
    tumblerclear (tovsaptr);
    tumblerincrement (tovsaptr, 0, 2, tovsaptr);       // V = 2 = LINKTOSPAN
    tumblerincrement (tovsaptr, 1, 1, tovsaptr);
    if (threevsaptr) {
        tumblerclear (threevsaptr);
        tumblerincrement (threevsaptr, 0, 3, threevsaptr);  // V = 3 = LINKTHREESPAN
        tumblerincrement (threevsaptr, 1, 1, threevsaptr);
    }
    return (TRUE);
}
```

The from-endset occupies V-coordinate `1.1`, the to-endset `2.1`, the type-endset `3.1`. These are then written into the link's granfilade POOM via `insertendsetsinorgl` → `insertpm`.

Simultaneously, **`insertendsetsinspanf`** (`do2.c:116-128`) writes the same endsets into the global spanfilade using the constants as explicit span-type tags:

```c
insertspanf(taskptr, spanfptr, linkisaptr, fromsporglset,  LINKFROMSPAN)
insertspanf(taskptr, spanfptr, linkisaptr, tosporglset,    LINKTOSPAN)
insertspanf(taskptr, spanfptr, linkisaptr, threesporglset, LINKTHREESPAN)
```

Inside `insertspanf` (`spanf1.c:22`):
```c
prefixtumbler (isaptr, spantype, &crumorigin.dsas[ORGLRANGE]);
```
The link ISA is stored in the spanfilade's orgl-dimension with the spantype (1, 2, or 3) as its leading tumbler component.

---

### Retrieval: How `whichend` Selects an Endset

When the client calls `followlink`, `fns.c:114-127` dispatches to `dofollowlink` → `link2sporglset` (`sporgl.c:67-95`), passing `whichend` unchanged:

**`link2sporglset` (`sporgl.c:80-83`):**
```c
tumblerclear (&zero);
tumblerincrement (&zero, 0, whichend, &vspan.stream);  // stream = whichend (1, 2, or 3)
tumblerincrement (&zero, 0/*1*/, 1, &vspan.width);     // width = 1
if (context = retrieverestricted((typecuc*)orgl, &vspan, V, (typespan*)NULL, I, (typeisa*)NULL)) {
```

The integer `whichend` is used **directly as the V-coordinate stream value**. `retrieverestricted` queries the link's granfilade POOM for everything in the range `[whichend, whichend+1)`. Because the from-, to-, and type-endsets were stored at V = 1, 2, and 3 respectively, `whichend` is a literal index into those fixed positions — there is no offset arithmetic, no array dereference, and no symbolic dispatch.

---

### What Happens With a Value Outside 1–3

The guard is in `getfollowlink` (`get1.c:63-74`):

```c
bool getfollowlink(typetask *taskptr, typeisa *linkisaptr, INT *whichendptr)
{
    prompt (taskptr, "enter link=> ");
    if (!getisa (taskptr, linkisaptr))
        return (FALSE);
    prompt (taskptr, "enter endset=> ");
    if (!(
       getnumber (taskptr, whichendptr)
    && (*whichendptr == 1 || *whichendptr == 2 || *whichendptr == 3)))
        return (FALSE);
    return (TRUE);
}
```

The check is a strict whitelist: `== 1 || == 2 || == 3`. Any other value — 0, 4, negative, anything — makes the entire condition false and `getfollowlink` returns `FALSE`.

`followlink` in `fns.c:121-127` short-circuits on that:
```c
if (
   getfollowlink (taskptr, &linkisa, &whichend)
&& dofollowlink (taskptr, &linkisa, &specset, whichend)){
      putfollowlink (taskptr, specset);
   }else
      putrequestfailed (taskptr);
```

`dofollowlink` is never called; `putrequestfailed` emits a protocol-level error response to the client.

**If the guard were bypassed** and `link2sporglset` were called directly with, say, `whichend = 0` or `4`: it would construct `vspan.stream = 0` (or 4) and query the link's POOM at a position where nothing was stored. `retrieverestricted` would return `NULL`, the `if (context = ...)` branch would fail, and `link2sporglset` would `return (FALSE)` — propagating failure through `dofollowlink` and again invoking `putrequestfailed`. Note that `DOCISPAN = 4` is the next defined span type (used for document-content spans), so querying with `whichend = 4` against a link object would find no link-endset data at that V-coordinate either.

---

### Summary

| Selector value | Meaning | Where stored (V-coordinate) |
|---|---|---|
| 1 (`LINKFROMSPAN`) | from / source endset | `1.1` in link POOM |
| 2 (`LINKTOSPAN`) | to / target endset | `2.1` in link POOM |
| 3 (`LINKTHREESPAN`) | type / three endset | `3.1` in link POOM |
| any other | — | rejected at `get1.c:71` |

The selector is a fixed, consecutive integer index (1/2/3) that doubles as both a virtual-address component at storage time (`setlinkvsas`, `do2.c:169-183`) and the V-coordinate query argument at retrieval time (`link2sporglset`, `sporgl.c:81`). Out-of-range values are rejected at the input layer by a whitelist check (`get1.c:71`) before any enfilade operation is attempted; the backend responds with a protocol failure, not a crash or undefined behavior.
