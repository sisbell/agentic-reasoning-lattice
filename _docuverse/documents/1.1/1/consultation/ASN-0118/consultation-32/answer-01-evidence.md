## Question 1 [evidence]

> When a spec-set span's start or width has a different tumbler depth than the document's bound V-positions (e.g., a depth-3 span over a depth-2 text subspace), does the resolution path (`specset2ispanset` and the underlying tumbler intersection) admit the span and correctly select the bound positions inside its denotation, or does any check reject or misresolve depth-mismatched spans?

## KB Synthesis

## Depth-Mismatched Span Resolution in `specset2ispanset`

The KB does not contain a golden test that directly probes this exact scenario, but the machinery is documented precisely enough to answer it with confidence.

### The path admits depth-mismatched spans without rejection

`specset2sporglset()` validates only document existence, not element-level tumbler structure [PRE-SPECSET]:

> "The backend's `specset2sporglset()` validates specsets at document granularity only. It checks that the referenced document exists but does not enforce element-level tumbler structure."

`acceptablevsa()` (the only candidate V-position validation hook) unconditionally returns `TRUE` [SS-SUBSPACE-CONVENTION, Finding 0010; PRE-INSERT, Finding 0011]. There is no depth check anywhere in the `specset2ispanset` → `permute` → `span2spanset` → `retrieverestricted` call chain.

### Resolution is purely tumbler-arithmetic

Once admitted, resolution flows through `whereoncrum()` [SS-WHEREONCRUM]:

> Computes `left = offset + cdsp`, `right = left + cwid`, then returns one of five spatial classifications via `intervalcmp`.

`intervalcmp` itself is purely numeric: five-way comparison of `address` against `[left, right)` using `tumblercmp` [SS-INTERVAL-CMP]. The POOM B-tree traversal (`findcbcinarea2d`) descends into subtrees whose ranges intersect the query interval using the same arithmetic [SS-ENFILADE-TREE, Finding 0071].

### The total order determines what gets matched

The critical property is from [INV-TUMBLER-TOTAL-ORDER] (Finding 0031):

> `tumblercmp(1.1.0.2, 1.1.0.2.0.1)` → `LESS` (trailing zeros vs non-zero digits)

Because tumblers are digit sequences with `exp` and mantissa, a shallower tumbler like `1.1` effectively carries trailing zeros. It is numerically **less than** `1.1.0.1`:

```
1.1          = {exp=0, mant=[1,1,0,0,...]}
1.1.0.1      = {exp=0, mant=[1,1,0,1,...]}
1.1 < 1.1.0.1
```

This follows directly from [SS-TUMBLER] (Finding 0031): "zeros within the mantissa act as hierarchical separators."

### Consequences

**Case A — Span deeper than bound V-positions** (e.g., span `[1.1.0.1, 1.1.0.2)`, bound positions at `1.1`, `1.2`, `1.3`):

- `1.1 < 1.1.0.1` → `1.1` is `TOMYLEFT` of the span
- `1.2 < 1.1.0.1`? No, `1.2 > 1.1.0.1` but `1.2 > 1.1.0.2` too → `1.2` is `TOMYRIGHT`
- Result: **no bound V-positions fall inside the span; `specset2ispanset` returns empty**. No error is raised.

**Case B — Span shallower than bound V-positions** (e.g., span `[1.0, 2.0)`, bound positions at `1.1`, `1.1.0.2.3`, `1.5`):

- All these are numerically in `[1.0, 2.0)` → `THRUME`
- Result: **all bound V-positions within the numeric range are correctly selected**, regardless of depth. This is the normal case for document-level retrieval specsets.

**Case C — Straddle at a boundary** (e.g., span `[1.0, 1.1.0.1)`):

- `1.1` = `1.1.0.0...` < `1.1.0.1`, so `1.1` is `THRUME` (inside)
- `1.1.0.1` is `ONMYRIGHTBORDER` (excluded per half-open semantics)
- The boundary classification from [SS-WHEREONCRUM] applies faithfully

### No misresolution — faithful arithmetic

There is no silent misresolution. The POOM lookup is a faithful tree search over the numeric interval. A depth-mismatched span either correctly matches the positions numerically within it, or returns empty if the numeric ranges don't overlap. The only surprise is that a caller assuming ".0." boundaries create "container" relationships may be wrong: `1.1.0.1` does NOT contain `1.1`; `1.1` is numerically smaller and lies outside it.

This is precisely what [PRE-SPECSET] acknowledges as the design boundary: the backend does not enforce that specset addresses match the document's element-level addressing scheme. The caller bears responsibility for constructing spans whose numeric ranges actually overlap the bound V-positions they intend to match.

---

## Code Exploration

Now I have everything I need. Let me trace the full resolution path with precise citations.

---

## Depth-Mismatched Tumbler Spans in the Resolution Path

**Short answer:** The resolution path contains **no depth check at any level**. Depth-mismatched spans are admitted by pure numerical tumbler comparison. Crum *selection* (which crums qualify) is numerically consistent. Crum *trimming* in `context2span` is **misresolved** when the span boundary falls inside a depth-2 crum at depth-3 precision, due to `tumblerintdiff` discarding the `exp` scaling factor.

---

### 1. Entry Point: `specset2ispanset` — No Depth Guard

`do2.c:14–46`:
```c
bool specset2ispanset(typetask *taskptr, typespec *specset, typeispanset *ispansetptr, int type)
{
    ...
    for (; specset; specset = ...) {
        if (((typeitemheader *)specset)->itemid == ISPANID) {
            // passed through directly
        } else if (((typeitemheader *)specset)->itemid == VSPECID) {
            if (iszerotumbler(&((typevspec *)specset)->docisa))
                qerror("retrieve called with docisa 0\n");
            if (!(findorgl(...) && (ispansetptr = vspanset2ispanset(...)))) {
                return (FALSE);
            }
        }
    }
    return (TRUE);
}
```

The only validation is `iszerotumbler(docisa)` [do2.c:28] — a zero-ISA check. There is **no check on the depth of the vspanset's stream or width tumblers**. `acceptablevsa` [do2.c:110–113] returns `TRUE` unconditionally and is not called from this path at all.

---

### 2. V→I Translation: `vspanset2ispanset` → `permute` → `span2spanset`

`orglinks.c:397–402`:
```c
typeispanset *vspanset2ispanset(typetask *taskptr, typeorgl orgl,
        typevspanset vspanptr, typeispanset *ispansetptr)
{
    return permute(taskptr, orgl, vspanptr, V, ispansetptr, I);
}
```

`permute` [orglinks.c:404–422] iterates every span in the vspanset and calls `span2spanset` per span. No depth examination.

`span2spanset` [orglinks.c:425–454] calls `retrieverestricted`, then for each returned context calls `context2span`. Still no depth check.

---

### 3. Retrieval: Purely Numerical Tumbler Intersection

`retrieverestricted` [retrie.c:56–85] copies the span's `stream` and computes `span1end = stream + width` via `tumbleradd`, then calls `retrieveinarea` → `findcbcinarea2d` → `crumqualifies2d` → `whereoncrum`.

**`whereoncrum` for POOM** [retrie.c:345–398]:
```c
case POOM:
    tumbleradd(&offset->dsas[index], &ptr->cdsp.dsas[index], &left);
    cmp = tumblercmp(address, &left);
    if (cmp == LESS) return (TOMYLEFT);
    else if (cmp == EQUAL) return (ONMYLEFTBORDER);
    tumbleradd(&left, &ptr->cwid.dsas[index], &right);
    cmp = tumblercmp(address, &right);
    if (cmp == LESS) return (THRUME);
    else if (cmp == EQUAL) return (ONMYRIGHTBORDER);
    else return (TOMYRIGHT);
```

`tumblercmp` [tumble.c:72–85] → `abscmp` [tumble.c:87–111]:
```c
static INT abscmp(tumbler *aptr, tumbler *bptr)
{
    if (aptr->exp != bptr->exp) {
        return (aptr->exp < bptr->exp) ? LESS : GREATER;
    }
    a = (INT *) aptr->mantissa;
    b = (INT *) bptr->mantissa;
    for (i = NPLACES; i--;) {
        if (!(cmp = *a++ - *b++)) { }
        else if (cmp < 0) return (LESS);
        else return (GREATER);
    }
    return (EQUAL);
}
```

`abscmp` compares `exp` first, then mantissa position by position. **There is no concept of "depth" — it is pure numerical ordering.** A depth-3 tumbler `1.0.1` (mantissa=[1,0,1,...], exp=0) compares as numerically LESS than the depth-2 text position `1.1` (mantissa=[1,1,...], exp=0) because `mantissa[1]=0 < 1`.

**Crum qualification is purely numerical.** A depth-3 span `[1.0.1, 2.0)` over the depth-2 text subspace `[1.1, 1.6)` causes:
- `startcmp = whereoncrum(crum, 0, 1.0.1, V)` → `tumblercmp(1.0.1, left=1.1) = LESS` → `TOMYLEFT` (-2), which is ≤ THRUME: **passes**
- `endcmp = whereoncrum(crum, 0, 2.0, V)` → `tumblercmp(2.0, left=1.1) = GREATER` → `TOMYRIGHT` (2), which is > ONMYLEFTBORDER: **passes**

The crum qualifies. No rejection.

---

### 4. The `absadd` Precision Loss

`tumble.c:460–484`. When adding `a + b` where `a.exp == b.exp`:
```c
ansmant[0] = amant[0] + bmant[0];
i = j = 1;
// ...
while (j <= NPLACES-1) {
    ansmant[j++] = bmant[i++];   // copies ONLY from b's mantissa
}
```

After the MSB addition, the loop copies from `bmant` — **not from `amant`**. The sub-stories of `a` beyond position 0 are lost. This means:

`absadd(1.0.1, 1.0.0)` = `2.0.0` — the `.1` of the first operand is discarded. This is the right boundary computation in `whereoncrum`. The right boundary of a depth-3 crum origin is computed without preserving its sub-stories.

In the normal depth-2 text case (e.g., `absadd(1.3, exp=-1 width)`) this works correctly because there are no sub-stories in either operand past the relevant position. But for depth-3 origins in the SPAN/POOM case, the right boundary loses the deepest story of the left operand.

---

### 5. The Core Misresolution: `context2span` + `tumblerintdiff`

`context.c:176–212`. After finding a qualifying crum, this function trims the returned I-span to fit the V-restriction:

```c
if (tumblercmp(&grasp.dsas[idx1], &lowerbound) == LESS) {
    tumblerincrement(&grasp.dsas[idx2], 0,
        (INT)tumblerintdiff(&lowerbound, &grasp.dsas[idx1]),
        &grasp.dsas[idx2]);
}
```

`tumblerintdiff` [tumble.c:591–597]:
```c
INT tumblerintdiff(tumbler *aptr, tumbler *bptr)
{
  tumbler c;
    tumblersub(aptr, bptr, &c);
    return (c.mantissa[0]);
}
```

It calls `tumblersub` (via `strongsub`) and returns **only `c.mantissa[0]`** — ignoring `c.exp`.

`strongsub` [tumble.c:534–565] strips the equal prefix and stores the first differing digit in `mantissa[0]`, with `exp` decremented by the number of equal leading digits. For `1.1.1 - 1.1`:
- mantissa[0]=1==1 → equal, exp becomes -1
- mantissa[1]=1==1 → equal, exp becomes -2
- mantissa[2]=1 vs 0 → differing: `answer.mantissa[0] = 1`
- Result: exp=-2, mantissa=[1,...]

`tumblerintdiff` returns **1** — treating the result as a depth-1 integer, ignoring `exp=-2`.

**The misresolution:** The difference `1.1.1 - 1.1` represents `1 * base^{-2}` (one depth-3 sub-unit). `tumblerintdiff` returns 1, which `context2span` uses as a **1-character I-trim**. This skips an entire character at the I-dimension boundary, when the correct V-offset is a sub-character fraction.

Concrete failure case: a depth-3 span starting at `1.1.5` (over a 5-character depth-2 crum at `[1.1, 1.6)`):
- `tumblerintdiff(1.1.5, 1.1)` → `strongsub` produces exp=-2, mantissa=[5]
- `tumblerintdiff` returns 5
- `tumblerincrement` shifts `grasp.dsas[I]` forward by 5 characters
- The crum covers 5 characters total → zero-width (or underflowing) I-span is returned

This is clearly wrong: `1.1.5` is numerically only `5 * base^{-2}` past `1.1` — a tiny sub-character offset — yet the code skips all 5 characters.

---

### 6. The Text V-Space Depth Is Depth-2

For completeness, the actual depth-2 structure of the text subspace, established by `findvsatoappend` [orglinks.c:36–48] and `insertpm` [orglinks.c:75–133]:

- Text VSAs are depth-2: `tumblerincrement(vsaptr, 0, 1, vsaptr)` then `tumblerincrement(vsaptr, 1, 1, vsaptr)` produces mantissa=[1,1,...] [orglinks.c:42–43]
- V-widths are `exp=-1` sub-addresses: `tumblerincrement(&zero, shift=1, inc, &crumwidth)` → exp=-1, mantissa=[inc] [orglinks.c:117]
- Text crums are at depth-2 positions: `istextcrum` checks `cdsp.dsas[V].mantissa[1] == 0` (depth-1 displacement, depth-2 absolute) [orglinks.c:248]

The entire populated text V-subspace lives in depth-2 tumbler addresses `[1.1, 2.0)`. There are no depth-3 positions in it.

---

### Summary

| Layer | Location | Depth check? | Effect of depth mismatch |
|-------|----------|--------------|--------------------------|
| `specset2ispanset` | do2.c:14 | None | Span passed through |
| `vspanset2ispanset` → `permute` | orglinks.c:397–422 | None | Each span processed |
| `retrieverestricted` → `findcbcinarea2d` | retrie.c:56–268 | None | All crums evaluated |
| `crumqualifies2d` → `whereoncrum` | retrie.c:270–398 | None | Pure numerical interval test |
| `tumblercmp` → `abscmp` | tumble.c:72–111 | None | Pure mantissa comparison, position by position |
| `absadd` (in boundary computation) | tumble.c:460–484 | None | Drops lower stories of first operand when copying tail from second |
| `context2span` + `tumblerintdiff` | context.c:176; tumble.c:591 | None | **Returns `c.mantissa[0]` ignoring `c.exp`; misscales I-trim by `base^k` for depth-k mismatch** |

**The path admits any depth-mismatched V-span without rejection.** Crum selection (which crums fall numerically inside the span) is consistent with pure tumbler ordering. The boundary trimming inside a qualifying crum is **misresolved**: `tumblerintdiff` in `context2span` discards the `exp` of the difference, applying an I-space trim that is `base^k` times too large when the span boundary has `k` more stories than the text V-positions. For the realistic case (depth-3 span over depth-2 text), the trim is `base` times too large, potentially skipping entire characters or overflowing the crum's I-extent.
