# Revision Consultation — ASN-0025

**Review:** review-6.md
**Date:** 2026-03-07 09:25

## Summary

7 REVISE items analyzed: 6 internal, 1 consulted (0 nelson, 1 gregory)

## Consultation Results

### Issue 6: REARRANGE parameters and precondition underspecified

**Category:** GREGORY
**Reason:** The Gregory note mentions `slicecbcpm` and a "move step (phase 2)" but the operation's parameter structure (move? swap? arbitrary permutation?) is not established. The ASN needs to know what the implementation actually supports to decide the right specification level.

**Gregory question:** What are the parameters to the rearrange operation in udanax-green — does it take a source span and a target position (cut-paste move), two spans to swap, or something more general, and what is the entry-point function signature?

**Gregory's Answer:**

## KB Synthesis

## REARRANGE Parameters and Entry Point

### Two Modes, Defined by Cut Count

REARRANGE is not a cut-paste move or a simple two-span swap. It takes an ordered list of **cut positions** (V-addresses) and operates on the regions between them. The mode is determined by how many cuts are provided:

**Pivot (3 cuts):** `rearrange(doc, [c1, c2, c3])`
- Region 1 = `[c1, c2)`, Region 2 = `[c2, c3)`
- Swaps the two adjacent regions around the pivot point
- Result: Region 2 appears first, then Region 1

**Swap (4 cuts):** `rearrange(doc, [c1, c2, c3, c4])`
- Region 1 = `[c1, c2)`, Middle = `[c2, c3)`, Region 2 = `[c3, c4)`
- Exchanges Region 1 and Region 2; the middle segment stays in place (though its V-addresses shift if the swapped regions differ in size)

Exactly 2 cuts is rejected with "Wrong number of cuts". [PRE-REARRANGE, Finding 0006]

### Entry Point

The backend entry point is `rearrangend()` in `backend/edit.c:78-160`. It operates directly on the document's POOM enfilade. The FEBE opcodes are command 3; the client exposes `session.pivot()` and `session.swap()`. [ST-REARRANGE, Finding 0056]

### Key Mechanical Details

- **Sort before use:** `sortknives()` at `edit.c:107` reorders cuts into ascending order regardless of input order, so misordered inputs are silently normalized. Cut ordering is NOT a precondition. [PRE-REARRANGE, Finding 0056]
- **Offset computation:** `makeoffsetsfor3or4cuts()` at `edit.c:164-184` computes a displacement vector for each region purely from the cut-point differences. For pivot with cuts `c0 < c1 < c2`: `diff[1] = c2 - c1` (region 1 moves forward by the size of region 2), `diff[2] = -(c1 - c0)` (region 2 moves backward by the size of region 1).
- **Application:** `tumbleradd(&ptr->cdsp.dsas[index], &diff[i], ...)` is called per POOM entry — V-addresses are shifted in place, I-addresses are never touched. [ST-REARRANGE, Finding 0056]
- **Cut domain:** All cuts are specified in the **pre-move** V-address space. [PRE-REARRANGE, Finding 0056]

### What It Is NOT

It is not a source-span + target-position cut-paste. There is no "destination" argument — the operation is a pure permutation within the existing V-space, defined entirely by the cut geometry. Content is never copied or moved to a new I-address; only V-address displacements change. [INV-REARRANGE-IDENTITY]

### Missing Precondition

REARRANGE does not validate that cuts stay within a single subspace. Cuts spanning the text/link boundary (e.g., `[1.1, 1.4, 2.5]`) cause content to shift from the text subspace (`1.x`) into the link subspace (`2.x`), violating the subspace convention with no error. [PRE-REARRANGE, Finding 0051; EC-REARRANGE-CROSS-SUBSPACE]

---

## Code Exploration

---

## The `rearrange` Operation in udanax-green

### TL;DR

`rearrange` takes a **document address** plus a **sequence of 3 or 4 tumbler cut positions** in V-space. It is not a (source-span, target-position) cut-paste, and it is not a named two-span swap. It is a **cut-sequence** operation: the cuts divide V-space into zones, and each zone's crums are displaced by a computed offset. 3 cuts → rotation; 4 cuts → swap of two non-adjacent spans.

---

### Call Chain

```
FEBE wire (request code 3)
  → rearrange()          fns.c:159
      → getrearrange()   get1.c:94 / get1fe.c:65   (parse wire)
      → dorearrange()    do1.c:34                   (open doc, dispatch)
          → rearrangepm() orglinks.c:137             (POOM wrapper)
              → rearrangend()  edit.c:78             (enfilade core)
```

---

### FEBE Entry Point

```c
// fns.c:159
void rearrange(typetask *taskptr)
{
  typeisa docisa;
  typecutseq cutseq;
  bool getrearrange(), dorearrange();

    (void) getrearrange (taskptr, &docisa, &cutseq);
    putrearrange (taskptr);
    if (!dorearrange (taskptr, &docisa, &cutseq))
        fprintf(stderr,"rearrange failed \n");
}
```

The request opcode is `REARRANGE = 3` [`requests.h:24`].

---

### Wire Parameters

`getrearrange` reads two things from the connection [`get1.c:94–103`]:

1. **Document ISA** — a tumbler identifying which document to operate on
2. **Cut sequence** — a `typecutseq` struct, read by `getcutseq()`

The `getcutseq` loop [`get2.c:278–298`] prompts:
```
"any cuts?"    → bool
"cut address=>" → tumbler (V-address)
```
…repeatedly until `anycuts == FALSE` or the limit is reached. Each cut is a bare **tumbler position** in V-space — not a span, not a (start, width) pair.

---

### `typecutseq` Structure

```c
// common.h:108–113
#define MAXCUTS  4

typedef struct structcutseq {
    INT numberofcuts;
    tumbler cutsarray[MAXCUTS];   // 3 or 4 tumbler positions
} typecutseq;
```

Maximum 4 cuts. The array holds raw tumbler **positions** (not widths).

---

### Internal Entry Point: `rearrangend`

```c
// edit.c:78
int rearrangend(typecuc *fullcrumptr, typecutseq *cutseqptr, INT index)
```

| Parameter | Type | Meaning |
|-----------|------|---------|
| `fullcrumptr` | `typecuc *` | Root node of the document's POOM enfilade |
| `cutseqptr` | `typecutseq *` | The 3 or 4 cut positions |
| `index` | `INT` | Dimension — always `V` (the virtual address dimension) |

The dimension is hardwired to `V` at every call site [`orglinks.c:139`]:
```c
rearrangend((typecuc*)docorgl, cutseqptr, V);
```

---

### What `rearrangend` Does Internally

It converts `typecutseq` into a `typeknives` struct [`ndenf.h:12–16`], sorts the blades, then calls `makeoffsetsfor3or4cuts` to compute per-zone displacement vectors:

```c
// edit.c:164
int makeoffsetsfor3or4cuts(typeknives *knives, tumbler diff[])
```

#### 3-cut case [`edit.c:177–181`] — **Rotation / Move**

Cuts at positions A < B < C divide V-space into four zones (0, 1, 2, 3):

```c
diff[1] = blades[2] - blades[1]   // zone 1: [A,B] shifts forward by (C−B)
diff[2] = -(blades[1] - blades[0]) // zone 2: [B,C] shifts backward by (B−A)
diff[3] = 0                        // zone 3: after C, stays put
```

Effect: content in `[A,B]` moves to `[C−(B−A), C]`; content in `[B,C]` moves to `[A, A+(C−B)]`. The range `[A,C]` is rotated so that `[B,C]` leads and `[A,B]` follows — a classic cut-paste move expressed as three cut points.

#### 4-cut case [`edit.c:169–176`] — **Two-Span Swap**

Cuts at positions A < B < C < D:

```c
diff[1] = blades[2] - blades[0]         // zone 1: [A,B] → shifts forward by (C−A)
diff[2] = (blades[3]-blades[2]) - (blades[1]-blades[0])  // zone 2: gap adjusts
diff[3] = -(blades[2] - blades[0])      // zone 3: [C,D] → shifts backward by (C−A)
```

Effect: `[A,B]` and `[C,D]` swap positions. If they have different widths, the gap `[B,C]` expands or contracts by `(D−C)−(B−A)` to compensate.

---

### Zone Classification

`rearrangecutsectionnd` [`edit.c:191–204`] classifies each crum by which zone it occupies — returning 0, 1, 2, 3, or −1 (straddles a cut, which is an error). Each crum in zone `i` has `diff[i]` added to its V-address [`edit.c:125`]:

```c
tumbleradd (&ptr->cdsp.dsas[index], &diff[i], &ptr->cdsp.dsas[index]);
```

Zone 0 (before the first cut) and zone 4 are handled by the `case 0: case 4:` branch — they never move [`edit.c:122`].

---

### Summary

| Question | Answer |
|----------|--------|
| Is it (source-span, target-position)? | No — no widths, no target positions |
| Is it two named spans to swap? | No — no span structs |
| What is it? | A sequence of 3 or 4 raw tumbler **cut positions** in V-space |
| 3 cuts → | Rotation: `[B,C]` moves before `[A,B]` within range `[A,C]` |
| 4 cuts → | Swap: non-adjacent spans `[A,B]` and `[C,D]` exchange positions |
| FEBE signature | `void rearrange(typetask *taskptr)` [`fns.c:159`] |
| Internal signature | `int rearrangend(typecuc *fullcrumptr, typecutseq *cutseqptr, INT index)` [`edit.c:78`] |
| `index` always | `V` (virtual address dimension) [`orglinks.c:139`] |
| Max cuts | 4 (`MAXCUTS` [`common.h:108`]) |
| Min cuts | 3 (implied by `makeoffsetsfor3or4cuts` which `gerror`s otherwise [`edit.c:183`]) |
