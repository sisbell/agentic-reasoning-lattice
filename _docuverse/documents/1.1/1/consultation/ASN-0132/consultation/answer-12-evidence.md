## Question 12 [evidence]

> Is there a single shared matching routine over the spanfilade that both the count and the enumeration dispatch through, or does the counting path carry its own copy of the four-set matching logic that could drift from what enumeration applies at the same moment?

## KB Synthesis

There is a single shared routine. No drift is possible.

From [SS-FIND-LINKS] (Finding 0035):

> FINDNUMOFLINKSFROMTOTHREE (opcode 29) is a trivial wrapper around FINDLINKSFROMTOTHREE. It calls `findlinksfromtothreesp()` to materialize the complete linked list of matching links, then walks the list counting elements. There is no count-only optimization.

The count path (`findnumoflinksfromtothreesp`, `spanf1.c:105-115`) calls the full `findlinksfromtothreesp()` search, receives the complete result linked list, and then linearly counts it. It does not reimplement the four-set matching logic — it reuses the exact enumeration result. The counting step is a post-hoc walk over what enumeration already produced.

Consequence: the two opcodes are guaranteed to agree on the matched set at any given instant, because the count is derived from the enumeration output, not computed independently. The only behavioral difference is that the count opcode discards the list after tallying it, while the enumeration opcode returns it.

---

## Code Exploration

---

## Answer: Single Shared Matching Routine — No Drift Possible, With One Suppressed Divergence

There is **one shared matching routine** over the spanfilade. The counting path carries no copy of the matching logic whatsoever. All three protocol operations — enumerate (`findlinksfromtothree`), count (`findnumoflinksfromtothree`), and paginate (`findnextnlinksfromtothree`) — converge on the same function before any endpoint matching begins.

---

### The Call Graph

**Enumerate path** (`fns.c:189`):
```
findlinksfromtothree()           fns.c:189
  dofindlinksfromtothree()       do1.c:348
    findlinksfromtothreesp()     spanf1.c:56   ← shared core
      intersectlinksets()        spanf2.c:46
```

**Count path** (`fns.c:204`):
```
findnumoflinksfromtothree()      fns.c:204
  dofindnumoflinksfromtothree()  do1.c:355
    findnumoflinksfromtothreesp() spanf1.c:105
      findlinksfromtothreesp()   spanf1.c:110  ← same shared core
      for (n=0; linkset; ...)    spanf1.c:112  ← only addition: a counter
```

**Paginate path** (`fns.c:219`):
```
findnextnlinksfromtothree()      fns.c:219
  dofindnextnlinksfromtothree()  do1.c:362
    findnextnlinksfromtothreesp() spanf1.c:117
      findlinksfromtothreesp()   spanf1.c:124  ← same shared core
```

The count's entire body, relative to the shared core, is a single `for` loop that walks the returned linked list and increments a counter:

```c
// spanf1.c:105-115
bool findnumoflinksfromtothreesp(..., INT *numptr)
{
  typelinkset linkset;
  INT n;
        if (!findlinksfromtothreesp (taskptr, spanfptr, fromvspecset, tovspecset,
                                     threevspecset, orglrange, &linkset))
                return(FALSE);
        for (n = 0; linkset; linkset = linkset->next, ++n);
        *numptr = n;
        return (TRUE);
}
```

There is no duplicate matching logic. The count is derived post-hoc from the same list the enumeration would return.

---

### The Matching Logic Lives in Two Places, Both Shared

**`findlinksfromtothreesp` (spanf1.c:56–103)** performs three independent lookups — one per endpoint set — and then intersects:

1. Convert each specset to a sporglset via `specset2sporglset()` [spanf1.c:71–75]
2. For each non-null specset, call `sporglset2linkset()` with its endpoint type constant (`LINKFROMSPAN`, `LINKTOSPAN`, `LINKTHREESPAN`) [spanf1.c:77, 85, 93]
3. Intersect the three resulting linksets via `intersectlinksets()` [spanf1.c:100]

**`intersectlinksets` (spanf2.c:46–120)** is the set-logic core. It handles all cardinality cases:
- Exactly one non-null set → use it directly [spanf2.c:64–71]
- Exactly two → O(n²) pairwise scan [spanf2.c:96–104]
- All three → O(n³) triple scan [spanf2.c:106–118]

```c
// spanf2.c:95-118
if (!linkset3) {
    for (; temp1; temp1 = temp1->next)
        for (temp2 = linkset2; temp2; temp2 = temp2->next)
            if (tumblereq (&temp1->address, &temp2->address)) { ... }
} else {
    for (; temp1; temp1 = temp1->next)
        for (temp2 = linkset2; temp2; temp2 = temp2->next)
            for (temp3 = linkset3; temp3; temp3 = temp3->next)
                if (tumblereq (&temp1->address, &temp2->address)
                    && tumblereq (&temp2->address, &temp3->address)) { ... }
}
```

This code is called once, by `findlinksfromtothreesp`, from which all three protocol operations descend.

---

### One Nominal Divergence That Is Currently Moot

There is one place where count and enumeration differ in what they pass: the `orglrange` / homeset parameter.

- `fns.c:198` (enumerate) passes `(typeispan*)NULL/*homeset*/` — the homeset from the request is explicitly discarded
- `fns.c:213` (count) passes the actual `homeset` from the request

This looks like a potential behavioral divergence: count could apply a home-document filter that enumeration ignores.

**However**, this divergence is currently rendered moot by `sporglset2linkset` at `sporgl.c:227`:

```c
// sporgl.c:227-233
if (TRUE||!homeset) {
    tumblerclear (&nullhomeset.stream);
    tumblerclear (&nullhomeset.width);
    nullhomeset.width.mantissa[0] = 100;
    nullhomeset.next = NULL;
    homeset = &nullhomeset;
}
```

The `TRUE||` short-circuits the actual `!homeset` test, making the branch unconditional. Whatever `orglrange` reaches this function — NULL from the enumerate path, or an actual homeset from the count path — it is always discarded and replaced with a synthetic "everything" range (stream = 0, width = 100). The passed-in homeset never influences the retrieval.

So: **both paths apply identical synthetic filtering**, and the nominal discrepancy at `fns.c` is a dead-code difference. If `TRUE||` were removed, count and enumeration could diverge for queries that supply a homeset constraint — count would filter, enumeration would not.

---

### Summary

| Path | Reaches `findlinksfromtothreesp`? | Own matching copy? |
|------|----------------------------------|-------------------|
| `findlinksfromtothree` (enumerate) | Yes, directly — `do1.c:352` | No |
| `findnumoflinksfromtothree` (count) | Yes, via `findnumoflinksfromtothreesp` — `spanf1.c:110` | No |
| `findnextnlinksfromtothree` (paginate) | Yes, via `findnextnlinksfromtothreesp` — `spanf1.c:124` | No |

There is one shared matching routine. The counting path is a thin wrapper that calls it and counts the list. The matching logic — sporglset expansion, per-endpoint retrieval through `retrieverestricted`, and `intersectlinksets` — cannot drift between count and enumeration because they share a single call site.
