## Question 16 [evidence]

> When a replacement link is created, the original's endset entries remain in the write-only spanfilade: is there any structural marker that distinguishes a superseded link's spanfilade entries from a current link's, or do both sets of DOCISPAN/endset entries remain equally live with no way to tell which link is the successor?

## KB Synthesis

There is no structural marker. Both the original and replacement link's entries remain equally live in the spanfilade — the system has no concept of supersession at any storage layer.

Here is the complete picture from the KB:

**The spanfilade is unconditionally append-only.** [INV-SPANF-WRITE-ONLY] states: no `deletespanf`, `removespanf`, or any removal function exists anywhere in `spanf1.c` or `spanf2.c`. Entries created by `insertendsetsinspanf` at link creation time persist permanently. When a "replacement" link is created, `insertendsetsinspanf` adds a new set of entries mapping the replacement link's endpoint I-addresses → new link ISA. The original link's entries — mapping possibly overlapping endpoint I-addresses → original link ISA — are untouched.

**The spanfilade's data model is a multimap.** [SS-SPANF-OPERATIONS] models it as `SpanEnfilade = Map<IAddress, Set<LinkISA>>`. For any I-address range covered by both the original and replacement link's endpoints, the result set now contains *both* ISAs. `find_links` returns both; there is nothing in the returned set that marks one as superseded.

**Links are permanent objects with no status field.** [INV-LINK-PERMANENCE] confirms there is no DELETELINK operation. The link orgl structure [SS-LINK-ENDPOINT] is `Link = (source: set<ContentId>, target: set<ContentId>, type: Tumbler)` — no successor pointer, no status flag, no version field.

**The three-layer model offers only one mutable layer.** [SS-THREE-LAYER-MODEL] draws the boundary clearly: I-space (link orgl) and spanfilade entries are permanent; only the POOM (document V-stream) is mutable. The only action that can make a link "disappear" from a document's visible structure is `DELETEVSPAN` targeting its 2.x V-position, which removes the POOM entry. But [SS-THREE-LAYER-MODEL] explicitly demonstrates the consequence: after DELETEVSPAN, `find_links` *still returns the link* (spanfilade intact), `follow_link` still works (orgl intact), and only `retrieve_vspanset` omits it. So even "removing" a link from a document's POOM does not prevent spanfilade-level discovery of both the original and replacement.

**The only implicit ordering information is monotonic ISA allocation.** [INV-MONOTONIC] guarantees that link ISAs are allocated in strictly increasing order, so a higher ISA was created later. But this is temporal ordering information embedded in the tumbler address — not a supersession marker, and the system provides no query interface to exploit it for "find me only the most recent link."

**Concrete consequence:** If you create link L1 on some content, then create replacement link L2 on the same or overlapping content, `find_links` returns `{L1, L2}` with no annotation. Both sets of DOCISPAN and endset entries are equally live. The system provides no structural means to distinguish them.

---

## Code Exploration

I now have everything I need. Here is my complete answer, with all code citations.

---

## Answer: No Structural Marker — Superseded and Current Link Entries Are Equally Live

The code confirms the worst case: there is **no structural marker** of any kind in the spanfilade that distinguishes a superseded link's entries from a current link's entries. Both sit as equal, live entries with identical structure, and the spanfilade has no mechanism to invalidate either.

---

### How Link Endsets Land in the Spanfilade

Every `CREATELINK` call reaches `docreatelink` [do1.c:195-221], which terminates in:

```c
// do1.c:218-219
&& insertendsetsinorgl (taskptr, linkisaptr, link, &fromvsa, fromsporglset, &tovsa, tosporglset, &threevsa, threesporglset)
&& insertendsetsinspanf (taskptr, spanf, linkisaptr, fromsporglset, tosporglset, threesporglset)
```

`insertendsetsinspanf` [do2.c:116-128] does nothing but call `insertspanf` three times:

```c
insertspanf(taskptr, spanfptr, linkisaptr, fromsporglset, LINKFROMSPAN)   // do2.c:119
insertspanf(taskptr, spanfptr, linkisaptr, tosporglset,   LINKTOSPAN)     // do2.c:120
insertspanf(taskptr, spanfptr, linkisaptr, threesporglset, LINKTHREESPAN) // do2.c:123
```

Inside `insertspanf` [spanf1.c:15-54], each entry is written with this two-dimensional key:

```c
prefixtumbler (isaptr, spantype, &crumorigin.dsas[ORGLRANGE]);   // spanf1.c:22
//   ORGLRANGE = spantype . linkISA  (e.g. "1.2.3.0.4.1" for LINKFROMSPAN on link 2.3.0.4.1)
movetumbler (&lstream, &crumorigin.dsas[SPANRANGE]);             // spanf1.c:49
//   SPANRANGE = the content address (I-address or sporgl origin)
```

The bottom-crum payload is `type2dbottomcruminfo`, which contains a single field:

```c
movetumbler(isaptr, &linfo.homedoc);   // spanf1.c:29 / 33 / 42
```

That is the entire record: ORGLRANGE = `spantype . linkISA`, SPANRANGE = content address, and `homedoc` = the link's ISA. **There is no version flag, no "superseded" bit, no generation counter, no pointer to a successor.** The entry is structurally indistinguishable from any other link entry of the same type.

---

### The Spanfilade Is Write-Only

`insertspanf` [spanf1.c:15] exists. `deletespanf` does not — not in `spanf1.c`, not anywhere in the backend. Finding 0057 documents this explicitly. The table from that finding applies directly:

| Operation | Granf Update | Spanf Update |
|-----------|-------------|--------------|
| CREATE_LINK | creates link orgl | `insertendsetsinspanf` (permanent) |
| *(no DELETELINK operation exists)* | — | — |

When a "replacement" link is created — meaning `createlink` is called to create a new link that semantically supersedes the old one — the new link's endset entries are added alongside the old link's entries. The old entries are never touched.

---

### The Disabled Kluge Is the Smoking Gun

`sporglset2linksetinrange` [sporgl.c:239-269] is the function that traverses the spanfilade to resolve which link ISAs match a given content range. Inside that function, line 251 contains this:

```c
if (FALSE/*trying to kluge links followable thru versions */&&((typeitemheader *)sporglset)->itemid == SPORGLID) {
    infoptr = &linfo;
    movetumbler (&((typesporgl *)sporglset)->sporgladdress, &linfo.homedoc);
  } else
    infoptr = NULL;
```

`FALSE` is a compile-time constant. This branch is dead code. The comment says "trying to kluge links followable thru versions" — meaning the team recognized that link retrieval could not distinguish version-related link entries and attempted a fix based on the `sporgladdress`/`homedoc` field to restrict which document version's entries to traverse. That attempt was abandoned and hard-coded to `FALSE`. The retrieval therefore ignores `infoptr` entirely (it passes `(typeisa*)NULL` when calling `retrieverestricted` [sporgl.c:259]):

```c
context = retrieverestricted(spanfptr, (typespan*)sporglset, SPANRANGE, &range, ORGLRANGE, (typeisa*)infoptr);
//                                                                                         ^^^^^^^^^^^^^^^^^^
//                                                     always NULL in practice — no homedoc filtering
```

`retrieverestricted` at [retrie.c:56-85] checks `infoptr` to optionally restrict by `homedoc`, but because `infoptr` is always NULL here, it skips that check and returns all entries for the SPANRANGE/ORGLRANGE intersection regardless of which version or generation the link belongs to. [retrie.c:77-82]:

```c
if (docisaptr) {
    movetumbler(docisaptr, &info.homedoc);
    infoptr = &info;
} else {
    infoptr = NULL;
}
```

---

### What `docreatenewversion` Does Not Do

`docreatenewversion` [do1.c:260-299] creates a new document ISA, copies the text subspace content via `docopyinternal` [do1.c:293], and closes. It does **not**:
- Update any link's spanfilade entries
- Mark any existing link as belonging to the old version
- Create any pointer from old link ISAs to the new document

Finding 0043 confirms: `CREATENEWVERSION` copies only text (1.x positions), not the link subspace (0.x). The links themselves — their ISAs and their spanfilade entries — belong to the original document and remain completely unchanged.

---

### ISA Tumbler Ordering: Chronology, Not Succession

The only structural difference between an older link and its "replacement" is that the newer link has a higher ISA tumbler, because `findnextlinkvsa` [do2.c:151-167] always allocates the link's V-space address at the end of the document's current address range:

```c
tumbleradd (&vspan.stream, &vspan.width, &vspanreach);    // do2.c:161
if (tumblercmp (&vspanreach, &firstlink) == LESS)
    movetumbler (&firstlink, vsaptr);
else
    movetumbler (&vspanreach, vsaptr);                    // do2.c:164-165
```

This gives newer links a higher position in the document's V-space (and thus a higher ISA tumbler), which encodes **time-of-creation order**. It does not encode semantic supersession. There is no code that walks the ISA hierarchy to ask "is link X a newer version of link Y?" — the granfilade ISA tree has no such relation-following logic.

---

### Summary

**Both the superseded link's and the replacement link's DOCISPAN/endset entries remain equally live in the spanfilade, with no structural way to distinguish them.**

The complete evidence chain:

1. `insertspanf` [spanf1.c:15-54] — entries contain only `spantype . linkISA` (ORGLRANGE), content address (SPANRANGE), and `homedoc`. No supersession field.
2. No `deletespanf` function exists anywhere in the backend.
3. `sporglset2linksetinrange` [sporgl.c:251] — the attempt to filter by version (`homedoc`) is explicitly hard-coded to `FALSE` with the comment "trying to kluge links followable thru versions."
4. `sporglset2linksetinrange` [sporgl.c:259] always passes `(typeisa*)NULL` to `retrieverestricted`, so no homedoc filtering occurs.
5. `docreatenewversion` [do1.c:260-299] never touches link spanfilade entries.
6. The FEBE protocol has no `DELETELINK`, `REPLACELINK`, or `INVALIDATELINK` operation — `init.c:30` lists all registered handlers.

The only out-of-band handle is semantic convention: the third endpoint of the replacement link could be used to point back to the superseded link. But no code enforces, queries, or interprets this convention — it is invisible to the retrieval engine.
