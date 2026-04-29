## Question 16 [gregory]

> In the `strongsub` exponent guard that provides DELETE's subspace isolation — if a document has text entries at `V:1.x` with `exp=0` and a deletion width also at `exp=0` (say, deleting a range wider than 1.0), does the exponent guard still fire, or does isolation fail because the width and position share the same exponent class?

## KB Synthesis

## Analysis: strongsub Guard Under Same-Exponent Conditions

The guard fails and subspace isolation breaks. Here is why.

### How the protection normally works

The `strongsub` exponent guard is: if `b.exp < a.exp`, return `a` unchanged. From [FC-SUBSPACE] Finding 0055's concrete example:

```
Text crum:  V-displacement 0.4  (exp = -1)
Link crum:  V-displacement 2.1  (exp =  0)   ← relative to root
Width:                     0.3  (exp = -1)

strongsub(link.cdsp=2.1, width=0.3): b.exp(-1) < a.exp(0) → TRUE → returns 2.1 unchanged
strongsub(text.cdsp=0.4, width=0.3): b.exp(-1) < a.exp(-1) → FALSE → subtracts → 0.1
```

Isolation holds because the link crum's relative displacement (exp=0) exceeds the deletion width's exponent (exp=-1). This is accidental — DELETE constructs its knife blades as `[origin, origin + width]` with no subspace-boundary computation [INT-DELETE-SUBSPACE-ASYMMETRY].

### What happens when width.exp = crum.exp

The guard condition is **strictly** less-than. From [FC-SUBSPACE] Finding 0055's corrected postcondition:

> `∀ entry ∈ poom(doc) : entry.vpos > delete_end ∧ entry.vpos.exp = width.exp =⟹ entry.vpos' = entry.vpos - delete_width`

If both text crum displacement and deletion width are exp=0, then `b.exp(0) < a.exp(0)` is **FALSE**. The guard does not fire. Subtraction proceeds. If link crums also have displacement at exp=0 (which they typically do, since `2.1 - root.cdsp` is often `1.0` or similar), those crums are also shifted. Subspace isolation fails for both.

### When does a width reach exp=0?

Normal character deletions produce widths like `0.11`, `0.100` — these stay at exp=-1 regardless of character count. An exp=0 width requires a deletion span that crosses a hierarchical unit boundary. For example, deleting from `1.1` to `3.1` (spanning the text and link subspaces) yields width `3.1 − 1.1 = 2.0` (exp=0). The backend imposes no precondition against this — `deletevspanpm` only checks for zero width [PRE-DELETE].

### Why this matters for spec

[INT-DELETE-SUBSPACE-ASYMMETRY] explicitly flags this:

> DELETE's protection is accidental — there is no comment suggesting awareness of the exponent guard as a subspace protection mechanism. If `strongsub` were modified to handle cross-exponent subtraction correctly, DELETE would break subspace isolation while INSERT would remain safe.

The frame condition `∀ op ∈ {DELETE} on subspace s, ∀ entry: entry.vpos.mantissa[0] ≠ s ⟹ entry.vpos' = entry.vpos` from [FC-SUBSPACE] therefore rests on an invariant that deletion widths are *always* at a lower exponent class than cross-subspace crum displacements. A cross-subspace deletion (width exp=0) violates this assumption, and isolation fails — both text and link crums at exp=0 would be shifted.

INSERT has no such fragility: its second blade is structurally computed at `(N+1).1` by `findaddressofsecondcutforinsert`, placing all cross-subspace entries in case-2 (no-shift) before any arithmetic occurs [SS-TWO-BLADE-KNIFE].

---

## Code Exploration

---

## Analysis: The `strongsub` Exponent Guard and DELETE Subspace Isolation

### The Guard in Question

`strongsub` at `tumble.c:544–547`:

```c
if (bptr->exp < aptr->exp) {
    movetumbler(aptr,cptr);
    return(0);
}
```

This is the only exponent check in the function. It fires when the subtrahend `b` is at a *strictly lower* (more negative) exponent than `a`. When it fires, it returns `a` unchanged — the effect is "a fine-grained subtrahend cannot shift a coarse-grained address."

### When Both Are `exp=0`: The Guard Does Not Fire

The `exp` field is a `short` [`common.h:63`], validated by `tumblercheckptr` to always be `<= 0` [`tumble.c:174–178`]:

```c
if (ptr->exp > 0){
    fprintf(stderr,"bad exp ");
    wrong = TRUE;
}
```

When a text entry's position is at `V:1.x` with `exp=0`, and the deletion width is also `exp=0` (e.g., `mantissa[0]=2`, representing a width greater than 1.0):

- The guard condition: `bptr->exp < aptr->exp` evaluates to `0 < 0` = **FALSE**
- The guard does **not** fire

Execution falls straight through to line 548:

```c
answer.exp = aptr->exp;
for (i = 0; aptr->mantissa[i] == bptr->mantissa[i]; ++i) {   // line 549
    --answer.exp;
    ...
}
answer.mantissa[0] = aptr->mantissa[i] - bptr->mantissa[i];  // line 556
```

Plain mantissa-level subtraction proceeds.

---

### Tracing the DELETE Call Path

`dodeletevspan` → `deletevspanpm` [`orglinks.c:145–152`] → `deletend` [`edit.c:31`].

Inside `deletend`, two things happen that touch `strongsub`:

**1. Computing the deletion boundary** [`edit.c:40–41`]:

```c
movetumbler (origin, &knives.blades[0]);
tumbleradd (origin, width, &knives.blades[1]);
```

`tumbleradd` is the macro `functiontumbleradd` [`common.h:197`]. Because both `origin` and `width` are positive (`sign=0`), this takes the `aptr->sign == bptr->sign` branch at `tumble.c:374` → calls `absadd`. **`strongsub` is not invoked here at all.**

**2. Shifting survivors after deletion** [`edit.c:63`]:

```c
case 2:
    tumblersub (&ptr->cdsp.dsas[index], width, &ptr->cdsp.dsas[index]);
    break;
```

`tumblersub` negates `width` and calls `tumbleradd(displacement, -width, ...)` [`tumble.c:406–430`]. Now signs differ. If `|displacement| > |width|`:

```c
} else if (abscmp (aptr, bptr) == GREATER) {
    strongsub (aptr, bptr, cptr);   // tumble.c:385
```

`strongsub` IS called here. For a crum at `V:3.5 = {exp=0, mantissa=[3,5,...]}` after a deletion of width `2 = {exp=0, mantissa=[2,...]}`:

- Guard: `bptr->exp(0) < aptr->exp(0)` → `0 < 0` = **FALSE** — guard bypassed
- Loop at line 549: compare `mantissa[0]`: `3 ≠ 2`, no matching prefix
- `answer.mantissa[0] = 3 - 2 = 1`, then digits from `a` copied: `answer.mantissa[1] = 5`
- Result: `{exp=0, mantissa=[1,5,...]}` = `V:1.5`

Correct arithmetic — the crum moves from `V:3.5` to `V:1.5`.

---

### What the Guard Actually Isolates (and What It Cannot)

The guard fires when `b->exp < a->exp` — i.e., when the subtrahend is at a **deeper level** than the minuend. Example:

- `a = V:5` — `{exp=0, mantissa=[5]}`
- `b = V:0.3` — `{exp=-1, mantissa=[3]}`

Condition: `-1 < 0` = TRUE → guard fires, returns `V:5` unchanged.

This prevents a sub-level width (e.g., a deletion whose width is expressed as a fractional V-amount at `exp=-1`) from erroneously displacing a main-level (`exp=0`) crum address. That is the isolation property: **sub-level deletions don't shift main-level addresses**.

But this protection is predicated entirely on an **exponent difference**. When both position and width are at `exp=0`, the guard has no basis to discriminate between them. It sees two values at the same level and performs normal subtraction.

---

### Isolation Failure in the `exp=0 / exp=0` Scenario

The V-space subspace structure, visible in `orglinks.c`:

- Text crums: `mantissa[1] == 0` (addresses like `V:1`, `V:2`, `V:3` — single-story) [`orglinks.c:247–252`]
- Link crums: `mantissa[0]==1 && mantissa[1]!=0` (addresses like `V:1.1`, `V:1.2`, ... — two-story starting with 1) [`orglinks.c:255–261`]

Both kinds have `exp=0`. The deletion range boundaries are computed in V-space via address arithmetic, and `deletecutsectionnd` [`edit.c:235–248`] classifies crums purely by whether their V-address falls inside `[blade[0], blade[1])`:

```c
for (i = knives->nblades-1; i >= 0; --i) {
    cmp = whereoncrum(ptr, offset, &knives->blades[i], knives->dimension);
    if (cmp == THRUME) return (-1);
    else if (cmp <= ONMYLEFTBORDER) return (i+1);
}
```

There is no exponent-based fast-path in this classification. A link crum at `V:1.5` and a text crum at `V:2.5` are indistinguishable at this layer — both are `exp=0`, both are `THRUME` inside a range `[V:1, V:3)`, both get classified as `case 1` and deleted.

**The strongsub exponent guard plays no role in preventing this.** It only acts on the displacement arithmetic for `case 2` crums — those *after* the deletion range — and it is only operative when the width has a smaller exponent than the displacement. When both are `exp=0`, the guard is inoperative and deletion arithmetic is flat mantissa subtraction with no subspace awareness.

---

### Summary

| Condition | Guard fires? | What happens |
|---|---|---|
| `b->exp = -1`, `a->exp = 0` | **YES** | Guard returns `a` unchanged — sub-level width cannot shift main-level address |
| `b->exp = 0`, `a->exp = 0` | **NO** | Falls through to mantissa loop at `tumble.c:549`; plain digit subtraction |

When both position (`V:1.x`, `exp=0`) and deletion width (`exp=0`) share the same exponent class, the guard at `tumble.c:544` evaluates to `0 < 0 = FALSE` and does not fire. Isolation does not come from this guard in that scenario — it requires an exponent difference to exist. The guard is a cross-level arithmetic safety valve, not a V-subspace discriminator. In the equal-exponent case, `deletecutsectionnd` treats text and link crums identically, and the `strongsub` path performs straightforward digit-by-digit subtraction with no subspace protection.
