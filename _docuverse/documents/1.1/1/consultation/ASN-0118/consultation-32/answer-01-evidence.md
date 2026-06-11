## Question 1 [evidence]

> When a spec's span has a depth (tumbler length) different from the V-position depth of the source's text subspace — e.g., a 3-component start over a depth-2 arrangement — does udanax-green's resolution path (specset2ispanset / acceptablevsa) accept it and resolve by intersection with bound positions, or does any check reject or normalize depth-mismatched spans?

## KB Synthesis

## Depth-Mismatched Span Resolution

The short answer: **no check rejects or normalizes depth-mismatched spans**. Every validation point on the path accepts them, and resolution proceeds by pure tumbler-arithmetic intersection with whatever POOM entries exist.

### Validation points — all pass-through

**`acceptablevsa()`** is the obvious candidate for rejecting a bad V-position, but the function in `do2.c:110-113` unconditionally returns `TRUE`. No subspace check, no tumbler-length check. [PRE-INSERT, Finding 0011; SS-SUBSPACE-CONVENTION, Finding 0010]

**`specset2sporglset()`** (the entry point for specset resolution) validates only that the referenced document exists in the granf. Element-level tumbler structure — including depth — is not inspected. A 3-component start over a 2-component arrangement is accepted as long as the document address resolves. [PRE-SPECSET, Finding 0001]

### Resolution path — pure tumbler arithmetic

After the document check passes, `specset2ispanset` calls `permute()` → `span2spanset()` → `retrieverestricted()`, which searches the POOM for content overlapping the query span. The search uses `whereoncrum()` / `intervalcmp()`, both of which are pure applications of the tumbler total order.

The total order is depth-agnostic. `abscmp` compares tumblers by exponent first, then lexicographically through mantissa digits. A 3-component `1.1.2` therefore sits strictly between `1.1` and `1.2` in the ordering, because after matching `1.1`, the shorter tumbler's implicit trailing zero is less than the continuation digit `2`. [INV-TUMBLER-TOTAL-ORDER, Finding 0031; SS-INTERVAL-CMP, Finding 0031]

Concretely: if a text POOM crum covers `[1.1, 1.2)`, then `intervalcmp(1.1, 1.2, 1.1.2)` returns `THRUME`, and the query hits. The intersection is resolved against actual POOM intervals without any normalization of the input depth.

### Downstream consequence if the span is also used as a V-position for INSERT

**`SS-INSERT-VWIDTH-ENCODING`** shows one place depth does matter operationally: `insertpm` computes `shift = tumblerlength(vsaptr) - 1` to encode the V-width. A depth-3 start gives `shift = 2` instead of the usual `1`, producing a V-width tumbler with a different exponent than crums created from standard 2-component positions. The invariant `value(V-width) == value(I-width)` still holds numerically, but the tumbler representation differs from the norm. [SS-INSERT-VWIDTH-ENCODING, SS-POOM-BOTTOM-CRUM, Finding 0076]

### Summary

| Stage | Behavior on depth mismatch |
|---|---|
| `acceptablevsa()` | Always TRUE — no depth check |
| `specset2sporglset()` | Document-existence check only |
| POOM search (`intervalcmp`) | Tumbler-arithmetic intersection — depth is irrelevant |
| No-match case | Returns empty sporglset — graceful, no error |
| V-width encoding (if used in INSERT) | Exponent shifts with depth, but numeric value preserved |

The system resolves by intersection. A depth-3 start that falls inside an existing POOM crum's interval produces a valid I-address result. One that falls outside all crums produces an empty result. Neither path rejects the span or normalizes its depth. [SS-TUMBLER, Finding 0001; INV-TUMBLER-TOTAL-ORDER, Finding 0031; PRE-SPECSET, Finding 0001; PRE-INSERT, Finding 0011]

---

## Code Exploration

I now have the complete picture from the source. Here is the full answer.

---

## Depth-Mismatch in `specset2ispanset` / `acceptablevsa`: Full Code Analysis

### Short answer

**No depth check exists anywhere in the resolution path.** `acceptablevsa` is an unconditional stub. The `tumblercmp`-based intersection arithmetic in `whereoncrum`/`crumqualifies2d` accepts depth-mismatched spans silently — it treats all tumblers as flat digit sequences, so a 3-component address `1.2.3` falls *inside* any depth-2 interval `[1.2, 1.3)` by the total order. The call does not crash or reject. However, the V→I clipping arithmetic in `context2span` produces **semantically incorrect** I-span offsets when depths differ, because `tumblerintdiff` returns `mantissa[0]` of the difference and that value misrepresents cross-depth offsets as same-depth units.

---

### 1. `acceptablevsa` — unconditional stub

`do2.c:110–113`:

```c
bool acceptablevsa(tumbler *vsaptr, typeorgl orglptr)
{
    return (TRUE);
}
```

Called in `do1.c:56` (inside `docopy`) and `do1.c:76` (inside `docopyinternal`) before any insertion. The function body is a single `return(TRUE)` — **no validation, no depth inspection, no orgl consultation.** It was clearly intended to validate the V-space address against the document's arrangement but was never implemented.

---

### 2. `specset2ispanset` dispatch — no depth check

`do2.c:14–46`. For a `VSPECID` item:

```c
findorgl(taskptr, granf, &vspecptr->docisa, &docorgl, type)
&& (ispansetptr = vspanset2ispanset(taskptr, docorgl, vspecptr->vspanset, ispansetptr))
```

No inspection of the depth (tumbler length) of `vspecptr->vspanset` components versus the document's V-arrangement before entering `vspanset2ispanset`.

---

### 3. Resolution path: `permute` → `span2spanset` → `retrieverestricted`

`orglinks.c:397–453`:
- `vspanset2ispanset` → `permute` iterates the restriction spanset  
- `span2spanset` calls `retrieverestricted((typecuc*)orgl, restrictionspanptr, V, NULL, I, NULL)`  
- `retrieverestricted` (`retrie.c:56–85`) passes `span1start`/`span1end` directly to `retrieveinarea`  

No depth check at any stage.

---

### 4. Tree intersection — `whereoncrum` and `tumblercmp`

The actual crum-qualification test is `crumqualifies2d` (`retrie.c:270–305`), which calls `whereoncrum` (`retrie.c:345–398`). For POOM/SPAN enfilades:

```c
// retrie.c:356-372
tumbleradd(&offset->dsas[index], &ptr->cdsp.dsas[index], &left);
cmp = tumblercmp(address, &left);
if (cmp == LESS) return(TOMYLEFT);
else if (cmp == EQUAL) return(ONMYLEFTBORDER);
tumbleradd(&left, &ptr->cwid.dsas[index], &right);
cmp = tumblercmp(address, &right);
if (cmp == LESS) return(THRUME);
else if (cmp == EQUAL) return(ONMYRIGHTBORDER);
else return(TOMYRIGHT);
```

`tumblercmp` → `abscmp` (`tumble.c:87–111`):

```c
static INT abscmp(tumbler *aptr, tumbler *bptr)
{
    if (aptr->exp != bptr->exp) { /* compare by exp */ }
    else {
        a = (INT *) aptr->mantissa;
        b = (INT *) bptr->mantissa;
        for (i = NPLACES; i--;) {   // all 16 slots, positional
            if (!(cmp = *a++ - *b++)) { }
            else if (cmp < 0) return (LESS);
            else return (GREATER);
        }
    }
    return (EQUAL);
}
```

**There is no depth concept here.** The tumbler struct (`common.h:59–65`) stores 16 mantissa slots (`NPLACES = 16`) and tumblers are compared slot-by-slot from most-significant to least-significant, with trailing zeros treated as literal digits.

**Depth-mismatch behavior under `abscmp`:**

- `1.2` is stored as mantissa `[1, 2, 0, 0, ...]`
- `1.3` is stored as mantissa `[1, 3, 0, 0, ...]`
- `1.2.3` is stored as mantissa `[1, 2, 3, 0, ...]`

Comparing `1.2.3` against the interval `[1.2, 1.3)`:
- `tumblercmp(1.2.3, 1.2)` → at slot 2: `3 − 0 = 3 > 0` → **GREATER** (i.e., not TOMYLEFT, not ONMYLEFTBORDER)
- `tumblercmp(1.2.3, 1.3)` → at slot 1: `2 − 3 = −1 < 0` → **LESS** → `THRUME` (inside)

So `whereoncrum` returns `THRUME` for `1.2.3` against a depth-2 crum spanning `[1.2, 1.3)`. **The crum qualifies.** The depth-3 address is topologically inside the depth-2 interval by the total order.

`crumqualifies2d` returns TRUE when `endcmp > ONMYLEFTBORDER` and `startcmp ≤ THRUME` — both satisfied here.

---

### 5. `context2span` — silently incorrect clipping

Once a crum qualifies, `context2span` (`context.c:176–212`) clips the crum's I-span to the restriction range. It adjusts the I-grasp/I-reach by the V-difference using `tumblerintdiff`:

```c
// context.c:191-203
if (tumblercmp(&grasp.dsas[idx1], &lowerbound) == LESS) {
    tumblerincrement(&grasp.dsas[idx2], 0,
        (INT) tumblerintdiff(&lowerbound, &grasp.dsas[idx1]),
        &grasp.dsas[idx2]);
}
if (tumblercmp(&reach.dsas[idx1], &upperbound) == GREATER) {
    tumblerincrement(&reach.dsas[idx2], 0,
        - tumblerintdiff(&reach.dsas[idx1], &upperbound),
        &reach.dsas[idx2]);
}
```

`tumblerintdiff` (`tumble.c:591–597`):

```c
INT tumblerintdiff(tumbler *aptr, tumbler *bptr)
{
    tumbler c;
    tumblersub(aptr, bptr, &c);
    return (c.mantissa[0]);   // only the first mantissa digit
}
```

**The depth-mismatch problem surfaces here.** Consider:

- Query lower bound: `1.2.3` → mantissa `[1, 2, 3, 0, ...]`
- Crum V-grasp: `1.2` → mantissa `[1, 2, 0, 0, ...]`
- Difference via `strongsub` (`tumble.c:534–565`): strips matching prefix digits, result has `exp = -2`, `mantissa = [3, 0, ...]` — representing `0.0.3`
- `tumblerintdiff` returns `mantissa[0] = 3`

The I-grasp is shifted by `+3`. But `3` here is **three sub-address units at depth-3**, not three depth-2 units. In a depth-2 V→I arrangement where each top-level unit maps to 1 I-unit, the entire depth-3 sub-address space `[1.2.0, 1.2.1, 1.2.2, ...]` lives *within the single depth-2 unit `1.2`*. `tumblerintdiff` extracts the `mantissa[0]` of `0.0.3`, which is `0`, not `3` — wait, let me be precise.

After `strongsub([1,2,3,...], [1,2,0,...])`:
- Slot 0: `1 == 1` → skip, `answer.exp--` → `-1`
- Slot 1: `2 == 2` → skip, `answer.exp--` → `-2`
- Slot 2: `3 ≠ 0` → `answer.mantissa[0] = 3 − 0 = 3`

Then `tumblerjustify` with `mantissa[0] = 3 ≠ 0` → no shift. Result: exp=-2, mantissa=[3,...].

So `tumblerintdiff` returns **3**, not 0. The I-grasp is shifted by 3 units. This is numerically wrong: those 3 units represent depth-3 sub-positions within a single depth-2 slot, but the V→I linear mapping in the POOM maps each depth-2 unit to a block of I-units. The `+3` adjustment skips 3 I-units as though the query started 3 depth-2 units into the crum — it does not.

The result is a **silently wrong I-span**: no crash, no error, no gerror, just an incorrect I-position returned from the resolution.

---

### Summary table

| Check point | Location | Depth-mismatch behavior |
|---|---|---|
| `acceptablevsa` | `do2.c:110–113` | **Unconditional stub — always TRUE** |
| `specset2ispanset` | `do2.c:14–46` | No depth check on vspanset |
| `vspanset2ispanset` / `permute` | `orglinks.c:397–422` | No depth check |
| `retrieverestricted` | `retrie.c:56–85` | Passes tumblers through as-is |
| `crumqualifies2d` / `whereoncrum` | `retrie.c:270–398` | Purely positional `tumblercmp`; `1.2.3` falls inside `[1.2, 1.3)` by total order — **intersects** |
| `context2span` | `context.c:176–212` | `tumblerintdiff` extracts `mantissa[0]` of cross-depth difference; yields wrong I-span offset, **no error** |
| `tumblercmp` / `abscmp` | `tumble.c:72–111` | 16-slot positional comparison, no depth metadata |

**Conclusion:** The path does not reject or normalize depth-mismatched spans. `acceptablevsa` is unimplemented. The intersection test (`whereoncrum` via `tumblercmp`) accepts a 3-component query address against a 2-component arrangement because lexicographic ordering places `1.2.n` inside `[1.2, 1.3)` for all `n`. The clipping arithmetic (`context2span` via `tumblerintdiff`) then silently produces incorrect I-span offsets, because `tumblerintdiff` returns `mantissa[0]` of the subtraction result, which misinterprets a cross-depth mantissa difference as a same-depth unit offset.
