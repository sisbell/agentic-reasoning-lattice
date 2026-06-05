## Question 19 [evidence]

> After REARRANGE fragments linked content across non-contiguous V-positions, does reading the endset report multiple V-spans where a single span existed before, while the underlying I-address spans remain unchanged?

## KB Synthesis

Yes to both parts.

## I-Address Spans: Unchanged

REARRANGE modifies only `ptr->cdsp.dsas[V]` (the V-dimension displacement in each POOM crum) via `tumbleradd`. The I-address component (`dsas[I]`) is never touched [ST-REARRANGE, INV-REARRANGE-IDENTITY]. The link orgl itself stores its endsets as sporgls indexed by I-address in the spanfilade — also never modified by REARRANGE [FC-LINK-DELETE-ISOLATION, SS-THREE-LAYER-MODEL].

## Endset V-Spans: Fragment Into Multiple

FOLLOWLINK/RETRIEVEENDSETS converts I-addresses back to V-positions by querying the document's current POOM via `linksporglset2specset` → `span2spanset` → `retrieverestricted` [SS-FOLLOWLINK, INT-SPORGL-LINK-INDEX]. The conversion returns one V-span per contiguous I-address run in V-space.

Before REARRANGE, if "CD" (I-addresses i₃, i₄) occupies contiguous V-positions 1.3–1.4, the POOM returns one span. After a pivot that separates "C" and "D" to non-adjacent V-positions, the POOM walk finds i₃ at one location and i₄ at another non-contiguous location — producing two (or more) V-spans from what was a single span [EC-PIVOT-LINK-FRAGMENTATION].

The KB confirms this with a concrete case: a link on "CD" before pivot produces 2 endset spans; after `pivot(ABCDEFGH, BC↔DE)` the endsets report 4 spans (with apparent duplication), which the KB notes may reflect internal POOM fragmentation artifacts [EC-PIVOT-LINK-FRAGMENTATION, EC-MULTISPAN-LINK-DUPLICATION].

## Summary

| Layer | Before REARRANGE | After REARRANGE |
|-------|-----------------|-----------------|
| Link orgl (I-space) | Endset = {i₃, i₄} | Endset = {i₃, i₄} — unchanged |
| POOM (V-space) | i₃→1.3, i₄→1.4 (contiguous) | i₃→new_pos₁, i₄→new_pos₂ (non-adjacent) |
| Endset V-spans | One span: [1.3, width 0.2] | Multiple spans reflecting non-contiguous V-positions |

---

## Code Exploration

Now I have the complete picture. Here is the full answer:

---

## After REARRANGE: V-span Fragmentation of Link Endsets

**Yes.** After REARRANGE fragments linked content across non-contiguous V-positions, reading the endset reports multiple V-spans where a single span existed before. The underlying I-address spans are completely unchanged.

Here is the exact execution path, with citations.

---

### 1. REARRANGE modifies V-coordinates, not I-coordinates

`rearrangepm()` [orglinks.c:137–142] is the entry point:

```c
bool rearrangepm(typetask *taskptr, tumbler *docisaptr, typeorgl docorgl, typecutseq *cutseqptr)
{
    rearrangend((typecuc*)docorgl, cutseqptr, V);
    logbertmodified(docisaptr, user);
    return (TRUE);
}
```

It calls `rearrangend()` on `docorgl` (the POOM) with index `V`. It does **not** touch the global `spanf`.

Inside `rearrangend()` [edit.c:78–160]:
- Cuts the POOM at the given V-positions [edit.c:110: `makecutsnd`]
- For each child crum in section 1, 2, or 3, applies a V-offset adjustment [edit.c:125]:
  ```c
  tumbleradd (&ptr->cdsp.dsas[index], &diff[i], &ptr->cdsp.dsas[index]);
  ```
  where `index == V`. The I-dimension (`ptr->cdsp.dsas[I]`) is never touched.
- Marks crums modified [edit.c:127: `ivemodified()`]
- Recombines and splits the tree [edit.c:139–141: `recombine()`, `splitcrumupwards()`]

**Result:** The POOM now maps the same I-address ranges to different, possibly non-contiguous V-positions. The `cdsp.dsas[I]` fields of every crum are unchanged.

---

### 2. Link endsets are stored in I-space in the spanfilade

When a link is created, `insertendsetsinspanf()` [do2.c:116–128] stores endpoints:

```c
insertspanf(taskptr, spanfptr, linkisaptr, fromsporglset, LINKFROMSPAN)
insertspanf(taskptr, spanfptr, linkisaptr, tosporglset, LINKTOSPAN)
```

Inside `insertspanf()` [spanf1.c:15–54], for each sporgl:
```c
movetumbler (&lstream, &crumorigin.dsas[SPANRANGE]);   // I-address: line 49
movetumbler (&lwidth,  &crumwidth.dsas[SPANRANGE]);    // I-width:   line 50
insertnd(taskptr, (typecuc*)spanfptr, &crumorigin, &crumwidth, &linfo, SPANRANGE); // line 51
```

The ORGLRANGE dimension holds the link ISA (prefixed with span type). The SPANRANGE dimension holds the **I-address of the content** — never a V-address. A link endpoint covering one contiguous I-span at creation time is stored as exactly one spanfilade crum.

---

### 3. Endset retrieval: I-spans fetched, then dynamically converted to V-spans

`retrieveendsetsfromspanf()` [spanf1.c:190–235] calls:
```c
retrievesporglsetinrange(taskptr, sporglset, &fromspace, &fromsporglset)  // line 223
linksporglset2specset(taskptr, &docisa, fromsporglset, fromsetptr, ...)   // line 224
```

Inside `retrievesporglsetinrange()` [spanf1.c:237–267], for each sporgl:
```c
context = retrieverestricted((typecuc*)spanf, (typespan*)sporglptr, SPANRANGE,
                              whichspace, ORGLRANGE, NULL);  // line 245
```

This queries the spanfilade by I-address (SPANRANGE). The spanfilade is unmodified by REARRANGE, so it returns the same crum(s) that were inserted at link creation — one crum per I-contiguous block, with the original I-coordinates.

Each context is then turned into a sporgl [line 250: `contextintosporgl()`].

---

### 4. The I→V conversion via `permute()` reveals fragmentation

`linksporglset2specset()` ultimately reaches `ispan2vspanset()` [orglinks.c:389–393]:

```c
typevspanset *ispan2vspanset(typetask *taskptr, typeorgl orgl, typeispan *ispanptr, typevspanset *vspansetptr)
{
    return permute(taskptr, orgl, ispanptr, I, vspansetptr, V);
}
```

`permute()` [orglinks.c:404–422] iterates over each restriction span and calls `span2spanset()`. `span2spanset()` [orglinks.c:425–454] calls:

```c
context = retrieverestricted((typecuc*)orgl, restrictionspanptr, restrictionindex,
                              (typespan*)NULL, targindex, (typeisa*)NULL);  // line 435
for (c = context; c; c = c->nextcontext) {
    context2span(c, restrictionspanptr, restrictionindex, &foundspan, targindex);  // line 443
    ...
}
```

This queries the **POOM** (`orgl`) by I-address to find the corresponding V-positions. After REARRANGE the POOM contains multiple physically distinct crums for the same I-range — one per V-region the content was scattered into. `retrieverestricted()` returns one context per intersecting crum.

`context2span()` [context.c:176–212] converts each context independently into a V-span:
```c
movetumbler (&grasp.dsas[idx2], &foundspanptr->stream);
tumblersub(&reach.dsas[idx2], &grasp.dsas[idx2], &foundspanptr->width);  // lines 206–207
```

There is no merging step — each crum context becomes its own V-span.

**Note:** There is a dead `cleanupvspanlist()` function [orglinks.c:297–312 inside `#ifdef UnDEFined`] that *would* have merged adjacent spans, but it is compiled out. The live path has no merging.

---

### 5. Concrete execution summary

Suppose a link endpoint was created over content occupying I-range [I₁, I₂] at V-positions [V₁, V₂] as a single block. The spanfilade stores one crum: SPANRANGE=[I₁, I₂], ORGLRANGE=LINKFROMSPAN.

REARRANGE is called with cuts at [V₁, Vₘ, V₂] (a 3-cut swap). After execution:
- Content [I₁, Iₘ] is now at V[Vₘ, V₂]   ← previously second half
- Content [Iₘ, I₂] is now at V[V₁, Vₘ]   ← previously first half

These are now **separate POOM crums at non-adjacent V-positions**.

When `dofollow` reads the endset:
1. Spanfilade lookup (SPANRANGE=I-addr) → one sporgl covering [I₁, I₂] (unchanged)
2. `permute()` queries POOM by [I₁, I₂] → hits **two crums**, returns **two contexts**
3. `context2span()` fires twice → **two V-spans**: [Vₘ, V₂] and [V₁, Vₘ]

The returned endset has two V-spans. The stored I-span is still [I₁, I₂] — one entry in the spanfilade, unmodified.

---

### Summary

| Layer | After REARRANGE | Why |
|---|---|---|
| Spanfilade (I-addresses) | **Unchanged** | `rearrangepm()` [orglinks.c:137] never modifies `spanf` |
| POOM (V-addresses) | **Modified** | `rearrangend()` [edit.c:125] adjusts `cdsp.dsas[V]` |
| Reported endset (V-spans) | **Multiple spans** | `ispan2vspanset()` → `permute()` → one context per POOM crum → one V-span per context [orglinks.c:443, context.c:206] |

The endset is stored in I-space and converted to V-space dynamically on every retrieval. REARRANGE rewrites the POOM's V-mapping without touching the spanfilade, so the same I-span now converts to as many V-spans as the rearrangement introduced discontinuities — with no merging pass to coalesce them back.
