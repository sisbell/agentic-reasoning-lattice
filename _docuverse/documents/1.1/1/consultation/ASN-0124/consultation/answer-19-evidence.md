## Question 19 [evidence]

> Is the FINDDOCSCONTAINING result stable under INSERT in a returned document — since DOCISPAN entries are keyed by I-address rather than V-position, do V-shifts from edits in any document leave the membership of the result set unchanged?

## KB Synthesis

Yes — FINDDOCSCONTAINING results for any pre-existing I-address range Q are fully stable under INSERT in any document. Three independent properties combine to guarantee this.

**V-shifts never touch the DOCISPAN index**

INSERT modifies POOM entries (V→I mappings), not spanfilade entries (I→doc mappings). The two structures are separate: the POOM lives in the granfilade per-document orgl, the DOCISPAN lives in the spanfilade. [SS-POOM-MUTABILITY] makes this explicit — the POOM is the only mutable layer; the spanfilade is write-only. When INSERT shifts V-positions within `[blade[0], blade[1])` [SS-TWO-BLADE-KNIFE, FC-SUBSPACE], it displaces POOM crums' `cdsp.dsas[V]` fields but never touches a single spanfilade entry. DOCISPAN entries store only I-addresses and document ISAs; they contain no V-position component at all [SS-DOCISPAN].

**INSERT allocates fresh I-addresses outside Q**

INSERT's new content receives I-addresses strictly greater than all previously allocated I-addresses ([INV-MONOTONIC], [INV-NO-IADDR-REUSE]). A pre-existing query range Q consists of I-addresses allocated before the INSERT. The newly inserted I-addresses are always outside Q. Therefore INSERT cannot add any document to FINDDOCSCONTAINING(Q): the new DOCISPAN entry created by INSERT maps the fresh I-addresses (outside Q) to the inserting document, which says nothing about membership in Q.

This holds regardless of *which* document performs the INSERT. Even if document E inserts content, those fresh I-addresses are disjoint from Q, so FINDDOCSCONTAINING(Q) is unchanged [ST-INSERT, FC-CONTENT-SPANF-ISOLATION].

**The spanfilade is strictly append-only**

Because no `deletespanf` function exists and no operation calls one, existing DOCISPAN entries can never be removed [INV-SPANF-WRITE-ONLY]. Specifically: `∀ t₁ < t₂ : spanf_entries(t₁) ⊆ spanf_entries(t₂)`. So even if a document's POOM no longer references some I-addresses in Q (because they were deleted), the DOCISPAN entry persists. INSERT cannot remove documents from the result set.

**Summary**

For any pre-existing I-address range Q and any INSERT operation on any document:
- No existing DOCISPAN entry in Q is modified (append-only spanfilade)
- No new document is added to FINDDOCSCONTAINING(Q) (fresh I-addresses outside Q)
- V-position shifts are irrelevant (DOCISPAN keyed on I-address, not V-address)

The membership of FINDDOCSCONTAINING(Q) is invariant under INSERT. The only operations that can expand FINDDOCSCONTAINING(Q) are those that share existing I-addresses from Q into a new document: specifically VCOPY/transclusion ([ST-VCOPY]) and CREATENEWVERSION ([ST-VERSION-CREATE], [ST-VERSION]), both of which write new DOCISPAN entries mapping Q's I-addresses to the destination document.

---

## Code Exploration

I now have everything needed for a complete, sourced answer.

---

## FINDDOCSCONTAINING Stability Under INSERT: Full Analysis

**Short answer**: Yes. V-shifts caused by INSERT leave FINDDOCSCONTAINING membership completely unchanged. The invariant holds by construction: the spanfilade's DOCISPAN entries are keyed by I-address in SPANRANGE, a dimension that INSERT never touches.

---

### 1. The Two Enfilades and Their Dimensions

`wisp.h:15-16` defines the spanfilade's two dimensions:

```c
#define ORGLRANGE 0   /* dimension 0: document ISA (with type tag) */
#define SPANRANGE 1   /* dimension 1: I-address of content */
```

And the POOM's dimensions (`wisp.h:19-20`):

```c
#define I  0    /* dimension 0: permascroll address */
#define V  1    /* dimension 1: virtual (document) position */
```

The spanfilade (SPAN enfilade) has no V-dimension. The POOM has both I and V.

---

### 2. How DOCISPAN Entries Are Written

Every INSERT ultimately flows through `doinsert` [do1.c:87-123]:

```c
ret = (inserttextingranf(taskptr, granf, &hint, textset, &ispanset)
    && docopy (taskptr, docisaptr, vsaptr, ispanset)
```

`inserttextingranf` → `inserttextgr` [granf2.c:83-109] calls `findisatoinsertgr` to find the next available I-address — always a fresh address beyond anything already allocated for that document — then records the text in the granfilade and returns a new `ispanset` holding those new I-addresses [granf2.c:102-107]:

```c
movetumbler (&spanorigin, &ispanptr->stream);
tumblersub (&lsa, &spanorigin, &ispanptr->width);
```

`docopy` [do1.c:45-65] then calls `insertspanf` [do1.c:62]:

```c
insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN)
```

Inside `insertspanf` [spanf1.c:22-51], the two dimensions of the spanfilade crum are set as:

```c
prefixtumbler (isaptr, spantype, &crumorigin.dsas[ORGLRANGE]);  /* ORGLRANGE = docISA + DOCISPAN tag */
tumblerclear (&crumwidth.dsas[ORGLRANGE]);
...
movetumbler (&lstream, &crumorigin.dsas[SPANRANGE]);  /* SPANRANGE = I-address */
movetumbler (&lwidth,  &crumwidth.dsas[SPANRANGE]);   /* SPANRANGE width = I-span width */
insertnd(taskptr,(typecuc*)spanfptr,&crumorigin,&crumwidth,&linfo,SPANRANGE);
```

The key: `lstream` and `lwidth` are taken directly from the `ispanset` [spanf1.c:27-28], which holds I-addresses. **The V-position `vsaptr` never appears in a spanfilade crum.**

---

### 3. What INSERT Does to V-Positions (and What It Doesn't Do)

The POOM insert path is `insertpm` [orglinks.c:75-134] → `insertnd(... V)` [insertnd.c:130] → `makegappm` [insertnd.c:54, defined at insertnd.c:124-172].

`makegappm` shifts crums that come after the insertion point by adjusting only the V-displacement:

```c
/* insertnd.c:162 */
tumbleradd(&ptr->cdsp.dsas[V], &width->dsas[V], &ptr->cdsp.dsas[V]);
```

This adjusts `dsas[V]` — the V-dimension — of POOM crums. It never touches `dsas[I]`. The spanfilade crums have no `dsas[V]` at all. **There is no path from `makegappm` into the spanfilade.**

---

### 4. How FINDDOCSCONTAINING Queries the Spanfilade

`dofinddocscontaining` [do1.c:15-23] → `finddocscontainingsp` [spanf1.c:151-188].

`finddocscontainingsp` first constructs a `docspace` probe in ORGLRANGE, typed as DOCISPAN:

```c
/* spanf1.c:168-169 */
tumblerincrement (&docspace.stream, 0, DOCISPAN, &docspace.stream);
tumblerincrement (&docspace.width, 0, 1, &docspace.width);
```

Then for each I-span in the query's `ispanset`, it calls `retrieverestricted` with the I-span in SPANRANGE:

```c
/* spanf1.c:171 */
context = retrieverestricted ((typecuc*)spanf, &docspace, ORGLRANGE, ispanset, SPANRANGE, (typeisa*)NULL);
```

This is a 2-D intersection query on the spanfilade:
- **ORGLRANGE constraint**: must be a DOCISPAN entry (type=4)
- **SPANRANGE constraint**: must overlap the query's I-span

Document addresses are extracted from `c->totaloffset.dsas[ORGLRANGE]` [spanf1.c:173], not SPANRANGE. **V-position appears nowhere in this lookup.**

---

### 5. V→I Translation at Query Time (V-spec callers)

When FINDDOCSCONTAINING is called with a V-spec rather than a direct I-span, `specset2ispanset` [do2.c:14-46] calls `vspanset2ispanset` [do2.c:36] → `permute(taskptr, orgl, vspanset, V, ispansetptr, I)` [orglinks.c:397-402].

`permute` [orglinks.c:404-422] → `span2spanset` [orglinks.c:425-454] walks the POOM via `retrieverestricted(orgl, restrictionspanptr, V, NULL, I, NULL)` to find which I-spans correspond to the given V-spans *at the moment of the call*.

The V→I map lives in the POOM, and INSERT does modify it (via `makegappm`). But this affects *which V-span maps to which I-span* — not the I-span-keyed spanfilade. After an INSERT, the same V-position may map to a different I-address, but:

- Content that existed before the INSERT still has its original I-addresses
- The DOCISPAN entries for that content are still present, unchanged
- A query with the content's V-position (even if shifted) will translate through the POOM to the same original I-addresses
- The spanfilade lookup will return the same document set

---

### 6. What Could Change the Result Set

Only two operations can add or remove documents from FINDDOCSCONTAINING results:

1. **A new `insertspanf` call** [spanf1.c:15-54] — which happens only when content is actually inserted into a document (`docopy` at do1.c:62 and do1.c:79), not as a V-shift side effect.

2. **Note on DELETE**: `dodeletevspan` [do1.c:158-167] removes content from the POOM via `deletevspanpm` [orglinks.c:145-152], but does **not** call `insertspanf` or any equivalent removal from the spanfilade. This means deleted content's DOCISPAN entries persist — a separate invariant with its own implications, but unrelated to the V-shift question.

---

### Summary

The claim in the question is correct and holds unconditionally:

- DOCISPAN entries in the spanfilade are indexed by **I-address** in SPANRANGE [`spanf1.c:49-51`]
- INSERT's V-shift (`makegappm`) modifies only **`dsas[V]`** of POOM crums [`insertnd.c:162`]
- The spanfilade has no V-dimension [`wisp.h:15-16`]; there is no coupling between POOM V-shifts and spanfilade state
- FINDDOCSCONTAINING queries the spanfilade exclusively by I-address [`spanf1.c:171`]
- New I-addresses allocated by INSERT are fresh and distinct from all prior I-addresses [`granf2.c:158-181`], so a new INSERT cannot retroactively make an existing document appear in or disappear from results for a query targeting pre-existing I-spans

V-shifts from edits in *any* document — whether a document in the result set or not — leave the FINDDOCSCONTAINING membership for a fixed I-span query unchanged.
