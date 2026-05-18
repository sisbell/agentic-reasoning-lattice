## Question 8 [evidence]

> In udanax-green, does the allocator structure embed content and link sub-allocators under each document into the global allocator hierarchy with parent pointers, or are they tracked as independent free-floating chains?

## KB Synthesis

The allocator is a **single global granfilade tree** — one flat B-tree for everything. There are no separate per-document sub-allocators, no parent pointers between allocator nodes, and no free-floating chains.

The hierarchy is implicit in the tumbler address space, not in the allocator structure. Every allocation — text content, link orgls, document addresses — goes through the same stateless query-and-increment algorithm on the same tree: call `findpreviousisagr` to find the highest existing address below a computed upper bound, then increment by 1 [SS-ADDRESS-SPACE Finding 0077, SS-ADDRESS-ALLOC Finding 0021].

What differs between allocation types is only the **upper bound** passed to `findpreviousisagr`:

- **Text content** in document D: upper bound is `D.isa` at depth 3+ (the document's content subspace) [SS-ADDRESS-ALLOC Finding 0065]
- **Link orgls** in document D: upper bound is `docISA.2.3` (the document's link element subspace) [SS-ADDRESS-ALLOC Finding 0065]
- **Document addresses** under account A: upper bound is the next sibling of A, `tumblerincrement(A, depth-1, 1)` [SS-ADDRESS-ALLOC Finding 0021]

This means document D's content allocation range and link allocation range are separate tumbler prefixes within the same tree, distinguished purely by address structure — not by any allocator object or chain. Finding 0077 confirms explicitly: "There is no single global Σ.next counter. Allocation is stateless query-and-increment on different tumbler ranges via `findpreviousisagr`."

The containment check (prefix-match via `tumblertruncate` + `tumblereq`) enforces that allocations land under the correct parent — this was a bug fix (Bug 0013) that added this guard after the flat tree was found to cross account boundaries without it [SS-TUMBLER-CONTAINMENT, PRE-ADDRESS-ALLOC].

---

## Code Exploration

I have all the evidence I need. Here is the full answer.

---

## Allocator Structure in Udanax-Green: Embedded with Back-Pointers

**The sub-allocators are not free-floating chains. They are embedded as addressable nodes inside the global granfilade, and each sub-allocator root carries a `leftbroorfather` pointer back to its containing granfilade node.**

---

### 1. The Two Global Roots

`backend/corediskout.c:21-22`:
```c
typegranf granf;    /* global content allocator (granfilade) */
typespanf spanf;    /* global link allocator (spanfilade) */
```

`granf` is the system-wide granfilade. Every document's content address space is an **orgl** (organized granfilade) — a POOM-type enfilade — stored as a leaf record inside `granf`. `spanf` is the parallel structure for links.

---

### 2. The Parent-Pointer Field

Every crum node at every level carries `leftbroorfather` — `backend/enf.h:42-44` (in `structcorecrumhedr`, repeated identically in `typecuc:66` and `typecbc:97`):

```c
struct structcorecrumhedr *leftbroorfather;
        /* if it is NULL then this is fullcrum */
        /* father if leftmost, else leftbro */
```

This is the normal tree-navigation pointer used throughout the enfilade. The orgl roots use it unconventionally — not to point at their parent within their own tree, but to point at the `typecbc` node in the **parent granfilade** that owns them.

---

### 3. Per-Document Sub-Allocator: Structure

`backend/wisp.h:87-92`:
```c
typedef struct structgranorgl {
        struct structcuc *orglptr;      /* pointer to the POOM enfilade root */
        typediskloafptr diskorglptr;    /* disk address */
        bool orglincore;                /* whether orglptr is valid in-core */
} typegranorgl;
```

This struct is held inside a `typegranbottomcruminfo` (`wisp.h:100-104`) with `infotype == GRANORGL` (`wisp.h:70`). One such bottom crum per document lives inside the global `granf` tree.

---

### 4. Sub-Allocator Creation and the Parent Link

`createorglgr` (`backend/granf2.c:111-128`) creates a new POOM enfilade and inserts its info record into `granf`:

```c
locinfo.infotype = GRANORGL;
locinfo.granstuff.orglstuff.orglptr = createenf (POOM);  /* new POOM enfilade */
...
insertseq ((typecuc*)fullcrumptr, isaptr, &locinfo);      /* insert into granf */
```

Inside `insertseq` (`backend/insert.c:49-51`), immediately after the new bottom crum is placed into the granfilade tree:

```c
if (info->infotype == GRANORGL){
    info->granstuff.orglstuff.orglptr->leftbroorfather = new;
}
```

`new` here is the freshly-created `typecbc` node now sitting in `granf`. The orgl root's `leftbroorfather` is set to point directly at it. The link goes both ways: `new->cinfo.granstuff.orglstuff.orglptr` points down to the orgl; `orgl->leftbroorfather` points back up to `new`.

---

### 5. The Back-Pointer Is Operationally Load-Bearing

The `leftbroorfather` on an orgl root is not decorative — it is required for cache eviction. `orglfree` (`backend/credel.c:481-488`) walks it to update the parent's in-core flags without searching:

```c
if (((typecbc *)ptr->leftbroorfather)->cinfo.granstuff.orglstuff.diskorglptr.diskblocknumber == DISKPTRNULL)
    qerror ("orglfree called with unwritten-out orgl.\n");
((typecbc *)ptr->leftbroorfather)->cinfo.granstuff.orglstuff.orglincore = FALSE;
((typecbc *)ptr->leftbroorfather)->cinfo.granstuff.orglstuff.orglptr = NULL;
subtreefree ((typecorecrum*)ptr);
```

When an orgl is evicted from memory, the system navigates straight up to its owning `typecbc` in `granf` and clears `orglincore` and `orglptr` — so subsequent `fetchorglgr` calls will know to re-load from disk.

The same back-pointer is re-established on disk load: `backend/corediskin.c:224`:
```c
ptr->leftbroorfather = (typecorecrum *) granorglptr;
```

---

### 6. The Global Roots Are a Special Case

During disk flush (`writeenfilades`, `backend/corediskout.c:68-87`), the two global roots are themselves given synthetic parents — a stack-allocated `typecbc temporgl` — so that `orglwrite` can recurse uniformly:

```c
temporgl.leftbroorfather = NULL;          /* root of the whole thing */
...
temporgl.cinfo.granstuff.orglstuff.orglptr = (typecuc *)granf;
((typecuc *)granf)->leftbroorfather = (typecorecrum *)&temporgl;
orglwrite (&temporgl);
```

After loading from disk, these synthetic parents are immediately cleared: `backend/corediskin.c:28,36`:
```c
tempcbc->cinfo.granstuff.orglstuff.orglptr->leftbroorfather = NULL;
```

So at runtime, `granf` and `spanf` are the apex nodes with `leftbroorfather == NULL`; all orgl roots point back into `granf`.

---

### Summary

The allocator hierarchy is:

```
granf  (global, leftbroorfather=NULL)
  ├── typecbc [GRANORGL, doc A's ISA]  ←── orglA->leftbroorfather
  │       orglptr → orglA (POOM enfilade, doc A's content address space)
  ├── typecbc [GRANORGL, doc B's ISA]  ←── orglB->leftbroorfather
  │       orglptr → orglB
  └── typecbc [GRANTEXT, ...]          (raw text stored directly in granf)

spanf (global, leftbroorfather=NULL)
  └── ... (link spans, same pattern)
```

Document sub-allocators are fully embedded in the global hierarchy:

| Mechanism | File:Line |
|-----------|-----------|
| `leftbroorfather` field on every crum | `enf.h:42` |
| Parent link set at insertion time | `insert.c:50` |
| Parent link used for cache eviction | `credel.c:481-488` |
| Parent link re-established on disk load | `corediskin.c:224` |
| Global roots given synthetic parents for flush | `corediskout.c:72-78` |
| Global roots cleared to NULL after load | `corediskin.c:28,36` |

The sub-allocators are not free-floating. They are addressable by document ISA through the granfilade tree, and their roots carry `leftbroorfather` back-pointers into that tree — a two-way embedding that the cache eviction code depends on.
