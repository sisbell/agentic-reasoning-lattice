## Question 11 [evidence]

> When CREATELINK allocates a link's identity via `findnextlinkvsa`, does the returned V-position come from a per-document link counter (`max(existing_link_v_positions)+1`), and is the link orgl's I-address allocated as `docISA.0.2.N` independently per home document?

## KB Synthesis

**V-position allocation (`findnextlinkvsa`)**

The first link in a document is placed at V-position `2.1` — hardcoded by incrementing the first mantissa digit to `2` then to `2.1`. Subsequent links are placed at `vspanreach` (the current end of the document's V-extent), not by computing `max(existing_link_v_positions)+1`. These two are equivalent in sequential single-user operation because link orgls are always appended, so `vspanreach` always equals the position after the last link. However, the mechanism is append-at-extent, not max-plus-one scan. [SS-LINK-SUBSPACE], [ST-CREATE-LINK]

**I-address allocation**

Yes, independently per home document. The allocation uses `findisatoinsertmolecule` with `upperbound = docISA.2.3`, bounding the search to that document's link element subspace. `findpreviousisagr` finds the highest existing link I-address below that bound within the document, then increments by 1. The result is `docISA.0.2.N` with N monotonically increasing per (home document, element_field=2) pair — link counters in document A are completely independent of those in document B. [SS-ADDRESS-SPACE (Finding 0065)], [SS-ADDRESS-ALLOC (Finding 0065)], [INV-MONOTONIC]

---

## Code Exploration

I now have enough detail to give a complete answer.

---

## CREATELINK: Link Identity and Address Allocation

### Call Chain Entry Points

`createlink` in `fns.c:101-111` dispatches to `docreatelink` [do1.c:195], which orchestrates two independent allocations: the link's I-address (in the granfilade) and its V-position (in V-space).

```c
// fns.c:107-108
getcreatelink (taskptr, &docisa, &fromspecset, &tospecset, &threespecset)
&& docreatelink (taskptr, &docisa, fromspecset, tospecset, threespecset, &linkisa)
```

```c
// do1.c:207-211 — two independent allocations in sequence
createorglingranf (taskptr, granf, &hint, linkisaptr)   // I-address
&& tumbler2spanset (taskptr, linkisaptr, &ispanset)
&& findnextlinkvsa (taskptr, docisaptr, &linkvsa)       // V-position
```

---

### V-Position: `findnextlinkvsa`

```c
// do2.c:151-167
bool findnextlinkvsa(typetask *taskptr, typeisa *docisaptr, tumbler *vsaptr)
{
  tumbler vspanreach, firstlink;
  typevspan vspan;
  bool doretrievedocvspan();
    tumblerclear (&firstlink);
    tumblerincrement (&firstlink, 0, 2, &firstlink);     // firstlink = "2"
    tumblerincrement (&firstlink, 1, 1, &firstlink);     // firstlink = "2.1"

    (void) doretrievedocvspan (taskptr, docisaptr, &vspan);         // read doc V-span
    tumbleradd (&vspan.stream, &vspan.width, &vspanreach);          // end = stream + width
    if (tumblercmp (&vspanreach, &firstlink) == LESS)
        movetumbler (&firstlink, vsaptr);                // floor at "2.1"
    else
        movetumbler (&vspanreach, vsaptr);               // append after all existing content
    return (TRUE);
}
```

`doretrievedocvspan` [do1.c:312-320] calls `findorgl` (keyed by `docisaptr`) then `retrievevspanpm`:

```c
// orglinks.c:165-172
bool retrievevspanpm(typetask *taskptr, typeorgl orgl, typevspan *vspanptr)
{
    movetumbler (&((typecuc *) orgl)->cdsp.dsas[V], &vspanptr->stream);
    movetumbler (&((typecuc *) orgl)->cwid.dsas[V], &vspanptr->width);
    return (TRUE);
}
```

**What `findnextlinkvsa` actually computes:** It reads the document's own crum's `cdsp.dsas[V]` (V-stream start) and `cwid.dsas[V]` (V-width), computes `stream + width` — the absolute V-address just past the end of the document's entire current V-span — and uses that as the new link's V-position. There is no scan over existing link V-positions. The mechanism is the stored V-span high-water mark, not `max(link_V_positions)+1`.

The question's framing is thus **partially correct, but imprecise**:
- It is **per-document**: the lookup is keyed by `docisaptr`, and each document's orgl carries its own independent V-span.
- It is **not a link counter**: it is the end of the document's full V-span (covering text content and previous links alike). Since each new link is appended via `docopy` [do1.c:185/212] — which extends the stored V-span — successive link V-addresses are always monotonically increasing. But the mechanism reads the document's V-extent, not the maximum link address.
- The floor `firstlink` evaluates to the printed tumbler `"2.1"` (not "0.2.1"): `tumblerincrement(zero, rightshift=0, bint=2)` → `{exp=0, mantissa[0]=2}` = `"2"`; then `tumblerincrement("2", rightshift=1, bint=1)` → `{exp=0, mantissa[0]=2, mantissa[1]=1}` = `"2.1"`.

---

### I-Address: `findisatoinsertmolecule` with `LINKATOM`

The hint is constructed at [do1.c:207]:
```c
makehint (DOCUMENT, ATOM, LINKATOM, docisaptr, &hint);
```

`LINKATOM = 2` [xanadu.h:146]. `createorglingranf` → `findisatoinsertgr` [granf2.c:130-156] → `findisatoinsertmolecule` [granf2.c:158-181]:

```c
// granf2.c:158-181
static int findisatoinsertmolecule(typecuc *fullcrumptr, typehint *hintptr, typeisa *isaptr)
{
  typeisa upperbound, lowerbound;

    tumblerincrement (&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound); // docISA.0.3 for LINKATOM
    clear (&lowerbound, sizeof(lowerbound));
    findpreviousisagr ((typecorecrum*)fullcrumptr, &upperbound, &lowerbound);    // highest existing < upperbound

    if (tumblerlength (&hintptr->hintisa) == tumblerlength (&lowerbound)) {      // no existing links
        tumblerincrement (&lowerbound, 2, hintptr->atomtype, isaptr);            // docISA.0.2
        tumblerincrement (isaptr, 1, 1, isaptr);                                 // docISA.0.2.1  ← first link
    } else if (hintptr->atomtype == TEXTATOM) {
            tumblerincrement (&lowerbound, 0, 1, isaptr);
    } else if (hintptr->atomtype == LINKATOM) {                                  // subsequent links
        tumblerincrement (&hintptr->hintisa, 2, 2, isaptr);                      // docISA.0.2
        if (tumblercmp (&lowerbound, isaptr) == LESS)
            tumblerincrement (isaptr, 1, 1, isaptr);                             // docISA.0.2.1
        else
            tumblerincrement (&lowerbound , 0, 1, isaptr);                       // prev_link + 1 → docISA.0.2.N
    }
}
```

**Tumbler arithmetic unpacked** (from `tumblerincrement` [tumble.c:599-623]):

For the non-zero case, `tumblerincrement(addr, rightshift, bint, dest)` finds the index `idx` of the rightmost non-zero mantissa component, then sets `mantissa[idx + rightshift] += bint`. The printing code [put.c:35-41] outputs `|exp|` leading `"0."` prefixes, then mantissa[0] through mantissa[place].

For `docISA = "1.5.0.1"` stored as `{exp=0, m[0]=1, m[1]=5, m[2]=0, m[3]=1}` (rightmost non-zero at `idx=3`):
- `tumblerincrement(docISA, 2, 2)` → sets `m[3+2] = m[5] += 2`, leaving `m[4]=0` → printed: `"1.5.0.1.0.2"`
- `tumblerincrement("1.5.0.1.0.2", 1, 1)` → rightmost non-zero is `m[5]=2`, sets `m[6] += 1` → `"1.5.0.1.0.2.1"`

The `rightshift=2` in line 166 (and line 171) creates exactly one zero-separator position between the document's last component and the link-type digit `2`, yielding the pattern `docISA.0.2.N`.

**Answers to both parts:**

1. **V-position is per-document**: Yes, `findnextlinkvsa` is keyed by `docisaptr` and reads that document's stored V-span end-point. But the counter is **not** `max(existing_link_v_positions)+1` — it is `docVspan.stream + docVspan.width`, the end of the document's total V-extent. The result is equivalent to appending after the last link only because links are appended last.

2. **I-address is `docISA.0.2.N`, independently per home document**: **Yes, confirmed exactly**. The first link gets `.0.2.1`; each subsequent link gets the previous link's last component incremented by 1 via `findpreviousisagr` + `tumblerincrement(lowerbound, 0, 1)`. The root is always `docISA`, making the counter fully per-document, with no shared global link counter.
