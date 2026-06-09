## Question 12 [evidence]

> Does CREATELINK store all three endsets (source, target, type) as I-address spans in the link orgl, converting endset V-spans to I-spans at creation time so the recorded endpoints reference content by identity rather than V-position?

## KB Synthesis

Yes. CREATELINK converts all three endsets (FROM, TO, THREE) from input V-spans to I-address spans (sporgls) at creation time, and the link orgl stores those sporgls — not the original V-positions.

**The conversion chain:**

The function `domakelink` [ST-LINK-CREATE Finding 0037] calls `vspanset2sporglset` on each input V-span. This function calls `vspanset2ispanset` → `permute` → `span2spanset`, which walks the POOM of the source document to find all contiguous I-address regions covered by the V-span. For each contiguous region it produces one sporgl: `(origin: IAddress, width: Tumbler, doc: ISA)` [SS-SPORGL].

A single user-supplied V-span can yield multiple sporgls when the span covers content from multiple sources — e.g., a V-span in document C covering text transcluded from both A ("AA") and B ("BB") produces two sporgls, one anchored at A's I-addresses and one at B's [SS-LINK-ENDPOINT Finding 0037]. The formal postcondition: `link.source_endset = { sporgl(origin=i.start, width=i.width, doc=source_doc) | i ∈ V_to_ISpans(source_doc, source_vspan) }`.

These sporgls are then written to two places [ST-CREATE-LINK Finding 0012]:
1. **The link orgl in granf** — indexed by the link's ISA, retrievable via FOLLOWLINK
2. **The spanfilade** — via `insertendsetsinspanf`, indexed by I-address range for content-identity-based discovery [INT-SPORGL-LINK-INDEX Finding 0013]

**Retrieval confirms I-address storage:**

FOLLOWLINK [SS-FOLLOWLINK Finding 0048] reads I-addresses from the link orgl via `link2sporglset`, then converts them to V-addresses using the *querying* document's current POOM via `linksporglset2specset`. If the I-addresses have no current POOM mapping in the queried document, the result is empty — there is no fallback to stored V-positions. This proves the stored representation is I-address based, not V-position based.

**Why Finding 0028's "fixed V-span" framing is the external contract, not the internal representation:**

Finding 0028 says "link endpoints are immutable V-spans fixed at creation time" and that `follow_link` "always returns the original VSpan referencing A at 1.4 for 0.3." This describes what FOLLOWLINK *produces* (V-spans reconstituted from the sporgls via the queried document's POOM), not what is *stored*. The immutability is of the I-addresses, not the V-positions — which is exactly why endsets shift when content is inserted before a linked region [INV-LINK-CONTENT-TRACKING Finding 0019].

**All three endsets, not just two:**

`setlinkvsas` [SS-SUBSPACE-CONVENTION Finding 0038] places FROM at V-position 2.x, TO at a second 2.x slot, and THREE (the type endpoint) at 3.x, using mantissa digit 0 = 2 for link endsets and 3 for type. The type endpoint references the bootstrap document's type registry [SS-LINK-ENDPOINT Finding 0024], and is stored as a sporgl just like the FROM and TO endpoints.

---

## Code Exploration

I have the full picture. Here is the complete answer.

---

## Does CREATELINK Store Endsets as I-Address Spans?

**Yes.** CREATELINK converts all three endset V-spans to I-spans at creation time before storing them. The conversion is not direct — it goes through an intermediate *sporgl* structure that pairs the I-span with the source document's ISA — but the stored coordinates are I-addresses, not V-positions.

---

### The Full Code Path

#### 1. Entry: `fns.c:100–112` — `createlink`

```c
if (   getcreatelink (taskptr, &docisa, &fromspecset, &tospecset, &threespecset)
    && docreatelink (taskptr, &docisa, fromspecset, tospecset, threespecset, &linkisa)){
        putcreatelink (taskptr, &linkisa);
```

`createlink` passes all three specsets (carrying V-span descriptions of the endset content) straight to `docreatelink`.

---

#### 2. Core logic: `do1.c:195–221` — `docreatelink`

```c
bool docreatelink(... typespecset fromspecset, typespecset tospecset, typespecset threespecset ...)
{
  typesporglset fromsporglset, tosporglset, threesporglset;
  ...
  && specset2sporglset (taskptr, fromspecset,  &fromsporglset,  NOBERTREQUIRED)  // line 214
  && specset2sporglset (taskptr, tospecset,    &tosporglset,    NOBERTREQUIRED)  // line 215
  && specset2sporglset (taskptr, threespecset, &threesporglset, NOBERTREQUIRED)  // line 216
  && setlinkvsas (&fromvsa, &tovsa, &threevsa)                                   // line 217
  && insertendsetsinorgl (taskptr, linkisaptr, link,
        &fromvsa, fromsporglset, &tovsa, tosporglset, &threevsa, threesporglset) // line 218
  && insertendsetsinspanf (taskptr, spanf, linkisaptr,
        fromsporglset, tosporglset, threesporglset)                              // line 219
```

`specset2sporglset` is the key call. The output type is `typesporglset`, not `typevspanset` or `typeispanset`.

---

#### 3. V→I conversion: `sporgl.c:14–65` — `specset2sporglset` → `vspanset2sporglset`

```c
bool specset2sporglset(... typespecset specset, typesporglset *sporglsetptr ...)
{
    for (; specset; ...) {
        if (itemid == ISPANID) {           // already an I-span: pass through
            *sporglsetptr = (typesporglset)specset;
        } else if (itemid == VSPECID) {    // V-spec: must convert
            sporglsetptr = vspanset2sporglset (taskptr,
                &((typevspec*)specset)->docisa,
                ((typevspec*)specset)->vspanset,
                sporglsetptr, type);       // sporgl.c:25
        }
    }
}
```

When the endset is a V-spec (the common case from a FEBE client), `vspanset2sporglset` is called:

```c
typesporglset *vspanset2sporglset(... typeisa *docisa, typevspanset vspanset ...)
{
    ispanset = NULL;
    findorgl (taskptr, granf, docisa, &orgl, type);   // sporgl.c:44: get the content enfilade
    for (; vspanset; vspanset = vspanset->next) {
        vspanset2ispanset (taskptr, orgl, vspanset, &ispanset);  // sporgl.c:48: V→I via permute
        for (; ispanset; ispanset = ispanset->next) {
            sporglset = taskalloc(taskptr, sizeof(typesporgl));
            sporglset->itemid         = SPORGLID;
            movetumbler (docisa,                &sporglset->sporgladdress);  // line 53: doc ISA
            movetumbler (&ispanset->stream,     &sporglset->sporglorigin);   // line 54: I-origin
            movetumbler (&ispanset->width,      &sporglset->sporglwidth);    // line 55: I-width
        }
    }
}
```

The conversion call at `sporgl.c:48` is `vspanset2ispanset`, defined in `orglinks.c:397–402`:

```c
typeispanset *vspanset2ispanset(... typeorgl orgl, typevspanset vspanptr ...)
{
    return permute(taskptr, orgl, vspanptr, V, ispansetptr, I);  // orglinks.c:401
}
```

`permute` walks the orgl enfilade to map each V-span to its corresponding I-address range(s). After this call, `ispanset` contains I-spans (permanent permascroll addresses).

Each resulting I-span is packaged into a `typesporgl` with three fields:
- `sporgladdress` — the document ISA (which content enfilade to consult for the reverse mapping)
- `sporglorigin` — I-span start address
- `sporglwidth` — I-span width

**A sporgl is an I-address span tagged with the document it was resolved through.** It carries the I-coordinates for content identity, not V-positions.

---

#### 4. Storage in the link orgl: `do2.c:130–149` — `insertendsetsinorgl`

```c
bool insertendsetsinorgl(... typeorgl link,
        tumbler *fromvsa, typesporglset fromsporglset,
        tumbler *tovsa,   typesporglset tosporglset,
        tumbler *threevsa, typesporglset threesporglset)
{
    insertpm(taskptr, linkisaptr, link, fromvsa, fromsporglset)  // line 132
    insertpm(taskptr, linkisaptr, link, tovsa,   tosporglset)    // line 133
    insertpm(taskptr, linkisaptr, link, threevsa, threesporglset) // line 137
}
```

`insertpm` (`orglinks.c:75–134`) inserts each sporgl as a 2D POOM crum in the link's own orgl:
- **I-coordinate** (`dsas[I]`): `sporglorigin`/`sporglwidth` — the content's I-address [orglinks.c:105–109]
- **V-coordinate** (`dsas[V]`): `fromvsa`/`tovsa`/`threevsa` — the link's V-position [orglinks.c:113]

The V-position here is the *link's* internal V-address (assigned by `setlinkvsas`/`findnextlinkvsa`), not the V-span of the referenced content. The referenced content is recorded purely by I-address.

---

#### 5. Storage in the spanfilade: `do2.c:116–128` — `insertendsetsinspanf`

```c
bool insertendsetsinspanf(... typesporglset fromsporglset, tosporglset, threesporglset)
{
    insertspanf(taskptr, spanfptr, linkisaptr, fromsporglset, LINKFROMSPAN)   // line 119
    insertspanf(taskptr, spanfptr, linkisaptr, tosporglset,  LINKTOSPAN)      // line 120
    insertspanf(taskptr, spanfptr, linkisaptr, threesporglset, LINKTHREESPAN) // line 123
}
```

`insertspanf` (`spanf1.c:15–54`) inserts each sporgl into the global spanfilade indexed by I-span range + link-type prefix, enabling FIND operations to look up links by content I-address. The ORGL-range coordinate encodes the link's ISA; the SPAN-range coordinate is the sporgl's I-origin/I-width.

---

### Summary

| Stage | Code | Data type |
|---|---|---|
| Input from FEBE client | `fns.c:107` | V-spec (docisa + V-spans) |
| After `specset2sporglset` | `sporgl.c:25, 48` | sporgl = (docisa, I-origin, I-width) |
| Stored in link orgl | `do2.c:132–138` | 2D POOM crum: I-coord = I-span, V-coord = link's V-pos |
| Stored in spanfilade | `do2.c:119–124` | I-span indexed by link type prefix |
| Return via FOLLOWLINK | `do1.c:223–232` → `sporgl.c:97–123` | sporgl → V-span (I→V via `ispan2vspanset`) |

**The V→I conversion happens unconditionally inside `vspanset2sporglset` (`sporgl.c:48`) for every V-spec endset.** The original V-positions are discarded; what is stored in both the link orgl and the spanfilade are I-addresses (in sporgl form). When a client later calls FOLLOWLINK, the reverse mapping `ispan2vspanset` (`orglinks.c:389–394`) reconstructs V-spans on demand from the stored I-spans.

This means that CREATELINK records endpoints by their **immutable content identity** (I-address), not by their **mutable V-position** at creation time. A link endpoint will follow the content even if it is rearranged to a different V-position in subsequent document versions.
