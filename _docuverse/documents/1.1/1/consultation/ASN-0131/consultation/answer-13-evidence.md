## Question 13 [evidence]

> What overlap relationship must a returned endset bear to the queried region — must its I-span merely intersect the region's I-spans, or must it be wholly contained — and is a partially overlapping endset returned in full or clipped to the region boundary?

## KB Synthesis

## Endset Overlap Semantics in RETRIEVEENDSETS

Two separate questions are embedded here: (1) the discovery threshold (intersect vs. contain), and (2) what portion of the matching endset is returned (full vs. clipped).

### Discovery threshold: intersection is sufficient

The spanfilade search in `retrieveendsetsfromspanf()` works by converting the input specset to an I-span query (SPANRANGE restriction) and finding spanfilade entries whose stored I-spans overlap that range. A single shared I-address suffices — full containment is not required. [SS-RETRIEVE-ENDSETS] describes the operation as "discovering all link endpoints that **intersect** a content region." This is consistent with [SS-FIND-LINKS], which confirms that "partial overlap suffices — a search specset that shares even one I-address with a link endpoint will discover that link."

### Returned endset: full sporgl, not clipped

The spanfilade stores complete sporgls (I-span + provenance) inserted by `insertendsetsinspanf()` at link creation time. When `retrievesporglsetinrange()` finds a match, it returns the entire stored sporgl — not the intersection of that sporgl with the query range. [SS-LINK-ENDPOINT] (Finding 0037) states: "`retrieve_endsets` reports multiple V-spans corresponding to the **stored I-spans**, one per contiguous I-region." The word "stored" is key — the return unit is what was recorded at creation, not the query-bounded subset.

This parallels the FOLLOWLINK contract in [SS-FOLLOW-LINK]: "even when a link is found via partial I-address overlap from a transclusion, `follow_link` returns the full endpoint as it was specified at link creation time. The link returns its full source, not the subset that enabled discovery."

### The confounding effect: POOM-based silent filtering

After the spanfilade returns full stored sporgls, `linksporglset2specset()` converts each sporgl's I-addresses to V-positions by looking them up in the querying document's POOM. Any I-address with no current POOM mapping (because it was deleted, or because it never existed in that document) is **silently dropped** — no V-span is emitted for it ([INV-ITOV-FILTERING]). This can make the returned result appear smaller than the full stored sporgl, but the mechanism is POOM availability, not query-boundary clipping.

[SS-RETRIEVE-ENDSETS] also notes: "endsets are resolved in terms of the querying document's V-space, not the link's home document" — this recontextualization (looking up I-addresses in the querying document's POOM rather than the home document's) is what drives the apparently query-local result, without any explicit boundary clipping.

### Summary

| Question | Answer |
|---|---|
| Overlap required for discovery | Intersection only — one shared I-address suffices |
| What portion of endset is returned | Full stored sporgl (complete I-span from link creation) |
| What reduces the apparent result | POOM availability: I-addresses absent from querying document's current POOM are silently dropped [INV-ITOV-FILTERING] |

Relevant entries: [SS-RETRIEVE-ENDSETS], [SS-LINK-ENDPOINT], [SS-FIND-LINKS], [SS-FOLLOW-LINK], [SS-SPORGL], [INV-ITOV-FILTERING], [INT-SPORGL-LINK-INDEX].

---

## Code Exploration

Now I have all the pieces needed to answer fully. Let me compile the complete analysis.

---

## Overlap Relationship and Clipping for Returned Endsets

The answer differs between the two retrieval paths, and the distinction rests entirely on which function processes each qualifying enfilade crum after it passes the filter.

---

### The Intersection Filter — `crumqualifies2d` (`retrie.c:270–305`)

Both paths flow through `findcbcinarea2d` → `crumqualifies2d`. The position constants from `common.h:86–90` are:

```c
#define TOMYLEFT       -2
#define ONMYLEFTBORDER -1
#define THRUME          0
#define ONMYRIGHTBORDER 1
#define TOMYRIGHT       2
```

For the restriction dimension (index1, typically V or SPANRANGE), the filter is:

```c
endcmp = iszerotumbler (span1end) ? TOMYRIGHT : whereoncrum (crumptr, offset, span1end, index1);
if ( endcmp <=/*=*/ ONMYLEFTBORDER){     // retrie.c:283
    return(FALSE);
}
startcmp = whereoncrum (crumptr, offset, span1start, index1);
if( (startcmp > THRUME)){                // retrie.c:287
    return (FALSE);
}
```

- **Reject** if the query's end is at or before the crum's left border (`endcmp <= -1`, i.e., `TOMYLEFT` or `ONMYLEFTBORDER`)
- **Reject** if the query's start is at or past the crum's right border (`startcmp > 0`, i.e., `ONMYRIGHTBORDER` or `TOMYRIGHT`)
- Everything else passes

The `/*=*/` annotation on `<=` records that this was formerly `==` — it was later tightened so that the endpoint-touching case (query end exactly at crum's left border) no longer qualifies.

**This is a pure intersection test.** A crum is selected if and only if the queried region has any interior overlap with the crum's extent in index1. Containment is not required.

---

### Path A: Content Retrieval — V→I via POOM (`context2span`)

**Call chain**: `doretrievev` → `specset2ispanset` (`do2.c:14`) → `vspanset2ispanset` (`orglinks.c:397`) → `permute` (`orglinks.c:404`) → `span2spanset` (`orglinks.c:425`) → `retrieverestricted` (`retrie.c:56`) → `findcbcinarea2d` (`retrie.c:229`) → `context2span` (`context.c:176`).

After `crumqualifies2d` passes a crum, `span2spanset` calls:

```c
context2span (c, restrictionspanptr, restrictionindex, &foundspan, targindex);   // orglinks.c:443
```

`context2span` (`context.c:176–212`) applies **proportional clipping**:

```c
movetumbler (&restrictionspanptr->stream, &lowerbound);
tumbleradd (&lowerbound, &restrictionspanptr->width, &upperbound);
prologuecontextnd (context, &grasp, &reach);   // sets grasp/reach = absolute crum start/end in both dims

if (tumblercmp (&grasp.dsas[idx1], &lowerbound) == LESS) {
    // crum starts before restriction — advance idx2 start by the V overhang
    tumblerincrement (&grasp.dsas[idx2], 0, (INT)tumblerintdiff(&lowerbound, &grasp.dsas[idx1]), &grasp.dsas[idx2]);
}
if (tumblercmp (&reach.dsas[idx1], &upperbound) == GREATER) {
    // crum ends after restriction — shrink idx2 end by the V overhang
    tumblerincrement (&reach.dsas[idx2], 0, -tumblerintdiff(&reach.dsas[idx1], &upperbound), &reach.dsas[idx2]);
}
movetumbler (&grasp.dsas[idx2], &foundspanptr->stream);
tumblersub(&reach.dsas[idx2],&grasp.dsas[idx2],&foundspanptr->width);
```

Each POOM crum encodes a linear 1:1 correspondence between V-positions and I-positions. The crum is a rectangular block in V×I space with equal width in both dimensions. `context2span` exploits this to clip the returned I-span proportionally:

- If the crum covers V=[3,7] → I=[10,14] and the query is V=[4,6]:
  - Left overhang: `lowerbound(4) – grasp.V(3) = 1` → `grasp.I` advances from 10 to 11
  - Right overhang: `reach.V(7) – upperbound(6) = 1` → `reach.I` retreats from 14 to 13
  - Returned I-span: [11, 13]

**Conclusion for content retrieval**: A POOM crum need only **intersect** the queried V-region. Its returned I-span is **clipped** by `context2span` to the exact I-interval that corresponds to the overlapping portion of the V-region. The full crum I-span is never returned for a partial overlap.

---

### Path B: Link Endset Retrieval — `contextintosporgl` (`sporgl.c:205`)

**Call chain** for `doretrieveendsets`: `retrieveendsetsfromspanf` (`spanf1.c:190`) → `retrievesporglsetinrange` (`spanf1.c:237`) → `retrieverestricted` → `findcbcinarea2d` → `contextintosporgl`.

After `crumqualifies2d` passes a spanfilade crum, `retrievesporglsetinrange` calls:

```c
contextintosporgl((type2dcontext*)c, (tumbler*)NULL, sporglset, SPANRANGE);   // spanf1.c:250
```

`contextintosporgl` (`sporgl.c:205–220`):

```c
int contextintosporgl(type2dcontext *context, tumbler *linkid, typesporgl *sporglptr, INT index)
{
    sporglptr->itemid = SPORGLID;
    sporglptr->next = NULL;
    movetumbler(/*linkid*/&context->context2dinfo.homedoc, &sporglptr->sporgladdress);
    movetumbler(&context->totaloffset.dsas[index], &sporglptr->sporglorigin);    // full crum start
    ...
    movetumbler (&context->contextwid.dsas[index], &sporglptr->sporglwidth);     // full crum width
}
```

The `context->totaloffset.dsas[index]` and `context->contextwid.dsas[index]` are set from the raw crum data in `makecontextfromcbc` (`context.c:151–174`) without any restriction-based adjustment:

```c
movewisp(offsetptr, &context->totaloffset);
movewisp(&crumptr->cwid, &context->contextwid);
if (crumptr->cenftype != GRAN)
    dspadd(&context->totaloffset, &crumptr->cdsp, &context->totaloffset, (INT)crumptr->cenftype);
```

The context records the crum's absolute position and full width. `contextintosporgl` copies these verbatim into the sporgl. There is **no clipping** against the queried I-region.

The same unclipped path is followed in `link2sporglset` (`sporgl.c:83–88`) and `sporglset2linksetinrange` (`sporgl.c:259–265`), both of which also call `contextintosporgl` or simply extract `c->totaloffset.dsas[ORGLRANGE]` (a link ISA, not a span at all).

**Conclusion for endset retrieval**: The spanfilade crum must merely **intersect** the queried I-region to qualify. The returned sporgl (and hence the reconstructed V-span after `ispan2vspanset`) carries the **full I-span** of the crum as stored — it is not clipped to the query boundary. A partially overlapping link endpoint is returned in its entirety.

---

### Summary Table

| Path | Function that converts crum → result | Overlap test | Returned span |
|------|---------------------------------------|-------------|---------------|
| V→I content retrieval (`doretrievev`) | `context2span` (`context.c:176`) | Intersection | **Clipped** to query region |
| Endset retrieval (`doretrieveendsets`) | `contextintosporgl` (`sporgl.c:205`) | Intersection | **Full** crum extent |
| Link following (`dofollowlink`) | `contextintosporgl` (`sporgl.c:86`) | Intersection | **Full** crum extent |

The **intersection test** is universal — it is the same `crumqualifies2d` filter in `retrie.c:270–305` regardless of context, and the `ONMYLEFTBORDER`/`THRUME` boundary constants (`common.h:87,88`) establish that touching at exactly the left border of a crum does not constitute overlap (the `/*=*/` comment at `retrie.c:283` records that this boundary case was once passed).

The divergence is entirely in the post-filter step: `context2span` performs proportional clipping by measuring the V-overhang and adjusting the I-span symmetrically; `contextintosporgl` takes `totaloffset` and `contextwid` verbatim and does not perform any boundary adjustment at all.
