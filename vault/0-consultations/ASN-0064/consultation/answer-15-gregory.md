## Question 15 [gregory]

> After candidate links are found via the spanfilade, `link2sporglset` extracts I-addresses from the link orgl in the granfilade — does this extraction read the link's actual endset spans, or does it rely on the spanfilade's indexed copy, and can these ever diverge?

## KB Synthesis

`link2sporglset` reads exclusively from the **granfilade link orgl** — the permanent, canonical record. It never consults the spanfilade.

## Two separate read paths

**FOLLOWLINK** uses `link2sporglset()` (`sporgl.c:67-95`), which calls `retrieverestricted()` against the granfilade to extract I-addresses from the link orgl at the requested endset position (0.1, 0.2, or 0.3) [SS-FOLLOWLINK]. No POOM check and no spanfilade access occur here.

**RETRIEVEENDSETS** works the other direction entirely: it takes a content region, converts it to I-addresses via sporglset, and searches the spanfilade using ORGLRANGE prefixes (LINKFROMSPAN=1, LINKTOSPAN=2, LINKTHREESPAN=3) to find links whose indexed I-addresses overlap [SS-RETRIEVE-ENDSETS]. The spanfilade is an inverted index (I-address → link ISA), serving discovery; the link orgl is the forward store (link ISA → endpoint I-addresses), serving retrieval.

## Can they diverge?

**Under normal operation: no.** At `CREATELINK` time, `docreatelink` writes both structures from the same sporglset [ST-CREATE-LINK]:
1. Creates the link orgl in the granfilade (permanent)
2. Indexes endpoint I-addresses in the spanfilade via `insertendsetsinspanf`

Both the granfilade link orgl and the spanfilade entries are written once and never modified — the granfilade is append-only and the spanfilade is write-only [INV-SPANF-WRITE-ONLY]. So under crash-free operation they represent the same I-address set.

**Under a crash: yes.** `docreatelink` performs these two writes sequentially with no transactional mechanism [INV-DUAL-ENFILADE-CONSISTENCY]. A crash between them leaves the link orgl in the granfilade with no spanfilade entries. The result: the link is followable by ID (orgl is authoritative) but undiscoverable by content-identity search (no spanfilade index). This is the consistency risk the KB identifies as the main threat to the dual-enfilade invariant.

**One important asymmetry**: the spanfilade can also contain *stale* entries from deleted content that no longer appears in any POOM [EC-STALE-SPANF-REFERENCE, INT-DELETE-SPANF-DIVERGENCE], but stale spanfilade entries for *content* do not affect what the link orgl says about its endpoints — the link orgl stores the original endpoint specification permanently. What `link2sporglset` returns is always the creation-time specification, unaffected by any subsequent content deletion.

---

## Code Exploration

I now have all the code I need to answer definitively. Here is the full analysis:

---

## Answer: `link2sporglset` reads from the link's granfilade orgl — never the spanfilade

### The two data structures written at link creation

`docreatelink` (do1.c:195–221) populates **both** structures from the same `fromsporglset`/`tosporglset` in a single chained expression:

```c
/* do1.c:218–219 */
&& insertendsetsinorgl (taskptr, linkisaptr, link, &fromvsa, fromsporglset,
                         &tovsa, tosporglset, &threevsa, threesporglset)
&& insertendsetsinspanf (taskptr, spanf, linkisaptr, fromsporglset, tosporglset, threesporglset)
```

**`insertendsetsinorgl`** (do2.c:130–149) calls `insertpm` (orglinks.c:75–134) for each endset. `insertpm` stores a 2D crum in the link's POOM enfilade:

- **I-dimension** (`crumorigin.dsas[I]`, `crumwidth.dsas[I]`): the actual I-span — origin from `unpacksporgl`'s `lstream`, width from `lwidth`  [orglinks.c:105–109]
- **V-dimension** (`crumorigin.dsas[V]`, `crumwidth.dsas[V]`): the V-address from `setlinkvsas` (do2.c:169–180):  FROM → `1.1`, TO → `2.1`, THREE → `3.1`

```c
/* orglinks.c:130–131 */
insertnd (taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);
tumbleradd (vsaptr, &crumwidth.dsas[V], vsaptr);
```

**`insertendsetsinspanf`** (do2.c:116–128) calls `insertspanf` (spanf1.c:15–54) for each endset. `insertspanf` stores a 2D crum in the **global spanfilade** (`spanf`), keyed by:

- **SPANRANGE** (`crumorigin.dsas[SPANRANGE]`, `crumwidth.dsas[SPANRANGE]`): the same I-span
- **ORGLRANGE** (`crumorigin.dsas[ORGLRANGE]`): `linkisaptr` prefixed by the endset type constant (`LINKFROMSPAN=1`, `LINKTOSPAN=2`, `LINKTHREESPAN=3`  [xanadu.h:36–38])

```c
/* spanf1.c:22 */
prefixtumbler (isaptr, spantype, &crumorigin.dsas[ORGLRANGE]);
```

---

### `link2sporglset` reads the granfilade — never the spanfilade

```c
/* sporgl.c:67–95 */
bool link2sporglset(typetask *taskptr, typeisa *linkisa, typesporglset *sporglsetptr, INT whichend, int type)
{
  typeorgl orgl;
  tumbler zero;
  typevspan vspan;
  ...
  if (!findorgl (taskptr, granf, linkisa, &orgl, type)){    /* ← granfilade */
      return (FALSE);
  }
  tumblerclear (&zero);
  tumblerincrement (&zero, 0, whichend, &vspan.stream);     /* stream = whichend */
  tumblerincrement (&zero, 0/*1*/, 1, &vspan.width);        /* width  = 1        */
  if (context = retrieverestricted((typecuc*)orgl, &vspan, V, (typespan*)NULL, I, (typeisa*)NULL)) {
      for (c = context; c; c = c->nextcontext) {
          sporglptr = (typesporgl *)taskalloc(taskptr,sizeof (typesporgl));
          contextintosporgl ((type2dcontext*)c, (tumbler*)NULL, sporglptr, I);
          ...
      }
      ...
  }
}
```

Three observations:

**1. `findorgl` goes to `granf`**, the global granfilade root [sporgl.c:77]. `fetchorglgr` returns the link's own POOM sub-enfilade node. This is the link's canonical data store — not `spanf`.

**2. `retrieverestricted` is called on `orgl`**, the link's POOM node [sporgl.c:83]. The arguments `V` (index1) and `I` (index2) make it a V→I lookup: find I-space crumbs whose V-position overlaps `[whichend, whichend+1)`. Since `setlinkvsas` stored FROM at `1.1`, TO at `2.1`, THREE at `3.1`, the query range `[1,2)` correctly contains `1.1` for FROM; `[2,3)` contains `2.1` for TO, etc.

**3. `contextintosporgl` extracts I-space** from the context result [sporgl.c:86, sporgl.c:205–220]:

```c
/* sporgl.c:211, 219 */
movetumbler(&context->totaloffset.dsas[index],&sporglptr->sporglorigin);
movetumbler (&context->contextwid.dsas[index], &sporglptr->sporglwidth);
```

`index` = `I`. So the sporgl's origin and width are read from the **I** dimension of the crum, which is exactly the I-span that `insertpm` stored. The V-address serves only as the lookup key — it is not propagated into the output sporgl.

The spanfilade variable `spanf` does not appear anywhere in `link2sporglset`, `contextintosporgl`, `findorgl`, or `retrieverestricted` (which dispatches on `fullcrumptr->cenftype` — POOM/SPAN/GRAN — not on which global variable was passed).

The complete downstream path from `dofollowlink` (do1.c:223–232) also avoids the spanfilade:

- `linksporglset2specset` (sporgl.c:97–123): for sporgls with a non-zero address, calls `linksporglset2vspec` → `sporglset2vspanset` → `ispan2vspanset` (orglinks.c:389–394) → `permute` → `span2spanset` (orglinks.c:425–454) → `retrieverestricted((typecuc*)orgl, ...)` on the **document's** POOM orgl. The spanfilade is not consulted at any step.

---

### The `doretrieveendsets` path reads the spanfilade

`doretrieveendsets` (do1.c:369–374) → `retrieveendsetsfromspanf` (spanf1.c:190–235) is an entirely separate operation. It:

1. Converts the link's vspec to a sporglset via `specset2sporglset` (which goes through the granfilade to do V→I)
2. Then calls `retrievesporglsetinrange` (spanf1.c:237–267), which calls `retrieverestricted` on **`spanf`** — the global spanfilade:

```c
/* spanf1.c:245 */
context = retrieverestricted((typecuc*)spanf, (typespan*)sporglptr, SPANRANGE,
                               whichspace, ORGLRANGE, (typeisa*)NULL/*kluge...*/);
```

This reads the spanfilade's indexed copy. `link2sporglset` and `doretrieveendsets` access different data structures and could in principle return different I-spans.

---

### Can the two structures diverge?

**At write time, they are identical**: Both `insertendsetsinorgl` and `insertendsetsinspanf` consume the same `fromsporglset`/`tosporglset` objects created from the same user-supplied specsets. Under a successful link creation, the I-spans stored in the granfilade orgl and the I-spans indexed in the spanfilade are the same.

**Partial failure is a live divergence path**: The two writes are sequenced with `&&` (do1.c:218–219). There is no rollback for the granfilade write if the spanfilade write fails. If `insertendsetsinorgl` succeeds and `insertendsetsinspanf` fails — or fails mid-way (it calls `insertspanf` for FROM, then TO, then THREE separately; do2.c:119–126) — the granfilade will have some or all endsets while the spanfilade has fewer:

```c
/* do2.c:118–126 */
if (!(
  insertspanf(taskptr,spanfptr,linkisaptr,fromsporglset,LINKFROMSPAN)
  &&insertspanf(taskptr,spanfptr,linkisaptr,tosporglset,LINKTOSPAN)))
      return (FALSE);   /* orgl already written; no rollback */
if (threesporglset) {
    if(!insertspanf(taskptr,spanfptr,linkisaptr,threesporglset,LINKTHREESPAN)){
        return (FALSE);
    }
}
```

In that scenario: `link2sporglset` (granfilade) succeeds and returns correct endsets; the spanfilade-based candidate search (`sporglset2linksetinrange`) fails to find the link via the missing endset. The structures diverge silently.

**No post-creation modification path exists**: Neither `domakelink` nor `docreatelink` updates endsets after the initial write. There is no "edit link endsets" operation. So divergence from modification is not a concern.

**Ordering may differ**: The granfilade POOM traversal returns crumbs in V-order (FROM before TO before THREE). The spanfilade SPAN traversal in `retrievesporglsetinrange` returns crumbs in I-address order. If a link's endsets happen to span non-contiguous I-space regions, the two paths will return the same set of I-spans but in different order.

---

### Summary

`link2sporglset` reads **exclusively from the link's granfilade orgl** (the link's own POOM enfilade node). The call at sporgl.c:77 passes `granf` to `findorgl`; the `retrieverestricted` at sporgl.c:83 queries the returned `orgl` POOM node in V-space; `contextintosporgl` at sporgl.c:86 extracts the I-dimension from each result crum. The spanfilade is not accessed at any point in this path.

The spanfilade holds a **parallel index** written at link creation from the same sporglset data. It is read only by the "find links by content region" path (`sporglset2linksetinrange` → `retrieverestricted` on `spanf`), not by `link2sporglset`. The two structures *can* diverge if `insertendsetsinorgl` succeeds but `insertendsetsinspanf` fails, because no rollback mechanism exists for the granfilade write. In that case, `link2sporglset` returns the correct endsets (from the granfilade), while the spanfilade-based candidate search does not find the link via its missing endset index entries.
