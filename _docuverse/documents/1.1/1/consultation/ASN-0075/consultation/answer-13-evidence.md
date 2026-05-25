## Question 13 [evidence]

> When DELETE removes a V→I mapping from a POOM, can the deleted I-address range still be recovered by querying the granfilade or spanfilade for I-addresses originally allocated under that document?

## KB Synthesis

Yes — the deleted I-address range survives in two independent structures and can be recovered.

## What DELETE Actually Touches

DELETE operates exclusively on the POOM enfilade. `dodeletevspan` → `deletevspanpm` → `deletend` removes bottom crums from the document's POOM tree via `disown` + `subtreefree`. There is no call to any granfilade or spanfilade removal function. [ST-DELETE Finding 0057, 0064]

## Granfilade Persistence

The granfilade is append-only. I-addresses allocated for content persist at their positions permanently — there is no free-list, no gap-tracking, and no garbage collection. `findpreviousisagr` will still find those I-addresses as the highest existing addresses when computing the next allocation, which is why they influence future allocation order but are never reused. [INV-IADDR-IMMUTABILITY, INV-NO-IADDR-REUSE, FC-GRANF-ON-DELETE]

The content bytes at those I-addresses are retrievable by anyone who knows the I-address range.

## Spanfilade Persistence

The spanfilade has no delete operation at all — `spanf1.c` and `spanf2.c` contain only insertion and query functions. DOCISPAN entries created by the original INSERT or COPY survive DELETE intact. This means `FINDDOCSCONTAINING` continues to report the document as containing those I-addresses even after they are gone from the V-stream. [INV-SPANF-WRITE-ONLY, INV-IADDRESS-PERMANENT, INT-DELETE-SPANF-DIVERGENCE]

This creates the "stale spanfilade reference" divergence: `actual_docs(i) ⊆ find_documents(i)` — the spanfilade is a superset of current POOM associations. [EC-STALE-SPANF-REFERENCE]

## Practical Recovery

The only identity-preserving restoration mechanism is VCOPY — copying from a document (typically a version created before deletion) that still holds V→I mappings to those I-addresses. VCOPY shares existing I-addresses rather than allocating fresh ones, so the restored content retains the original identity chain. DELETE + INSERT of identical text does NOT restore identity; it allocates new I-addresses, severing all transclusion, link, and version-comparison relationships. [ST-COPY Finding 0064, INV-DELETE-NOT-INVERSE]

**Summary:** The deleted I-address range remains permanently in the granfilade (content bytes accessible) and the spanfilade (DOCISPAN entries intact), making identity-preserving recovery possible via VCOPY from any surviving document that still references those I-addresses.

---

## Code Exploration

All key claims are confirmed. Here is my complete answer.

---

## Can Deleted V→I Mappings Be Recovered via Granfilade or Spanfilade?

**Short answer: Yes.** When `DELETE` removes a V→I mapping from a POOM, the underlying I-address allocations in the granfilade and spanfilade are **not touched**. They remain permanently accessible by I-address.

---

### The DELETE Call Chain

**`fns.c:333`** — FEBE handler `deletevspan()`:
```c
(void) getdeletevspan (taskptr, &docisa, &vspan);
putdeletevspan (taskptr);
if (!dodeletevspan (taskptr, &docisa, &vspan))
```

**`do1.c:158`** — `dodeletevspan()`:
```c
return (
   findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
&& deletevspanpm (taskptr, docisaptr, docorgl, vspanptr)
```

Note the commented-out `/* ht stuff */` at `do1.c:166` — this is a stub placeholder for hypertext operations that was never implemented. The `findorgl` call locates the document's POOM via the **granfilade** (read-only lookup), but does not modify it.

**`orglinks.c:145`** — `deletevspanpm()`:
```c
deletend((typecuc*)docorgl, &vspanptr->stream, &vspanptr->width, V);
logbertmodified(docisaptr, user);
```

The only structural mutation is `deletend()` called with `index = V`. It operates exclusively on the POOM's V-dimension.

---

### What `deletend` Actually Destroys

**`edit.c:31`** — `deletend()`:
```c
knives.dimension = index;   /* index == V */
makecutsnd (fullcrumptr, &knives);
...
switch (deletecutsectionnd ((typecorecrum*)ptr, &fgrasp, &knives)) {
  case 1:
    disown ((typecorecrum*)ptr);
    subtreefree ((typecorecrum*)ptr);     /* edit.c:59-60 */
    break;
  case 2:
    tumblersub (&ptr->cdsp.dsas[index], width, &ptr->cdsp.dsas[index]);  /* edit.c:63 */
    break;
}
```

- **Case 1** (crum entirely within deleted V-range): the POOM crum struct is unlinked and freed
- **Case 2** (crum partially overlapping): the V-dimension offset is adjusted, but the crum — and thus the I-addresses it encodes — survives with modified V-coordinates

Critically: `index = V` means cuts and offsets are computed solely in the **V dimension**. The crum's I-dimension data (`cdsp.dsas[I]`) is never written.

---

### Granfilade: Untouched

A search across all `backend/*.c` for any deletion function targeting the granfilade — `deletegr`, `removeisagr`, `freegr` — returns **no matches**. There is no granfilade deletion function at all.

**`granf2.c:83`** — `inserttextgr()` allocates I-addresses by scanning `findpreviousisagr()` to find the high-water mark, then inserting content at the next available I-address. Once inserted, those entries are permanent. The granfilade is append-only in practice.

**`granf2.c:255`** — `findpreviousisagr()` scans granfilade crums to find the previous I-address boundary. It does not distinguish between content whose POOM mapping was deleted and content still mapped — the granfilade has no concept of "deleted."

---

### Spanfilade: Also Untouched

Similarly, no `deletespanf` or equivalent exists. **`spanf1.c:51`** — `insertspanf()` inserts entries into the spanfilade keyed by I-addresses:
```c
insertnd(taskptr,(typecuc*)spanfptr,&crumorigin,&crumwidth,&linfo,SPANRANGE);
```

These entries are indexed by I-address ranges that were allocated at insert time. The DELETE operation never calls any spanfilade modification function.

---

### The Consequence

The architecture separates three concerns:

| Structure | Stores | After DELETE |
|-----------|--------|--------------|
| Granfilade | I-address → text content | **Unchanged** |
| Spanfilade | I-address → document membership | **Unchanged** |
| POOM | V-address → I-address mapping | **Modified** — crums freed or offset-adjusted |

DELETE severs the **V→I link** in the POOM. It does not revoke the I-address allocation. The granfilade retains the content bytes; the spanfilade retains the I-address-to-document mapping. Both are reachable by anyone who holds — or can reconstruct — the original I-address span.

This means deleted content is **not destroyed**, only **unmapped from virtual address space**. A query that bypasses the POOM and addresses the granfilade directly by I-span (`doretrieve` with an I-span, or a direct `retrievecrums` call through the granfilade) will return the original content. The I-addresses survive indefinitely — there is no garbage collection or I-address reclamation in this codebase.
