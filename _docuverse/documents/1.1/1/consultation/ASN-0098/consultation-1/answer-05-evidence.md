## Question 5 [evidence]

> Does udanax-green's span or endset construction follow any convention — e.g., tight coverage matching the I-addresses resident at construction time — that ensures K.α-allocated addresses fall outside existing endset coverage?

## KB Synthesis

## Endset Coverage and Allocation Disjointness

The KB does not describe an **explicit** tight-coverage convention designed with this goal in mind, but the property holds implicitly through two independent mechanisms that combine.

### Endset Construction Is POOM-Resident-Exact

`vspanset2sporglset` converts V-spans to sporgls via `vspanset2ispanset` → `permute` → `span2spanset` → `retrieverestricted`, walking the document's POOM to find every contiguous I-address region covered by the input spans [SS-VSPAN-TO-SPORGL, SS-SPORGL]. The resulting endset I-address coverage exactly matches the I-addresses resident in the POOM at construction time — neither more nor less. A multi-source V-span (transcluded content) produces multiple sporgls, one per contiguous I-address run [SS-LINK-ENDPOINT, Finding 0037]. This makes the coverage tight in the sense asked about.

### Subsequent Allocations Are Strictly Greater

Because `findpreviousisagr` queries the entire granfilade tree for the current maximum I-address and increments by 1 [SS-ADDRESS-SPACE, Finding 0061], every allocation after link creation receives an address strictly exceeding all previously allocated addresses. This holds unconditionally:

- Text content allocations [INV-MONOTONIC]: `∀ alloc_a, alloc_b : time(a) < time(b) ⟹ iaddr(b) > iaddr(a)`
- Link orgl allocations within a document's element-subspace-2 partition [SS-ADDRESS-ALLOC, Finding 0065]
- No I-address is ever freed or reused [INV-NO-IADDR-REUSE]

DELETE does not affect the granfilade — it removes only POOM mappings [FC-GRANF-ON-DELETE] — so even deleted I-addresses remain in the granfilade tree as allocation anchors, preventing gaps from being filled.

### Caveat: CREATELINK Advances the Counter

CREATELINK allocates a link orgl I-address within the same granfilade tree, advancing the maximum and creating a gap in the subsequent text I-address sequence [INT-LINK-INSERT, Finding 0063]. This means text content inserted after CREATELINK is non-contiguous with text inserted before — but crucially, those new text I-addresses still fall outside (strictly above) the endset's covered range, since the endset was built from I-addresses that existed before CREATELINK.

### Summary

The disjointness property — that K.α-allocated addresses fall outside existing endset coverage — holds by composition: **tight POOM-resident capture at construction time** [SS-VSPAN-TO-SPORGL] plus **strict monotonic allocation** [INV-MONOTONIC, INV-NO-IADDR-REUSE]. There is no named invariant or design comment articulating this as an intentional goal; it is an emergent consequence of the append-only granfilade strategy.

---

## Code Exploration

---

## Analysis: Span/Endset Construction Conventions and K.α Address Allocation

### 1. What "endsets" and "spans" mean here

There are two distinct coverage structures to track:

**I-space spans (granfilade coverage):** The granfilade is indexed by `WIDTH` (I-space). Text and orgls occupy I-address ranges stored as bottom-crum records (`GRANTEXT`, `GRANORGL`). The *effective span* of a content block is the I-address range it occupies.

**V-space endsets (POOM + spanfilade):** Links store their endpoint content as sporglsets that record I-spans. Those are mapped through the POOM to V-addresses, and the link endpoint records (keyed by `LINKFROMSPAN`/`LINKTOSPAN`/`LINKTHREESPAN`) are stored in the spanfilade. The term "endset" in the code refers specifically to these three link-endpoint records.

The constants at `xanadu.h:36–39`:
```c
#define LINKFROMSPAN    1
#define LINKTOSPAN      2
#define LINKTHREESPAN   3
#define DOCISPAN        4
```

---

### 2. I-space allocation: `findisatoinsertgr` and its two paths

Every new I-space address goes through `granf2.c:130` (`findisatoinsertgr`), which dispatches on atom type:

```c
bool findisatoinsertgr(typecuc *fullcrumptr, typehint *hintptr, typeisa *isaptr)
{
    if (hintptr->subtype == ATOM) {
        if (!isaexistsgr (fullcrumptr, &hintptr->hintisa)) { return FALSE; }
        findisatoinsertmolecule (fullcrumptr, hintptr, isaptr);
    } else {
        findisatoinsertnonmolecule (fullcrumptr, hintptr, isaptr);
    }
    tumblerjustify(isaptr);
    return (TRUE);
}
```
[`granf2.c:130–156`]

**Path A — atoms (text, links):** `findisatoinsertmolecule` [`granf2.c:158–181`]:
```c
tumblerincrement (&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound);
clear (&lowerbound, sizeof(lowerbound));
findpreviousisagr ((typecorecrum*)fullcrumptr, &upperbound, &lowerbound);
if (tumblerlength (&hintptr->hintisa) == tumblerlength (&lowerbound)) {
    tumblerincrement (&lowerbound, 2, hintptr->atomtype, isaptr);
    tumblerincrement (isaptr, 1, 1, isaptr);
} else if (hintptr->atomtype == TEXTATOM) {
        tumblerincrement (&lowerbound, 0, 1, isaptr);
} else if (hintptr->atomtype == LINKATOM) {
    tumblerincrement (&hintptr->hintisa, 2, 2, isaptr);
    if (tumblercmp (&lowerbound, isaptr) == LESS)
        tumblerincrement (isaptr, 1, 1, isaptr);
    else
        tumblerincrement (&lowerbound , 0, 1, isaptr);
}
```

The protocol: set `upperbound = hintisa + (atomtype+1) × 10⁻²`, find the last existing ISA below that bound via `findpreviousisagr`, then allocate at `lowerbound + 1` (last digit incremented). The new address is strictly greater than all existing addresses within the hinted scope.

**Path B — documents/accounts:** `findisatoinsertnonmolecule` [`granf2.c:203–242`]:
```c
depth = hintptr->supertype == hintptr->subtype ? 1 : 2;
hintlength = tumblerlength (&hintptr->hintisa);
tumblerincrement (&hintptr->hintisa, depth - 1, 1, &upperbound);
...
findpreviousisagr ((typecorecrum*)fullcrumptr, &upperbound, &lowerbound);
...
if (iszerotumbler(&lowerbound) || !lowerbound_under_hint) {
    tumblerincrement(&hintptr->hintisa, depth, 1, isaptr);
} else {
    tumblertruncate (&lowerbound, hintlength + depth, isaptr);
    tumblerincrement(isaptr, tumblerlength(isaptr)==hintlength?depth:0, 1, isaptr);
}
```

Same pattern: finds previous, increments. `lowerbound_under_hint` guards against picking up an address from a sibling account.

**In both paths, the allocation is strictly monotonically increasing within the hinted scope.** There is no randomness, no gap pre-reservation, and no look-ahead. The algorithm is: "find the highest existing address in this scope, produce the next one."

---

### 3. Endset construction is tight

**Text insertion** — `inserttextgr` [`granf2.c:83–109`]:
```c
if (!findisatoinsertgr ((typecuc*)fullcrumptr, hintptr, &lsa))
    return (FALSE);
movetumbler (&lsa, &spanorigin);
for (; textset; textset = textset->next) {
    ...
    insertseq ((typecuc*)fullcrumptr, &lsa, &locinfo);
    tumblerincrement (&lsa, 0, textset->length, &lsa);
}
ispanptr->stream = spanorigin;
tumblersub (&lsa, &spanorigin, &ispanptr->width);  // width = exactly bytes written
```

`width = lsa − spanorigin` = exactly the characters just inserted. No pre-allocated headroom, no over-coverage.

`findlastisaincbcgr` [`granf2.c:280–284`] is what `findpreviousisagr` uses at leaf level:
```c
int findlastisaincbcgr(typecbc *ptr, typeisa *offset)
{
    if (ptr->cinfo.infotype == GRANTEXT)
        tumblerincrement (offset, 0, (INT) ptr->cinfo.granstuff.textstuff.textlength - 1, offset);
}
```
This returns `start_of_last_text + length − 1`, i.e., the address of the last byte. Then `findisatoinsertmolecule` increments it by 1 (`tumblerincrement(&lowerbound, 0, 1, isaptr)`), yielding `start_of_last_text + length` — exactly the exclusive right endpoint of the last span. The new allocation starts where the previous span ends.

**POOM extension logic** — `isanextensionnd` [`insertnd.c:301–309`]:
```c
bool isanextensionnd(typecbc *ptr, typedsp *offsetptr, typedsp *originptr, type2dbottomcruminfo *infoptr)
{
    if (!tumblereq (&infoptr->homedoc, &((type2dcbc *)ptr)->c2dinfo.homedoc))
        return (FALSE);
    prologuend ((typecorecrum*)ptr, offsetptr, &grasp, &reach);
    return (lockeq (reach.dsas, originptr->dsas, (unsigned)dspsize(ptr->cenftype)));
}
```
A new crum extends an existing one only when (a) same `homedoc` AND (b) `reach == origin` exactly. This is exact-boundary coverage — no overlap, no gap. Non-abutting insertions create a new crum via `insertcbcnd` [`insertnd.c:242–275`].

**Link ISA footprint** — `tumbler2spanset` [`do2.c:48–61`] converts a link's ISA to its granfilade footprint:
```c
tumblerincrement (&spanptr->width, tumblerlength (tumblerptr)-1, 1, &spanptr->width);
```
Width is `10^{−(length−1)}` — exactly one "unit" at the tumbler's own depth. Tight.

---

### 4. Spanfilade endsets: fixed slots, not I-space range coverage

`retrieveendsetsfromspanf` [`spanf1.c:190–235`] and `insertendsetsinspanf` [`do2.c:116–128`] show that endsets in the spanfilade are indexed in ORGLRANGE by a fixed small integer prefixed to the link ISA (not a range):

```c
fromspace.stream.mantissa[0] = LINKFROMSPAN;   // = 1
fromspace.width.mantissa[0] = 1;
tospace.stream.mantissa[0]  = LINKTOSPAN;      // = 2
tospace.width.mantissa[0]   = 1;
```
[`spanf1.c:210–214`]

And `insertspanf` [`spanf1.c:22`]:
```c
prefixtumbler (isaptr, spantype, &crumorigin.dsas[ORGLRANGE]);
```
The ORGLRANGE key is `prefixtumbler(linkISA, 1/2/3)` — a unique address per link, not a range competing with content. The SPANRANGE dimension carries the actual content I-spans the user specified. The two dimensions do not interfere with each other.

---

### 5. V-space: what the backend does and does not guarantee

**For text:** The caller supplies the V-address (`vsaptr`) directly to `doinsert` [`do1.c:87`]. The backend's `acceptablevsa` [`do2.c:110–113`] is:
```c
bool acceptablevsa(tumbler *vsaptr, typeorgl orglptr)
{
    return (TRUE);
}
```
Completely unchecked. The POOM will accept any V-address, including one that overlaps existing content. V-space coverage for text depends entirely on client correctness.

**For links:** V-addresses are allocated by `findnextlinkvsa` [`do2.c:151–167`]:
```c
tumblerclear (&firstlink);
tumblerincrement (&firstlink, 0, 2, &firstlink);
tumblerincrement (&firstlink, 1, 1, &firstlink);   // firstlink = 2.1

doretrievedocvspan (taskptr, docisaptr, &vspan);
tumbleradd (&vspan.stream, &vspan.width, &vspanreach);
if (tumblercmp (&vspanreach, &firstlink) == LESS)
    movetumbler (&firstlink, vsaptr);
else
    movetumbler (&vspanreach, vsaptr);
```
New link V-address = max(document's current V-reach, 2.1). This guarantees link metadata lands past all existing V-content (text is in V ≥ 1.0; links get V ≥ 2.1). The `setlinkvsas` convention [`do2.c:169–183`] then assigns from-endpoint at 1.1, to-endpoint at 2.1, three-endpoint at 3.1 *within the link's own orgl* — these are intra-link relative slots, not global V-space.

---

### 6. Does the convention ensure K.α addresses fall outside existing endset coverage?

**In I-space (granfilade): YES, by the sequential allocation algorithm itself.**

The invariant is maintained operationally, not by an explicit assertion:

1. `findpreviousisagr` finds the last (highest) existing ISA below `upperbound`
2. `lowerbound` = that address (with the last-byte correction from `findlastisaincbcgr`)
3. New ISA = `lowerbound + 1` at the same digit depth

Since all existing spans end at addresses ≤ `lowerbound`, and the new address is `lowerbound + 1`, the new address is strictly past the right endpoint of every existing span in scope. It cannot fall inside any existing I-space span.

This is a consequence of tight endset coverage + monotonically increasing allocation. If endsets over-covered (padded beyond actual content), a new allocation could land in padding and create a false collision. The tight construction in `inserttextgr` is what makes the allocation safe.

**In V-space for text: NOT guaranteed by the backend.** `acceptablevsa` is a stub. This is a known gap — the backend trusts the client not to supply overlapping V-addresses for text.

**In V-space for links: YES, guaranteed by `findnextlinkvsa`**, which ensures link V-addresses land past all existing V-content.

---

### Summary

| Address space | Coverage convention | Guarantee for K.α |
|---|---|---|
| I-space (granfilade text/links) | Tight: `width = lsa − spanorigin` exactly | **Yes** — `findpreviousisagr + increment` ensures strict monotone order |
| I-space (POOM extension) | Exact boundary: `isanextensionnd` requires `reach == origin` | **Yes** — same allocation path |
| V-space text (client-supplied) | Not validated (`acceptablevsa` returns TRUE always) | **No guarantee from backend** |
| V-space links | `findnextlinkvsa` sets to max(doc reach, 2.1) | **Yes** — always past existing V-content |

The tight endset construction is not incidental — without it, `findpreviousisagr`'s "last ISA" would be inside a padded span, and `lowerbound + 1` would land inside existing coverage. The tight coverage is structurally necessary for safe sequential allocation, even though no assertion checks this invariant explicitly.
