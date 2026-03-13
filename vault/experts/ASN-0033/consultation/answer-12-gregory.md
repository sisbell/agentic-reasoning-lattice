## Question 12 [gregory]

> Is there a node-level data structure (analogous to a document's POOM) that indexes accounts under a node, or is the node→account relationship implicit in the tumbler prefix convention with no dedicated orgl?

## KB Synthesis

The KB does not document any dedicated node-level orgl or POOM structure for indexing accounts. Based on the available evidence, the node→account relationship is **implicit in the tumbler prefix convention**, enforced through address arithmetic on the single global granfilade.

## What the KB says

**Single flat tree.** [SS-ADDRESS-ALLOC] Finding 0021 is explicit: "The entire granf (global address enfilade) is a single flat tree; the allocation algorithm enforces hierarchical structure by bounding searches to the parent's address range." There is no per-node secondary index — containment is computed on demand via `findpreviousisagr` bounded searches.

**Containment is arithmetic.** [SS-TUMBLER-CONTAINMENT] Finding 0021 documents the containment predicate: truncate address A to the length of B and compare. This is pure tumbler arithmetic — `tumblertruncate` + `tumblereq` — with no orgl lookup involved.

**The `makehint` table is incomplete for node→account.** [SS-ADDRESS-SPACE] Finding 0021 lists allocation hints:

| supertype | subtype | depth |
|-----------|---------|-------|
| NODE | NODE | 1 |
| ACCOUNT | DOCUMENT | 2 |
| DOCUMENT | DOCUMENT | 1 |
| DOCUMENT | ATOM | — |

There is no NODE→ACCOUNT row. Accounts (`1.1.0.x`) sit two `.0.`-boundaries below a node (`1.1`), but the KB records no dedicated mechanism for traversing or indexing that relationship — only the prefix convention.

**Orgls exist for documents and links, not nodes.** [SS-GRANF-OPERATIONS] documents the granfilade operations: `findorgl()`, `createorglingranf()`, `inserttextingranf()`, `ispanset2vstuffset()`. These are invoked for documents and link orgls. The KB contains no finding describing a node orgl being created or opened.

## Answer

There is no node-level POOM or dedicated index. The node→account→document hierarchy exists entirely in the tumbler digit sequence. Navigation or enumeration of accounts under a node would require walking the global granfilade tree bounded by the node's address prefix — the same `findpreviousisagr` / `tumblertruncate` machinery used for all address-range queries. This is convention over structure: the hierarchy is reconstructible from address arithmetic, not stored as a separate data structure.

This is consistent with the broader design pattern the KB describes — the implementation uses a single flat B-tree and trusts callers to impose hierarchical semantics through address construction. Just as the subspace convention (1.x for text, 2.x for links) is unenforced at the storage layer [SS-SUBSPACE-CONVENTION], the node→account containment relationship is unenforced by any dedicated node-level structure.

---

## Code Exploration

Now I have everything needed. Here is the complete answer.

---

## Is there a node-level data structure indexing accounts under a node?

**Short answer: No.** There is no dedicated node-level orgl that inventories its child accounts. The node→account relationship is entirely implicit in the tumbler address prefix convention. Every node gets a POOM orgl (via the same `createorglgr` pathway as documents), but that POOM stores no children list — it is empty by design. The single global `granf` is the only index, and it is organized by address space: finding children means range-scanning granf for addresses prefixed by the parent.

---

### 1. The Global Index: `granf`

`xanadu.h:13-14`:
```c
#define typegranf INT *   /* temp -- INT for alignment */
extern typegranf granf;
```

There is exactly one granfilade in the system. All nodes, accounts, documents, and atoms are stored as leaf entries in this single tree, keyed by their tumbler address. There is no per-node sub-granf.

---

### 2. What Creating a Node Actually Does

`do1.c:243-258`:
```c
bool docreatenode_or_account(typetask *taskptr, typeisa *isaptr)
{
    typeisa isa;
    typehint hint;
    bool createorglingranf();
    bool result;

    tumblercopy(isaptr, &isa);
    makehint (NODE, NODE, 0, &isa, &hint);
    result = createorglingranf (taskptr, granf, &hint, &isa);
    if (result) {
        tumblercopy(&isa, isaptr);
    }
    return result;
}
```

Notice: this same function handles both nodes and accounts — there is no `docreateaccount` distinct from `docreatenode`. Both call `createorglingranf` with `supertype=NODE, subtype=NODE`. The distinction between "node" and "account" is a naming convention outside the storage layer, not a structural distinction.

`createorglingranf` delegates to `createorglgr` at `granf2.c:111-128`:
```c
bool createorglgr(typetask *taskptr, typegranf fullcrumptr, typehint *hintptr, typeisa *isaptr)
{
    typegranbottomcruminfo locinfo;
    bool findisatoinsertgr();
    typecuc *createenf();

    if (!findisatoinsertgr ((typecuc*)fullcrumptr, hintptr, isaptr))
        return (FALSE);
    locinfo.infotype = GRANORGL;
    locinfo.granstuff.orglstuff.orglptr = createenf (POOM);  // ← a POOM, not a node-index
    reserve ((typecorecrum*)locinfo.granstuff.orglstuff.orglptr);
    locinfo.granstuff.orglstuff.orglincore = TRUE;
    locinfo.granstuff.orglstuff.diskorglptr.diskblocknumber = DISKPTRNULL;
    locinfo.granstuff.orglstuff.diskorglptr.insidediskblocknumber = 0;
    insertseq ((typecuc*)fullcrumptr, isaptr, &locinfo);
    rejuvinate ((typecorecrum*)locinfo.granstuff.orglstuff.orglptr);
    return (TRUE);
}
```

What gets created is a `POOM` enfilade (`createenf(POOM)`) — the same type used for documents. It is immediately inserted into `granf` at the newly-assigned address and left empty. No subsequent call populates this POOM with account references.

---

### 3. The Hint Mechanics — Depth Determines Address Hierarchy

`do2.c:78-84`:
```c
int makehint(INT typeabove, INT typebelow, INT typeofatom, typeisa *isaptr, typehint *hintptr)
{
    hintptr->supertype = typeabove;
    hintptr->subtype   = typebelow;
    hintptr->atomtype  = typeofatom;
    movetumbler (isaptr, &hintptr->hintisa);
}
```

And in `findisatoinsertnonmolecule` at `granf2.c:203-242`, the key line:

```c
depth = hintptr->supertype == hintptr->subtype ? 1 : 2;
```

| Call site | supertype | subtype | depth | Meaning |
|---|---|---|---|---|
| Node/account creation | `NODE(1)` | `NODE(1)` | 1 | One tumbler level deeper |
| New document under account | `ACCOUNT(2)` | `DOCUMENT(3)` | 2 | Two tumbler levels deeper |
| New version in same account | `DOCUMENT(3)` | `DOCUMENT(3)` | 1 | One level deeper |
| Atom in document | `DOCUMENT(3)` | `ATOM(4)` | 2 | Two levels deeper |

`xanadu.h:140-143`:
```c
#define NODE      1
#define ACCOUNT   2
#define DOCUMENT  3
#define ATOM      4
```

When `makehint(NODE, NODE, 0, parentAddr, &hint)` is called and `findisatoinsertnonmolecule` runs, the new node gets address `parentAddr + Δ(depth=1)` — one tumbler component beyond the parent. If parent is `1.0.1`, the first child node/account gets `1.0.1.0.1`. The second child would get `1.0.1.0.2`. These are just arithmetic positions in the global address space; there is no pointer from parent to child stored anywhere.

---

### 4. Finding Children Requires a Range Scan, Not a Pointer Walk

`fetchorglgr` (`granf2.c:22-81`) retrieves the orgl for a known exact address using `retrievecrums`:

```c
typeorgl fetchorglgr(typetask *taskptr, typegranf fullcrumptr, typeisa *address)
{
    ...
    if ((context = retrievecrums ((typecuc*)fullcrumptr, address, WIDTH)) == NULL)
        return NULL;

    if (!tumblereq((tumbler*)&context->totaloffset, address)) {
        crumcontextfree(context);
        return (NULL);    // ← exact match required
    }
    ...
}
```

An exact address match is required. There is no "give me all entries under prefix X" operation in the retrieval interface — `retrievecrums` looks up one specific address. To enumerate all accounts under a node, one would need to range-scan `granf` for the node's prefix interval (from `nodeAddr` to `nodeAddr + 1` in tumbler arithmetic). No such enumeration function is called at node/account creation time, and no index is maintained to avoid it.

---

### 5. Why POOM, Not a Dedicated Node Structure?

The architecture is uniform: **every orgl in `granf` is a POOM**, regardless of whether it belongs to a node, account, document, or link. The `GRANORGL` bottom-crum type (`granf2.c:119`) holds an `orglptr` pointing to a POOM enfilade. There is no `GRANNODE` or `GRANACCOUNT` bottom-crum type. Nodes and documents are structurally identical in storage — they differ only in how they were addressed (via `NODE,NODE` hint vs. `ACCOUNT,DOCUMENT` hint) and in whether content was subsequently inserted into their POOM.

---

### Conclusion

The node→account relationship is **entirely implicit in the tumbler prefix convention**. There is no dedicated node-level orgl that indexes accounts. Creating a node allocates an empty POOM orgl stored in `granf` at the node's address (identical to what document creation does), but nothing writes a child list into that POOM. The sole structural fact encoding the relationship is that a child account's tumbler address begins with the parent node's tumbler address — a pure arithmetic convention enforced at allocation time by `findisatoinsertnonmolecule` and nowhere else.
