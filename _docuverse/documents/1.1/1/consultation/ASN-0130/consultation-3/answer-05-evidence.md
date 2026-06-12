## Question 5 [evidence]

> When udanax-green stores newly inserted text, does a single insertion mint consecutive I-addresses on the document's origin chain as one uninterrupted run, or can interleaved operations (on the same or other documents) leave one insertion's addresses non-contiguous?

## KB Synthesis

## Single Insertion: Always One Contiguous Run

A single INSERT of *N* bytes always mints exactly one contiguous I-address run. `inserttextingranf` locates the start address once via `findisatoinsertgr`, then calls `tumblerincrement(&lsa, 0, textlength, &lsa)` to advance by the full byte count in a single step. The resulting width is `tumblersub(end, start)` — one unbroken span of *N* addresses [ST-INSERT Finding 0031].

Because the backend event loop is single-threaded with run-to-completion dispatch, no other operation can interleave mid-INSERT [INV-ATOMICITY Finding 0042].

---

## Across Multiple Insertions: It Depends on What Intervenes

Content I-addresses are namespaced **per document**, not global. Each document owns a separate tumbler subrange for its text content, allocated via `findisatoinsertmolecule` with bounds derived from that document's ISA [SS-ADDRESS-SPACE Finding 0077]. Therefore:

**Operations on other documents cannot break contiguity** — they allocate into a different tumbler range entirely.

Within the *same* document's content subspace, contiguity between successive inserts depends on what happens between them:

| Interleaving operation | I-address contiguity |
|---|---|
| Nothing / DELETE / REARRANGE | **Contiguous** — these don't touch the granfilade content tree [FC-GRANF-ON-DELETE Finding 0061] |
| CREATENEWVERSION | **Contiguous** — allocates only a document address, not content [INV-MONOTONIC Finding 0077] |
| **CREATELINK** | **Broken** — allocates a link orgl in the same content subspace, advancing `max_iaddr` past the link's address range [INV-MONOTONIC Finding 0063] |

The CREATELINK case is observable: INSERT "ABC" + CREATELINK + INSERT "DEF" yields two distinct I-address spans (a gap where the link orgl sits), while INSERT "ABC" + DELETE + INSERT "DEF" produces one contiguous span [INV-MONOTONIC Finding 0063].

---

## Summary

- **One insertion** → one contiguous run, always.
- **Operations on other documents** → no effect (separate address namespaces).
- **Same-document interleaving** → contiguous unless CREATELINK intervenes, which allocates into the shared per-document content subspace and advances the allocation frontier.

---

## Code Exploration

I have all the evidence I need. Here is the complete analysis.

---

## Answer: I-Address Allocation for a Single Insertion

### Short answer

A single `insert` call **always mints one uninterrupted, contiguous run of I-addresses**. Interleaved operations — whether on the same document or a different one — **cannot** make that run non-contiguous, because:

1. Each FEBE request is processed **serially** (no preemption).
2. The allocator calls `findisatoinsertgr` **once** at the top of the insert, then advances a single cursor through the permascroll linearly.
3. Text atoms for different documents live in **non-overlapping subspaces** of the global granfilade.

---

### The execution path

#### `fns.c:84-98` — FEBE entry point
```c
void insert(typetask *taskptr)
{
    (void) getinsert (taskptr, &docisa, &vsa, &textset);
    putinsert (taskptr);
    if (!doinsert (taskptr, &docisa, &vsa, textset)) ...
}
```
Each `insert` request is dispatched from `bed.c:128` (`xanadu(&task)`) and runs to completion before the event loop iterates. The `select`-based loop at `bed.c:103-149` is single-threaded — no interleaving is possible within one request.

#### `do1.c:87-122` — `doinsert`
```c
bool doinsert(typetask *taskptr, typeisa *docisaptr, tumbler *vsaptr, typetextset textset)
{
    typehint hint;
    typespanset ispanset;
    INT ret;
    makehint(DOCUMENT, ATOM, TEXTATOM, docisaptr, &hint);   // do1.c:117
    ret = (inserttextingranf(taskptr, granf, &hint, textset, &ispanset)  // do1.c:118
           && docopy (taskptr, docisaptr, vsaptr, ispanset));
    return(ret);
}
```
`makehint` stores the document's own ISA as `hint.hintisa`, with `supertype=DOCUMENT`, `subtype=ATOM`, `atomtype=TEXTATOM`. This hint pins the allocation to a subspace rooted at the document's address.

`granf` (`xanadu.h:14`: `extern typegranf granf`) is the single global permascroll — every document's atoms live in it, partitioned by their document ISA prefix.

#### `granf1.c:44-47` — thin wrapper
```c
bool inserttextingranf(...)
{
    return (inserttextgr (taskptr, granfptr, hintptr, textset, ispansetptr));
}
```

#### `granf2.c:83-109` — `inserttextgr` (the allocator)

This is where contiguity is guaranteed:

```c
bool inserttextgr(typetask *taskptr, typegranf fullcrumptr, typehint *hintptr,
                  typetextset textset, typeispanset *ispansetptr)
{
    tumbler lsa, spanorigin;
    ...
    if (!findisatoinsertgr ((typecuc*)fullcrumptr, hintptr, &lsa))   // ONE allocation query
        return (FALSE);
    movetumbler (&lsa, &spanorigin);                                  // save start
    for (; textset; textset = textset->next) {
        locinfo.granstuff.textstuff.textlength = textset->length;
        movmem(textset->string, locinfo.granstuff.textstuff.textstring, ...);
        insertseq ((typecuc*)fullcrumptr, &lsa, &locinfo);            // store chunk at lsa
        tumblerincrement (&lsa, 0, textset->length, &lsa);            // advance by chunk size
    }
    ispanptr->stream = spanorigin;                                    // single ispan
    tumblersub (&lsa, &spanorigin, &ispanptr->width);                 // width = total length
    *ispansetptr = ispanptr;
    return (TRUE);
}
```

Three things make this atomic and contiguous:

1. **`findisatoinsertgr` is called exactly once** — the starting address `lsa` is fixed before any character is stored.
2. **`lsa` is advanced by `textset->length` after each chunk** (`tumblerincrement(&lsa, 0, textset->length, &lsa)`, `tumble.c:599-623`, `rightshift=0` means "add to the last digit"). This is a flat, sequential counter.
3. **A single `typeispan` is returned** with `stream = spanorigin` and `width = final_lsa − spanorigin` — the entire text from all chunks maps to one span.

If `textset` is a multi-node linked list (multiple chunks), all chunks still get consecutive addresses because the loop never re-queries `findisatoinsertgr`. The width is exactly the sum of all chunk lengths.

---

### How the starting address is chosen

#### `granf2.c:130-156` — `findisatoinsertgr`
```c
bool findisatoinsertgr(typecuc *fullcrumptr, typehint *hintptr, typeisa *isaptr)
{
    if (hintptr->subtype == ATOM) {
        if (!isaexistsgr (fullcrumptr, &hintptr->hintisa)) return FALSE;
        findisatoinsertmolecule (fullcrumptr, hintptr, isaptr);   // text/link atoms
    } else {
        findisatoinsertnonmolecule (fullcrumptr, hintptr, isaptr); // documents/accounts
    }
    tumblerjustify(isaptr);
    return (TRUE);
}
```

#### `granf2.c:158-181` — `findisatoinsertmolecule` (for TEXTATOM)
```c
static int findisatoinsertmolecule(typecuc *fullcrumptr, typehint *hintptr, typeisa *isaptr)
{
    typeisa upperbound, lowerbound;
    tumblerincrement (&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound);
    clear (&lowerbound, sizeof(lowerbound));
    findpreviousisagr ((typecorecrum*)fullcrumptr, &upperbound, &lowerbound);
    if (tumblerlength (&hintptr->hintisa) == tumblerlength (&lowerbound)) {
        // first insertion under this document
        tumblerincrement (&lowerbound, 2, hintptr->atomtype, isaptr);
        tumblerincrement (isaptr, 1, 1, isaptr);
    } else if (hintptr->atomtype == TEXTATOM) {
        tumblerincrement (&lowerbound, 0, 1, isaptr);   // increment from last address
    }
    ...
}
```

With `atomtype = TEXTATOM = 1`:
- `upperbound = hintisa + 2 levels + 2` — this is the upper bound of the document's **text atom subspace** `[D.0.1, D.0.2)`.
- `findpreviousisagr` scans the global granfilade for the **last existing address strictly below** `upperbound`. That search is bounded by `upperbound`, so it can only return an address inside this document's text subspace.
- If text already exists: `isaptr = lowerbound + 1` (the very next address after the last one stored).
- If no text exists yet: generates the first address at depth `hintisa + 2 + TEXTATOM`.

**Key consequence for interleaving across documents**: `upperbound` is derived from the calling document's `hintisa`. Because each document has a unique ISA, each document's text subspace `[D.0.1, D.0.2)` is disjoint from every other document's. `findpreviousisagr` cannot return an address from a different document's subspace.

---

### Why interleaved operations cannot cause non-contiguity

**Same-document interleaving** (e.g., a link creation or rearrange between two `insert` calls):

- `docreatelink` uses `atomtype = LINKATOM = 2` → allocates into `[D.0.2, D.0.3)`, a different subspace than text atoms `[D.0.1, D.0.2)`. `findisatoinsertmolecule` for the next text insert will still find the last text address and increment from it. No gap.
- `dodeletevspan` / `dorearrange` modify the POOM enfilade, not the permascroll. Permascroll addresses (`lsa` values) are permanent and never deleted or reused. A subsequent text insertion still finds the previous high-water mark in `[D.0.1, D.0.2)` and increments.

**Cross-document interleaving** (insert into doc2 between two inserts into doc1):

- Doc2's text goes into `[D2.0.1, D2.0.2)`. Doc1's `findisatoinsertmolecule` uses `upperbound` derived from D1, so it never sees D2's allocations. Completely non-interfering.

**The event loop** (`bed.c:103-149`) processes one `xanadu(&task)` call at a time — there is no preemption, no threads, no re-entry. A single `insert` request runs `inserttextgr` to completion before any other request can run. The concern about "mid-insertion interleaving" does not apply architecturally.

---

### Summary

| Scenario | Contiguous? | Why |
|---|---|---|
| Single `insert` call, one text chunk | Yes — always | `inserttextgr` allocates start once, advances `lsa` linearly |
| Single `insert` call, multi-chunk `textset` | Yes — always | Same loop, no re-query of `findisatoinsertgr` |
| Two `insert` calls to the same document | Yes — tightly packed | `findisatoinsertmolecule` always finds the last address and increments by 1 |
| `insert` into doc2 between two inserts into doc1 | No gap in doc1 | Doc2 uses a disjoint subspace; doc1's allocator ignores it |
| Link creation on doc1 between two text inserts | No gap in doc1's text | Link atoms live in `[D.0.2, D.0.3)`, not `[D.0.1, D.0.2)` |

A single insertion always produces **one uninterrupted I-address run**. Across multiple insertions on the same document, addresses are packed with **no gaps** regardless of what other operations run between them, because the permascroll text subspace per document is contiguous and address allocation always starts from the previous high-water mark.
