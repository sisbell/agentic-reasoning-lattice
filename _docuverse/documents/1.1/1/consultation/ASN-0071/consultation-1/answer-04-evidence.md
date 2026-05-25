## Question 4 [evidence]

> What is a minimal udanax-green scenario showing two documents sharing a single content I-address through transclusion, suitable for verifying that find returns both documents exactly once?

## KB Synthesis

## Minimal Two-Document Transclusion Scenario

### Setup

**Step 1 — Insert into source document A:**

```
SETACCOUNTAT(1.1.0.1)
CREATEDOCUMENT → A = 1.1.0.1.0.1
OPENDOCUMENT(A, WRITEBERT)
INSERT(A, vsa=1.1, text="hello")    # 5 bytes
CLOSEDOCUMENT(A)
```

This allocates 5 contiguous I-addresses α₁..α₅ in the granfilade and writes one DOCISPAN entry `(α₁, width=0.5) → A` to the spanfilade [ST-INSERT][SS-DOCISPAN].

**Step 2 — Transcode into destination document B:**

```
CREATEDOCUMENT → B = 1.1.0.1.0.2
OPENDOCUMENT(B, WRITEBERT)
COPY(source=VSpec(A, 1.1, 0.5), dest=B, at=1.1)
CLOSEDOCUMENT(B)
```

COPY shares the existing I-addresses α₁..α₅ — no new ones are allocated — and writes one DOCISPAN entry `(α₁, width=0.5) → B` [ST-VCOPY][SS-DOCISPAN].

### Verification query

```
FINDDOCSCONTAINING(VSpec(A, 1.1, 0.5)) → {A, B}
```

### Why exactly once per document

[SS-DOCISPAN] Finding 0047: `insertspanf` makes **one `insertnd` call per `typeispan`**. Since "hello" is 5 contiguous bytes, both INSERT and COPY each produce exactly one I-span, so each produces exactly one DOCISPAN entry. Neither document is registered more than once for this I-address range.

[INV-SPANF-WRITE-ONLY] guarantees the entries are not removed or deduplicated — both persist permanently.

### What to avoid

- Do **not** delete content afterward. [EC-STALE-SPANF-REFERENCE]: deletion does not remove DOCISPAN entries, so deleted content still appears in `FINDDOCSCONTAINING`, making the "exactly once" assertion meaningless if content is modified.
- Do **not** COPY a second time into B. A second COPY would write a second DOCISPAN entry for B over the same I-address range, and whether the spanfilade deduplicates this is not documented in the KB — safest to use exactly one INSERT and one COPY.

### Minimal invariants exercised

| Property | Citation |
|----------|----------|
| COPY shares I-addresses, does not allocate new ones | [ST-VCOPY] Finding 0002 |
| Both INSERT and COPY create DOCISPAN entries | [FC-CONTENT-SPANF-ISOLATION] Finding 0036 |
| DOCISPAN granularity is per-I-span, not per-byte | [SS-DOCISPAN] Finding 0047 |
| Spanfilade is append-only; entries persist | [INV-SPANF-WRITE-ONLY] Finding 0057 |
| Content identity is shared (not copied) by transclusion | [INV-TRANSITIVE-IDENTITY] |

---

## Code Exploration

Now I have everything needed. Here is the complete analysis.

---

## Minimal Transclusion + Find Scenario

### The Code Path

**Step 1 — Insert allocates fresh I-addresses**

`doinsert` [`do1.c:87-123`]:
```c
bool doinsert(typetask *taskptr, typeisa *docisaptr, tumbler *vsaptr, typetextset textset)
{
    makehint(DOCUMENT, ATOM, TEXTATOM, docisaptr, &hint);
    ret = (inserttextingranf(taskptr, granf, &hint, textset, &ispanset)
        && docopy (taskptr, docisaptr, vsaptr, ispanset)
    );
    return(ret);
}
```

`inserttextingranf` allocates one or more I-addresses in the granfilade and returns them as an `ispanset`. Then `docopy` (same function used by vcopy) records those I-addresses in two places:

- The document's **POOM enfilade** — mapping V-addresses to I-addresses via `insertpm` [`orglinks.c:75-134`]
- The **spanfilade** — recording that this I-span belongs to this document via `insertspanf`, with dimension tag `DOCISPAN` [`do1.c:62`]

**Step 2 — VCopy reuses the same I-addresses**

`docopy` [`do1.c:45-65`]:
```c
bool docopy(typetask *taskptr, typeisa *docisaptr, tumbler *vsaptr, typespecset specset)
{
    return (
       specset2ispanset (taskptr, specset, &ispanset, NOBERTREQUIRED)
    && ...
    && insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset)
    && insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN)
    ...
    );
}
```

When called for a `vcopy`:

1. `specset2ispanset` [`do2.c:14-46`] walks the source document's POOM enfilade (via `vspanset2ispanset` → `permute` → `span2spanset` → `retrieverestricted`) and resolves the source V-span back to its underlying I-addresses. These are the **same I-addresses** that were allocated during the original insert.
2. `insertpm` creates new POOM crums in the **destination document's** enfilade, pointing those same I-addresses at the destination's V-space.
3. `insertspanf` creates new spanfilade entries recording: I-span X now belongs to the **destination document** as well, with tag `DOCISPAN`.

After vcopy, the spanfilade contains two entries for the same I-address: one for source and one for dest.

**Step 3 — find_documents queries the spanfilade**

`finddocscontainingsp` [`spanf1.c:151-188`]:
```c
bool finddocscontainingsp(typetask *taskptr, typespanset ispanset, typelinkset *addresssetptr)
{
    headptr = addresssetptr;
    *addresssetptr = NULL;
    clear (&docspace, sizeof(typespan));
    tumblerincrement (&docspace.stream, 0, DOCISPAN, &docspace.stream);  // line 168
    tumblerincrement (&docspace.width, 0, 1, &docspace.width);
    for (; ispanset; ispanset = ispanset->next) {
        context = retrieverestricted((typecuc*)spanf, &docspace, ORGLRANGE,
                                      ispanset, SPANRANGE, (typeisa*)NULL);  // line 171
        for (c = context; c; c = c->nextcontext) {
            movetumbler (&c->totaloffset.dsas[ORGLRANGE], &docid);
            beheadtumbler (&docid, &document.address);
            if (isinlinklist(*headptr, &document.address))  // line 175
                continue;
            ...
            addresssetptr = (typelinkset *) onitemlist(...);
        }
        contextfree(context);
    }
    return (TRUE);
}
```

Called from `dofinddocscontaining` [`do1.c:15-23`] after `specset2ispanset` converts the search V-spec to I-addresses.

Three things to understand here:

1. **`docspace` restricts to `DOCISPAN` only** (line 168): the span covers exactly the document-content dimension of the spanfilade. Link endsets (`LINKFROMSPAN`, `LINKTOSPAN`, `LINKTHREESPAN`) are in different numeric slots and are excluded from this search.

2. **`retrieverestricted` is a 2D spanfilade lookup** [`retrie.c:56-85`]: it searches `spanf` where `ORGLRANGE` (the document dimension) falls within `docspace` AND `SPANRANGE` (the I-address dimension) overlaps `ispanset`. Both source and dest are in `docspace`; both hold the same I-span.

3. **`isinlinklist` at line 175 prevents duplicates**: if the same document ISA already appears in the result list (possible because the ispanset might contain multiple I-spans all belonging to the same document), it is skipped. This guarantees each document appears **exactly once** regardless of how many I-addresses matched.

---

### The Minimal Scenario

Insert one byte into source. VCopy that exact byte to dest. Call find_documents from source's perspective. The spanfilade contains exactly two `DOCISPAN` entries for that one I-address — one per document. `finddocscontainingsp` returns both, deduplicated.

```python
def scenario_transclusion_single_iaddress(session):
    """Two documents share one content I-address; find returns both exactly once.

    Trace:
      insert "X" → inserttextingranf allocates I₁ → docopy records (source, DOCISPAN, I₁)
      vcopy      → docopy records (dest, DOCISPAN, I₁) using the same I-address
      find       → finddocscontainingsp queries spanf restricted to DOCISPAN,
                   finds both entries, isinlinklist deduplicates → [source, dest]
    """
    # --- source document ---
    source = session.create_document()
    src_rw = session.open_document(source, READ_WRITE, CONFLICT_FAIL)
    session.insert(src_rw, Address(1, 1), ["X"])          # allocates I₁

    src_vs = session.retrieve_vspanset(src_rw)             # V-span [1.1, width=1]
    src_contents = session.retrieve_contents(
        SpecSet(VSpec(src_rw, list(src_vs.spans)))
    )
    session.close_document(src_rw)

    # --- dest document: transclude the single byte ---
    dest = session.create_document()
    dest_rw = session.open_document(dest, READ_WRITE, CONFLICT_FAIL)
    src_ro = session.open_document(source, READ_ONLY, CONFLICT_COPY)

    src_vs2 = session.retrieve_vspanset(src_ro)
    src_specs = SpecSet(VSpec(src_ro, list(src_vs2.spans)))
    session.vcopy(dest_rw, Address(1, 1), src_specs)       # reuses I₁

    dest_vs = session.retrieve_vspanset(dest_rw)
    dest_contents = session.retrieve_contents(
        SpecSet(VSpec(dest_rw, list(dest_vs.spans)))
    )
    session.close_document(dest_rw)

    # --- find: search from source's I-address ---
    search_spec = SpecSet(VSpec(src_ro, list(src_vs2.spans)))
    found = session.find_documents(search_spec)
    session.close_document(src_ro)

    return {
        "name": "transclusion_single_iaddress",
        "description": (
            "Two documents share one content I-address via vcopy; "
            "find_documents returns both exactly once"
        ),
        "operations": [
            {"op": "create_document", "role": "source", "result": str(source)},
            {"op": "insert",  "doc": "source", "text": "X",
             "note": "inserttextingranf allocates I₁; docopy records (source, DOCISPAN, I₁)"},
            {"op": "create_document", "role": "dest",   "result": str(dest)},
            {"op": "vcopy",   "from": "source", "to": "dest",
             "note": "docopy records (dest, DOCISPAN, I₁) — same I-address"},
            {"op": "contents", "doc": "source", "result": src_contents},
            {"op": "contents", "doc": "dest",   "result": dest_contents},
            {"op": "find_documents",
             "search": "source I-span covering 'X'",
             "result": [str(d) for d in found],
             "expected_count": 2,
             "comment": (
                 "finddocscontainingsp searches spanf restricted to DOCISPAN; "
                 "isinlinklist deduplicates; must return exactly [source, dest]"
             )},
        ]
    }
```

---

### Why "exactly once" is guaranteed

The deduplication lives at [`spanf1.c:175`]:
```c
if (isinlinklist(*headptr, &document.address))
    continue;
```

`isinlinklist` does a linear scan of the already-accumulated result list. If the same document ISA appears again (which can happen when the search `ispanset` contains multiple I-spans all belonging to the same document), it is skipped. Since our scenario uses exactly one I-address, there can be at most one match per document, so the deduplication is not exercised in this minimal case — but it would fire if we extended the search span. The scenario is therefore clean: 1 I-address → 2 spanfilade entries (one per document) → 2 results.

---

### What makes this truly minimal

| Property | Value | Reason |
|----------|-------|--------|
| Content inserted | 1 byte `"X"` | Smallest possible I-span |
| Documents | 2 (source, dest) | Minimum to demonstrate sharing |
| Transclusion scope | 100% of source content | No ambiguity about which I-address is shared |
| Operations | insert, vcopy, find | No links, no versions, no delete |
| Expected result | `[source, dest]`, `len == 2` | The deduplication invariant, directly verifiable |

The `scenario_find_documents_transcluded` already in `discovery.py` uses 14 characters and a non-trivial prefix in the dest; this scenario strips all of that away to isolate the single-I-address sharing property.
