# Revision Consultation — ASN-0027

**Review:** review-2.md
**Date:** 2026-03-10 09:50

## Summary

3 REVISE items analyzed: 2 internal, 1 consulted (0 nelson, 1 gregory)

## Consultation Results

### Issue 2: A3 precondition specifies no operation parameters

**Category:** GREGORY
**Reason:** The ASN already cites Gregory's evidence about REARRANGE's mechanism (modifying V-displacements) but lacks the operation's input signature. The implementation determines whether REARRANGE takes a cut-and-paste spec `(d, p_from, k, p_to)`, a full permutation, or another form.

**Gregory question:** What parameters does the rearrange operation accept in udanax-green — does it take a source position, width, and destination position (cut-and-paste), or some other input form?

**Gregory's Answer:**

## KB Synthesis

The rearrange operation takes **a document and a set of cut positions (tumblers)** — not a source/width/destination triple.

## Parameter Form

REARRANGE (FEBE command 3) accepts:
- A target document
- Exactly **3 or 4 cut positions** (V-addresses), provided as a list

The backend validates cut count strictly: any other count (e.g., 2) aborts with "Wrong number of cuts" [PRE-REARRANGE, Finding 0006].

Cut positions are **pre-sorted** by the implementation via `sortknives()`, so the caller does not need to supply them in order [PRE-REARRANGE, Finding 0056].

## Two Modes

**Pivot (3 cuts: `cut0, cut1, cut2`)**

Swaps the two adjacent regions `[cut0, cut1)` and `[cut1, cut2)`:
- `diff[1] = cut2 - cut1` (region 1 moves forward by size of region 2)
- `diff[2] = -(cut1 - cut0)` (region 2 moves backward by size of region 1)

Result: `"ABCDE"` with cuts `1.2, 1.4, 1.6` → `"ADEBC"` [ST-REARRANGE, Finding 0016]

**Swap (4 cuts: `cut0, cut1, cut2, cut3`)**

Swaps two non-adjacent regions `[cut0, cut1)` and `[cut2, cut3)`, leaving the middle `[cut1, cut2)` in place:
- `diff[1] = cut2 - cut0` (region 1 moves to region 3's position)
- `diff[2] = (cut3 - cut2) - (cut1 - cut0)` (middle shifts by size difference)
- `diff[3] = -(cut2 - cut0)` (region 3 moves to region 1's position)

Result: `"ABCDEFGH"` with cuts `1.2, 1.4, 1.6, 1.8` → `"AFGDEBCH"` [ST-REARRANGE, Finding 0016]

## Key Implementation Detail

The offsets are computed from the cut-point positions alone via `makeoffsetsfor3or4cuts()`, then applied per-orgl via `tumbleradd` on V-dimension displacements. No I-addresses are touched — rearrange is a pure V-space permutation [ST-REARRANGE, Finding 0056].

All cut positions reference the **pre-move address space** [PRE-REARRANGE, Finding 0056]. The operation is called as e.g. `session.pivot(doc, cut1, cut2, cut3)` or `session.swap(doc, cut1, cut2, cut3, cut4)` at the FEBE client level.

---

## Code Exploration

---

## The `rearrange` Operation: Parameters and Semantics

### Short Answer

Rearrange does **not** take a source position, width, and destination. It takes a **sequence of 3 or 4 V-address cut points** that divide the document's virtual address space into segments, then transposes those segments in place.

---

### Wire Protocol

**FEBE opcode: `3`** [`backend/requests.h:24`]

```
REARRANGE ::= <opcode 3> <doc_tumbler> <ncuts> <cut1> <cut2> [<cut3>] [<cut4>]
```

The front-end `getrearrange()` reads exactly two things off the wire:
1. The **document ISA** (a tumbler identifying the target document)
2. A **cutseq** — a count followed by that many tumblers

[`backend/get1fe.c:65-73`]:
```c
bool getrearrange(typetask *taskptr, typeisa *docisaptr, typecutseq *cutseqptr)
{
    fprintf(interfaceinput, "%d~", REARRANGE);
    return (
       gettumbler (taskptr, docisaptr)
    && getcutseq (taskptr, cutseqptr));
}
```

[`backend/get2fe.c:224-241`]:
```c
bool getcutseq(typetask *taskptr, typecutseq *cutseqptr)
{
    if (!(getnumber(taskptr, &ncuts) && (ncuts == 3 || ncuts == 4)))
        return (FALSE);
    cutseqptr->numberofcuts = ncuts;
    for (i = 0; i < ncuts; ++i)
        if (!gettumbler(taskptr, &cutseqptr->cutsarray[i]))
            return (FALSE);
    return (TRUE);
}
```

**`ncuts` must be exactly 3 or 4.** Any other value returns `FALSE` immediately.

The `typecutseq` struct [`backend/common.h:110-113`]:
```c
#define MAXCUTS 4
typedef struct structcutseq {
    INT numberofcuts;
    tumbler cutsarray[MAXCUTS];
} typecutseq;
```

---

### Two Forms

**3-cut form — called "pivot" in the client** [`febe/client.py:799-800`]:
```python
def pivot(self, docid, start, pivot, end):
    self.xc.command(3, docid, [start, pivot, end])
```
Specifies three V-address positions A < B < C. The document is sliced at those three points; the two **adjacent** middle segments [A,B) and [B,C) swap positions.

**4-cut form — called "swap" in the client** [`febe/client.py:802-803`]:
```python
def swap(self, docid, starta, enda, startb, endb):
    self.xc.command(3, docid, [starta, enda, startb, endb])
```
Specifies four V-address positions A < B < C < D. The two **non-adjacent** segments [A,B) and [C,D) swap; the middle segment [B,C) stays put.

---

### Execution Path

1. **`rearrange()`** [`fns.c:159-173`] — top-level FEBE handler; calls `getrearrange` then `dorearrange`
2. **`dorearrange()`** [`do1.c:34-43`] — finds the document's POOM (orgl), calls `rearrangepm()`
3. **`rearrangepm()`** [`orglinks.c:137-142`] — thin wrapper; calls `rearrangend(fullcrumptr, cutseqptr, V)` on the V-axis
4. **`rearrangend()`** [`edit.c:78-160`] — core logic

`rearrangend` at `edit.c:102-110`:
```c
knives.dimension = index;              // V-axis
knives.nblades = cutseqptr->numberofcuts;
for (i = 0; i < knives.nblades; i++)
    movetumbler(&cutseqptr->cutsarray[i], &knives.blades[i]);
sortknives(&knives);                   // ensures A < B < C [< D]
makeoffsetsfor3or4cuts(&knives, diff);
```

The cuts are **sorted** before use. The caller does not need to supply them in order.

---

### What the Offsets Compute

[`edit.c:164-184`], `makeoffsetsfor3or4cuts`:

For **3 cuts** [A, B, C] (after sort):
- Section 1 ([A,B)) gets `diff[1] = C − B` — moves right by the width of [B,C)
- Section 2 ([B,C)) gets `diff[2] = −(B − A)` — moves left by the width of [A,B)
- Section 3 ([C,∞)) stays: `diff[3] = 0`

Result: segments [A,B) and [B,C) swap. The V-span from [A,C) is reordered; nothing outside it moves.

For **4 cuts** [A, B, C, D]:
- Section 1 ([A,B)) gets `diff[1] = C − A`
- Section 2 ([B,C)) gets `diff[2] = (D−C) − (B−A)`
- Section 3 ([C,D)) gets `diff[3] = −(C−A)` (sign-flipped copy of diff[1])

Result: segments [A,B) and [C,D) swap. The interstitial [B,C) shifts by the net width difference between the two outer segments.

Each affected POOM crum has its V-axis displacement (`ptr->cdsp.dsas[V]`) shifted by the appropriate `diff[i]` [`edit.c:125-127`]:
```c
tumbleradd(&ptr->cdsp.dsas[index], &diff[i], &ptr->cdsp.dsas[index]);
ivemodified((typecorecrum*)ptr);
```

---

### Key Architectural Point

The content (I-addresses in the granfilade) **never moves**. Only the V→I mapping in the POOM is rearranged. This is why rearrange preserves content identity: after a pivot, the same I-addresses are present in the document; they are simply reachable via different V-addresses. The client scenario `pivot_preserves_identity` [`febe/scenarios/rearrange.py:254-293`] tests this directly.

The protocol documented in [`docs/febe-protocol.md:160-173`] confirms:
> `REARRANGE ::= <rearrangerequest> <doc id> <cut set>`
> - **3 cuts:** Regions cut1→cut2 and cut2→cut3 transpose
> - **4 cuts:** Regions cut1→cut2 and cut3→cut4 transpose
