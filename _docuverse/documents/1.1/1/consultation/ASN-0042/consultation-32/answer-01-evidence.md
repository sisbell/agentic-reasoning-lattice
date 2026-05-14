## Question 1 [evidence]

> When a node-level session invokes `docreatenewdocument`/`docreatenewversion` and the immediate user-field slots `1..hwm` under its node prefix have been allocated to delegated accounts, does the allocator produce a fresh address by advancing past those slots unilaterally, or does it require coordination with the sub-account sessions?

## KB Synthesis

The KB is sufficient to answer this directly.

**The allocator advances unilaterally, with no coordination required.**

The mechanism is documented in [SS-ADDRESS-ALLOC] (Finding 0021) and made explicit in [SS-ADDRESS-SPACE] (Finding 0061):

> Each INSERT queries the granfilade tree via `findpreviousisagr` to find the highest existing I-address below an upper bound, then increments by 1. The allocation is purely derived from current tree state — there is no cached "next available" pointer.

[SS-ADDRESS-SPACE] (Finding 0077) reinforces: there is no Σ.next counter. Allocation is a stateless query-and-increment over the global granfilade.

For `docreatenewdocument`/`docreatenewversion`, `findisatoinsertnonmolecule` [ST-ADDRESS-ALLOC]:
1. Computes `upperbound = tumblerincrement(hintisa, depth-1, 1)` (next sibling of the parent node).
2. Calls `findpreviousisagr` to find the highest existing address below that bound.
3. Applies the containment check ([SS-TUMBLER-CONTAINMENT]): verifies the found address is actually under the parent prefix via truncate-and-compare.
4. Allocates the next sibling of whatever was found — delegated account addresses included.

The delegated account slots (`node.0.1`, `node.0.2`, ...) are visible to `findpreviousisagr` because they reside in the same global granfilade tree, bounded by the same upper bound. The allocator finds the highest among them and increments past it. No session-local state, no inter-session signaling.

The single-threaded event loop ([INV-ATOMICITY], [INV-SEQUENTIAL-DISPATCH] Finding 0042) provides serialization — each operation runs to completion before the next — so concurrent sessions cannot interleave allocations, but this is structural serialization, not coordination. A node-level session simply reads the granfilade as it currently stands and allocates the next available address.

---

## Code Exploration

I have all the evidence I need. Here is the full answer.

---

## Address Allocation Under Delegated Slots: Fully Unilateral

**Short answer:** The allocator advances past delegated slots unilaterally. It has no knowledge of, and requires no coordination with, sub-account sessions. The granfilade tree is the sole source of truth.

---

### Entry Points

Both functions build a hint, then delegate entirely to `createorglingranf`:

**`docreatenewdocument`** [`do1.c:234–241`]:
```c
bool docreatenewdocument(typetask *taskptr, typeisa *isaptr)
{
    typehint hint;
    makehint (ACCOUNT, DOCUMENT, 0, &taskptr->account, &hint);
    return (createorglingranf (taskptr, granf, &hint, isaptr));
}
```
Always uses `taskptr->account` — the calling session's own account tumbler — as the hint anchor.

**`docreatenewversion`** [`do1.c:260–276`]:
```c
if (tumbleraccounteq(isaptr, wheretoputit) && isthisusersdocument(isaptr)) {
    makehint (DOCUMENT, DOCUMENT, 0, isaptr, &hint);
} else {
    makehint (ACCOUNT, DOCUMENT, 0, wheretoputit, &hint);
}
```
When called from `doopen` in `bert.c`, `wheretoputit` is always `&taskptr->account` [`bert.c:274, 290, 296`]. The DOCUMENT/DOCUMENT branch (depth-1, sub-version) fires only when the source doc is already in the caller's account. The ACCOUNT/DOCUMENT branch (depth-2, fresh slot) fires for everything else — and is structurally identical to `docreatenewdocument`.

---

### The Allocator: `findisatoinsertnonmolecule` [`granf2.c:203–242`]

This is where the slot is chosen. The full logic:

```c
depth = hintptr->supertype == hintptr->subtype ? 1 : 2;      // line 209
hintlength = tumblerlength (&hintptr->hintisa);               // line 211
tumblerincrement (&hintptr->hintisa, depth - 1, 1, &upperbound); // line 213
clear (&lowerbound, sizeof(lowerbound));                       // line 215
findpreviousisagr ((typecorecrum*)fullcrumptr, &upperbound, &lowerbound); // line 217
```

Then, if anything was found under the hint:
```c
tumblertruncate (&lowerbound, hintlength + depth, isaptr);           // line 239
tumblerincrement(isaptr, tumblerlength(isaptr)==hintlength?depth:0, 1, isaptr); // line 240
```

**There is no per-session high-water-mark variable anywhere.** The allocator reconstructs "next free" on every call by scanning the live tree.

---

### The Tree Scanner: `findpreviousisagr` [`granf2.c:255–278`]

```c
int findpreviousisagr(typecorecrum *crumptr, typeisa *upperbound, typeisa *offset)
{
    if (crumptr->height == 0) {
        findlastisaincbcgr ((typecbc*)crumptr, offset);   // line 264
        return(0);
    }
    for (ptr = findleftson((typecuc*)crumptr); ptr; ptr = findrightbro(ptr)) {
        if (...THRUME || ...ONMYRIGHTBORDER || !ptr->rightbro) {
            findpreviousisagr (ptr, upperbound, offset);  // line 272
            return(0);
        } else {
            tumbleradd(offset, &ptr->cwid.dsas[WIDTH], offset); // line 275
        }
    }
}
```

This is a pure tree walk. It finds the **highest address below `upperbound`** under the hint, accumulating width contributions from enfilade nodes. It does not check who allocated an entry, what session owns it, or whether it belongs to a sub-account. **Every entry in the tree under the hint is equally visible.**

---

### The Hint Window and Delegated Slots

For `ACCOUNT, DOCUMENT`, `depth = 2` [`granf2.c:209`]. With an account tumbler like `A`, the scan covers all addresses from `A` up to `A+1` (exclusive). If delegated sub-accounts have placed documents at `A.0.1`, `A.0.2`, `A.0.3`, then:

1. `findpreviousisagr` returns `lowerbound = A.0.3` — the highest extant entry.
2. The validity check at [`granf2.c:231–232`] confirms it is genuinely under `A`.
3. `tumblertruncate` at depth `hintlength + 2` truncates to `A.0.3`.
4. `tumblerincrement` yields `A.0.4` — the next free slot.

**No message is sent to any sub-account session. No shared counter is consulted. The parent advances unilaterally.**

---

### Session Account Identity

`taskptr->account` is set at connection time:

- **`bed.c:123`**: `task.account = player[user].account;`
- **`get1.c:199–201`**: populated from the client-provided tumbler via `gettumbler`; stored back into both `taskptr->account` and `player[user].account`

Each session carries a fixed account address. All `docreatenewversion` calls from `doopen` in `bert.c` pass `&taskptr->account` as `wheretoputit` — the allocator always works within the calling session's own account subtree.

---

### `bert.c` Is Not an Allocator

The bert table [`bert.c:13–29`] is a hash table of open-document records (`bertentry`). It tracks which connections have which documents open (`READBERT`/`WRITEBERT`), reference counts, and creation/modification flags. It plays no role in address allocation and has no hwm field. The document address is determined before `addtoopen` is ever called [`bert.c:275`, `297`].

---

### Conclusion

When a node-level session calls `docreatenewdocument` or `docreatenewversion`, the allocator:

1. Builds a hint anchored at `taskptr->account` [`do1.c:239, 275`].
2. Calls `findpreviousisagr` to find the highest address already in the tree under that prefix [`granf2.c:217`].
3. Increments by one past whatever it finds [`granf2.c:239–240`].

Slots allocated by delegated sub-accounts are **fully visible** to this scan — they live in the same granfilade — so the allocator naturally advances past them. There is no coordination protocol, no shared counter, no lock, no inter-session message. The tree is the authority, and the advancement is entirely unilateral.
