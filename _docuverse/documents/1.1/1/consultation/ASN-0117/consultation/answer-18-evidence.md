## Question 18 [evidence]

> When a DELETE in the text subspace `1.x` subtracts a text-level width (exp=-1) from a link position (exp=0), does the `strongsub` exponent guard return the link position unchanged, preserving link subspace `2.x` entries?

## KB Synthesis

Yes. The `strongsub` exponent guard preserves link subspace entries exactly as described.

**The mechanism** [FC-SUBSPACE, Finding 0055]:

`deletecutsectionnd` classifies a link crum at V-position `2.1` (exp=0) as **case 2** (shift candidate) when both knife blades `[origin, origin+width]` lie to its left. Case 2 executes:

```c
tumblersub(&ptr->cdsp.dsas[V], width, &ptr->cdsp.dsas[V])
```

But `tumblersub` delegates to `strongsub`, which has this guard [SS-TUMBLER, Finding 0055]:

```c
if (bptr->exp < aptr->exp) { movetumbler(aptr, cptr); return(0); }
```

For a text deletion width `0.3` (exp=−1) and link displacement `2.1` (exp=0):
- `b.exp` (−1) < `a.exp` (0) → guard fires → returns `2.1` unchanged

**The result** [FC-SUBSPACE Finding 0055 concrete example]:

```
DELETE 3 bytes at 1.1 (width = 0.3, exp = -1)
Link crum at 2.1 (exp = 0)
strongsub(2.1, 0.3) → exponent mismatch → 2.1 returned unchanged
```

After deleting all text, the link remains at V-position `2.1`, still discoverable via `find_links` and followable via `follow_link`.

**Critical caveat** [INT-DELETE-SUBSPACE-ASYMMETRY]: This protection is **accidental**, not designed. INSERT uses a deliberate two-blade knife with a computed subspace boundary (`findaddressofsecondcutforinsert` produces `(N+1).1` as the second blade). DELETE has no such structural guard — its knife is simply `[origin, origin+width]`. Subspace isolation for DELETE depends entirely on the invariant that text deletion widths always have lower exponent than cross-subspace displacements. If `strongsub` were modified to handle cross-exponent subtraction, DELETE would break subspace isolation while INSERT would remain safe.

---

## Code Exploration

---

## Answer

**Yes — the `strongsub` exponent guard at `tumble.c:544–547` fires exactly in this scenario and returns the link position unchanged.**

---

### Full Call Chain

**1. Entry point — `dodeletevspan` → `deletevspanpm`**

`do1.c:158–167`:
```c
bool dodeletevspan(typetask *taskptr, typeisa *docisaptr, typevspan *vspanptr)
{
  ...
  return (findorgl(...) && deletevspanpm(taskptr, docisaptr, docorgl, vspanptr));
}
```

`orglinks.c:145–152`:
```c
bool deletevspanpm(typetask *taskptr, tumbler *docisaptr, typeorgl docorgl, typevspan *vspanptr)
{
    if (iszerotumbler(&vspanptr->width)) return (FALSE);
    deletend((typecuc*)docorgl, &vspanptr->stream, &vspanptr->width, V);
    ...
}
```

`deletend` is called with `stream` = deletion origin in text subspace 1.x, `width` = text-level width (`exp=-1`), `index` = V (virtual stream dimension).

---

**2. `deletend` — displacement subtraction for nodes to the right**

`edit.c:31–76`. After computing the two knife-cut positions at `origin` and `origin+width`, the loop classifies each node:

```c
case 2:
    tumblersub(&ptr->cdsp.dsas[index], width, &ptr->cdsp.dsas[index]);
    break;
```
`edit.c:63` — nodes classified as "to the right" of the deleted span receive `cdsp = cdsp - width`.

A link node at absolute V-position `2.x` (exp=0) lies to the right of knife blades at 1.x (exp=-1), so it falls into **case 2** and this subtraction is attempted.

---

**3. `tumblersub` dispatches to `tumbleradd`**

`tumble.c:406–440`. The general path:

```c
movetumbler(bptr, &temp);
temp.sign = !temp.sign;          /* negate the width */
tumbleradd(aptr, &temp, cptr);   /* link_pos + (-width) */
```
`tumble.c:426–428` — the link position is `aptr` (exp=0, positive), the negated width is `temp` (exp=-1, negative).

---

**4. `functiontumbleradd` — sign mismatch triggers `abscmp` then `strongsub`**

`tumble.c:365–404`. Since the two operands have opposite signs:

```c
} else if (abscmp(aptr, bptr) == GREATER) {
    strongsub(aptr, bptr, cptr);
    cptr->sign = aptr->sign;
```
`tumble.c:384–386`.

`abscmp` [tumble.c:87–111] compares exponents first:
```c
if (aptr->exp != bptr->exp) {
    if (aptr->exp < bptr->exp)  return(LESS);
    else                         return(GREATER);
}
```
`tumble.c:92–96`. Since `aptr->exp=0 > bptr->exp=-1`, `abscmp` returns **GREATER**, routing to `strongsub`.

---

**5. `strongsub` — the exponent guard**

`tumble.c:534–565`. After the equality check, the first thing `strongsub` tests is:

```c
if (bptr->exp < aptr->exp) {
    movetumbler(aptr,cptr);
    return(0);
}
```
`tumble.c:544–547`.

With `bptr->exp = -1` (text-level width) and `aptr->exp = 0` (link position), the condition `-1 < 0` is **true**. `movetumbler(aptr, cptr)` copies the link position to the output and the function returns immediately — **no arithmetic is performed**.

Back in `functiontumbleradd`, `cptr->sign = aptr->sign` (positive) is set. The result is the original link position, unchanged.

---

### Why This Is Architecturally Correct

Text content lives in V-subspace `1.x`, using fractional addresses where the width of a single content item has `exp=-1` (one story below the integer level). Link entries live in V-subspace `2.x`, whose positions have `exp=0` (integer level, since `2.something` starts at the integer story).

The guard `bptr->exp < aptr->exp` is exactly the condition "the quantity being subtracted is finer-grained than the position being updated." When a text-level delete (exp=-1) walks the POOM V-dimension and encounters link entries (exp=0), `strongsub` recognizes the exponent mismatch and leaves those entries at their original addresses.

The link subspace `2.x` positions survive the delete intact. They are not shifted.
