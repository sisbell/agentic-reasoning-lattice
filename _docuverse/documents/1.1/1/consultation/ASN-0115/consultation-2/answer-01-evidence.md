## Question 1 [evidence]

> Do the spans fed into `specset2ispanset` carry a deepest-level action point (ordinal spans), or can the resolution chain receive a non-ordinal span whose interval crosses from the content subspace into the link subspace?

## KB Synthesis

## Short Answer

Yes — a non-ordinal span that crosses the subspace boundary **can** and **does** enter `specset2ispanset`, and the resolution chain has no guard against it.

---

## Mechanism

`specset2ispanset` delegates through `permute()` → `span2spanset()` → `retrieverestricted()`. Every function in this chain is **type-agnostic**: it searches the POOM for all entries whose V-position falls within the supplied interval, without testing which subspace the entries belong to. [SS-DUAL-ENFILADE, Finding 0011]

The POOM itself stores both text entries (V-positions `1.x`) and link orgl references (V-positions `2.x` internally) as plain tumblers with no type tag. `retrieverestricted()` returns everything in the queried interval. [SS-DUAL-ENFILADE, Finding 0009]

---

## The Concrete Cross-Subspace Path

`RETRIEVEDOCVSPAN` (opcode 14) reads the root node's raw V-dimension width via `retrievevspanpm()` — no subspace awareness. For a document containing 10 chars of text plus 1 link, it returns `1.1 for 1.2`. This single span has its left border in the text subspace and its right border in the link subspace. [SS-VSPAN-VS-VSPANSET, Findings 0017, 0035]

When that bounding-box span is wrapped in a VSpec and handed to `specset2ispanset`, the POOM interval query covers both `1.x` entries (yielding permascroll I-addresses) and `2.x` entries (yielding link orgl ISAs). The result is a heterogeneous I-span set mixing two incomparable address types. [PRE-RETRIEVE-CONTENTS, Finding 0010]

---

## Why There Is No Subspace Guard at This Level

`acceptablevsa()` — the intended gate for checking V-position validity before POOM operations — unconditionally returns `TRUE`. [PRE-SUBSPACE-CONVENTION, Finding 0010]

The two-blade knife that enforces subspace isolation for **INSERT** (blade₁ = insertion point, blade₂ = `(N+1).1` subspace boundary) is specific to the write path in `makegappm()`/`insertcutsectionnd()`. It has no analogue in the read path that `specset2ispanset` uses. [SS-TWO-BLADE-KNIFE, FC-SUBSPACE, Finding 0054]

The **read** path has no equivalent structural guard — cross-subspace intervals are accepted and processed silently.

---

## Observable Consequences

| Downstream consumer | What happens with mixed I-span set |
|---|---|
| `ispanset2vstuffset` (content retrieval) | Looks up link orgl ISAs in the permascroll → NULL/garbage bytes [PRE-RETRIEVE-CONTENTS] |
| `correspond.c` (compare_versions) | Assumes all I-addresses are permascroll; link ISAs never intersect text → crashes [EC-COMPARE-VERSIONS-LINK-CRASH] |
| `insertspanf` / DOCISPAN | Indexes link ISAs as if they were content addresses — semantically meaningless entries [PRE-VCOPY] |

The `compare_versions` crash (Bug 0009) is the clearest proof: it receives exactly this mixed result and aborts because `correspond.c`'s nested loop has no path for handling empty intersections between incomparable I-address types. [EC-COMPARE-VERSIONS-LINK-CRASH, PRE-COMPARE-VERSIONS]

---

## Summary

`specset2ispanset` is purely an interval query over the POOM. It will happily accept a span like `1.1 for 1.2` that straddles the `1.x`/`2.x` subspace boundary, and will return a mixed I-address set containing both permascroll addresses and link orgl ISAs. There is no deepest-level action point that filters this: the subspace invariant is **caller-enforced convention**, not a structural property of the resolution chain itself. [INV-SUBSPACE-CONVENTION, SS-SUBSPACE-CONVENTION]

---

## Code Exploration

Now I have everything needed for a complete, cited answer.

---

## Answer

### What enters `specset2ispanset`

`specset2ispanset` [`do2.c:14`] iterates a mixed linked list (`typespecset`), dispatching on `itemid`:

```c
for (; specset; specset = ...) {
    if (((typeitemheader *)specset)->itemid == ISPANID) {
        *ispansetptr = (typeispanset)specset;          // pass through verbatim
        ispansetptr = ...;
    } else if (((typeitemheader *)specset)->itemid == VSPECID) {
        findorgl(...) && vspanset2ispanset(taskptr, docorgl,
            ((typevspec *)specset)->vspanset, ispansetptr) // convert V→I
    }
}
```
[`do2.c:23-39`]

The `typespec` union [`xanadu.h:85-89`] wraps two fundamentally different kinds of spans:

| Tag | Type | Space | Path |
|-----|------|-------|------|
| `ISPANID` | `typeispan` | **I-space (ordinal)** | threaded directly into output, no conversion |
| `VSPECID` | `typevspec.vspanset` | **V-space (virtual)** | converted via `vspanset2ispanset` |

`typeispan` is a typedef alias for `typespan` [`xanadu.h:75`], and so is `typevspan` [`xanadu.h:73`] — the concrete struct is identical (`{next, itemid, stream, width}`) but the semantic domain differs: I-space is the ordinal permascroll address; V-space is the virtual document address.

---

### The `ISPANID` path — deepest-level action points

`ISPANID` items are already-resolved ordinal spans. They are threaded verbatim into the output `typeispanset` at `do2.c:25-26`. They never re-enter the V→I resolution chain. I-space is flat and ordinal; there is no content/link subspace distinction in I-space, so no boundary-crossing issue exists here.

---

### The `VSPECID` path — the full resolution chain

For `VSPECID`, the `vspanset` (V-space spans) passes through this chain:

1. **`vspanset2ispanset`** [`orglinks.c:397-402`]  
   ```c
   return permute(taskptr, orgl, vspanptr, V, ispansetptr, I);
   ```

2. **`permute`** [`orglinks.c:404-422`]  
   Walks each V-span and calls `span2spanset` for each, verbatim.

3. **`span2spanset`** [`orglinks.c:425-454`]  
   ```c
   context = retrieverestricted((typecuc*)orgl, restrictionspanptr,
                                 restrictionindex, (typespan*)NULL, targindex, ...);
   ```
   Passes the raw V-span as `restrictionspanptr` with `index1=V`, `span2ptr=NULL`.

4. **`retrieverestricted`** [`retrie.c:56-85`]  
   Computes `span1start = span.stream`, `span1end = span.stream + span.width` using raw `tumbleradd`. No subspace check.

5. **`findcbcinarea2d`** [`retrie.c:229-268`] → **`crumqualifies2d`** [`retrie.c:270-305`]  
   ```c
   endcmp = iszerotumbler(span1end) ? TOMYRIGHT
           : whereoncrum(crumptr, offset, span1end, index1);
   ...
   startcmp = whereoncrum(crumptr, offset, span1start, index1);
   ```
   Uses `whereoncrum` → `tumblercmp` [`retrie.c:345-397`, `tumble.c:72-84`]. **`tumblercmp` is a plain total order on tumblers: it compares `.exp` then `.mantissa[]` lexicographically.** It has no knowledge of subspace boundaries.

**Nowhere in steps 1–5 is there a check for whether the V-span crosses the content/link subspace boundary.** The functions `istextcrum` [`orglinks.c:246-252`] and `islinkcrum` [`orglinks.c:255-260`] — which do know about the boundary — are only used in `maxtextwid` and `retrievevspansetpm`, which are on a completely separate call path.

---

### Can a cross-boundary V-span actually reach `specset2ispanset`?

**Yes. It happens by design in `docreatenewversion`** [`do1.c:260-299`]:

```c
if (!doretrievedocvspanfoo(taskptr, isaptr, &vspan)) return FALSE;

vspec.next = NULL;
vspec.itemid = VSPECID;
movetumbler(isaptr, &vspec.docisa);
vspec.vspanset = &vspan;
...
docopyinternal(taskptr, newisaptr, &vspan.stream, &vspec);
```

`doretrievedocvspanfoo` [`do1.c:301-309`] calls `retrievedocumentpartofvspanpm` [`orglinks.c:155-162`]:

```c
movetumbler(&((typecuc*)orgl)->cdsp.dsas[V], &vspanptr->stream);
movetumbler(&((typecuc*)orgl)->cwid.dsas[V], &vspanptr->width);
```

This reads the root crum's V-displacement and V-width — the full extent of the document in V-space. If the document contains both text crums (1-story V-addresses, `mantissa[1]==0`) and link crums (2-story V-addresses, `mantissa[0]==1 && mantissa[1]!=0` per [`orglinks.c:257`]), then `cwid.dsas[V]` encompasses both. The resulting `typevspan` spans the entire V-range, crossing the content/link boundary. This span is then directly assigned to `vspec.vspanset` and fed into `docopyinternal` → `specset2ispanset`.

The subspace structure in the V-address ordering:
- Text crums: `cdsp.dsas[V].mantissa[1] == 0` and `is1story(cwid)` [`orglinks.c:248`] — single-story V-addresses
- Link crums: `cdsp.dsas[V].mantissa[0] == 1 && mantissa[1] != 0` [`orglinks.c:257`] — 2-story V-addresses of form `1.n`

A root crum that contains both will have a V-width covering both, so the vspan passed to `specset2ispanset` has an interval `[stream, stream+width)` that includes both `1` (text) and `1.n` (link) addresses.

---

### The one partial guard that exists

`filter_vspanset_to_text_subspace` [`do1.c:386-411`] was added as a "SEMANTIC FIX" for Bug 009 (`do1.c:377-385`). It strips V-spans with `stream < 1` (i.e., pre-content metadata below the text subspace start). It is applied explicitly in `doshowrelationof2versions` [`do1.c:437-441`] before calling `specset2ispanset`.

However, this filter does **not** split a span that starts at `1` (text space) and extends through `1.n` (link space). Its threshold is `tumblercmp(&stream, &text_subspace_start) >= EQUAL` where `text_subspace_start = 1` (tumbler `{mantissa[0]=1}`) [`do1.c:394-396`]. A cross-boundary span starting at `1` passes the filter unchanged.

---

### Summary

The `ISPANID` arm of `specset2ispanset` carries **already-resolved ordinal I-spans** — deepest-level action points. They bypass the resolution chain entirely.

The `VSPECID` arm carries **V-space spans** that enter the resolution chain. There is **no guard** in the resolution chain (`vspanset2ispanset` → `permute` → `span2spanset` → `retrieverestricted` → `findcbcinarea2d` → `crumqualifies2d`) against a V-span whose interval crosses from the content subspace into the link subspace. `crumqualifies2d` uses plain `tumblercmp` with no subspace semantics. Cross-boundary V-spans do reach the chain in practice — `docreatenewversion` passes the root crum's full V-extent (including both text and link address ranges) through this path.
