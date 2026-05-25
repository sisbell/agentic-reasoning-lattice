## Question 14 [evidence]

> If a span's I-addresses fall under the parent tumbler `1.1.0.1.0.5.0.1.x`, is the origin document always reliably `1.1.0.1.0.5` by tumbler-prefix decomposition, or can fragmented allocation break this assumption?

## KB Synthesis

## Short Answer

Yes, the prefix decomposition is reliable in the fixed implementation, but fragmented allocation warrants a nuance.

## Why the Prefix Is Reliable

Allocation for a document's content I-addresses is bounded by an upper bound derived directly from `docISA`. From [SS-ADDRESS-ALLOC] Finding 0065:

> `upperbound` is set to `docISA.2.3` (for links) — bounding search to the document's link subspace. `findpreviousisagr` finds the highest existing I-address below that bound.

The same `findisatoinsertmolecule` mechanism applies to text atoms with an analogous bound. The result: every allocation for document `1.1.0.1.0.5` searches only within that document's namespace.

The containment check ([SS-TUMBLER-CONTAINMENT]) reinforces this: after `findpreviousisagr` locates a candidate address, the implementation verifies it actually falls under the parent prefix via tumbler truncation-and-comparison. This fix addressed Bug 0013, which had allowed allocation to cross account boundaries ([PRE-ADDRESS-ALLOC]):

> Before fix: allocating under `1.1.0.2` found `1.1.0.1.0.1`, incremented to `1.1.0.1.0.2` (under the wrong account).

## What Fragmented Allocation Does — And Doesn't — Break

[ST-CRUM-BOUND] Finding 0063 and [INV-MONOTONIC] Finding 0063 confirm that interleaved CREATELINK operations create **gaps** in the text I-address sequence within a document. After `INSERT "ABC"` → `CREATELINK` → `INSERT "DEF"`, the text I-addresses for "ABC" and "DEF" are non-contiguous because the link orgl consumed I-space between them.

Critically, this fragmentation stays within `1.1.0.1.0.5.0.x.y` — the gaps appear inside the prefix, not outside it. From [FC-GRANF-ON-DELETE] Finding 0061:

> The allocation function can be modeled as a pure function of the granfilade state: `next_iaddr(granf) = max_iaddr(granf) + 1`. No hidden session state participates.

So `findpreviousisagr` returns the maximum I-address within the bounded range, and the new allocation increments from there — always remaining under the document's prefix.

## The One Caveat

From [INV-MONOTONIC] Finding 0077:

> The formal model should NOT use a single `Σ.next` counter. Instead, allocation is a family of independent functions partitioned by tumbler range.

This means the guarantee holds **per allocation subspace**. Element field `1` (as in `1.1.0.1.0.5.0.1.x`) is not documented in the KB as a recognized atom type (field 2 = links, field 3 = text per [SS-ADDRESS-ALLOC] Finding 0065). If `1.1.0.1.0.5.0.1.x` addresses exist, they were allocated within the correct document range, but their semantic type is not defined in the known allocation vocabulary — the prefix attribution to document `1.1.0.1.0.5` is structurally correct, but what those addresses represent is unspecified.

**Summary**: Fragmented allocation creates non-contiguous numbering within a document's prefix but cannot produce I-addresses belonging to one document under another document's prefix — provided the Bug 0013 containment fix is in place [PRE-ADDRESS-ALLOC], [SS-TUMBLER-CONTAINMENT], [INV-ACCOUNT-ISOLATION].

---

## Code Exploration

I now have all the source evidence needed. Here is my complete answer.

---

## Answer: Tumbler Prefix Decomposition and Document Origin Reliability

### Short Answer

The assumption **is reliable in practice**, but it is **not maintained by prefix decomposition alone**. It is maintained by a structural invariant plus two explicit guards layered into the allocation code. Fragmented allocation cannot break it under normal operation, but there is a subtle reason why — one that is not obvious from the tumbler arithmetic alone.

---

### The Tumbler Data Structure

**`backend/common.h:59-65`**
```c
typedef struct structtumbler {
    humber xvartumbler;
    char varandnotfixed;
    char sign  BIT ;
    short exp;
    tdigit mantissa[NPLACES];   /* NPLACES = 16 */
} tumbler;
```

A tumbler is a fixed-width positional number. The `exp` field shifts the mantissa left (negative = leading zeros). There is **no explicit "document prefix" field** — document identity is encoded purely by depth and value in the mantissa. `typeisa` is a typedef alias for `tumbler` (`backend/xanadu.h:23`).

`tumblerlength` returns the conceptual "depth" of a tumbler:

**`backend/tumble.c:259-262`**
```c
INT tumblerlength(tumbler *tumblerptr)
{
    return (nstories (tumblerptr) - tumblerptr->exp);
}
```

`tumblertruncate` zero-fills all positions beyond depth `bint`, extracting the first-N-stories prefix:

**`backend/tumble.c:625-639`**
```c
int tumblertruncate(tumbler *aptr, INT bint, tumbler *cptr)
{
  tumbler answer;
  INT i;
    movetumbler (aptr, &answer);
    for  (i = answer.exp; i < 0 && bint > 0; ++i, --bint);
    if (bint <= 0)
        tumblerclear (&answer);
      else
        for (; bint < NPLACES; ++bint)
            answer.mantissa[bint] = 0;
    tumblerjustify (&answer);
    movetumbler (&answer, cptr);
}
```

---

### How Text I-Addresses Are Allocated

The allocation path for text insertion is:

`doinsert` → `inserttextgr` → `findisatoinsertgr` → `findisatoinsertmolecule`

**`backend/granf2.c:83-109`** — `inserttextgr`:
```c
if (!findisatoinsertgr ((typecuc*)fullcrumptr, hintptr, &lsa))   /* line 92 */
    return (FALSE);
movetumbler (&lsa, &spanorigin);                                   /* line 94 */
for (; textset; textset = textset->next) {
    ...
    insertseq ((typecuc*)fullcrumptr, &lsa, &locinfo);
    tumblerincrement (&lsa, 0, textset->length, &lsa);             /* line 100 */
}
ispanptr->stream = spanorigin;
tumblersub (&lsa, &spanorigin, &ispanptr->width);                  /* line 106 */
```

One starting address (`spanorigin`) is allocated at line 92. All subsequent chunks in the same call are placed contiguously by incrementing `lsa` at rightshift=0 (deepest digit). The returned ispan covers `[spanorigin, spanorigin+totalwidth)` — entirely within one document's address space, assuming the starting allocation was correct.

---

### The Allocation Logic for Molecules (Text/Link Atoms)

`findisatoinsertgr` dispatches by hint type:

**`backend/granf2.c:130-156`**:
```c
if (hintptr->subtype == ATOM) {
    if (!isaexistsgr (fullcrumptr, &hintptr->hintisa)) {   /* line 136 */
        return (FALSE);
    }
    findisatoinsertmolecule (fullcrumptr, hintptr, isaptr);
} else {
    findisatoinsertnonmolecule (fullcrumptr, hintptr, isaptr);
}
```

**Guard 1** (`line 136`): Text cannot be inserted unless the document's ORGL entry already exists in the granfilade at exactly `hintisa`. This is the prerequisite that makes the rest work.

**`backend/granf2.c:158-181`** — `findisatoinsertmolecule` (`TEXTATOM = 1`, from `backend/xanadu.h:145`):
```c
tumblerincrement (&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound);  /* line 162 */
clear (&lowerbound, sizeof(lowerbound));
findpreviousisagr ((typecorecrum*)fullcrumptr, &upperbound, &lowerbound);
if (tumblerlength (&hintptr->hintisa) == tumblerlength (&lowerbound)) {       /* line 165 */
    tumblerincrement (&lowerbound, 2, hintptr->atomtype, isaptr);              /* line 166 */
    tumblerincrement (isaptr, 1, 1, isaptr);                                   /* line 167 */
} else if (hintptr->atomtype == TEXTATOM) {
    tumblerincrement (&lowerbound, 0, 1, isaptr);                              /* line 169 */
}
```

**Step-by-step for document `1.1.0.1.0.5`, `TEXTATOM=1`:**

`tumblerincrement` at line 162 with rightshift=2, bint=`TEXTATOM+1`=2:
- `idx` = last non-zero mantissa position of `1.1.0.1.0.5` = position 5 (`5` is the last nonzero digit)
- Adds 2 at mantissa[7]: `upperbound = 1.1.0.1.0.5.0.2`

`findpreviousisagr` (`backend/granf2.c:255-278`) then searches the enfilade for the largest ISA **strictly less than `1.1.0.1.0.5.0.2`**. It has no document-boundary awareness of its own.

---

### The Structural Invariant That Prevents Cross-Document Allocation

The correctness of `findisatoinsertmolecule` rests on a **structural invariant**: the granfilade always contains the document's ORGL entry at exactly `hintisa` (enforced by Guard 1 at line 136).

**Case 1 — First text insertion into document:**
- The granfilade contains the ORGL entry at `1.1.0.1.0.5`
- `1.1.0.1.0.5 < 1.1.0.1.0.5.0.2`, so `findpreviousisagr` returns `lowerbound = 1.1.0.1.0.5`
- `tumblerlength(lowerbound) == tumblerlength(hintisa)` → `True` (both depth 6)
- Line 166: `tumblerincrement(&1.1.0.1.0.5, 2, 1, isaptr)` → idx=5, mantissa[7]+=1 → `1.1.0.1.0.5.0.1`
- Line 167: `tumblerincrement(&1.1.0.1.0.5.0.1, 1, 1, isaptr)` → idx=7, mantissa[8]+=1 → **`1.1.0.1.0.5.0.1.1` ✓**

**Case 2 — Subsequent text insertion (existing text at `1.1.0.1.0.5.0.1.N`):**
- `findpreviousisagr` returns `lowerbound = 1.1.0.1.0.5.0.1.N` (deepest entry < `1.1.0.1.0.5.0.2`)
- `tumblerlength(lowerbound) = 9 ≠ 6` → TEXTATOM branch
- Line 169: `tumblerincrement(&1.1.0.1.0.5.0.1.N, 0, 1, isaptr)` → **`1.1.0.1.0.5.0.1.N+1` ✓**

**The key**: because the document ORGL entry is at `hintisa`, and `hintisa < hintisa.0.2 ≤ nextdocument`, the lowerbound returned by `findpreviousisagr` is **always ≥ `hintisa`** and **always within** `[hintisa, hintisa.0.2)`. Every address in that interval correctly carries the prefix `1.1.0.1.0.5`.

Unlike `findisatoinsertnonmolecule`, `findisatoinsertmolecule` does **not** perform an explicit `tumblertruncate` + `tumblereq` prefix check. It doesn't need one because the ORGL sentinel does the work structurally.

---

### The Explicit Guard for Non-Atom (Document/Account) Allocation

For completeness: `findisatoinsertnonmolecule` does need an explicit check because there is no structural floor analogous to the ORGL sentinel. The guard is:

**`backend/granf2.c:228-241`**:
```c
lowerbound_under_hint = FALSE;
if (!iszerotumbler(&lowerbound)) {
    tumblertruncate(&lowerbound, hintlength, &truncated);          /* truncate to document depth */
    lowerbound_under_hint = tumblereq(&truncated, &hintptr->hintisa);
}

if (iszerotumbler(&lowerbound) || !lowerbound_under_hint) {
    tumblerincrement(&hintptr->hintisa, depth, 1, isaptr);         /* start fresh */
} else {
    tumblertruncate (&lowerbound, hintlength + depth, isaptr);
    tumblerincrement(isaptr, tumblerlength(isaptr)==hintlength?depth:0, 1, isaptr);
}
```

This is **BUG FIX #2** (noted in the comment). `findpreviousisagr` can return an ISA from a different account (e.g., it finds `1.1.0.1.0.1.x` when trying to allocate under `1.1.0.2`). The truncate-and-compare rejects it and starts fresh at `hintisa.0.1`.

---

### Can Fragmented Allocation Break the Assumption?

**No.** Fragmented allocation means the text atoms for a document have gaps: e.g., `1.1.0.1.0.5.0.1.1`–`1.1.0.1.0.5.0.1.50`, gap, `1.1.0.1.0.5.0.1.100`–`1.1.0.1.0.5.0.1.150`. The next allocation will land at `1.1.0.1.0.5.0.1.151` because `findpreviousisagr` finds `.0.1.150` as the largest existing ISA below the `1.1.0.1.0.5.0.2` bound.

Every fragment, however sparse, remains under `1.1.0.1.0.5.0.1.x` because:
1. The starting address was bounded by the ORGL sentinel
2. Subsequent addresses are derived by rightshift=0 increment from the previous endpoint
3. The upperbound `1.1.0.1.0.5.0.2` is never crossed

**The one failure mode**: if the ORGL entry at `1.1.0.1.0.5` were absent or corrupted in the granfilade, `findpreviousisagr` could return an ISA from the previous document's text space, placing new text at `prevdoc.0.1.M+1` — in the wrong document's namespace. The check at `granf2.c:136` (`isaexistsgr`) is the gate preventing this, but it is the single load-bearing invariant.

---

### Summary

| Mechanism | Location | Purpose |
|-----------|----------|---------|
| Document existence check | `granf2.c:136` | Cannot insert text without a document ORGL entry |
| ORGL sentinel as floor | Structural: ORGL at `hintisa` | Ensures `findpreviousisagr` returns `>= hintisa` |
| Upperbound `hintisa.0.2` | `granf2.c:162` | Restricts search to document's content space |
| Sequential increment | `granf2.c:100` | Keeps multi-chunk inserts contiguous within document |
| Explicit prefix guard (non-atom) | `granf2.c:228-233` | Rejects stray lowerbound from adjacent account |

The answer to the question: **The origin document `1.1.0.1.0.5` is reliably derivable from the prefix `1.1.0.1.0.5.0.1.x`**, but the system does not derive it by decomposition at query time. The invariant is enforced at **allocation time** through the structural fact that each document's ORGL entry pre-occupies `hintisa` in the granfilade, acting as a floor that bounds all content searches within the correct document's namespace.
