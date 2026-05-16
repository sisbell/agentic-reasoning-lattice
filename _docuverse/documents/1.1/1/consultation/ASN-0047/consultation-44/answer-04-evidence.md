## Question 4 [evidence]

> Does udanax-green allocate node-level addresses dynamically at runtime (and if so, by what mechanism is uniqueness guaranteed across a federation), or is the node address fixed once at server startup with no in-system K.δ-equivalent for nodes?

## KB Synthesis

The KB cannot answer this question.

Every address in the KB starts with the node prefix `1.1` (e.g., account `1.1.0.1`, document `1.1.0.1.0.1`), but no finding explains how that prefix is assigned, whether it is fixed configuration or runtime-allocated, or what guarantees uniqueness across a federation.

What the KB does establish about the address and allocation machinery:

- The tumbler hierarchy is `Node.0.User.0.Doc.0.Element` by convention [SS-TUMBLER / Finding 0001], with `.0.` as field separators.
- All runtime address allocation (`findisatoinsertnonmolecule`, `findisatoinsertmolecule`) operates within the local `enf.enf` granfilade by query-and-increment [SS-ADDRESS-ALLOC, ST-ADDRESS-ALLOC]. The allocator has no cross-node awareness in any documented finding.
- All persistent state is in a single local file; no finding documents a federation protocol, cross-node coordination message, or K.δ-equivalent [SS-UNIFIED-STORAGE / Finding 0059].

The KB covers everything *below* the node level in depth, but contains no finding about node address assignment, no finding about what happens at server startup with respect to the node field, and no finding about how a multi-node deployment would arbitrate uniqueness. That tier of the system is simply not present in the extracted findings.

---

## Code Exploration

I have all I need. Here is the complete answer.

---

## Node Address Allocation in udanax-green

### Short Answer

Addresses are **allocated dynamically at runtime**, not fixed at startup. Uniqueness within a single server is guaranteed structurally — by walking the granfilade tree to find the current maximum and incrementing it. There is **no K.δ-equivalent for federation**; the server address component is a hardcoded constant with no mechanism for cross-server uniqueness.

---

### The Allocation Mechanism

The central allocator is `findisatoinsertnonmolecule()` [`backend/granf2.c:203-242`]. It is called whenever a new orgl (document, node, account, link) is created, via this chain:

```
fns.c → do1.c:docreatenewdocument → granf1.c:createorglingranf
                                   → granf2.c:createorglgr
                                   → granf2.c:findisatoinsertgr
                                   → granf2.c:findisatoinsertnonmolecule
```

The function takes a `typehint` — a struct [`xanadu.h:148-153`] carrying three fields:

```c
INT supertype;   /* parent type: ACCOUNT, DOCUMENT, NODE */
INT subtype;     /* child type: DOCUMENT, NODE, ATOM */
typeisa hintisa; /* the parent's tumbler address */
```

`makehint()` loads the caller's address into `hintisa` [`do2.c:78-84`]:

```c
int makehint(INT typeabove, INT typebelow, INT typeofatom, typeisa *isaptr, typehint *hintptr) {
    hintptr->supertype = typeabove;
    hintptr->subtype = typebelow;
    hintptr->atomtype = typeofatom;
    movetumbler(isaptr, &hintptr->hintisa);
}
```

For document creation [`do1.c:239`]:
```c
makehint(ACCOUNT, DOCUMENT, 0, &taskptr->account, &hint);
```

For new-version creation, when the target document belongs to this user [`do1.c:271`]:
```c
makehint(DOCUMENT, DOCUMENT, 0, isaptr, &hint);
```

---

### How the New Address Is Computed

`findisatoinsertnonmolecule` [`granf2.c:203-242`] computes the new address in two steps:

**Step 1** — Find the current maximum. `findpreviousisagr()` [`granf2.c:255-278`] walks the granfilade tree recursively, accumulating `cwid.dsas[WIDTH]` fields via `tumbleradd` and returning the highest ISA that is strictly less than `upperbound`:

```c
findpreviousisagr((typecorecrum*)fullcrumptr, &upperbound, &lowerbound);
```

**Step 2** — Increment to produce the new address. Two cases:

```c
if (iszerotumbler(&lowerbound) || !lowerbound_under_hint) {
    /* First child: parent.0.1 */
    tumblerincrement(&hintptr->hintisa, depth, 1, isaptr);   // granf2.c:237
} else {
    /* Subsequent child: truncate previous to parent depth, then increment */
    tumblertruncate(&lowerbound, hintlength + depth, isaptr);
    tumblerincrement(isaptr, tumblerlength(isaptr)==hintlength ? depth : 0, 1, isaptr); // granf2.c:240
}
```

`tumblerincrement()` [`tumble.c:599-623`] adds `bint` to mantissa position `idx + rightshift`:

```c
cptr->mantissa[idx + rightshift] += bint;
```

So the first document under account `1.1.0.1` gets address `1.1.0.1.0.1`; the second gets `1.1.0.1.0.2`; and so on.

---

### Why Uniqueness Holds Within a Single Server

There is **no counter variable**. The "counter" is the granfilade tree itself. Correctness relies on two implicit invariants:

1. The granfilade is the single, shared, authoritative store for all ISA addresses [`granf1.c:50-55` calls into the same `granfptr` global].
2. The server is single-threaded at the request level — `bed.c`'s `select()` loop [`bed.c:110-143`] dispatches one request at a time, so `findpreviousisagr` + `insertseq` is effectively atomic: no two allocations race.

---

### The Federation Question: No K.δ Equivalent

The server's "own" address is `defaultaccount`, a hardcoded literal in `be.c:37`:

```c
tumbler defaultaccount = {0,0,0,0, 1,1,0,1,0,0,0,0}; /* 1.1.0.1 */
```

This value is copied into `task.account` at startup [`be.c:88`]:
```c
movetumbler(&defaultaccount, &task.account);
```

In the multi-user (`bed.c`) path, each player carries their own `account` tumbler [`players.h:20`], and the dispatcher loads it per-request [`bed.c:123`]:
```c
task.account = player[user].account;
```

But there is **no mechanism** by which different servers receive distinct tumbler prefixes, no protocol to negotiate or register a server-specific K.δ, and no network address embedded in the tumbler structure. The field is literally called `"xanadu host and account tumbler"` in the comment at `players.h:20`, but that intent is not implemented — it's just the same `1.1.0.1` constant for every server running this codebase.

---

### Summary Table

| Property | Answer | Evidence |
|---|---|---|
| Allocation time | Dynamic, at each create operation | `granf2.c:117`, `do1.c:240` |
| Uniqueness mechanism | Walk tree for max, then increment | `granf2.c:217,237,240` |
| Persistent counter? | No — tree is the counter | No counter variable anywhere |
| Thread safety | Single-threaded dispatch via `select` | `bed.c:110-143` |
| Federation / K.δ | **Not implemented** — hardcoded `1.1.0.1` | `be.c:37,88` |
| Collision across servers | Would occur — no distinguishing prefix | `players.h:20`, `be.c:37` |
