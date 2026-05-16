## Question 7 [evidence]

> Does udanax-green's node-allocation pathway (granf2.c and surrounding code) ever root node addresses under any tumbler other than the single global granfilade?

## KB Synthesis

No. The allocation pathway in `granf2.c` operates exclusively on one global granfilade — there is no secondary or per-document granfilade.

The core evidence is in **[SS-ADDRESS-SPACE]** (Finding 0021): *"The entire granf (global address enfilade) is a single flat tree; the allocation algorithm enforces hierarchical structure by bounding searches to the parent's address range."* All address allocation — document orgls, link orgls, text atoms — goes through the same tree via `findisatoinsertgr`, which dispatches to either `findisatoinsertmolecule` (depth 3+, for content) or `findisatoinsertnonmolecule` (depth 1–2, for orgls/documents). Both functions search the same global granfilade.

**[SS-UNIFIED-STORAGE]** (Finding 0059) confirms this physically: all persistent state lives in a single file `enf.enf`, with the granfilade root pinned at `GRANFDISKLOCATION` and the spanfilade root at `SPANFDISKLOCATION`. There is one granfilade root.

**[SS-ADDRESS-SPACE]** (Finding 0077) refines this: document addresses and content I-addresses occupy *different tumbler ranges* within the single tree and are allocated by different code paths, but both query and mutate the same granfilade instance. The address: `next_doc_addr(granf, parent) = max_child(granf, parent) + 1` and `next_content_addr(granf, doc) = max_content(granf, doc) + 1` are both functions over the same `granf`.

The apparent hierarchy (account → document → version → atom) is enforced entirely by the bounding search: `findpreviousisagr` is called with an upper-bound tumbler derived from the parent address, constraining which existing entries are candidates for the increment. The structure is logical, not physical — no separate tree exists per account or per document.

POOM enfilades (one per document, storing V→I mappings) and the spanfilade (link index) are separate enfilades with different `denftype` tags, but they are not part of the address-allocation pathway in `granf2.c` at all. **[SS-GRANF-OPERATIONS]** and **[SS-SPANF-OPERATIONS]** (Finding 0012) describe these as distinct subsystems accessed through different global variables (`granf` vs `spanf`), with the granfilade being the sole locus of address allocation.

---

## Code Exploration

I now have a complete picture. Let me write the answer.

---

## Answer

**No. The node-allocation pathway never roots addresses under any granfilade other than the single global `granf`.**

---

### The Single Global Granfilade

`xanadu.h:13-14` declares the only granfilade that ever exists:

```c
#define typegranf INT *   /* temp -- INT for alignment */
extern typegranf granf;
```

This is initialized exactly once at startup, in `entexit.c:initmagicktricks()`:

```c
// entexit.c:41-46
if (initenffile()) {
    initkluge ((typecuc**)&granf, (typecuc**)&spanf);   // load from disk
} else {
    granf = (typegranf) createenf (GRAN);               // fresh start
    spanf = (typespanf) createenf (SPAN);
}
```

The `createenf(GRAN)` call (`enf.h:12`, `GRAN == 1`) occurs **once and only once** in the entire codebase. After initialization, no second GRAN-type enfilade is ever created.

---

### Every Allocation Pathway Passes the Same `granf`

All document creation, node creation, text insertion, and link creation in `do1.c` routes to either `createorglingranf` or `inserttextingranf`, and every call passes the same global `granf`:

| Call site | File:line | What it creates |
|---|---|---|
| `createorglingranf(taskptr, granf, ...)` | `do1.c:240` | new document |
| `createorglingranf(taskptr, granf, ...)` | `do1.c:252` | node/account |
| `createorglingranf(taskptr, granf, ...)` | `do1.c:277` | new version |
| `createorglingranf(taskptr, granf, ...)` | `do1.c:182, 209` | link |
| `inserttextingranf(taskptr, granf, ...)` | `do1.c:118` | text content |
| `findorgl(taskptr, granf, ...)` | `do1.c:40, 55, 75, 164, 186, 307, 318, 327` | look up existing |

`granf1.c:createorglingranf` simply delegates to `granf2.c:createorglgr`, which receives the same pointer:

```c
// granf1.c:50-55
bool createorglingranf(typetask *taskptr, typegranf granfptr, typehint *hintptr, typeisa *isaptr)
{
    return (createorglgr(taskptr, granfptr, hintptr, isaptr));
}
```

---

### The Allocation Logic Inside `granf2.c`

`createorglgr` [granf2.c:111-128] does two things:

1. Calls `findisatoinsertgr(fullcrumptr, hintptr, isaptr)` to locate the next available ISA address **within** `fullcrumptr` (which is always `granf`).
2. Calls `insertseq((typecuc*)fullcrumptr, isaptr, &locinfo)` to insert the new node **into** that same `fullcrumptr`.

`findisatoinsertgr` [granf2.c:130-156] dispatches to:
- `findisatoinsertmolecule` for ATOM subtypes (text, links) — searches `fullcrumptr` directly.
- `findisatoinsertnonmolecule` for non-ATOM subtypes (DOCUMENT, ACCOUNT, NODE) — also searches `fullcrumptr` directly via `findpreviousisagr`.

Both search and insert operations are always performed on the same `fullcrumptr` passed in — always `granf`.

---

### The `createenf(POOM)` Confusion — Not an Alternative Granfilade

Inside `createorglgr` [granf2.c:120]:

```c
locinfo.granstuff.orglstuff.orglptr = createenf (POOM);
```

This creates a new POOM-type enfilade (the document's *content* orgl — its virtual address space). But this POOM is **stored as the value** of a `GRANORGL`-type leaf node inside `granf`; it is not an alternative ISA address space. The POOM has no ISA tumbler of its own — it is accessed via the ISA address allocated in `granf`.

Three enfilade types exist (`enf.h:12-14`):
- `GRAN = 1` — the global ISA address tree (one instance: `granf`)
- `POOM = 2` — per-document content orgls (many, all stored as values inside `granf`)
- `SPAN = 3` — the global spanfilade (one instance: `spanf`)

---

### The `hintisa` Is Always an Address Within `granf`'s Namespace

The `makehint` calls in `do1.c` set `hintptr->hintisa` to an existing ISA address (the user's account, an existing document, a passed-in node tumbler). These are all coordinates inside the single `granf` ISA space. `findisatoinsertnonmolecule` [granf2.c:203-242] searches from that hint address to find the next free slot, but the slot is always created inside `granf`.

---

### Conclusion

The node-allocation pathway in `granf2.c` is closed under the single global `granf`. There is no code path that allocates ISA addresses into any other GRAN-type structure. The global `granf` is the unique, total ISA address registry for all accounts, nodes, documents, links, and text in the running system.
