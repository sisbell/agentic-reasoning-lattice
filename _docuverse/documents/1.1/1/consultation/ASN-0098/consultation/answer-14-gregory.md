## Question 14 [gregory]

> When CREATENEWVERSION copies only text subspace `1.x` and not links from subspace `2.x`, is the link's own I-address (its orgl at `docISA.0.2.N`) excluded from the version's POOM — and if so, does `RETRIEVEDOCVSPANSET` on the version show zero entries in the link subspace even though `find_links` discovers the original's links through shared text I-addresses?

## KB Synthesis

Yes on all three counts, and the KB is explicit about each.

**Link subspace excluded from version POOM**

`CREATENEWVERSION` calls `doretrievedocvspanfoo` → `retrievedocumentpartofvspanpm`, which reads `cdsp.dsas[V]` and `cwid.dsas[V]` from the root crum. These fields track the **text subspace** displacement starting at position `1`, not position `0` (the link subspace). The link subspace at `2.x` is structurally outside this V-dimension range. [SS-DUAL-ENFILADE / Finding 0043], [ST-VERSION-CREATE / Finding 0043, 0046]

The copy then runs via `docopyinternal`, which inserts only the text V-span into the new document's POOM. No link orgl ISAs (the `docISA.0.2.N` entries) are placed into the version's POOM. [ST-VERSION-CREATE / Finding 0046]

**RETRIEVEDOCVSPANSET confirms zero link entries**

Golden test evidence from Finding 0043 is direct:

```
Source vspanset (normalized output):
  at 0 for 0.1   (link subspace — internal 2.x)
  at 1 for 1     (text subspace)

Version vspanset:
  at 1.1 for 0.34   (text only, no link subspace)
```

The version's `retrieve_vspanset` returns only a text span. [SS-VSPAN-VS-VSPANSET], [ST-VERSION-CREATE / Finding 0043]

**find_links works anyway — through shared text I-addresses**

This is the key decoupling. `find_links` does not query the POOM at all — it queries the **spanfilade** (span enfilade) by I-address. The version's text subspace shares permascroll I-addresses with the source's text subspace (that's what `docopyinternal` establishes). Those I-addresses are already indexed in the spanfilade because the source's original `INSERT`/`COPY` operations wrote DOCISPAN entries. [SS-DUAL-ENFILADE / Finding 0012], [FC-CONTENT-SPANF-ISOLATION / Finding 0036], [INT-LINK-VERSION / Finding 0046]

When you call `find_links` on the version, the call chain is:
1. Convert version V-span to I-spans (via the version's POOM, which maps text V-positions to shared permascroll I-addresses)
2. Search the spanfilade by those I-addresses
3. Return links whose endsets intersect

Since the I-addresses are identical between source and version, the same spanfilade entries fire. [INT-LINK-VERSION / Finding 0032, 0046], [INV-LINK-GLOBAL-VISIBILITY]

**The link orgl's own I-address (`docISA.0.2.N`) is irrelevant here**

The link's I-address (its identity in the granfilade, e.g. `1.1.0.1.0.1.0.2.1`) is neither copied nor needed for discovery. Discovery runs through the **endpoint content** I-addresses (the permascroll text that the link's FROM/TO/THREE endsets reference), not through the link orgl's own address. The version inherits discoverability because it inherits the endpoint content identity — not because it has any representation of the link in its POOM. [SS-THREE-LAYER-MODEL / Finding 0040], [INT-LINK-TRANSCLUSION / Finding 0043]

**Summary**

| | Version |
|---|---|
| Link subspace in POOM | Empty |
| `retrieve_vspanset` link entries | None |
| `find_links` result | Same as source |

The version's POOM-level link subspace is empty; link **discoverability** is preserved purely through shared text I-addresses in the spanfilade. These are independent mechanisms. [SS-THREE-LAYER-MODEL], [FC-SUBSPACE / Finding 0043], [ST-VERSION-CREATE / Finding 0043, 0046]

---

## Code Exploration

Now I have everything needed for a complete answer. Let me compile it with full code citations.

---

## Full Answer

### Summary

Yes, the link's own I-address (its orgl at `docISA.0.2.N`) **is excluded** from the new version's POOM. `RETRIEVEDOCVSPANSET` on the version shows **zero entries** in the link subspace. And `find_links` **does discover** the original's links through shared text I-addresses. Here is the complete code trace.

---

### 1. How CREATENEWVERSION Copies Content

`docreatenewversion` [do1.c:260-299]:

```c
doretrievedocvspanfoo(taskptr, isaptr, &vspan)         // [do1.c:281]
...
vspec.docisa = *isaptr;                                 // source = original doc
vspec.vspanset = &vspan;                               // the V-range to copy
docopyinternal(taskptr, newisaptr, &vspan.stream, &vspec);  // [do1.c:293]
```

The vspan comes from `doretrievedocvspanfoo` [do1.c:301-309], which calls `retrievedocumentpartofvspanpm` [orglinks.c:155-162]:

```c
bool retrievedocumentpartofvspanpm(typetask *taskptr, typeorgl orgl, typevspan *vspanptr)
{ /* this is a kluge*/
    vspanptr->next = NULL;
    vspanptr->itemid = VSPANID;
    movetumbler (&((typecuc *) orgl)->cdsp.dsas[V], &vspanptr->stream);  // [orglinks.c:159]
    movetumbler (&((typecuc *) orgl)->cwid.dsas[V], &vspanptr->width);  // [orglinks.c:160]
    return (TRUE);
}
```

This reads the root crum's `cdsp.dsas[V]` and `cwid.dsas[V]` directly.

---

### 2. The Root Crum's V-Span Covers Only Text

Per Finding 0066 and [wisp.c] `setwispnd`: for a POOM with text at V=1.x and link at V=2.x, the root's `cdsp.dsas[V]` = the minimum V-address across all content = **1** (text start). Its `cwid.dsas[V]` = the bounding box width = **1** (representing the extent of the text).

The comment at [do1.c:302] says `/* this routine is a kluge not yet kluged*/`, signaling this function is not intended to handle multi-subspace documents. The returned vspan is:

```
stream = 1    (= V=1, start of text subspace)
width  = 1    (= width 1, covering V=1.x only)
```

The range `[1, 1+1]` = `[1, 2)` encompasses the text subspace (V=1.x) but does **not** reach the link subspace at V=2.1 (since 2.1 > 2.0). The link at V=2.x sits just outside this range.

Validated empirically in `golden/versions/version_copies_link_subspace.json`:
```
Source vspanset: at 0 for 0.1    (link, normalized from V=2.x)
                 at 1 for 1      (text)

Version vspanset: at 1.1 for 0.15   (text only — confirmed)
```

---

### 3. specset2ispanset Finds Only Text I-Spans

`docopyinternal` [do1.c:66-82]:

```c
specset2ispanset(taskptr, specset, &ispanset, NOBERTREQUIRED)  // V→I on original doc
&& insertpm(taskptr, docisaptr, docorgl, vsaptr, ispanset)     // put I-spans in new doc
&& insertspanf(taskptr, spanf, docisaptr, ispanset, DOCISPAN)  // register in spanf
```

`specset2ispanset` [do2.c:14-46] → `vspanset2ispanset` [orglinks.c:397-402] → `permute(V→I)` [orglinks.c:404-422] → `retrieverestricted` traverses the original document's POOM with restriction span `[1, 2)` in V. This finds **only** the text crums (at V=1.x, mapping to permascroll I-addresses). The link crum at V=2.1 is outside the restriction range — it is never visited.

The returned `ispanset` is therefore **permascroll I-addresses only** — no link ISA.

`insertpm` [orglinks.c:75-134] inserts these text I-spans into the new version's POOM starting at `vsaptr = &vspan.stream = 1`. The link's I-address (docISA.0.2.N) is **never placed** in the new version's POOM at all — neither in text subspace nor link subspace. It is completely absent.

---

### 4. RETRIEVEDOCVSPANSET Shows Zero Link Entries

`doretrievedocvspanset` [do1.c:322-336] → `retrievevspansetpm` [orglinks.c:173-221]:

```c
if (is1story(&ccptr->cwid.dsas[V])) { /* if it is just text return that */
    // return single text span
} else {
    // extract link and text spans separately
    linkvspan.stream = ccptr->cwid.dsas[V] with mantissa[1]=0
    ...
    maxtextwid(taskptr, ccptr, &voffset, &maxwid);
}
```

`is1story` [tumble.c:237-247]:
```c
bool is1story(tumbler *tumblerptr)
{
    INT i;
    for (i = 1; i < NPLACES; i++)
        if (tumblerptr->mantissa[i] != 0)
            return (FALSE);
    return (TRUE);
}
```

Returns TRUE when only `mantissa[0]` is non-zero — i.e., the width spans only a single "story" (the V=1.x story with no link-subspace component).

The new version's POOM contains only text I-spans at V=1.x. Its root `cwid.dsas[V]` is a text-only tumbler with no multi-story component. `is1story` returns **TRUE**, so `retrievevspansetpm` takes the simple branch, returning **one text span and zero link entries**. The link subspace component is structurally zero because there are no crums at V=2.x in the new version's orgl.

`RETRIEVEDOCVSPANSET` output for the version: text span only. **Zero entries in the link subspace.**

---

### 5. find_links Discovers Original's Links Via Shared I-Addresses

When the version was built, `insertspanf(taskptr, spanf, newisaptr, ispanset, DOCISPAN)` [do1.c:79] registered the new version's text I-spans in the global spanf under the new version's ISA. These are **the same permascroll I-addresses** as the original document's text content.

When `findlinksfromtothreesp` [spanf1.c:56-103] is called with a V-spec pointing to the new version's text:

```c
if (fromvspecset)
    specset2sporglset(taskptr, fromvspecset, &fromsporglset, NOBERTREQUIRED);
if (fromvspecset) {
    sporglset2linkset(taskptr, (typecuc*)spanfptr, fromsporglset, &fromlinkset,
                      orglrange, LINKFROMSPAN);
```

`specset2sporglset` on the new version maps its text V-positions to I-spans (permascroll addresses). These permascroll addresses are **identical** to the original's text I-spans, because `docopyinternal` copied the same permascroll content without allocating new I-addresses.

The original document's link registration (during `docreatelink` [do1.c:195-221]) called `insertendsetsinspanf` [do2.c:116-128]:
```c
insertspanf(taskptr, spanfptr, linkisaptr, fromsporglset, LINKFROMSPAN)
insertspanf(taskptr, spanfptr, linkisaptr, tosporglset, LINKTOSPAN)
```

This recorded in the global spanf: `text_permascroll_I-span → original_link_ISA` (under LINKFROMSPAN / LINKTOSPAN orgl-range keys derived from the link's ISA).

`sporglset2linkset` searches the spanf by I-span — not by document ISA. When the version's text permascroll I-spans are submitted, they match the registered link endpoints from the original. The link ISA (docISA.0.2.N) is returned.

**`find_links` discovers the original document's links** because:
- Link discovery is I-address-based (global spanf), not V-address-based (per-POOM)
- The new version shares permascroll I-spans with the original
- The original's link endpoints were registered against those same I-spans

This is validated by golden tests (Finding 0007: `version_with_links`; Finding 0026: `link_to_transcluded_content`).

---

### Concise Answer to Each Part

| Question | Answer | Mechanism |
|----------|--------|-----------|
| Is the link's I-address (orgl at `docISA.0.2.N`) excluded from the version's POOM? | **Yes, fully excluded** | `retrievedocumentpartofvspanpm` [orglinks.c:155-162] returns a vspan covering only V=1.x (text). `permute(V→I)` never visits the crum at V=2.x. The link's ISA is never passed to `insertpm`. |
| Does `RETRIEVEDOCVSPANSET` show zero entries in the link subspace? | **Yes, zero entries** | The new version's POOM has no crums at V=2.x. `retrievevspansetpm` [orglinks.c:173-221] via `is1story` [tumble.c:237] reports a single text span only. |
| Does `find_links` discover the original's links through shared text I-addresses? | **Yes** | The spanf stores link endpoints by permascroll I-address globally. `findlinksfromtothreesp` [spanf1.c:56-103] searches by I-span, not by document. The version shares text permascroll I-spans with the original, so the original's links are found through them. |

The architectural asymmetry is this: the POOM (V→I mapping) is **per-document and subspace-aware** — only the text subspace (V=1.x) is copied by `CREATENEWVERSION`. The spanf (I→link mapping) is **global and document-agnostic** — it tracks link endpoints purely by I-address, making links follow shared content identity across all versions.
