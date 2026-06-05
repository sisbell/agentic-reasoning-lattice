## Question 14 [evidence]

> If a new link is created (CREATELINK) between two windowed reads, does the new link appear in a later window, and does its insertion disturb the cursor position of links already enumerated?

## KB Synthesis

## New Link Between Paginated Windows

### Does the new link appear?

FINDNEXTNLINKSFROMTOTHREE re-executes the **full** `findlinksfromtothreesp()` search on every call — there is no server-side cursor state [SS-PAGINATE-LINKS]. A newly created link is indexed in the spanfilade immediately by `insertendsetsinspanf` as part of CREATELINK [ST-CREATE-LINK, SS-SPANF-OPERATIONS]. If its endpoint I-addresses intersect the query range, it will be present in the full result set on the next call.

Whether it surfaces in a **later window** depends on where it falls in the result ordering relative to the cursor. The new link receives a monotonically higher ISA than existing links in the same home document [INV-MONOTONIC, SS-ADDRESS-ALLOC]. If the result list is ordered by link ISA (not explicitly confirmed in the KB for the intersection path in `spanf2.c`), the new link appears after all previously seen links and will be returned in a later window. If ordering is determined by span-dimension traversal order instead, the new link's position is not predictable and it could be silently skipped.

### Does it disturb the cursor?

The cursor is a link ISA tumbler found by linear scan with `tumblereq` [SS-PAGINATE-LINKS]. Creating a new link does not delete or modify any existing link ISA. Provided the cursor link still exists in the new result set (it wasn't deleted between calls), the walk finds it correctly and the position is undisturbed.

The only cursor-invalidation risk the KB documents is **deletion** of the cursor link between calls — which returns an empty result [SS-PAGINATE-LINKS, EC-CURSOR-INVALIDATION]. A new link creation does not trigger this.

### Summary

| Question | Answer |
|---|---|
| New link in full result? | Yes — spanfilade indexed at CREATELINK time |
| New link in later window? | Likely yes if ordered by ISA, but ordering not explicitly confirmed |
| Cursor structurally disturbed? | No — cursor link ISA unchanged by new link creation |
| Consistency guaranteed? | No — pagination is stateless; result set may shift between calls |

---

## Code Exploration

The finding write was denied, so I'll present the complete answer now without the file.

---

## Answer: CREATELINK Between Two Windowed Reads

### The Windowed Protocol

"Windowed reads" is `FINDNEXTNLINKSFROMTOTHREE` (opcode 31), implemented in `findnextnlinksfromtothreesp` (`spanf1.c:117-149`). The cursor is a **link ISA tumbler** passed by the client. Every call is entirely stateless — it re-executes the full search, scans linearly for the cursor, and returns what follows.

```c
// spanf1.c:124
if (!findlinksfromtothreesp(taskptr, spanf, fromvspecset, tovspecset, threevspecset, orglrangeptr, &linkset))
    return (FALSE);
// spanf1.c:129-133
for (; linkset; linkset = linkset->next) {
    if (tumblereq(&linkset->address, lastlinkisaptr)) {
        *nextlinksetptr = linkset->next;
        break;
    }
}
```

There is **no server-side cursor state**. The server does not know about prior calls.

---

### Does CREATELINK put the new link into spanf?

Yes, unconditionally. `docreatelink` (`do1.c:195-221`) terminates with:

```c
&& insertendsetsinspanf(taskptr, spanf, linkisaptr, fromsporglset, tosporglset, threesporglset)
```

`insertendsetsinspanf` (`do2.c:116-128`) calls `insertspanf` (`spanf1.c:15-54`) for each endpoint, which calls:

```c
// spanf1.c:51
insertnd(taskptr, (typecuc*)spanfptr, &crumorigin, &crumwidth, &linfo, SPANRANGE);
```

After CREATELINK returns, the new link's endpoint spans are in `spanf` and will be found by `findlinksfromtothreesp` on the very next call.

---

### Does the new link appear in a later window?

**Conditionally yes.** The key is enumeration order. `sporglset2linksetinrange` (`sporgl.c:239-269`) builds the link list by querying `spanf` via `retrieverestricted` (restricting by SPANRANGE = content I-spans), then appending each hit to the tail via `onlinklist` (`spanf2.c:42`):

```c
temp->next = linkset;  // appended at tail in enfilade traversal order
```

The order is **SPANRANGE traversal order** — i.e., I-space coordinate order of the link's *endpoint content spans* — not link ISA order.

So, given Window 1 returned [A, B, C] and cursor = C's ISA, then CREATELINK creates D:

| D's endpoint I-spans vs. C's | New full list | Cursor finds C | Window 2 sees D? |
|---|---|---|---|
| After C in I-space | [A, B, C, **D**, ...] | Yes | **Yes** |
| Before C in I-space | [A, B, **D**, C, ...] | Yes | **No — D is permanently before the cursor, silently skipped** |

---

### Does insertion disturb the cursor?

**No — the cursor ISA is stable.** CREATELINK allocates a fresh ISA for the new link via `createorglingranf` (`do1.c:209`). That ISA is always monotonically greater than all existing link ISAs (Finding 0061). It does not alter any existing link's ISA. The cursor link C is found correctly by `tumblereq` on every subsequent call.

**POOM V-shifts do not reach the cursor.** Finding 0052 established that CREATELINK calls `insertpm → makegappm` (`insertnd.c:54`, `insertnd.c:162`) which shifts V-positions of POOM entries after the insertion point. But `findnextlinkvsa` (`do2.c:151-167`) always places the new link at `vspanreach` — the current end of the document's V-extent. There are no POOM entries after `vspanreach`, so no existing entries shift. More critically, the windowed enumeration uses the spanfilade indexed by I-space (not the POOM in V-space), so POOM shifts cannot affect the cursor at all.

---

### The Permanent Blind Spot

The dangerous case: **CREATELINK with endpoint content older than the cursor link's content.** If link D references content at I-address 1.50 and the cursor link C references content at I-address 1.100, then D's I-span sorts before C's in the spanfilade traversal. Window 1 saw [A, B, C] before D existed. After CREATELINK, the full list is [A, ..., D, ..., C, ...]. The cursor finds C correctly, returns C.next. D is now *behind* the cursor — it was never seen, and it never will be in this pagination session.

This is not a bug in the cursor: the cursor (C's ISA) is faithfully preserved. It is an inherent limitation of **stateless pagination against a live mutable index**: insertions before the cursor position are invisible to the current pass.

---

### Summary

| Question | Answer | Evidence |
|---|---|---|
| Is the new link in `spanf` immediately? | Yes | `insertendsetsinspanf` → `insertspanf` → `insertnd` at `spanf1.c:51` |
| Does it appear in a later window? | Yes if its endpoint I-spans sort after the cursor link's spans | `sporglset2linksetinrange` traversal order, `spanf1.c:124-133` |
| Is it silently missed if endpoint I-spans sort before cursor? | Yes, permanently | `spanf1.c:131`: returns `linkset->next` after cursor; nothing before cursor is visited |
| Does CREATELINK corrupt the cursor ISA? | No | New ISA is fresh and monotonically larger; existing ISAs unchanged |
| Do POOM V-shifts reach the cursor? | No | POOM is V-space; cursor is link ISA (I-space); spanf indexed by I-space |
| What if cursor link is deleted? | Returns empty: `*nptr = 0` | `spanf1.c:136-139` |
