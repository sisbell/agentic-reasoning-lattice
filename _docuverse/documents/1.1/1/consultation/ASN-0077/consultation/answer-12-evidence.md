## Question 12 [evidence]

> Given an I-address from a content span, how does the system determine which document originally allocated it — is it derivable from the tumbler hierarchy (e.g., parent prefix of the I-address) alone, or does it require a spanfilade lookup?

## KB Synthesis

## Derivation of Originating Document from a Content I-Address

Two mechanisms are available, and they answer slightly different questions.

---

### 1. Tumbler Hierarchy Alone — Sufficient for Allocation Origin

Content I-addresses are allocated within a **document-scoped tumbler subspace**. The allocation call `makehint(DOCUMENT, ATOM, TEXTATOM, docisaptr, &hint)` bounds the search to the document's address range, and `findisatoinsertmolecule` allocates by incrementing from the highest existing address within that bounded region [SS-ADDRESS-ALLOC, Finding 0065; SS-ADDRESS-SPACE, Finding 0077].

The resulting structure:

```
doc  = 1.1.0.1.0.1
text = 1.1.0.1.0.1.3.0.1.N   (element field 3 = text, element N)
link = 1.1.0.1.0.1.0.2.N     (element field 2 = link, element N)
```

[SS-ADDRESS-SPACE, Finding 0077] makes this explicit:

> `next_content_addr(granf, doc) = max_content(granf, doc) + 1` — allocation is partitioned per-document, not global.

**Therefore**: Given a content I-address, the originating document is recoverable by tumbler prefix matching — truncate the I-address to the document-address length and compare [SS-TUMBLER-CONTAINMENT]. This requires no spanfilade lookup; the hierarchy encodes it structurally.

---

### 2. What the System Actually Uses in Practice

The system does **not** perform prefix derivation for document lookup. Instead it maintains two indexes:

**DOCISPAN (spanfilade)** — used by `find_documents` / FINDDOCSCONTAINING. Created by `insertspanf(..., DOCISPAN)` at INSERT and COPY time [SS-DOCISPAN, Finding 0036]. This index maps I-address ranges → documents and is the runtime query mechanism.

**`homedoc` field in POOM crums** — used for crum coalescing (`isanextensionnd`). Records the I-address's origin document at the per-crum level [INV-IADDR-PROVENANCE, Finding 0046]:

> Each I-address has exactly one native document — the document where INSERT first allocated it. The `homedoc` field in each POOM crum records the I-address origin document.

---

### 3. Critical Distinction: Allocation Origin vs. Current Containment

The three mechanisms give different answers after `DELETE`:

| Mechanism | Answers | Survives DELETE? |
|-----------|---------|-----------------|
| Tumbler prefix match | Which doc *allocated* the I-address | Yes (structure is permanent) |
| DOCISPAN spanfilade | Which docs *have ever contained* the I-address | Yes (write-only index, stale entries persist) [INV-SPANF-WRITE-ONLY] |
| POOM crum `homedoc` | Which doc *currently maps* the I-address to a V-position | No (POOM entries removed by DELETE) |

After DELETE, the DOCISPAN still returns the document as a containing document, but attempting I→V resolution silently drops the I-address [INV-ITOV-FILTERING; EC-STALE-SPANF-REFERENCE]. This makes DOCISPAN a **superset** of current containment: `actual_docs(i) ⊆ find_documents(i)`.

---

### Conclusion

The originating document is **derivable from the tumbler hierarchy alone** via prefix matching — allocation is document-scoped by construction. However, the system **does not use this derivation at runtime**; instead it relies on the DOCISPAN spanfilade (historical, superset semantics) and POOM crum `homedoc` fields (current-state, lost on DELETE). Prefix derivation would require a granfilade tree traversal and is never implemented as a query path.

---

## Code Exploration

I now have all I need. Here is the complete answer, with every claim anchored to source.

---

## How udanax-green Determines Document Ownership of an I-Address

### 1. I-Address Allocation: Structural Prefix Relationship

Content atoms are allocated *inside* the document's I-address namespace. The key function is `findisatoinsertmolecule` [`granf2.c:158–181`]:

```c
tumblerincrement (&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound);  // granf2.c:162
clear (&lowerbound, sizeof(lowerbound));
findpreviousisagr ((typecorecrum*)fullcrumptr, &upperbound, &lowerbound);      // granf2.c:164
if (tumblerlength (&hintptr->hintisa) == tumblerlength (&lowerbound)) {
    tumblerincrement (&lowerbound, 2, hintptr->atomtype, isaptr);              // granf2.c:166
    tumblerincrement (isaptr, 1, 1, isaptr);
} ...
```

The upper bound is `docisa.0.(atomtype+1)`. All text atoms therefore live in the range `[docisa.0.TEXTATOM.1, docisa.0.(TEXTATOM+1))`. The document's I-address IS structurally a prefix of its content atoms.

The hint itself is set at the callsite [`do1.c:117`]:
```c
makehint(DOCUMENT, ATOM, TEXTATOM, docisaptr, &hint);
ret = (inserttextingranf(taskptr, granf, &hint, textset, &ispanset) ...
```

So allocation is always under the document's I-address. After the fact, `tumblerlength(&hintptr->hintisa)` [`granf2.c:165`] distinguishes whether a found I-address is still at the document level (same length) or already in atom territory (longer).

### 2. Why Tumbler Prefix Alone Is Insufficient

The structural prefix relationship does exist, but there is no way to recover the document boundary from a content I-address in isolation:

- The tumbler is purely positional — it carries no type tag or depth marker that signals "document ends here"
- The prefix depth varies by account/document hierarchy; the content tumbler encodes no length-of-owner field
- Most critically: **the same content I-span can be referenced by multiple documents**

That last point is the decisive one. `docopy` [`do1.c:45–65`] inserts the same content `ispanset` into a second document's POOM and spanfilade entry without moving or re-allocating the I-addresses:

```c
&& insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset)      // do1.c:60 — POOM of new doc
&&  insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN)  // do1.c:62 — spanfilade of new doc
```

After a copy, the content I-span has two owners. The original allocating document is findable by truncating the tumbler; the copy-owner is not. Pure prefix analysis recovers only one.

### 3. The Actual Mechanism: Spanfilade Lookup

The system always goes through the spanfilade. The entry point is `dofinddocscontaining` [`do1.c:15–23`]:

```c
bool dofinddocscontaining(typetask *taskptr, typespecset specset, typelinkset *addresssetptr)
{
    typeispanset ispanset;
    return (
       specset2ispanset (taskptr, specset, &ispanset, NOBERTREQUIRED)
    && finddocscontainingsp (taskptr, ispanset, addresssetptr));
}
```

`finddocscontainingsp` [`spanf1.c:151–188`] performs a 2D spanfilade query:

```c
tumblerincrement (&docspace.stream, 0, DOCISPAN, &docspace.stream);   // spanf1.c:168 — restrict ORGLRANGE to doc-type entries
tumblerincrement (&docspace.width, 0, 1, &docspace.width);
for (; ispanset; ispanset = ispanset->next) {
    context = retrieverestricted ((typecuc*)spanf,
        &docspace, ORGLRANGE,       // constraint axis 1: only DOCISPAN entries
        ispanset, SPANRANGE,        // constraint axis 2: content I-span being queried
        (typeisa*)NULL);            // spanf1.c:171
    for (c = context; c; c = c->nextcontext) {
        movetumbler (&c->totaloffset.dsas[ORGLRANGE], &docid);
        beheadtumbler (&docid, &document.address);   // spanf1.c:174 — strip DOCISPAN prefix
        ...
    }
}
```

`DOCISPAN = 4` [`xanadu.h:39`] is one of four span-type prefix values (LINKFROMSPAN=1, LINKTOSPAN=2, LINKTHREESPAN=3, DOCISPAN=4). `prefixtumbler` [`spanf1.c:22`] encodes the document I-address with this prefix into ORGLRANGE when inserting:

```c
prefixtumbler (isaptr, spantype, &crumorigin.dsas[ORGLRANGE]);   // spanf1.c:22
```

`beheadtumbler` [`tumble.c:673`] simply increments `exp` by one (shifts out the leading digit) to recover the raw document I-address from the prefixed ORGLRANGE key.

### 4. The `homedoc` Field: Redundant Consistency Check, Not a Lookup Path

When inserting into the spanfilade, the document I-address is also stored as `linfo.homedoc` [`spanf1.c:29`]:

```c
movetumbler (isaptr, &linfo.homedoc);
```

This is carried in `type2dbottomcruminfo`. It is used as a filter in `retrieverestricted` (when `docisaptr` is non-NULL) to restrict results to a specific document — it is a *guard*, not the primary lookup. In `finddocscontainingsp`, `retrieverestricted` is called with `(typeisa*)NULL` for the last argument [`spanf1.c:171`], so `homedoc` filtering is inactive during the document-discovery query. You cannot use `homedoc` without already having the spanfilade entries that contain it.

### 5. The Granfilade Is One-Dimensional — No Reverse Index

The granfilade is indexed by I-address only (one dimension, the WIDTH axis). `inserttextgr` [`granf2.c:83–109`] writes crums sequentially at the allocated I-address. There is no reverse mapping from "content I-address → allocating document" stored in the granfilade. The `hint` parameter carries the document context during allocation but disappears afterward.

### Summary

| Question | Answer |
|---|---|
| Are content I-addresses structurally inside the document's I-address namespace? | **Yes** — `findisatoinsertmolecule` allocates atoms at `docisa.0.atomtype.N` |
| Can the original allocating document be derived from the tumbler prefix alone? | **Theoretically yes**, but only if you know the document's tumbler depth, which is not encoded in the content I-address |
| Can ALL referencing documents (including copies) be found from the tumbler alone? | **No** — `docopy` creates new ownership without moving the I-address |
| What does the code actually use? | **Spanfilade 2D lookup**: `retrieverestricted(spanf, DOCISPAN-docspace, ORGLRANGE, ispan, SPANRANGE, NULL)` |
| Is there a direct granfilade reverse index by document? | **No** — the granfilade is 1D by I-address; no reverse mapping exists |

The spanfilade lookup is not merely the practical mechanism — it is the only mechanism that correctly handles copied content, where the same content I-span is referenced by multiple documents. Tumbler prefix analysis would find only the original allocator, missing all copy-owners.
