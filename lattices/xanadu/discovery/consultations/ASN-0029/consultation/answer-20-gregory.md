## Question 20 [gregory]

> Is there any mechanism to enumerate all documents in the system — for example, can a session walk the granfilade's document-level address range to discover existing documents, or is document discovery limited to `FINDDOCSCONTAINING` via shared I-addresses?

## KB Synthesis

Based on the KB, the short answer is: **no general document enumeration mechanism is documented in the FEBE protocol**. Document discovery is limited to content-identity-based lookup.

## What the KB documents

**FINDDOCSCONTAINING** is the only reverse-lookup operation [SS-DOCISPAN]. It queries the DOCISPAN sub-index in the spanfilade — `Map<ISpan, Set<DocISA>>` — to find documents that contain specific I-address ranges. This requires knowing *what content* you're looking for, not "show me everything." [SS-SPANF-OPERATIONS] confirms the spanfilade supports only insertion and range-query; there's no "enumerate all" operation.

**Granfilade structure** does encode all document addresses in a hierarchical B-tree [SS-ADDRESS-ALLOC], [SS-ADDRESS-SPACE]. The internal allocation mechanism `findpreviousisagr` traverses this tree to find the highest existing address under a parent prefix — which is a bounded walk of a sub-tree. In principle this traversal could enumerate all documents under an account. But this is an **internal allocation primitive**, not a user-facing operation. The FEBE request dispatch table (`init.c:requestfns`) doesn't include any such enumeration opcode.

**Tumbler containment** [SS-TUMBLER-CONTAINMENT] provides the predicate `contains(prefix, addr)` via truncation-and-compare, which would be the building block for any address-space walk. But no FEBE operation exposes this as a query.

**Address monotonicity** [INV-MONOTONIC] means the granfilade address sequence is gapless and grows predictably — you could in principle probe `account.0.1`, `account.0.2`, etc. But the system provides no documented way to ask "what is the next valid document address after X?" at the FEBE level.

## What this implies for spec

Document discovery is entirely **content-identity-driven**:
- You find documents by content they've ever contained, via FINDDOCSCONTAINING [INV-IADDRESS-PERMANENT]
- The spanfilade is write-only and append-only [INV-SPANF-WRITE-ONLY], so it accumulates provenance but supports no iteration
- There is no document directory or catalog object

If you need to enumerate your own documents, the only viable path through the documented interface is knowing that your documents are allocated under your account address (e.g., `1.1.0.2.0.1`, `1.1.0.2.0.2`, ...) and probing sequentially — but the KB documents no FEBE opcode to support even that efficiently. The internal `findpreviousisagr` exists, but only as part of the allocation path [SS-ADDRESS-ALLOC].

This is a significant capability gap: the system can answer "which documents contain X?" but not "what documents exist?"

---

## Code Exploration

I now have everything needed. Here is the full answer.

---

## Document Enumeration in udanax-green

### Short answer

**No.** There is no mechanism for a session to enumerate all documents in the system. The granfilade exposes only point-lookup access; it has no range-walk interface through FEBE. Document discovery is entirely mediated by `FINDDOCSCONTAINING` — which itself requires that you already possess I-addresses.

---

### The complete FEBE operation table

From `init.c:43–75`, the full set of registered request handlers is:

```
COPY, INSERT, RETRIEVEDOCVSPANSET, REARRANGE, RETRIEVEV,
NAVIGATEONHT, SHOWRELATIONOF2VERSIONS, CREATENEWDOCUMENT,
DELETEVSPAN, CREATENEWVERSION, RETRIEVEDOCVSPAN, QUIT,
SOURCEUNIXCOMMAND, FOLLOWLINK, FINDDOCSCONTAINING, CREATELINK,
RETRIEVEENDSETS, FINDNUMOFLINKSFROMTOTHREE, FINDLINKSFROMTOTHREE,
FINDNEXTNLINKSFROMTOTHREE, CREATENODE_OR_ACCOUNT, OPEN, CLOSE,
XACCOUNT, DUMPSTATE
```

There is no `LISTDOCUMENTS`, `ENUMERATEDOCUMENTS`, `NEXTDOCUMENT`, or any range-scan operation.

---

### What `FINDDOCSCONTAINING` actually does

```
finddocscontaining [fns.c:20]
  → dofinddocscontaining [do1.c:15]
      → specset2ispanset [do2.c:14]       (convert V-specs to I-spans)
      → finddocscontainingsp [spanf1.c:151]
```

`finddocscontainingsp` [spanf1.c:151–188] works as follows:

1. Accepts an `ispanset` — a set of I-address ranges.
2. Sets `docspace` to the `DOCISPAN` slice of the ORGLRANGE dimension [spanf1.c:168–169]:
   ```c
   tumblerincrement (&docspace.stream, 0, DOCISPAN, &docspace.stream);
   tumblerincrement (&docspace.width, 0, 1, &docspace.width);
   ```
3. For each I-span, calls `retrieverestricted(spanf, &docspace, ORGLRANGE, ispanset, SPANRANGE, NULL)` [spanf1.c:171] — querying the 2D spanfilade for entries where the ORGLRANGE dimension falls in the document slice **and** the SPANRANGE dimension intersects the given I-span.
4. Extracts the document address from `c->totaloffset.dsas[ORGLRANGE]` [spanf1.c:173–174] and strips the DOCISPAN prefix with `beheadtumbler`.

The critical constraint: **this operation is entirely input-driven by I-addresses you already hold.** Without prior I-addresses, you cannot call it meaningfully. It answers "which documents contain this content?", not "what documents exist?"

---

### The granfilade is a point-lookup structure

The granfilade (`granf`, typed `typegranf = INT *` [xanadu.h:13]) is a sequential enfilade (GRAN type) indexed by document tumblers. Document addresses are allocated as sub-tumblers of an account:

- `docreatenewdocument` [do1.c:234–241] calls `makehint(ACCOUNT, DOCUMENT, ...)` with `taskptr->account` as the hint address.
- `findisatoinsertnonmolecule` [granf2.c:203–242] allocates the next free address by calling `findpreviousisagr` to find the highest existing address under the account, then incrementing. Documents under account `1.1` land at `1.1.0.1`, `1.1.0.2`, etc.

But `findpreviousisagr` [granf2.c:255–278] is an **internal allocation helper** — it is never exposed through FEBE. It is called only from `findisatoinsertnonmolecule` during document creation.

The only publicly accessible granfilade lookup is `fetchorglgr` [granf2.c:22–81], called from `findorgl` [granf1.c:17–41], called from every operation that needs to open a document's POOM. It performs an exact-match lookup:

```c
if (!tumblereq((tumbler*)&context->totaloffset, address)) {
    crumcontextfree(context);
    return (NULL);   /* [granf2.c:37–39] */
}
```

If the address does not exist in the granfilade, `fetchorglgr` returns NULL. There is no "next document" or "iterate" path.

---

### Can a session probe sequential addresses?

Theoretically, a session could guess addresses (`account.0.1`, `account.0.2`, …) and issue `RETRIEVEDOCVSPANSET` or `OPEN`. But:

- `OPEN` → `doopen` [bert.c:264] calls `checkforopen` [bert.c:52]. If the document is not open and is owned by you (`isthisusersdocument` [be.c:171–176] checks `tumbleraccounteq`), `checkforopen` returns 0 ("open required"), and `doopen` adds it to the bert table and **returns success** — even if the address does not correspond to any real document in the granfilade. The existence check only fires later, when `findorgl` is called.

- `RETRIEVEDOCVSPANSET` → `doretrievedocvspanset` → `findorgl` → `fetchorglgr`. If `fetchorglgr` returns NULL (no document at that address), the operation fails. But the failure is indistinguishable from a permissions failure; there is no "does not exist vs. not accessible" distinction exposed to the client.

More fundamentally: probing sequential addresses would require knowing the account prefix, knowing the per-account document numbering increment, and the numbers are contiguous only within a single account's creation sequence. Across accounts, addresses are disjoint by the tumbler hierarchy.

---

### `findpreviousisagr` — the closest thing to a range scan

`findpreviousisagr` [granf2.c:255–278] does walk the granfilade tree to find the highest address below a given upper bound:

```c
for (ptr = findleftson((typecuc*)crumptr); ptr; ptr = findrightbro(ptr)) {
    if (
     (tmp= whereoncrum (ptr, (typewid*)offset, upperbound, WIDTH)) == THRUME
    || tmp == ONMYRIGHTBORDER
    || !ptr->rightbro) {
        findpreviousisagr (ptr, upperbound, offset);   /* [granf2.c:272] */
        return(0);
    } else {
        tumbleradd(offset, &ptr->cwid.dsas[WIDTH], offset);  /* [granf2.c:275] */
    }
}
```

This is a recursive descent that could, in principle, be iterated to enumerate all existing document addresses. But it is **not exposed through any FEBE request**. It is used solely in `findisatoinsertnonmolecule` [granf2.c:217] to allocate the next document address. A client session has no way to invoke it.

---

### The architectural conclusion

The design is intentional. Udanax-green's document model assumes the transclusion graph as the navigation primitive:

1. You know a document address (you created it, or were told it).
2. You retrieve content → get I-addresses.
3. You use `FINDDOCSCONTAINING` with those I-addresses to find all documents that include the same content.
4. You follow links with `FOLLOWLINK` / `FINDLINKSFROMTOTHREE` to discover related documents.

The system has no concept of a "document directory" or "document namespace" that can be walked. The granfilade is a sparse address space, not a list. Document discovery is exclusively I-address–mediated: you can only find documents you are already connected to through the content graph.

The `FINDDOCSCONTAINING` operation is the **ceiling** of what the system offers for discovery — and it requires possession of I-addresses as a prerequisite, not an output.
