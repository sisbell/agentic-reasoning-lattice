## Question 15 [gregory]

> When COPY brings in a multi-span specset where some source spans happen to be I-address-contiguous with existing target POOM entries, does `isanextensionnd` coalesce across the specset boundary — merging the last byte of one copied span with the first byte of the next if they are I-adjacent?

## KB Synthesis

## Short answer: Yes, but only when all three extension conditions coincidentally align

`isanextensionnd` has no awareness of specset structure. It inspects only the current POOM state against the incoming insertion. The check is purely arithmetic [PRE-COPY / Finding 0046]:

1. **Same `homedoc`**: the new content's I-address origin document matches the existing crum's recorded `homedoc`
2. **V-contiguity**: the new content's target V-origin equals the existing crum's V-reach
3. **I-contiguity**: the new content's I-origin equals the existing crum's I-reach

When COPY processes a multi-span specset, `docopy` converts the full specset to I-spans via `specset2ispanset`, then iterates through the resulting I-spans calling `insertpm` for each. After span N is inserted, a POOM crum exists covering it. When span N+1 is subsequently inserted, `isanextensionnd` checks the crum created by span N against the incoming data — the fact that they came from adjacent VSpecs is invisible to it.

Therefore, if span N's last byte maps to I-address `α_k` (reach = `α_{k+1}`) and span N+1's first byte happens to be `α_{k+1}`, AND both are being placed at V-positions such that the target V-addresses are also contiguous, AND both came from the same source document (`homedoc` match) — coalescing fires. The specset boundary is not a barrier.

### Conditions that make cross-boundary coalescing likely

From [ST-VCOPY] (Finding 0046) and [INV-MONOTONIC] (Finding 0033):

- **I-contiguity**: arises naturally when the source spans were originally inserted sequentially with no intervening `CREATELINK` or other non-text allocations between them [INT-LINK-INSERT / Finding 0063]. Spans from fragmented or multi-source content will not be I-contiguous.

- **V-contiguity**: requires that the caller places span N+1 immediately after span N at the target. Since specset order determines insertion order [INV-SPECSET-ORDER], if the VSpecs in the specset describe adjacent target positions, this holds.

- **Same homedoc**: requires both spans originated from the same source document. Cross-document specsets (referencing content from multiple documents) will fail this check [PRE-COPY].

### What the KB does not cover

The KB has no direct experimental evidence for or against cross-specset coalescing. This answer is inferred from the code-level description of `isanextensionnd` in [PRE-COPY / Finding 0046] and [ST-INSERT / Finding 0062] — neither of which mentions specset structure as a factor. If you need a definitive answer, a targeted test (two I-contiguous spans in a single specset copied to contiguous target V-positions, then checking crum count) would confirm it.

---

## Code Exploration

I have all the code I need. Here is the complete analysis with citations.

---

## Answer: Does `isanextensionnd` coalesce across the specset boundary?

**Short answer: Yes — but only when the two consecutive specset spans share the same source document (homedoc). The V-address alignment is automatic and exact; the homedoc check is the decisive gate.**

---

### Call Chain for COPY

`docopy` [do1.c:45–65] converts its specset to an ispanset and calls:

```c
insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset)   /* do1.c:60 */
```

`insertpm` [orglinks.c:75–134] iterates span-by-span over the sporglset:

```c
for (; sporglset; sporglset = (typesporglset) sporglset->xxxxsporgl.next) {
    unpacksporgl (sporglset, &lstream, &lwidth, &linfo);
    movetumbler (&lstream, &crumorigin.dsas[I]);
    movetumbler (&lwidth,  &crumwidth.dsas[I]);
    movetumbler (vsaptr,   &crumorigin.dsas[V]);   // V-origin = current VSA
    // ... compute crumwidth.dsas[V] from lwidth ...
    insertnd (taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);
    tumbleradd (vsaptr, &crumwidth.dsas[V], vsaptr);   // advance VSA  [orglinks.c:131]
}
```

The critical line is [orglinks.c:131]: `vsaptr` is advanced by span A's V-width immediately after `insertnd` returns, *before* span B is processed. Span B therefore receives `crumorigin.dsas[V]` = span A's V-end, making B's V-origin exactly equal to A's V-reach.

---

### What `isanextensionnd` Tests

`insertcbcnd` [insertnd.c:242–275] iterates all bottom crums in the father, testing each against:

```c
if (isanextensionnd ((typecbc*)ptr, grasp, origin, infoptr))  /* insertnd.c:250 */
```

`isanextensionnd` [insertnd.c:301–309]:

```c
bool isanextensionnd(typecbc *ptr, typedsp *offsetptr, typedsp *originptr,
                     type2dbottomcruminfo *infoptr)
{
    typedsp grasp, reach;
    if (!tumblereq (&infoptr->homedoc, &((type2dcbc *)ptr)->c2dinfo.homedoc))
        return (FALSE);                              /* homedoc gate */
    prologuend ((typecorecrum*)ptr, offsetptr, &grasp, &reach);
    return (lockeq (reach.dsas, originptr->dsas,
                    (unsigned)dspsize(ptr->cenftype)));
}
```

**`prologuend`** [retrie.c:334–339] computes:

```
grasp = offset + ptr->cdsp          (absolute start)
reach = grasp  + ptr->cwid          (absolute end)
```

**`dspsize(POOM) = DSPSIZEPM = 2`** [wisp.h:26], meaning a POOM displacement contains two tumblers: `dsas[I]` and `dsas[V]`.

**`lockeq`** [wisp.c:261–267] iterates over exactly `loxize` tumblers:

```c
bool lockeq(tumbler *lock1, tumbler *lock2, unsigned loxize)
{
    while (loxize--)
        if (!tumblereq (lock1++, lock2++))
            return(FALSE);
    return(TRUE);
}
```

With `loxize = 2`, it requires `reach.dsas[I] == origin.dsas[I]` **AND** `reach.dsas[V] == origin.dsas[V]` simultaneously. There is no way to satisfy only the I-dimension.

---

### The Specset-Boundary Scenario

Suppose the ispanset contains two consecutive spans A and B that are I-adjacent:
- Span A: I-range = `[Ia, Ia+wa)`, inserted at V-start `Vs`
- Span B: I-range = `[Ia+wa, Ia+wa+wb)` — I-adjacent to A

After `insertnd` for A:
- A's POOM crum has reach: `(I: Ia+wa, V: Vs+wa)`
- `vsaptr` is advanced to `Vs+wa`

`insertnd` for B uses:
- `crumorigin.dsas[I]` = `Ia+wa`
- `crumorigin.dsas[V]` = `Vs+wa` (the advanced vsaptr)

So B's origin = `(I: Ia+wa, V: Vs+wa)` = A's reach exactly.

`isanextensionnd` now checks:
1. **Homedoc:** from `unpacksporgl` [sporgl.c:184–187], if both are SPORGLID items, `infoptr->homedoc` = `sporglptr->sporgladdress`. If A and B came from the same source document, the homedoc tumblers match → passes. If from different source documents → returns `FALSE` immediately, no coalescence.
2. **`lockeq(reach, origin, 2)`:** as shown above, `reach == origin` in both dimensions → `TRUE`.

**When the homedoc check passes, `isanextensionnd` fires and `dspadd(&ptr->cwid, width, &ptr->cwid, ...)` [insertnd.c:251] widens A's crum to absorb B** — the two POOM entries are merged into one.

---

### Interaction with Pre-Existing POOM Entries

For an existing crum C with V-reach = `V_old`:
- C's reach = `(I: some_I_end, V: V_old)`
- First copied span's origin = `(I: A.I.start, V: vsaptr)`

The V-contiguity condition `V_old == vsaptr` is **not generally true** — it holds only if COPY's insertion VSA happens to land at exactly the V-end of C. This is coincidental, not structural. The systematic coalescence effect described above is exclusive to *intra-loop* span pairs within a single `insertpm` call.

---

### Summary

| Condition | Result |
|-----------|--------|
| Consecutive spans in specset, same source document, I-adjacent | **Coalesced** into one POOM crum — V-alignment is guaranteed by `vsaptr` advancement at [orglinks.c:131] |
| Consecutive spans in specset, different source documents, I-adjacent | **Not coalesced** — homedoc check at [insertnd.c:305] fails first |
| New span I-adjacent to a pre-existing POOM crum | **Not systematically coalesced** — requires V-contiguity too, which is not guaranteed |

`isanextensionnd` tests both I and V dimensions atomically via `lockeq(..., dspsize(POOM))` = `lockeq(..., 2)` [insertnd.c:308, wisp.h:26, wisp.c:263–265]. The VSA-advancement loop in `insertpm` [orglinks.c:131] is precisely what creates automatic V-adjacency between successive spans, making the I-adjacency condition both necessary and sufficient for intra-specset coalescence (same homedoc).
