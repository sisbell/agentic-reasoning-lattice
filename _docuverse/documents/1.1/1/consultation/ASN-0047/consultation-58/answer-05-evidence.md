## Question 5 [evidence]

> In udanax-green's link allocation path (`findnextlinkvsa`/`docreatelink`), are the addresses `[d.0.1]` and `[d.0.2]` ever materialized as granfilade entries or atomtype-prefix bridges, or does the implementation produce `[d.0.s_L.1] = [d.0.2.1]` directly without the structural intermediates appearing in any allocator's domain?

## KB Synthesis

## Direct Answer: No Intermediate Entries Are Materialized

The implementation produces `d.0.2.1` directly. Neither `d.0.1` nor `d.0.2` (nor `d.0.3`) ever appear as granfilade entries. They are purely computational bounds used by the search algorithm.

### The Allocation Mechanism

From [SS-ADDRESS-ALLOC] and [SS-ADDRESS-SPACE] (Finding 0065), the link ISA allocation in `findisatoinsertmolecule` runs:

1. **Compute upperbound**: `tumblerincrement(docISA, 2, LINKATOM+1)` = `tumblerincrement(d, 2, 3)` = `d.0.3`. This is an arithmetically derived value — no granfilade write occurs.

2. **Search**: `findpreviousisagr(upperbound)` traverses the granfilade B-tree to find the highest existing ISA strictly below `d.0.3`. When no links exist yet, the result is the document orgl at `d` itself (the nearest previously allocated entry below the bound). [SS-ADDRESS-ALLOC, Finding 0021]

3. **First-link branch**: `lowerbound (= d) < d.0.2` evaluates TRUE → allocate directly at `d.0.2.1` via `tumblerincrement(lowerbound, 0, 1)` applied relative to the element-subspace boundary.

The addresses `d.0.2` and `d.0.3` serve only as tumbler arithmetic inputs to `tumblerincrement` and as range fences for `findpreviousisagr`. No `insertnd` or `createorglingranf` call deposits them into the tree.

### Why No Bridges Are Needed

The granfilade is described as "a single flat tree; the allocation algorithm enforces hierarchical structure by bounding searches to the parent's address range" [SS-ADDRESS-ALLOC, Finding 0021]. Hierarchy is an emergent property of tumbler prefix containment [SS-TUMBLER-CONTAINMENT], not a structural property requiring intermediate nodes.

The allocator is "stateless query-and-increment on different tumbler ranges via `findpreviousisagr`" [SS-ADDRESS-SPACE, Finding 0077]. It reads existing tree state and derives the next ISA arithmetically — no scaffolding entries are inserted.

### Tumbler Ordering Confirms the Gap

By [INV-TUMBLER-TOTAL-ORDER], in the granfilade before any link is created, the address space between `d` and `d.0.3` is empty (no entries). Text atoms reside at `d.3.0.x.x`, which sorts *above* `d.0.3` because digit 7 of `d.3...` is `3` versus `d.0.3`'s digit 7 of `0`, so `d.3.0.x.x > d.0.3`. [SS-ADDRESS-SPACE, Finding 0077] The link search range `(d, d.0.3)` therefore contains only previously allocated link orgls — nothing else.

### Consequence for `docreatelink`

When `docreatelink` calls `createorglingranf` for the first link, the single entry inserted is at `d.0.2.1`. Subsequent links land at `d.0.2.2`, `d.0.2.3`, etc. by the same query-and-increment pattern [SS-ADDRESS-SPACE, Finding 0065]. There are no atomtype-prefix bridges at `d.0.1`, `d.0.2`, or `d.0.3` in any allocator's domain.

---

## Code Exploration

I now have everything needed. Here is the full answer.

---

## Link Allocation Path: Address Materialization Analysis

### Short answer

Neither `[d.0.1]` nor `[d.0.2]` is ever materialized as a granfilade entry or as an explicit atomtype-prefix bridge node. The implementation produces `[d.0.2.1]` in a single `createorglgr` call. Both prefix values are transient intermediate computations inside `findisatoinsertmolecule`, discarded before any write reaches the enfilade.

---

### The call chain

`docreatelink` (do1.c:195) evaluates this short-circuit chain:

```c
createorglingranf (taskptr, granf, &hint, linkisaptr)     // do1.c:209
&& tumbler2spanset (taskptr, linkisaptr, &ispanset)        // do1.c:210
&& findnextlinkvsa (taskptr, docisaptr, &linkvsa)          // do1.c:211
&& docopy (taskptr, docisaptr, &linkvsa, ispanset)         // do1.c:212
…
&& insertendsetsinspanf (…)                                // do1.c:219
```

The only write into the granfilade is `createorglingranf` → `createorglgr` (granf1.c:50–54 → granf2.c:111–128). `createorglgr` calls `findisatoinsertgr` to compute the address, then calls `insertseq` once with that address (granf2.c:125). There is exactly one granfilade insertion per link, at the final resolved address.

---

### Address computation inside `findisatoinsertmolecule`

`makehint(DOCUMENT, ATOM, LINKATOM, docisaptr, &hint)` (do1.c:207) sets:

- `hint.subtype = ATOM`
- `hint.atomtype = LINKATOM = 2` (xanadu.h:146)
- `hint.hintisa = [d]` (the document ISA)

`findisatoinsertgr` (granf2.c:130) sees `subtype == ATOM`, confirms the document exists, then calls `findisatoinsertmolecule` (granf2.c:158).

```c
// granf2.c:162
tumblerincrement (&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound);
// → upperbound = [d.0.3]  (atomtype+1 = 3, right-shifted 2 positions from [d])

// granf2.c:163-164
clear (&lowerbound, sizeof(lowerbound));
findpreviousisagr ((typecorecrum*)fullcrumptr, &upperbound, &lowerbound);
// → lowerbound = highest granfilade entry below [d.0.3]
//   On first link with no text atoms: lowerbound = [d]  (the doc orgl itself)
//   On first link after text atoms:   lowerbound = [d.0.1.m] (last text orgl)
```

**Branch taken for LINKATOM (granf2.c:170–175):**

```c
tumblerincrement (&hintptr->hintisa, 2, 2, isaptr);   // line 171
// → isaptr = [d.0.2]   ← computed but NOT stored anywhere

if (tumblercmp (&lowerbound, isaptr) == LESS)          // line 172
    tumblerincrement (isaptr, 1, 1, isaptr);           // line 173
    // lowerbound ([d] or [d.0.1.m]) < [d.0.2] → TRUE for first link
    // → isaptr = [d.0.2.1]
else
    tumblerincrement (&lowerbound , 0, 1, isaptr);     // line 175
    // subsequent links: lowerbound = [d.0.2.n] → isaptr = [d.0.2.n+1]
```

After `findisatoinsertmolecule` returns, `findisatoinsertgr` calls `tumblerjustify(isaptr)` (granf2.c:154) and returns. Back in `createorglgr`:

```c
// granf2.c:125
insertseq ((typecuc*)fullcrumptr, isaptr, &locinfo);
// Exactly one granfilade node written, at [d.0.2.1]
```

`[d.0.2]` is only ever held in a local `isaptr` variable across two lines (171–173) and is overwritten by line 173. It is never passed to `insertseq` or any other write path.

---

### What about `[d.0.1]`?

The TEXTATOM allocator path (granf2.c:168–169) is symmetric. When `lowerbound = [d]` and `hintptr->hintisa = [d]`:

The **first branch** fires when `tumblerlength([d]) == tumblerlength([d])`:

```c
// granf2.c:166-167
tumblerincrement (&lowerbound, 2, hintptr->atomtype, isaptr);  // [d.0.1]
tumblerincrement (isaptr, 1, 1, isaptr);                       // [d.0.1.1]
```

For subsequent text atoms, the TEXTATOM branch fires:

```c
// granf2.c:169
tumblerincrement (&lowerbound, 0, 1, isaptr);  // [d.0.1.m] + 1 = [d.0.1.m+1]
```

In both text cases, `[d.0.1]` is a transient value overwritten on the next line or not computed at all. It is never passed to `insertseq`.

---

### `findnextlinkvsa` — vspace address, not granfilade

`findnextlinkvsa` (do2.c:151–167) allocates where the link's **self-reference span** sits in vspace — the content address stream, not the granfilade. It computes:

```c
// do2.c:157-158
tumblerincrement (&firstlink, 0, 2, &firstlink);  // [0.2]
tumblerincrement (&firstlink, 1, 1, &firstlink);  // [0.2.1]
```

This `[0.2.1]` is a document-relative vspace address, not an ISA. It is the floor below which link self-references are placed. This has no bearing on granfilade structure.

---

### Spanfilade entries — prefix by spantype, not atomtype

`insertendsetsinspanf` (do1.c:219) calls `insertspanf` for each end:

```c
// spanf1.c:21
prefixtumbler (isaptr, spantype, &crumorigin.dsas[ORGLRANGE]);
```

`prefixtumbler` (tumble.c:641–651) prepends `spantype` to the link ISA:

- LINKFROMSPAN = 1 → orglrange key = `[1.d.0.2.1]`
- LINKTOSPAN = 2 → orglrange key = `[2.d.0.2.1]`

These spantype prefixes (1, 2) are distinct from atomtype prefixes (TEXTATOM=1, LINKATOM=2) used in granfilade address arithmetic. The spanfilade contains no structural intermediate for `[d.0.2]`; its orglrange dimension is keyed directly from the final link ISA.

---

### Summary

| Address | Appears in granfilade? | Where it appears |
|---|---|---|
| `[d.0.1]` | No | Transient local in `findisatoinsertmolecule` lines 166–167, overwritten line 167 |
| `[d.0.2]` | No | Transient local in `findisatoinsertmolecule` line 171, overwritten line 173 |
| `[d.0.2.1]` | **Yes** | Stored by `insertseq` at granf2.c:125, first link orgl entry |
| `[1.d.0.2.1]` | Spanfilade only | Spanfilade ORGLRANGE, written by `prefixtumbler` at spanf1.c:21 |

The allocator in `findisatoinsertmolecule` uses `[d.0.2]` purely as a **comparison sentinel** — the floor of the LINKATOM namespace — to determine whether existing links already occupy it. It is not a structural node. The implementation produces `[d.0.2.1]` directly with a single `insertseq` call, and no atomtype-prefix bridge at `[d.0.1]` or `[d.0.2]` ever appears in any allocator's domain.
