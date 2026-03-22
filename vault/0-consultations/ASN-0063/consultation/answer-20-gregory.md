## Question 20 [gregory]

> For a link with endsets spanning content in multiple documents (e.g., source in doc1, target in doc2), are the spanfilade entries keyed by the I-address spans alone regardless of document origin, so that discovery from any third document transcluding either span would find the link?

## KB Synthesis

Yes — spanfilade entries are keyed by I-address spans alone, independent of document origin. Discovery from any third document transcluding either endpoint span will find the link.

**Indexing at link creation**

When `docreatelink` runs, `insertendsetsinspanf()` inserts all endpoint sporgls into the spanf [ST-CREATE-LINK, SS-SPORGL]. Each sporgl packages `(origin: IAddress, width, sporgladdress: DocISA)`, but the index key is the I-address range. The spanfilade structure is `Map<IAddress, Set<LinkISA>>` [SS-SPANF-OPERATIONS, SS-DUAL-ENFILADE]. The document of origin (`sporgladdress`) is stored for later V-address *resolution*, not for keying discovery.

**Discovery is pure I-address intersection**

`find_links(S) = { L | I-addresses(S) ∩ I-addresses(L.source) ≠ ∅ }` [SS-FIND-LINKS]. The spanfilade search converts the query specset to I-spans, then searches by I-address regardless of which document those I-addresses came from [INT-SPORGL-LINK-INDEX]. Document identity plays no role in the match.

**The orgl-dimension filter is disabled**

`sporglset2linkset()` contains the guard `if (TRUE||!homeset)`, which permanently replaces any caller-supplied orgl range with a hardcoded width-100 range from tumbler zero [EC-FIND-LINKS-GLOBAL, PRE-FIND-LINKS/Finding 0069]. So even if a caller attempted to scope discovery to a specific document, the implementation ignores it. All `find_links` calls are effectively global in the orgl dimension.

**Transclusion makes this the core mechanism**

Because vcopy shares I-addresses rather than copying them [ST-VCOPY, INT-LINK-TRANSCLUSION], any third document transcluding content from either endpoint inherits the same I-addresses. Since spanfilade lookup is I-address-only, that third document will discover the link identically to the original endpoint documents. This is stated as a system-wide invariant: links are globally visible through content identity [INV-LINK-GLOBAL-VISIBILITY].

**Endpoint resolution (V-addresses) is separate**

After discovery, `FOLLOWLINK` or `RETRIEVEENDSETS` resolves I-addresses back to V-positions through the querying document's POOM [SS-FOLLOWLINK, ST-RETRIEVE-ENDSETS]. The `sporgladdress` field is used at this stage to look up which document holds the content — but by then discovery has already succeeded. Unreferenced I-addresses are silently dropped during I-to-V conversion [INV-ITOV-FILTERING], but that is a post-discovery filter, not a discovery gate.

**Concrete implication**

A link with source in doc1 and target in doc2 is fully discoverable from doc3 if doc3 transcludes any content overlapping either endpoint — even partially [SS-FIND-LINKS/Finding 0028]. The spanfilade contains no document-scoped partitioning that would prevent this.

---

## Code Exploration

Now I have a complete picture. Let me compile the full answer.

---

## Answer: Cross-Document Link Discovery via Spanfilade I-Address Keys

The spanfilade is a 2D enfilade (two axes: SPANRANGE and ORGLRANGE). Link endset entries are **keyed purely on I-address spans in the SPANRANGE axis**. The source document is stored as metadata in the crum bottom info but is **explicitly not used as a filter during retrieval**. Cross-document discovery through transcluded content works because I-addresses are permanent and shared across all transclusions.

---

### 1. The Spanfilade Key Structure: `insertspanf` [spanf1.c:15–54]

When `docreatelink` [do1.c:195–221] stores a link's endsets, it ends up calling `insertendsetsinspanf` [do2.c:116–128], which calls `insertspanf` three times (once per endset type):

```c
insertspanf(taskptr, spanfptr, linkisaptr, fromsporglset, LINKFROMSPAN)
insertspanf(taskptr, spanfptr, linkisaptr, tosporglset,   LINKTOSPAN)
insertspanf(taskptr, spanfptr, linkisaptr, threesporglset, LINKTHREESPAN)
```

Inside `insertspanf` [spanf1.c:22–52], for a SPORGLID item:

```c
movetumbler(&((typesporgl*)sporglset)->sporglorigin, &lstream);   // I-address origin
movetumbler(&((typesporgl*)sporglset)->sporglwidth,  &lwidth);    // I-address width
movetumbler(&((typesporgl*)sporglset)->sporgladdress, &linfo.homedoc); // source doc (metadata)
```

Then:

```c
prefixtumbler(isaptr, spantype, &crumorigin.dsas[ORGLRANGE]); // = spantype.linkISA
movetumbler(&lstream, &crumorigin.dsas[SPANRANGE]);           // = I-address of content
insertnd(taskptr, (typecuc*)spanfptr, &crumorigin, &crumwidth, &linfo, SPANRANGE);
```
[spanf1.c:22, 49–51]

The 2D crum key is:
- **ORGLRANGE axis**: `prefixtumbler(linkISA, spantype)` = the link's ISA with the endset type (1=FROM, 2=TO, 3=THREE) prepended [tumble.c:641–650]
- **SPANRANGE axis**: the **I-address** of the linked content

The `linfo.homedoc` (the document that owns the content) is stored in the **bottom crum info**, not in either key axis. It is not indexed.

---

### 2. How V-Spans Become I-Spans: `specset2sporglset` [sporgl.c:14–65]

`docreatelink` calls `specset2sporglset` [do1.c:214–216] to convert from/to/three V-specs into sporgl sets before inserting. For a V-spec input:

```c
vspanset2sporglset(taskptr, &docisa, vspanset, sporglsetptr, type)  // sporgl.c:25
```

This does V→I permutation via `vspanset2ispanset` [sporgl.c:48], then packages each I-span as a sporgl with:

```c
movetumbler(docisa, &sporglset->sporgladdress);       // source document ISA
movetumbler(&ispanset->stream, &sporglset->sporglorigin); // I-address origin
movetumbler(&ispanset->width,  &sporglset->sporglwidth);  // I-address width
```
[sporgl.c:53–55]

So the sporgl carries the home document address as a **side-channel field**, separate from the I-coordinates that become the spanfilade key.

---

### 3. The Retrieval Side: `sporglset2linksetinrange` [sporgl.c:239–269]

When finding links for a given V-span, the query path is:

`dofindlinksfromtothree` [do1.c:348–353] → `findlinksfromtothreesp` [spanf1.c:56–103] → `sporglset2linkset` [sporgl.c:222–237] → `sporglset2linksetinrange` [sporgl.c:239–269]

Inside `sporglset2linksetinrange`, the critical block is:

```c
if (FALSE/*trying to kluge links followable thru versions*/
    && ((typeitemheader*)sporglset)->itemid == SPORGLID) {
        infoptr = &linfo;
        movetumbler(&((typesporgl*)sporglset)->sporgladdress, &linfo.homedoc);
} else
        infoptr = NULL;
```
[sporgl.c:251–255]

**The `FALSE` guard permanently disables home-document filtering.** `infoptr` is always `NULL`. Then:

```c
context = retrieverestricted(spanfptr, (typespan*)sporglset, SPANRANGE,
                             &range, ORGLRANGE, (typeisa*)infoptr);
```
[sporgl.c:259]

The query presents the sporgl as an I-span restriction (`SPANRANGE`), finds all link ISAs in `ORGLRANGE` that overlap, and **never filters by source document**. The comment "trying to kluge links followable thru versions" shows this was a deliberate design decision — disabling the filter was intentional to make links discoverable through transclusions.

---

### 4. The Full Cross-Document Scenario

Given a link with source endset in doc1 and target in doc2, and a third document (doc3) that transcluces content from doc1:

1. **Link creation**: doc1's V-span → I-span via permutation on doc1's granfilade orgl → stored in spanfilade under that I-span + link ISA key. `linfo.homedoc = doc1-ISA` (stored but not indexed).

2. **Discovery from doc3**: doc3's V-span for the same content → I-span via permutation on doc3's granfilade. Because doc3 transcluded content from doc1's permascroll, **both point to the same I-span**.

3. **Retrieval**: `sporglset2linksetinrange` queries the spanfilade with that I-span in SPANRANGE. It hits the same crum (since the key was the I-span, not the V-span or document ISA). `infoptr = NULL` means no document filter. The link ISA is extracted from ORGLRANGE and returned.

---

### Conclusion

**Yes.** The spanfilade is keyed by I-address spans (SPANRANGE) and link ISA + endset type (ORGLRANGE). The source document is stored in `linfo.homedoc` as crum metadata but is never used as a retrieval filter — the `if (FALSE...)` guard at [sporgl.c:251] ensures it. Any document that transcluces content sharing the same I-address (permascroll identity) will discover links whose endsets reference that content, regardless of which document originally contained it or which document is hosting the transclusion. The architecture makes link traversability a property of permanent content identity, not document ownership.
