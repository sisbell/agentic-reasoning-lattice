## Question 15 [evidence]

> When a link reaches the region only through transcluded content — the link resides in document A but the region is in document B that COPY-shares A's I-addresses — does the query surface that endset for B purely through shared I-address identity, with no reference to A's POOM?

## KB Synthesis

Yes — the discovery is purely through shared I-address identity, with no reference to A's POOM at any stage.

## The discovery path

When `find_links` or `retrieve_endsets` is called on a region in document B:

1. **B's POOM only.** The specset is converted to I-addresses using B's POOM via `specset2ispanset` (or `specset2sporglset` for endsets). A's POOM is not consulted. [SS-DUAL-ENFILADE, SS-SPANF-OPERATIONS]

2. **Spanfilade search.** Those I-addresses are searched in the spanfilade. When the link in A was created, `insertendsetsinspanf` indexed its endpoint I-addresses into the spanfilade. Since B shares those I-addresses via transclusion, B's POOM yields the same I-addresses, which hit the same spanfilade entries. [ST-CREATE-LINK, INT-SPORGL-LINK-INDEX]

3. **No cross-POOM reference.** The spanfilade maps `I-address → (link ISA, endpoint type)` — a flat index blind to which document's POOM produced the query I-addresses. [SS-SPANF-OPERATIONS, INT-LINK-TRANSCLUSION]

This is the mechanism described in [INT-LINK-TRANSCLUSION]: "vcopy creates shared content identity between documents… the only link-relevant effect of transclusion is sharing I-addresses, which enables link discovery from the destination document. The link itself is unmodified."

## Endset resolution: also no reference to A's POOM

For `retrieve_endsets`, after discovery the link's stored endpoint sporgls are converted back to V-addresses via `linksporglset2specset()`. This function looks up the endpoint I-addresses in the **querying document** (B)'s POOM, not A's. [SS-RETRIEVE-ENDSETS, SS-FOLLOWLINK]

The invariant [INV-ITOV-FILTERING] formalizes this: unreferenced I-addresses are silently filtered — if B's POOM maps some of the endpoint I-addresses, those V-positions are returned; if not, they are dropped without error. A's POOM is never consulted for the resolution step either.

## Summary

The full pipeline — discovery through spanfilade search, then endset resolution back to V-addresses — uses only B's POOM and the global spanfilade. A's POOM is a closed book throughout. The transclusion relationship matters only insofar as it established shared I-addresses; once those addresses are in both POOMs, the link subsystem operates on I-space alone. [FC-CONTENT-SPANF-ISOLATION, INV-LINK-GLOBAL-VISIBILITY]

---

## Code Exploration

I now have everything I need. Here is the full answer.

---

## Answer: Link Surfacing Through Transcluded Content — Pure I-Address Identity

**Yes.** When a link resides in document A but the queried region is in document B that COPY-shares A's I-addresses, `dofollow`/`dofind` surfaces that endset **purely through I-address range intersection**, with **no reference to document A's POOM** — and with document identity checking explicitly and permanently disabled by the implementation.

---

### 1. COPY Propagates I-Addresses Without Remapping

`docopy` [do1.c:45-65] runs three operations in sequence:

```c
specset2ispanset (taskptr, specset, &ispanset, NOBERTREQUIRED)  // line 54
&& insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset)     // line 60
&& insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN)  // line 62
```

`specset2ispanset` [do2.c:14-46] reuses ISPANID items verbatim:

```c
if (((typeitemheader *)specset)->itemid == ISPANID) {
    *ispansetptr = (typeispanset)specset;   // direct reuse — no new address
    ispansetptr = (typeispanset *)&((typeitemheader *)specset)->next;
}   // do2.c:24-26
```

So document B's `insertpm` call receives the **same I-address tumbler values** as document A holds. `insertpm` maps them to new V-addresses in B's POOM [orglinks.c:105-113], but the I-addresses themselves are unchanged. `insertspanf` then registers B as owner of those I-addresses in the **global spanfilade** [spanf1.c], tagged with B's docisa via `DOCISPAN` but keyed by the same I-address ranges.

Result: both A and B independently own entries in the global spanfilade for the same I-address ranges.

---

### 2. The Link Query Path Never Touches Document A's POOM

`dofollow`/`dofind` ultimately calls `sporglset2linksetinrange` [sporgl.c:239-269], the function that looks up links whose endsets intersect a given I-address range. The query is a direct spanfilade walk — **document A's POOM is not consulted at any point**.

---

### 3. The Document-Identity Gate Is Permanently Disabled

The only place in the entire query path where document identity could filter results is at sporgl.c:249-255:

```c
infoptr = &linfo;
for (; sporglset; ...) {
    if (FALSE/*trying to kluge links followable thru versions */
        && ((typeitemheader *)sporglset)->itemid == SPORGLID) {
        infoptr = &linfo;
        movetumbler (&((typesporgl *)sporglset)->sporgladdress, &linfo.homedoc);
    } else
        infoptr = NULL;   // ALWAYS executes — sporgl.c:255
    ...
    context = retrieverestricted (spanfptr, (typespan*)sporglset, SPANRANGE,
                                  (typespan*)NULL, ORGLRANGE, (typeisa*)infoptr);
}
```

`if (FALSE && ...)` is a compile-time constant false. The else branch — `infoptr = NULL` — **always** executes. The comment records the intent: _"trying to kluge links followable thru versions"_ — the developers knew document-scoped lookup was needed but never implemented it.

`infoptr = NULL` flows into `retrieverestricted` [retrie.c:56-85]:

```c
if (docisaptr) {
    movetumbler(docisaptr, &info.homedoc);
    infoptr = &info;
} else {
    infoptr = NULL;    // retrie.c:81
}
```

And then into `findcbcinarea2d` [retrie.c:229-268], which contains an **explicit debug assertion** that `infoptr` must remain NULL:

```c
if(infoptr){
    fprintf(stderr,"not NULL infoptr versions mumble specialcase 11/27/84 "
                   "shouldent happen till we try something fancier\n");
    gerror("findcbcinarea2d");   // retrie.c:244-246
}
```

The 1984 timestamp confirms this is architectural, not accidental.

---

### 4. `crumqualifies2d` — The Sole Homedoc Check, Always Skipped

The only per-crum document-identity test in the retrieval tree walk:

```c
// retrie.c:274
if ((crumptr->height == 0) && infoptr && !tumblereq (&infoptr->homedoc,
    &(((type2dcbc *)crumptr)->c2dinfo.homedoc))) {
    return (FALSE);
}
```

Three conjuncts: leaf node, **`infoptr` non-NULL**, homedoc mismatch. Since `infoptr` is always NULL (see §3), the `&&` short-circuits before the tumbler comparison ever executes. The homedoc stored in every crum leaf is read but never compared. All subsequent tests in `crumqualifies2d` [retrie.c:282-301] are pure I-address range comparisons (`span1`, `span2` intervals).

---

### 5. `unpacksporgl` Confirms: ISPANID Clears Homedoc

When a link endset is stored as an ISPANID (a bare I-address span — the normal case for content links), `unpacksporgl` [sporgl.c:178-195] explicitly **zeroes** the homedoc field:

```c
if (((typeitemheader *)sporglptr)->itemid == ISPANID) {
    movetumbler (&((typeispan *)sporglptr)->stream, streamptr);
    movetumbler (&((typeispan *)sporglptr)->width, widthptr);
    tumblerclear (&infoptr->homedoc);   // sporgl.c:183 — homedoc := 0
}
```

A SPORGLID (version-relative reference) would carry a `sporgladdress` for the home document [sporgl.c:187], but ISPANID endsets carry no document identity at all — only the kluge path (disabled) would have set one.

---

### Summary

| Step | What happens | Document A's POOM involved? |
|------|-------------|---------------------------|
| `docopy` converts specset | I-addresses reused verbatim [do2.c:24-26] | No |
| `insertpm` into doc B | New V-addresses; same I-addresses [orglinks.c:105-113] | No |
| `insertspanf` into global spanfilade | I-address ranges registered for doc B | No |
| `sporglset2linksetinrange` query | `infoptr = NULL` always [sporgl.c:255] | No |
| `retrieverestricted` → `findcbcinarea2d` | `infoptr` stays NULL; debug trap if ever non-NULL [retrie.c:244-246] | No |
| `crumqualifies2d` | homedoc check gated on `infoptr != NULL` — never runs [retrie.c:274] | No |

**The query surfaces the endset for B purely through shared I-address identity.** Both documents carry the same I-address ranges in the global spanfilade; the link whose endset covers that range is found by I-address interval intersection alone. Document A's POOM is not referenced, document identity is not checked anywhere in the path, and the code contains a debug-mode error trap placed in 1984 to prevent the document-scoped path from ever being accidentally re-entered.
