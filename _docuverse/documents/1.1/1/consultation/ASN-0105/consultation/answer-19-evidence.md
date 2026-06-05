## Question 19 [evidence]

> If the read span crosses from the text subspace (`1.x`) into the link subspace (`2.x`), does `retrieverestricted` return link orgl I-addresses intermixed with text, or is there a boundary that halts the read at the subspace transition?

## KB Synthesis

`retrieverestricted` returns link orgl I-addresses intermixed with text — there is no boundary detection or halt at the subspace transition.

**The storage layer is type-agnostic.** `retrieverestricted`, `permute`, and `docopy` operate on V→I mappings uniformly, with no type metadata attached to either the V-position or the I-address [SS-SUBSPACE-CONVENTION, Finding 0009, 0011]. The POOM is a flat multimap of `(V-position, I-address)` entries [SS-POOM-MULTIMAP]. A query spanning `1.x` through `2.x` will accumulate all entries in that range — permascroll I-addresses from `1.x` and link orgl ISAs from `2.x` — in a single unsorted result set.

**No runtime guard exists.** `acceptablevsa()` unconditionally returns TRUE [SS-SUBSPACE-CONVENTION, Finding 0010], and the two-blade knife mechanism that *would* stop the shift region at a subspace boundary [SS-TWO-BLADE-KNIFE] is a construct used only within INSERT's POOM modification path — it is not consulted during reads.

**The consequences are silent and downstream.** If the mixed I-address result is passed to `ispanset2vstuffset` for permascroll content lookup, the link orgl ISAs are not permascroll addresses; the lookup returns NULL or garbage bytes with no error [PRE-RETRIEVE-CONTENTS, Finding 0010]. The `retrieve_vspan` operation on a document with both subspaces returns a meaningless bounding-box width that spans the gap, illustrating that the read boundary is not enforced there either [EC-VSPAN-MISLEADING-SIZE, Finding 0035].

**The correct pattern** — forcing callers to filter to text subspace before retrieval — is a precondition obligation, not an implementation guarantee [PRE-COMPARE-VERSIONS, PRE-RETRIEVE-CONTENTS, INV-SUBSPACE-CONVENTION].

---

## Code Exploration

---

## Answer: `retrieverestricted` Has No Subspace Boundary — Returns Both Subspaces Intermixed

### The Subspace Layout

The document V-address space has two distinct subspaces, distinguished by the leading tumbler digit:

**Text subspace (1.x):** V-addresses with first mantissa digit = 1. When the first text is appended, `findvsatoappend` [orglinks.c:42-43] assigns the address 1.1:
```c
tumblerincrement (vsaptr, 0, 1, vsaptr); /* sets mantissa[0]=1 */
tumblerincrement (vsaptr, 1, 1, vsaptr); /* appends .1 */
```

**Link subspace (2.x):** V-addresses with first mantissa digit = 2, starting at 2.1. `findnextlinkvsa` [do2.c:156-158] establishes this floor:
```c
tumblerincrement (&firstlink, 0, 2, &firstlink); /* = 2 */
tumblerincrement (&firstlink, 1, 1, &firstlink); /* = 2.1 */
```

`findvsatoappend` [orglinks.c:37] further uses `linkspacevstart = 2.0` as the explicit subspace boundary: if `reach.dsas[V] >= 2.0`, the document already has link content in the 2.x range.

`setlinkvsas` [do2.c:169-176] confirms: within a link orgl's internal POOM, from-end-sets are stored at 1.1, to-end-sets at 2.1.

---

### The Call Chain: No Boundary Check Exists

`retrieverestricted` [retrie.c:56-85] accepts two spans and a document ISA, converts them to tumbler start/end pairs, and calls `retrieveinarea`:

```c
typecontext *retrieverestricted(typecuc *fullcrumptr, typespan *span1ptr, INT index1,
                                typespan *span2ptr,   INT index2, typeisa *docisaptr)
{
    ...
    movetumbler (&span1ptr->stream, &span1start);
    tumbleradd  (&span1start, &span1ptr->width, &span1end);
    ...
    temp = retrieveinarea (fullcrumptr, &span1start, &span1end, index1, ...);
```

No subspace inspection occurs here.

`retrieveinarea` [retrie.c:87-110] dispatches to `findcbcinarea2d` for SPAN/POOM enfilades. No subspace check.

`findcbcinarea2d` [retrie.c:229-268] walks the crum tree, calling `crumqualifies2d` on each node, collecting all bottom crums that qualify:

```c
for (; crumptr; crumptr = getrightbro (crumptr)) {
    if (!crumqualifies2d (crumptr, offsetptr, span1start, span1end, index1,
                          span2start, span2end, index2, infoptr))
        continue;
    if (crumptr->height != 0)
        findcbcinarea2d (findleftson (...), &localoffset, ...);
    else {
        context = makecontextfromcbc ((typecbc*)crumptr, (typewid*)offsetptr);
        incontextlistnd (headptr, context, index1);
    }
}
```

`crumqualifies2d` [retrie.c:270-305] tests whether the crum's range intersects the requested 2D area. The V-dimension check reduces to `whereoncrum` calls:

```c
endcmp   = iszerotumbler(span1end) ? TOMYRIGHT : whereoncrum(crumptr, offset, span1end,   index1);
startcmp = whereoncrum(crumptr, offset, span1start, index1);
```

`whereoncrum` [retrie.c:345-398] computes `left = offset + cdsp` and `right = left + width`, then returns `THRUME` if `address < right` and `startcmp <= THRUME`. The comparison is `tumblercmp` — a pure numerical total order on tumblers [tumble.c:72-85]:

```c
if (aptr->sign == bptr->sign)
    return (aptr->sign ? abscmp(bptr,aptr) : abscmp(aptr,bptr));
```

`abscmp` [tumble.c:87-111] compares `exp` field first, then mantissa digits lexicographically. There is no subspace-discriminating logic anywhere in this chain. A crum at V=1.8 and a crum at V=2.2 are both tested identically against a requested range [1.5, 2.3].

**Result:** `findcbcinarea2d` collects I-addresses for all crums whose V-range intersects the requested span, regardless of whether they are in the 1.x text subspace or the 2.x link subspace. These are inserted into the context list via `incontextlistnd` [retrie.c:263], ordered by their I-address. There is no halt, no filter, no discontinuity at the 1.x/2.x boundary inside `retrieverestricted`.

---

### How Callers Handle This

`span2spanset` [orglinks.c:425-454] — the primary caller of `retrieverestricted` during V→I conversion — simply passes the V-span through:

```c
context = retrieverestricted((typecuc*)orgl, restrictionspanptr, restrictionindex,
                              (typespan*)NULL, targindex, (typeisa*)NULL);
for (c = context; c; c = c->nextcontext) {
    context2span (c, restrictionspanptr, restrictionindex, &foundspan, targindex);
    nextptr = (typespan*)onitemlist (taskptr, (typeitem*)&foundspan, (typeitemset*)targspansetptr);
}
```

No subspace filtering here either.

The only subspace-aware guard in the entire codebase is `filter_vspanset_to_text_subspace` [do1.c:386-411], added explicitly after the fact, which keeps only V-spans with `stream >= 1.0`:

```c
tumblerclear(&text_subspace_start);
tumblerincrement(&text_subspace_start, 0, 1, &text_subspace_start);
for (; vspanset; vspanset = vspanset->next) {
    if (tumblercmp(&vspanset->stream, &text_subspace_start) >= EQUAL) {
        /* keep */ ...
    }
    /* else: skip — link subspace */
}
```

This is called only by `doshowrelationof2versions` [do1.c:440-441], with a comment crediting Bug 009. It is not wired into the V→I retrieval path.

---

### Conclusion

**`retrieverestricted` returns link orgl I-addresses intermixed with text.** No code in `retrieverestricted`, `retrieveinarea`, `findcbcinarea2d`, `crumqualifies2d`, or `whereoncrum` tests for subspace. The V-space is treated as a flat, totally-ordered tumbler space. A span crossing from 1.x into 2.x will match all crums — text and link alike — whose V-range intersects the requested interval, returning their I-addresses in a single context list ordered by I-address. Subspace discrimination is entirely the caller's responsibility, and based on the code, only `doshowrelationof2versions` currently exercises that discipline.
