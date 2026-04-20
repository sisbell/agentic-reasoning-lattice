## Question 16 [gregory]

> When content becomes unreachable from all V-space mappings, it persists in I-space indefinitely — is there any mechanism or query to enumerate these orphaned I-address ranges, or are they invisible unless you already know their addresses?

## KB Synthesis

No. Orphaned I-address ranges — content in the granfilade with no current POOM mapping — are invisible through any available query mechanism unless you already know their addresses.

## What persists and why

[INV-IADDRESS-PERMANENT] and [INV-NO-IADDR-REUSE] establish the situation: every I-address ever allocated lives forever in the granfilade, and DELETE never removes them — it only removes the POOM (V→I) mappings [FC-GRANF-ON-DELETE]. The I-space grows monotonically and unconditionally.

## The only reverse-lookup mechanism: FINDDOCSCONTAINING

[INV-IADDRESS-PERMANENT] documents that `FINDDOCSCONTAINING(i)` continues to report documents even after deletion removes the V-space mapping. But [EC-STALE-SPANF-REFERENCE] makes this problematic: the spanfilade is append-only ([INV-SPANF-WRITE-ONLY]) and is never cleaned up after DELETE ([INT-DELETE-SPANF-DIVERGENCE]). The formal relationship is:

```
actual_docs(i) ⊆ find_documents(i)
```

The reverse does not hold. FINDDOCSCONTAINING returns a **superset** — stale references to documents whose POOM no longer maps those I-addresses. To distinguish live from orphaned, you'd need to perform I-to-V conversion in every returned document: [INV-ITOV-FILTERING] specifies that the conversion layer silently drops any I-address with no current POOM mapping, returning empty results for orphaned addresses. But this requires you to already have the I-addresses to query.

## No scan or enumeration exists

The granfilade is a B-tree keyed by I-address, but no FEBE operation exposes "walk all allocated I-addresses" or "find I-addresses with no V-space mapping." [SS-UNIFIED-STORAGE] confirms all state is in a single tree structure, but tree traversal is not an exposed operation. The FEBE protocol offers:

- Content retrieval (requires knowing V-positions)
- FINDDOCSCONTAINING (requires knowing I-addresses, returns stale superset)
- I-to-V conversion (silently filters misses per [INV-ITOV-FILTERING], requires knowing I-addresses)

None of these let you enumerate the set of orphaned addresses from scratch.

## Compound workaround (partial)

If you know a specific I-address is suspect, the closest approximation is:
1. Call FINDDOCSCONTAINING to get candidate documents
2. For each candidate, attempt I-to-V conversion
3. Empty results → orphaned in that document; empty across all candidates → globally orphaned

But there is no way to discover the orphaned I-addresses themselves without prior knowledge of their values. [EC-GHOST-LINK] notes this in the link context: permanent I-space existence doesn't imply reachability, and reconstitution is possible if you know the address — but discovery from scratch is not supported.

---

## Code Exploration

## Orphaned I-Address Ranges in Udanax-Green: No Enumeration Mechanism Exists

The short answer: **orphaned I-address ranges are invisible to the system.** There is no mechanism to discover them, and the architecture makes no provision for it.

---

### How I-Space Is Structured

I-space content lives in the **granfilade** — a tree of enfilades stored on disk. Addresses are allocated during insertions (`findisatoinsertmolecule` in `backend/granf2.c`) and persist permanently. There is no free-list, no reference count per I-address, and no allocation bitmap for I-space.

The only traversal primitive that walks the granfilade is `findpreviousisagr()` [`backend/granf2.c:255-278`], which searches *downward* to find an address below an upper bound — used purely as an allocation hint, not enumeration.

---

### The V↔I Asymmetry

The bridge functions in `backend/orglinks.c` all operate *one direction only when you already know something*:

- `vspanset2ispanset()` [`:397`] — converts V-spans → I-spans (you must supply the V-spans)
- `ispan2vspanset()` [`:389`] — converts I-spans → V-spans (you must supply the I-spans)
- `permute()` [`:404-422`] — iterates over a *provided* restriction spanset; it cannot discover spans that have no V-space existence

There is no "what I-spans exist?" query. All I-space access flows through V-space references.

---

### What the Find/Query Functions Cover

Every query in `backend/do2.c` and `backend/fns.c` requires V-space input:

- `dofind` / `finddocscontaining` [`backend/do1.c:15-23`, `backend/fns.c:20-32`] — finds documents containing *specified* content, not unspecified orphans
- `findnextlinkvsa()` [`backend/do2.c:151`] — scans for links within a *specified* document's V-space
- `doretrieve()` — retrieves at a *known* I-address

None of these can discover content for which there is no surviving V-space reference.

---

### Memory Management Is Not Content Tracking

`grimlyreap()` [`backend/credel.c:106-162`] and `isreapable()` [`:164-289`] manage the **in-memory crum cache** — they free RAM, not disk content. The doubly-linked `nextcrum`/`prevcrum` ring in `backend/enf.h:37-38,61-62` connects in-memory crums for reaping purposes only; it is not a traversal of all I-space addresses.

`diskalloc()` [`backend/diskalloc.c:27-54`] tracks **disk loaf block allocation** via bitmap, not I-address usage. Reclaiming a disk block does not reclaim an I-address range.

---

### Conclusion

When a V-span is deleted, its corresponding I-spans become permanently orphaned:

1. The granfilade retains the content nodes on disk
2. No reference counter decrements
3. No free-list records the now-unreachable range
4. No scan can discover the gap without already knowing the I-addresses

**To enumerate orphans would require:** a forward I-space iterator (no `getNextIAddress()` exists), an allocation registry for I-space (only disk blocks are tracked), and a cross-reference sweep comparing all allocated I-ranges against all V-space mappings. The architecture provides none of these. The content is not invisible *because* it is orphaned — it was always invisible; V-space was the only way to point at it, and once that pointer is gone, the data is unreachable but not freed.
