# Revision Consultation — ASN-0051

**Review:** review-1.md
**Date:** 2026-03-20 20:03

## Summary

5 REVISE items analyzed: 4 internal, 1 consulted (1 nelson, 1 gregory)

## Consultation Results

### Issue 1: SV6 (BoundaryExclusion) proof is wrong and the theorem is likely false

**Category:** BOTH
**Reason:** The counterexample is mathematically valid from the tumbler algebra, but deciding whether to salvage SV6 (by finding a missing allocator constraint) or abandon it requires both Nelson's design intent about coverage closure and evidence of how the green allocator actually behaves with child-depth addresses.

**Nelson question:** Does the Xanadu design intend that new content can never enter an existing link's endset coverage — i.e., is the "strap between bytes" meant to be literally closed to future allocations — and if so, what mechanism or constraint on allocation was meant to guarantee this?

**Nelson's Answer:**

## Answer: Endsets Are NOT Closed to Future Allocations (at All Levels)

Nelson does not intend that endsets are literally closed to future content. The design is more nuanced: the "strap between bytes" metaphor describes survivability under *editing*, not exclusion of future allocations. And at broader address levels, Nelson explicitly designs for spans that encompass content that doesn't yet exist.

### The Direct Evidence: Spans Grow

Nelson states explicitly that spans can encompass future content:

> "A span that contains nothing today may at a later time contain a million documents." [LM 4/25]

And ghost elements demonstrate the same principle:

> "It is possible to link to a node, or an account, even though there is nothing stored in the docuverse corresponding to them." [LM 4/23]

> "A link to or search of an account or node will find any of the documents under it." [LM 4/23]

A link whose endset covers an account span will, by design, match future documents created under that account. This is not an accident — it's the intended behavior.

### Two Levels of Analysis

The answer depends on what level of the tumbler hierarchy the endset addresses:

**Byte-level endsets (the "strap"):** At the element level within a single document, I-address allocation is sequential and append-only. New bytes get the next integer position: 1, 2, 3, ..., N, N+1. A link endset covering bytes 5–10 will never accidentally capture byte N+1 because N+1 > 10. The "strap" is effectively closed — but not by an explicit design constraint. It's a *consequence* of sequential allocation in the append-only Istream:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

**Document/account/server-level endsets:** At these levels, the forking mechanism creates new addresses *between* existing ones on the tumbler line. Document 2 can fork into 2.1, 2.2, 2.3 — all of which fall between address 2 and address 3. A span covering addresses 1 through 5 will capture documents 2.1, 2.2, etc. This is by design:

> "One digit can become several by a forking or branching process. This consists of creating successive new digits to the right; we call these 'under' the previous digit." [LM 4/20]

### What the "Strap" Metaphor Actually Means

The strap metaphor is about **survivability under editing**, not about exclusion of future content:

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes. This has a crucial advantage: it means that links can survive editing. If any of the bytes are left to which a link is attached, the link remains on them." [LM 4/42]

The language "bytes are left to which a link is attached" describes the link tracking *which specific bytes it was attached to at creation*. If those bytes are rearranged, split, or partially deleted, the strap follows them. The metaphor addresses what happens to existing bytes, not whether new bytes can enter the span's address range.

### The Mechanism (Such As It Is)

There is no *explicit* constraint or allocation rule that Nelson states to guarantee byte-level closure. What exists is an *architectural property*:

1. **Istream is append-only** — new bytes get addresses after existing bytes
2. **Element-level allocation is sequential** — no forking at the byte level is specified
3. **Links point to I-addresses** — not V-addresses, which do shift under editing

These together mean that at the byte level, new content cannot enter an existing endset's range. But Nelson never states this as a design constraint — it falls out of the append-only architecture.

### A Potential Gap: Link-Level Subdivision

Nelson notes that link element addresses *might* be subdivided in the future:

> "The subdivision of links by further digits (after '2' and the position) is a distinct possibility, and several possible uses have been discussed." [LM 4/31]

If link 2.5 could fork into 2.5.1, 2.5.2, those sub-links would fall within a span covering 2.5 to 2.10. Nelson does not address whether this would affect endsets that happen to span that range. This is an acknowledged area of future development, not a resolved design question.

### Summary

| Level | Closed to future allocations? | Mechanism |
|-------|-------------------------------|-----------|
| Bytes in a document | Yes (effectively) | Sequential append-only allocation |
| Links in a document | Currently yes, future uncertain | Sequential now, subdivision "a distinct possibility" |
| Documents under an account | **No** — by design | Forking creates sub-addresses within range |
| Accounts under a server | **No** — by design | Forking, ghost elements |

The "strap between bytes" is not meant to be literally closed to future allocations as a design principle. At the byte level, closure is a side effect of sequential allocation. At broader levels, Nelson explicitly intends the opposite: spans encompass future content, and this is a feature, not a bug. No explicit allocation constraint is specified to guarantee closure — the guarantee (where it exists) emerges from the append-only, sequential nature of Istream element allocation.

**Gregory question:** Does the udanax-green allocator ever use child-spawning (inc(t, 1) producing addresses like [D.0.n.1]) within I-address ranges that are already covered by existing link endset spans, or does the implementation constrain allocation patterns to prevent this?

**Gregory's Answer:**

## KB Synthesis

The allocator does **not** produce child-spawning addresses within existing link endset spans. The KB provides three independent constraints that prevent this.

---

## 1. Text I-address allocation uses `rightshift=0` — no child-spawning

[SS-ADDRESS-ALLOC] Finding 0061 and Finding 0033 establish that text content allocation calls:

```
tumblerincrement(&lowerbound, rightshift=0, 1, isaptr)
```

`rightshift=0` increments at the last significant digit — producing a sibling address (`I.n+1`), never a child (`I.n.1`). The algorithm queries `findpreviousisagr` to find the current maximum, then adds exactly `0.1` at the leaf level. There is no mechanism in the text insertion path to produce hierarchically deeper addresses.

## 2. Namespace partitioning separates permascroll addresses from orgl ISAs

[SS-CONTENT-IDENTITY] Finding 0009 establishes that link endsets contain **permascroll I-addresses** (the text content they reference), which start with `2.x`, while link orgl ISAs start with `1.x` (document namespace). These are non-overlapping tumbler ranges by the global address hierarchy [SS-ADDRESS-SPACE].

Link allocation (Finding 0065) uses `rightshift=2` only to compute the **upper bound** (`docISA.2.3`) that constrains the search. The actual address assigned is still `findpreviousisagr(max) + 0.1` within the bounded range — again no child-spawning.

## 3. Monotonicity makes the question moot for text I-addresses

[INV-MONOTONIC] establishes that all content I-address allocations are strictly increasing:

> `∀ alloc_a, alloc_b : time(a) < time(b) ⟹ iaddr(b) > iaddr(a)`

[INV-NO-IADDR-REUSE] confirms that allocations never fill gaps. Since link endsets reference I-addresses that were previously allocated (and are thus ≤ current max), any new allocation (at max+1) is **always strictly beyond** every existing endset span. There is no code path that produces a new I-address that falls within `[endset.origin, endset.origin + endset.width)`.

---

## The one complication: link orgl allocation disrupts text contiguity

[ST-CRUM-BOUND] Finding 0063 shows that `CREATELINK` allocates a link orgl ISA in the granfilade, advancing the allocation counter shared with text. This creates a **gap** in the text I-address sequence (INSERT "ABC" → I.1–I.3, CREATELINK consumes space, INSERT "DEF" → I.4+), observable as two shared span pairs in `compare_versions`. But this gap does not cause child-spawning — it just means the next text block starts further along the monotonic sequence, still strictly beyond all existing endset spans.

---

## Summary

The implementation constrains allocation patterns to prevent intersection with existing endset spans through:
1. `rightshift=0` in `tumblerincrement` for content → siblings only, never children [SS-ADDRESS-ALLOC]
2. Separate namespaces for permascroll (`2.x`) vs orgl (`1.x`) addresses [SS-CONTENT-IDENTITY]
3. Element-field partitioning within document namespace (field 2 for links, field 3 for text) [SS-ADDRESS-ALLOC] Finding 0065
4. Strict monotonic allocation with no reuse [INV-MONOTONIC, INV-NO-IADDR-REUSE]

The `rightshift=2` invocation only appears in bound computation, not in address assignment. No production code path produces a child address within an occupied I-span.

---

## Code Exploration

---

## Answer: Does the Allocator Use Child-Spawning Within Existing Link Endset Spans?

### The Short Answer

Child-spawning (specifically the `tumblerincrement(isaptr, 1, 1, isaptr)` call that converts `D.0.2` → `D.0.2.1`) **does occur**, but **only when allocating the very first link** under a document, and the implementation **does not check the spanfilade at all**. The design relies on the structural separation of TEXTATOM/LINKATOM address subspaces to prevent overlap — not on explicit spanfilade consultation.

---

### The Complete Allocation Path for a Link ISA

**Entry point:** `docreatelink` [do1.c:195]:
```c
makehint(DOCUMENT, ATOM, LINKATOM, docisaptr, &hint);
createorglingranf(taskptr, granf, &hint, linkisaptr)
```
This calls `findisatoinsertgr` → `findisatoinsertmolecule` because `hintptr->subtype == ATOM`.

**`findisatoinsertgr`** [granf2.c:130-156]:
```c
if (hintptr->subtype == ATOM) {
    if (!isaexistsgr(fullcrumptr, &hintptr->hintisa)) { return FALSE; }
    findisatoinsertmolecule(fullcrumptr, hintptr, isaptr);
}
```
No spanfilade is mentioned here or anywhere in the call chain.

**`findisatoinsertmolecule`** [granf2.c:158-181]:
```c
tumblerincrement(&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound);
// For LINKATOM=2: upperbound = D + .0.3
clear(&lowerbound, sizeof(lowerbound));
findpreviousisagr((typecorecrum*)fullcrumptr, &upperbound, &lowerbound);
// Searches the GRANFILADE ONLY — no spanfilade query
```

The three branches for LINKATOM (when `tumblerlength(hintisa) != tumblerlength(lowerbound)`):

```c
} else if (hintptr->atomtype == LINKATOM) {
    tumblerincrement(&hintptr->hintisa, 2, 2, isaptr);   // isaptr = D.0.2
    if (tumblercmp(&lowerbound, isaptr) == LESS)
        tumblerincrement(isaptr, 1, 1, isaptr);           // CHILD-SPAWN: D.0.2 → D.0.2.1
    else
        tumblerincrement(&lowerbound, 0, 1, isaptr);      // SIBLING: D.0.2.k → D.0.2.(k+1)
}
```
[granf2.c:170-175]

---

### When Does Child-Spawning Fire?

`tumblerincrement(isaptr, 1, 1, isaptr)` (the `inc(t, 1)` path) fires when:

- `lowerbound < D.0.2`

This means **no previous link ISA exists** in the granfilade for this document. Specifically:
- If the granfilade for document D contains only the document orgl itself (`D` at length 4), `lowerbound = D` (same length as `hintisa`) → **this goes to the same-length branch**, which also uses a similar pattern: `tumblerincrement(&lowerbound, 2, LINKATOM, isaptr)` then `tumblerincrement(isaptr, 1, 1, isaptr)` [granf2.c:166-167].
- If the granfilade has only text atoms (`D.0.1.x`), those are LESS than `D.0.2` → child-spawn fires → result: `D.0.2.1`.

After the first link, `lowerbound = D.0.2.k` (a previous link ISA, GREATER than `D.0.2`) → sibling increment: `D.0.2.(k+1)`. **Child-spawning is a one-time event per document's link subspace.**

---

### What Are the TEXTATOM and LINKATOM Subspaces?

From [xanadu.h:145-146]:
```c
#define TEXTATOM  1
#define LINKATOM  2
```

Under document D:
- Text atoms live at: `D.0.1.x` (TEXTATOM subspace)
- Link ISAs live at: `D.0.2.x` (LINKATOM subspace)

Since `D.0.1.* < D.0.2.*` in tumbler ordering (position n+1 of mantissa: `1 < 2`), these subspaces are **disjoint and ordered**. `findpreviousisagr` searching below `D.0.3` will find text atoms if they are the highest existing content — but those are in the wrong subspace to trigger overlap.

---

### How Link Endset Spans Are Stored in the Spanfilade

**`insertendsetsinspanf`** [do2.c:116-128]:
```c
bool insertendsetsinspanf(..., typeisa *linkisaptr, typesporglset fromsporglset, ...) {
    insertspanf(taskptr, spanfptr, linkisaptr, fromsporglset, LINKFROMSPAN)
    insertspanf(taskptr, spanfptr, linkisaptr, tosporglset, LINKTOSPAN)
    // optional three-span...
}
```

**`insertspanf`** [spanf1.c:22-52]:
```c
prefixtumbler(isaptr, spantype, &crumorigin.dsas[ORGLRANGE]);
// ORGLRANGE = prefixtumbler(linkisa, LINKFROMSPAN=1, ...) = "1.linkisa"
...
movetumbler(&lstream, &crumorigin.dsas[SPANRANGE]);
// SPANRANGE = the endpoint's I-span (text content or other link ISAs)
insertnd(taskptr, (typecuc*)spanfptr, &crumorigin, &crumwidth, &linfo, SPANRANGE);
```

So each spanfilade entry has:
- **ORGLRANGE axis**: a prefixed derivation of the link ISA (not the ISA itself)
- **SPANRANGE axis**: the I-addresses of the endpoint content (the text spans the link points to)

For typical links to text content: SPANRANGE = `D.0.1.n` to `D.0.1.m` — strictly in TEXTATOM subspace, below `D.0.2.*`. The newly allocated link ISA `D.0.2.k` cannot fall inside a text span because `D.0.2.k > D.0.1.*` by definition.

---

### Width of a Link ISA's I-Span

`tumbler2spanset` [do2.c:48-61] — called in `docreatelink` to create the ispan for the link's own position:

```c
tumblerincrement(&spanptr->width, tumblerlength(tumblerptr)-1, 1, &spanptr->width);
```

For `tumblerptr = D.0.2.1` (length 7): `rightshift = 6`, starting from zero:
- width gets mantissa[0]=1 with exp=-6
- Result: one unit at depth 7

Adding this width to `D.0.2.1`:
```
D.0.2.1 [1,1,0,1,0,2,1] exp=0
+width  [1,0,0,0,0,0,0] exp=-6 (= position 6)
= [1,1,0,1,0,2,2] = D.0.2.2
```

**Each link ISA has a half-open unit span `[D.0.2.k, D.0.2.(k+1))`**. The next allocated ISA `D.0.2.(k+1)` falls exactly on the right boundary — `ONMYRIGHTBORDER` in `intervalcmp` [tumble.c:158] — which is **not** inside the span.

---

### No Spanfilade Check Exists

Searching the code for any interaction between the granfilade allocator and the spanfilade:

- `findisatoinsertmolecule` [granf2.c:158-181]: calls only `findpreviousisagr` on `fullcrumptr` (the granfilade)
- `findpreviousisagr` [granf2.c:255-278]: recurses on the granfilade tree exclusively
- `findisatoinsertnonmolecule` [granf2.c:203-241]: same — only granfilade

**There is no call to any spanfilade function during I-address allocation.**

---

### Structural Guarantee vs. Explicit Checking

The implementation **constrains allocation patterns through structure, not explicit checking**:

| Potential conflict type | Resolution mechanism |
|---|---|
| New link ISA overlaps existing text spans | Impossible: text at `D.0.1.*`, links at `D.0.2.*`, different subspace |
| New link ISA overlaps previous link ISA spans | Impossible: sequential allocation with unit-width spans, new ISA = right boundary of previous span |
| New link ISA overlaps spans of OTHER documents' content | Impossible: different document prefixes entirely |
| First link ISA (`D.0.2.1`) conflicts with pre-existing spans in link subspace | Only conceivable if a previous endset spanned `[D.0.2.1, ...)` before any link in D was created. This cannot happen because endset spans are created **during** link creation, and `D.0.2.1` is allocated before endsets are inserted [do1.c:209 before 219] |

---

### Conclusion

**Yes, child-spawning `inc(t, 1)` does produce `D.0.2.1`-style addresses** — specifically via `tumblerincrement(isaptr, 1, 1, isaptr)` at [granf2.c:173] — but only for the **first link under each document** (when the LINKATOM subspace `D.0.2.*` is empty). Subsequent links use the sibling increment at [granf2.c:175].

**The implementation does not explicitly constrain allocation against the spanfilade.** `findpreviousisagr` [granf2.c:255] searches only the granfilade. The design instead relies on two architectural invariants:

1. **TEXTATOM (=1) and LINKATOM (=2) subspaces are disjoint** [xanadu.h:145-146] — text-content endset spans in `D.0.1.*` cannot reach into `D.0.2.*`
2. **Sequential granfilade-based allocation** guarantees each new ISA `D.0.2.k` equals exactly the right boundary of the span covering the previous ISA `D.0.2.(k-1)` — which in half-open interval semantics means it is never "inside" that span

The potential gap: if a user crafted endset I-spans that explicitly covered future link ISA territory (e.g., by spanning link references to include `D.0.2.k` where k hasn't been allocated yet), the allocator would have no defense. But this cannot arise in practice because the docreatelink sequence allocates the link ISA at [do1.c:209] **before** inserting its endsets at [do1.c:219] — ensuring the ISA exists in the granfilade before any span references it.
