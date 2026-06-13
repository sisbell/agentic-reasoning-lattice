## Question 20 [evidence]

> After an INSERT or REARRANGE shifts V-positions in the queried document, do the returned endsets report the new shifted V-positions (since endsets resolve through the current POOM) while remaining the same I-identity endsets, and can a pivot fragment a single-span endset into multiple spans in the answer?

## KB Synthesis

Yes to both parts.

## Part 1: Endsets report current, shifted V-positions

Endset resolution works through the **current POOM**, so any V-position shifts from INSERT or REARRANGE are immediately reflected in returned endsets.

The mechanism is documented in [SS-FOLLOWLINK] (Finding 0048): FOLLOWLINK retrieves the endset I-addresses from the link orgl (permanent, never changing), then converts them to V-addresses by calling `linksporglset2specset` → `span2spanset` → `retrieverestricted` against the queried document's current POOM. RETRIEVEENDSETS uses the same I-to-V conversion path [SS-RETRIEVE-ENDSETS].

Because I-addresses are immutable [INV-IADDR-IMMUTABILITY] and INSERT/REARRANGE only modify V-positions in the POOM [ST-INSERT], [ST-REARRANGE], [INV-REARRANGE-IDENTITY], the endset I-addresses are the same identities throughout — but the V-positions those I-addresses map to change. The POOM lookup at query time returns the *current* V-positions.

This is confirmed explicitly in [INV-LINK-CONTENT-TRACKING] (Finding 0019):

> **V-address shifts**: When content is inserted within or before a linked region, the endset V-addresses shift to reflect the new positions:
> ```
> Before: link on "here" at V 1.7 width 0.4
> Insert: "right " at position 1.7
> After:  link reports 1.13 width 0.4
> ```

The link's I-addresses are unchanged; the V-addresses in the endset answer are freshly computed from the shifted POOM.

## Part 2: Pivot can fragment a single-span endset into multiple spans

Yes. [EC-PIVOT-LINK-FRAGMENTATION] documents this precisely:

> When linked content is rearranged via pivot, the link's endsets become fragmented into multiple spans.
>
> ```
> Before: "ABCDEFGH" — link on "CD" at V 1.3 width 0.2
> Pivot:  swap BC and DE
> After:  "ADEBCFGH" — endsets report FOUR spans:
>         - 1.2 width 0.1 (twice)
>         - 1.5 width 0.1 (twice)
> find_links returns the same link TWICE
> ```

**Why:** REARRANGE preserves I-addresses but moves their V-positions [INV-REARRANGE-IDENTITY]. After the pivot, the I-addresses for "C" and "D" — which had been at contiguous V-positions 1.3–1.4 — now sit at non-contiguous V-positions 1.5 and 1.2 respectively. When the I-to-V conversion in `linksporglset2specset` looks up those I-addresses in the POOM, it finds them scattered at separate V-regions and returns multiple V-spans.

The duplication artifact (four spans, link appearing twice in `find_links`) is noted as potentially a bug or an artifact of how the enfilade represents fragmented spans after pivot — the KB does not resolve this conclusively [EC-MULTISPAN-LINK-DUPLICATION].

The same fragmentation mechanism underlies why [ST-LINK-CREATE] / [SS-LINK-ENDPOINT] (Finding 0037) notes that a single V-span at creation time can already produce multiple I-spans in the endset when the content was assembled from multiple transclusion sources — and post-pivot fragmentation is the reverse phenomenon.

---

## Code Exploration

Now I have all the code I need. Let me trace the complete execution path.

---

## Full Analysis

### Question: After INSERT or REARRANGE shifts V-positions, do returned endsets report the new shifted V-positions while remaining the same I-identity endsets, and can a pivot fragment a single-span endset into multiple spans?

**Short answer: Yes to all three.** Here is the line-by-line proof.

---

### Part 1 — INSERT and REARRANGE mutate V-coordinates directly in the POOM

**INSERT path:**

`fns.c:84-98` → `doinsert` [`do1.c:87-123`] → `docopy` → `insertpm` [`orglinks.c:75-134`] → `insertnd` [`insertnd.c:15`].

For a POOM, `insertnd` calls `makegappm` first [`insertnd.c:53-55`]:

```c
case POOM:
    makegappm (taskptr, fullcrumptr, origin, width);
    ...
    bothertorecombine=doinsertnd(fullcrumptr,origin,width,infoptr,index);
```

Inside `makegappm` [`insertnd.c:124-172`], every child crum classified as `case 1` (crum lies entirely at V ≥ insertion point) has its V-displacement field directly incremented:

```c
case 1:  /* insertnd.c:161-163 */
    tumbleradd(&ptr->cdsp.dsas[V], &width->dsas[V], &ptr->cdsp.dsas[V]);
    ivemodified (ptr);
```

The `cdsp.dsas[V]` field of each displaced crum is mutated in place. `setwispupwards` then propagates the changed cumulative widths back to the root [`insertnd.c:56-58`]. The POOM tree now encodes the new V-layout.

**REARRANGE path:**

`fns.c:159-173` → `dorearrange` [`do1.c:34-43`] → `rearrangepm` [`orglinks.c:137-142`] → `rearrangend` [`edit.c:78-160`].

`rearrangend` classifies each bottom crum into a cut-section (0–3) and applies a pre-computed offset `diff[i]` directly to its V-displacement:

```c
case 1:  case 2:  case 3:  /* edit.c:124-127 */
    tumbleradd (&ptr->cdsp.dsas[index], &diff[i], &ptr->cdsp.dsas[index]);
    ivemodified((typecorecrum*)ptr);
```

Again the POOM crums are mutated in place. Their `cdsp.dsas[V]` now reflects post-rearrange V-positions.

---

### Part 2 — Endsets are stored as I-spans (permascroll addresses), never touched by INSERT/REARRANGE

**Link creation:**

`docreatelink` [`do1.c:195-220`]:

```c
specset2sporglset (taskptr, fromspecset, &fromsporglset, NOBERTREQUIRED)
...
insertendsetsinorgl (taskptr, linkisaptr, link, &fromvsa, fromsporglset, ...)
insertendsetsinspanf (taskptr, spanf, linkisaptr, fromsporglset, ...)
```

`specset2sporglset` [`sporgl.c:14-33`] → `vspanset2sporglset` [`sporgl.c:35-65`]:

```c
(void) vspanset2ispanset (taskptr, orgl, vspanset, &ispanset);
for (; ispanset; ispanset = ispanset->next) {
    sporglset = (typesporgl *) taskalloc (taskptr, sizeof(typesporgl));
    ...
    movetumbler (docisa, &sporglset->sporgladdress);     /* document ISA */
    movetumbler(&ispanset->stream, &sporglset->sporglorigin);  /* I-start */
    movetumbler (&ispanset->width, &sporglset->sporglwidth);   /* I-width */
```

The V-span from the original specset is immediately converted to an I-span (via `vspanset2ispanset` → `permute(V→I)`) and the I-span is what goes into the sporgl. Then `insertpm` [`orglinks.c:75-134`] plants a 2D crum in the link's POOM with:
- V-coordinate = fixed VSA (`fromvsa` = `1.1` for FROM, `2.1` for TO, per `setlinkvsas` [`do2.c:169-183`])
- I-coordinate = the I-span from the sporgl
- `linfo.homedoc` = the document that owns the permascroll content

Neither `makegappm` (INSERT) nor `rearrangend` (REARRANGE) on the **target document** touches the link's POOM. The I-spans stored there are permanent permascroll addresses.

---

### Part 3 — Following a link reads V-positions from the *current* POOM

**`followlink` path:**

`fns.c:114-127` → `dofollowlink` [`do1.c:223-232`]:

```c
bool dofollowlink(typetask *taskptr, typeisa *linkisaptr, typespecset *specsetptr, INT whichend)
{
  typesporglset sporglset;
    return (
       link2sporglset (taskptr, linkisaptr, &sporglset, whichend, NOBERTREQUIRED)
    && linksporglset2specset (taskptr, &((typesporgl *)sporglset)->sporgladdress,
                              sporglset, specsetptr, NOBERTREQUIRED));
}
```

**Step 1 — Extract the I-span from the link's POOM:**

`link2sporglset` [`sporgl.c:67-95`] opens the link's POOM, queries it at the endset's V-slot (`whichend`), and calls `contextintosporgl` with index `I`:

```c
contextintosporgl ((type2dcontext*)c, (tumbler*)NULL, sporglptr, I);
```

`contextintosporgl` [`sporgl.c:205-220`]:

```c
movetumbler(/*linkid*/&context->context2dinfo.homedoc, &sporglptr->sporgladdress);
movetumbler(&context->totaloffset.dsas[I], &sporglptr->sporglorigin);   /* I-start */
movetumbler (&context->contextwid.dsas[I], &sporglptr->sporglwidth);    /* I-width */
```

The `sporgladdress` is the home document (target of the endset). The `sporglorigin`/`sporglwidth` are the stored I-span — unchanged since link creation.

**Step 2 — Convert I-span to V-spans using the *current* POOM:**

`linksporglset2specset` [`sporgl.c:97-123`] → `linksporglset2vspec` [`sporgl.c:127-137`] → `sporglset2vspanset` [`sporgl.c:141-176`]:

```c
(void) findorgl (taskptr, granf, homedoc/*&sporglptr->sporgladdress*/, &orgl, type);
...
movetumbler (&sporglptr->sporglorigin, &ispan.stream);
movetumbler (&sporglptr->sporglwidth, &ispan.width);
vspansetptr = ispan2vspanset (taskptr, orgl, &ispan, vspansetptr);
```

`findorgl` opens the **target document's current POOM**. `ispan2vspanset` → `permute(taskptr, orgl, ispanptr, I, vspansetptr, V)` [`orglinks.c:389-394`] → `span2spanset` [`orglinks.c:425-453`] → `retrieverestricted` → `findcbcinarea2d` [`retrie.c:229-268`].

`findcbcinarea2d` walks the POOM tree checking `crumqualifies2d` for each crum. The context is built by `makecontextfromcbc` [`context.c:151-174`]:

```c
if (crumptr->cenftype != GRAN)
    dspadd(&context->totaloffset, &crumptr->cdsp, &context->totaloffset, (INT)crumptr->cenftype);
```

`dspadd` accumulates each crum's `cdsp` (including `cdsp.dsas[V]`) into `totaloffset`. Because `makegappm`/`rearrangend` mutated those `cdsp.dsas[V]` fields, this accumulation picks up the **current** post-mutation V-coordinates.

`context2span` [`context.c:176-212`] then computes the final V-span:

```c
prologuecontextnd (context, &grasp, &reach);
/* clip grasp/reach to the I-span restriction ... */
movetumbler (&grasp.dsas[idx2], &foundspanptr->stream);   /* idx2 = V */
tumblersub(&reach.dsas[idx2], &grasp.dsas[idx2], &foundspanptr->width);
```

`grasp.dsas[V]` and `reach.dsas[V]` are the post-mutation V-positions. **The returned V-span reflects the current document state.**

The same path applies to `retrieveendsets` (`fns.c:350-362` → `doretrieveendsets` [`do1.c:369-374`] → `retrieveendsetsfromspanf` [`spanf1.c:190-235`]), which looks up I-spans in the spanfilade then converts them to V-spans via `linksporglset2specset` → `sporglset2vspanset` against the current POOM.

---

### Part 4 — Pivot fragmentation: a single I-span can yield multiple V-spans

The `retrieverestricted` call inside `span2spanset` [`orglinks.c:435`] returns a **linked list** of contexts:

```c
context = retrieverestricted((typecuc*)orgl, restrictionspanptr, restrictionindex,
                             (typespan*)NULL, targindex, (typeisa*)NULL);
for (c = context; c; c = c->nextcontext) {
    context2span (c, restrictionspanptr, restrictionindex, &foundspan, targindex);
    nextptr = (typespan *)onitemlist (taskptr, (typeitem*)&foundspan,
                                     (typeitemset*)targspansetptr);
}
```

`findcbcinarea2d` [`retrie.c:229-268`] adds a context entry for every bottom crum that satisfies `crumqualifies2d` — there is no constraint that the result must be a single contiguous span.

**Fragmentation scenario (INSERT):**

Suppose endset I-span = [3..7) originally maps to a single V-region [3..7). An INSERT at V=5 of width 3 does the following via `makegappm`:

1. `makecutsnd` places cuts at V=5 and at `findaddressofsecondcutforinsert(5)` [`insertnd.c:174-183`], which splits the crum spanning V=[1..11) into sub-crums.
2. `case 1` shifts the sub-crum covering original V=[5..11) (I=[5..11)) by `+3` → V=[8..14).

After INSERT the POOM has:
- Crum A: I=[1..5), V=[1..5) — original content before insertion point
- Crum B: I=[11..14), V=[5..8) — newly inserted text
- Crum C: I=[5..11), V=[8..14) — original content after insertion point

For I-span [3..7): `findcbcinarea2d` finds Crum A (I=[1..5) overlaps [3..5)) **and** Crum C (I=[5..11) overlaps [5..7)). Two contexts are returned. `context2span` clips each to the I-restriction:

- From Crum A: V-span [3..5)
- From Crum C: V-span [8..10)

A single stored I-span yields two V-spans. The endset has been **fragmented by the pivot** (the insertion point).

**Fragmentation scenario (REARRANGE):**

`rearrangend` [`edit.c:78-160`] inserts knife cuts at the rearrange positions, then applies `diff[i]` offsets to each section. If a REARRANGE cut V=p falls inside the V-range covered by the endset's I-span, `makecutsnd` splits the crum at that point (`splitcrumseq`/`splitcrumnd`), and the two resulting sub-crums get different `diff[i]` offsets → non-contiguous V-spans from a single I-span.

---

### Summary

| Claim | Verdict | Key code |
|---|---|---|
| Endsets store I-spans (permascroll), not V-spans | **Confirmed** | `vspanset2sporglset` [`sporgl.c:35-65`], `contextintosporgl` with `I` index [`sporgl.c:205-220`] |
| INSERT mutates POOM V-coordinates in-place | **Confirmed** | `makegappm` case 1 [`insertnd.c:161-163`] |
| REARRANGE mutates POOM V-coordinates in-place | **Confirmed** | `rearrangend` cases 1–3 [`edit.c:124-127`] |
| Returned V-positions are computed from the *current* POOM | **Confirmed** | `sporglset2vspanset` opens current POOM [`sporgl.c:152`]; `makecontextfromcbc` accumulates current `cdsp` [`context.c:167`]; `context2span` returns current V-coordinates [`context.c:206-207`] |
| Stored I-identity (permascroll address) is unchanged | **Confirmed** | `sporglorigin`/`sporglwidth` in link's POOM crums are never modified by target-document edits |
| A pivot can fragment a single I-span into multiple V-spans | **Confirmed** | `span2spanset` loops over *all* contexts returned by `retrieverestricted` [`orglinks.c:439-444`]; `findcbcinarea2d` emits one context per qualifying bottom crum [`retrie.c:260-264`]; a pivot split creates two qualifying crums for one I-span |
