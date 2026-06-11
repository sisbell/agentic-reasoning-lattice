## Question 1 [evidence]

> Does udanax-green's link-creation entry point (CREATELINK) accept endsets as arbitrary span sets carrying content extents, or only whole-entity references — i.e., is the caller-facing surface range-valued or effectively address-valued?

## KB Synthesis

The caller-facing surface of CREATELINK is **range-valued** — callers provide SpecSets composed of VSpecs, each carrying `(document, start_tumbler, width_tumbler)`. The width field is semantically meaningful and participates in precondition checking.

**Evidence from the KB:**

[PRE-ZERO-WIDTH] is the sharpest proof: zero-width endpoints crash the backend (Bug 0017), while width=1 succeeds. This only makes sense if the API genuinely accepts an extent — an address-valued interface would have no width parameter to be zero.

[SS-SPECSET] defines the carrier type: `VSpec = (doc: Tumbler, start: Tumbler, width: Tumbler)` and `SpecSet = seq<VSpec>`. This is the same type used for retrieve, vcopy, and compare_versions — a general span-set, not an entity handle.

[SS-LINK-ENDPOINT] Finding 0028 confirms the internal state structure that results: "A link records its source and target as specific V-spans in specific documents (e.g., source = Document A at V 1.4 for 0.3, target = Document B at V 1.1 for 0.6)."

[ST-LINK-CREATE] Finding 0037 shows what happens *after* the range is accepted: `vspanset2sporglset` decomposes the caller-supplied V-span into one I-span per contiguous I-address region. The caller does NOT pre-split; the backend handles it transparently. The input is a single contiguous V-extent; the stored endset may be multiple sporgls. This decomposition would be meaningless if the API accepted only whole-entity addresses.

[SS-LINK-ENDPOINT] Finding 0024 shows the type endpoint is also a VSpec referencing an extent in the bootstrap document — e.g., QUOTE_TYPE at `1.0.2.3`, MARGIN_TYPE at `1.0.2.6.2`. These are span references into the type registry, not bare addresses.

**Summary:** The CREATELINK surface is range-valued throughout: callers pass SpecSets of VSpecs (document, start, width) for from-, to-, and type-endpoints. Internally, these V-spans are converted to sporgls (I-spans with document provenance) for permanent storage and spanfilade indexing, but the decomposition from V-ranges to I-spans is the system's responsibility, not the caller's. The API is `create_link(home_doc, from_specset, to_specset, type_specset)` where each specset can cover an arbitrary content region.

---

## Code Exploration

I now have the complete picture. Here is the full answer.

---

## CREATELINK: Range-Valued Endsets, Not Address-Valued

### Answer

**CREATELINK accepts genuine range-valued endsets.** Each endset is an arbitrary span set carrying content extents (origin + width), not whole-entity references. This is true at every layer of the stack, from the wire protocol through conversion and storage.

---

### Evidence, Layer by Layer

#### 1. Wire Protocol: `getcreatelink` / `getspecset` / `getspan`

`fns.c:107` dispatches to `getcreatelink`. The deserialization in `get1.c:46–61`:

```c
bool getcreatelink(... typespecset *fromspecsetptr, *tospecsetptr, *threespecsetptr)
{
    prompt(taskptr, "fromset\n");
    if (!getspecset(taskptr, fromspecsetptr)) return FALSE;
    ...
}
```

`getspecset` (`get2.c:162–192`) iterates, offering either a raw `ISPANID` span or a `VSPECID` vspec per element. For a vspec, it calls `getvspec` (`get2.c:194–203`), which reads a `docisa` address and then calls `getspanset` to read the vspanset. `getspanset` calls `getspan` (`get2.c:228–238`):

```c
bool getspan(typetask *taskptr, typespan *spanptr, char id)
{
    prompt(taskptr, "enter span\n       start=> ");
    if (!getisa(taskptr, &spanptr->stream)) return FALSE;
    spanptr->itemid = id;
    prompt(taskptr, "       width=> ");
    if (!(getisa(taskptr, &spanptr->width))) return FALSE;
    return TRUE;
}
```

The wire reads both `stream` (origin) **and** `width` (extent). This is a range, not an address. Multiple spans form a linked list (`vspanset`), so the caller can supply an arbitrary multi-segment region.

---

#### 2. Type System: `typevspec` and `typevspan`

From `xanadu.h`:

```c
typedef struct structtypevspec {
    struct structtypevspec *next;
    typeitemid itemid;
    typeisa    docisa;      // which document
    typevspanset vspanset;  // set of v-spans (origin + width)
} typevspec;

typedef typespan typevspan;   // stream + width
typedef typevspan * typevspanset;
```

Each `typevspan` is a `typespan`, which has `stream` (starting V-address) and `width` (V-extent). The entire `vspanset` is a linked list of such spans — a fully arbitrary multi-span range within a named document.

---

#### 3. Conversion: `docreatelink` → `specset2sporglset` → `vspanset2sporglset`

`do1.c:195–221` is the core `docreatelink`:

```c
bool docreatelink(... typespecset fromspecset, tospecset, threespecset, ...)
{
    ...
    && specset2sporglset(taskptr, fromspecset, &fromsporglset, NOBERTREQUIRED)
    && specset2sporglset(taskptr, tospecset,   &tosporglset,   NOBERTREQUIRED)
    && specset2sporglset(taskptr, threespecset,&threesporglset,NOBERTREQUIRED)
    && insertendsetsinorgl(taskptr, linkisaptr, link,
                           &fromvsa, fromsporglset,
                           &tovsa,   tosporglset,
                           &threevsa,threesporglset)
    && insertendsetsinspanf(taskptr, spanf, linkisaptr,
                            fromsporglset, tosporglset, threesporglset)
```

`specset2sporglset` (`sporgl.c:14–33`) dispatches on item type:

```c
} else if (((typeitemheader *)specset)->itemid == VSPECID) {
    if (!(sporglsetptr = vspanset2sporglset(taskptr,
            &((typevspec *)specset)->docisa,
            ((typevspec *)specset)->vspanset,
            sporglsetptr, type))) {
        return FALSE;
    }
}
```

`vspanset2sporglset` (`sporgl.c:35–65`) iterates over every vspan in the vspanset and converts each one through the enfilade:

```c
for (; vspanset; vspanset = vspanset->next) {
    (void) vspanset2ispanset(taskptr, orgl, vspanset, &ispanset);
    for (; ispanset; ispanset = ispanset->next) {
        sporglset = (typesporgl *) taskalloc(...);
        sporglset->itemid = SPORGLID;
        movetumbler(docisa,            &sporglset->sporgladdress); // doc
        movetumbler(&ispanset->stream, &sporglset->sporglorigin);  // start
        movetumbler(&ispanset->width,  &sporglset->sporglwidth);   // EXTENT
```

Both `sporglorigin` and `sporglwidth` are populated — the extent is faithfully preserved. `vspanset2ispanset` (`orglinks.c:397–402`) itself delegates to `permute`, which calls `retrieverestricted` to convert V-space ranges to I-space ranges through the enfilade — the width/extent is what defines the extent of the I-span returned.

---

#### 4. Storage: `typesporgl`

The stored representation (`xanadu.h:115–121`):

```c
typedef struct structsporgl {
    struct structsporgl *next;
    typeitemid itemid;
    tumbler sporglorigin;   // I-space start of the endset content
    tumbler sporglwidth;    // I-space width of the endset content
    typeisa sporgladdress;  // home document ISA
} typesporgl;
```

All three fields are non-degenerate: `sporgladdress` is the document, `sporglorigin` is the start, `sporglwidth` is the extent. This is not a pointer to an entity — it is a range record. The `unpacksporgl` function (`sporgl.c:178–203`) explicitly reads all three fields; a zero width triggers a `qerror`, confirming that zero-width (address-only) sporgls are malformed.

---

### Summary

| Layer | Mechanism | Range or Address? |
|---|---|---|
| Wire format | `getspan` reads `stream` + `width` | Range |
| Caller type | `typevspec` holds `docisa` + `vspanset` (linked spans) | Range |
| Conversion | `vspanset2sporglset` maps each vspan to I-span, preserving width | Range |
| Storage type | `typesporgl` stores `sporglorigin` + `sporglwidth` + `sporgladdress` | Range |
| Validation | Zero width in `unpacksporgl` is a hard error | Range enforced |

**CREATELINK's caller-facing surface is range-valued throughout.** Endsets are arbitrary span sets — each element specifying a document ISA plus one or more (origin, width) pairs in V-space. The system converts V-space ranges to I-space ranges via the enfilade and stores them as `sporgl` records retaining full extent information. There is no reduction to whole-entity (address-only) references anywhere in the path.
