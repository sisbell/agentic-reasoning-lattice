## Question 1 [evidence]

> How does udanax-green represent link types and type designators — are type addresses element-level tumblers, content addresses, or some other convention, and what stability guarantees does the implementation provide for them?

## KB Synthesis

## Link Type Representation in udanax-green

Link types are **content references into a type registry in the bootstrap document**, not enums or flags. They participate fully in the standard address/identity system.

### Type Address Structure

Type designators are VSpec references into the bootstrap document (doc 1) at subspace `1.0.2.x`:

| Type     | Registry Address | Tumbler Structure |
|----------|-----------------|-------------------|
| JUMP     | `1.0.2.2`       | `version.0.types.2` |
| QUOTE    | `1.0.2.3`       | `version.0.types.3` |
| FOOTNOTE | `1.0.2.6`       | `version.0.types.6` |
| MARGIN   | `1.0.2.6.2`     | `version.0.types.6.subtype.2` |

These are element-level tumblers following the docuverse `.0.` field-separator convention — they are standard content addresses, not a special type namespace [SS-LINK-ENDPOINT Finding 0024].

### V-Space Storage

Within a link's home document POOM, the type endpoint occupies the **third subspace** (`3.x`). `setlinkvsas()` hardcodes three subspace assignments: `1` = text, `2` = link orgls, `3` = type endpoints [SS-DUAL-ENFILADE Finding 0038, SS-SUBSPACE-CONVENTION Finding 0038].

The spanfilade indexes type endpoints as `LINKTHREESPAN=3`, separate from `LINKFROMSPAN=1` and `LINKTOSPAN=2` [INT-SPORGL-LINK-INDEX].

### Hierarchy via Tumbler Containment

The type hierarchy is encoded structurally: `1.0.2.6.2` (MARGIN) is a child of `1.0.2.6` (FOOTNOTE) in tumbler containment order. This enables type range queries via address-range matching — "find all footnote-family links" translates to an address-containment predicate [SS-LINK-ENDPOINT Finding 0024].

### Stability Guarantees

The bootstrap document is permanent under the `INV-LINK-PERMANENCE` model, so type addresses are stable in principle. However, there is a documented anomaly: when both source and target endpoints of a link are fully deleted, `follow_link(link_id, LINK_TYPE)` returns empty even though the bootstrap document was untouched [EC-ORPHANED-LINK Finding 0024]. This suggests type resolution has an undocumented dependency on endpoint resolution — the implementation does not provide independent stability for the type endset when other endsets are orphaned. Whether this is a bug or deliberate is unresolved in the KB.

---

## Code Exploration

I now have a complete picture from the code. Let me compile the full answer.

---

## How udanax-green Represents Link Types and Type Designators

### 1. The Three-Endset Is the Type — No Separate Type Code

Udanax-green has no integer type tag, type registry, or type enum for links. The **type of a link is the content pointed to by its third endset**, called the "three" endset.

`createlink` in `fns.c:100-112` dispatches to `getcreatelink` (`get1.c:46-61`), which accepts four protocol arguments: a home document ISA, then three specsets:

```c
bool getcreatelink(typetask *taskptr, typeisa *docisaptr, typespecset *fromspecsetptr,
                   typespecset *tospecsetptr, typespecset *threespecsetptr)
```

There is no "type" parameter beyond `threespecset`. The type is whatever content the third specset addresses. Two links share a type if and only if their three endsets resolve to the same I-space (permascroll) content.

---

### 2. Type Address Form: A Content Specset, Not an Element-Level Tumbler

Type addresses are NOT element-level tumblers in the sense of addressing a position within a virtual document. They are `typespecset` values — a polymorphic union defined in `xanadu.h:85-89`:

```c
typedef union {
    typevspec xxxvspec;    // VSPECID: document ISA + virtual span(s)
    typeispan xxxispan;    // ISPANID: I-space (permascroll) span
} typespec;
typedef typespec * typespecset;
```

A `typevspec` (`xanadu.h:78-84`) is:
```c
typedef struct structtypevspec {
    struct structtypevspec *next;
    typeitemid itemid;          // VSPECID
    typeisa docisa;             // document ISA (tumbler)
    typevspanset vspanset;      // virtual span address within that document
} typevspec;
```

So the type is specified as content in V-space (document + vspan) or as a direct I-space address. The implementation makes no distinction: `docreatelink` at `do1.c:195-221` passes all three specsets through the same conversion pipeline (`specset2sporglset`) without any special-casing of the three endset.

---

### 3. Internal Storage: Fixed V-Addresses in the Link's Own POOM

Each link object has its own POOM (granfilade node, created by `createorglingranf` with atom type `LINKATOM` — `do1.c:207`). Within that link's private V-address space, the three endsets are stored at **fixed V-positions** assigned by `setlinkvsas` at `do2.c:169-182`:

```c
bool setlinkvsas(tumbler *fromvsaptr, tumbler *tovsaptr, tumbler *threevsaptr)
{
    tumblerclear (fromvsaptr);
    tumblerincrement (fromvsaptr, 0, 1, fromvsaptr);   // mantissa[0] = 1
    tumblerincrement (fromvsaptr, 1, 1, fromvsaptr);   // mantissa[1] = 1  → V = 1.1

    tumblerclear (tovsaptr);
    tumblerincrement (tovsaptr, 0, 2, tovsaptr);       // mantissa[0] = 2
    tumblerincrement (tovsaptr, 1, 1, tovsaptr);       // mantissa[1] = 1  → V = 2.1

    if (threevsaptr) {
        tumblerclear (threevsaptr);
        tumblerincrement (threevsaptr, 0, 3, threevsaptr);  // mantissa[0] = 3
        tumblerincrement (threevsaptr, 1, 1, threevsaptr);  // mantissa[1] = 1  → V = 3.1
    }
```

Within the link's POOM:
- V = 1.1 → from endset  
- V = 2.1 → to endset  
- **V = 3.1 → type (three) endset**

Finding 0038 confirms this interpretation: "mantissa[0] = 3 → type subspace" (the same subspace structure applies inside a link object as it does in a document object).

When following the type endset, `link2sporglset` at `sporgl.c:81-83` retrieves the I-content stored in the link's POOM for V-range [3, 4):

```c
tumblerincrement (&zero, 0, whichend, &vspan.stream);  // stream = 3
tumblerincrement (&zero, 0, 1, &vspan.width);          // width = 1
if (context = retrieverestricted((typecuc*)orgl, &vspan, V, (typespan*)NULL, I, (typeisa*)NULL)) {
```

V=3.1 falls in [3, 4), so this correctly retrieves the type content.

---

### 4. Spanfilade Indexing: `3.linkisa`

The spanfilade (the "spanf" used for link discovery across the system) indexes each link's endsets using `prefixtumbler(linkisa, spantype)` at `spanf1.c:22`:

```c
prefixtumbler (isaptr, spantype, &crumorigin.dsas[ORGLRANGE]);
```

The span type constants from `xanadu.h:36-39`:

```c
#define LINKFROMSPAN    1
#define LINKTOSPAN      2
#define LINKTHREESPAN   3
#define DOCISPAN        4
```

The ORGL-dimension key in the spanfilade for the type endset is therefore `3.linkisa` (the link's ISA with the integer 3 prepended as the outermost tumbler digit). When `findlinksfromtothreesp` at `spanf1.c:92-98` queries by type, it calls:

```c
sporglset2linkset (taskptr, (typecuc*)spanfptr, threesporglset, &threelinkset, orglrange, LINKTHREESPAN);
```

passing `LINKTHREESPAN = 3` — the search is constrained to the type subspace of the spanfilade. The SPAN dimension of the search is the I-address of the type designator's content. This means type-based link discovery operates on content identity, not document position.

---

### 5. Following vs. Searching by Type

`getfollowlink` at `get1.c:63-74` accepts `whichend ∈ {1, 2, 3}`:

```c
getnumber (taskptr, whichendptr)
&& (*whichendptr == 1 || *whichendptr == 2 || *whichendptr == 3)
```

Endpoint 3 returns the type designator as a specset via `dofollowlink` → `link2sporglset` → `linksporglset2specset` (all in `sporgl.c`).

`findlinksfromtothree` (FEBE opcode 30) accepts an optional `threespecset` to search **by** type. Internally this computes the I-address of the type content and queries the spanfilade at `LINKTHREESPAN` — enabling "find all links of this type." This is structurally symmetric with searching by from or to endpoint.

---

### 6. Stability Guarantees

**Link ISA — permanently stable.** The link's identity address (ISA) is a tumbler assigned once by `createorglingranf` at `do1.c:209`. It is global, unique, and never changes. The type endset is always retrievable from V=3.1 in the link's POOM keyed by that ISA.

**Type endset content — depends on the specset form:**

| Specset form | Stability |
|---|---|
| **ISPANID** (I-space span) | Permanent. Permascroll addresses are immutable. The content at that I-address never changes. |
| **VSPECID** (document ISA + vspan) | Volatile. The V→I mapping is resolved at query time through the target document's current POOM. If that document is edited, the content at that V-position changes, and the type designator drifts. |

**The implementation enforces neither.** `getcreatelink` (`get1.c:46-61`) accepts any valid specset as the type. There is no check in `docreatelink` (`do1.c:195-221`) that the three endset is stable or refers to immutable content.

**Spanfilade key stability:** The spanfilade key is the I-address of the type content at insertion time (computed via `specset2sporglset` → `vspanset2sporglset` → `vspanset2ispanset`, i.e., V→I lookup through the current POOM). This I-address is immutable once written into the spanfilade. So:

- If the type content is later edited (V-address shifts), the spanfilade key becomes stale relative to the new V-position.
- The link's TYPE ENDSET (as returned by followlink) is re-resolved at query time, so it tracks the current V-position. But the spanfilade index (for find-by-type) uses the I-address frozen at link creation.

In practice, if the type designator was created by inserting text (which gets a permanent permascroll I-address via `inserttextingranf`), then transclusion semantics ensure the underlying content identity is stable regardless of V-position changes. The spanfilade type search will continue to work through edits to the type document, AS LONG AS the type content itself (the permascroll bytes) hasn't been deleted from every copy.

**Summary:** The type designator in udanax-green is a content address (specset pointing to bytes or a document region), NOT an element-level tumbler or integer code. It is stored at a fixed V-position (3.1) within the link's private POOM. The spanfilade indexes it as `3.linkisa`. The implementation guarantees ISA permanence but provides no enforcement of type-content stability — that is left entirely to convention, consistent with the design philosophy documented in Finding 0011 ("Convention Over Enforcement").
