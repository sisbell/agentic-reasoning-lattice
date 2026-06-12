## Question 13 [evidence]

> For a fork of a fork (CREATENEWVERSION applied to `docISA.0.1`), is the grandchild allocated as `docISA.0.1.0.1` — encoding the full ancestry chain in the tumbler mantissa — and does this consume mantissa digits toward the `NPLACES=16` limit, bounding fork depth?

## KB Synthesis

## Fork-of-Fork Address Structure and Depth Bound

The KB gives a clear answer by synthesizing three entries.

### Address format: `.1`, not `.0.1`

Per [SS-VERSION-ADDRESS] Finding 0068, `docreatenewversion` selects the allocation hint with `makehint(DOCUMENT, DOCUMENT, depth=1)`. Depth=1 means the allocation crosses **no** `.0.` boundary — it simply appends one digit to the current address. The KB confirms this with a concrete example:

```
1.1.0.1.0.1          (doc)
└── 1.1.0.1.0.1.1    (v1 = VERSION(doc))
    └── 1.1.0.1.0.1.1.1  (v2 = VERSION(v1))
```

So if `docISA.0.1` is the first version, the grandchild is **`docISA.0.1.1`**, not `docISA.0.1.0.1`. The `.0.` separator only appears at ACCOUNT→DOCUMENT transitions (depth=2 per [SS-ADDRESS-SPACE] Finding 0021); DOCUMENT→DOCUMENT transitions use depth=1 and produce a bare appended digit.

### Digit consumption per fork level

From [SS-TUMBLER] Finding 0031, tumblers are stored as a fixed-length mantissa of `NPLACES=16` digits, with `tumblerlength(t) = nstories(t) - t.exp` counting significant digits. For the address `1.1.0.1.0.1` the mantissa is `[1,1,0,1,0,1,0,...,0]` with `tumblerlength = 6`. Each VERSION call appends one digit, advancing `tumblerlength` by one:

| depth | address | tumblerlength |
|-------|---------|---------------|
| base  | `1.1.0.1.0.1` | 6 |
| 1     | `1.1.0.1.0.1.1` | 7 |
| 2     | `1.1.0.1.0.1.1.1` | 8 |
| …     | … | … |
| 10    | `1.1.0.1.0.1.1.1.1.1.1.1.1.1.1.1` | 16 |

### Depth is bounded by NPLACES=16

Yes. Because each fork appends one mantissa digit ([SS-ADDRESS-SPACE] Finding 0068: "the address simply grows by one component per version level"), and the mantissa is capped at 16 positions ([SS-TUMBLER] Finding 0031), fork depth from a base address of length N is bounded at **16 − N**. For the typical 6-digit account/document structure, the maximum fork depth is **10 levels**.

One tension to note: [SS-ADDRESS-SPACE] Finding 0068 states "The depth of version nesting is unlimited," but this appears to be a design-intent claim that does not account for the NPLACES physical ceiling. The allocation code (`findisatoinsertnonmolecule`, `tumblerincrement`) does not enforce a depth guard, so overflow into a 17th digit would silently corrupt the tumbler representation — the KB contains no evidence of a soft failure or error for this case.

---

## Code Exploration

I have all the evidence I need. Here is the complete answer.

---

## Fork-of-Fork Address Allocation in udanax-green

### Short Answer

**No.** The grandchild is **not** allocated as `docISA.0.1.0.1`. Versioning one's own document appends a **single mantissa digit** with no zero separator. The fork of `docISA.0.1` is `docISA.0.1.1`, and the fork of that is `docISA.0.1.1.1`. Each fork depth consumes exactly one of the 16 mantissa slots, bounding fork depth to `NPLACES − len(address)`.

---

### Tracing the Allocation Path

#### Step 1 — `docreatenewversion` selects the hint type

`do1.c:260–277`:

```c
bool docreatenewversion(typetask *taskptr, typeisa *isaptr, typeisa *wheretoputit, typeisa *newisaptr)
{
    if (tumbleraccounteq(isaptr, wheretoputit) && isthisusersdocument(isaptr)) {
        makehint (DOCUMENT, DOCUMENT, 0, isaptr, &hint);   // [do1.c:271]
    } else {
        makehint (ACCOUNT, DOCUMENT, 0, wheretoputit, &hint);   // [do1.c:275]
    }
    ...
    createorglingranf(taskptr, granf, &hint, newisaptr);   // [do1.c:277]
```

`isthisusersdocument` [`be.c:171`] checks `tumbleraccounteq(tp, &taskptrx->account)`. For a user forking their own document, the **first branch fires**: the hint carries `supertype = DOCUMENT (3)`, `subtype = DOCUMENT (3)`, `hintisa = docISA`.

#### Step 2 — `findisatoinsertgr` dispatches on `ATOM` vs non-`ATOM`

`granf2.c:130–156`:

```c
bool findisatoinsertgr(typecuc *fullcrumptr, typehint *hintptr, typeisa *isaptr)
{
    if (hintptr->subtype == ATOM) {
        findisatoinsertmolecule(...);   // text/link atoms
    } else {
        findisatoinsertnonmolecule(...);  // [granf2.c:152]  ← hit here
    }
    tumblerjustify(isaptr);
    return (TRUE);
```

Versioning is `subtype = DOCUMENT`, not `ATOM`, so `findisatoinsertnonmolecule` runs.

#### Step 3 — `findisatoinsertnonmolecule` computes `depth`

`granf2.c:203–242`:

```c
static int findisatoinsertnonmolecule(...)
{
    depth = hintptr->supertype == hintptr->subtype ? 1 : 2;   // [granf2.c:209]
    hintlength = tumblerlength(&hintptr->hintisa);
    tumblerincrement(&hintptr->hintisa, depth - 1, 1, &upperbound);
    ...
```

- `ACCOUNT → DOCUMENT`: ACCOUNT(2) ≠ DOCUMENT(3) → **depth = 2** → `tumblerincrement(hintisa, 1, 1, upperbound)`, then first allocation: `tumblerincrement(hintisa, 2, 1, isaptr)`. The `+2` skips position `idx+1` (left as zero = separator) and writes at `idx+2`. **This is why documents under accounts get `.0.N`.**

- `DOCUMENT → DOCUMENT`: DOCUMENT(3) = DOCUMENT(3) → **depth = 1** → `tumblerincrement(hintisa, 0, 1, upperbound)`, then first allocation: `tumblerincrement(hintisa, 1, 1, isaptr)`. The `+1` writes directly at `idx+1`. **No zero separator is inserted.**

#### Step 4 — `tumblerincrement` mechanics

`tumble.c:599–623`:

```c
int tumblerincrement(tumbler *aptr, INT rightshift, INT bint, tumbler *cptr)
{
    for (idx = NPLACES ; aptr->mantissa[--idx] == 0 && idx > 0;);
    if (idx + rightshift >= NPLACES) {
        gerror ("tumblerincrement overflow\n");    // [tumble.c:616]
    }
    cptr->mantissa[idx + rightshift] += bint;
    tumblerjustify(cptr);
```

`idx` is the index of the last non-zero mantissa digit. `rightshift = depth` determines how far past that index the new digit is written. For versioning (`depth = 1`), the new digit goes at `idx + 1` — one place beyond the parent's last digit, with no zero in between.

---

### Concrete Trace

The golden test at `golden/versions/version_address_allocation.json` records the actual allocations:

| Operation | Result address |
|-----------|---------------|
| `create_document` (doc1) | `1.1.0.1.0.1` |
| `create_version` from doc1 | `1.1.0.1.0.1.1` |
| `create_version` from doc1 again | `1.1.0.1.0.1.2` |
| `create_version` from version1 | `1.1.0.1.0.1.1.1` |

And `golden/versions/version_chain.json` (v1 → v2 → v3):

| | Address |
|-|---------|
| v1 | `1.1.0.1.0.1` |
| v2 (fork of v1) | `1.1.0.1.0.1.1` |
| v3 (fork of v2) | `1.1.0.1.0.1.1.1` |

The mantissa for `1.1.0.1.0.1` is `[1,1,0,1,0,1, 0,0,0,0,0,0,0,0,0,0]` (last non-zero at index 5).

Version appends at index 6: `[1,1,0,1,0,1,1, 0,…]`.

Fork of that appends at index 7: `[1,1,0,1,0,1,1,1, 0,…]`.

**No zero separator is ever inserted between fork levels.**

---

### Why the `.0.N` Pattern Appears Only at Document Creation

`common.h:53`:
```c
#define NPLACES 16   /* places in mantissa of tumbler - increased from 11 to support deeper version chains */
```

The `.0.N` pattern is produced by `depth = 2`, which is used for:
- `ACCOUNT → DOCUMENT` (new document under account) — `do1.c:239`
- `NODE → NODE` — `do1.c:251`
- Cross-account new-version — `do1.c:275`

When depth = 2, `tumblerincrement(hintisa, 2, 1, isaptr)` writes at `idx+2`, naturally leaving `idx+1` as zero (separator). This is what produces the `.0.1` in `1.1.0.1` (account `1.1` → first document skips one slot → zero at position 2, digit at position 3).

Versioning one's own document uses `depth = 1`: writes at `idx+1`, no zero separator. The structure `1.1.0.1.0.1` ends with `.0.1` not because versioning made it so, but because document creation did.

---

### NPLACES=16 Bounds Fork Depth

The original implementation used `NPLACES = 11`. The comment explicitly states it was **"increased from 11 to support deeper version chains."**

For a base document like `1.1.0.1.0.1` (6 mantissa slots occupied, last non-zero at `idx = 5`):

| Fork depth | Last non-zero idx | Needed slot for next fork | In bounds? |
|------------|-------------------|--------------------------|------------|
| 0 (root)   | 5                 | 6                        | ✓ (6 < 16) |
| 1          | 6                 | 7                        | ✓ |
| …          | …                 | …                        | … |
| 10         | 15                | 16                       | ✗ **overflow** |

At fork depth 10, `idx = 15` and `idx + rightshift = 16 >= NPLACES = 16` → `gerror("tumblerincrement overflow\n")` [`tumble.c:616`].

**Maximum fork depth = `NPLACES − len(base_address) − 1` = `16 − 6 − 1 = 9` additional fork levels** from a 6-digit document. A document with a longer base address (e.g., a 7-digit address under a more deeply nested account) has one fewer fork level available.

---

### Summary

1. **The grandchild is `docISA.0.1.1`, not `docISA.0.1.0.1`.** Version children never get a zero separator — that separator only appears when `depth = 2` (document-under-account). Versioning own document always uses `depth = 1` [`granf2.c:209`], appending a single digit directly.

2. **Each fork depth consumes exactly one mantissa digit**, not two. The ancestry chain is encoded as a flat sequence of non-zero digits after the document's base address (e.g., `1.1.0.1.0.1.1.1.1` for three forks deep).

3. **`NPLACES = 16` hard-bounds fork depth.** The overflow guard at `tumble.c:612–616` calls `gerror` when `idx + rightshift >= 16`. For a standard 6-digit document, this means **10 fork levels maximum**. The comment in `common.h:53` confirms this limit was already once extended (from 11 to 16) to accommodate deeper chains.
