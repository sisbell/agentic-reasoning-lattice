## Question 20 [evidence]

> Is there any mechanism in the spanfilade index structure that would let `find_links` distinguish between two links with overlapping I-address endsets — e.g., a "current" and a "superseded" version — or are they returned as an undifferentiated set?

## KB Synthesis

The KB is unambiguous: `find_links` returns an **undifferentiated set**. Several converging facts establish this.

**The index structure is a flat multimap.** [SS-SPANF-OPERATIONS] models the spanfilade link index as `Map<IAddress, Set<LinkISA>>`. When a query I-address range intersects the endsets of two links, both `LinkISA` values are included in the returned set — the index carries no metadata to distinguish one link from another.

**The orgl-range filter that could have helped is permanently disabled.** The search operates in two dimensions: a span dimension (I-address content) and an orgl dimension (document/link origin). [EC-FIND-LINKS-GLOBAL] and [PRE-FIND-LINKS / Finding 0069] document that `sporglset2linkset()` contains a `TRUE||!homeset` guard that always fires, replacing whatever orgl range the caller provides with a hardcoded width-100 range covering all orgls. Even if a caller tried to scope a query to "only links allocated in this version's document," the backend ignores it.

**The `homedocids` filter is also broken.** [EC-HOMEDOCIDS-FILTER-BROKEN] confirms the parameter is accepted without error but has no effect on results.

**The spanfilade is append-only; there is no supersession mechanism.** [INV-SPANF-WRITE-ONLY] establishes that spanfilade entries are never removed. There is no "superseded" flag or recency metadata on link orgls. [INV-LINK-PERMANENCE] confirms links are permanent once created; the system has no concept of link lifecycle beyond existence.

**What a caller can do post-hoc:** Links in the result set differ only by their ISA addresses, which encode home document and creation order [SS-ADDRESS-SPACE / Finding 0065]. An application could inspect ISA structure to infer ordering — links under the same home document get sequential suffixes (`.0.2.1`, `.0.2.2`, …) — but this is entirely application-layer logic. The spanfilade search itself provides no such discrimination.

---

## Code Exploration

I now have all the source I need to answer the question definitively. Here is the full analysis:

---

## Answer: No Version Discrimination in the Spanfilade — Links Are an Undifferentiated Set

### The Data Structure: What the Spanfilade Stores

The global spanfilade `spanf` is a 2-dimensional enfilade indexed by two ranges simultaneously. When `docreatelink` creates a link [`do1.c:195`], it ends by calling `insertendsetsinspanf` [`do1.c:219`], which calls `insertspanf` once per endset role:

```c
insertspanf(taskptr, spanfptr, linkisaptr, fromsporglset, LINKFROMSPAN)
insertspanf(taskptr, spanfptr, linkisaptr, tosporglset,   LINKTOSPAN)
insertspanf(taskptr, spanfptr, linkisaptr, threesporglset, LINKTHREESPAN)
```
[`do2.c:116–128`]

Inside `insertspanf` [`spanf1.c:15`], each crum inserted into the 2D tree carries:

- **SPANRANGE dimension** → the I-address span of the endset content (`lstream`/`lwidth`, extracted from the sporgl)
- **ORGLRANGE dimension** → `prefixtumbler(isaptr, spantype, &crumorigin.dsas[ORGLRANGE])` [`spanf1.c:22`]

That prefix packs `spantype` (1=FROM, 2=TO, 3=THREE) as the leading component, followed by the link's ISA tumbler. There are no other fields in the crum. The `type2dbottomcruminfo` stored at leaf level contains only a `homedoc` tumbler. **There is no version-status, generation counter, or "superseded" flag.**

---

### The Query Path: `sporglset2linkset`

When `findlinksfromtothreesp` [`spanf1.c:56`] is called, it calls `sporglset2linkset` for each non-null endset specset [`spanf1.c:77, 85, 93`]. That function lives in `sporgl.c:222`:

```c
int sporglset2linkset(typetask *taskptr, typecuc *spanfptr, typesporglset sporglset,
                      typelinkset *linksetptr, typeispan *homeset, INT spantype)
{
    ...
    for (; homeset; homeset = homeset->next) {
        sporglset2linksetinrange(taskptr, spanfptr, sporglset, linksetptr, homeset, spantype);
    }
}
```
[`sporgl.c:234–237`]

Inside `sporglset2linksetinrange` [`sporgl.c:239`]:

```c
prefixtumbler(&orglrange->stream, spantype, &range.stream);
prefixtumbler(&orglrange->width, 0, &range.width);
context = retrieverestricted(spanfptr, (typespan*)sporglset, SPANRANGE,
                              &range, ORGLRANGE, (typeisa*)infoptr);
```
[`sporgl.c:257–259`]

This calls into `retrieveinarea` → `findcbcinarea2d` [`retrie.c:87,97`], which is a pure range search:
- **SPANRANGE** must intersect the query sporgl's I-address range
- **ORGLRANGE** must fall within `range` (the spantype prefix, spanning all ISAs for that link role)

For every matching leaf crum, the link's ISA is extracted:

```c
beheadtumbler(&c->totaloffset.dsas[ORGLRANGE], &linksa);
onlinklist(taskptr, linksetptr, &linksa);
```
[`sporgl.c:264–265`]

`beheadtumbler` strips off the leading `spantype` component and returns the raw ISA tumbler. That ISA is then appended to the result list by `onlinklist` [`spanf2.c:26`], which deduplicates by ISA equality only:

```c
for (temp = *linksetptr; nextlink = temp->next; temp = nextlink) {
    if (tumblereq(&temp->address, linkisaptr))
        return(0);   // already present, skip
}
```
[`spanf2.c:38–41`]

Finally, `intersectlinksets` [`spanf2.c:46`] computes the three-way intersection using `tumblereq` on ISAs alone [`spanf2.c:98, 109`].

**At no point in this chain is any version, genealogy, or recency information consulted.**

---

### The `acceptablevsa` Stub

The function that could have enforced version-based filtering is `acceptablevsa` [`do2.c:110`]:

```c
bool acceptablevsa(tumbler *vsaptr, typeorgl orglptr)
{
    return (TRUE);
}
```
[`do2.c:110–113`]

It unconditionally approves every VSA. This is the hook where "is this V-address within the current version's valid range?" could have been checked. It was never implemented.

---

### The Dead Code Confession

The clearest evidence that version-aware link traversal was **attempted but abandoned** is this commented-out branch in `sporglset2linksetinrange` [`sporgl.c:251`]:

```c
if (FALSE/*trying to kluge links followable thru versions */
    && ((typeitemheader *)sporglset)->itemid == SPORGLID) {
    infoptr = &linfo;
    movetumbler(&((typesporgl *)sporglset)->sporgladdress, &linfo.homedoc);
} else
    infoptr = NULL;
```
[`sporgl.c:251–255`]

The intent was to pass a `homedoc` restriction into `retrieverestricted`, which would have allowed the 2D search to filter crums by their `type2dbottomcruminfo.homedoc` field — i.e., only returning links that "belong to" a particular document version. But the condition is hard-coded to `FALSE`, making `infoptr` always `NULL`. The `infoptr != NULL` path in `findcbcinarea2d` actually triggers a `gerror` in non-DISTRIBUTION builds:

```c
if(infoptr){
    fprintf(stderr,"not NULL infoptr versions mumble specialcase 11/27/84 ...\n");
    gerror("findcbcinarea2d");
}
```
[`retrie.c:244–247`]

So passing `infoptr` to `findcbcinarea2d` was never even tested — the 2D search explicitly cannot handle it.

---

### Versioning at the Document Level vs. the Spanfilade Level

When `docreatenewversion` [`do1.c:260`] creates a new version of a document, it calls `docopyinternal` to copy content from the old orgl into a new one with a new ISA. This new orgl gets fresh I-address spans. A link created against the old version's I-spans is indexed in the spanfilade with those old spans. A link created against the new version's I-spans is indexed with the new spans.

If a query specset resolves to an I-span that overlaps **both** the old and new versions' content addresses, `sporglset2linkset` will return ISAs for **both** the old-version link and the new-version link. There is no mechanism in the spanfilade to suppress the old one.

---

### Conclusion

The spanfilade index structure provides **no mechanism** to distinguish "current" from "superseded" links with overlapping I-address endsets. Two such links are returned as an undifferentiated set, ordered only by the traversal order of `findcbcinarea2d` over the 2D crum tree. The design has three layers of version-blindness:

1. **Storage**: crums in the spanfilade carry only `(I-span, link-ISA)` pairs — no version metadata [`spanf1.c:22, 49–51`].
2. **Retrieval**: `sporglset2linkset` extracts ISAs via `beheadtumbler` with no genealogy lookup [`sporgl.c:264`].
3. **Filtering**: `acceptablevsa` is a `return TRUE` stub [`do2.c:110–113`]; the `infoptr` path in `findcbcinarea2d` was abandoned (`FALSE` guard) and would `gerror` if ever reached [`sporgl.c:251`, `retrie.c:244`].

Any discrimination between current and superseded links must be performed by the caller using knowledge of the ISA version tree from the granfilade — the spanfilade itself is version-transparent.
