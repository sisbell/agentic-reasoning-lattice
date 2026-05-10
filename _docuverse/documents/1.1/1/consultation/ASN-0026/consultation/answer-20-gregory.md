## Question 20 [gregory]

> Is there a mechanism that detects or prevents a POOM from containing two entries whose I-address ranges overlap — for example, if COPY transcludes content that partially overlaps with content already present in the target document at different V-positions?

## KB Synthesis

There is no mechanism — neither detection nor prevention — for overlapping I-address ranges in the POOM. The KB is explicit on all relevant points.

## The POOM is designed to hold overlapping I-ranges

[SS-POOM-MULTIMAP] establishes that the POOM is explicitly a **multimap**: "a single I-address can map to multiple V-positions within the same document." The search algorithm `findcbcinarea2d()` accumulates *all* matching contexts via `incontextlistnd()`, never replacing existing entries. This is the fundamental mechanism for transclusion.

[EC-SELF-TRANSCLUSION] confirms vcopy within the same document creates exactly this state — the same I-addresses at multiple V-positions — and treats it as correct behavior. [ST-VCOPY] (Finding 0039) verifies pairwise comparisons among three positions sharing one I-address all report shared content. There is no cardinality constraint on how many V-positions can reference the same I-address.

## COPY performs no overlap checking

[PRE-COPY] is explicit:

> The COPY operation performs NO duplicate checking before inserting V→I mappings into the target document's POOM. `isanextensionnd()` checks only whether the new content is contiguous with an existing crum — never whether the I-address already exists in the target. A COPY of I-addresses that already exist at some V-position in the target document is unconditionally accepted.

The only check `isanextensionnd()` performs is for *contiguity* (enabling crum extension rather than creation of a new crum). Overlap is not checked and not rejected.

## The "bijection" invariant does not guard against this

[INV-POOM-BIJECTIVITY] describes I₁ as a bijection between V-addresses and I-addresses, but the violation it documents is DELETE producing *negative V-positions* — not overlapping I-ranges. The multimap structure from [SS-POOM-MULTIMAP] makes clear that the I→V direction is deliberately not injective; the functional constraint (each V-position maps to exactly one I-address) runs V→I only.

## Summary

The scenario in the question — COPY of content that partially overlaps existing content at different V-positions — is precisely what transclusion does, and the POOM is structurally designed to accommodate it. No assertion, validation, or structural constraint exists to detect or reject it. The closest observable effect is that `ispan2vspanset` returns a set of multiple V-spans for the overlapping I-range [SS-POOM-MULTIMAP], but this is the correct query result, not an error signal.

---

## Code Exploration

All citations confirmed. Here is the full technical answer.

---

## POOM I-Address Overlap Detection in udanax-green

**Short answer: There is no such mechanism. The backend trusts callers to never produce overlapping I-spans. Overlapping inserts would silently create a corrupted POOM.**

---

### The Validation Hook That Does Nothing

`acceptablevsa()` is the designated gate in `docopy`:

```c
// do2.c:110-113
bool acceptablevsa(tumbler *vsaptr, typeorgl orglptr)
{
    return (TRUE);
}
```

It is the only place in the COPY call chain where such a check could plausibly occur. It is completely vacuous — no examination of the existing POOM contents, no comparison against any span.

It is called at `do1.c:56`, between resolving the target POOM (`findorgl`) and performing the actual insertion (`insertpm`). The slot exists; the body is empty.

---

### The COPY Call Chain

`docopy` [do1.c:45-65]:

```c
return (
   specset2ispanset (taskptr, specset, &ispanset, NOBERTREQUIRED)   // convert spec→I-spans
&& findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)        // locate target POOM
&& acceptablevsa (vsaptr, docorgl)                                  // ← always TRUE
&& asserttreeisok(docorgl)
&& insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset)         // insert into POOM
&&  insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN)     // insert into spanfilade
&& asserttreeisok(docorgl)
);
```

`asserttreeisok` checks structural tree integrity (node heights, sibling pointers) — not semantic invariants about I-span ranges.

---

### `insertpm` — No I-Span Comparison

`insertpm` [orglinks.c:75-134] iterates over the incoming sporglset, builds `crumorigin`/`crumwidth` with the I-stream address on the I-axis and the V-address on the V-axis, then calls `insertnd` [orglinks.c:130]:

```c
// orglinks.c:100-131
for (; sporglset; sporglset = (typesporglset) sporglset->xxxxsporgl.next) {
    unpacksporgl (sporglset, &lstream, &lwidth, &linfo);
    movetumbler (&lstream, &crumorigin.dsas[I]);     // I-axis origin
    movetumbler (&lwidth,  &crumwidth.dsas[I]);      // I-axis width
    movetumbler (vsaptr,   &crumorigin.dsas[V]);     // V-axis origin
    ...
    insertnd (taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);
    tumbleradd (vsaptr, &crumwidth.dsas[V], vsaptr);
}
```

There is no query of existing crums' I-axis ranges at any point here.

---

### `insertnd` → `makegappm` — V-Axis Gap Only

`makegappm` [insertnd.c:124-172] is the function that shifts existing content to make room for an insertion. The guard at lines 140–143:

```c
if (iszerotumbler (&fullcrumptr->cwid.dsas[V])
|| tumblercmp (&origin->dsas[V], &grasp.dsas[V]) == LESS
|| tumblercmp (&origin->dsas[V], &reach.dsas[V]) != LESS)
    return(0);    /* this if for extensions to bc without calling cut*/
```

This only checks the **V-axis** — whether the V-insertion point falls inside the existing tree's V-range. It adjusts V-displacements of existing crums [lines 161-164] so that they slide right to accommodate the new entry. It does not look at the I-axis at all, because V-axis gap-making and I-axis content identity are independent concerns.

---

### `insertcbcnd` — Adjacency Check, Not Overlap Check

At the bottom level [insertnd.c:242-309], `insertcbcnd` iterates existing crums and calls `isanextensionnd`:

```c
// insertnd.c:249-258
for (ptr = findleftson (father); ptr; ptr = findrightbro (ptr)) {
    if (isanextensionnd ((typecbc*)ptr, grasp, origin, infoptr)) {
        dspadd (&ptr->cwid, width, &ptr->cwid, (INT)father->cenftype);  // widen crum
        ...
        return(...);
    }
}
// else: fall through and create a new crum
```

```c
// insertnd.c:301-309
bool isanextensionnd(typecbc *ptr, typedsp *offsetptr, typedsp *originptr, type2dbottomcruminfo *infoptr)
{
  typedsp grasp, reach;
  bool lockeq();
    if (!tumblereq (&infoptr->homedoc, &((type2dcbc *)ptr)->c2dinfo.homedoc))
        return (FALSE);
    prologuend ((typecorecrum*)ptr, offsetptr, &grasp, &reach);
    return (lockeq (reach.dsas, originptr->dsas, (unsigned)dspsize(ptr->cenftype)));
}
```

`isanextensionnd` checks: does the incoming span's **origin exactly equal** the existing crum's right boundary (`reach`)? If yes, widen that crum. If no, fall through and create a new crum.

This is a **coalescence optimization**, not an overlap check. If the incoming I-span's origin falls *within* an existing crum's I-range rather than at its right edge, `isanextensionnd` returns FALSE, a new crum is created without complaint, and the POOM now contains two crums with overlapping I-addresses.

---

### THRUME — Not an Overlap Guard

`makegappm` treats a `THRUME` return from `insertcutsectionnd` as a fatal error [insertnd.c:157-159]:

```c
case -1:      /* THRUME*/
    dump(ptr);
    gerror ("makegappm can't classify crum\n");
```

`insertcutsectionnd` returns -1 when a V-axis cut lands exactly on a crum boundary [edit.c:~221-224]. This is a V-axis structural anomaly during gap-making — not an I-axis overlap detection.

---

### Summary

| Function | File | I-overlap check? | What it actually validates |
|---|---|---|---|
| `acceptablevsa()` | do2.c:110 | **None** — always `TRUE` | Nothing |
| `insertpm()` | orglinks.c:75 | **None** | VSA not zero/negative |
| `makegappm()` | insertnd.c:124 | **None** | V-axis insertion point in range |
| `isanextensionnd()` | insertnd.c:301 | **None** | Exact adjacency at right boundary |
| `insertcbcnd()` | insertnd.c:242 | **None** | Crum not zero-width |
| `insertspanf()` | spanf1.c:15 | **None** | None |
| `asserttreeisok()` | (debug) | **None** | Tree height/structure consistency |

**No function in the COPY path reads existing I-span ranges from the POOM and compares them against the incoming I-span.**

---

### Architectural Implication

The POOM is a 2D enfilade. `insertpm` inserts crums keyed by `(V-address, I-address)` pairs. The V-axis is managed carefully — `makegappm` shifts existing crums to keep V-addresses consistent after each insert. The I-axis is treated as **read-only metadata** attached to each crum: the backend records *which* I-content lives *where* in V-space, but it never cross-checks the I-addresses of distinct crums against each other.

The invariant "no two POOM entries share any I-address" is therefore a **pre-condition that callers must enforce**, not a post-condition the backend verifies. If a COPY operation transcludes an I-span that partially overlaps content already present in the POOM at different V-positions, the backend will silently insert a new crum with that overlapping I-span. The structural tree operations will succeed; the semantic corruption will be undetected.
