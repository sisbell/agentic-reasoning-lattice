## Question 18 [gregory]

> Links are stored in the document's link subspace at `0.2.x` in the POOM — what is the significance of a link having a V-address within a specific document, given that links are discoverable globally via I-address overlap regardless of which document "owns" them?

## KB Synthesis

The significance is three-layered, and the layers serve distinct purposes:

## 1. The POOM entry makes a link part of the document's *visible content structure*

`retrieve_vspanset` and `retrieve_contents` operate through the POOM. A link at V-address `2.x` in the home document's POOM appears in the vspanset result and is returned by `retrieve_contents` as a link reference — it is structurally part of the document's content, not merely an annotation on it. Without the POOM entry, the document has no way to say "here are the links I contain" at the V-space level. [SS-THREE-LAYER-MODEL], [SS-VSPAN-VS-VSPANSET]

## 2. The home document establishes the link's permanent I-address namespace

Link I-addresses are allocated per-document under `docISA.2.x`. The home document at creation time determines where in the global granfilade the link orgl lives — permanently. This is separate from the POOM entry: the I-address is allocated whether or not the home doc's POOM retains the `2.x` mapping. [SS-ADDRESS-SPACE] Finding 0065, [SS-LINK-HOME-DOCUMENT]

## 3. The POOM entry is the only *mutable* layer of link membership

This is the architectural point: the three layers have different persistence properties:
- **I-space** (link orgl): append-only, permanent [INV-LINK-PERMANENCE]
- **Spanfilade**: write-only, permanent [INV-SPANF-WRITE-ONLY]
- **POOM (V-stream)**: mutable — the only layer that can be modified

`DELETEVSPAN(2.x)` removes the POOM entry while leaving the link fully intact and globally discoverable. The result is the "reverse orphan" state: `find_links` still finds the link (spanfilade intact), `follow_link` still works (I-space intact), but `retrieve_vspanset` no longer shows it and the document no longer "contains" it structurally. [SS-THREE-LAYER-MODEL], [EC-REVERSE-ORPHAN]

## The upshot

Global discoverability via I-address overlap is a property of the **spanfilade layer** — it has nothing to do with POOM membership. The home document's POOM entry serves as the document's *ownership record* and *presentation slot*: it determines which links a document can enumerate as its own, what appears in its vspanset, and what position in V-space the link occupies for pagination purposes.

In short: I-address overlap makes a link *findable from* a document; the POOM entry makes a link *contained by* a document. These are independent predicates that can diverge — a link created in document A is discoverable from document B via transclusion with no POOM entry in B, while a link can be removed from A's POOM (via DELETEVSPAN) and still be discoverable from A via the spanfilade. [FC-LINK-DELETE-ISOLATION], [INT-LINK-TRANSCLUSION]

---

## Code Exploration

Now I have everything I need. Let me write the full answer.

---

## The Significance of a Link's V-Address Within Its Owning Document

### What "owning" means structurally

When `docreatelink` runs, it does three separate things to establish a link:

**1. Allocates the link's ISA tumbler in the document's namespace** [do1.c:207–209]:
```c
makehint(DOCUMENT, ATOM, LINKATOM, docisaptr, &hint);
createorglingranf(taskptr, granf, &hint, linkisaptr)
```
The `makehint` call records `docisaptr` as the parent context for ISA allocation. The resulting `linkisaptr` tumbler is permanently scoped to the creating document's address space. This is not a runtime relationship — it's baked into the link's identity.

**2. Inserts the link's ISA into the document's POOM** [do1.c:211–212]:
```c
findnextlinkvsa(taskptr, docisaptr, &linkvsa)
docopy(taskptr, docisaptr, &linkvsa, ispanset)
```
`findnextlinkvsa` [do2.c:151–167] computes a V-address in the link subspace (starting at mantissa[0]=2, mantissa[1]=1 if the document has no prior links; otherwise just past the current reach), and `docopy` inserts the link's ISA there. The link is now part of the document's POOM content.

**3. Stores endpoints in the link's own orgl and in the global spanfilade** [do1.c:213–219]:
```c
findorgl(taskptr, granf, linkisaptr, &link, NOBERTREQUIRED)
setlinkvsas(&fromvsa, &tovsa, &threevsa)
insertendsetsinorgl(taskptr, linkisaptr, link, &fromvsa, fromsporglset, ...)
insertendsetsinspanf(taskptr, spanf, linkisaptr, fromsporglset, tosporglset, ...)
```
The link's own orgl stores endpoint sporgl sets at fixed internal V-addresses (from=1.1, to=2.1, three=3.1) [do2.c:169–183]. The global spanfilade (`spanf`) gets entries keyed by the link's ISA in ORGLRANGE and the endpoint I-spans in SPANRANGE [spanf1.c:22–51].

---

### What the V-address ownership actually does

#### A. Version inheritance — links travel with their documents

`docreatenewversion` [do1.c:260–299] copies the *entire* V-span of the source document:
```c
doretrievedocvspanfoo(taskptr, isaptr, &vspan)
// vspan.stream and vspan.width cover text + link subspace
docopyinternal(taskptr, newisaptr, &vspan.stream, &vspec)
```
The V-span returned by `retrievedocumentpartofvspanpm` [orglinks.c:155–162] is the full root crum extent — it encompasses both text content and link references. Because link ISAs live in the document's link subspace, they're automatically duplicated into the new version's POOM. **A link is owned by whichever version of the document it was created in, and that link reference propagates forward through all derived versions.**

#### B. Write-access gating at creation time

`docopy` calls `findorgl(taskptr, granf, docisaptr, &docorgl, WRITEBERT)` [do1.c:55]. You need write access to the containing document to create a link in it. Without that, you can't call `findnextlinkvsa` successfully because the BERT check will fail.

However — critically — the link's *own* orgl is opened with `NOBERTREQUIRED` [do1.c:213]. Once a link exists, anyone can follow it regardless of whether they have access to the document that "owns" it.

#### C. POOM-level partitioning for text vs. link content

The code explicitly distinguishes link crums from text crums [orglinks.c:246–261]:
```c
bool istextcrum(typecorecrum *crumptr) {
    if (crumptr->cdsp.dsas[V].mantissa[1] == 0 && is1story(&crumptr->cwid.dsas[V]))
        return TRUE;
}
bool islinkcrum(typecorecrum *crumptr) {
    if (crumptr->cdsp.dsas[V].mantissa[0] == 1 && crumptr->cdsp.dsas[V].mantissa[1] != 0)
        return TRUE;
}
```
`maxtextwid` [orglinks.c:240] skips link crums entirely: `if(ptr && !islinkcrum(ptr))`. The text extent of a document is measured without counting link references. `retrievevspansetpm` [orglinks.c:173–221] returns *two* separate V-spans: one for the text portion and one for the link portion, explicitly splitting them.

And `filter_vspanset_to_text_subspace` [do1.c:386–411] — added as a semantic fix — filters out all V < 1.0 content before version comparison, because:
```c
/* Link references at V-position 0.x are document metadata, not
 * transcludable content. They have unique ISAs, not permascroll addresses,
 * so comparing them is semantically undefined. */
```
The link subspace is explicitly categorized as *metadata*, not content.

---

### What the V-address ownership does NOT do

#### Link following ignores document ownership entirely

`dofollowlink` [do1.c:223–232]:
```c
link2sporglset(taskptr, linkisaptr, &sporglset, whichend, NOBERTREQUIRED)
linksporglset2specset(taskptr, &((typesporgl *)sporglset)->sporgladdress, sporglset, specsetptr, NOBERTREQUIRED)
```
The containing document is never consulted. The link is opened directly via its ISA tumbler, BERT is bypassed, and the endpoint sporgl set is read from the link's own orgl.

#### Link finding ignores document ownership entirely

`findlinksfromtothreesp` [spanf1.c:56–103] converts query specsets to sporglsets (V→I), then calls:
```c
sporglset2linkset(taskptr, (typecuc*)spanfptr, fromsporglset, &fromlinkset, orglrange, LINKFROMSPAN)
```
This searches the global spanfilade by I-span overlap. The spanfilade has no index keyed by which document owns the link. Any link whose endpoint I-spans overlap the query I-spans is returned, regardless of which document created it.

The disabled code in `retrievesporglsetinrange` [spanf1.c:245] is the tell:
```c
context = retrieverestricted((typecuc*)spanf, (typespan*)sporglptr, SPANRANGE, whichspace, ORGLRANGE,
    (typeisa*)NULL /*kluge to make links show thru to version &sporglptr->sporgladdress*/);
```
The `NULL` is passed where the home document ISA could have been used to *restrict* link retrieval to a specific document's links. The comment shows this was considered and rejected — passing `NULL` means every link in the spanfilade is eligible regardless of its home document. The alternative (using `&sporglptr->sporgladdress`) would have made link traversal version-aware by filtering links to those owned by a particular document version.

---

### The real answer to the question

The V-address within the document's link subspace serves three purposes:

1. **Tumbler namespace scoping**: The link's ISA is permanently allocated under the creating document's ISA via `makehint` [do1.c:207]. The link's identity is cryptographically/structurally tied to its creator document.

2. **Version propagation**: Because the link's ISA is stored in the document's POOM, it travels to all new versions of the document automatically. The link is permanently associated with the document *lineage*, not just a single version.

3. **Creation-time access control**: You need WRITEBERT on the containing document to create a link. After creation, the document association is irrelevant to link operation.

The V-address ownership does **not** matter for link following, finding, or access control at runtime. Links are globally discoverable through the spanfilade's I-space index — which is entirely document-agnostic. The containing document's V-address is metadata about provenance and lineage, not a functional constraint on link traversal.

The abandoned `homedoc` kluge [spanf1.c:245] reveals the original design tension: the Xanadu architecture *wanted* links to be version-aware (belonging to a particular document version), but the implementation settled on unconditional global discoverability. The V-address records what *would have* mattered, but the runtime machinery ignores it.
