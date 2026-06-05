## Question 20 [evidence]

> If the document's POOM contains a negative V-position from a prior DELETE shift, how does that fragment sort and appear within the ordered multi-span result relative to positive-V fragments?

## KB Synthesis

A POOM entry with a negative V-position, if found during an I-space–driven retrieval (e.g., FOLLOWLINK's `ispan2vspanset` path), sorts to the **head** of the ordered multi-span result — before every positive-V fragment.

**Why it sorts first:**
`incontextlistnd()` builds the result list by insertion-sort on `totaloffset.dsas[V]` (the left V-boundary) [INV-RETRIEVAL-V-SORTED]. The comparison uses `tumblercmp`, which classifies negative tumblers as strictly `LESS` than zero and all positive tumblers, regardless of magnitude [SS-TUMBLER Finding 0053]:

```
tumblercmp(-0.8, 0.0)  → LESS
tumblercmp(-0.8, 1.1)  → LESS
tumblercmp(-0.8, -0.3) → GREATER  (larger magnitude = more negative)
```

So a negative-V context is always inserted at or near the front of the accumulation list.

**Whether it appears at all:**
The POOM crum with a negative displacement physically remains in the tree — `deletend` Case 2 (`tumblersub` via `strongsub`) silently stores the negative result without removing the entry [SS-TUMBLER Finding 0053, INV-POOM-BIJECTIVITY]. When `findcbcinarea2d` traverses the POOM on an I-space restriction query, it can reach this crum. `incontextlistnd` then places it first.

**Practical effect:**
Any I→V conversion that hits this crum returns a span with a negative start address. Since normal V-space queries use positive ranges, this fragment is invisible to V-range–driven searches — but it surfaces as an anomalous head entry in I-space–driven retrievals (FOLLOWLINK, RETRIEVEENDSETS), yielding a specset whose first span has an invalid (negative) V-address [EC-DEEPLY-ORPHANED-LINK Finding 0053, INV-POOM-BIJECTIVITY].

---

## Code Exploration

I've read all the relevant source files. Let me compile the verified answer.

---

## Answer: Negative V-Position Fragments in Ordered Multi-Span Results

### How DELETE Shifts Produce Negative V-Positions

`deletend` in `edit.c:31–76` processes a DELETE by calling `makecutsnd` to cut the POOM tree at the deletion boundaries, then classifying each child crum via `deletecutsectionnd`. Case 2 covers crums whose content lies entirely to the **right** of the deleted range — they must shift leftward in V-space:

```c
// edit.c:62-64
case 2:
    tumblersub (&ptr->cdsp.dsas[index], width, &ptr->cdsp.dsas[index]);
    /* This will get set to modified in setwisp */
    break;
```

`tumblersub(a, b, c)` computes `c = a - b` [tumble.c:406–430]:

```c
} else {
    movetumbler (bptr, &temp);
    temp.sign = !temp.sign;     // negate b → -b
    tumbleradd (aptr, &temp, cptr);  // a + (-b) = a - b
}
```

When the crum's local V-displacement (`cdsp.dsas[V]`) is **smaller than** the deletion `width`, `tumbleradd` of a positive `a` and a larger-magnitude negative `-b` produces a negative result: the `sign` flag is set to `1` on the output tumbler. The commented-out debug code [tumble.c:432–438] shows the developers tracked these negative outputs during development:

```c
/*
    if (cptr->sign) {
        fprintf(stderr,"TUMBLERSUB NEGATIVE OUTPUT\n");
```

Negative tumblers are valid representations — `tumblercheckptr` [tumble.c:180] only rejects **negative zero** (`sign=1, mantissa[0]=0`), not arbitrary negatives.

---

### How V-Positions Propagate Into Retrieved Contexts

`makecontextfromcbc` [context.c:151–174] constructs a context from a leaf crum by accumulating displacements:

```c
// context.c:167
if (crumptr->cenftype != GRAN)
    dspadd(&context->totaloffset, &crumptr->cdsp, &context->totaloffset, (INT)crumptr->cenftype);
```

If `cdsp.dsas[V]` is negative from the delete shift, this carries through into `context->totaloffset.dsas[V]` — the context's absolute V-start.

---

### The Sorting Mechanism

`findcbcinarea2d` [retrie.c:229–268] is the core multi-span retrieval loop. When it finds a qualifying leaf, it calls:

```c
// retrie.c:262-263
context = makecontextfromcbc ((typecbc*)crumptr, (typewid*)offsetptr);
incontextlistnd (headptr, context, index1);
```

`incontextlistnd` [context.c:75–111] inserts each new context into a linked list sorted by V-position:

```c
// context.c:80-93
prologuecontextnd (c, &grasp, (typedsp*)NULL);  // → grasp = c's totaloffset
...
if (whereoncontext (clist, &grasp.dsas[index], index) < THRUME) {
    c->nextcontext = clist;
    *clistptr = c;       // Insert at BEGINNING
    return(0);
}
```

`whereoncontext` [context.c:124–148] calls `intervalcmp` [tumble.c:144–160], which calls `tumblercmp` [tumble.c:72–85]:

```c
// tumble.c:82-84
if (aptr->sign == bptr->sign)
    return (aptr->sign ? abscmp(bptr,aptr) : abscmp(aptr,bptr));
return (aptr->sign ? LESS : GREATER);   // ← KEY LINE
```

When comparing a **negative** V-address (`sign=1`) against any **positive** bound (`sign=0`), `tumblercmp` returns `LESS` unconditionally — no magnitude comparison. `intervalcmp` then returns `TOMYLEFT`. Since `TOMYLEFT < THRUME`, the condition at `context.c:90` fires and the negative-V context is inserted at the **head** of the list.

---

### Conclusion

A fragment whose POOM V-position has been shifted negative by a DELETE operation **sorts before all positive-V fragments** in the ordered multi-span result. It will appear at the beginning of the retrieved context list. The mechanism is entirely in signed tumbler comparison: `tumblercmp` returns `LESS` for any negative tumbler vs. any positive tumbler [tumble.c:84], `intervalcmp` maps this to `TOMYLEFT` [tumble.c:149–150], and `incontextlistnd` places the fragment at the list head [context.c:90–94].

This means such a fragment represents content whose virtual address has drifted below the document origin — a valid but semantically anomalous state, invisible to the comparison machinery which simply treats it as numerically smallest. There is no guard or clamping: if `cdsp - width < 0` at [edit.c:63], the negative value is stored, propagated, and sorted faithfully as less than zero.
