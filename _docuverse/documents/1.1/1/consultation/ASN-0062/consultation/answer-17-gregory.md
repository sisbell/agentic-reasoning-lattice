## Question 17 [gregory]

> When copying a specset containing multiple V-spans from different source documents, does `docopy` process each span independently against its respective source POOM, and does the target receive one contiguous V-range or multiple disjoint ranges corresponding to each source span?

## KB Synthesis

**Short answer:** `docopy` processes each VSpec against its own source document's POOM independently. The target receives **one contiguous V-range** (starting at the caller-specified insertion point), but the content is stored internally as multiple POOM crums — one per source provenance group — that cannot merge across source-document boundaries.

---

**Processing: each span against its own source POOM**

`specset2ispanset` converts each VSpec to I-spans by looking up V→I mappings in the document named by that VSpec's doc tumbler. Spans from different source documents therefore traverse different POOM trees independently. This is confirmed by the cross-document vcopy scenario in [ST-VCOPY (Finding 0003)]: "Cross-document vcopy works atomically; all spans are placed into the target in a single operation" — atomic here means the whole specset is submitted as one request, not that a single tree lookup handles all sources.

**Target V-addresses: contiguous**

Content from span 1 is placed at `[target_vpos, target_vpos + width₁)`, span 2 at `[target_vpos + width₁, target_vpos + width₁ + width₂)`, and so on in VSpec order [SS-SPECSET], [INV-SPECSET-ORDER]. The result is a single contiguous V-range in the target.

`retrieve_vspanset` confirms this: [INV-VSPAN-CONSOLIDATION] states the enfilade returns maximally consolidated spans, and contiguous V-addresses would be reported as a single span.

**Internal POOM crums: NOT merged across sources**

At the crum level, content from different source documents stays separate. `isanextensionnd()` at `insertnd.c:293-301` requires both V-contiguity AND matching `homedoc` before extending an existing crum. Content transcluded from doc A has a different `homedoc` than content from doc B, so they are stored as separate POOM crums even though their V-addresses are adjacent [INV-IADDR-PROVENANCE]:

> "crums from different source documents are never merged … the extension check's `homedoc` condition means crums from different source documents are never merged"

**Observable consequence**

`compare_versions` between the target and source A reveals only the A-derived portion; between target and source B reveals only the B-derived portion [ST-VCOPY (Finding 0003)]:

> "compare returns TWO shared regions — one per copied span"
> "per-span identity is preserved, not merged into a single region"

So from the caller's perspective the target has one contiguous V-span; from the identity/provenance perspective it has multiple independent I-address records with different origins — which is precisely what enables transitive content tracking [INV-TRANSITIVE-IDENTITY].

---

## Code Exploration

---

## Answer: How `docopy` handles a multi-source specset

### The call chain

`docopy` [`do1.c:45`] executes in two distinct phases:

```c
bool docopy(typetask *taskptr, typeisa *docisaptr, tumbler *vsaptr, typespecset specset)
{
    typeispanset ispanset;
    typeorgl docorgl;
    return (
       specset2ispanset (taskptr, specset, &ispanset, NOBERTREQUIRED)   // Phase 1
    && findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
    && acceptablevsa (vsaptr, docorgl)
    && insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset)          // Phase 2
    && insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN) );
}
```

---

### Phase 1 — `specset2ispanset`: each V-span is resolved against its own source POOM

`specset2ispanset` [`do2.c:14`] iterates over all specs in the specset:

```c
for (; specset; specset = (typespec *)((typeitemheader *)specset)->next) {
    ...
    } else if (((typeitemheader *)specset)->itemid == VSPECID) {
        if (!(
          findorgl (taskptr, granf, &((typevspec *)specset)->docisa, &docorgl, type)
        && (ispansetptr = vspanset2ispanset (taskptr, docorgl, ((typevspec *)specset)->vspanset, ispansetptr))))
            return (FALSE);
    }
}
```
[`do2.c:27–38`]

For each `VSPECID` in the specset, it calls `findorgl` with that spec's own `docisa`. If the specset has two V-specs referencing document A and document B, `findorgl` is called twice — once with A's ISA, once with B's ISA — yielding two separate POOM `orgl` handles. Then `vspanset2ispanset` (→ `permute` → `span2spanset` → `retrieverestricted`) uses each document's own POOM to translate its V-ranges to I-spans. **Yes: each V-span is processed against its respective source POOM.** The resulting I-spans are all chained into one flat `ispanset` linked list.

---

### Phase 2 — `insertpm`: all I-spans are packed into one contiguous V-range

`insertpm` [`orglinks.c:75`] receives the flat `ispanset` (passed as its `sporglset` argument) and iterates:

```c
for (; sporglset; sporglset = (typesporglset) sporglset->xxxxsporgl.next) {
    unpacksporgl (sporglset, &lstream, &lwidth, &linfo);
    movetumbler (&lstream, &crumorigin.dsas[I]);
    movetumbler (&lwidth,  &crumwidth.dsas[I]);
    movetumbler (vsaptr,   &crumorigin.dsas[V]);
    shift = tumblerlength (vsaptr) - 1;
    inc   = tumblerintdiff (&lwidth, &zero);
    tumblerincrement (&zero, shift, inc, &crumwidth.dsas[V]);
    insertnd (taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);
/**/tumbleradd (vsaptr, &crumwidth.dsas[V], vsaptr);    // ← advances vsaptr
}
```
[`orglinks.c:100–131`]

The critical line is **`orglinks.c:131`**: after inserting each I-span as a POOM crum, `vsaptr` is advanced by that crum's V-width. The next I-span gets the immediately following V-address. There are no V-gaps between spans from different source documents.

**Result: the target document receives one contiguous V-range** from the initial `vsaptr` to `vsaptr + Σ(all copied widths)`, regardless of how many source documents the specset spans.

---

### What about crum merging?

`isanextensionnd` [`insertnd.c:301`] checks whether two adjacent I-spans can be merged into the same POOM crum:

```c
bool isanextensionnd(typecbc *ptr, typedsp *offsetptr, typedsp *originptr, type2dbottomcruminfo *infoptr)
{
    if (!tumblereq (&infoptr->homedoc, &((type2dcbc *)ptr)->c2dinfo.homedoc))
        return (FALSE);
    ...
    return (lockeq (reach.dsas, originptr->dsas, ...));
}
```
[`insertnd.c:305–308`]

The `homedoc` field (from `type2dbottomcruminfo`, `wisp.h:108`) identifies the source document. However, because `docopy` calls `specset2ispanset` (not `specset2sporglset`), the items in the ispanset have `itemid == ISPANID`. When `unpacksporgl` processes an ISPANID item, it **zeroes the homedoc**:

```c
if (((typeitemheader *)sporglptr)->itemid == ISPANID) {
    movetumbler (&((typeispan *)sporglptr)->stream, streamptr);
    movetumbler (&((typeispan *)sporglptr)->width,  widthptr);
    tumblerclear (&infoptr->homedoc);    // ← homedoc = 0 for plain I-spans
}
```
[`sporgl.c:180–183`]

Contrast this with the SPORGLID path (used by `specset2sporglset` in `docreatelink`), which does preserve the `sporgladdress` as `homedoc` [`sporgl.c:187`].

So in the POOM crums written by `docopy`, all `c2dinfo.homedoc` fields are zero — the per-span source document identity is not preserved in the target's POOM structure. Spans from different source documents that happen to be I-adjacent (which is impossible since they come from different permascrolls) would be merged; in practice they are stored as separate crums simply because their I-ranges don't abut.

---

### Summary

| Question | Answer | Evidence |
|---|---|---|
| Does `docopy` process each V-span against its respective source POOM? | **Yes** — `specset2ispanset` calls `findorgl` with each spec's `docisa` separately | `do2.c:35` |
| Does the target receive contiguous or disjoint V-ranges? | **One contiguous V-range** — `insertpm` advances `vsaptr` after each I-span, packing all spans without gaps | `orglinks.c:131` |
| Is source document identity preserved in the target's POOM? | **No** — `specset2ispanset` produces plain ISPANID items; `unpacksporgl` zeros `homedoc` for ISPANID entries | `sporgl.c:183` |

The design collapses multi-source content into a flat contiguous V-span in the target. The V-space of the target grows by the total size of all copied content, contiguously, but the POOM crums record no memory of which source document each chunk came from.
