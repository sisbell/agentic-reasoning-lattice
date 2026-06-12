## Question 17 [evidence]

> After CREATENEWVERSION, are the DOCISPAN entries created in the spanfilade for the new version's address one-per-contiguous-I-span mirroring the source's spans, and do they coexist with (rather than replace or reference) the source's own DOCISPAN entries for the same I-addresses?

## KB Synthesis

## CREATENEWVERSION and DOCISPAN Entries

**Yes to both parts of the question.** Here is the synthesis:

### 1. One DOCISPAN entry per contiguous I-span

`CREATENEWVERSION` uses the path `docopyinternal` → `specset2ispanset` → `insertpm` + `insertspanf` [ST-VERSION, Finding 0077]. The `insertspanf` call follows the same granularity rule as any COPY operation:

> DOCISPAN entries in the spanfilade have per-span granularity, not per-byte. `insertspanf` iterates over the `ispanset` linked list and makes one `insertnd` call per `typeispan` struct. [SS-DOCISPAN, Finding 0047]

So if the source's text subspace maps to N contiguous I-spans (e.g., fragmented by prior edits or transclusions), the version receives exactly N DOCISPAN entries — one per contiguous I-address run. A pristine document with a single contiguous V-span produces 1 DOCISPAN entry for the version.

Note also that CREATENEWVERSION copies **only the text subspace** (1.x), not the link subspace (2.x) [ST-VERSION-CREATE, Finding 0046], so DOCISPAN entries are created only for text I-spans.

### 2. Coexistence with the source's DOCISPAN entries

The spanfilade is unconditionally append-only:

> No deletion function exists anywhere in the spanf codebase. The spanfilade is a write-only (append-only) index. [INV-SPANF-WRITE-ONLY, Finding 0057]

When `insertspanf` is called during `docopyinternal`, it is passed the **version's** document ISA (d'), not the source's. So the new entries record `{I-address-range → d'}`. The source's existing entries recording `{I-address-range → d}` are untouched.

Both sets persist permanently and independently. This is the mechanism behind observable cross-version behavior: `FINDDOCSCONTAINING` on any I-address from the source returns both d and d' [INV-IADDRESS-PERMANENT, Finding 0023], and `find_links` discovers links via shared I-addresses in both documents [INT-LINK-VERSION, Finding 0046].

The `insertspanf` path has no deduplication or replacement logic — it simply appends. A single I-address range may therefore appear in the spanfilade multiple times, once per document that has ever placed content at those addresses via INSERT, COPY, or CREATENEWVERSION [INV-SPANF-GROWTH, Finding 0047].

### Summary

| Property | Answer |
|----------|--------|
| Granularity of version's DOCISPAN entries | One per contiguous I-span in source's text vspan |
| Mirror source's I-span structure? | Yes — same `specset2ispanset` result drives both POOM insertion and DOCISPAN creation |
| Source's existing DOCISPAN entries removed? | No — spanfilade is append-only, no deletion exists |
| Source's entries updated to reference version? | No — version gets its own independent entries tagged with d' |
| Both sets coexist? | Yes — permanently and independently |

---

## Code Exploration

I now have all the evidence needed. Here is the complete answer.

---

## CREATENEWVERSION: DOCISPAN Entry Creation in the Spanfilade

### The Call Chain

`createnewversion` [fns.c:289] dispatches to `docreatenewversion` [do1.c:260]. The relevant section:

```c
// do1.c:281-293
if (!doretrievedocvspanfoo (taskptr, isaptr, &vspan)) {
    return FALSE;
}
vspec.next = NULL;
vspec.itemid = VSPECID;
movetumbler(isaptr, &vspec.docisa);
vspec.vspanset = &vspan;

addtoopen(newisaptr, user, TRUE, WRITEBERT);
docopyinternal(taskptr, newisaptr, &vspan.stream, &vspec);
```

`doretrievedocvspanfoo` retrieves the source document's full V-span (the `stream` tumbler for the vsa, and `vspan` as the content descriptor). `docopyinternal` [do1.c:66] then runs the full copy pipeline on behalf of the new document's ISA (`newisaptr`):

```c
// do1.c:74-79
if (!specset2ispanset (taskptr, specset, &ispanset, NOBERTREQUIRED)) return FALSE;
if (!findorgl (taskptr, granf, docisaptr, &docorgl, NOBERTREQUIRED)) return FALSE;
if (!acceptablevsa (vsaptr, docorgl)) return FALSE;
if (!asserttreeisok(docorgl)) return FALSE;
if (!insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset)) return FALSE;
if (!insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN)) return FALSE;
```

Here `docisaptr` is `newisaptr` — the **new** document's ISA throughout.

---

### Question 1: Are the DOCISPAN entries one-per-contiguous-I-span?

**Yes. The granularity is one I-span per bottom-crum leaf node of the source POOM.**

`specset2ispanset` [do2.c:14] processes the `vspec` built from the source's V-span and calls:

```c
// do2.c:35-36
findorgl (taskptr, granf, &((typevspec *)specset)->docisa, &docorgl, type)
&& (ispansetptr = vspanset2ispanset (taskptr, docorgl, ((typevspec *)specset)->vspanset, ispansetptr))
```

`vspanset2ispanset` [orglinks.c:397-402] delegates to `permute` in the V→I direction. `permute` [orglinks.c:404-422] loops over each source V-span and calls `span2spanset`. `span2spanset` [orglinks.c:425-453] calls:

```c
// orglinks.c:435
context = retrieverestricted((typecuc*)orgl, restrictionspanptr, restrictionindex, (typespan*)NULL, targindex, (typeisa*)NULL);
```

`retrieverestricted` [retrie.c:56] dispatches to `retrieveinarea` → `findcbcinarea2d`, which traverses the source document's POOM enfilade and returns one `typecontext` per **bottom-crum leaf node** that overlaps the source V-span.

For each context, `context2span` [context.c:176-212] is called:

```c
// context.c:186-207
movetumbler (&restrictionspanptr->stream, &lowerbound);
tumbleradd (&lowerbound, &restrictionspanptr->width, &upperbound);
prologuecontextnd (context, &grasp, &reach);
if (tumblercmp (&grasp.dsas[idx1], &lowerbound) == LESS) {
    tumblerincrement (&grasp.dsas[idx2], 0, (INT) tumblerintdiff(&lowerbound, &grasp.dsas[idx1]), &grasp.dsas[idx2]);
}
if (tumblercmp (&reach.dsas[idx1], &upperbound) == GREATER) {
    tumblerincrement (&reach.dsas[idx2], 0, - tumblerintdiff (&reach.dsas[idx1], &upperbound), &reach.dsas[idx2]);
}
movetumbler (&grasp.dsas[idx2], &foundspanptr->stream);
tumblersub(&reach.dsas[idx2],&grasp.dsas[idx2],&foundspanptr->width);
```

This clips each leaf node's I-range to the source V-span boundary (handling the partial-overlap case at both ends), then emits one `typespan` (I-span) per leaf node. The resulting ispanset therefore has **exactly one I-span per contiguous I-address block** represented by the source POOM's leaf segmentation, clipped at the source's edges. These mirror the source's own atomic segments, not some independent granularity.

---

### Question 2: Do the new document's entries coexist with the source's?

**Yes. They are independent entries in the same spanfilade, indexed by different ORGLRANGE keys, with no mutual reference.**

#### ORGLRANGE key construction

`insertspanf` [spanf1.c:22]:

```c
prefixtumbler (isaptr, spantype, &crumorigin.dsas[ORGLRANGE]);
```

where `isaptr` is `newisaptr` (the new document's ISA) and `spantype` is `DOCISPAN`. `prefixtumbler` [tumble.c:641-651] builds the ORGLRANGE key by prepending the spantype integer and shifting the ISA:

```c
tumblerclear (&temp1);
temp1.mantissa[0] = bint;        // DOCISPAN prefix
movetumbler (aptr, &temp2);
if (!iszerotumbler (&temp2))
    temp2.exp -= 1;
tumbleradd (&temp1, &temp2, cptr);
```

The source document's existing DOCISPAN entries were inserted by the same `insertspanf` path when the source was originally written, using `prefixtumbler(source_isa, DOCISPAN)`. Since `new_isa ≠ source_isa`, the two sets of entries occupy **distinct, non-overlapping regions of the ORGLRANGE dimension** of the 2D spanfilade.

#### Insertion is purely additive

`insertspanf` calls `insertnd` [spanf1.c:51], which for the `SPAN` case [insertnd.c:63] calls `doinsertnd` → `insertmorend` → `insertcbcnd`. `insertcbcnd` [insertnd.c:249-275] first checks `isanextensionnd` [insertnd.c:301-309]:

```c
// insertnd.c:305-306
if (!tumblereq (&infoptr->homedoc, &((type2dcbc *)ptr)->c2dinfo.homedoc))
    return (FALSE);
```

The `homedoc` field in the new entry is `new_isa` (`linfo.homedoc = isaptr` at [spanf1.c:29]). Any existing source-document entry has `homedoc = source_isa`. Since these differ, `isanextensionnd` returns `FALSE` immediately — **no new-document span can ever be merged into a source-document span**. The new entries cannot accidentally consolidate with the source's entries even when I-addresses are adjacent.

When no extension is possible, `insertcbcnd` creates a new crum node and `adopt`s it:

```c
// insertnd.c:260-263
new = createcrum (0, (INT)father->cenftype);
reserve (new);
adopt (new, SON, (typecorecrum*)father);
dspsub (origin, grasp, &new->cdsp, (INT)father->cenftype);
```

No existing nodes are deleted, overwritten, or redirected. The source's DOCISPAN entries remain structurally unmodified.

---

### Summary

| Aspect | Answer | Key Evidence |
|---|---|---|
| **Granularity** | One I-span per bottom-crum leaf of the source POOM, clipped at V-span boundaries | `context2span` [context.c:176]; `span2spanset` [orglinks.c:439-444] |
| **Mirrors source spans** | Yes — the leaf segmentation of the source enfilade is the granularity; `context2span` performs clipping, not re-chunking | `prologuecontextnd` + clamp logic [context.c:188-203] |
| **Coexist vs. replace** | Coexist — new entries are separate leaf nodes under a different ORGLRANGE key | `prefixtumbler(newisa, DOCISPAN)` ≠ `prefixtumbler(srcisa, DOCISPAN)` [spanf1.c:22; tumble.c:641] |
| **Coexist vs. reference** | Coexist — the source's entries are not modified, dereferenced, or pointed to | `isanextensionnd` [insertnd.c:305-306]; `adopt` [insertnd.c:262] |
| **Merge prevention** | `homedoc` inequality guard prevents any cross-document span consolidation | `isanextensionnd` [insertnd.c:305] |

After CREATENEWVERSION, the spanfilade holds two independent families of DOCISPAN entries at the same I-addresses: one family keyed under `prefixtumbler(source_isa, DOCISPAN)`, another under `prefixtumbler(new_isa, DOCISPAN)`. Each family has the same I-span granularity (one entry per source POOM leaf, clipped at the source vspan boundary). They neither reference nor shadow each other — they are simply parallel records in different ORGLRANGE slices of the same 2D spanfilade enfilade.
