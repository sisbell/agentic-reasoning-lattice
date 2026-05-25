## Question 1 [evidence]

> Does udanax-green permit endsets with coverage in both content and link subspaces, and if so what representation does the follow-equivalent operation return?

## KB Synthesis

## Cross-Subspace Endsets in udanax-green

### Is it permitted?

Yes — the backend has no enforcement preventing a link endpoint V-span from covering both the text subspace (1.x) and the link subspace (2.x). The critical evidence:

- `acceptablevsa()` unconditionally returns `TRUE` [SS-SUBSPACE-CONVENTION Finding 0010, PRE-INSERT Finding 0049]
- `vspanset2ispanset` → `permute` → `retrieverestricted` is fully type-agnostic; it walks the POOM and returns whatever I-addresses are mapped, regardless of type [SS-DUAL-ENFILADE Finding 0011]
- `domakelink` / `vspanset2sporglset` applies no subspace filter before constructing the endset [ST-LINK-CREATE Finding 0037]

### What gets stored in the endset?

`vspanset2sporglset` walks the POOM for the given V-span and creates **one sporgl per contiguous I-address region** [ST-LINK-CREATE Finding 0037]. For a V-span straddling 1.x and 2.x:

- The 1.x positions produce sporgls with **permascroll I-addresses** (e.g., `2.1.0.5.0.123`)
- The 2.x positions produce sporgls with **link orgl ISAs** (e.g., `1.1.0.1.0.1.0.2.1`)

These are in completely different I-address domains and are non-comparable [SS-CONTENT-IDENTITY Finding 0009, PRE-COMPARE-VERSIONS Finding 0015]. The endset holds both as independent sporgl entries.

### What does the follow-equivalent operation return?

`FOLLOWLINK` calls `link2sporglset()` → `linksporglset2specset()` → `span2spanset()` → `retrieverestricted()`, which looks up each sporgl's I-address in the **home document's POOM** to recover V-positions [SS-FOLLOWLINK Finding 0048]. The conversion is type-agnostic:

- The permascroll I-addresses resolve to **1.x V-positions** where that text content currently lives
- The link orgl ISAs resolve to **2.x V-positions** where those link orgls are stored in the document

The result is a V-span set covering both subspaces. Normalized output representation follows [SS-DUAL-ENFILADE Finding 0038]: when both text and links are present, links appear at `"0"` (normalized from 2.x) and text at `"1"`.

### Downstream complications

1. **Spanfilade indexing**: The link orgl ISA sporgls get indexed in the spanfilade under the link orgl's I-address [INT-SPORGL-LINK-INDEX]. This means `find_links` searches on documents containing those same link orgl ISAs (at their 2.x V-positions) would potentially surface this endpoint — a confusing cross-reference since link ISAs are unique per-document [SS-ADDRESS-SPACE Finding 0065].

2. **Subspace invariant violation**: This constitutes a violation of [INV-SUBSPACE-CONVENTION] — link orgl ISAs embedded in a content-bearing endset are not permascroll content origins and have no "common origin" semantics [PRE-COMPARE-VERSIONS Finding 0015].

3. **`compare_versions` unsafety**: Any downstream use of these endset I-addresses in `correspond.c`-style comparison would produce crashes, since link ISAs and permascroll addresses are non-intersecting address sorts [EC-COMPARE-VERSIONS-LINK-CRASH].

### Summary

The backend **permits** cross-subspace endsets by convention-over-enforcement. The endset stores separate sporgls for each I-address domain. `FOLLOWLINK` returns a V-span set covering both 1.x (text content) and 2.x (link orgl references) positions in the home document. This is semantically unsound — the subspace discipline [INV-SUBSPACE-CONVENTION, FC-SUBSPACE] exists precisely to keep these domains separate, but no runtime guard enforces it at link creation time.

---

## Code Exploration

I now have all the source evidence needed. Here is the complete analysis.

---

## Does udanax-green permit endsets spanning both content and link subspaces?

**Short answer: Yes — unconditionally. No validation filters V-spans by subspace at link creation or follow time. The follow operation returns a heterogeneous `typespecset` that can contain vspans in both ranges.**

---

### 1. Type structure

`xanadu.h:65-89` defines the relevant types:

```c
typedef struct structtypespan {      // typespan / typevspan / typeispan
    struct structtypespan *next;
    typeitemid itemid;
    tumbler stream;
    tumbler width;
} typespan;

typedef struct structtypevspec {     // typespec item for a document reference
    struct structtypevspec *next;
    typeitemid itemid;
    typeisa docisa;                  // which document
    typevspanset vspanset;           // V-span list within that document
} typevspec;

typedef union {
    typevspec xxxvspec;
    typeispan xxxispan;
} typespec;
typedef typespec * typespecset;
```

A `typespecset` is a linked list of items, each tagged with either `VSPECID` (document + V-spans) or `ISPANID` (raw I-span). **A single specset can freely mix both.** [xanadu.h:28-29, xanadu.h:85-89]

Span-type constants that tag endsets within the spanfilade [xanadu.h:36-39]:

```c
#define LINKFROMSPAN    1
#define LINKTOSPAN      2
#define LINKTHREESPAN   3
#define DOCISPAN        4
```

---

### 2. Link creation imposes no subspace restriction

`docreatelink` [do1.c:195-221] is the entry point:

```c
bool docreatelink(typetask *taskptr, typeisa *docisaptr,
                  typespecset fromspecset, typespecset tospecset, typespecset threespecset,
                  typeisa *linkisaptr)
{
    ...
    && specset2sporglset(taskptr, fromspecset, &fromsporglset, NOBERTREQUIRED)
    && specset2sporglset(taskptr, tospecset, &tosporglset, NOBERTREQUIRED)
    && specset2sporglset(taskptr, threespecset, &threesporglset, NOBERTREQUIRED)
    && setlinkvsas(&fromvsa, &tovsa, &threevsa)
    && insertendsetsinorgl(taskptr, linkisaptr, link, &fromvsa, fromsporglset,
                           &tovsa, tosporglset, &threevsa, threesporglset)
    && insertendsetsinspanf(taskptr, spanf, linkisaptr, fromsporglset, tosporglset, threesporglset)
}
```

`specset2sporglset` [sporgl.c:14-33] iterates every item in the specset and converts without any V-address filter:

```c
for (; specset; specset = ...) {
    if (itemid == ISPANID) {
        *sporglsetptr = (typesporglset)specset;   // pass I-span through directly
    } else if (itemid == VSPECID) {
        sporglsetptr = vspanset2sporglset(taskptr,
            &((typevspec *)specset)->docisa,
            ((typevspec *)specset)->vspanset,   // ALL vspans, no subspace check
            sporglsetptr, type);
    }
}
```

`vspanset2sporglset` [sporgl.c:35-65] iterates every vspan — including any in the link subspace — calling `vspanset2ispanset` → `permute` to translate each to I-space, then wraps the result in a `typesporgl`:

```c
for (; vspanset; vspanset = vspanset->next) {
    vspanset2ispanset(taskptr, orgl, vspanset, &ispanset);
    // build sporgl from each returned ispanset...
    movetumbler(docisa, &sporglset->sporgladdress);
    movetumbler(&ispanset->stream, &sporglset->sporglorigin);
    movetumbler(&ispanset->width, &sporglset->sporglwidth);
}
```

No guard. A vspan at V=0.3 (link subspace) is handled identically to one at V=1.3 (content subspace).

The endsets are stored in two places:

- **In the link's own orgl** (permutation matrix) at internal V-addresses set by `setlinkvsas` [do2.c:169-182]: fromvsa=1.1, tovsa=2.1, threevsa=3.1.
- **In the global spanfilade** via `insertendsetsinspanf` [do2.c:116-128], which calls `insertspanf` for each of from (`LINKFROMSPAN=1`), to (`LINKTOSPAN=2`), and optionally three (`LINKTHREESPAN=3`) [spanf1.c:15-54].

---

### 3. The follow operation: `dofollowlink`

`followlink` [fns.c:114-127] → `dofollowlink` [do1.c:223-232]:

```c
bool dofollowlink(typetask *taskptr, typeisa *linkisaptr, typespecset *specsetptr, INT whichend)
{
    typesporglset sporglset;
    return (
       link2sporglset(taskptr, linkisaptr, &sporglset, whichend, NOBERTREQUIRED)
    && linksporglset2specset(taskptr, &((typesporgl *)sporglset)->sporgladdress,
                             sporglset, specsetptr, NOBERTREQUIRED)
    );
}
```

**Step A — `link2sporglset`** [sporgl.c:67-95]:

```c
tumblerincrement(&zero, 0, whichend, &vspan.stream);  // V = whichend (1, 2, or 3)
tumblerincrement(&zero, 0, 1, &vspan.width);           // width = 1
context = retrieverestricted((typecuc*)orgl, &vspan, V, (typespan*)NULL, I, (typeisa*)NULL);
for (c = context; c; c = c->nextcontext) {
    sporglptr = taskalloc(sizeof(typesporgl));
    contextintosporgl((type2dcontext*)c, (tumbler*)NULL, sporglptr, I);
    ...
}
```

This queries the link's orgl at V=whichend, retrieving **all I-space sporgl entries** associated with that endset position. These I-spans were deposited there at link creation time regardless of which V-subspace the original specset pointed to.

**Step B — `linksporglset2specset`** [sporgl.c:97-123]:

```c
for (; sporglset; sporglset = ...) {
    specset = taskalloc(sizeof(typevspec));
    if (iszerotumbler(&((typesporgl *)sporglset)->sporgladdress)) {
        // sporgladdress == 0: this sporgl is a raw I-span
        ((typeitemheader *)specset)->itemid = ISPANID;
        movetumbler(&sporglset->sporglorigin, &((typeispan *)specset)->stream);
        movetumbler(&sporglset->sporglwidth,  &((typeispan *)specset)->width);
    } else {
        // sporgladdress != 0: convert I-span → V-span via the document's orgl
        linksporglset2vspec(taskptr, homedoc, &sporglset, (typevspec*)specset, type);
    }
    *specsetptr = specset;
    specsetptr = (typespecset *)&((typeitemheader *)specset)->next;
}
```

`linksporglset2vspec` → `sporglset2vspanset` → `ispan2vspanset` → `permute` → `span2spanset` [orglinks.c:389-454]:

```c
typevspanset *ispan2vspanset(...) { return permute(taskptr, orgl, ispanptr, I, vspansetptr, V); }

typespanset *permute(...) {
    for (; restrictionspanset; restrictionspanset = restrictionspanset->next) {
        targspansetptr = span2spanset(taskptr, orgl, restrictionspanset, restrictionindex,
                                      targspansetptr, targindex);
    }
    return save;
}

typespanset *span2spanset(...) {
    context = retrieverestricted((typecuc*)orgl, restrictionspanptr, restrictionindex,
                                 (typespan*)NULL, targindex, (typeisa*)NULL);
    for (c = context; c; c = c->nextcontext) {
        context2span(c, restrictionspanptr, restrictionindex, &foundspan, targindex);
        nextptr = onitemlist(taskptr, (typeitem*)&foundspan, (typeitemset*)targspansetptr);
    }
    ...
}
```

The returned V-spans are **whatever the document's permutation matrix maps those I-spans to**. If the stored I-spans originally covered both a V=1.x content range and a V=2.x link-atom range (because the client built the endset that way), the result will contain vspans in both ranges.

---

### 4. Concrete representation of the follow return value

`dofollowlink` returns through `putfollowlink(taskptr, specset)` [fns.c:124]. The returned `typespecset` is a **linked list** whose items can be:

| `itemid` | Type | Contents | When |
|---|---|---|---|
| `VSPECID` (3) | `typevspec` | `docisa` + `vspanset` | sporgladdress non-zero; V-spans recovered via I→V permutation |
| `ISPANID` (1) | `typeispan` | `stream` + `width` | sporgladdress is zero (raw I-span endset) |

The `vspanset` within a `VSPECID` item is an unsorted, unfiltered list of `typevspan` entries. If the endset at creation time pointed to both content (V >= 1.0) and link-subspace (V < 1.0, or V in the 1.x link atom range) addresses, the recovered vspanset will contain spans from both ranges, interleaved according to the order `putvspaninlist` inserts them [orglinks.c:329-387].

---

### 5. The only filter is in `doshowrelationof2versions`

The code explicitly acknowledges mixed-subspace specsets are possible and problematic in `doshowrelationof2versions` [do1.c:428-449]:

```c
/* Bug 009 SEMANTIC FIX: Filter vspanset to text subspace only (V >= 1.0).
 * Link references at V-position 0.x are document metadata, not
 * transcludable content. */
filter_specset_to_text_subspace(taskptr, version1);
filter_specset_to_text_subspace(taskptr, version2);
```

This filter [do1.c:386-426] is applied **only** in `doshowrelationof2versions`. It is absent from `dofollowlink`, `retrieveendsetsfromspanf`, and the create-link path. Its existence confirms that mixed-subspace coverage is a real representational possibility in the system, not a prevented state.

---

### Summary

**udanax-green does permit endsets with coverage spanning both content and link V-subspaces.** `docreatelink` [do1.c:195-221] and `specset2sporglset` [sporgl.c:14-33] impose no restriction. The stored sporgl entries faithfully record the I-space addresses regardless of which V-subspace they originated from.

The follow operation (`dofollowlink` [do1.c:223-232]) returns a **`typespecset`** — a linked list of `VSPECID` or `ISPANID` tagged items. For `VSPECID` items, the `vspanset` is produced by I→V permutation through the document's orgl [orglinks.c:389-454] and will contain spans in whichever V-subspace ranges the stored I-spans map to, with no filtering. Mixed-subspace vspansets are fully representable in the return value and are only stripped in the separate `compare_versions` path [do1.c:437-441].
