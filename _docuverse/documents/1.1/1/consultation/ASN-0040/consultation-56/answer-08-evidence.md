## Question 8 [evidence]

> Does udanax-green use one shared mechanism for address allocation and baptismal commitment, or two separate ones with the allocator feeding a distinct registry?

## KB Synthesis

One shared mechanism. The granfilade is simultaneously the allocator and the registry — allocation and baptismal commitment are the same single act.

**Allocation queries the same tree it commits into.** `findisatoinsertgr` dispatches to either `findisatoinsertmolecule` (content) or `findisatoinsertnonmolecule` (documents/links), both of which call `findpreviousisagr` to traverse the granfilade tree for the current maximum address, then increment by one. The resulting address is immediately written into that same granfilade tree — via `inserttextingranf`, `createorglingranf`, or equivalent. There is no separate "candidate address" handed off to a distinct registry. [SS-ADDRESS-ALLOC, Finding 0021; SS-ADDRESS-SPACE, Finding 0077]

**No global counter exists.** Allocation is a stateless pure function of current granfilade state: `next_addr(granf) = max_addr(granf) + 1`. This means the granfilade tree IS the authoritative namespace record. [INV-MONOTONIC, Finding 0061]

**The spanfilade is a secondary index, not the primary registry.** After granfilade commitment, `insertspanf` writes DOCISPAN or link-endpoint entries for discoverability — but the spec models spanfilade as derived state: `SpanEnfilade = Map<IAddress, Set<LinkISA>>` fully determined by what's in the granfilade. [SS-SPANF-OPERATIONS; FC-CONTENT-SPANF-ISOLATION]

**The granfilade is append-only** — once committed, an address is permanent. Delete and rearrange never touch it. [FC-GRANF-ON-DELETE; INV-NO-IADDR-REUSE]

So: one mechanism (granfilade), two index structures (granfilade + spanfilade), with the spanfilade feeding off granfilade events rather than constituting a separate registry of identity.

---

## Code Exploration

I have all the information I need. Here is the complete answer.

---

## Two Separate Mechanisms: Allocator into Enfilade, Commitment into BERT

Udanax-green uses **two distinct mechanisms** — an enfilade-based address allocator and a separate in-memory BERT registry — connected by an explicit call sequence in the operation layer. The allocator does not automatically commit to BERT; that step is a separate, explicit act.

---

### Mechanism 1: Address Allocation (the Enfilade Tree)

The allocator lives in `backend/granf2.c`. Its job is to find the next unused tumbler within a type hierarchy and plant a new node into the granfilade enfilade tree.

**Entry point** is `findisatoinsertgr()` [`granf2.c:130`], which dispatches on atom type:

```c
if (hintptr->subtype == ATOM) {
    findisatoinsertmolecule(fullcrumptr, hintptr, isaptr);   // line 142
} else {
    findisatoinsertnonmolecule(fullcrumptr, hintptr, isaptr); // line 152
}
tumblerjustify(isaptr);
```

**For non-atom types** (DOCUMENT, ACCOUNT, NODE), `findisatoinsertnonmolecule()` [`granf2.c:203`]:

1. Computes `upperbound = hintisa + depth-1 components` [`line 213`]
2. Calls `findpreviousisagr()` to scan the enfilade for the highest existing address below that bound [`line 217`]
3. If nothing exists yet under the hint, generates `hintisa.0.1` as the first child [`line 237`]:
   ```c
   tumblerincrement(&hintptr->hintisa, depth, 1, isaptr);
   ```
4. If items exist, truncates and increments the lowerbound [`lines 239–240`]:
   ```c
   tumblertruncate(&lowerbound, hintlength + depth, isaptr);
   tumblerincrement(isaptr, tumblerlength(isaptr)==hintlength ? depth : 0, 1, isaptr);
   ```

**For atom types** (TEXTATOM, LINKATOM), `findisatoinsertmolecule()` [`granf2.c:158`] similarly finds the highest previous isa under the document's atom subspace.

The address returned by these functions is then planted into the granfilade via `createorglgr()` [`granf2.c:111`]:

```c
if (!findisatoinsertgr((typecuc*)fullcrumptr, hintptr, isaptr))
    return (FALSE);
locinfo.infotype = GRANORGL;
locinfo.granstuff.orglstuff.orglptr = createenf(POOM);   // line 120
reserve((typecorecrum*)locinfo.granstuff.orglstuff.orglptr);
insertseq((typecuc*)fullcrumptr, isaptr, &locinfo);        // line 125
```

`insertseq()` is the call that makes the address **permanent in the enfilade tree** — it is now part of the on-disk data structure. This is allocation and structural commitment in one shot, but it has nothing to do with BERT.

---

### Mechanism 2: Baptismal Commitment (the BERT Registry)

The BERT registry is a **separate, in-memory, per-session hash table** declared as a file-static in `backend/bert.c`:

```c
#define NUMBEROFBERTTABLE 1327
static conscell *berttable[NUMBEROFBERTTABLE];   // bert.c:29
```

Each entry is a `bertentry` struct [`bert.c:13–19`]:

```c
typedef struct {
    int connection;
    tumbler documentid;
    char created, modified;
    int type;
    int count;
} bertentry;
```

The **baptism call** is `addtoopen()` [`bert.c:128`]:

```c
int addtoopen(tumbler *tp, int connection, int created, int type)
{
    hash = hashoftumbler(tp);
    ptr = eallocwithtag(sizeof(bertentry), BERTTAG);
    tumblercopy(tp, &ptr->documentid);   // line 140 — tumbler locked in
    ptr->connection = connection;
    ptr->count = 1;
    ptr->created = created;
    ptr->modified = FALSE;
    ptr->type = type;
    consp->next = berttable[hash];
    berttable[hash] = consp;             // line 150 — entered into registry
}
```

The hash function [`bert.c:234`] mixes the tumbler's exponent and mantissa digits using the `primes[]` array [`bert.c:26`] modulo 1327 (a prime).

BERT does **not** store document content — only session metadata: which connection has it open, whether it was newly created (`created`), whether it has been written to (`modified`), and what access mode (READBERT or WRITEBERT). `checkforopen()` [`bert.c:52`] enforces the concurrency rules — cross-connection read/write conflicts and same-connection upgrade paths.

---

### The Joining: How the Two Are Wired Together

The explicit join is visible in `docreatenewversion()` [`do1.c:260–299`]:

```c
bool docreatenewversion(typetask *taskptr, typeisa *isaptr, typeisa *wheretoputit, typeisa *newisaptr)
{
    // ...
    if (!createorglingranf(taskptr, granf, &hint, newisaptr))  // line 277
        return FALSE;
    // ... sets up vspan from source document ...

    addtoopen(newisaptr, user, TRUE, WRITEBERT);    // line 292 — BERT commitment
    docopyinternal(taskptr, newisaptr, &vspan.stream, &vspec);
    logbertmodified(newisaptr, user);               // line 295 — mark dirty
    doclose(taskptr, newisaptr, user);              // line 296 — remove from BERT
}
```

Step 1 (`createorglingranf`) allocates the new tumbler address and inserts it into the enfilade tree. Steps 2–4 (`addtoopen`, `logbertmodified`, `doclose`) open the new address in BERT, copy content in, mark it modified, then immediately close it. The `removefromopen()` logic [`bert.c:173`] is:

```c
status = bert->created && !bert->modified;
if (status) deleteversion(tp);
```

Because `logbertmodified` sets `modified=TRUE` before `doclose`, the condition is FALSE and the newly created document survives. An uncommitted document (created but never written to) would be deleted on close.

`exitbert()` [`bert.c:195`] sweeps the entire BERT table on connection exit — BERT entries do not outlive the session, confirming that BERT is a **transactional lock/rollback overlay**, not the permanent address registry. The permanent registry is the granfilade tree on disk.

---

### Summary

| | Allocator | BERT Registry |
|---|---|---|
| **Where** | `granf2.c` (`findisatoinsertnonmolecule`, `findisatoinsertmolecule`) | `bert.c` (`addtoopen`) |
| **Data structure** | Granfilade enfilade tree (on-disk B-tree) | In-memory hash table `berttable[1327]` |
| **What it stores** | The address as a tree node with content metadata | Per-session: connection, created/modified flags, access type |
| **Permanence** | Survives across sessions (written to disk via `insertseq`) | Ephemeral — cleared by `exitbert()` on disconnect |
| **Commitment moment** | `insertseq()` in `granf2.c:125` | `addtoopen()` in `bert.c:128–150` |
| **Rollback mechanism** | `deleteversion()` (called from `removefromopen`) | The BERT entry itself — `created && !modified` triggers deletion |

The allocator and the BERT registry are **two separate mechanisms** with different data structures serving different purposes. The allocator feeds the enfilade (the permanent structural store); BERT is a distinct, session-scoped hash table for access control and transactional rollback. They are joined explicitly in the operation layer — `createorglingranf()` followed immediately by `addtoopen()` — with no shared code path between them.
