## Question 10 [gregory]

> Is `tumblersub(a, b)` intended to be a true group subtraction (always yielding a valid distance), or are there tumbler pairs where the negative result is a representation artifact that should never appear in practice?

## KB Synthesis

The KB evidence points to **representation artifact** — negative results from `tumblersub` are not intended valid distances.

## The case for "always valid group subtraction"

The type system was clearly built with negative tumblers in mind. `tumblersub` negates the subtrahend's sign and calls `tumbleradd` [SS-TUMBLER, Finding 0053], `tumblercmp` correctly sorts negative tumblers before all positives [INV-TUMBLER-TOTAL-ORDER], and the sign-magnitude encoding is structurally consistent. The capability exists.

## Why it's actually a representation artifact

**Intended use context is always non-negative.** The primary consumer of `tumblersub` is span width computation: `width = tumblersub(end, start)` in `granf2.c:106` [SS-SPAN]. This is only called when `end >= start` by construction — a negative width has no meaningful interpretation in a content span.

**Negative V-positions from DELETE are explicitly described as a missing precondition violation.** [PRE-DELETE, Finding 0053] states directly that a *complete* precondition for DELETE should include `∀ entry : entry.vpos > delete_end ⟹ entry.vpos - delete_width ≥ 0`. The fact that this is labeled a *missing precondition* rather than a design choice confirms negative results are unintended. [INV-POOM-BIJECTIVITY] further confirms: entries with negative V-positions "exist in the POOM tree but maps to no valid V-address" — leaked dead state, not valid negative distances.

**The `strongsub` exponent guard is incidental protection, not intentional design.** [SS-TUMBLER, Finding 0055] shows that cross-exponent subtraction returns the minuend unchanged — but this was not designed as a guard against underflow. It's an arithmetic side effect that happens to prevent cross-subspace corruption. [INT-DELETE-SUBSPACE-ASYMMETRY] explicitly flags this as a fragile, unintentional invariant.

**No operation consumes negative tumblers.** The system has `iszerotumbler()` to detect zero, but no `isnegativetumbler()` used in any meaningful data structure path. Negative results have nowhere to go — they become invisible entries that cannot even be targeted by a subsequent DELETE (their V-position is unreachable by any positive-valued span argument).

## Summary

`tumblersub` was built as a general signed arithmetic operation — a complete implementation — but the **intended domain is non-negative results**. The sign-magnitude representation is an implementation convenience (subtraction-as-negation-plus-addition), not a design feature for negative distances. When the precondition `a >= b` is violated, the result is not a valid distance in any address space; it's undefined behavior that manifests as invisible leaked POOM entries [EC-DEEPLY-ORPHANED-LINK].

---

## Code Exploration

I now have a complete picture. Here is my full analysis:

---

## `tumblersub`: True Group Subtraction, with Intentional Negative Intermediates

### The Implementation

`tumblersub(a, b, c)` [tumble.c:406–440] is implemented as full signed arithmetic: it negates `b->sign` and delegates to `tumbleradd` [tumble.c:426–428]. `tumbleradd` dispatches to `absadd`, `strongsub`, or `weaksub` depending on signs and relative magnitude [tumble.c:374–396]. The `sign` field in the tumbler struct is a genuine signed-magnitude bit [common.h:62]:

```c
char sign  BIT ;  /* 1 if negative, otherwise 0 */
```

The tumbler representation explicitly supports negative values. `tumblercheck` [tumble.c:169–227] validates a negative tumbler as legal — it only rejects `sign=1` when `mantissa[0] == 0` (negative zero), not when `sign=1` in general [tumble.c:180–183]:

```c
if (ptr->sign && ptr->mantissa[0] == 0){
    fprintf(stderr," negative zero ");
    wrong = TRUE;
}
```

So **negative tumblers are a valid state** in the representation, not an artifact.

---

### The Commented-Out Debug Sentinels

The most revealing evidence is the two diagnostic blocks commented out inside `tumblersub` [tumble.c:409–417, 432–438]:

```c
/*
    if(aptr->sign || bptr->sign) {
        fprintf(stderr,"TUMBLERSUB NEG IN \n");
        ...
    }
*/
...
/*
    if (cptr->sign) {
        fprintf(stderr,"TUMBLERSUB NEGATIVE OUTPUT\n");
        ...
    }
*/
```

These were *observability* probes, not *defensive guards*. They were added to monitor how often the function received signed inputs or produced signed outputs, then commented out once the developers understood the call sites. They do not reject negative results — they were watching for them. Their existence confirms the authors knew negative outputs could occur.

---

### Call Sites: Two Distinct Usage Modes

**Mode 1 — Width/span arithmetic (majority of sites):** The caller guarantees `a ≥ b`, so negative output indicates a logic error. Examples:

- `edit.c:63`: `tumblersub(&ptr->cdsp.dsas[index], width, ...)` — reducing a crum's displacement by `width`, where `width ≤ displacement` by construction.
- `correspond.c:319,327`: `tumblersub(&span2->width, &span1->width, ...)` — used only inside a switch branch that has already compared the widths.
- `orglinks.c:377,381`: width calculations for new spans inside `vspanset2ispanset`, called only when `spanptr->stream ≤ oldspanend` is known.
- `makeroom.c:31`: `tumblersub(&grasp->dsas[i], &origin->dsas[i], &base)` — entered only inside `if (tumblercmp(&origin->dsas[i], &grasp->dsas[i]) == LESS)` [makeroom.c:26], so `base > 0` is guaranteed.

In all these sites a negative result would mean a tree invariant had been violated upstream.

**Mode 2 — Geometric offset arithmetic (edit.c):** The caller deliberately computes a signed displacement. This is the clearest proof of intentional negative use.

`edit.c:178–180`:
```c
tumblersub (&knives->blades[2], &knives->blades[1], &diff[1]);
tumblersub (&knives->blades[1], &knives->blades[0], &diff[2]); /* should be negative */
diff[2].sign = !diff[2].sign;
```

The comment `/* should be negative */` is explicit. The sign is then flipped on the next line to convert the result to a positive absolute value for use as an offset. Crucially, the *same computation* could have been written as `tumblersub(blades[0], blades[1], diff[2])`, but the developer chose to express the geometric semantics as a negative and then flip.

`edit.c:174–176`:
```c
/*  tumblersub (&knives->blades[0], &knives->blades[2], &(diff[3]));*/  /* should be <0 */
movetumbler (&diff[1], &diff[3]);
diff[3].sign = !diff[1].sign;
```

The `/* should be <0 */` call was commented out and replaced with a manual sign-flip of `diff[1]` — but the intent is the same: produce a negated distance. The replacement avoids an unnecessary `tumblersub` call when the value is already computed.

---

### `strongsub` and `weaksub` Are Internal, Not Asymmetric

These two helpers [tumble.c:534–589] implement magnitude subtraction where `|a| ≥ |b|` is a precondition. They are only invoked from inside `tumbleradd` [tumble.c:384–393], after `abscmp` has already established which operand is larger. They are not exposed as the general subtraction interface — `tumblersub` is. The use of `strongsub`/`weaksub` internally does not mean the outer operation is restricted to non-negative results.

---

### Conclusion

`tumblersub(a, b)` **is a true signed group subtraction**. It always yields a valid tumbler value — including negative ones. Negative results are not representation artifacts; they are legitimate values that the type supports and that callers sometimes deliberately produce (as signed geometric offsets in `edit.c`).

The design intent has two tiers:

1. **Span/width arithmetic**: callers establish `a ≥ b` as a precondition and expect a positive result. A negative result here would indicate an upstream invariant violation, which the (now-commented-out) `"TUMBLERSUB NEGATIVE OUTPUT"` probe was designed to catch during development.

2. **Rearrangement offset arithmetic** (`edit.c:makeoffsetsfor3or4cuts`): negative results are *intended*, explicitly noted with comments like `/* should be negative */`, and consumed by immediately flipping the sign to form a positive displacement in the opposite direction.

The function is general; the non-negativity assumption is a *caller responsibility*, not a function contract. Nothing in `tumblersub` prevents or rejects negative output.
