## Question 2 [evidence]

> Does udanax-green's find-numbers-of-links operation exclude nullified or retracted links from its tally, or does it count every link resident in the store?

## KB Synthesis

## FINDNUMOFLINKSFROMTOTHREE Counts Discoverable Links Only — No Nullification Exists

**Short answer:** The operation counts every link currently discoverable via I-address intersection with the input specsets. Udanax-green has no "nullified" or "retracted" link concept at all — links are permanent — but orphaned links (whose endpoint content has been deleted from all V-streams) are silently excluded because the I-address intersection search returns nothing for them.

---

### Mechanism

[SS-FIND-LINKS, Finding 0035] is unambiguous:

> FINDNUMOFLINKSFROMTOTHREE is a trivial wrapper around FINDLINKSFROMTOTHREE. It calls `findlinksfromtothreesp()` to materialize the complete linked list of matching links, then walks the list counting elements. There is no count-only optimization.

The search path: caller's V-specsets → I-addresses (via current POOM) → spanfilade lookup for overlap → intersect from/to/three result sets → count. The count equals the cardinality of what FINDLINKSFROMTOTHREE would return.

---

### Why No Nullification Exists

[INV-LINK-PERMANENCE]: "There is no DELETELINK operation in the FEBE protocol. Once created, a link exists forever." The spanfilade is append-only [INV-SPANF-WRITE-ONLY] — no removal path exists at any layer.

---

### What Actually Gets Excluded

The filtering is implicit, not explicit:

**Orphaned links excluded:** [EC-ORPHANED-LINK] / [PRE-FIND-LINKS, Finding 0029] — if a link's endpoint content has been deleted from all documents' V-streams, no query specset will produce I-addresses that intersect the link's endpoint I-addresses. The spanfilade entry persists, but the search returns zero matches. These links are uncountable via this operation.

**Reverse-orphaned links still counted:** [EC-REVERSE-ORPHAN] — a link removed from its home document's POOM via `DELETEVSPAN(2.x)` is *still discoverable* via the spanfilade. `find_links(source_specs) → [link_id]` still works. FINDNUMOFLINKSFROMTOTHREE counts it.

**Stale spanfilade entries:** [INT-DELETE-SPANF-DIVERGENCE] — DELETE never removes spanfilade entries. However, since the count depends on *query I-address intersection* (not on enumerating all spanfilade entries), stale entries only affect the count if a caller happens to query content whose I-addresses appear in stale entries — which would mean that content is still present in *some* document's V-stream, making those links legitimately discoverable.

---

### Summary Table

| Link state | Counted? | Reason |
|---|---|---|
| Normal link, endpoint content present | Yes | I-address overlap found |
| Reverse orphan (POOM entry deleted, I-space intact) | Yes | Spanfilade + I-space still intact [EC-REVERSE-ORPHAN] |
| Orphaned (endpoint content deleted from all V-streams) | No | No I-address intersection possible [EC-ORPHANED-LINK] |
| "Nullified/retracted" | N/A | Concept does not exist [INV-LINK-PERMANENCE] |

The tally is purely a function of current V-stream state relative to the input specsets — not of any explicit link lifecycle flag.

---

## Code Exploration

I have traced the complete call chain. Here is the answer.

---

## Does `find-numbers-of-links` exclude nullified or retracted links?

**No — it counts every matching link in the store, unconditionally. Nullification and retraction do not exist in udanax-green's data model or operation set.**

---

### Call chain

```
fns.c:204   findnumoflinksfromtothree()
  do1.c:355   dofindnumoflinksfromtothree()
    spanf1.c:105  findnumoflinksfromtothreesp()
      spanf1.c:110    findlinksfromtothreesp()         ← retrieves matching links
      spanf1.c:112    for(n=0; linkset; linkset=linkset->next, ++n)  ← raw count
```

### Key evidence

**1. The count loop is unconditional** [`spanf1.c:112`]:

```c
for (n = 0; linkset; linkset = linkset->next, ++n);
*numptr = n;
```

Every element in the returned `linkset` is counted. There is no `if (link->status != NULLIFIED)` guard or anything like it.

**2. The `typelink` struct has no status field** [`xanadu.h:98-107`]:

```c
typedef struct structtypeaddress {
    struct structtypeaddress *next;
    typeitemid  itemid;
    typeisa     address;          /* just a tumbler address */
} typeaddress;
typedef typeaddress typelink;
typedef typelink  * typelinkset;
```

`typelink` carries only `next`, `itemid`, and `address`. There is nowhere to record nullification or retraction state.

**3. Link retrieval has no filter** [`sporgl.c:263-266`]:

```c
for (c = context; c; c = c->nextcontext) {
    beheadtumbler(&c->totaloffset.dsas[ORGLRANGE], &linksa);
    onlinklist(taskptr, linksetptr, &linksa);    /* append, no filter */
}
```

`sporglset2linksetinrange` adds every link ISA returned by the enfilade query, with no status check.

**4. `onlinklist` only deduplicates** [`spanf2.c:26-44`]:

```c
for (temp = *linksetptr; nextlink = temp->next; temp = nextlink) {
    if (tumblereq(&temp->address, linkisaptr))
        return(0);     /* duplicate — skip; still no status filter */
}
temp->next = linkset;
```

The only gate is address equality (deduplication). No concept of validity state.

**5. No nullify/retract operations exist anywhere.** A search across all `.c` and `.h` files finds zero occurrences of `nullif`, `retract`, `NULLIF`, `RETRACT`, `deletelinkop`, or any cognate. The `init.c` dispatch table (`requestfns[]`) registers only: `createlink`, `findlinksfromtothree`, `findnumoflinksfromtothree`, `findnextnlinksfromtothree`, and `followlink`. There is no delete-link, nullify-link, or retract-link slot.

**6. Link creation is append-only** [`do1.c:195-221`]:

`docreatelink` inserts into the granfilade and spanfilade; there is no corresponding removal path. Once a link is created, it is permanent.

---

### Conclusion

`find-numbers-of-links` (`FINDNUMOFLINKSFROMTOTHREE`, opcode 29) tallies **every link resident in the spanfilade** that satisfies the from/to/three endpoint intersection. Because udanax-green has no link-status field, no nullify or retract operation, and no deletion path, "all links in the store" and "all non-nullified links" are identical sets. The theoretical Xanadu concepts of nullification and retraction were never implemented in this codebase.
