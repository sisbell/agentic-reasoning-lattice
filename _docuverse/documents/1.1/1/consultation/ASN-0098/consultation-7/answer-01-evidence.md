## Question 1 [evidence]

> How does udanax-green construct endset spans when a link is created against existing content, and what placement of span endpoints (start, width) does the implementation enforce relative to the allocator's emission sequence?

## KB Synthesis

## Endset Span Construction at Link Creation

When `domakelink` receives a user-provided V-span as a link endpoint, it constructs endset spans through a two-phase pipeline that maps position back to identity.

### Phase 1: V-to-I Conversion

`vspanset2sporglset` [SS-SPORGL] drives the conversion:

1. Calls `vspanset2ispanset` → `permute` → `span2spanset` → `retrieverestricted` to walk the target document's POOM and collect all context entries (V→I mappings) that fall within the specified V-span.
2. For each **contiguous I-address region** found, creates one sporgl: `{ origin: IAddress, width: TumblerWidth, source_doc: ISA }` [ST-LINK-CREATE / Finding 0037].

The critical point: one V-span input may produce **multiple sporgls** if the content was assembled from different I-address origins (e.g., transcluded from two sources). The inner loop in `sporgl.c:49-58` creates one sporgl per `typeispan` returned — it never merges across I-address discontinuities.

### Phase 2: Span Endpoint Values

For each sporgl the implementation assigns:

- **`origin`** = the I-address of the first byte in that contiguous I-region, as recorded in the POOM crum's `cdsp.dsas[I]` field [SS-POOM-BOTTOM-CRUM / Finding 0076].
- **`width`** = `tumblersub(end_iaddr, start_iaddr)` — a tumbler whose numeric value equals the byte count of content in that region [SS-SPAN / Finding 0031].

The width is copied directly from the I-span without re-encoding (unlike the POOM's V-width, which is re-encoded at V-space precision [SS-INSERT-VWIDTH-ENCODING]).

### Relationship to Allocator Emission Sequence

I-address allocation is strictly monotonically increasing and query-and-increment [INV-MONOTONIC / Finding 0033]:

```
INSERT "ABCDE" → I.1, I.2, I.3, I.4, I.5 (contiguous, one I-span)
```

For content inserted in a single uninterrupted sequence, the endset has **one sporgl** with `origin = I.1`, `width = 0.5`.

But if a `CREATELINK` or any non-text granfilade allocation occurs between inserts, the I-address counter advances past a gap [INT-LINK-INSERT / Finding 0063]:

```
INSERT "ABC" → I.1, I.2, I.3
CREATELINK   → link orgl consumes space ~I.2.0
INSERT "DE"  → I.2.1, I.2.2  (non-contiguous with ABC)
```

A V-span covering "ABCDE" would now produce **two sporgls**:
- `{ origin: I.1, width: 0.3 }` — for "ABC"
- `{ origin: I.2.1, width: 0.2 }` — for "DE"

### What the Implementation Enforces

The implementation enforces **no span shape constraints** beyond what the POOM already records. The endset is purely **derived from the POOM state at link-creation time**:

- The `origin` of each sporgl is whatever I-address happens to be at the start of each contiguous V→I run in the POOM.
- The `width` is whatever tumbler subtraction yields for that run's length.
- Content transcluded from multiple sources (with non-contiguous I-origins) is **automatically split** into one sporgl per contiguous region [ST-LINK-CREATE / Finding 0037].

There is no precondition that forces contiguity of the endset's I-address range — contiguity is a property of the content's insertion history, not a link-level constraint. A link endpoint pointing at transcluded content from N distinct insertion events will have N sporgls, regardless of how the user specified the V-span.

The subspace constraint applies implicitly: because `compare_versions` and link discovery operate in I-space over permascroll addresses, a V-span that includes the link subspace (`2.x`) would pull in link orgl ISAs — a different I-address type that is not shared via transclusion and would produce meaningless sporgls [PRE-COMPARE-VERSIONS, FC-SUBSPACE].

---

## Code Exploration

I now have everything needed to give a complete, cited answer.

---

## How udanax-green Constructs Endset Spans for Link Creation

### Entry Point

`createlink` [fns.c:100] delegates to `docreatelink` [do1.c:195] after parsing the FEBE request. `docreatelink` is a 9-step boolean chain:

```c
// do1.c:208–220
createorglingranf(taskptr, granf, &hint, linkisaptr)
&& tumbler2spanset(taskptr, linkisaptr, &ispanset)
&& findnextlinkvsa(taskptr, docisaptr, &linkvsa)
&& docopy(taskptr, docisaptr, &linkvsa, ispanset)
&& findorgl(taskptr, granf, linkisaptr, &link, NOBERTREQUIRED)
&& specset2sporglset(taskptr, fromspecset, &fromsporglset, NOBERTREQUIRED)
&& specset2sporglset(taskptr, tospecset, &tosporglset, NOBERTREQUIRED)
&& specset2sporglset(taskptr, threespecset, &threesporglset, NOBERTREQUIRED)
&& setlinkvsas(&fromvsa, &tovsa, &threevsa)
&& insertendsetsinorgl(taskptr, linkisaptr, link, &fromvsa, fromsporglset, &tovsa, tosporglset, &threevsa, threesporglset)
&& insertendsetsinspanf(taskptr, spanf, linkisaptr, fromsporglset, tosporglset, threesporglset)
```

---

### Step 1: Link ISA Allocation

```c
makehint(DOCUMENT, ATOM, LINKATOM, docisaptr, &hint);   // do2.c:78–84
createorglingranf(taskptr, granf, &hint, linkisaptr);    // do1.c:209
```

`createorglingranf` assigns a fresh tumbler address to the link — the allocator's next available slot, sequentially later than all previously allocated content ISAs.

---

### Step 2: The Link's Own Span — `tumbler2spanset` [do2.c:48–61]

```c
spanptr->itemid = ISPANID;
movetumbler(tumblerptr, &spanptr->stream);          // stream = linkISA
tumblerclear(&spanptr->width);                      // width = 0
tumblerincrement(&spanptr->width,
    tumblerlength(tumblerptr)-1,                    // rightshift = (depth - 1)
    1,
    &spanptr->width);
```

Since width starts at zero, `tumblerincrement` takes its zero-tumbler branch [tumble.c:603–608]:

```c
cptr->exp = -rightshift;     // = -(tumblerlength - 1)
cptr->mantissa[0] = 1;
```

**Enforced placement**: `start = linkISA`; `width = 1` with exponent `-(depth-1)`. If the link ISA has `n` digit levels, the width is one atomic unit at level `n–1` — a single slot at the allocator's current resolution. Every link is exactly one tumbler-atom wide, with width derived from ISA depth, not content size.

---

### Step 3: Document Placement Floor — `findnextlinkvsa` [do2.c:151–167]

```c
tumblerclear(&firstlink);
tumblerincrement(&firstlink, 0, 2, &firstlink);   // firstlink = 2
tumblerincrement(&firstlink, 1, 1, &firstlink);   // firstlink = {mantissa[0]=2, mantissa[1]=1} = 2.1

doretrievedocvspan(taskptr, docisaptr, &vspan);
tumbleradd(&vspan.stream, &vspan.width, &vspanreach);   // end-of-content
if (tumblercmp(&vspanreach, &firstlink) == LESS)
    movetumbler(&firstlink, vsaptr);    // use 2.1 if document content ends before 2.1
else
    movetumbler(&vspanreach, vsaptr);   // otherwise place after existing content
```

**Enforced placement**: The link's virtual home in the containing document is `max(2.1, end_of_document_content)`. The floor of `2.1` is hardcoded — links cannot be placed below virtual address 2.1, keeping them from colliding with text content at V=1.x.

The link ISA span is then installed into the document POOM at `linkvsa` via `docopy` [do1.c:212].

---

### Step 4: V→I Conversion of Endset Specsets — `specset2sporglset` / `vspanset2sporglset` [sporgl.c:14–65]

```c
// sporgl.c:47–58
for (; vspanset; vspanset = vspanset->next) {
    vspanset2ispanset(taskptr, orgl, vspanset, &ispanset);   // V → permascroll
    sporglset->sporgladdress = *docisa;                        // home document
    sporglset->sporglorigin  = ispanset->stream;              // permascroll start
    sporglset->sporglwidth   = ispanset->width;               // permascroll width
}
```

The user-supplied `fromspecset` / `tospecset` / `threespecset` (virtual spans in document X) are walked through the granf via `vspanset2ispanset` to produce permascroll `{origin, width}` pairs. **These permascroll addresses are for content that was allocated before the link** — they are strictly earlier in the allocator's emission sequence than the link's own ISA.

---

### Step 5: Fixed Endset V-Positions — `setlinkvsas` [do2.c:169–183]

```c
tumblerclear(fromvsaptr);
tumblerincrement(fromvsaptr, 0, 1, fromvsaptr);   // → mantissa[0]=1 → V=1
tumblerincrement(fromvsaptr, 1, 1, fromvsaptr);   // → mantissa[1]+=1 → V=1.1

tumblerclear(tovsaptr);
tumblerincrement(tovsaptr, 0, 2, tovsaptr);       // → V=2
tumblerincrement(tovsaptr, 1, 1, tovsaptr);       // → V=2.1

tumblerclear(threevsaptr);
tumblerincrement(threevsaptr, 0, 3, threevsaptr); // → V=3
tumblerincrement(threevsaptr, 1, 1, threevsaptr); // → V=3.1
```

**Enforced placement**: Every link's internal POOM is partitioned at hardcoded addresses:

| Endset | V-position in link's own POOM |
|--------|-------------------------------|
| from   | 1.1                           |
| to     | 2.1                           |
| three  | 3.1                           |

These are absolute, invariant positions. No matter how many links exist, or what the permascroll addresses of the referenced content are, the internal layout is always the same.

---

### Step 6: Spanf Registration — `insertspanf` [spanf1.c:15–54]

`insertendsetsinspanf` [do2.c:116–128] calls `insertspanf` once per endset type, passing `LINKFROMSPAN=1`, `LINKTOSPAN=2`, `LINKTHREESPAN=3` [xanadu.h:36–38]:

```c
// spanf1.c:22–51
prefixtumbler(isaptr, spantype, &crumorigin.dsas[ORGLRANGE]);
tumblerclear(&crumwidth.dsas[ORGLRANGE]);           // ORGL width = 0

// for SPORGLID items:
movetumbler(&sporgl->sporglorigin, &lstream);       // permascroll start
movetumbler(&sporgl->sporglwidth, &lwidth);         // permascroll width
movetumbler(&lstream, &crumorigin.dsas[SPANRANGE]);
movetumbler(&lwidth, &crumwidth.dsas[SPANRANGE]);

insertnd(taskptr, (typecuc*)spanfptr, &crumorigin, &crumwidth, &linfo, SPANRANGE);
```

`prefixtumbler(linkISA, spantype, result)` [tumble.c:641–651]:

```c
temp1.mantissa[0] = bint;    // spantype = 1, 2, or 3
temp2 = *linkISA;
if (!iszerotumbler(&temp2))
    temp2.exp -= 1;           // shift linkISA one level deeper
tumbleradd(&temp1, &temp2, cptr);  // result = spantype.linkISA
```

**Spanf entry structure for each endset:**

| Dimension | Start | Width |
|-----------|-------|-------|
| ORGL (link axis) | `spantype.linkISA` — e.g., `1.L` for from-endset of link L | **0** — the link is a point, not a range, in this dimension |
| SPAN (content axis) | permascroll origin of referenced content | permascroll width of referenced content |

The ORGL width being zero is significant: the spanf stores each endset as a point-reference to the link, not a range. Retrieval searches within the ORGL range `[spantype, spantype+1)` to collect all links of a given endset type intersecting a query span.

During `retrieveendsetsfromspanf` [spanf1.c:210–217]:

```c
fromspace.stream.mantissa[0] = LINKFROMSPAN;   // = 1
fromspace.width.mantissa[0] = 1;               // range [1, 2) in ORGL
```

This sweeps all orgl keys in `[1, 2)` — all from-endsets of all links in the spanf — filtered by overlap with the queried content span.

---

### Placement Summary: Relation to the Allocator's Emission Sequence

The implementation enforces a strict temporal/positional asymmetry:

1. **Endset content spans** (`sporglorigin`, `sporglwidth`) — reference permascroll addresses that were **emitted earlier** than the link's own ISA. They are the existing content the link is annotating.

2. **Link ISA** — the allocator's **most recently emitted** address at link-creation time. Its span `start = linkISA`, `width = 1 at depth (tumblerlength−1)` occupies exactly one new slot in the allocator sequence.

3. **Spanf ORGL key** = `spantype.linkISA` — the link ISA is prefixed with its endset type number (1, 2, 3). The ORGL width is zero: the link contributes no "span" in the orgl dimension, only a point lookup key.

4. **Spanf SPAN key** — permascroll `{origin, width}` of the referenced content; always older in emission sequence than the link ISA.

5. **Link's document virtual position** — hardcoded floor of V=2.1, enforced by comparing against `end_of_document_content`. Links are always at V ≥ 2.1 in the hosting document.

6. **Link's internal endset positions** — hardcoded at V=1.1, 2.1, 3.1 within the link's own POOM regardless of permascroll topology.

The allocator's emission sequence thus flows: existing content ISAs → link ISA → nothing from the endset construction itself. The link always closes its permascroll slot after the content it references.
