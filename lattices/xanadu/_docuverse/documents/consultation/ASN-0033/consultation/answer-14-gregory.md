## Question 14 [gregory]

> Are the granfilade and spanfilade per-node structures (one pair per node) or single global structures that contain entries from all nodes, distinguished only by their tumbler prefixes?

## KB Synthesis

**Single global structures, distinguished by tumbler prefixes.**

There is exactly one `granf` and one `spanf` for the entire running system. [SS-DUAL-ENFILADE]

From initialization:

```c
granf = createenf(GRAN);   // one global content/structure enfilade
spanf = createenf(SPAN);   // one global link search index
```

`corediskout.c:21-22` declares these as global variables; `entexit.c:44-45` creates them once at startup. [SS-DUAL-ENFILADE, Finding 0012]

**What's in each:**

- **granf** — everything: the permascroll (text atoms at `2.x.x.x` I-addresses), all document orgls, all link orgls, and the V→I mappings for every document. All of it in one tree. [SS-GRANF-OPERATIONS]

- **spanf** — one global link search index: DOCISPAN entries (I-address → document) and link endset entries (I-address → link ISA) for the entire system. [SS-SPANF-OPERATIONS]

**Separation is by tumbler prefix, not by structure.** Document 1.1.0.1.0.1's content lives at I-addresses like `1.1.0.1.0.1.3.x.x`. Document 1.1.0.1.0.2's content lives at `1.1.0.1.0.2.3.x.x`. Allocation for a document is bounded by searching the global granfilade tree within that tumbler range via `findpreviousisagr` with an upper-bound constraint. [SS-ADDRESS-ALLOC, SS-ADDRESS-SPACE Finding 0077]

**POOMs are different.** Each document has its own per-document POOM enfilade tree (the V→I mapping structure). These are separate enfilade trees, typed `POOM` in their disk block headers, accessed via the document's orgl in the granfilade. They live in the same `enf.enf` disk file alongside GRAN and SPAN blocks, but each is a distinct tree rooted at its document's orgl. [SS-UNIFIED-STORAGE, SS-POOM-MUTABILITY]

So: granfilade = one global tree, spanfilade = one global tree, POOMs = one per document.

---

## Code Exploration

Now I have everything needed. Here is the full answer:

---

## Answer: Granfilade and Spanfilade Are Single Global Structures

Both `granf` and `spanf` are **single global structures** — there is exactly one of each for the entire system. They are not per-node or per-document structures. All content from all documents and all links live inside these two global trees, distinguished by their tumbler addresses.

---

### 1. There Are Exactly Two Globals

In `xanadu.h`:

```c
// xanadu.h:13-16
#define typegranf INT *   /* temp -- INT for alignment */
extern typegranf granf;       
#define typespanf INT *   /* temp -- INT for alignment */
extern typespanf spanf;
```

These are declared as global `extern` variables — one pointer per filade type. The actual definitions live in `corediskout.c`:

```c
// corediskout.c:21-22
typegranf granf;
typespanf spanf;
```

### 2. They Are Created Once at Startup

In `entexit.c:41-46`, during `initmagicktricks()`, the system either loads them from disk or creates them fresh:

```c
if (initenffile()) {
    initkluge ((typecuc**)&granf, (typecuc**)&spanf);
} else {
    granf = (typegranf) createenf (GRAN);
    spanf = (typespanf) createenf (SPAN);
}
```

`createenf(GRAN)` and `createenf(SPAN)` each create a single enfilade root node. The `cenftype` field in every crum's header (`enf.h:34`) is set to one of `GRAN=1`, `POOM=2`, or `SPAN=3` — so every node in the tree carries a type tag, but the tree itself is singular.

### 3. Every Operation Passes the Global Root

Throughout `do1.c`, every document operation passes the same global `granf` or `spanf` root:

- `do1.c:40` — `findorgl(taskptr, granf, docisaptr, &docorgl, WRITEBERT)`
- `do1.c:55` — `findorgl(taskptr, granf, docisaptr, &docorgl, WRITEBERT)`
- `do1.c:62` — `insertspanf(taskptr, spanf, docisaptr, ispanset, DOCISPAN)`
- `do1.c:118` — `inserttextingranf(taskptr, granf, &hint, textset, &ispanset)`
- `do1.c:182` — `createorglingranf(taskptr, granf, &hint, linkisaptr)`
- `do1.c:191` — `insertendsetsinspanf(taskptr, spanf, linkisaptr, ...)`
- `do1.c:240` — document creation: `createorglingranf(taskptr, granf, &hint, isaptr)`

There is no per-document or per-node `granf` / `spanf` pointer — it is always the one global.

### 4. Tumbler Prefixes Are How All Content Is Distinguished

Since the filade is a tumbler-keyed tree, **every entry in the granfilade is distinguished purely by its ISA (Internal Storage Address)**, which is a tumbler. The `typehint` structure passed to insert functions encodes the addressing hierarchy (ACCOUNT → DOCUMENT → ATOM) — but all these addresses live in the same tree.

For example, `insertspanf` in `spanf1.c:22` does:

```c
prefixtumbler(isaptr, spantype, &crumorigin.dsas[ORGLRANGE]);
```

This prefixes the link's ISA with the span type (`LINKFROMSPAN=1`, `LINKTOSPAN=2`, `LINKTHREESPAN=3`, `DOCISPAN=4`) to create the 2D key for the entry in the single global `spanf` tree. All links and documents coexist in `spanf`, separated only by their tumbler prefixes.

Similarly, `granf2.c:34` retrieves an orgl by calling `retrievecrums((typecuc*)fullcrumptr, address, WIDTH)` — where `fullcrumptr` is always the same global root, and `address` is a tumbler that uniquely identifies the entry within the tree.

### 5. Per-Document Version Trees (POOMs) Are Subtrees of `granf`

Each document or link does get its own POOM (the version tree, type `POOM`) — but this POOM is stored **as a leaf entry inside `granf`**, not as a separate parallel structure. In `granf2.c:120`:

```c
locinfo.granstuff.orglstuff.orglptr = createenf(POOM);
insertseq((typecuc*)fullcrumptr, isaptr, &locinfo);
```

The POOM is created and then inserted as a bottom crum's payload into `granf` at the document's ISA address. `fetchorglgr` in `granf2.c:34` retrieves it again by calling `retrievecrums` on the global `granf` root with the document's tumbler address.

---

### Summary

| Structure | Count | Distinguished by |
|-----------|-------|-----------------|
| `granf` (granfilade) | 1 global | Tumbler ISA address per document/link/text-atom |
| `spanf` (spanfilade) | 1 global | 2D (ORGLRANGE × SPANRANGE) tumbler key, ORGLRANGE prefix = span type (1–4) |
| POOM per document | Many, but embedded as payloads inside `granf` bottom crums | ISA address within `granf` |

There is one granfilade and one spanfilade for the entire server process. Content from all documents is interleaved within each, navigable only via tumbler arithmetic.
