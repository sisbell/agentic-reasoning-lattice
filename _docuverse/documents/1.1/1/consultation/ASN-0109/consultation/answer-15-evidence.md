## Question 15 [evidence]

> Since endsets reference content by I-address identity, does reading a link's source endset reveal the same I-spans regardless of which document or version the linked content currently appears in?

## KB Synthesis

**Yes and no — the I-spans stored in the endset are stable, but their V-address rendering is context-dependent.**

## The stable part: raw endset I-spans

The link orgl stores endset sporgls at creation time in I-space [SS-SPORGL]. These are permanent. `link2sporglset()` extracts I-addresses directly from the link orgl without any POOM lookup — it always returns the same I-address ranges [SS-FOLLOWLINK Finding 0048]:

> "link2sporglset() extracts I-addresses from the link orgl at the requested endset position via retrieverestricted() — no POOM check occurs at this stage."

Since the link orgl is in I-space (append-only, never deleted), and I-addresses are immutable [INV-IADDR-IMMUTABILITY, INV-LINK-PERMANENCE], the raw I-spans in the source endset are identical regardless of which document or version asks.

## The context-dependent part: V-address conversion

FOLLOWLINK's second phase — `linksporglset2specset()` — converts those I-addresses to V-spans by looking them up in a **specific** document's POOM [SS-FOLLOWLINK]:

> "The same link endset can produce different V-address results (or empty results) depending on which document context is used."

The filtering invariant [INV-ITOV-FILTERING] applies universally: any I-address with no POOM mapping in the queried document is **silently dropped**. So the same endset produces:
- Full V-spans in a document whose POOM maps those I-addresses
- Empty results in a document whose POOM has no mapping (e.g., after deletion) [EC-GHOST-LINK]

## One wrinkle at creation time

If the linked V-span covered content transcluded from multiple sources, the endset contains **multiple I-spans**, not one — one per contiguous I-address region [SS-LINK-ENDPOINT Finding 0037, ST-LINK-CREATE Finding 0037]. This decomposition happens at creation and is also fixed thereafter.

## Summary

| Layer | Stable? |
|-------|---------|
| I-spans stored in the link orgl | **Yes** — immutable, same for all callers |
| V-address rendering via FOLLOWLINK | **No** — depends on which document's POOM is queried |

The I-spans revealed by the endset are identical everywhere; only their V-space projection varies by context [SS-FOLLOWLINK, INV-ITOV-FILTERING, INV-LINK-PERMANENCE].

---

## Code Exploration

Now I have everything I need. Let me trace the complete path carefully.

---

## Answer

**Yes — a link's source endset stores I-spans, and those I-spans are stable regardless of which document or version the linked content currently appears in.** However, the V-spans that `dofollowlink` actually returns to the client are computed by mapping those I-spans back through the *original* document's orgl, not through any newer version.

---

### What a sporgl is

The unit of endset storage is `typesporgl` [xanadu.h:115-121]:

```c
typedef struct structsporgl {
    struct structsporgl *next;
    typeitemid   itemid;
    tumbler      sporglorigin;    /* I-span origin (permascroll address) */
    tumbler      sporglwidth;     /* I-span width  (permascroll address) */
    typeisa      sporgladdress;   /* document ISA — NOT a V-span */
} typesporgl;
```

Three fields. Two are I-coordinates (`sporglorigin`, `sporglwidth`). One is the document ISA (`sporgladdress`). There is no V-span stored anywhere in the endset.

---

### How a link is created: V→I happens once, at creation time

`docreatelink` [do1.c:195-221] converts the caller-supplied V-spec endsets into sporgls:

```
docreatelink
  └─ specset2sporglset        [sporgl.c:14]
       └─ vspanset2sporglset  [sporgl.c:35]
```

Inside `vspanset2sporglset` [sporgl.c:35-65]:

```c
// line 48
(void) vspanset2ispanset(taskptr, orgl, vspanset, &ispanset);
for (; ispanset; ispanset = ispanset->next) {
    // ...
    movetumbler(docisa, &sporglset->sporgladdress);  // line 53: store doc ISA
    movetumbler(&ispanset->stream, &sporglset->sporglorigin);  // line 54: store I-origin
    movetumbler(&ispanset->width,  &sporglset->sporglwidth);   // line 55: store I-width
```

`vspanset2ispanset` [orglinks.c:397-402] calls `permute(V→I)` — it walks the document's POOM enfilade and extracts the I-coordinate paired with each V-address. The result is pure permascroll address.

From this point forward the endset contains **only I-coordinates + document ISA**. The V-addresses that the caller provided are discarded. They are never stored.

---

### How a link is followed: I-spans are read back first

`dofollowlink` [do1.c:223-232]:

```c
return (
   link2sporglset(taskptr, linkisaptr, &sporglset, whichend, NOBERTREQUIRED)
&& linksporglset2specset(taskptr, &((typesporgl*)sporglset)->sporgladdress,
                         sporglset, specsetptr, NOBERTREQUIRED));
```

`link2sporglset` [sporgl.c:67-95] queries the link's own orgl:

```c
// line 83
if (context = retrieverestricted((typecuc*)orgl, &vspan, V,
                                  (typespan*)NULL, I, (typeisa*)NULL)) {
    for (c = context; c; c = c->nextcontext) {
        // ...
        contextintosporgl((type2dcontext*)c, (tumbler*)NULL, sporglptr, I);  // line 86
```

`contextintosporgl` [sporgl.c:205-220]:

```c
movetumbler(&context->context2dinfo.homedoc, &sporglptr->sporgladdress); // line 209
movetumbler(&context->totaloffset.dsas[I],   &sporglptr->sporglorigin);  // line 211
movetumbler(&context->contextwid.dsas[I],    &sporglptr->sporglwidth);   // line 219
```

The `dsas[I]` fields come directly from the POOM crum's I-dimension — the same I-coordinates that were stored when the link was created. **They have never changed.** The POOM is an enfilade; its crums encode a fixed V↔I pairing established at insertion time. No subsequent document version can alter those stored I-coordinates.

---

### The I→V translation on the way out

After `link2sporglset` reconstructs the in-memory sporgl list, `linksporglset2specset` [sporgl.c:97-123] converts to a specset for the caller:

```c
if (iszerotumbler(&((typesporgl*)sporglset)->sporgladdress)) {
    // zero address → raw I-span returned as ISPANID  [lines 112-114]
} else {
    linksporglset2vspec(taskptr, homedoc, &sporglset, (typevspec*)specset, type); // line 116
```

For the non-trivial case, `sporglset2vspanset` [sporgl.c:141-176]:

```c
// line 152
(void) findorgl(taskptr, granf, homedoc/*&sporglptr->sporgladdress*/, &orgl, type);
// ...
// line 157
vspansetptr = ispan2vspanset(taskptr, orgl, &ispan, vspansetptr);
```

`ispan2vspanset` [orglinks.c:389-394]:

```c
return permute(taskptr, orgl, ispanptr, I, vspansetptr, V);
```

This calls `permute(I→V)` — it queries the document's current POOM to find what V-position corresponds to each I-span. The `homedoc` used here is `sporglset->sporgladdress` — the **original document ISA that was stored at link creation time**, not the current version or any other document.

---

### What this means for the question

The I-spans in `sporglorigin`/`sporglwidth` are **permanently fixed at the permascroll level**. They identify content by its origin in the global I-coordinate space (the permascroll). This identity does not depend on:

- Which document the content was inserted into
- Whether new versions of that document exist
- Whether the content was copied into other documents

So: **reading a link's endset always recovers the same I-spans**, regardless of document history or versioning. The I-address is the stable identity.

What *does* vary is the V-span returned to the client. `dofollowlink` maps those fixed I-spans back to V-addresses in the **original referencing document** (`sporgladdress`, stored at link creation). If that document has never changed, the V-addresses are stable too. If the content was copied to a new document or a new version was made, the V-spans in this call still point to the original document — the link "knows" only about that document's coordinate space.

To find the same content (same I-spans) in a different document, a separate operation is needed: `dofinddocscontaining` [do1.c:15-23], which inverts the I-spans through other documents' orlgs.

---

### Summary of the call chain

```
docreatelink [do1.c:195]
  specset2sporglset / vspanset2sporglset [sporgl.c:35]
    vspanset2ispanset → permute(V→I) [orglinks.c:397,401]
    → stores: sporglorigin (I), sporglwidth (I), sporgladdress (doc ISA)
  insertpm [orglinks.c:75]
    → POOM crum gets: cdsp.dsas[I] = sporglorigin, cdsp.dsas[V] = link V-slot

dofollowlink [do1.c:223]
  link2sporglset [sporgl.c:67]
    retrieverestricted(link orgl, V → I) [sporgl.c:83]
    contextintosporgl: sporglorigin ← context.dsas[I]  ← ORIGINAL I-SPAN
  linksporglset2specset [sporgl.c:97]
    sporglset2vspanset [sporgl.c:141]
      findorgl(homedoc=sporgladdress)  ← original document's orgl
      ispan2vspanset → permute(I→V) on original document's current structure
```

The I-spans are read back unchanged. The V-spans are computed fresh from the original document's current orgl state.
