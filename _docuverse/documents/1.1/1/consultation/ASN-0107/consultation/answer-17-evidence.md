## Question 17 [evidence]

> Is the count monotonically non-decreasing across the lifetime of the store given that links are never retracted (INV-LINK-PERMANENCE) and the spanfilade only grows (FC-SPANFILADE-MONOTONIC)?

## KB Synthesis

Yes, the count is monotonically non-decreasing across the lifetime of the store. This follows from both cited properties independently, and they reinforce each other through the three-layer architecture.

**Link count in I-space**

[INV-LINK-PERMANENCE] establishes that no DELETELINK operation exists in the FEBE protocol. Once a link orgl is allocated in I-space via `createorglingranf`, it is permanent by P0. [SS-THREE-LAYER-MODEL] formalizes this: I-space is the permanent layer, and no operation removes from it. DELETEVSPAN on the 2.x subspace removes only the POOM entry, leaving the link orgl intact [Finding 0040]. Therefore `|link_orgls(t₁)| ≤ |link_orgls(t₂)|` for all `t₁ < t₂`.

**Spanfilade entry count**

[INV-SPANF-WRITE-ONLY] establishes that the spanfilade is append-only. Inspection of `spanf1.c` and `spanf2.c` reveals only insertion and query functions — no `deletespanf` or removal mechanism exists [Finding 0057, confirmed by Finding 0067]. The formal invariant is:

```
∀ t₁ < t₂ : spanf_entries(t₁) ⊆ spanf_entries(t₂)
```

DELETE does not call any spanf function [Finding 0057, `do1.c:162-171`]. This makes the spanfilade a historical journal, not a current-state index — stale entries accumulate after document deletions, which is the root cause of [EC-STALE-SPANF-REFERENCE].

**Combined consequence**

[SS-THREE-LAYER-MODEL] labels these as P0 (I-space permanence) and P0' (spanfilade monotonicity) respectively — distinct but complementary permanence properties. [INV-SPANF-GROWTH] further bounds growth rate: `|DOCISPAN| ≤ Σ_{all INSERT/COPY ops} |ispanset(op)|`, O(operations) not O(bytes).

The count is thus monotonically non-decreasing by construction, with the only growth trigger being CREATELINK (which writes to both layers atomically per [ST-CREATE-LINK]).

---

## Code Exploration

I now have all the evidence needed. Here is my complete answer.

---

## Is the Count Monotonically Non-Decreasing?

**Short answer: It depends on which count you mean. At the spanfilade data-structure level, yes. At the observable level through V-space queries, no — the two given invariants are not sufficient.**

---

### 1. What "the count" is

The FEBE protocol exposes link counting through `findnumoflinksfromtothreesp`, defined at `spanf1.c:105–115`:

```c
bool findnumoflinksfromtothreesp(typetask *taskptr, typespanf spanfptr,
    typespecset fromvspecset, typespecset tovspecset, typespecset threevspecset,
    typeispan *orglrange, INT *numptr)
{
  typelinkset linkset;
  INT n;
    if (!findlinksfromtothreesp(taskptr, spanfptr, fromvspecset,
            tovspecset, threevspecset, orglrange, &linkset))
        return(FALSE);
    for (n = 0; linkset; linkset = linkset->next, ++n);   // count walk
    *numptr = n;
    return (TRUE);
}
```

Everything depends on what `findlinksfromtothreesp` returns.

---

### 2. The full query path: V-space gates the spanfilade lookup

`findlinksfromtothreesp` at `spanf1.c:56–103` works in two distinct stages:

**Stage A — V→I conversion (goes through the POOM):**

```c
if (fromvspecset)
    specset2sporglset(taskptr, fromvspecset, &fromsporglset, NOBERTREQUIRED);
```

`specset2sporglset` at `sporgl.c:14–33` branches on item type:

```c
} else if (((typeitemheader *)specset)->itemid == VSPECID) {
    if (!(sporglsetptr = vspanset2sporglset(taskptr, &((typevspec *)specset)->docisa,
            ((typevspec *)specset)->vspanset, sporglsetptr, type)))
        return (FALSE);
```

`vspanset2sporglset` at `sporgl.c:44–48`:

```c
if (!findorgl(taskptr, granf, docisa, &orgl, type)) return (NULL);
for (; vspanset; vspanset = vspanset->next) {
    (void) vspanset2ispanset(taskptr, orgl, vspanset, &ispanset);  // POOM lookup
```

This calls `vspanset2ispanset` which traverses the document's orgl enfilade (the POOM, stored in `granf`) to convert V-positions to I-positions. **If content at those V-positions has been deleted, `vspanset2ispanset` returns an empty ispanset. No sporglset entries are produced.**

**Stage B — Early-exit on empty sporglset:**

```c
if (fromvspecset) {
    sporglset2linkset(taskptr, (typecuc*)spanfptr, fromsporglset, &fromlinkset, orglrange, LINKFROMSPAN);
    if (!fromlinkset) {
        *linksetptr = NULL;
        return (TRUE);   // spanf1.c:79–81 — exits with count 0
    }
}
```

If V→I conversion produced nothing, `fromlinkset` is NULL, and the function returns with `*linksetptr = NULL` before ever consulting the spanfilade. The count is zero.

**Stage C — Only if Stage A succeeds: search the spanfilade.**

`sporglset2linkset` → `sporglset2linksetinrange` at `sporgl.c:239–269` calls `retrieverestricted` to search the spanfilade for link I-addresses whose ORGL dimension overlaps the given I-span range.

---

### 3. The spanfilade internal state IS monotonically non-decreasing

FC-SPANFILADE-MONOTONIC is borne out by code. Every link creation calls `insertendsetsinspanf` at `do2.c:116–121`:

```c
bool insertendsetsinspanf(typetask *taskptr, typespanf spanfptr, typeisa *linkisaptr,
    typesporglset fromsporglset, typesporglset tosporglset, typesporglset threesporglset)
{
    if (!(
        insertspanf(taskptr, spanfptr, linkisaptr, fromsporglset, LINKFROMSPAN)
        && insertspanf(taskptr, spanfptr, linkisaptr, tosporglset, LINKTOSPAN)))
        return (FALSE);
```

This is called from `docreatelinkinternal` at `do1.c:191` and `docreatelink` at `do1.c:219`. The growth path is: `insertspanf` → `insertnd` → `adopt` → `++father->numberofsons` at `genf.c:519`.

**No corresponding delete path exists for the spanfilade.** Inspection of `spanf1.c` and `spanf2.c` (confirmed in Finding 0057, sourced at `do1.c:162–171` and `orglinks.c:145–152`): `dodeletevspan` only calls `deletend` on the document's POOM orgl, never on the spanfilade. There is no `deletespanf`, `removespanf`, or any function that calls `disown` on a spanfilade node. The spanfilade is **write-only** at the API level.

Therefore:
- **INV-LINK-PERMANENCE** ensures no mechanism exists to retire a link orgl from I-space, removing the only conceivable motivation for cleaning up spanfilade entries.
- **FC-SPANFILADE-MONOTONIC** is confirmed by code: `adopt` increments `numberofsons`, `disown` (`genf.c:395`) is never called on spanfilade nodes.

**Corollary:** The raw count of link-endset entries in the spanfilade is monotonically non-decreasing. Each `CREATELINK` call inserts new LINKFROMSPAN and LINKTOSPAN entries, and these are never removed.

---

### 4. The observable V-space query count is NOT monotonically non-decreasing

The two given invariants are **not sufficient** to guarantee the observable count.

The gap is V-space. `dodeletevspan` at `do1.c:162–171`:

```c
bool dodeletevspan(typetask *taskptr, typeisa *docisaptr, typevspan *vspanptr)
{
  typeorgl docorgl;
    return (
        findorgl(taskptr, granf, docisaptr, &docorgl, WRITEBERT)
        && deletevspanpm(taskptr, docisaptr, docorgl, vspanptr)
        /*&& TRUE*/ /* ht stuff */ );
}
```

`deletevspanpm` at `orglinks.c:145–152`:

```c
bool deletevspanpm(typetask *taskptr, tumbler *docisaptr,
                   typeorgl docorgl, typevspan *vspanptr)
{
    if (iszerotumbler(&vspanptr->width)) return (FALSE);
    deletend((typecuc*)docorgl, &vspanptr->stream, &vspanptr->width, V);
    logbertmodified(docisaptr, user);
    return (TRUE);
}
```

`deletend` at `edit.c:31–76` removes the V→I mapping crums from the document's orgl. After this, `vspanset2ispanset` called on those former V-positions returns an empty ispanset. The spanfilade entry is **still there** but **invisible** to V-specset queries.

The behavior is directly confirmed by empirical results (Finding 0029):

```
Before delete: find_links(source_spec) → [link_id]   (count = 1)
After delete:  find_links(source_spec) → []           (count = 0)
```

Even with INV-LINK-PERMANENCE + FC-SPANFILADE-MONOTONIC in force, deleting the content at a link's endpoint V-positions makes that link invisible to any V-specset query against those positions. The observable count drops to zero for that query.

---

### 5. The missing third invariant

The two given invariants preserve the data layer:

| Layer | Invariant | Effect |
|-------|-----------|--------|
| I-space (link orgls) | INV-LINK-PERMANENCE | Link records never deleted from granfilade |
| Spanfilade (endset index) | FC-SPANFILADE-MONOTONIC | Index entries never removed |
| V-space / POOM | **not constrained** | `deletend` can remove V→I mappings |

Because V-space is not constrained, any `DELETEVSPAN` call can cause a previously nonzero `findnumoflinksfromtothree` result to collapse to zero for queries that use V-specsets against the deleted positions.

To guarantee that the observable count is monotonically non-decreasing, a third invariant would be needed — something like "V→I mappings are never removed from the POOM" or equivalently "DELETEVSPAN is never called." Neither is given, and the code explicitly provides `deletend` at `edit.c:31–76` as the active deletion path.

---

### 6. Exception: I-specset queries

`specset2sporglset` at `sporgl.c:20–22` has a second branch:

```c
if (((typeitemheader *)specset)->itemid == ISPANID) {
    *sporglsetptr = (typesporglset)specset;
    sporglsetptr = (typesporglset *)&((typeitemheader *)specset)->next;
```

When specsets are passed as ISPANID (I-space addresses directly), there is no V→I conversion step. The sporglset is built directly from the provided I-spans, and the spanfilade is queried using those I-spans. In this case, given INV-LINK-PERMANENCE + FC-SPANFILADE-MONOTONIC, the count **is** monotonically non-decreasing: the spanfilade only gains entries, and the link I-addresses being queried are permanent.

---

### Summary

| Count | Monotonically non-decreasing? | Why |
|-------|-------------------------------|-----|
| Raw spanfilade entry count | **Yes** | FC-SPANFILADE-MONOTONIC + no `deletespanf` at code level |
| `findnumoflinksfromtothree` via I-specsets | **Yes** | Bypasses POOM; spanfilade-only query; both invariants hold |
| `findnumoflinksfromtothree` via V-specsets | **No** | V→I conversion fails when content is deleted via `dodeletevspan` / `deletend`; early exit at `spanf1.c:79–81` |

The two invariants INV-LINK-PERMANENCE and FC-SPANFILADE-MONOTONIC are **necessary but not sufficient** to guarantee monotonic growth of the observable link count. They successfully preserve the underlying data — link orgls at I-addresses, endset entries in the spanfilade — but the query mechanism's mandatory V→I stage at `sporgl.c:44–48` introduces a dependency on POOM state that neither invariant constrains.
