## Question 16 [evidence]

> Does the correspondence computation in `correspond.c` operate on the granfilade I-address dimension, or does it consult the spanfilade's 2D index keyed by (I-span, document)?

## KB Synthesis

## `correspond.c` uses the granfilade I-address dimension, not the spanfilade.

The correspondence computation works as follows:

1. **V→I conversion via granfilade**: Both documents' V-spans are converted to sporgls — intermediate representations carrying `(I-address, width, source_doc)` — by querying each document's POOM (which is stored in the granfilade). This is the `vspanset2sporglset` path. [INT-SPORGL-VERSION-COMPARE], [SS-SPORGL]

2. **I-address intersection**: `correspond.c` implements a nested loop that intersects the two sporgl sets by `sporglorigin` field. Any overlapping I-address ranges indicate content with common origin. [SS-COMPARE-VERSIONS]

3. **Map back to V-spans**: Matching I-spans are resolved back to V-positions in each document via the POOM. [ST-COMPARE-VERSIONS]

The spanfilade is not consulted. [FC-CONTENT-SPANF-ISOLATION] establishes the isolation boundary: the spanfilade is a link search index mapping I-addresses to link orgls (and DOCISPAN entries mapping I-addresses to documents for `find_documents`), while content comparison accesses only the granfilade. [SS-DUAL-ENFILADE], [SS-DOCISPAN]

The spanfilade's 2D structure (ORGLRANGE × SPANRANGE) is used by `find_links` and `retrieve_endsets` only. [INT-SPORGL-LINK-INDEX]

This design also explains why `compare_versions` crashes when given link-subspace spans [EC-COMPARE-VERSIONS-LINK-CRASH]: the granfilade V→I conversion for `2.x` positions returns link orgl ISAs, which are in a different I-address space from permascroll addresses, so the intersection arithmetic is semantically undefined and the nested loop in `correspond.c` hits an unhandled case.

---

## Code Exploration

I have traced the complete call chain. Here is the full answer.

---

## Answer

The correspondence computation in `correspond.c` is a **two-phase operation**: it first uses the granfilade's 1D I-address dimension to resolve a per-document orgl, and then uses that orgl's 2D POOM index (keyed by I and V simultaneously) for the actual span conversion. It does **not** consult a shared spanfilade index keyed by (I-span, document). Here is the full trace.

---

### Phase 1 — Granfilade lookup by document I-address

The entry point is `restrictvspecsetovercommonispans` [`correspond.c:18`], which loops over all `(ispanset × specset)` pairs. For each vspec it calls:

```c
// correspond.c:67
if(!findorgl(taskptr, granf, &((typevspec *)specset)->docisa, &versionorgl, READBERT))
```

`findorgl` is in `granf1.c:17`. After checking access control via `checkforopen`, it calls:

```c
// granf2.c:34
context = retrievecrums((typecuc*)fullcrumptr, address, WIDTH);
```

`retrievecrums` uses `cenftype == GRAN` (`retrie.c:20-21`) to dispatch `findcbcseqcrum`, which walks the granfilade tree on the `WIDTH` dimension (defined as index 0 in `wisp.h:12`). This is a **1D sequential search**. The granfilade crum at the matched I-address stores an `orglptr` of type `typecuc*` (a POOM enfilade root):

```c
// granf2.c:62
ret = context->corecrum->cinfo.granstuff.orglstuff.orglptr;
```

So after Phase 1, `versionorgl` is the root of the **per-document POOM**, not anything from a shared spanfilade.

---

### Phase 2 — POOM 2D lookup by (I-span → V-span)

Back in `correspond.c:74`:

```c
if(ispan2vspanset(taskptr, versionorgl, ispanset, &docvspanset))
```

`ispan2vspanset` is `orglinks.c:389-394`:

```c
return permute(taskptr, orgl, ispanptr, I, vspansetptr, V);
```

`I = 0`, `V = 1` per `wisp.h:19-20`. `permute` (`orglinks.c:404`) loops over each ispan and calls `span2spanset` (`orglinks.c:425`), which calls:

```c
// orglinks.c:435
context = retrieverestricted((typecuc*)orgl, restrictionspanptr, restrictionindex, (typespan*)NULL, targindex, (typeisa*)NULL);
```

`retrieverestricted` (`retrie.c:56`) sets up span bounds and calls `retrieveinarea` (`retrie.c:87`), which dispatches on `cenftype`:

```c
// retrie.c:95-98
case SPAN:
case POOM:
    findcbcinarea2d(... span1start, span1end, index1, span2start, span2end, index2 ...)
```

`cenftype == POOM = 2` per `enf.h:13`. `findcbcinarea2d` (`retrie.c:229`) recursively walks the POOM tree and at every node calls `crumqualifies2d` (`retrie.c:270`), which checks the crum against **both** dimensions:

```c
// retrie.c:282-299
endcmp = whereoncrum(crumptr, offset, span1end, index1);   // I-dimension check
...
startcmp = whereoncrum(crumptr, offset, span1start, index1);
...
endcmp = whereoncrum(crumptr, offset, span2end, index2);   // V-dimension check
...
startcmp = whereoncrum(crumptr, offset, span2start, index2);
```

For the `ispan2vspanset` call, `index1 = I = 0` and `index2 = V = 1`. The POOM crums store `cdsp.dsas[I]` (I-offset) and `cdsp.dsas[V]` (V-offset) per `enf.h:47-48`. So the 2D area search qualifies crums whose **I-extent intersects the input ispan** and whose **V-extent intersects any V range** (span2start/end are zero, effectively unbounded, since `span2ptr == NULL` at `retrie.c:70-76`).

Once bottom crums are found, `context2span` (`context.c:176`) does the geometric projection: it clips the crum's (I, V) window to the input ispan on `idx1=I` and reads out the corresponding `idx2=V` extent:

```c
// context.c:194
tumblerincrement(&grasp.dsas[idx2], 0, (INT) tumblerintdiff(&lowerbound, &grasp.dsas[idx1]), &grasp.dsas[idx2]);
// context.c:206-207
movetumbler(&grasp.dsas[idx2], &foundspanptr->stream);
tumblersub(&reach.dsas[idx2], &grasp.dsas[idx2], &foundspanptr->width);
```

This is standard permutation-matrix projection: find the POOM cells that contain the requested I-addresses, clip the I-edges to the query boundary, and read off the proportional V-addresses.

---

### What about a (I-span, document) shared index?

The `type2dbottomcruminfo` struct (`wisp.h:107-110`) has a `homedoc` tumbler field that could support filtering by document inside a shared POOM. `crumqualifies2d` at `retrie.c:274` does check `infoptr->homedoc` — but only when `infoptr != NULL`. In every call from `span2spanset`, `docisaptr` is passed as `NULL` (`orglinks.c:435`), so `infoptr` is always `NULL` at `retrie.c:81`. The distribution build even hard-errors on a non-NULL `infoptr`:

```c
// retrie.c:249-250
if (infoptr)
    gerror("!NULL");
```

This means the homedoc filtering path in `crumqualifies2d` is **dead code** in the current build. There is no shared (I-span, document) 2D spanfilade being consulted. Each document gets its own POOM, resolved individually through the granfilade.

---

### The spanfilade confusion

The code has three enfilade types (`enf.h:12-14`):

| Constant | Value | Used for |
|---|---|---|
| `GRAN` | 1 | Granfilade (1D, WIDTH dim): document ISA → orgl |
| `POOM` | 2 | Permutation matrix (2D, I+V dims): I-address ↔ V-address |
| `SPAN` | 3 | Spanfilade (2D, ORGLRANGE+SPANRANGE): link endpoint indexing |

What the question calls the "spanfilade's 2D index keyed by (I-span, document)" does not exist as an active data structure. The POOM is the 2D (I, V) index, but it is per-document (keyed only by (I, V) within one document's POOM). The "document" dimension is handled externally by the granfilade lookup in Phase 1.

---

### Summary

**Correspondence computation uses the granfilade I-address dimension first (Phase 1), then the per-document POOM's (I, V) 2D index (Phase 2).** It does not consult any shared spanfilade index keyed by (I-span, document). The per-document factoring is hardcoded: `findorgl` (`granf1.c:17`) extracts one POOM per document, and `ispan2vspanset` (`orglinks.c:389`) queries that POOM's 2D (I→V) mapping. A future shared (I-span, document) index is stubbed in `type2dbottomcruminfo.homedoc` and `crumqualifies2d:274` but is disabled by the unconditional `NULL` passed as `docisaptr` throughout the correspondence call chain (`retrie.c:249-250`).
