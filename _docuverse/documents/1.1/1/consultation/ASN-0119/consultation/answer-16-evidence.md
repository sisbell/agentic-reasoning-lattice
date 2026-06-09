## Question 16 [evidence]

> When a single endset spans a cut boundary so that part lies in `[a,b)` and part in the untouched middle `[b,c)`, does REARRANGE fragment that endset into multiple non-contiguous V-spans on subsequent resolution?

## KB Synthesis

**Yes, REARRANGE fragments that endset into multiple non-contiguous V-spans on subsequent resolution.** This is directly observed and mechanically explained by the KB.

## Direct Evidence

[EC-PIVOT-LINK-FRAGMENTATION] (Finding 0019) documents the exact phenomenon:

> When linked content is rearranged via pivot, the link's endsets become fragmented into multiple spans. Example: link on "CD" at V 1.3 width 0.2, after pivot swapping BC and DE, endsets report **four spans** — and the link appears duplicated in `find_links` results.

## Mechanism

The fragmentation is a consequence of the I/V architecture:

1. **REARRANGE mutates only V-addresses** [ST-REARRANGE, INV-REARRANGE-IDENTITY, Finding 0056]: `rearrangend()` applies `tumbleradd` to POOM displacements (`cdsp.dsas[V]`). I-addresses are never touched. The endset's I-address range `[α_a, α_c)` remains unchanged in the link orgl.

2. **Content straddles the cut**: The endset covers `[a, c)` with cut at `b`. After pivot:
   - Region `[a, b)` → displaced by `diff[1]` → new V-position X
   - Region `[b, c)` → displaced by `diff[2]` → new V-position Y (different, non-adjacent to X)

3. **Resolution queries the current POOM** [SS-FOLLOWLINK, Finding 0048]: FOLLOWLINK and RETRIEVEENDSETS both call `linksporglset2specset()` → `span2spanset()` → `retrieverestricted()` to convert the endset's I-addresses to V-addresses. The POOM now maps what was one contiguous I-range to two disjoint V-ranges.

4. **One V-span per contiguous I-region** [SS-SPORGL, ST-LINK-CREATE / Finding 0037]: `vspanset2sporglset` (and the reverse path) produces one sporgl/span per contiguous I-address region. Since the formerly unified I-range now resolves to two separated V-positions, two V-spans are returned.

## The Middle Region Case Specifically

For content in the untouched middle `[b, c)` with `diff[2]` potentially negative (as in a pivot where region 2 shifts backward), the displacement is valid as long as `strongsub`'s exponent guard doesn't suppress it [SS-TUMBLER, Finding 0055]. Within the same subspace and exponent level, both halves do shift, and they shift by *different amounts* — guaranteeing non-contiguity post-rearrangement.

## Summary

| Before REARRANGE | After REARRANGE |
|---|---|
| Endset I-range: `[α_a, α_c)` (one contiguous range) | I-range: unchanged `[α_a, α_c)` |
| V-mapping: one contiguous span `[a, c)` | V-mapping: two disjoint spans at X and Y |
| FOLLOWLINK returns: 1 V-span | FOLLOWLINK returns: 2 V-spans (fragmented) |

The duplication artifact noted in [EC-PIVOT-LINK-FRAGMENTATION] (same link appearing twice in `find_links`) stems from the same cause: the fragmented I-spans each independently match the search, producing redundant link results.

---

## Code Exploration

I now have everything needed. Here is the complete answer.

---

## Answer

**Yes. REARRANGE physically splits the POOM crum at the cut boundary, and subsequent I→V resolution via `ispan2vspanset` finds both halves separately, yielding two non-contiguous V-spans.**

Here is the complete chain, with every claim cited to source.

---

### 1. Where endsets are stored — I-spans, not V-spans

`docreatelink` (`do1.c:195`) converts V-spec endpoints to sporgl (I-space) form and stores them in the spanfilade:

```c
// do1.c:214–220
&& specset2sporglset (taskptr, fromspecset, &fromsporglset, NOBERTREQUIRED)
...
&& insertendsetsinspanf (taskptr, spanf, linkisaptr, fromsporglset, tosporglset, threesporglset)
```

`insertspanf` (`spanf1.c:15`) writes the **I-span** (`sporglorigin` / `sporglwidth`) into `SPANRANGE` of the spanfilade crum:

```c
// spanf1.c:31–34
movetumbler (&((typesporgl *)sporglset)->sporglorigin, &lstream);
movetumbler (&((typesporgl *)sporglset)->sporglwidth, &lwidth);
...
movetumbler (&lstream, &crumorigin.dsas[SPANRANGE]);
```

The spanfilade is **not touched** by REARRANGE. Only the POOM (orglink enfilade) changes.

---

### 2. REARRANGE operates exclusively on the POOM

`dorearrange` (`do1.c:34`) → `rearrangepm` (`orglinks.c:137`) → `rearrangend(docorgl, cutseqptr, V)` (`edit.c:78`):

```c
// orglinks.c:137–142
bool rearrangepm(typetask *taskptr, tumbler *docisaptr, typeorgl docorgl, typecutseq *cutseqptr)
{
    rearrangend((typecuc*)docorgl, cutseqptr, V);
    ...
}
```

Dimension is always `V`. The spanfilade (`spanf`) is never touched.

---

### 3. `makecutsnd` splits every straddling crum before classification

`rearrangend` (`edit.c:110`) calls `makecutsnd` first:

```c
// edit.c:110–111
makecutsnd (fullcrumptr, &knives);
newfindintersectionnd (fullcrumptr, &knives, &father, &foffset);
```

Inside `makecutsnd` (`ndcuts.c:15`) → `makecutsdownnd` (`ndcuts.c:33`) → `makecutsbackuptohere` (`ndcuts.c:69`):

```c
// ndcuts.c:77–90  (height == 0, i.e. bottom crum)
for (i = 0; i < knives->nblades; i++) {
    if (whereoncrum((typecorecrum*)ptr, offset, &knives->blades[i], knives->dimension) == THRUME) {
        new = (typecuc *)createcrum((INT)ptr->height,(INT)ptr->cenftype);
        ...
        slicecbcpm((typecorecrum*)ptr, offset, (typecorecrum*)new, &knives->blades[i], knives->dimension);
```

`THRUME == 0` (`common.h:88`) means the knife lies strictly inside this crum. Every such crum is immediately passed to `slicecbcpm`.

By the time the section-classification loop in `rearrangend` runs, no straddling crums remain. This is why `THRUME` is a fatal error there:

```c
// edit.c:116–121
case -1:
    gerror ("rearrangend can't classify crum\n");
```

---

### 4. `slicecbcpm` splits the crum at the cut, preserving I-span coverage

`slicecbcpm` (`ndcuts.c:373`) computes `localcut = cut - grasp[V]` — the V-offset of the knife within the crum — and applies it across **all dimensions**:

```c
// ndcuts.c:438–448
movewisp (&ptr->cwid, &newwid);
for (i = 0; i < widsize(enftype); i++) { /* I really don't understand this loop */
    newwid.dsas[i].mantissa[0] = localcut.mantissa[0];
    tumblerjustify (&newwid.dsas[i]);
}
locksubtract ((tumbler*)&ptr->cwid, (tumbler*)&newwid, (tumbler*)&new->cwid, (unsigned)widsize(enftype));
movewisp (&newwid, &ptr->cwid);
dspadd (&ptr->cdsp, &ptr->cwid, &new->cdsp, enftype);
move2dinfo (&((type2dcbc *)ptr)->c2dinfo, &((type2dcbc *)new)->c2dinfo);
adopt(new, RIGHTBRO, ptr);
```

Gregory's own comment — "I really don't understand this loop" — is on the key line. The loop copies `localcut.mantissa[0]` into every dimension's mantissa, meaning the I-dimension is cut at the **same relative offset** as the V-dimension. The result:

- `ptr` (left half): V-span `[a, b)` → I-span `[ia, ia+Δ)`
- `new` (right half): V-span `[b, c)` → I-span `[ia+Δ, ic)`

Both halves inherit the same `c2dinfo.homedoc` (the orglink address), so they remain valid POOM crums.

---

### 5. The two halves receive different displacements

`rearrangecutsectionnd` (`edit.c:191`) classifies each crum by section:

```c
// edit.c:195–203
for (i = knives->nblades -1; i >= 0 ; --i) {
    cmp = whereoncrum (ptr, offset, &knives->blades[i], knives->dimension);
    if (cmp == THRUME) {
        return (-1);  // impossible now, fatal if hit
    } else if (cmp <= ONMYLEFTBORDER) {
        return (i+1);
    }
}
return (0);
```

And `rearrangend` (`edit.c:113–136`) applies the computed offset `diff[i]` to the V-displacement of section 1, 2, or 3 crums only:

```c
// edit.c:124–127
case 1:  case 2:  case 3:  /* 3 only moves in 4 cuts */
    tumbleradd (&ptr->cdsp.dsas[index], &diff[i], &ptr->cdsp.dsas[index]);
    ivemodified((typecorecrum*)ptr);
    break;
```

The left half (section 1, `[a,b)` in V) gets `diff[1]` added to `cdsp.dsas[V]`. The right half (`[b,c)` in the untouched middle, section 0 or 2) gets nothing. After REARRANGE:

- Left half: V-span at `a + diff[1]`, I-span `[ia, ia+Δ)`
- Right half: V-span unchanged at `b`, I-span `[ia+Δ, ic)`

These two V-spans are non-contiguous (unless `diff[1] = 0`, which is never the case for a real rearrangement).

---

### 6. Resolution via `ispan2vspanset` finds both halves

When a follow or endset retrieval calls `ispan2vspanset` (`orglinks.c:389`) → `permute` → `span2spanset` (`orglinks.c:425`) → `retrieverestricted` (`retrie.c:56`) → `findcbcinarea2d` (`retrie.c:229`):

```c
// retrie.c:252–265
for (; crumptr; crumptr = getrightbro (crumptr)) {
    if (!crumqualifies2d (crumptr, offsetptr, span1start, span1end, index1, ...)) {
        continue;
    }
    if (crumptr->height != 0) {
        ...findcbcinarea2d(findleftson, ...)...
    } else {
        context = makecontextfromcbc ((typecbc*)crumptr, (typewid*)offsetptr);
        incontextlistnd (headptr, context, index1);
    }
}
```

`crumqualifies2d` (`retrie.c:270`) checks whether the crum's I-span intersects the query I-span `[ia, ic)`:

```c
// retrie.c:282–291
endcmp = iszerotumbler (span1end) ? TOMYRIGHT : whereoncrum (crumptr, offset, span1end, index1);
if (endcmp <= ONMYLEFTBORDER) { return(FALSE); }
startcmp = whereoncrum (crumptr, offset, span1start, index1);
if (startcmp > THRUME) { return (FALSE); }
```

Both POOM halves intersect `[ia, ic)`, so both qualify. Each is added to the context list via `incontextlistnd`. `span2spanset` then calls `context2span` on each, extracting the V-span at the crum's current V-displacement.

The result returned to the caller is **two V-span entries**: `[a+diff[1], b+diff[1])` and `[b, c)`. These are non-contiguous.

---

### Summary

| Step | Location | What happens |
|------|----------|--------------|
| 1. Endset created | `do1.c:219`, `spanf1.c:49` | I-span stored in spanfilade SPANRANGE; spanfilade never modified by rearrange |
| 2. REARRANGE called | `orglinks.c:139` | `rearrangend` on POOM with `index=V` |
| 3. Cut at `b` | `ndcuts.c:79–89` | `makecutsbackuptohere` detects `THRUME`, calls `slicecbcpm` |
| 4. POOM crum split | `ndcuts.c:373–449` | Left half `[a,b)`, right half `[b,c)`, same I-span coverage shared proportionally |
| 5. Left half displaced | `edit.c:124–127` | `diff[1]` added to `cdsp.dsas[V]` of left half only |
| 6. Resolution | `retrie.c:252–265` | `findcbcinarea2d` finds both halves; two non-contiguous V-spans returned |

**The endset's I-span in the spanfilade is never fragmented.** The fragmentation is a V-space artifact: the POOM now maps that single I-span range to two disjoint V-spans, and every I→V lookup (`ispan2vspanset`, `permute`, `span2spanset`) will reflect this until the document is rearranged again or the link is re-created.

One further structural note: `whereoncrum` (`retrie.c:345`) for `POOM` type computes `left = offset.dsas[index] + ptr->cdsp.dsas[index]` and `right = left + ptr->cwid.dsas[index]` — strictly over the **specified** `index` dimension only. So `THRUME` detection, classification, and displacement are all cleanly separated per-dimension. There is no cross-dimension confusion: the V-dimension rearrangement does not corrupt I-span addressing.
