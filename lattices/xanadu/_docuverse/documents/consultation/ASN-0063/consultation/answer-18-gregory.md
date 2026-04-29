## Question 18 [gregory]

> If CREATELINK is called with endsets referencing I-addresses that no current POOM maps to (content that was deleted from all documents but persists in the granfilade), does the link creation succeed, and are the resulting spanfilade entries valid for future discovery if that content is later transcluded?

## KB Synthesis

## Short answer

CREATELINK cannot succeed through the normal API with endsets referencing I-addresses that no current POOM maps to — but if a link reaches that state through post-creation deletion, its spanfilade entries remain permanently valid for future discovery via transclusion.

---

## Part 1: Can CREATELINK produce endsets with unreferenced I-addresses?

The FEBE CREATELINK API takes V-span specsets as endpoint inputs, not I-addresses. The path is: V-spans → `vspanset2sporglset` → `vspanset2ispanset` → `retrieverestricted`, which walks the home document's POOM to resolve V-positions to I-addresses [SS-VSPAN-TO-SPORGL, ST-LINK-CREATE].

From [INV-ITOV-FILTERING] and [SS-FOLLOWLINK]: if `retrieverestricted` finds no POOM entry for a given V-position, it returns NULL and that I-address is silently dropped. If all endpoint I-addresses are unreferenced, the resulting sporglset is empty. An empty (zero-width) endset passed to link creation crashes the backend (Bug 0017) [PRE-LINK-CREATE].

**Conclusion:** Through the normal interface, CREATELINK cannot produce endsets with unreferenced I-addresses — the V-to-I conversion gate prevents it.

The relevant scenario is the inverse: a link is created while the content exists in a POOM, then the content is subsequently deleted from all documents. The link then holds endsets whose I-addresses are no longer mapped by any POOM — the standard orphaned link state [EC-ORPHANED-LINK, EC-GHOST-LINK].

---

## Part 2: Are the spanfilade entries valid for future discovery?

**Yes, unconditionally.**

Three permanent-layer properties guarantee this:

**The link orgl persists.** No operation removes entries from I-space. The link's orgl at its allocated I-address is permanent [INV-LINK-PERMANENCE].

**The spanfilade entries persist.** `insertendsetsinspanf` writes entries at link creation time. No delete mechanism exists anywhere in `spanf1.c` or `spanf2.c`. The entries are write-only [INV-SPANF-WRITE-ONLY]. The mapping `α → link_ISA` survives indefinitely in the spanfilade regardless of what happens to any POOM.

**Discovery is purely I-address intersection.** `find_links` converts the search specset to I-addresses and intersects against the spanfilade [SS-FIND-LINKS]. If any document later acquires a POOM mapping to those I-addresses — via transclusion — the I-address intersection fires and the link is discovered [INT-LINK-TRANSCLUSION].

From [EC-GHOST-LINK]: "Reconstitution is always possible since I-addresses are permanent. VCOPY `a` into new document D2 → `poom.D2(1.1) = a` → FOLLOWLINK(L, TO, D2) works." The granfilade retains the content bytes at those I-addresses forever [INV-IADDR-IMMUTABILITY, INV-NO-IADDR-REUSE], so the I-addresses are both discoverable via spanfilade and resolvable via granfilade once any POOM maps to them.

**The lifecycle:**
```
t0: CREATELINK(source_vspan, target_vspan)
    → spanfilade: α₁..αₙ → link_ISA (permanent)
    
t1: DELETE content from all documents
    → all POOMs: α₁..αₙ no longer mapped
    → find_links → [] (no POOM to match against)
    → follow_link → [] (no V-position to report)
    → spanfilade: α₁..αₙ → link_ISA (UNCHANGED)
    
t2: VCOPY content sharing α₁..αₙ into new document D
    → poom.D: v → α₁..αₙ now mapped
    → find_links(D, v) → [link_ISA] (spanfilade match fires again)
```

This follows from the three-layer model [SS-THREE-LAYER-MODEL]: I-space and spanfilade are permanent; POOM presence is transient. Link discoverability is gated on POOM state, but the spanfilade entries standing behind that gate are never invalidated.

---

## Code Exploration

I now have a complete picture from the source. Here is the full answer.

---

## CREATELINK with Orphaned I-Addresses: Source Analysis

### Framing: What "I-addresses that no current POOM maps to" means

When content is deleted from all documents, `dodeletevspan` [orglinks.c:145-152] calls `deletend` only on the document's POOM:

```c
bool deletevspanpm(typetask *taskptr, tumbler *docisaptr, typeorgl docorgl, typevspan *vspanptr)
{
    if (iszerotumbler(&vspanptr->width))
        return (FALSE);
    deletend((typecuc*)docorgl, &vspanptr->stream, &vspanptr->width, V);
    logbertmodified(docisaptr, user);
    return (TRUE);
}
```

There is no corresponding deletion from the granfilade. Granfilade content — inserted via `inserttextgr` [granf2.c:83-109] using `insertseq` — is never removed. The I-addresses assigned to that content remain permanently valid in the content store.

---

### How the Protocol Accepts Raw I-Spans

`getspecset` [get2.c:162-192] explicitly offers the caller a choice:

```c
prompt (taskptr,"a span? ");
if(!getbool(taskptr,&type))
    return(FALSE);
if(type) {
    specset=(typespec *)taskalloc(taskptr,sizeof(typespan));
    if (!getspan(taskptr,specset,ISPANID))   // direct I-span
        return(FALSE);
}else{
    specset=(typespec *)taskalloc(taskptr,sizeof(typevspec));
    if (!getvspec(taskptr,specset))           // V-spec (doc + V-spans)
        return(FALSE);
}
```

A client can bypass V→I lookup entirely by supplying raw ISPANID items as endsets — including I-addresses that correspond to content deleted from all documents.

---

### Part 1: Does CREATELINK Succeed?

`docreatelink` [do1.c:195-221] runs this chain:

```c
createorglingranf(taskptr, granf, &hint, linkisaptr)          // 1
&& tumbler2spanset(taskptr, linkisaptr, &ispanset)             // 2
&& findnextlinkvsa(taskptr, docisaptr, &linkvsa)               // 3
&& docopy(taskptr, docisaptr, &linkvsa, ispanset)              // 4
&& findorgl(taskptr, granf, linkisaptr, &link, NOBERTREQUIRED) // 5
&& specset2sporglset(taskptr, fromspecset, &fromsporglset, NOBERTREQUIRED) // 6
&& specset2sporglset(taskptr, tospecset, &tosporglset, NOBERTREQUIRED)     // 7
&& specset2sporglset(taskptr, threespecset, &threesporglset, NOBERTREQUIRED)// 8
&& setlinkvsas(&fromvsa, &tovsa, &threevsa)                    // 9
&& insertendsetsinorgl(...)                                     // 10
&& insertendsetsinspanf(...)                                    // 11
```

The critical step is **6–8**. `specset2sporglset` [sporgl.c:14-33]:

```c
for (; specset; specset = ...) {
    if (((typeitemheader *)specset)->itemid == ISPANID) {
        *sporglsetptr = (typesporglset)specset;   // passed through, NO validation
        sporglsetptr = (typesporglset *)&((typeitemheader *)specset)->next;
    } else if (((typeitemheader *)specset)->itemid == VSPECID) {
        if (!(sporglsetptr = vspanset2sporglset(taskptr, &((typevspec *)specset)->docisa,
              ((typevspec *)specset)->vspanset, sporglsetptr, type))) {
            return (FALSE);
        }
    }
}
```

**For ISPANID items, the code performs zero validation.** The I-span is taken as-is and placed directly into the sporglset. There is no lookup, no POOM consultation, no check that the I-address names content in any live document.

**Step 10** — `insertendsetsinorgl` [do2.c:130-149] → `insertpm` [orglinks.c:75-134] — stores the endsets in the link's own POOM. `insertpm` calls `unpacksporgl` [sporgl.c:178-203], which handles ISPANID correctly by reading `stream` and `width` directly. It only fails if the width is zero; a non-zero I-span proceeds.

**Step 11** — `insertendsetsinspanf` [do2.c:116-128] → `insertspanf` [spanf1.c:15-54] — inserts into the global spanfilade:

```c
if (((typeitemheader *)sporglset)->itemid == ISPANID) {
    movetumbler(&((typeispan *)sporglset)->stream, &lstream);
    movetumbler(&((typeispan *)sporglset)->width, &lwidth);
    movetumbler(isaptr, &linfo.homedoc);  // homedoc = link's own ISA
} ...
movetumbler(&lstream, &crumorigin.dsas[SPANRANGE]);
movetumbler(&lwidth, &crumwidth.dsas[SPANRANGE]);
insertnd(taskptr, (typecuc*)spanfptr, &crumorigin, &crumwidth, &linfo, SPANRANGE);
```

The I-address is recorded in SPANRANGE, the link address (prefixed with LINKFROMSPAN / LINKTOSPAN / LINKTHREESPAN) in ORGLRANGE.

**Conclusion: link creation succeeds unconditionally for ISPANID endsets.** The link is fully formed in the granfilade, its POOM contains the endset spans, and the global spanfilade has entries keyed on the provided I-addresses.

---

### The V-Spec Path Behaves Differently

For completeness: if the client instead supplies a VSPECID specset pointing to content that has been deleted from the document, `vspanset2sporglset` [sporgl.c:35-65] calls `vspanset2ispanset` via `permute` [orglinks.c:404-422] → `span2spanset` [orglinks.c:425-454] → `retrieverestricted` on the document's POOM. Since the deletion removed the V→I mapping from the POOM, `retrieverestricted` returns no context, `span2spanset` produces nothing, and the sporglset is empty. `insertspanf`'s loop over an empty sporglset is a no-op. The link is created but no endset entries appear in the spanfilade. **This case does not produce discoverable links.**

---

### Part 2: Are the Spanfilade Entries Valid for Future Discovery?

When the content is later transcluded into a new document:

1. `docopy` [do1.c:45-65] → `insertpm` adds the V→I mapping to the new document's POOM, and `insertspanf(..., DOCISPAN)` records the document-content relationship in the spanfilade.

2. A subsequent FIND query calls `dofindlinksfromtothreesp` [do1.c:348-353] → `findlinksfromtothreesp` [spanf1.c:56-103] → for each endset type, calls `sporglset2linkset` [sporgl.c:222-237] → `sporglset2linksetinrange` [sporgl.c:239-269]:

```c
for (; sporglset; sporglset = ...) {
    if (FALSE/*kluge*/ && ((typeitemheader *)sporglset)->itemid == SPORGLID) {
        infoptr = &linfo;
        movetumbler(&((typesporgl *)sporglset)->sporgladdress, &linfo.homedoc);
    } else
        infoptr = NULL;    // always NULL — the FALSE short-circuits this branch
    ...
    context = retrieverestricted(spanfptr, (typespan*)sporglset, SPANRANGE,
                                 &range, ORGLRANGE, (typeisa*)infoptr);
    for (c = context; c; c = c->nextcontext) {
        beheadtumbler(&c->totaloffset.dsas[ORGLRANGE], &linksa);
        onlinklist(taskptr, linksetptr, &linksa);
    }
}
```

The `FALSE&&SPORGLID` branch is permanently disabled — `infoptr` is always NULL. Discovery calls `retrieverestricted` with a null `docisaptr`, which means `findcbcinarea2d` [retrie.c:229-268] receives a null `infoptr`, and the `crumqualifies2d` homedoc filter [retrie.c:274-279] is skipped entirely:

```c
if ((crumptr->height == 0) && infoptr &&
    !tumblereq(&infoptr->homedoc, &(((type2dcbc *)crumptr)->c2dinfo.homedoc))) {
    return (FALSE);  // only applies when infoptr != NULL
}
```

Discovery is therefore **purely I-address based**. The spanfilade entries created with orphaned I-addresses — regardless of whether `homedoc` was set to the link's ISA or a source document's ISA — are found by any query that overlaps those I-addresses in SPANRANGE, constrained to the appropriate LINKFROMSPAN / LINKTOSPAN / LINKTHREESPAN subspace.

When the content is transcluded, the new document's POOM maps its V-spans to the same I-addresses. `vspanset2sporglset` recovers those I-addresses and passes them to `sporglset2linksetinrange`, which matches against the spanfilade entries created during the original CREATELINK. **The entries are valid and the links are discovered.**

---

### Summary

| Condition | CREATELINK succeeds? | Spanfilade entries created? | Future discovery works? |
|-----------|---------------------|----------------------------|------------------------|
| Endsets as direct ISPANID (I-spans with no current POOM mapping) | **Yes** — no validation in `specset2sporglset` [sporgl.c:20-22] | **Yes** — `insertspanf` [spanf1.c:49-51] stores I-address in SPANRANGE unconditionally | **Yes** — discovery is purely I-address based; homedoc filtering is disabled [retrie.c:274-279] |
| Endsets as VSPECID pointing to deleted content | Yes (link is created) | **No** — empty sporglset from failed V→I permutation | **No** — no entries to find |

The design is intentional at the granfilade level: content in the granfilade is **permanent and append-only**. The I-address space is the durable identity fabric. CREATELINK with direct I-addresses creates a relationship between content identities, not between document positions. When that content is later made visible again through transclusion into any document, the link relationship correctly surfaces — because the spanfilade was indexed on identity, not on visibility.

The one difference in how the entries are stored: for ISPANID endsets, `insertspanf` [spanf1.c:29] records `homedoc = linkisa` (the link's own address), whereas for SPORGLID endsets (converted from V-specs), it records `homedoc = sporgladdress` (the source document's ISA) [spanf1.c:33]. This distinction is currently inert — the homedoc field in the bottom crum is stored but never consulted during retrieval, because the `infoptr` path in `sporglset2linksetinrange` [sporgl.c:251] is unconditionally dead code.
