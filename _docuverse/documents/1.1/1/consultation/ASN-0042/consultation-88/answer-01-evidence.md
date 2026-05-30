## Question 1 [evidence]

> Is every modification to the granfilade/baptismal registry routed through the `Bop` baptism procedure, or are there allocation/delegation write paths that bypass it?

## KB Synthesis

The KB contains no mention of a "Bop" procedure, "baptism" procedure, or "baptismal registry." This terminology does not appear in any KB entry.

The granfilade write paths documented in the KB route through these mechanisms:

- **Text content**: `doinsert` → `inserttextingranf` → `findisatoinsertmolecule` [SS-ADDRESS-SPACE, ST-INSERT]
- **Document address allocation**: `createorglingranf` → `findisatoinsertnonmolecule` [ST-ADDRESS-ALLOC, SS-ADDRESS-ALLOC]
- **Link orgls**: `docreatelink` → `createorglingranf` [ST-CREATE-LINK]
- **Version allocation**: `docreatenewversion` → `createorglingranf` [ST-VERSION]
- **COPY**: `docopy` → `insertpm` + `insertspanf` [ST-VCOPY, SS-DOCISPAN]

All allocation paths are stateless query-and-increment on the granfilade tree via `findpreviousisagr` + `tumblerincrement` [SS-ADDRESS-SPACE Finding 0061, 0077]. There is no documented baptism layer in the KB.

If "Bop" or "baptismal registry" is a concept from the udanax-green source code or design documents, it is not captured in the current knowledge base — I cannot answer this question from the KB alone.

---

## Code Exploration

Now I have everything I need for a complete answer.

---

## Finding: No `Bop` Function Exists — Granfilade Write Paths Are Strictly Funneled

### Preliminary Finding: `Bop` Does Not Exist in the C Source

The function name `Bop` appears **nowhere** in the udanax-green C codebase — not in any `.c` file, not in any `.h` file. The "baptism procedure" terminology comes from Xanadu design literature but was never implemented under that name in the C code. What exists instead is a two-layer write funnel.

---

### The Granfilade Write Architecture

The **only** function that physically writes entries into the granfilade is:

```c
int insertseq(typecuc *fullcrumptr, tumbler *address, typegranbottomcruminfo *info)
// insert.c:17
```

`insertseq` is called in **exactly two places**, both in `granf2.c`:

- `granf2.c:99` — inside `inserttextgr()`, to commit a GRANTEXT leaf
- `granf2.c:125` — inside `createorglgr()`, to commit a GRANORGL leaf

No other call sites exist. Every granfilade write in the entire system flows through one of these two functions.

---

### ISA Allocation — The Actual "Baptism"

Before either write, the new ISA (tumbler address) must be allocated. Both `inserttextgr()` and `createorglgr()` begin by calling:

```c
bool findisatoinsertgr(typecuc *fullcrumptr, typehint *hintptr, typeisa *isaptr)
// granf2.c:130
```

This is the sole ISA allocator — the closest thing in the code to a "baptism" procedure. It dispatches based on `hintptr->subtype`:

- **`ATOM` subtype** → `findisatoinsertmolecule()` [granf2.c:158]  
  Computes the new ISA by calling `tumblerincrement()` against `lowerbound` [granf2.c:166–175], finding the next available address within the parent document's atom space.

- **Non-ATOM subtype** (DOCUMENT, ACCOUNT, NODE) → `findisatoinsertnonmolecule()` [granf2.c:203]  
  Calls `tumblertruncate()` + `tumblerincrement()` to produce a child address under `hintptr->hintisa` [granf2.c:237–240].

There is also a dead function `klugefindisatoinsertnonmolecule()` [granf2.c:183] which just calls `tumblercopy(&hintptr->hintisa, isaptr)` — but it is **entirely commented out** inside `#ifdef UnDeFIned` / `#endif` [granf2.c:196–199] and is **never called** from `findisatoinsertgr`. It represents an old, broken allocation path that was preserved in source but abandoned.

---

### Complete Call Graph: All Paths to `insertseq`

```
ATOM (text) path:
  doinsert() [do1.c:118]
    → inserttextingranf() [granf1.c:44]
      → inserttextgr() [granf2.c:83]
          → findisatoinsertgr() [granf2.c:92]   ← ISA allocated here
          → insertseq() [granf2.c:99]            ← granfilade written here

ORGL (document/link/node) path:
  docreatenewdocument()       [do1.c:240]
  docreatelink()              [do1.c:209]
  domakelink()                [do1.c:182]
  docreatenewversion()        [do1.c:277]
  docreatenode_or_account()   [do1.c:252]
    → createorglingranf() [granf1.c:50]
      → createorglgr() [granf2.c:111]
          → findisatoinsertgr() [granf2.c:117]   ← ISA allocated here
          → insertseq() [granf2.c:125]            ← granfilade written here
```

**No other paths exist.** Every creation operation — text insertion, document creation, link creation, version creation, node/account creation — goes through `findisatoinsertgr()` before reaching `insertseq()`. There are no bypass paths to `insertseq` that skip ISA allocation.

---

### BERT (Access Control Registry) — Separate from the Granfilade

BERT (`berttable[]` in `bert.c:29`) is a distinct hash-table registry that tracks which connections have which documents open. It is **not** the granfilade. Its write paths are:

| Function | Location | Normal caller |
|---|---|---|
| `addtoopen()` | bert.c:128 | `doopen()` [bert.c:264–321] |
| `logbertmodified()` | bert.c:97 | `doopen()` indirectly; also `orglinks.c` |
| `removefromopen()` | bert.c:154 | `doclose()` [bert.c:325] |

**One intentional BERT bypass exists:** `docreatenewversion()` [do1.c:290–296] calls `addtoopen()` directly, skipping `doopen()`:

```c
/* Skip doopen ownership check - we just created this document so we own it.
   Add directly to bert table instead. */
addtoopen(newisaptr, user, TRUE, WRITEBERT);           // do1.c:292
docopyinternal(taskptr, newisaptr, &vspan.stream, &vspec);
logbertmodified(newisaptr, user);                       // do1.c:295
doclose(taskptr, newisaptr, user);
```

This is deliberate: the document was just created by `createorglingranf()` so ownership is guaranteed. The bypass skips `doopen()`'s ownership-check state machine but still registers correctly in BERT. This is a BERT bypass, not a granfilade bypass.

---

### Summary

| Question | Answer |
|---|---|
| Does a function named `Bop` exist? | **No** — not in any `.c` or `.h` file |
| Is there a single ISA allocation choke point? | **Yes** — `findisatoinsertgr()` [granf2.c:130] |
| Is there a single granfilade write primitive? | **Yes** — `insertseq()` [insert.c:17] |
| Can anything reach `insertseq()` without going through ISA allocation? | **No** — only two callers exist, both always call `findisatoinsertgr()` first |
| Are there BERT write bypasses? | **One** — `docreatenewversion()` [do1.c:292] calls `addtoopen()` directly, intentionally and with a comment explaining why |
| Dead/abandoned bypass code in granfilade? | **One** — `klugefindisatoinsertnonmolecule()` [granf2.c:183], fully dead under `#ifdef UnDeFIned` |

Every ISA baptism in the live code goes through `findisatoinsertgr()`. Every granfilade write goes through `insertseq()` via exactly two callers, both in `granf2.c`. No allocation or delegation write path bypasses this funnel.
