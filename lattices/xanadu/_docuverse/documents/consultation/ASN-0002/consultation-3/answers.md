# Revision Consultation — ASN-0002

**Review:** review-3.md
**Date:** 2026-03-06 13:38

## Summary

5 REVISE items analyzed: 2 internal, 3 consulted (1 nelson, 3 gregory)

## Consultation Results

### Issue 1: CREATELINK's V-space effect is unspecified

**Category:** GREGORY
**Reason:** The ASN's state model defines V-space with a link subspace, but whether CREATELINK populates it is an implementation question — does the code insert an entry into the target document's link subspace mapping, or do links exist only in I-space?

**Gregory question:** When CREATELINK creates a link, does it insert a V-space entry in the target document's link subspace (analogous to how INSERT adds text V-positions), or does the link exist only as an I-space content entry with no V-space presence in any document?

**Gregory's Answer:**

## KB Synthesis

CREATELINK inserts a V-space entry in the **home document's** link subspace. It does not modify the V-space of the source or target endpoint documents.

## What CREATELINK writes

According to [ST-CREATE-LINK] (Finding 0012), link creation is a compound state transition across three structures:

1. **I-space**: Creates a new link orgl via `createorglingranf()` at a fresh ISA — the permanent link object
2. **Home document POOM**: Copies the link's ISA into the home document at the next available V-position in the `2.x` subspace via `docopy()` — this is the V-space entry
3. **Spanfilade**: Indexes all endpoint I-addresses via `insertendsetsinspanf()` — enables content-identity-based discovery

The V-space entry goes into the **home document** (first parameter of `create_link`), not into any source or target document [SS-LINK-HOME-DOCUMENT].

## Which V-subspace

From [SS-LINK-SUBSPACE] (Finding 0052), the first link is placed at V-position `2.1`, with subsequent links appended at `vspanreach`. Internally this is `2.x`; `retrieve_vspanset` normalizes this to `0.x` when the home document also contains text [SS-DUAL-ENFILADE] (Finding 0038).

## The three-layer model

[SS-THREE-LAYER-MODEL] (Finding 0040) makes the structure explicit:

| Layer | What's stored | Mutability |
|-------|--------------|------------|
| I-space | Link orgl at permanent I-address | Permanent |
| Spanfilade | Endpoint I-addresses → link ISA | Append-only |
| POOM (home doc) | V-position `2.x` → link orgl ISA | Mutable via DELETEVSPAN |

`CREATELINK` writes to all three layers. `DELETEVSPAN(2.x)` removes only the POOM entry while the link remains fully intact and discoverable in I-space and spanfilade [FC-LINK-DELETE-ISOLATION].

## What the source/target documents gain

The source and target endpoint documents gain **nothing in their own V-space**. Link discoverability from those documents is entirely I-address-based: `find_links` converts a query V-span to I-addresses and searches the spanfilade. Since the endpoint documents already contain those I-addresses (they are the source of the content), they can discover the link without any modification to their own POOMs [INT-LINK-TRANSCLUSION].

---

## Code Exploration

I have all the code I need. Let me now synthesize the complete answer.

---

## Answer: Where Does CREATELINK's V-Space Entry Live?

Neither option in the question is exactly correct. The link gets a V-space entry — but it is in the **home document's link subspace**, not in the target document's. The link does not exist as a pure I-space entity. Here is the full execution trace with citations.

---

### Entry Point: `fns.c:100-112`

```c
void createlink(typetask *taskptr)
{
  typeisa docisa, linkisa;
  typespecset fromspecset, tospecset, threespecset;
  ...
  getcreatelink (taskptr, &docisa, &fromspecset, &tospecset, &threespecset)
  && docreatelink (taskptr, &docisa, fromspecset, tospecset, threespecset, &linkisa)
```

`docisa` is the **home document** — the document that will own the link. Per `docs/client-api.md:315`:

> `docid`: The opened handle of the document that will "own" the link

---

### `docreatelink` — Full Trace (`do1.c:195-221`)

#### Step 1 — Allocate an I-space identity for the link

```c
makehint (DOCUMENT, ATOM, LINKATOM, docisaptr, &hint);   // do1.c:207
createorglingranf (taskptr, granf, &hint, linkisaptr)     // do1.c:209
```

`createorglingranf` allocates a new enfilade node ("orgl") in the global granfilade and returns its I-space address (ISA) in `linkisaptr`. The hint `(DOCUMENT, ATOM, LINKATOM)` marks this as a link-typed atom belonging to `docisaptr`. The link now exists as an I-space content object.

#### Step 2 — Represent the link's ISA as an I-space span

```c
tumbler2spanset (taskptr, linkisaptr, &ispanset)   // do1.c:210
```

`do2.c:48-61`: allocates an `ISPANID` span of width 1 at the link's ISA. This is the link's I-space "body" — a content range of length 1 in the global I-space.

#### Step 3 — Find the next open V-address in the home document's link subspace

```c
findnextlinkvsa (taskptr, docisaptr, &linkvsa)   // do1.c:211
```

`do2.c:151-167`:

```c
tumblerclear (&firstlink);
tumblerincrement (&firstlink, 0, 2, &firstlink);   // component[0] = 2
tumblerincrement (&firstlink, 1, 1, &firstlink);   // component[1] = 1

doretrievedocvspan (taskptr, docisaptr, &vspan);
tumbleradd (&vspan.stream, &vspan.width, &vspanreach);
if (tumblercmp (&vspanreach, &firstlink) == LESS)
    movetumbler (&firstlink, vsaptr);         // no links yet: use firstlink
else
    movetumbler (&vspanreach, vsaptr);        // append after existing content
```

`firstlink` is the first V-address in the link subspace of the **home document**. The function consults `docisaptr`'s current V-extent and returns the next free V-address at or beyond that subspace boundary.

The link subspace V-addresses are confirmed by `orglinks.c:255-261`:

```c
bool islinkcrum(typecorecrum *crumptr)
{
    if(crumptr->cdsp.dsas[V].mantissa[0] == 1 && crumptr->cdsp.dsas[V].mantissa[1] != 0){
        /* if the whole crum is displaced into link space it is a link crum
           this is true if the tumbler is a 1.n tumbler where n!= 0 */
        return TRUE;
    }
    return FALSE;
}
```

Text crums (`orglinks.c:246`) have `mantissa[1] == 0`; link crums have `mantissa[0] == 1 && mantissa[1] != 0`. They live in different V-subspaces within the same home document.

#### Step 4 — Insert a V-space entry in the home document — THIS IS THE KEY STEP

```c
docopy (taskptr, docisaptr, &linkvsa, ispanset)   // do1.c:212
```

`docopy` at `do1.c:45-65`:

```c
bool docopy(typetask *taskptr, typeisa *docisaptr, tumbler *vsaptr, typespecset specset)
{
    specset2ispanset (taskptr, specset, &ispanset, NOBERTREQUIRED)
    && findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
    && acceptablevsa (vsaptr, docorgl)
    && insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset)      // write V→I into home doc's POOM
    && insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN)   // index link's I-address → home doc
}
```

`insertpm` (`orglinks.c:75-134`) inserts a POOM entry mapping V-position `linkvsa` → the link's I-space span (`ispanset`) **into the home document's enfilade**. This is structurally identical to how INSERT places text V-positions.

`insertspanf` with `DOCISPAN` (`spanf1.c:15-53`) records in the global span filade that the link's I-space content lives in `docisaptr`, enabling FINDDOCSCONTAINING.

**Result: The link has a V-space position in the home document's link subspace. The home document is the owner document passed to CREATELINK — not the source or target content documents.**

---

#### Step 5 — Translate endpoint V-addresses to I-addresses (sporglsets)

```c
specset2sporglset (taskptr, fromspecset, &fromsporglset, NOBERTREQUIRED)   // do1.c:213
specset2sporglset (taskptr, tospecset,  &tosporglset,   NOBERTREQUIRED)   // do1.c:214
specset2sporglset (taskptr, threespecset, &threesporglset, NOBERTREQUIRED) // do1.c:215
```

`sporgl.c:14-65`: for each V-specset (which names a document + V-span), `vspanset2sporglset` calls `vspanset2ispanset` to look up the corresponding I-space addresses in the source/target/type documents' POMMs. The result is a **sporgl** — a triple of `(I-origin, I-width, home-docisa)`.

**The source and target documents are READ here (to perform the V→I mapping), but nothing is written into them.**

---

#### Step 6 — Write endpoint addresses into the link's own internal POOM

```c
setlinkvsas (&fromvsa, &tovsa, &threevsa)   // do1.c:216
insertendsetsinorgl (taskptr, linkisaptr, link, &fromvsa, fromsporglset, &tovsa, tosporglset, &threevsa, threesporglset)  // do1.c:217
```

`setlinkvsas` (`do2.c:169-183`) assigns fixed internal V-positions within the link object:

```c
fromvsaptr:   tumblerincrement(0,1) then (1,1) → 0.1.1
tovsaptr:     tumblerincrement(0,2) then (1,1) → 0.2.1
threevsaptr:  tumblerincrement(0,3) then (1,1) → 0.3.1
```

`insertendsetsinorgl` (`do2.c:130-148`) calls `insertpm` three times to insert the sporglsets (endpoint I-addresses) at positions 0.1.1, 0.2.1, and 0.3.1 **in the link's own POOM** — not in any content document. This is how `FOLLOWLINK` later retrieves the endpoints: it calls `link2sporglset` (`sporgl.c:67-95`) which does `retrieverestricted` on the link's orgl at the appropriate internal V-position.

---

#### Step 7 — Index link in the span filade by endpoint I-addresses

```c
insertendsetsinspanf (taskptr, spanf, linkisaptr, fromsporglset, tosporglset, threesporglset)  // do1.c:218
```

`do2.c:116-128`:

```c
insertspanf(taskptr, spanfptr, linkisaptr, fromsporglset, LINKFROMSPAN)
insertspanf(taskptr, spanfptr, linkisaptr, tosporglset,   LINKTOSPAN)
insertspanf(taskptr, spanfptr, linkisaptr, threesporglset, LINKTHREESPAN)
```

`spanf1.c:15-53`: for each sporgl (endpoint I-address), writes an entry into the global `spanf` mapping `(endpoint-I-address, LINKFROMSPAN|LINKTOSPAN|LINKTHREESPAN) → link-ISA`. This is what enables FINDLINKSFROMTOTHREE to query by endpoint V-range. Again, **nothing is written into the source or target documents**.

---

## Definitive Answer

CREATELINK **does** create a V-space entry — but in the **home document's link subspace**, not in the target or source documents.

| Structure | What is written | Where |
|---|---|---|
| Home document's POOM | V-address (link subspace) → link ISA | `docisaptr` (the "owner" doc) |
| Link's own POOM | 0.1.1 → FROM sporgl, 0.2.1 → TO sporgl, 0.3.1 → THREE sporgl | Inside the link's own orgl |
| Global span filade (`spanf`) | endpoint I-addresses → link ISA, tagged LINKFROMSPAN/LINKTOSPAN/LINKTHREESPAN | Global index; not any document's POOM |
| Source/target/type documents | **Nothing written** — only read (V→I lookup) | — |

The architectural pattern is: text INSERT places content in I-space and maps its I-address to V-positions in one document. CREATELINK does the same for the link object itself (in the home document's link subspace), and then additionally records the endpoint I-addresses in the link's own internal V-space structure and in the global span filade for lookup. The source and target documents gain no new V-space entries; they are consulted only to resolve the client-supplied V-specifications into I-addresses that the link can store.

### Issue 2: Endset reference domain contradicts ghost address linkability

**Category:** BOTH
**Reason:** Nelson's text says links can reference ghost elements, but the mechanism matters — whether endsets are stored as spans (start + length, naturally covering gaps and ghosts) or as sets of individual addresses determines how to resolve the contradiction. Nelson clarifies intent; Gregory clarifies storage representation.

**Nelson question:** When you say links may be made to ghost elements that "embrace all the contents below them," is the endset a span descriptor (a range that may cover addresses without stored content) rather than a set of individual content addresses?

**Nelson's Answer:**

Yes, exactly. An endset is a set of span descriptors — tumbler ranges — not a set of individual content addresses. This is explicit in the architecture.

## The Span Is a Range, Not an Enumeration

Nelson is clear that a span designates a *region* of tumbler-space, defined by its boundaries:

> "A span in the tumbler line, represented by two tumblers, refers to a subtree of the entire docuverse, (or merely to a series of elements of the same type, which is a degenerate case of a subtree)." [LM 4/24]

> "The first point of a span may designate a server, an account, a document or an element; so may the last point. There is no choice as to what lies between; this is implicit in the choice of first and last point." [LM 4/25]

The span doesn't enumerate what's inside it. The contents are determined by what happens to exist (or come to exist) within that range:

> "A span that contains nothing today may at a later time contain a million documents." [LM 4/25]

And crucially, a span is not a count:

> "A tumbler-span is not a conventional number, and it does not designate the number of bytes contained. It does not designate a number of anything." [LM 4/24]

## Ghost Elements Follow Directly

When I say links can be made to ghost elements that "embrace all the contents below them" [LM 4/23], this works precisely because the endset is a range descriptor, not a content-address set. A link whose endset spans a ghost account address covers the entire subtree rooted there — every document, version, and byte that exists (or will exist) under that account.

> "It is possible to link to a node, or an account, even though there is nothing stored in the docuverse corresponding to them." [LM 4/23]

> "A link to or search of an account or node will find any of the documents under it." [LM 4/23]

The endset says "from this tumbler to that tumbler." Whether anything is stored within that range is irrelevant to the endset's validity. The span is a *zone* on the tumbler line:

> "A span may be visualized as a zone hanging down from the tumbler line — what is called in computer parlance a depth-first spanning tree." [LM 4/25]

## Endsets Are Span-Sets

Each endset is itself a *set* of such spans — potentially multiple disjoint ranges:

> "The from-set may be an arbitrary collection of spans, pointing anywhere in the docuverse. Similarly, the to-set may be an arbitrary collection of spans pointing anywhere in the docuverse. We adopt the same convention for link types." [LM 4/43]

> "There is a universal address space, the tumbler line... We may visualize a link's endsets as mapping to it." [LM 4/45]

So an endset is: a set of (start-tumbler, end-tumbler) pairs, each pair defining a range on the tumbler line. Those ranges may cover ghost addresses, stored content, or both. The system resolves what actually exists within those ranges at query time, not at link-creation time.

This is what makes the ghost element mechanism work without any special machinery — it's just spans over tumbler-space, and tumbler-space is sparsely populated by design.

**Gregory question:** How are link endsets stored in the implementation — as span descriptors (start address + width) that define a range, or as enumerated sets of individual I-addresses? Can a stored endset span cover addresses not in dom.ispace?

**Gregory's Answer:**

## KB Synthesis

## Link Endset Storage

**Stored as span descriptors, not enumerated sets.**

### The Sporgl Format

Link endsets are stored as `Endset = set<Sporgl>` where each sporgl is a span descriptor:

```
Sporgl = { origin: IAddress, width: TumblerWidth, source_doc: ISA }
```

[SS-SPORGL] defines this explicitly. The `origin` is the start I-address and `width` is the span extent — a half-open interval `[origin, origin+width)`. The endset is a *set of spans*, not an enumerated set of individual addresses.

### How Endsets Are Built

When `domakelink` is called, the conversion chain `vspanset2sporglset` → `vspanset2ispanset` → `permute` → `span2spanset` → `retrieverestricted` walks the POOM to find contiguous I-address regions. **One sporgl is created per contiguous I-address region** [ST-LINK-CREATE / Finding 0037].

This is the transclusion case: if a V-span covers "AA" from source A and "BB" from source B, the two I-address regions are non-contiguous, producing two sporgls rather than one. The stored endset faithfully reflects the content identity structure, not the visual layout.

### Can a Stored Span Cover Addresses Not in dom.ispace?

**No, by construction.**

Each sporgl span is derived from an actual POOM entry lookup. POOM entries reference I-addresses that were allocated by INSERT or COPY [ST-INSERT, PRE-COPY]. INSERT allocates I-addresses contiguously via `findisatoinsertmolecule` → `tumblerincrement`, so within a single INSERT operation the resulting range `[α, α+n)` is fully occupied [SS-ADDRESS-SPACE / Finding 0033].

Furthermore, the granfilade is permanent and append-only [INV-IADDR-IMMUTABILITY, INV-NO-IADDR-REUSE]. Once allocated, I-addresses remain in dom.ispace forever regardless of subsequent DELETEs. DELETE removes POOM entries (V→I mappings) but does not touch the granfilade [FC-GRANF-ON-DELETE]. So even sporgls created from content later deleted from V-space reference I-addresses that remain valid in dom.ispace.

One nuance: the endsets are indexed in the spanfilade at link creation time [INT-SPORGL-LINK-INDEX]. After deletion, those stored endset spans still name valid I-addresses — the addresses exist permanently — but resolution through the POOM may return empty because no V-position maps to them anymore. This is the ghost link case [EC-GHOST-LINK]: `dom.ispace` membership is permanent, but V-space presence is mutable.

### Summary

| Property | Answer |
|----------|--------|
| Storage format | Set of span descriptors (`set<Sporgl>`) |
| Span granularity | One sporgl per maximal contiguous I-address region |
| Can span cover unallocated addresses? | No — derived from actual POOM entries |
| Can span cover deleted (V-unreachable) addresses? | Yes — I-addresses are permanent; V-presence is separate |

---

## Code Exploration

---

## Answer: Link Endset Storage in udanax-green

### The Core Representation: Span Descriptors, Not Enumerated Sets

Endsets are stored as **span descriptors** — `(origin, width)` pairs — not enumerated sets of individual I-addresses.

The central type is `typesporgl`, defined in `xanadu.h:115-121`:

```c
typedef struct structsporgl{
    struct structsporgl *next;
    typeitemid itemid;
    tumbler sporglorigin;   /* start I-address */
    tumbler sporglwidth;    /* extent */
    typeisa sporgladdress;  /* home document ISA */
} typesporgl;
```

A "sporgl" encodes a contiguous I-address range as `(sporglorigin, sporglwidth)`. When an endset covers non-contiguous I-ranges, it is represented as a **linked list** of sporgls — each element is itself a contiguous span. The list as a whole can be non-contiguous; no single element spans a gap.

---

### How Endsets Are Created: V→I Conversion

The client passes a `typevspec` (document ISA + V-span set). The conversion chain is:

**`docreatelink` (`do1.c:195-221`)** →  
**`specset2sporglset` (`sporgl.c:14-33`)** →  
**`vspanset2sporglset` (`sporgl.c:35-65`)** calls `vspanset2ispanset` →  
**`permute` / `span2spanset` (`orglinks.c:404-454`)** traverses the link document's POOM (permutation matrix enfilade) →  
Returns I-spans; each becomes one `typesporgl`:

```c
/* sporgl.c:50-57 */
sporglset = (typesporgl *) taskalloc(taskptr, sizeof(typesporgl));
sporglset->itemid = SPORGLID;
movetumbler(docisa, &sporglset->sporgladdress);
movetumbler(&ispanset->stream, &sporglset->sporglorigin);
movetumbler(&ispanset->width, &sporglset->sporglwidth);
```

The I-spans are derived by POOM traversal (`retrieverestricted` in `retrie.c`), which visits only crums that actually exist in the tree. So at creation time, each sporgl covers exactly a contiguous range of allocated permascroll content.

---

### Where Endsets Are Stored: Two Locations

`docreatelink` stores endsets in two places (`do1.c:218-219`):

#### 1. The Link's Own POOM (Permutation Matrix Enfilade)

`insertendsetsinorgl` (`do2.c:130-149`) calls `insertpm` (`orglinks.c:75-134`) for each of the three endsets. The V-slot for each endset is fixed by `setlinkvsas` (`do2.c:169-183`):

```c
/* do2.c:170-181 */
fromvsa  = 1.1  /* mantissa[0]=1, mantissa[1]=1 */
tovsa    = 2.1  /* mantissa[0]=2, mantissa[1]=1 */
threevsa = 3.1  /* mantissa[0]=3, mantissa[1]=1 */
```

In `insertpm`, each sporgl becomes a 2D crum with:
- `crumorigin.dsas[I]` ← `sporglorigin` (I start address)
- `crumwidth.dsas[I]`  ← `sporglwidth` (I width)
- `crumorigin.dsas[V]` ← the link's V-slot (1.1, 2.1, or 3.1)
- `crumwidth.dsas[V]`  ← proportional to sporgl width (`orglinks.c:116-117`)
- `type2dbottomcruminfo.homedoc` ← `sporgladdress` (the home document ISA)

#### 2. The Global Spanfilade Index

`insertendsetsinspanf` (`do2.c:116-128`) calls `insertspanf` (`spanf1.c:15-54`) for each endset type. Each sporgl becomes a 2D crum in the spanfilade:

```c
/* spanf1.c:22-51 */
crumorigin.dsas[ORGLRANGE] = prefixtumbler(linkisaptr, spantype)
/* LINKFROMSPAN=1, LINKTOSPAN=2, LINKTHREESPAN=3 */
crumorigin.dsas[SPANRANGE] = sporglorigin
crumwidth.dsas[SPANRANGE]  = sporglwidth
/* bottom crum info: homedoc = sporgladdress */
```

The spanfilade is the forward index used by `findlinksfromtothree` and `retrieveendsets`. Given a query I-span, the spanfilade's SPANRANGE dimension locates all crums whose I-spans intersect, and the ORGLRANGE dimension yields the link ISAs.

---

### Can a Stored Endset Span Cover Addresses Not in dom.ispace?

**At creation time: No, structurally prevented.**

The sporgls are produced by traversing the POOM via `retrieverestricted`. POOM crums are present only for content that was actually inserted via `insertpm`. Each crum represents a contiguous I-range of real allocated atoms. The I-spans returned by `permute` are therefore tight fits to existing permascroll content — there are no gaps or unallocated regions within a single returned sporgl.

**After document modification: Yes, possible by design.**

The stored endset I-spans in the link's POOM and the spanfilade are **not updated** when the source document is later modified (delete via `dodeletevspan`/`deletend`, or rearrange via `rearrangepm`/`rearrangend`). The link stores a snapshot of the I-spans at creation time.

- In Xanadu's permascroll model, I-addresses are permanent: allocated content never disappears from permascroll I-space, even if it is "deleted" from a document's V-space. A delete removes the V→I POOM mapping but not the permascroll content.
- Therefore, a stored endset I-span will always refer to valid permascroll content.
- But that content may no longer be mapped to any V-address in the source document. Whether this constitutes "not in dom.ispace" depends on definition: it is outside the document's current *virtual* I-space, but still within the global permascroll I-space.

**No validation at storage time.** `acceptablevsa` (`do2.c:110-113`) unconditionally returns `TRUE`:

```c
bool acceptablevsa(tumbler *vsaptr, typeorgl orglptr)
{
    return (TRUE);
}
```

And `insertspanf` / `insertpm` perform no check that a sporgl's I-range falls within any allocated region. The only guard is in `unpacksporgl` (`sporgl.c:195-202`), which rejects zero-width sporgls — it does not check upper bounds.

---

### Summary

| Question | Answer |
|---|---|
| Span descriptor or enumerated set? | **Span descriptor**: `(sporglorigin, sporglwidth)` tumbler pairs, held in `typesporgl`. Non-contiguous endsets are linked lists of sporgls. |
| Where stored? | **Two places**: (1) the link's POOM (I/V 2D crum, homedoc in cinfo); (2) the global spanfilade (SPANRANGE/ORGLRANGE 2D crum, prefixed by span type). |
| Can a stored endset span cover addresses not in dom.ispace? | **At creation: no** — sporgls come directly from POOM traversal of existing content. **After document modification: yes** — stored I-spans are not retroactively updated; they may point to I-addresses no longer in the document's V-space (though still valid in global permascroll I-space). There is no runtime bounds check at insertion or retrieval. |

### Issue 4: REARRANGE's precondition is absent

**Category:** GREGORY
**Reason:** The valid inputs for REARRANGE — what arguments it takes, whether regions must be disjoint/contiguous/non-empty, whether they must be within bounds — are implementation-level constraints that the code defines.

**Gregory question:** What arguments does the REARRANGE operation take (two disjoint spans? arbitrary regions?), and what constraints must those arguments satisfy for the operation to be well-defined — must regions be disjoint, contiguous, non-empty, and within the document's current V-space bounds?

**Gregory's Answer:**

## KB Synthesis

## REARRANGE Arguments and Constraints

### What REARRANGE Takes

REARRANGE takes **3 or 4 V-position cut points** (tumblers), not span pairs. The cuts define region boundaries within the document's V-space. [ST-REARRANGE, Finding 0006]

**Pivot (3 cuts):** `[cut0, cut1, cut2]`
- Region 1 = `[cut0, cut1)`, Region 2 = `[cut1, cut2)`
- Offset: Region 1 shifts `+= (cut2 - cut1)`, Region 2 shifts `−= (cut1 - cut0)`
- Result: regions swap around the `cut1` pivot

**Swap (4 cuts):** `[cut0, cut1, cut2, cut3]`
- Region 1 = `[cut0, cut1)`, Middle = `[cut1, cut2)`, Region 3 = `[cut2, cut3)`
- Regions 1 and 3 exchange positions; middle shifts by the size difference

### Enforced Constraints

**Cut count: exactly 3 or 4.** Providing 2 cuts causes a hard backend abort with "Wrong number of cuts". No other count is accepted. [PRE-REARRANGE, Finding 0006]

**Ordering: not required.** `sortknives()` reorders cuts into ascending order before computation. Misordered input is silently normalized. [PRE-REARRANGE, Finding 0056]

### Missing / Unenforced Constraints

**Non-empty regions: not required.** When `cut0 == cut1` (empty region), the offset contribution is zero and the operation degrades to a no-op for that region. `EC-REARRANGE-EMPTY-REGION` confirms this is accepted without error: `cut0 = cut1 ⟹ rearrange(doc, [cut0, cut1, cut2]) = doc`.

**Within document bounds: not validated.** Cut points are V-address tumblers. The algorithm computes offsets purely via tumbler arithmetic (`makeoffsetsfor3or4cuts`) without checking whether cuts fall within the document's current V-extent. Out-of-bounds cuts produce no-ops for the empty regions beyond the extent. [ST-REARRANGE, Finding 0056]

**Subspace-preserving: not enforced — this is a critical missing precondition.** The implementation has no guard preventing cuts from spanning subspace boundaries (1.x text vs 2.x links). A pivot with `[1.1, 1.4, 2.5]` will displace text content from V:1.x to V:2.x (link subspace), violating the content discipline. The implementation accepts this and stores the result silently. [PRE-REARRANGE, Finding 0051; EC-REARRANGE-CROSS-SUBSPACE]

**Disjoint regions: implicit by construction.** The cuts partition V-space into contiguous, non-overlapping intervals. For pivot, the two operative regions `[cut0, cut1)` and `[cut1, cut2)` are adjacent (share boundary at `cut1`, no overlap). For swap, regions 1 and 3 are separated by the middle `[cut1, cut2)`.

### The Formal Precondition Gap

The only *implemented* precondition is `|cuts| ∈ {3, 4}`. The spec-level precondition should additionally include:

```
∀ orgl ∈ affected(cuts): subspace(vpos(orgl) + diff[section(orgl)]) == subspace(vpos(orgl))
```

This subspace-preservation clause is **not checked** by the implementation. [PRE-REARRANGE, Finding 0051]

### Document-Level Precondition

The caller must hold WRITEBERT for the target document (OPEN for write access). [PRE-OPEN-DOC, co-occurring with PRE-REARRANGE]

### What REARRANGE Guarantees Regardless

- Content identity (I-addresses) is preserved — only V-positions change. [INV-REARRANGE-IDENTITY]
- Content outside all cut ranges is unchanged. [FC-REARRANGE-EXTERIOR]
- Links bound to rearranged content survive (I-address-based). [INV-REARRANGE-LINK-SURVIVAL]
- Pivot is self-inverse: applying the same 3 cuts twice restores the original state. [INV-PIVOT-SELF-INVERSE]

---

## Code Exploration

I now have everything needed to give a comprehensive answer. Here is the full analysis:

---

## REARRANGE Operation: Arguments and Constraints

### Protocol Signature

**Wire-level** (`get2fe.c:65-73`):
```c
bool getrearrange(typetask *taskptr, typeisa *docisaptr, typecutseq *cutseqptr)
{
    return (
       gettumbler (taskptr, docisaptr)
    && getcutseq (taskptr, cutseqptr));
}
```

The operation takes:
1. **Document ISA** — a tumbler identifying the target document
2. **A cut sequence** — a `typecutseq`, defined in `common.h:108-113`:

```c
#define MAXCUTS  4

typedef struct structcutseq {
    INT numberofcuts;
    tumbler cutsarray[MAXCUTS];
} typecutseq;
```

The cut sequence contains **N point addresses** in V-space — not spans with widths. These are scalar tumbler positions at which the document is to be sliced, not regions.

---

### Constraint: Exactly 3 or 4 Cuts (Enforced at Protocol Layer)

`getcutseq` in `get2fe.c:224-241` enforces this at parse time:

```c
bool getcutseq(typetask *taskptr, typecutseq *cutseqptr)
{
  INT ncuts, i;
    if (!(
       getnumber (taskptr, &ncuts)
    && (ncuts == 3 || ncuts == 4)))
        return (FALSE);          // ← hard protocol rejection
    cutseqptr->numberofcuts = ncuts;
    for (i = 0; i < ncuts; ++i) {
        if(!gettumbler (taskptr, &cutseqptr->cutsarray[i]))
            return(FALSE);
    }
    return(TRUE);
}
```

Any other count causes the entire request to fail before it reaches backend logic. Internally, `makeoffsetsfor3or4cuts` in `edit.c:182-183` also calls `gerror("Wrong number of cuts.")` for any other value.

---

### Constraint: Cuts Are Auto-Sorted (Order Not Required from Caller)

`rearrangend` in `edit.c:102-107` calls `sortknives` before any other work:

```c
knives.nblades = cutseqptr->numberofcuts;
for (i = 0; i < knives.nblades; i++) {
    movetumbler (&cutseqptr->cutsarray[i], &knives.blades[i]);
}
sortknives (&knives);
```

`sortknives` (`edit.c:250-263`) is a bubble-sort that puts cuts into ascending V-space order. **Callers are not required to provide cuts in sorted order.**

---

### What the Cuts Mean: Sections and Offsets

After sorting, the cuts define contiguous sections of V-space. `makeoffsetsfor3or4cuts` (`edit.c:164-184`) computes a displacement (`diff[1..3]`) for each inter-cut section:

**3-cut case** — cuts `[A, B, C]`, sections 0..3:

```c
tumblersub (&knives->blades[2], &knives->blades[1], &diff[1]); // diff[1] = C - B
tumblersub (&knives->blades[1], &knives->blades[0], &diff[2]); // diff[2] = -(B - A)
diff[2].sign = !diff[2].sign;
tumblerclear (&(diff[3]));                                      // diff[3] = 0
```

- Section 0 (before A): **unchanged** (case 0 in `rearrangend` switch)
- Section 1 ([A, B)): shifted by `+(C − B)` → moves to where section 2 was
- Section 2 ([B, C)): shifted by `−(B − A)` → moves to where section 1 was
- Section 3 (after C): **unchanged**

This is a **swap of two adjacent regions** [A,B) and [B,C).

**4-cut case** — cuts `[A, B, C, D]`, sections 0..4:

```c
tumblersub (&knives->blades[2], &knives->blades[0], &(diff[1])); // diff[1] = C - A
// ...
diff[3].sign = !diff[1].sign;                                     // diff[3] = -(C - A)
// diff[2] = (D-C) - (B-A)
```

- Section 0 (before A): **unchanged**
- Section 1 ([A, B)): shifted by `+(C − A)`
- Section 2 ([B, C)): shifted by `(D−C) − (B−A)`
- Section 3 ([C, D)): shifted by `−(C − A)`
- Section 4 (after D): **unchanged**

This moves section 1 to start at C and section 3 to start at A; section 2 slides by the difference in widths. For a clean no-gap, no-overlap result, **sections 1 and 3 should have equal width**, but this is not enforced.

The sections are classified per crum by `rearrangecutsectionnd` (`edit.c:191-204`), which uses `whereoncrum` to find which interval each crum falls into, then applies `diff[i]` via `tumbleradd` on the crum's V-space displacement (`edit.c:125`):

```c
case 1:  case 2:  case 3: /* 3 only moves in 4 cuts */
    tumbleradd (&ptr->cdsp.dsas[index], &diff[i], &ptr->cdsp.dsas[index]);
    ivemodified((typecorecrum*)ptr);
    break;
```

---

### Constraint: Document Must Be Open for Writing (Enforced)

`dorearrange` in `do1.c:34-43` calls `findorgl` with `WRITEBERT`:

```c
bool dorearrange(typetask *taskptr, typeisa *docisaptr, typecutseq *cutseqptr)
{
    return (
       findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)  // ← ownership check
    && rearrangepm (taskptr, docisaptr, docorgl, cutseqptr)
    );
}
```

`WRITEBERT` is defined in `common.h:167` and enforces that the document is open for write by the requesting user. If not, `findorgl` returns `FALSE` and the operation fails cleanly.

---

### What Is NOT Enforced

| Constraint | Enforced? | Consequence of Violation |
|---|---|---|
| Exactly 3 or 4 cuts | **YES** — `get2fe.c:231` | Request rejected at parse time |
| Document open for write | **YES** — `do1.c:40` | Returns `FALSE` |
| Cuts sorted | Auto-corrected — `edit.c:107` | No issue |
| Cuts must be distinct (non-degenerate) | **NO** | Zero-width sections → no-op displacement (`diff = 0`); no error |
| Cuts must be within document's V-space | **NO** | Out-of-bounds cuts pass through `makecutsnd` / `rearrangecutsectionnd` without hitting any crums; the operation silently succeeds but rearranges nothing |
| Regions must be non-empty | **NO** | Same as above |
| Regions 1 and 3 must have equal width (4-cut) | **NO** | Creates gaps or overlaps in V-space; content may collide |
| Cuts must be in the text subspace (V ≥ 1.0) | **NO** | Could target link-subspace content |

Note: `rearrangend` (`edit.c:78`) contains a commented-out call to `fixincoresubtreewids` inside an `#ifdef UNdeFined` block, indicating the developers knew that wid (width) consistency could be left in an incorrect state in some code paths. The comment reads: *"a temp kluge zzz till we find where setwisp isn't called"* — confirming that the operation was known to be fragile around tree-consistency when cuts are ill-specified.

---

### The Critical Guard: `THRUME` Must Never Occur at Classification Time

If a cut was *not* properly pre-split before `rearrangecutsectionnd` runs, `whereoncrum` might return `THRUME` (the address passes through the crum rather than landing on a boundary). `rearrangecutsectionnd` returns `-1` in that case (`edit.c:197-199`), and `rearrangend` calls `gerror("rearrangend can't classify crum\n")` — a fatal error (`edit.c:116-121`). The pre-splitting done by `makecutsnd` should prevent this, but **this is an implicit contract, not a checked precondition**.

---

### Summary

The REARRANGE operation takes a document ISA and a sequence of **exactly 3 or 4 V-space cut-point addresses** (not spans). The only hard constraints enforced by the code are:

1. **Exactly 3 or 4 cuts** (rejected at parse time, `get2fe.c:231`)
2. **Document must be open for writing** (`do1.c:40` via `WRITEBERT`)

Everything else — that cuts be distinct, non-empty, within V-space bounds, or that sections have compatible widths for a clean rearrangement — is **the caller's responsibility and is not validated**. Violations do not produce errors; they produce silent no-ops or corrupted V-space geometry.
