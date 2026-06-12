## Question 3 [evidence]

> In udanax-green's emit path, is document-residence validation performed before or after the idempotency/dedup check — specifically, does a dedup hit return the existing address without ever consulting the document store, and does the nullify path check document residence on every call?

## KB Synthesis

This question is not answerable from the KB.

The KB contains no entries describing an "emit path," an idempotency or dedup check, or a "nullify path" in udanax-green's operation. None of the documented operation sequences (INSERT, COPY, CREATELINK, VERSION, DELETE, REARRANGE) include a deduplication or idempotency gate in their call chains as documented.

The closest concepts in the KB are:

- **`isanextensionnd()`** [ST-INSERT, Finding 0062] — checks whether new content can be coalesced into an existing POOM crum by testing reach-equality and `homedoc` match. This is a structural optimization, not a dedup check, and it comes after the document-residence check.

- **The INSERT precondition chain** [PRE-INSERT, Finding 0036]: `findorgl(…, WRITEBERT)` → `acceptablevsa()` → `asserttreeisok()` — document-residence validation (`findorgl`) is the *first* gate before any structural operations proceed. There is no documented dedup check in this chain.

- **Address allocation** [SS-ADDRESS-ALLOC, Finding 0061] — is stateless query-and-increment with no duplicate detection; it always allocates fresh addresses beyond the current maximum.

If "emit path" refers to an operation or subsystem not captured in the KB's 78 findings, the implementation behavior there is simply not documented here. You would need to consult the source directly — likely in `do1.c`, `do2.c`, or the granfilade allocation path in `granf2.c`.

---

## Code Exploration

I have read all the relevant source files. Here is my complete answer.

---

## Answer: Emit Path Ordering in udanax-green

### The Emit Path

The "emit path" for new text content is:

```
fns.c:insert (line 84)
  → do1.c:doinsert (line 87)
    → granf1.c:inserttextingranf (line 44)
      → granf2.c:inserttextgr (line 83)
        → granf2.c:findisatoinsertgr (line 130)
          → granf2.c:isaexistsgr [DOCUMENT RESIDENCE CHECK]
          → granf2.c:findisatoinsertmolecule [ADDRESS CALCULATION]
        → insert.c:insertseq [ACTUAL INSERTION]
      → do1.c:docopy (line 119)
        → granf1.c:findorgl (line 17)
          → bert.c:checkforopen [BERT ACCESS CHECK]
        → orglinks.c:insertpm (line 75)
```

---

### 1. Document-Residence Validation Ordering

**Document-residence validation is the first gate, and there is no dedup/idempotency check anywhere in the path.**

In `findisatoinsertgr` [granf2.c:130–156], the ATOM-subtype branch reads:

```c
if (hintptr->subtype == ATOM) {
    if (!isaexistsgr (fullcrumptr, &hintptr->hintisa)) {   // ← line 136
        return (FALSE);
    }
    findisatoinsertmolecule (fullcrumptr, hintptr, isaptr);  // ← line 142
}
```

`isaexistsgr` [granf2.c:244–253] queries the granfilade enfilade directly:

```c
bool isaexistsgr(typecuc *crumptr, typeisa *isaptr)
{
    context = retrieve (crumptr, isaptr, WIDTH);        // walks enfilade
    ret = tumblereq ((tumbler*)&context->totaloffset, isaptr);  // does it exist?
    contextfree (context);
    return (ret);
}
```

This hits the content store on every call—there is no short-circuit, cache, or skip path. If the document ISA is absent from the granfilade, the function returns `FALSE` immediately and the insertion is aborted before any address is computed.

After this check, `findisatoinsertmolecule` [granf2.c:158–181] computes the next available insertion address by calling `findpreviousisagr` and incrementing. It does not compare content for equality; it merely finds a fresh slot.

---

### 2. There Is No Idempotency/Dedup Check

The premise of the question—that a dedup check exists—is not implemented in the code.

- `acceptablevsa` [do2.c:110–113] is a **stub** that unconditionally returns `TRUE`. It performs no comparison against previously inserted content.
- `findisatoinsertmolecule` [granf2.c:158] uses `findpreviousisagr` only to find the *next free slot*, not to match content.
- `isanextensionnd` [insertnd.c:301] and `fillupcbcseq` [insert.c:74] are **physical-adjacency optimizations** (coalescing adjacent crums for storage efficiency), not semantic dedup. They check address contiguity and homedoc identity, not content equality.
- There is no hash table, no content fingerprint, and no "return existing address" path anywhere in the insert flow.

**Consequence:** Every call to `inserttextingranf` allocates a fresh unique ISA in the granfilade, regardless of whether identical content was previously inserted. There are no "dedup hits."

---

### 3. The Nullify Path Does Not Check Document Residence

The nullify path is in `bert.c:removefromopen` [bert.c:154–193]:

```c
status = bert->created && !bert->modified;
if (status) {
    deleteversion(tp);           // ← line 175–176
}
```

This fires when a document that was *created* (`created=TRUE`) is closed without ever being written to (`modified=FALSE`). **It does not check document residence.** It operates entirely within the bert in-memory hash table, iterating by hash bucket and document id.

Furthermore, `deleteversion` [bert.c:348–353] is a **stub**:

```c
int deleteversion(tumbler *tp)
{
#ifndef DISTRIBUTION
fprintf(stderr,"deleteversion: tp = ");dumptumbler(tp);fprintf(stderr,"\n");
#endif
}
```

In DISTRIBUTION mode the body is empty; in debug mode it only prints to stderr. No granfilade lookup, no residence check, no actual deletion occurs.

---

### Summary

| Question | Answer | Citation |
|---|---|---|
| Is document-residence validation before or after the dedup check? | Residence check (`isaexistsgr`) is **first**; there is no dedup check | granf2.c:136 |
| Does a dedup hit return the existing address without consulting the document store? | This path **does not exist** — every insert allocates a fresh address | granf2.c:158–181, do2.c:110–113 |
| Does the nullify path check document residence on every call? | **No.** The nullify path (`removefromopen` → `deleteversion`) is a bert hash-table operation; `deleteversion` is a stub | bert.c:173, bert.c:348–353 |

The ordering question as posed has a false premise: there is no idempotency/dedup check in the emit path at any level. The only pre-insertion gate is the granfilade residence check (`isaexistsgr`), which queries the enfilade on every call without exception.
