## Question 1 [evidence]

> Does udanax-green's spec-set resolution path (specset2ispanset and the surrounding V-spec acceptance code) admit a spec whose span tumblers have a different depth than the document's bound V-positions — e.g., a depth-3 start/width over a depth-2 text subspace — and if so, does it resolve such a span by pure intersection with the bound positions, or does any check reject or normalize the depth mismatch?

## KB Synthesis

## V-spec Depth Mismatch: Resolution by Pure Tumbler Intersection

The KB does not contain a dedicated finding on this exact scenario, but the answer can be synthesized with confidence from several entries.

### The acceptance layer performs no depth check

`acceptablevsa()` in `do2.c:110-113` unconditionally returns `TRUE` [PRE-INSERT, SS-SUBSPACE-CONVENTION]. There is no structural validation of the tumbler depth of a caller-supplied V-address at entry. `specset2sporglset()` validates only document existence, not element-level tumbler structure [PRE-SPECSET]. So a depth-3 start tumbler (e.g. `1.1.0.1`) passes through without rejection.

### The POOM lookup is pure tumbler-order intersection

`permute()` (`orglinks.c:389-422`) and `retrieverestricted()` are fully type-agnostic — they treat all V-addresses as uninterpreted tumblers [SS-DUAL-ENFILADE, Finding 0011]. The lookup proceeds through `intervalcmp` / `whereoncrum`, both of which classify an address relative to a crum's `[grasp, reach)` interval using the total tumbler order only [SS-INTERVAL-CMP, SS-WHEREONCRUM]. No normalization of depth is performed.

### Tumbler ordering determines what, if anything, resolves

From [INV-TUMBLER-TOTAL-ORDER, SS-TUMBLER]: tumblers are compared exponent-first, then mantissa lexicographically. In the 16-digit mantissa representation:

- `1.1` → mantissa `[1,1,0,0,…]`
- `1.1.0.1` → mantissa `[1,1,0,1,0,…]`
- `1.2` → mantissa `[1,2,0,0,…]`

Therefore `1.1 < 1.1.0.1 < 1.2` in the total order. A spec with start=`1.1.0.1` and a small width lands entirely in the "gap" between the depth-2 V-positions `1.1` and `1.2`. No POOM crum whose grasp is `1.1` and reach is `1.2` (or similar depth-2 round numbers) will be classified `THRUME` for an address in that gap — the crum whose grasp is `1.1` has `whereoncrum(crum, 1.1.0.1) = THRUME` (strictly interior), so that crum *is* entered and its content is examined. But if the crum covers `[1.1, 1.12)` (11 characters), then `1.1.0.1` falls inside it and that I-address mapping would be returned.

Conversely, if the spec start is `1.1.0.1` but the crum only covers `[1.1, 1.11)`, whether the range intersects depends entirely on the endpoint arithmetic. There is no coercion.

### Width depth mismatch is also unguarded

The `strongsub` exponent guard [SS-TUMBLER, Finding 0055] applies only during DELETE's shift arithmetic (`tumblersub` via `strongsub`), not during POOM lookup. The lookup computes `end = tumbleradd(start, width)` and then applies interval classification — cross-depth widths pass through normally. A depth-3 width like `0.0.0.5` is a valid tumbler and produces a valid range endpoint; the lookup just intersects that range against POOM entries.

### Summary

There is no depth normalization, no depth rejection, and no special handling of mismatches anywhere in the path from VSpec → `specset2ispanset` → `permute` → `retrieverestricted` → `intervalcmp`. The resolution is pure tumbler-order interval intersection. A depth-3 spec applied over depth-2 bound V-positions will:

- **Resolve non-empty** if and only if its `[start, start+width)` tumbler range contains or overlaps depth-2 POOM entries under the total order
- **Resolve empty silently** (no error) if the range falls entirely in the gaps between depth-2 positions
- **Never be rejected or normalized**

This is consistent with the broader convention-over-enforcement design documented throughout the KB [SS-SUBSPACE-CONVENTION, PRE-INSERT]: the storage layer is a uniform tumbler-addressed B-tree, and all semantic constraints — including "V-addresses should match the depth at which content was inserted" — are caller obligations with no backend enforcement.

---

## Code Exploration

I have all the evidence I need. Here is the complete analysis:

---

## Depth-Mismatch Handling in Spec-Set → I-Span Resolution

### Short answer

The code **admits** a spec whose V-span tumblers have a different depth (more mantissa levels) than the document's bound V-positions, and resolves it by pure numeric intersection with no depth check or normalization. The one hook explicitly intended to police V-addresses (`acceptablevsa`) is an unconditional stub. When the depths do differ, the subsequent arithmetic in `context2span` misreads sub-integer tumbler differences as integer content offsets, silently producing incorrect I-spans.

---

### 1. Tumbler depth encoding

The tumbler structure is defined in `backend/common.h:59-65`:

```c
typedef struct structtumbler {
    humber xvartumbler;
    char   varandnotfixed;
    char   sign  BIT;
    short  exp;
    tdigit mantissa[NPLACES];   /* NPLACES = 16 */
} tumbler;
```

"Depth" of a tumbler is `tumblerlength()` = `nstories() - exp` [`tumble.c:259-262`], where `nstories` is `index_of_last_nonzero_mantissa_place + 1`. A depth-1 address (e.g. `3`) has only `mantissa[0]` non-zero. A depth-3 address (e.g. `1.0.2`) has `mantissa[0]=1, mantissa[1]=0, mantissa[2]=2`. `is1story()` [`tumble.c:237-247`] tests the depth-1 condition: returns `TRUE` iff all `mantissa[i] == 0` for `i ≥ 1`.

The text subspace of a document uses depth-1 V-addresses exclusively, confirmed by `istextcrum()` [`orglinks.c:246-253`]:
```c
bool istextcrum(typecorecrum *crumptr) {
    if(crumptr->cdsp.dsas[V].mantissa[1] == 0 && is1story(&crumptr->cwid.dsas[V]))
        return TRUE;
    return FALSE;
}
```

Sub-addresses like `1.0.2` fall between integer positions `1` and `2` in the tumbler total order (since `mantissa[0]=1` places them after `1` and `mantissa[0] < 2` places them before `2`).

---

### 2. Entry point: `specset2ispanset`

`do2.c:14-46`:
```c
bool specset2ispanset(typetask *taskptr, typespec *specset, typeispanset *ispansetptr, int type)
{
    ...
    for (; specset; specset = ...) {
        if (... itemid == ISPANID) {
            /* pass through as-is */
        } else if (... itemid == VSPECID) {
            if (iszerotumbler (&((typevspec *)specset)->docisa))
                qerror("retrieve called with docisa 0\n");
            if (!(
              findorgl(taskptr, granf, &((typevspec*)specset)->docisa, &docorgl, type)
            && (ispansetptr = vspanset2ispanset(taskptr, docorgl,
                    ((typevspec *)specset)->vspanset, ispansetptr)))){
                return (FALSE);
            }
        }
    }
    return (TRUE);
}
```

The only guard on the `VSPECID` branch is that `docisa` is non-zero. **There is no check on the depth, structure, or range of the `vspanset` tumblers.** The vspan stream and width are passed directly into `vspanset2ispanset`.

---

### 3. The `acceptablevsa` stub

The function that was clearly intended to validate V-space addresses is at `do2.c:110-113`:

```c
bool acceptablevsa(tumbler *vsaptr, typeorgl orglptr)
{
    return (TRUE);
}
```

It is called in `do1.c:56` (inside `docopy`) and `do1.c:76` (inside `docopyinternal`), and its prototype appears in `backend/protos.h`. The body is empty — it accepts any tumbler, regardless of depth, regardless of the document's actual V-extent. Any VSA validation that was planned was never implemented.

---

### 4. Call chain: V-span to I-span

`vspanset2ispanset` [`orglinks.c:397-402`] immediately delegates:
```c
typeispanset *vspanset2ispanset(...)
{
    return permute(taskptr, orgl, vspanptr, V, ispansetptr, I);
}
```

`permute` [`orglinks.c:404-422`] iterates over each V-span and calls `span2spanset`. `span2spanset` [`orglinks.c:425-454`] calls:
```c
context = retrieverestricted((typecuc*)orgl, restrictionspanptr, V, (typespan*)NULL, I, (typeisa*)NULL);
```

`retrieverestricted` [`retrie.c:56-85`] extracts `span1start`/`span1end` via:
```c
movetumbler(&span1ptr->stream, &span1start);
tumbleradd(&span1start, &span1ptr->width, &span1end);
```
— a plain copy and add. No depth check. It then calls `retrieveinarea` → `findcbcinarea2d`.

---

### 5. Intersection test: `crumqualifies2d` and `whereoncrum`

`findcbcinarea2d` [`retrie.c:229-268`] walks the enfilade tree and calls `crumqualifies2d` for each node. `crumqualifies2d` [`retrie.c:270-305`] checks span overlap via `whereoncrum`:

```c
endcmp = iszerotumbler(span1end) ? TOMYRIGHT : whereoncrum(crumptr, offset, span1end, index1);
if (endcmp <= ONMYLEFTBORDER) return(FALSE);
startcmp = whereoncrum(crumptr, offset, span1start, index1);
if (startcmp > THRUME) return(FALSE);
```

`whereoncrum` for a POOM node [`retrie.c:354-372`]:
```c
tumbleradd(&offset->dsas[index], &ptr->cdsp.dsas[index], &left);
// compare address to left, then to right = left + cwid
```

Both comparisons use `tumblercmp` [`tumble.c:72-85`], which delegates to `abscmp`. `abscmp` first compares `exp` fields, then lexicographically compares `mantissa[]` arrays. It has no concept of "depth mismatch" — it treats tumblers as pure numbers. A depth-3 spec address like `1.0.2` falls numerically between depth-1 addresses `1` and `2`, so it satisfies `whereoncrum` for any crum whose V-range includes the interval `[1, 2)`.

**Conclusion on qualification:** A depth-3 spec span **does** intersect and qualify depth-1 document crums, because the numeric overlap test has no depth awareness.

---

### 6. I-coordinate computation: `context2span`

After qualification, `span2spanset` calls `context2span` [`context.c:176-212`] to translate V-restriction into I-span:

```c
int context2span(typecontext *context, typespan *restrictionspanptr, INT idx1,
                 typespan *foundspanptr, INT idx2)
{
    movetumbler(&restrictionspanptr->stream, &lowerbound);
    tumbleradd(&lowerbound, &restrictionspanptr->width, &upperbound);
    prologuecontextnd(context, &grasp, &reach);

    if (tumblercmp(&grasp.dsas[idx1], &lowerbound) == LESS) {
        tumblerincrement(&grasp.dsas[idx2], 0,
            (INT) tumblerintdiff(&lowerbound, &grasp.dsas[idx1]),
            &grasp.dsas[idx2]);
    }
    if (tumblercmp(&reach.dsas[idx1], &upperbound) == GREATER) {
        tumblerincrement(&reach.dsas[idx2], 0,
            -tumblerintdiff(&reach.dsas[idx1], &upperbound),
            &reach.dsas[idx2]);
    }
    movetumbler(&grasp.dsas[idx2], &foundspanptr->stream);
    tumblersub(&reach.dsas[idx2], &grasp.dsas[idx2], &foundspanptr->width);
```

The clipping arithmetic calls `tumblerintdiff` [`tumble.c:591-597`]:
```c
INT tumblerintdiff(tumbler *aptr, tumbler *bptr) {
    tumbler c;
    tumblersub(aptr, bptr, &c);
    return (c.mantissa[0]);
}
```

This returns only `mantissa[0]` of the difference, discarding the `exp` field. When a depth-3 spec boundary like `1.0.2` is compared against a depth-1 crum start `1`:

- `tumblersub(1.0.2, 1)` → `strongsub` peels off matching prefix digits, yielding result with `exp=-2, mantissa[0]=2` [`tumble.c:534-565`].
- `tumblerintdiff` returns `c.mantissa[0]` = **2**.
- The code then shifts the I-start by **2 content units**, as if the depth-3 address `1.0.2` were 2 characters past the crum's V-start.

In reality `1.0.2` is a sub-address in the gap between depth-1 positions `1` and `2` — it does not correspond to 2 content units of offset. The `exp=-2` in the difference is silently discarded; the depth information is lost.

This means: with a depth-3 spec over a depth-1 text subspace, `context2span` produces an I-span that is offset from reality by the sub-digit value — a nonsensical result. No error is raised.

---

### Summary table

| Location | What it does | Depth check? |
|---|---|---|
| `specset2ispanset` [`do2.c:14`] | Entry: iterates spec items, dispatches VSPECID | None — only checks `docisa != 0` |
| `acceptablevsa` [`do2.c:110`] | Hook intended to validate VSA against document | **Stub: always `return TRUE`** |
| `vspanset2ispanset` / `permute` [`orglinks.c:397,404`] | V→I delegation chain | None |
| `retrieverestricted` [`retrie.c:56`] | Extracts span bounds, calls area search | None |
| `crumqualifies2d` / `whereoncrum` [`retrie.c:270,345`] | Numeric interval overlap test | None — uses `tumblercmp`, pure numeric ordering |
| `context2span` [`context.c:176`] | Maps V restriction to I result via clipping | None; `tumblerintdiff` discards `exp`, silently misinterprets depth-3 boundaries as integer offsets |

**The path admits depth-mismatched specs at every stage. Resolution is pure numeric intersection. No check rejects or normalizes the depth mismatch, but the arithmetic in `context2span` silently produces wrong I-spans when spec tumblers have deeper sub-addresses than the document's bound V-positions.**
