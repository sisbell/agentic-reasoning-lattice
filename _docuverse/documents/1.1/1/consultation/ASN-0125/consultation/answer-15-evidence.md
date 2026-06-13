## Question 15 [evidence]

> Can a link's source or target endset contain another link orgl's I-address span (`docISA.0.2.N`), and does `insertendsetsinspanf` index such link-orgl I-spans in the spanfilade exactly as it indexes text I-spans — making a separate link-between-links mechanically expressible as a supersession record?

## KB Synthesis

## Link-Between-Links: Mechanical Feasibility Analysis

The short answer is **yes, mechanically**, but with a semantically critical limitation that changes what "supersession" can mean.

---

### The Conversion Path

When `create_link` is called, endpoint V-spans are converted to I-spans via `vspanset2sporglset` → `vspanset2ispanset` → `permute` → `span2spanset`. This chain is entirely type-agnostic [SS-DUAL-ENFILADE, Finding 0011]:

> `insertpm`, `docopy`, `retrieverestricted`, and `permute` are all type-agnostic.

If the source V-span covers a position in the link subspace (e.g., V:2.1), the POOM at that position maps to a link orgl ISA (e.g., `docISA.0.2.N`). That ISA becomes the `sporglorigin` in the resulting sporgl. `acceptablevsa` will not reject this because it unconditionally returns TRUE [PRE-INSERT, Finding 0049].

---

### Spanfilade Indexing

`insertendsetsinspanf` receives the sporglset and inserts one `insertnd` call per I-span into the spanfilade [INT-SPORGL-LINK-INDEX, Finding 0013]. The call is:

```c
insertspanf(taskptr, spanf, link_isa, sporglset, LINKFROMSPAN)
```

The spanfilade is a pure `(I-address-range → link-ISA)` index with no type metadata on entries [SS-SPANF-OPERATIONS]. A link orgl ISA in the I-address field is stored and indexed identically to a permascroll byte address. So yes: **`insertendsetsinspanf` indexes link-orgl I-spans exactly as it indexes text I-spans.**

---

### Discovery Path

`find_links` converts its search specset to I-addresses via the same type-agnostic `specset2ispanset` chain, then intersects against the spanfilade [SS-FIND-LINKS, Finding 0028]:

> `find_links(S) = { L | I-addresses(S) ∩ I-addresses(L.source) ≠ ∅ }`

If the search specset covers V:2.1 in the home document, the I-address produced is the link orgl ISA. The spanfilade search returns any link that indexed that ISA as an endpoint. The supersession link is mechanically discoverable.

---

### The Fundamental Limitation

Here is the critical difference from text-to-text links. [SS-CONTENT-IDENTITY, Finding 0009] makes this explicit:

> **Link orgl ISAs** are unique references, not shareable content. Two documents **cannot share** a link ISA via transclusion because each link is a distinct object.

For text content, discovery propagates transitively: transclude "here" into doc C, and links on "here" become discoverable from C via shared I-addresses. For link ISAs, **no such propagation exists**. The ISA `docA.0.2.1` appears in the POOM of exactly one document (the home document), at exactly one V-position (2.1). It cannot be transcluded. `compare_versions` would crash if it encountered the link-subspace span [EC-COMPARE-VERSIONS-LINK-CRASH].

This means a link-between-links is discoverable **only by searching the specific document that contains the link reference in its 2.x subspace**, not from any document that "references" the linked link.

---

### What This Means for Supersession

A supersession record expressed this way:

1. **Is mechanically insertable** — the storage layer accepts it without error
2. **Is discoverable** — `find_links(source=V:2.x in home_doc)` returns it
3. **Is not transitively discoverable** — unlike text links, supersession cannot be found by any document that "transcluded" the original link
4. **Is permanent and followable** — once created, the link orgl ISA is in I-space permanently [INV-LINK-PERMANENCE], and FOLLOWLINK on the supersession record still resolves it even after the original link's content is deleted [EC-GHOST-LINK]

The spanfilade indexing is symmetric: the supersession link's ISA is indexed under the link orgl ISA, so `find_links` from the home document can discover the supersession in both directions (from the source link orgl ISA, or searching for links whose target is that ISA).

**Bottom line**: The storage layer is agnostic enough that link-about-link is mechanically sound. The constraint is semantic, not mechanical: link ISAs are object identities, not content identities, so supersession records are isolated to their creation context and don't benefit from the transclusion-propagation that makes text-to-text links globally visible [INV-LINK-GLOBAL-VISIBILITY].

---

## Code Exploration

I now have all the pieces. Here is the full answer.

---

## Can Link Endsets Contain Link-Orgl I-Address Spans, and Are They Indexed Identically?

### Address Structure of Link Orgls (`docISA.0.2.N`)

Link orgls are allocated by `findisatoinsertmolecule` [granf2.c:158-181] when `atomtype == LINKATOM` (value 2, from xanadu.h:146). For a document at `docISA`, here is the allocation:

```c
// granf2.c:171-175
} else if (hintptr->atomtype == LINKATOM) {
    tumblerincrement (&hintptr->hintisa, 2, 2, isaptr);   // seed: docISA.0.2
    if (tumblercmp (&lowerbound, isaptr) == LESS)
        tumblerincrement (isaptr, 1, 1, isaptr);           // first link: docISA.0.2.0.1
    else
        tumblerincrement (&lowerbound , 0, 1, isaptr);     // subsequent: lowerbound + 1
}
```

`tumblerincrement(aptr, rightshift, bint, cptr)` [tumble.c:599-623] finds the last non-zero mantissa position `idx` and adds `bint` to `mantissa[idx + rightshift]`. For a document at `1.1.0.1` (idx=3), `tumblerincrement(&docISA, 2, 2)` yields `mantissa[5] = 2` → `1.1.0.1.0.2`. The subsequent `tumblerincrement(isaptr, 1, 1)` appends a `.1`, giving `1.1.0.1.0.2.1` as the first link ISA. Each successive link gets `docISA.0.2.N` for N = 1, 2, 3, … confirmed by the sequential increment logic at granf2.c:175.

After creation, `docreatelink` [do1.c:195-221] copies the link's ISA back into the document's POOM at a **V-position in the link-reference space**:

```c
// do2.c:151-166 — findnextlinkvsa
tumblerincrement (&firstlink, 0, 2, &firstlink);  // → 2
tumblerincrement (&firstlink, 1, 1, &firstlink);  // → 2.1
```

The first link reference is at V=2.1, the second at V=2.2, etc. These are distinct from text positions (V=1.1, 1.2, … set by `findvsatoappend` [orglinks.c:42-43]).

---

### Part 1: Can a Link Endset Contain `docISA.0.2.N`?

**Yes, unconditionally.** The critical path is `specset2sporglset` [sporgl.c:14-33]:

```c
// sporgl.c:23-28
} else if (((typeitemheader *)specset)->itemid == VSPECID) {
    if (!(sporglsetptr = vspanset2sporglset(taskptr,
              &((typevspec *)specset)->docisa,
              ((typevspec *)specset)->vspanset,
              sporglsetptr, type))) {
        return (FALSE);
    }
}
```

`vspanset2sporglset` [sporgl.c:35-65] calls `vspanset2ispanset` [orglinks.c:389-394] → `permute` [orglinks.c:404-422] → `span2spanset` [orglinks.c:425-454] → `retrieverestricted` on the document's orgl (POOM). The POOM stores the full I↔V mapping, including the link-reference entries inserted by `insertpm` when `docopy` was called. **No filter exists at any layer of this pipeline.**

If the caller passes a V-specset covering V=2.3 for document docX, `permute` queries the POOM, finds the crum whose V-extent covers 2.3, and extracts its I-coordinate: `docX.0.2.3` (the ISA of the link at that V-position). This lands in a `typesporgl` item:

```c
// sporgl.c:51-57
sporglset->itemid = SPORGLID;
movetumbler(docisa, &sporglset->sporgladdress);   // home doc
movetumbler(&ispanset->stream, &sporglset->sporglorigin);  // I-address = docISA.0.2.3
movetumbler(&ispanset->width, &sporglset->sporglwidth);
```

A caller can also bypass V-to-I conversion entirely by passing an `ISPANID` directly with `stream = linkISA`. `specset2sporglset` handles that at sporgl.c:20-22 with a simple pointer assignment — no validation.

---

### Part 2: Does `insertendsetsinspanf` Index Link-Orgl I-Spans the Same as Text I-Spans?

**Yes, bit-for-bit identically.** Here is `insertendsetsinspanf` [do2.c:116-128] in full:

```c
bool insertendsetsinspanf(typetask *taskptr, typespanf spanfptr, typeisa *linkisaptr,
    typesporglset fromsporglset, typesporglset tosporglset, typesporglset threesporglset)
{
    bool insertspanf();
    if (!(
        insertspanf(taskptr, spanfptr, linkisaptr, fromsporglset, LINKFROMSPAN)
        && insertspanf(taskptr, spanfptr, linkisaptr, tosporglset, LINKTOSPAN)))
            return (FALSE);
    if (threesporglset) {
        if(!insertspanf(taskptr, spanfptr, linkisaptr, threesporglset, LINKTHREESPAN)){
            return (FALSE);
        }
    }
    return(TRUE);
}
```

Each call passes the sporglset — whatever I-spans it contains — to `insertspanf` [spanf1.c:15-54]. That function:

```c
prefixtumbler(isaptr, spantype, &crumorigin.dsas[ORGLRANGE]);  // spanf1.c:22
tumblerclear(&crumwidth.dsas[ORGLRANGE]);
...
for (; sporglset; ...) {
    if (itemid == ISPANID) {
        movetumbler(&ispanptr->stream, &lstream);      // spanf1.c:27
        movetumbler(&ispanptr->width, &lwidth);        // spanf1.c:28
        movetumbler(isaptr, &linfo.homedoc);
    } else if (itemid == SPORGLID) {
        movetumbler(&sporglptr->sporglorigin, &lstream);  // spanf1.c:31
        movetumbler(&sporglptr->sporglwidth, &lwidth);    // spanf1.c:32
        movetumbler(&sporglptr->sporgladdress, &linfo.homedoc);  // spanf1.c:33
    }
    movetumbler(&lstream, &crumorigin.dsas[SPANRANGE]);
    movetumbler(&lwidth, &crumwidth.dsas[SPANRANGE]);
    insertnd(taskptr, (typecuc*)spanfptr, &crumorigin, &crumwidth, &linfo, SPANRANGE);  // spanf1.c:51
}
```

`prefixtumbler(isaptr, spantype, ...)` [tumble.c:641-651] prepends `spantype` before the link's ISA to form the ORGLRANGE key (e.g., `LINKFROMSPAN.newLinkISA`). The `lstream`/`lwidth` from the sporglset become the SPANRANGE key. `insertnd` is called with these raw tumblers.

There is **no branch, no type tag, no filter** that distinguishes `lstream = docISA.0.1.N` (text I-address) from `lstream = docISA.0.2.N` (link-orgl I-address). The spanfilade node is created identically in both cases.

---

### Part 3: Is a Link-Between-Links Mechanically Expressible as a Supersession Record?

**Yes, through the standard `docreatelink` path without any modification.**

Concretely, to make a supersession record "link A (`docX.0.2.3`) is superseded by link B (`docX.0.2.4`)":

1. Build a V-specset: `{docisa: docX, vspanset: {stream:2.3, width:1}}` — this names the V-position of link A in docX.
2. Build a second V-specset: `{docisa: docX, vspanset: {stream:2.4, width:1}}` — for link B.
3. Call `createlink` [fns.c:100-112] → `docreatelink` [do1.c:195-221].
4. `specset2sporglset` converts V=2.3 → I-span `docX.0.2.3` (SPORGLID, sporgladdress=docX).
5. `insertendsetsinspanf` calls `insertspanf(..., fromsporglset, LINKFROMSPAN)` and `insertspanf(..., tosporglset, LINKTOSPAN)`.
6. The spanfilade gains entries:
   - SPANRANGE = `docX.0.2.3`, ORGLRANGE = `LINKFROMSPAN.supersessionLinkISA`
   - SPANRANGE = `docX.0.2.4`, ORGLRANGE = `LINKTOSPAN.supersessionLinkISA`

The **query path** is equally undiscriminating. `sporglset2linksetinrange` [sporgl.c:239-268]:

```c
context = retrieverestricted(spanfptr, (typespan*)sporglset, SPANRANGE, &range, ORGLRANGE, ...);
for (c = context; c; c = c->nextcontext) {
    beheadtumbler(&c->totaloffset.dsas[ORGLRANGE], &linksa);  // strips spantype prefix
    onlinklist(taskptr, linksetptr, &linksa);
}
```

`retrieverestricted` queries by the I-span as a SPANRANGE key, finds the supersession link, and `beheadtumbler` strips the `LINKFROMSPAN` prefix to yield `supersessionLinkISA`. The query returns the supersession link whenever someone asks "which links have this link orgl's I-span in their from/to/three endset?"

---

### One Important Caveat: `filter_vspanset_to_text_subspace`

`doshowrelationof2versions` [do1.c:428-448] calls `filter_vspanset_to_text_subspace` [do1.c:386-411], which strips V-spans below `1.0`. Since text starts at V=1.1 and link-references start at V=2.1, this filter would **not** strip link-reference V-spans from specsets passed to `compare_versions`. This filter is also entirely absent from the `createlink` and `followlink` paths. So link-between-links construction and retrieval are unaffected.

---

### Summary

| Question | Answer | Key code |
|----------|--------|----------|
| Can endsets contain `docISA.0.2.N`? | **Yes** — POOM maps V=2.N ↔ I=`docISA.0.2.N`; no filter on that path | sporgl.c:35-65, orglinks.c:389-454 |
| Does `insertendsetsinspanf` treat them identically to text I-spans? | **Yes** — `insertspanf` reads raw tumbler values, no type discrimination | do2.c:116-128, spanf1.c:15-54 |
| Is link-between-links expressible as a supersession record? | **Yes** — standard `docreatelink` path, no modification needed | do1.c:195-221, sporgl.c:239-268 |

A link whose from-endset covers `docISA.0.2.3` and whose to-endset covers `docISA.0.2.4` is a valid Xanadu link in every mechanical sense: it is stored, indexed, and retrievable by the same algorithms that handle all other links. The supersession semantics are purely a matter of client interpretation.
