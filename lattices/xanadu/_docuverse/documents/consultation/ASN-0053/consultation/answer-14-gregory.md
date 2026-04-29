## Question 14 [gregory]

> How does `tumblerlength` (significant digits: `nstories(t) - t.exp`) interact with span width — does a width tumbler with more significant digits subdivide positions more finely than one with fewer, and what happens when a span's width has a different `tumblerlength` than its start?

## KB Synthesis

## `tumblerlength`, Width Precision, and Span Arithmetic

### `tumblerlength` encodes address-space depth, not content granularity

From [SS-TUMBLER] Finding 0031: `tumblerlength(t) = nstories(t) - t.exp` — the count of significant digits. For a V-address like `1.1`, tumblerlength=2. For an I-address like `0.0.0.0.0.0.0.0.11`, tumblerlength=9. Both can represent the integer 11 as a width, but at different exponent levels.

A width tumbler with more significant digits does NOT inherently subdivide positions more finely in the content sense. The digit count reflects how deep in the address hierarchy the value lives. From [SS-POOM-BOTTOM-CRUM] Finding 0076:

```
V-width for 11 chars: 0.11      (exp=-1, 2 digits)
I-width for 11 chars: 0.0.0.0.0.0.0.0.11  (exp=-8 or so, 9 digits)
```

Both encode the integer 11. [INV-WIDTH-VALUE-EQUIVALENCE] states this explicitly: `tumblerintdiff(crum.width.dsas[V], zero) == tumblerintdiff(crum.width.dsas[I], zero)` — same value, different precision.

### How V-width is derived from I-width

From [SS-INSERT-VWIDTH-ENCODING] Finding 0076, `insertpm` encodes V-width as:

```
shift = tumblerlength(vsaptr) - 1
inc   = tumblerintdiff(&lwidth, &zero)       // extract integer from I-width
tumblerincrement(&zero, shift, inc, &V-width) // encode at V-space precision
```

The V-width exponent is `-shift = -(tumblerlength(vsaptr) - 1)`, determined by the V-address length, not the I-width. So for V-address `1.1` (tumblerlength=2), V-width gets exp=-1; mantissa[0] holds the byte count. The I-width is copied directly. This is a lossy-on-representation-but-value-preserving transformation.

### When widths have different `tumblerlength` than their start: the `strongsub` gate

This mismatch is operationally significant. From [SS-TUMBLER] Finding 0055, `strongsub(a, b)` has an **exponent guard**: if `b.exp < a.exp`, it returns `a` unchanged — no subtraction occurs.

This is precisely why DELETE at V-position `1.x` does not shift link entries at `2.x` ([FC-SUBSPACE], [ST-DELETE] Finding 0055):

```
Deletion width: 0.3  (exp = -1)  
Link displacement: 2.1 (exp = 0)
strongsub(2.1, 0.3): b.exp(-1) < a.exp(0) → NO-OP, returns 2.1
```

The link crum's displacement has exp=0 (integer level); the deletion width is at exp=-1 (fractional/sub-unit level). The exponent mismatch prevents the shift from occurring. This is the **accidental subspace isolation** mechanism for DELETE — in contrast to INSERT's deliberate two-blade knife ([SS-TWO-BLADE-KNIFE], [INT-DELETE-SUBSPACE-ASYMMETRY]).

More generally, if you have a span whose start and width are at the same exponent level, arithmetic behaves as expected. If the width's exponent is lower than the start's exponent, `strongsub`-based shifting is a no-op. `tumbleradd` does not have this guard — it always adds — so computing `reach = start + width` always works regardless of exponent mismatch, but subtracting (shifting) only works when exponents match.

### Practical consequence for the spec

- For text content, span widths are always flat integer byte counts. The tumblerlength asymmetry between V-space (`0.11`) and I-space (`0.0.0.0.0.0.0.0.11`) is an encoding artifact, not a semantic difference ([INV-SINGLE-CHAR-GRANULARITY]).
- The `strongsub` exponent guard is the mechanism behind DELETE's frame condition on the link subspace ([FC-SUBSPACE] Finding 0055). Any Dafny proof of DELETE's subspace isolation must reason about tumbler exponent relationships, not just subspace digit values.
- V-width exponent is a function of V-address depth, so inserting at deeper V-addresses (more digits) produces V-widths with more negative exponents — still encoding the same byte count but at a different precision level.

---

## Code Exploration

Now I have everything I need. Let me write the full answer.

---

## `tumblerlength`, Span Width, and Hierarchical Subdivision

### What `tumblerlength` actually measures

```c
// tumble.c:249-262
INT nstories(tumbler *tumblerptr)
{
    for (i = NPLACES; i > 0 && tumblerptr->mantissa[--i] == 0;);
    return (i + 1);
}

INT tumblerlength(tumbler *tumblerptr)
{
    return (nstories (tumblerptr) - tumblerptr->exp);
}
```

`nstories` returns the index of the last non-zero mantissa digit + 1: the number of mantissa positions actually used.

`tumblerlength` = `nstories + |exp|`, since `exp` is always ≤ 0 [`tumblercheckptr` at `tumble.c:174` enforces this].

`exp` is decremented each time `tumblerjustify` removes leading zeros from the mantissa (`tumble.c:310`: `tumblerptr->exp -= shift`). So `|exp|` records how many hierarchical levels were collapsed. `tumblerlength` is therefore the **total hierarchical depth**: the number of significant levels, including both the stored digits and the removed leading zeros.

Concretely:
- Address `1.2` (mantissa `[1,2,0,…]`, exp=0): nstories=2, tumblerlength=**2**
- Address `1.2.3` (mantissa `[1,2,3,0,…]`, exp=0): nstories=3, tumblerlength=**3**
- A width of "5 at depth 5" (mantissa `[5,0,…]`, exp=−5): nstories=1, tumblerlength=**6**

---

### How span widths are constructed

In `tumbler2spanset` [`do2.c:57–58`]:
```c
tumblerclear (&spanptr->width);
tumblerincrement (&spanptr->width, tumblerlength (tumblerptr)-1/*zzzzz*/, 1, &spanptr->width);
```
Starting from zero, `tumblerincrement` with `rightshift = tumblerlength(stream) - 1` produces:
```c
// tumble.c:603-607
if (iszerotumbler (aptr)) {
    tumblerclear (cptr);
    cptr->exp = -rightshift;   // → exp = -(tumblerlength-1)
    cptr->mantissa[0] = bint;  // → mantissa[0] = 1
}
```
So `tumblerlength(width) = nstories(1) - (-(tumblerlength(stream)-1)) = 1 + (tumblerlength(stream)-1) = tumblerlength(stream)`. **Width is explicitly constructed to have the same tumblerlength as the stream.**

The same pattern appears in `insertpm` [`orglinks.c:115–117`]:
```c
shift = tumblerlength (vsaptr) - 1;
inc = tumblerintdiff (&lwidth, &zero);
tumblerincrement (&zero, shift, inc, &crumwidth.dsas[V]);
```
The V-dimension crum width again gets `tumblerlength = shift + 1 = tumblerlength(vsaptr)`.

And in `inserttextgr` [`granf2.c:106`]:
```c
tumblersub (&lsa, &spanorigin, &ispanptr->width);
```
`lsa` and `spanorigin` are at the same hierarchical depth (same document/atom level), so `strongsub` produces a width whose depth matches the stream.

---

### Does more significant digits = finer subdivision? Yes.

The span end is `stream + width`, computed via `absadd` [`tumble.c:460–484`], which aligns tumblers by their `exp` before adding. Work through three cases with the same stream `1.2` (mantissa `[1,2,0,…]`, exp=0):

**Width = `[1]` at exp=0 (tumblerlength=1) — coarsest:**
```
absadd: exps equal (0 == 0)
answer.mantissa[0] = 1 + 1 = 2
```
Span end = `2`. The span `[1.2, 2)` covers all of chapter 1's content after section 2, including 1.3, 1.4, … up to (not including) 2.

**Width = `[1]` at exp=−1 (tumblerlength=2) — matching:**
```
absadd: aptr->exp (0) > bptr->exp (-1), temp=1
answer.mantissa[0] = a[0] = 1
answer.mantissa[1] = a[1] + b[0] = 2 + 1 = 3
```
Span end = `1.3`. The span `[1.2, 1.3)` covers exactly section 2, including all sub-addresses 1.2.anything.

**Width = `[1]` at exp=−2 (tumblerlength=3) — finest:**
```
absadd: aptr->exp (0) > bptr->exp (-2), temp=2
answer.mantissa[0..2) = a[0..2) = [1, 2]
answer.mantissa[2] = a[2] + b[0] = 0 + 1 = 1
```
Span end = `1.2.1`. The span `[1.2, 1.2.1)` contains only addresses of the form `1.2.k` where k < 1, i.e., only the address `1.2` itself — a span that resolves to a single atomic position.

So yes: **a width tumbler with more significant digits (larger tumblerlength) produces a finer-grained span boundary.** Each additional level of depth narrows the span by one hierarchical tier.

---

### What happens when span width has a different `tumblerlength` than its start?

The system treats this as a **fatal invariant violation**. `ndcuts.c:431`:
```c
if (tumblerlength (cut) != tumblerlength (&ptr->cwid.dsas[index]))
#ifndef DISTRIBUTION
    gerror ("level mismatch\n");
```
(Identical check at `ndcuts.c:504` in the old-code block.)

This check fires during crum splitting: when the enfilade tries to insert a cut point through a node whose width is at a different depth than the cut address, the arithmetic fails. `strongsub` at `tumble.c:548–562` computes the local offset by skipping matching leading digits—if the cut is at depth 3 but the crum width is at depth 5, the subtraction produces a result at the wrong depth, the surviving crum width becomes inconsistent, and the enfilade invariants break.

The reason the depths must match: `tumblerincrement` at `tumble.c:621` places the incremented value at position `idx + rightshift`. If the existing crum has a width at depth 5 and the cut is at depth 3, the result of `locksubtract` at `ndcuts.c:444` will distribute the subtraction across incompatible digit positions, producing a nonsensical new width.

`granf2.c:240` shows how the system defends against this during address allocation:
```c
tumblerincrement(isaptr, tumblerlength(isaptr)==hintlength ? depth : 0, 1, isaptr);
```
The increment depth is chosen conditionally based on whether the found `isaptr` is already at the expected depth (`hintlength`). If not, `depth` is zeroed out — a safety path to avoid placing an address at the wrong level.

---

### Summary

| Property | Effect |
|---|---|
| `tumblerlength(width) < tumblerlength(start)` | Width crosses to a coarser tier; span covers many sub-addresses of adjacent parent nodes |
| `tumblerlength(width) == tumblerlength(start)` | Width is at the same tier as the address; span covers a natural "unit" at that depth |
| `tumblerlength(width) > tumblerlength(start)` | Width crosses to a finer tier; span covers a sub-range of the address's own level |
| Mismatched in a POOM/SPAN crum | `gerror("level mismatch")` — fatal, since `strongsub`/`tumblerincrement` produce garbage at the wrong depth |

The invariant `tumblerlength(width) == tumblerlength(stream)` is enforced by construction at every insertion site (`do2.c:58`, `orglinks.c:115–117`, `granf2.c:106`) and checked defensively at split time (`ndcuts.c:431`, `ndcuts.c:504`). It is a first-class structural constraint of the enfilade: a span lives at a specific hierarchical depth, and both its start and width must agree on what that depth is.
