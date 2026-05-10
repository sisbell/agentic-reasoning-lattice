## Question 12 [gregory]

> When `strongsub` returns its input unchanged due to the exponent guard, what does that imply about the algebraic closure of span difference — can subtracting one span's width from another's start position fail to produce a meaningful displacement?

## KB Synthesis

The exponent guard in `strongsub` means span difference is **not algebraically closed** — the operation silently degenerates to identity rather than producing a displacement when operand exponents don't match.

Here's what the code actually does:

```c
// strongsub(a, b, c): computes c = a - b
if (bptr->exp < aptr->exp) {
    movetumbler(aptr, cptr);  // c = a, unchanged
    return(0);
}
// otherwise, proceed with actual subtraction
```

So `strongsub(a, b)` returns `a` — not `a - b`, not zero, not an error — whenever `b.exp < a.exp`. [SS-TUMBLER Finding 0055]

**The algebraic consequence:** Span displacement is only meaningful within an exponent class. When you compute "shifted position = old_position - deletion_width", the subtraction is a genuine displacement only when `deletion_width.exp >= old_position.exp`. When the width lives at a lower exponent (finer granularity) than the position, the result is the original position, as if no deletion occurred.

This is exactly what happens with subspace isolation in DELETE [FC-SUBSPACE Finding 0055]:

- Text content at V-displacement `0.4` (exp=-1)
- Link content at V-displacement `2.1` (exp=0)  
- Deletion width `0.3` (exp=-1)

For text: `strongsub(0.4, 0.3)` — exponents match, subtraction proceeds, yields `0.1`. Meaningful displacement.

For links: `strongsub(2.1, 0.3)` — `0.3.exp(-1) < 2.1.exp(0)`, guard fires, returns `2.1`. Not a displacement — identity.

**The deeper problem:** This makes span algebra contextually valid only within a single exponent level. If you have a span at position `1.x` (exp=-1) and try to subtract a width computed in a different exponent class, the arithmetic silently does nothing rather than flagging a type mismatch. The system doesn't distinguish between "these operands are incompatible" and "the subtraction produced the original value." [INT-DELETE-SUBSPACE-ASYMMETRY]

Compare this to INSERT's approach [SS-TWO-BLADE-KNIFE Finding 0054]: INSERT explicitly computes a second knife blade at the subspace boundary `(N+1).1`, using structural geometry to exclude cross-subspace entries from the shift region before any arithmetic occurs. DELETE has no such guard — it relies on the arithmetic failing silently at the exponent boundary.

The practical implication for the spec: you cannot reason about `tumblersub(start, width)` producing a "displacement" without also knowing that `start.exp >= width.exp`. When this condition fails, the operation is a no-op that looks like success. Any formal model of DELETE's postcondition must be qualified: `entry.vpos' = entry.vpos - width` holds only when `entry.vpos.exp = width.exp`; otherwise `entry.vpos' = entry.vpos` [ST-DELETE Finding 0055].

The closure property you'd expect — that subtracting any valid width from any valid position yields the position minus that width — does not hold across the tumbler type. Span difference is a partial function whose domain is restricted to same-exponent operands.

---

## Code Exploration

Now I have everything I need. Here is the full analysis.

---

## `strongsub` Exponent Guard and Algebraic Closure of Span Difference

### The Exponent Guard — Exact Code

`strongsub` is defined at `backend/tumble.c:534`:

```c
int strongsub(tumbler *aptr, tumbler *bptr, tumbler *cptr)
{
  tumbler answer;
  register INT i, j;

    tumblerclear(&answer);
    if (tumblereq (aptr, bptr)) {
        movetumbler (&answer, cptr);   // return zero
        return(0);
    }
    if (bptr->exp < aptr->exp) {        // <<< THE EXPONENT GUARD
        movetumbler(aptr,cptr);         // return aptr UNCHANGED
        return(0);
    }
    ...
```

The guard fires when `bptr->exp < aptr->exp` — i.e., when `b` is expressed at a **finer hierarchical depth level** than `a`. The result is that `cptr` receives `aptr`'s value unchanged. No error is raised. The subtraction silently does nothing.

---

### What `exp` Means

The tumbler struct is declared in `backend/common.h:59–65`:

```c
typedef struct structtumbler {
    humber xvartumbler;
    char varandnotfixed;
    char sign  BIT;
    short exp;
    tdigit mantissa[NPLACES];  // NPLACES == 16
} tumbler;
```

`tumblercheckptr` at `backend/tumble.c:174` treats `exp > 0` as invalid — so `exp` is always ≤ 0. `tumblerjustify` at `tumble.c:289–313` normalizes a tumbler by left-shifting leading zeros and decrementing `exp` accordingly. The effect: a more-negative `exp` means the first mantissa digit occupies a finer (deeper) hierarchical position in the address tree.

`tumblerlength` at `tumble.c:259–262` confirms this:

```c
INT tumblerlength(tumbler *tumblerptr) {
    return (nstories (tumblerptr) - tumblerptr->exp);
}
```

Since `exp ≤ 0`, length grows with more-negative `exp`.

---

### How the Guard Is Reached: `abscmp` Drives `strongsub`

`strongsub` is called only from `functiontumbleradd` at `tumble.c:384–386`:

```c
} else if (abscmp (aptr, bptr) == GREATER) {
    strongsub (aptr, bptr, cptr);
    cptr->sign = aptr->sign;
```

`abscmp` at `tumble.c:87–111` checks `exp` **first**:

```c
static INT abscmp(tumbler *aptr, tumbler *bptr)
{
    if (aptr->exp != bptr->exp) {
        if (aptr->exp < bptr->exp) {
            return(LESS);
        } else {
            return(GREATER);   // aptr->exp > bptr->exp => aptr is COARSER
        }
    } else {
        // compare mantissas digit by digit
    }
    return (EQUAL);
}
```

Because exp ≤ 0, "`aptr->exp > bptr->exp`" means `aptr` is at a **coarser** hierarchical level (less-negative exp). When `abscmp` returns `GREATER` based solely on the exponent comparison, it means `a` is defined at a coarser level than `b`. This is exactly when `strongsub` is called — and then at `tumble.c:544`, `bptr->exp < aptr->exp` is true, so the guard fires immediately.

**The exponent guard is the direct consequence of `abscmp`'s exponent-first ordering.** They are two halves of the same implicit assumption: when `a` is coarser-grained than `b`, the system considers `a > b` in magnitude, calls `strongsub`, and `strongsub` immediately bails out by returning `a`.

---

### What `strongsub` Actually Computes (When the Guard Doesn't Fire)

When `aptr->exp == bptr->exp`, the guard does not fire and `strongsub` proceeds at `tumble.c:548–564`:

```c
answer.exp = aptr->exp;
for (i = 0; aptr->mantissa[i] == bptr->mantissa[i]; ++i) {
    --answer.exp;
    if (i >= NPLACES) {
        movetumbler (&answer, cptr);
        return(0);
    }
}
answer.mantissa[0] = aptr->mantissa[i] - bptr->mantissa[i];
if (++i >= NPLACES) { ... }
for (j = 1; j < NPLACES && i < NPLACES;)
    answer.mantissa[j++] = aptr->mantissa[i++];
```

This is **not arithmetic subtraction**. It is a hierarchical displacement computation: skip the common prefix (counting down `exp` for each matching level), then subtract the first diverging digit, then copy the remaining tail of `a`. It produces the address of `a` relative to `b` within their shared sub-tree. This operation is meaningful only when both tumblers are at the same hierarchical depth (same `exp`).

---

### `tumblersub` and the Span Difference Path

`tumblersub` at `tumble.c:406–440` is the entry point for span differences:

```c
int tumblersub(tumbler *aptr, tumbler *bptr, tumbler *cptr)
{
    if (iszerotumbler (bptr))
        movetumbler (aptr, cptr);
    else if (tumblereq (aptr, bptr))
        tumblerclear (cptr);
    else if (iszerotumbler (aptr)) {
        movetumbler (bptr, cptr);
        cptr->sign = !cptr->sign;
    } else {
        movetumbler (bptr, &temp);
        temp.sign = !temp.sign;
        tumbleradd (aptr, &temp, cptr);   // dispatches to strongsub or weaksub
    }
    tumblerjustify (cptr);
}
```

For span operations, `orglinks.c:377` and `orglinks.c:381` call `tumblersub` to compute widths from end-points:

```c
// orglinks.c:377
tumblersub(&oldspanend, &spanptr->stream, &ptr->width);
// orglinks.c:381
tumblersub(&newspanend, &ptr->stream, &ptr->width);
```

These compute `end - start = width`. If `end` and `start` are at the same depth, `exp` values match, `abscmp` compares mantissas, and when `end > start`, `strongsub` correctly computes the displacement.

---

### When Span Difference Fails to Produce a Meaningful Displacement

Consider subtracting **a span's width** from **another span's start position** — the conceptual operation of "position B.width units before A.start":

```
result = tumblersub(A.start, B.width, result)
```

This flows into `tumbleradd(A.start, -B.width, result)`. The dispatch in `functiontumbleradd` calls `abscmp`:

- If `A.start.exp > B.width.exp` (A.start is at a coarser hierarchical level than B.width) → `abscmp` returns `GREATER` → `strongsub(A.start, B.width, result)` is called → **exponent guard fires** → result = A.start unchanged.

The width had no effect. The displacement was not computed.

**This is a silent failure.** The function returns `0` (success), `cptr` contains `aptr`'s value, and no error path is taken.

---

### The Algebraic Implication

The exponent guard reveals that **tumbler subtraction is not closed over the set of all valid tumblers at different hierarchical depths**. Specifically:

1. **No additive inverse at cross-depth.** For tumblers `a` (coarser) and `b` (finer), `a - b` does not yield a value `d` such that `b + d = a`. Instead it yields `a`, breaking the expected displacement relationship.

2. **The "subtraction" is really a same-level operation only.** `strongsub` is a relative-position function, not an arithmetic difference. It only produces a meaningful result when `a.exp == b.exp` — the two tumblers are at the same hierarchical depth, `a > b` in magnitude. This corresponds to the case where `a` and `b` share a common prefix in the address tree and `a` diverges from `b` to the right.

3. **Width and position must be at the same depth for span arithmetic to be valid.** In `insertpm` at `orglinks.c:115–117`, widths are explicitly constructed at the same depth level as the position:
   ```c
   shift = tumblerlength (vsaptr) - 1;
   inc = tumblerintdiff (&lwidth, &zero);
   tumblerincrement (&zero, shift, inc, &crumwidth.dsas[V]);
   ```
   The `shift` aligns the width digit to the VSA's depth level. This is the **required precondition** — violated, span difference degrades silently.

4. **`abscmp`'s exponent-first ordering creates an incoherent magnitude relationship for cross-depth tumblers.** It declares the coarser-grained tumbler "greater" even if in a numeric sense the finer-grained quantity could be larger. `strongsub` inherits this incoherence and papers over it with the guard.

---

### Concrete Example of the Failure

Suppose:
- `A.start` = `1.2` (exp=0, mantissa=`[1, 2, 0, ...]`) — a two-level address
- `B.width` = `0.0.5` → normalized to (exp=-2, mantissa=`[5, 0, ...]`) — a sub-sub-address quantity

`abscmp(A.start, B.width)`:  
→ `A.start.exp (0) != B.width.exp (-2)`, `A.start.exp > B.width.exp` → returns `GREATER`

`strongsub(A.start, B.width, result)`:  
→ `B.width.exp (-2) < A.start.exp (0)` → guard fires → `result = A.start = 1.2`

`1.2 - 0.0.5 = 1.2`. The fractional width `0.0.5` was entirely swallowed. No displacement occurred.

---

### Summary

When `strongsub` returns its input unchanged due to the exponent guard at `tumble.c:544–547`, it means the subtrahend (`b`) lives at a finer hierarchical depth than the minuend (`a`). The tumbler system has no mechanism to "carry" a fine-grained displacement upward into a coarser-grained address. The exponent guard is an admission of this: rather than produce a wrong answer, it returns `a` unchanged.

For span difference, this means: **subtracting one span's width from another's start position can fail to produce a meaningful displacement whenever the width is expressed at a finer hierarchical depth than the start position.** The operation is defined and closed only within a single depth level. Across depth levels, the result is the coarser operand itself — the width disappears without trace or error. The tumbler algebra is not a group under subtraction; it is a partial operation whose domain of meaningful closure is the set of same-`exp` tumbler pairs.
