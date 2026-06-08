## Question 14 [evidence]

> When a left-shift via `tumblersub` produces a negative V-position, does that entry sort before all positive entries in `tumblercmp`, and does the POOM continue to function for retrieval despite violating the expected bijectivity invariant?

## KB Synthesis

Yes to both, with an important nuance on which entries can actually go negative.

## Ordering of negative V-positions

[SS-TUMBLER / Finding 0053] is explicit: `tumblercmp` uses sign-magnitude representation with a simple sign check first. A negative tumbler compares as `LESS` against all positive tumblers and zero, regardless of magnitude. So a V-position of -0.8 sorts before V=0, before V=1.1, before V=2.1 — before every valid V-address in the document. Within the negative class, larger absolute value is "more negative" and sorts lower still.

## POOM behavior with a negative-V entry

The POOM continues to function correctly for all non-negative V-addresses. The negative-V entry is invisible to retrieval, not corrupting to it.

The mechanism: `whereoncrum` and `intervalcmp` compare the query start against the crum's grasp and reach. Any valid V-range query has a non-negative start. A crum with a negative displacement will always classify as `TOMYLEFT` relative to any positive query boundary. The B-tree traversal therefore skips it without error — the entry occupies tree space and costs some traversal overhead, but is never included in a result set.

[INV-POOM-BIJECTIVITY / Finding 0053] captures the formal consequence: the I₁ bijection invariant weakens to apply only over non-negative V-addresses. The negative-V crum represents leaked state — exists in the tree, unreachable by V-space queries, and (crucially) unreachable by a subsequent `DELETEVSPAN` call since that requires a positive-valued target span.

## Critical scope limitation from Finding 0055

The scenario where this arises is narrower than Finding 0053 initially implied. [SS-TUMBLER / Finding 0055] establishes that `strongsub` has an exponent guard: when the subtrahend's exponent is strictly less than the minuend's exponent, the function returns the minuend unchanged.

For the canonical concern — DELETE at 1.x shifting link entries at 2.x — the deletion width (exp≈-1) is less than the link displacement exponent (exp=0), so `strongsub` is a no-op. [FC-SUBSPACE / Finding 0055] and [INT-DELETE-SUBSPACE-ASYMMETRY] both confirm: link V-positions survive intact. Negative V-positions from DELETE can only arise when both the deletion width and the target entry's displacement share the same exponent and the deletion width exceeds the entry's displacement — a same-subspace-only hazard.

---

## Code Exploration

Now I have enough to trace the complete execution path. Let me give the full answer.

---

## Answer: Negative V-Position from `tumblersub`, Sorting, and POOM Retrieval

### 1. How `tumblersub` Produces a Negative V-Position

`tumblersub` [tumble.c:406–440]:

```c
} else if (iszerotumbler (aptr)) {
    movetumbler (bptr, cptr);
    cptr->sign = !cptr->sign;          // zero - b → negative b
} else {
    movetumbler (bptr, &temp);
    temp.sign = !temp.sign;
    tumbleradd (aptr, &temp, cptr);    // a + (-b)
}
tumblerjustify (cptr);
```

When `a < b` (neither zero), `functiontumbleradd` [tumble.c:302–325] takes the else branch: `abscmp(a, b)` is not `GREATER`, so `weaksub(b, a, cptr)` runs and `cptr->sign = bptr->sign`. Since `bptr` had its sign flipped before the call (`temp.sign = !temp.sign`), the output carries `sign = 1`. The mantissa digits themselves remain non-negative—the sign is a separate flag, not two's complement.

**The commented debug trace in `tumblersub` [tumble.c:408–413] was explicitly watching for this:**
```c
/*
    if (cptr->sign) {
        fprintf(stderr,"TUMBLERSUB NEGATIVE OUTPUT\n");
```
The comment proves the authors knew this could occur.

---

### 2. The Specific Left-Shift Path That Can Produce It

In `deletend` [edit.c:62–65]:

```c
case 2:
    tumblersub (&ptr->cdsp.dsas[index], width, &ptr->cdsp.dsas[index]);
    /* This will get set to modified in setwisp */
    break;
```

Case 2 is returned by `deletecutsectionnd` [edit.c:235–248] when the deletion blade `blades[1]` (= `origin + width`) is at or to the left of the crum's left boundary—meaning the crum sits entirely to the right of the deleted span, and must shift left.

**The crum's `cdsp.dsas[V]` is a RELATIVE displacement from its parent's absolute V-position.** The crum's absolute V-start = `fgrasp.dsas[V] + ptr->cdsp.dsas[V]`. The absolute value must be ≥ `origin + width`, but `ptr->cdsp.dsas[V]` alone can be smaller than `width` if the parent's absolute position (`fgrasp.dsas[V]`) accounts for most of that distance. In that case:

```
ptr->cdsp.dsas[V] - width < 0
```

and `tumblersub` sets `sign = 1` on the stored relative displacement, while the absolute V-position of the crum remains positive. The representation invariant (`cdsp` should be non-negative) is violated; the semantic invariant (absolute V-positions are positive and non-overlapping) is not—yet.

The same can happen in `rearrangend` [edit.c:124–127] when `diff[2]` is negative (explicitly commented at edit.c:179: `/* should be negative */`), and `tumbleradd` of a negative diff drives a small relative `cdsp` below zero.

---

### 3. How `tumblercmp` Sorts a Negative V-Position

`tumblercmp` [tumble.c:73–80]:

```c
INT tumblercmp(tumbler *aptr, tumbler *bptr)
{
    if (iszerotumbler(aptr)){
        if (iszerotumbler(bptr))  return (EQUAL);
        else                      return (bptr->sign ? GREATER : LESS);
    }
    if (iszerotumbler(bptr))
        return (aptr->sign ? LESS : GREATER);
    if (aptr->sign == bptr->sign)
        return (aptr->sign ? abscmp(bptr,aptr) : abscmp(aptr,bptr));
    return (aptr->sign ? LESS : GREATER);   // ← key line
}
```

The final `return` handles the mixed-sign case. When `a` is negative (`aptr->sign == 1`) and `b` is positive (`bptr->sign == 0`): returns `LESS`. When two negatives are compared (both `sign == 1`), arguments to `abscmp` are **reversed** (`abscmp(bptr, aptr)` instead of `abscmp(aptr, bptr)`), so -5 < -3, consistent with real arithmetic.

**The total order is: negative < zero < positive.** An entry with a negative `cdsp.dsas[V]` will sort before all positive-valued tumblers and before zero.

---

### 4. Does the POOM Continue to Function for Retrieval?

The retrieval path for POOM is: `doretrievev` → `ispan2vspanset` → `permute` → `span2spanset` → `retrieverestricted` → `retrieveinarea` → `findcbcinarea2d` → `crumqualifies2d` → `whereoncrum`.

The decisive code is in `whereoncrum` [retrie.c:361–389]:

```c
case POOM:
    tumbleradd(&offset->dsas[index], &ptr->cdsp.dsas[index], &left);
    cmp = tumblercmp(address, &left);
    ...
    tumbleradd (&left, &ptr->cwid.dsas[index], &right);
    cmp = tumblercmp(address, &right);
    ...
```

When `ptr->cdsp.dsas[V]` is negative (`sign = 1`) and `offset->dsas[V]` is positive, `tumbleradd` handles mixed signs via `functiontumbleradd` [tumble.c:295–340]:

```c
} else if (abscmp (aptr, bptr) == GREATER) {
    strongsub (aptr, bptr, cptr);
    cptr->sign = aptr->sign;           // result positive if |offset| > |cdsp|
} else {
    weaksub (bptr, aptr, cptr);
    cptr->sign = bptr->sign;           // result negative if |offset| < |cdsp|
}
```

As long as `|parent_absolute|` > `|cdsp|` (which holds as long as the absolute V-position is still positive), `left` is computed correctly as a positive tumbler. The interval-overlap tests in `crumqualifies2d` then work correctly.

**The POOM continues to function for retrieval, conditionally.** The crum is found at the correct absolute V-position because `tumbleradd` on the traversal path reconstructs the right absolute address from the signed relative `cdsp`. The `findcbcinarea2d` traversal [retrie.c:258–296] does not assume sorted sibling order—it checks every sibling via `crumqualifies2d`—so no crum is skipped due to ordering anomalies.

---

### 5. Limits: When It Breaks

The tolerance ends if the absolute V-position itself goes negative. If `|parent_absolute| < |cdsp|`, `tumbleradd` produces a negative `left`, and `tumblercmp` will classify it as less than any positive query address. The crum becomes permanently invisible to any positive-valued retrieval query.

`insertpm` [orglinks.c:70–82] has a hard guard against this at insertion time:

```c
if (tumblercmp (vsaptr, &zero) == LESS)
#ifndef DISTRIBUTION
    gerror ("insertpm called with negative vsa.\n");
```

But no equivalent guard exists on the `tumblersub` in `deletend` [edit.c:63] or in `setwispupwards`/`recombine` [edit.c:74–75] that runs immediately after.

In debug builds (`#ifndef DISTRIBUTION`), `tumblercheckptr` [tumble.c:149–200] would catch the negative `cdsp` digit:

```c
for (i = 0; i < NPLACES; ++i){
    if ((INT)(ptr->mantissa[i]) < 0){
        fprintf(stderr,"negative digit");
        wrong = TRUE;
    }
}
```

But in `DISTRIBUTION` mode the check is absent and the tree silently carries the violated invariant.

---

### Summary

| Question | Answer | Primary Citation |
|---|---|---|
| Does `tumblersub` produce negative V-positions? | Yes, when `a < b`: sets `sign=1` on result | tumble.c:406–440 |
| Which call path causes it in the POOM? | `deletend` case 2: `tumblersub(&ptr->cdsp.dsas[V], width, ...)` on a child with small relative displacement | edit.c:63 |
| How does `tumblercmp` sort a negative V-position? | Before zero and all positives; `return (aptr->sign ? LESS : GREATER)` at the mixed-sign branch | tumble.c:79 |
| Does POOM retrieval survive the violation? | Yes—conditionally. `whereoncrum` calls `tumbleradd(offset, cdsp)` which correctly handles signed relative displacements, computing the right absolute V-start | retrie.c:366 |
| Is bijectivity preserved? | At the absolute level yes (no overlapping absolute spans). At the representation level no (`cdsp < 0` violates the invariant). If the absolute position itself goes negative, the crum becomes unreachable. | tumble.c:149–200, orglinks.c:70–82 |
