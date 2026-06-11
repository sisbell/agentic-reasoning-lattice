## Question 1 [evidence]

> Does any read operation in udanax-green enumerate the set of stored documents (listing document keys from the granfilade or equivalent), or is the document store consulted on the read path only as an existence/membership check against a caller-supplied address?

## KB Synthesis

No read operation in udanax-green enumerates stored documents. Every granfilade read path is a lookup against a caller-supplied address; reverse document discovery runs through the spanfilade, not the granfilade document keys.

**Granfilade read path: existence and content lookup only**

The core granfilade operation `findorgl()` [SS-GRANF-OPERATIONS] takes a caller-supplied ISA and returns the corresponding orgl or FALSE if not found — pure membership check. This is the gatekeeper for `retrieve_contents`, `RETRIEVEDOCVSPAN`, `RETRIEVEDOCVSPANSET`, `follow_link`, and every other document-reading call [SS-DOCUMENT-LIFECYCLE, PRE-RETRIEVE-CONTENTS]. None of them iterate document keys; they all require the caller to supply the document address.

The allocation helper `findpreviousisagr` [SS-ADDRESS-ALLOC, SS-ADDRESS-SPACE] does traverse the granfilade tree to find the highest existing address below a bound, but it exists solely on the write path (address allocation for INSERT, VERSION, MAKELINK) and is not exposed as a query operation.

**Reverse document discovery: spanfilade DOCISPAN, not granfilade enumeration**

`FINDDOCSCONTAINING` / `find_documents` [SS-DOCISPAN] does return a set of document ISAs, but it is not an enumeration — it requires a specific I-address range as input and queries the spanfilade's DOCISPAN sub-index (type 4 spanfilade entries, created by `insertspanf(..., DOCISPAN)` during INSERT and COPY) [SS-DOCISPAN Finding 0036]. The granfilade document structure is not traversed; the spanfilade acts as the reverse index. Furthermore, this index is a superset index that retains stale entries after DELETE [INV-SPANF-WRITE-ONLY, EC-STALE-SPANF-REFERENCE] — it is append-only and not kept in sync with current POOM state.

**Summary**

The document store (granfilade) is consulted on the read path exclusively as an existence/membership check against a caller-supplied address. No operation traverses or enumerates document keys from the granfilade. The only mechanism for discovering documents from content is content-identity-based lookup through the spanfilade DOCISPAN index [SS-DUAL-ENFILADE, FC-CONTENT-SPANF-ISOLATION], and that operation requires a specific I-address query, not a scan of document-space.

---

## Code Exploration

I now have all the evidence needed. Let me compile the complete answer from the source traces.

---

## Answer: The Granfilade Is a Pure Point-Lookup Store — No Read Operation Enumerates Document Keys

No read operation in udanax-green produces a list of stored document addresses. Every read path requires the caller to supply a specific document address (a tumbler/ISA), and the granfilade either returns the orgl for that exact address or returns NULL. The document store is consulted only as an existence/membership check against a caller-supplied address.

---

### The Central Entry Point: `findorgl` (`granf1.c:17`)

Every substantive read operation eventually calls `findorgl`:

```c
bool findorgl(typetask *taskptr, typegranf granfptr, typeisa *isaptr, typeorgl *orglptr, int type)
```

The caller always supplies `isaptr` — a fully-formed tumbler address. `findorgl` does exactly two things:

1. **`checkforopen(isaptr, type, user)`** [`bert.c:52`] — an existence/permission check in the BERT hash table against that specific address.
2. **`fetchorglgr(taskptr, granfptr, isaptr)`** [`granf2.c:39`] — a point lookup in the granfilade for that exact address.

Neither step enumerates anything.

---

### The Read-Path Function Chain

Every exposed read operation terminates in `findorgl`:

| FEBE handler (`fns.c`) | do-layer (`do1.c` / `do2.c`) | granfilade call |
|---|---|---|
| `retrievedocvspan` [`fns.c:304`] | `doretrievedocvspan` [`do1.c:312`] | `findorgl(…, READBERT)` [`do1.c:318`] |
| `retrievedocvspanset` [`fns.c:129`] | `doretrievedocvspanset` [`do1.c:322`] | `findorgl(…, READBERT)` [`do1.c:327`] |
| `retrievev` [`fns.c:175`] | `doretrievev` → `specset2ispanset` [`do1.c:338`] | `findorgl` per vspec [`do2.c:35`] |
| `showrelationof2versions` [`fns.c:250`] | `doshowrelationof2versions` → `specset2ispanset` [`do1.c:444`] | `findorgl` per vspec [`do2.c:35`] |
| `followlink` [`fns.c:114`] | `dofollowlink` [`do1.c:223`] | no granfilade call (spanfilade only) |
| `findlinksfromtothree` [`fns.c:189`] | `dofindlinksfromtothree` [`do1.c:348`] | no granfilade call (spanfilade only) |

---

### `fetchorglgr` Is a Three-Step Point Lookup (`granf2.c:22`)

```c
typeorgl fetchorglgr(typetask *taskptr, typegranf fullcrumptr, typeisa *address)
{
    if (tumblercmp (&((typecuc*)fullcrumptr)->cwid.dsas[WIDTH], address) == LESS)
        return (NULL);                                    // granf2.c:31 — range guard

    if ((context = retrievecrums ((typecuc*)fullcrumptr, address, WIDTH)) == NULL)
        return NULL;                                      // granf2.c:34 — tree descent

    if (!tumblereq((tumbler*)&context->totaloffset, address)) {
        crumcontextfree(context);
        return (NULL);                                    // granf2.c:37 — exact-match check
    }
    …
}
```

Step 1 (`granf2.c:31`): rejects the address if it lies beyond the granfilade's total width — no scan.
Step 2 (`granf2.c:34`): calls `retrievecrums` → `findcbcseqcrum` [`retrie.c:167`], which descends the enfilade tree following sibling pointers and child links until it reaches a leaf at or near `address`. This is O(height) tree descent, not a full scan.
Step 3 (`granf2.c:37`): confirms the leaf's accumulated offset equals `address` exactly. If not, the address is not stored and NULL is returned.

No step produces or iterates a list of stored keys.

---

### `findcbcseqcrum` Is a Descending Tree Search, Not a Scan (`retrie.c:167`)

```c
typecrumcontext *findcbcseqcrum(typecorecrum *ptr, typedsp *offsetptr, tumbler *address)
{
    for (; getrightbro (ptr); ptr = ptr->rightbro) {
        if (whereoncrum (ptr, offsetptr, address, WIDTH) <= THRUME)
            break;
        dspadd (offsetptr, &ptr->cwid, offsetptr, (INT)ptr->cenftype);
    }
    if (ptr->height != 0) {
        ptr = findleftson ((typecuc*)ptr);
        return (findcbcseqcrum (ptr, offsetptr, address));
    } else {
        return (createcrumcontext (ptr, offsetptr));
    }
}
```

At each level it scans siblings only to find the child subtree that straddles `address`, then recurses into that child. Siblings past the match point are skipped. This is a directed descent to a single leaf, identical in structure to a B-tree search.

---

### `findpreviousisagr` — The Only Tree Scan, and It Is Insertion-Only (`granf2.c:255`)

```c
int findpreviousisagr(typecorecrum *crumptr, typeisa *upperbound, typeisa *offset)
{ RECURSIVE
    if (crumptr->height == 0) {
        findlastisaincbcgr ((typecbc*)crumptr, offset);
        return(0);
    }
    for (ptr = findleftson((typecuc*)crumptr); ptr; ptr = findrightbro(ptr)) {
        if (…whereoncrum… == THRUME || !ptr->rightbro) {
            findpreviousisagr (ptr, upperbound, offset);
            return(0);
        } else {
            tumbleradd(offset, &ptr->cwid.dsas[WIDTH], offset);
        }
    }
}
```

This does traverse the tree to find the largest stored address below an `upperbound`. However it is called exclusively from `findisatoinsertnonmolecule` [`granf2.c:217`] and `findisatoinsertmolecule` [`granf2.c:164`], both of which are reachable only from `findisatoinsertgr` [`granf2.c:130`], which is called only from `inserttextgr` [`granf2.c:83`] and `createorglgr` [`granf2.c:111`] — both write operations. No read path reaches `findpreviousisagr`. The result is used only to compute a new insertion address; it is never returned to the client.

---

### `finddocscontainingsp` — The Only "List" Read, and It Does Not Touch the Granfilade (`spanf1.c:151`)

```c
bool finddocscontainingsp(typetask *taskptr, typespanset ispanset, typelinkset *addresssetptr)
{
    for (; ispanset; ispanset = ispanset->next) {
        context = retrieverestricted ((typecuc*)spanf, &docspace, ORGLRANGE,
                                      ispanset, SPANRANGE, (typeisa*)NULL);
        for (c = context; c; c = c->nextcontext) {
            movetumbler (&c->totaloffset.dsas[ORGLRANGE], &docid);
            beheadtumbler (&docid, &document.address);
            …
        }
    }
}
```

This is called via `dofinddocscontaining` [`do1.c:15`] → `finddocscontaining` [`fns.c:20`]. It looks up document addresses in the **spanfilade** (`spanf`), not the granfilade (`granf`). The caller-supplied `ispanset` already contains permascroll addresses; the spanfilade cross-indexes those addresses to document ISAs. The granfilade is never queried. The function returns document ISAs that happen to contain the supplied content spans — this is a content-index lookup, not a document enumeration.

---

### The BERT Table Does Not Expose Enumeration (`bert.c`)

The BERT table `berttable[1327]` [`bert.c:29`] tracks open documents by connection. `exitbert` [`bert.c:195`] iterates over the full table to clean up on disconnect. But `exitbert` is called only from `dobertexit` [`bert.c:339`] → `quitxanadu` [`fns.c:431`] — a session teardown, not a read operation. No read handler touches `berttable` except through `checkforopen` [`bert.c:52`], which is a point lookup by hash of the caller-supplied tumbler.

---

### Conclusion

The granfilade in udanax-green functions as a pure point-lookup store on the read path. A caller must know the document address in advance; the system will confirm existence and return the orgl, or return NULL. There is no operation that lists, iterates, or enumerates stored document addresses from the granfilade. The only granfilade tree traversal beyond a directed descent (`findpreviousisagr`) is part of the insertion machinery and is not reachable from any read handler.
