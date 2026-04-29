## Question 4 [gregory]

> The three storage tiers have different mutability contracts: granfilade (append-only), spanfilade (write-only), and document arrangements (fully mutable) — was this three-tier mutability hierarchy an explicit design

## KB Synthesis

Yes, but with different degrees of explicitness across the three tiers.

**Granfilade: deliberately permanent**

The granfilade's append-only property was the most explicit design choice, directly implementing Nelson's "bytes never die, addresses never change" principle. I-address permanence wasn't an implementation detail — it's the entire foundation of transclusion. If I-addresses could be reused or deleted, the content identity system collapses: you couldn't distinguish "content that shares origin" from "content that happens to occupy the same address." [INV-NO-IADDR-REUSE], [INV-IADDR-IMMUTABILITY], and [INV-MONOTONIC] are not accidents — they're the implementation of a deliberate theoretical commitment.

**POOM: necessarily mutable**

The POOM mutability was also explicit, but for a different reason: it's the *only place mutability can live*. The whole point of the dual-enfilade architecture is to separate the stable identity layer (I-space) from the mutable view layer (V-space). If nothing could be deleted or rearranged in V-space, you'd have a write-once document system, not a hypertext editor. [SS-POOM-MUTABILITY] states this cleanly: the POOM is "the sole locus of destructive mutation." That concentration of mutability was intentional — it's what keeps the identity guarantees clean.

**Spanfilade: write-only by consequence more than declaration**

This is the most interesting case. [INV-SPANF-WRITE-ONLY] documents that no `deletespanf` function exists anywhere in the codebase — but that's subtly different from saying deletion was explicitly prohibited. The content identity associations in the spanfilade (DOCISPAN entries) are permanent because *the underlying fact they record is permanent*: if a document ever contained certain I-addresses, that historical fact doesn't become false when the V-stream changes. Deletion from V-space means the content is no longer *visible*, not that it was never *there*.

That said, the consequences of write-only spanfilade weren't fully anticipated. [EC-STALE-SPANF-REFERENCE] and [INT-DELETE-SPANF-DIVERGENCE] show that FIND_DOCUMENTS returns supersets of current document membership after deletion — a behavioral consequence that required post-hoc rationalization as "FIND_DOCUMENTS returns historically accurate results, not current state." I'm not sure that framing was in the original design notes; it reads more like an acceptable tradeoff that was recognized after the implementation was built.

**The coherent view**

The three tiers do form a coherent hierarchy when you see them through Nelson's lens:

- I-space: what *is* (permanent, content identity)
- Spanfilade: what *has been* (monotonically growing, historical associations)  
- POOM: what *appears now* (mutable, the current view)

Each tier answers a different temporal question. That architecture — whether fully articulated up front or discovered through implementation — coheres around the idea that information systems should accumulate knowledge rather than forget it. The permanence wasn't just a technical property; it was a statement about what a document system *should* do.

---

## Code Exploration

Now I have enough direct evidence. Here is my full analysis:

---

## Was the Three-Tier Mutability Hierarchy an Explicit Design?

**Short answer:** The hierarchy is architecturally real and behaviorally consistent, but the code contains no explicit design declarations—no comments stating "this tier is intentionally immutable." The contracts emerge from structural choices that reflect the Xanadu permascroll philosophy, with different degrees of intentionality at each tier.

---

### Tier 1: Granfilade — Append-Only

**What the code shows:** `granf2.c` exposes exactly two write operations:

- `inserttextgr()` [granf2.c:83-109] — appends GRANTEXT nodes via `insertseq()`
- `createorglgr()` [granf2.c:111-128] — appends GRANORGL nodes via `insertseq()`

There is no `deletegr()`, no `updategr()`, no "replace at address X" operation anywhere in the file. The address assignment functions (`findisatoinsertgr`, `findisatoinsertmolecule`, `findisatoinsertnonmolecule`) always seek the *next available* position, never an existing one:

```c
/* granf2.c:235-241 */
if (iszerotumbler(&lowerbound) || !lowerbound_under_hint) {
    /* Nothing under this hint - create first child as hintisa.0.1 */
    tumblerincrement(&hintptr->hintisa, depth, 1, isaptr);
} else {
    tumblertruncate (&lowerbound, hintlength + depth, isaptr);
    tumblerincrement(isaptr,tumblerlength(isaptr)==hintlength?depth:0,1,isaptr);
}
```

The granfilade is the **permascroll**: once text or a link-orgl is written at an ISA address, that binding is permanent. No API exists to revoke it.

**Is this explicit?** Not in the sense of a design comment. But the API boundary enforces it absolutely—not through guards but through the complete absence of mutation paths. The `klugefindisatoinsertnonmolecule()` function [granf2.c:183-201] (now superseded but retained) shows the team was actively reasoning about address assignment correctness; permanence is the precondition those fixes depend on.

---

### Tier 2: Spanfilade — Write-Only (Additive Index)

**What the code shows:** `spanf1.c` has one write operation:

- `insertspanf()` [spanf1.c:15-54] — inserts 2D span records via `insertnd()`

All other functions are read-only queries: `findlinksfromtothreesp()`, `findnumoflinksfromtothreesp()`, `finddocscontainingsp()`, `retrieveendsetsfromspanf()`, `retrievesporglsetinrange()`.

There is no `deletespanf()`, no update path. The spanfilade is a pure **link index** — it records where links point and what documents contain what spans. Entries are added when links are created; they are never retracted.

**Is this explicit?** Again, no design comment states this. But the spanfilade's role as a query index makes deletion semantically problematic: if you retract a span-to-document mapping, link following breaks. The additive-only contract is enforced by the absence of any deletion API, which is consistent with the fact that in Xanadu, the *existence* of a link is a permanent fact (even if the content it references lives in a mutable document arrangement).

---

### Tier 3: Document Arrangements (POOM Enfilade) — Fully Mutable

**What the code shows:** `edit.c` provides all three mutation modes:

- **Insert:** `insertcutsectionnd()` [edit.c:207-233]
- **Delete:** `deletend()` [edit.c:31-76] — calls `subtreefree()` [edit.c:60], which **physically frees POOM nodes** from memory
- **Rearrange:** `rearrangend()` [edit.c:78-160] — shifts crum positions by adjusting `cdsp` coordinates and calling `ivemodified()` [edit.c:127]

`deletend()` case 1 is unambiguous:

```c
/* edit.c:58-61 */
case 1:
    disown ((typecorecrum*)ptr);
    subtreefree ((typecorecrum*)ptr);
    break;
```

Nodes in a document's POOM enfilade are genuinely deleted — not just hidden. Case 2 goes further, mutating the crum's width in-place:

```c
/* edit.c:62-65 */
case 2:
    tumblersub (&ptr->cdsp.dsas[index], width, &ptr->cdsp.dsas[index]);
    /* This will get set to modified in setwisp */
    break;
```

The BERT write-lock system [bert.c:37-51] makes the mutability contract explicit at the access-control level — `WRITEBERT` is required for all three mutation operations, `READBERT` is the floor for queries:

```c
/* bert.c:44-49 */
type		    Not Open	#   Open READ	#  Open WRITE
  |		!owned	| owned	#conn==	|conn!=	#conn==	|conn!=
  v		--------+-------#-------+-------#-------+-------
READ		   0	|   0	#  READ |   0   # WRITE | -1
WRITE		  -1	|   0	#  -1	|  -1	# WRITE | -1
```

This is the one place in the codebase where mutability is *explicitly enforced by code*: you cannot call `dodeletevspan()` [do1.c:158-167] or `docopy()` [do1.c:45-65] without first acquiring WRITEBERT on the document.

---

### The Disabled `levelpull()` as a Design Signal

A key data point: `levelpull()` in `genf.c` is completely stubbed out [genf.c:318-342]:

```c
int levelpull(typecuc *fullcrumptr)
{
/*  typecuc *ptr; */
return(0);
/*
    if (!isfullcrum (fullcrumptr))
    ...
    disown (ptr);
    fullcrumptr->height--;
    transferloaf (ptr, fullcrumptr);
    ...
    freecrum (ptr);
*/
}
```

`levelpull()` would have compacted an enfilade by collapsing a level when it had only one son. The code that calls it (in `recombine.c`) still calls it — but it's now a no-op. This suggests the team deliberately chose not to implement a structural optimization that would mutate the tree in a non-trivial way, possibly because it complicated the persistence model. This is a **design choice by omission**, not unlike the granfilade's lack of delete.

---

### Summary

| Tier | Mutability | Enforcement Mechanism | Explicit? |
|------|-----------|----------------------|-----------|
| Granfilade | Append-only | No delete/update API exists | No — emergent from permascroll philosophy |
| Spanfilade | Write-only (additive) | No delete API exists | No — emergent from index semantics |
| Document arrangements | Fully mutable | BERT write-lock enforced by `checkforopen()` | **Yes** — BERT table is a written-out state machine |

The three-tier hierarchy is **architecturally intentional but not explicitly commented as such**. The granfilade and spanfilade constraints derive from the permascroll principle — content and links are permanent — but this principle is expressed through the absence of mutation APIs rather than through defensive code or documentation. The only tier with *explicit* mutability control is the document arrangement, where the BERT system [bert.c:37-51] is a deliberately designed access-control mechanism with a comment-documented state transition table.

The design intent lives in the Xanadu literature, not the C comments. The code faithfully implements it, but you have to know what you're looking for to see it.
