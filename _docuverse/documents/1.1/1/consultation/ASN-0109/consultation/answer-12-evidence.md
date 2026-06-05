## Question 12 [evidence]

> Does reading endsets resolve the stored I-address spans into V-positions, or does the reader receive raw I-addresses from the link orgl before any I→V conversion occurs?

## KB Synthesis

Endset reading always delivers V-positions — the I→V conversion is internal to both retrieval paths, never exposed to the caller.

**FOLLOWLINK** [SS-FOLLOWLINK] performs a two-phase process: `link2sporglset()` pulls the stored I-addresses from the link orgl (via `retrieverestricted()`), then `linksporglset2specset()` converts those I-addresses to V-addresses by looking them up in the specified `homedoc`'s POOM. The caller receives a specset of V-spans, not raw I-addresses.

**RETRIEVEENDSETS** [SS-RETRIEVE-ENDSETS] works through the spanfilade rather than the link orgl directly: it converts the input V-specset to I-addresses (sporglset), searches the spanfilade by I-address range, then converts results back to V-addresses using the *querying document's* docid — not the link's home document. This means endsets are always expressed relative to the query context.

A critical consequence: if an I-address has no POOM mapping in the queried document (e.g., after deletion), `span2spanset()` returns NULL and that I-address is **silently dropped** from the result [INV-ITOV-FILTERING]. This is why ghost links [EC-GHOST-LINK] return empty specsets rather than errors — the I-addresses exist in permanent storage but resolve to nothing in the current POOM.

The two operations differ in what they look up: FOLLOWLINK reads from the link orgl directly given a known link ISA; RETRIEVEENDSETS discovers links via the spanfilade given a content region. Both deliver V-address specsets as output.

---

## Code Exploration

All key code is confirmed. Here is my full answer.

---

## Reading Endsets: I-Address Storage vs. V-Position Delivery

The link orgl stores endsets as **I-addresses**. The FEBE client receives **V-positions** — because I→V conversion is performed within the same call chain as the orgl retrieval, before the result is returned. There is one exception: raw I-spans with no homedoc pass through unconverted.

---

### The Read Path, Step by Step

#### 1. FEBE Handler — `fns.c:114`

```c
void followlink(typetask *taskptr)
{
  ...
    if (getfollowlink(taskptr, &linkisa, &whichend)
     && dofollowlink(taskptr, &linkisa, &specset, whichend))
        putfollowlink(taskptr, specset);
```

The FEBE `followlink` handler calls `dofollowlink`, then immediately serializes the result via `putfollowlink`. The client sees whatever `dofollowlink` returns.

---

#### 2. Core Dispatch — `do1.c:223`

```c
bool dofollowlink(typetask *taskptr, typeisa *linkisaptr, typespecset *specsetptr, INT whichend)
{
  typesporglset sporglset;

    return (
       link2sporglset(taskptr, linkisaptr, &sporglset, whichend, NOBERTREQUIRED)
    && linksporglset2specset(taskptr, &((typesporgl *)sporglset)->sporgladdress,
                             sporglset, specsetptr, NOBERTREQUIRED));
}
```

Two phases, sequential and mandatory:
- `link2sporglset` → retrieve raw I-addresses from the link orgl
- `linksporglset2specset` → convert to final specset (which may or may not invoke I→V)

---

#### 3. Retrieving Raw I-Addresses from the Link Orgl — `sporgl.c:67`

```c
bool link2sporglset(typetask *taskptr, typeisa *linkisa, typesporglset *sporglsetptr, INT whichend, int type)
{
  ...
    tumblerincrement(&zero, 0, whichend, &vspan.stream);   // slot: 1=from, 2=to, 3=three
    tumblerincrement(&zero, 0, 1,        &vspan.width);

    if (context = retrieverestricted((typecuc*)orgl, &vspan, V, (typespan*)NULL, I, (typeisa*)NULL)) {
        for (c = context; c; c = c->nextcontext) {
            sporglptr = ...
            contextintosporgl((type2dcontext*)c, (tumbler*)NULL, sporglptr, I);
```

- `vspan` encodes the slot number (whichend) as the V-axis position — this is the link orgl's addressing scheme: V-position 1 = from-endset, 2 = to-endset, 3 = three-endset.
- `retrieverestricted(..., &vspan, V, NULL, I, ...)` queries the orgl **restricted to that V-position**, extracting the **I-axis** data [`sporgl.c:83`].
- `contextintosporgl(..., I)` [`sporgl.c:86`] populates the sporgl with:
  - `sporgladdress` ← `context->context2dinfo.homedoc` (the document tumbler, usually non-zero) [`sporgl.c:209`]
  - `sporglorigin` ← `context->totaloffset.dsas[I]` (raw I-axis offset) [`sporgl.c:211`]
  - `sporglwidth` ← `context->contextwid.dsas[I]` (raw I-axis width) [`sporgl.c:219`]

**At this point the sporgl holds raw I-addresses.** The data has not been converted to V-positions yet.

---

#### 4. The Conversion Fork — `sporgl.c:97`

```c
bool linksporglset2specset(typetask *taskptr, typeisa *homedoc, typesporglset sporglset,
                           typespecset *specsetptr, int type)
{
    for (; sporglset; ...) {
        if (iszerotumbler(&((typesporgl *)sporglset)->sporgladdress)) {
            // No homedoc: pass through as raw I-span
            ((typeitemheader *)specset)->itemid = ISPANID;
            movetumbler(&sporglset->sporglorigin, &((typeispan *)specset)->stream);
            movetumbler(&sporglset->sporglwidth,  &((typeispan *)specset)->width);
        } else {
            linksporglset2vspec(taskptr, homedoc, &sporglset, (typevspec*)specset, type);
        }
    }
}
```

`sporgl.c:105`: Branch on whether `sporgladdress` (the homedoc tumbler) is zero:

| Condition | Path | Result |
|-----------|------|--------|
| `sporgladdress == 0` | raw I-span passthrough | `ISPANID` — client gets raw I-addresses |
| `sporgladdress != 0` | I→V conversion | `VSPECID` — client gets V-positions |

The zero case is the edge path (raw I-spans unattached to any document). In practice, all content has a homedoc, so the non-zero branch is normal.

---

#### 5. I→V Conversion Chain — `sporgl.c:127` → `sporgl.c:141` → `orglinks.c:389`

```c
// sporgl.c:136
sporglset2vspanset(taskptr, homedoc, sporglsetptr, &specptr->vspanset, type);

// sporgl.c:157 — core I→V call
vspansetptr = ispan2vspanset(taskptr, orgl, &ispan, vspansetptr);

// orglinks.c:389
typevspanset *ispan2vspanset(typetask *taskptr, typeorgl orgl, typeispan *ispanptr, typevspanset *vspansetptr)
{
    return permute(taskptr, orgl, ispanptr, I, vspansetptr, V);
}
```

`permute` with `(I → V)` calls `span2spanset` [`orglinks.c:415`], which calls:

```c
// orglinks.c:435
context = retrieverestricted((typecuc*)orgl, restrictionspanptr, I,  // restrict by I
                             (typespan*)NULL,                        // no further clamp
                             V,                                      // extract V axis
                             (typeisa*)NULL);
```

This is the inverse of the write-path `vspanset2ispanset`. It queries the content document's orgl (the permutation matrix), restricts to the I-address range, and extracts the corresponding V-positions.

---

### The Write Path (Confirming Storage Format)

During link creation (`do1.c:214–219`), the input endsets (which may be V-specs) are first converted to I-addresses:

```c
specset2sporglset(taskptr, fromspecset,  &fromsporglset, NOBERTREQUIRED)
specset2sporglset(taskptr, tospecset,    &tosporglset,   NOBERTREQUIRED)
specset2sporglset(taskptr, threespecset, &threesporglset,NOBERTREQUIRED)
```

`specset2sporglset` → `vspanset2sporglset` (sporgl.c:35) calls `vspanset2ispanset` (orglinks.c:397–401) which is `permute(V → I)`. The I-addresses are then stored in the link orgl via `insertendsetsinorgl`.

**Conclusion: the link orgl stores I-addresses. The I→V round-trip is complete and symmetric.**

---

### Summary

```
WRITE path:  V-spec → vspanset2ispanset (V→I) → store in link orgl
READ  path:  load from link orgl (raw I-addresses) → ispan2vspanset (I→V) → V-spec returned to client
```

The FEBE client **receives V-positions**, not raw I-addresses. The I→V conversion via `ispan2vspanset` at `orglinks.c:389` (called from `sporglset2vspanset` at `sporgl.c:157`) occurs entirely within the `dofollowlink` call, before `putfollowlink` serializes the result.

The only case where a FEBE client would receive a raw I-address (`ISPANID`) from `linksporglset2specset` is if a sporgl has `sporgladdress == 0` [`sporgl.c:105`] — an I-span with no associated document. This is the exception path, not the normal case.
