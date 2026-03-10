## Question 13 [gregory]

> The `strongsub` exponent guard in DELETE returns the link position unchanged when width.exp < pos.exp — was this intentional isolation design or an accident that happens to work, and are there tumbler configurations where the guard fails to protect link subspace positions?

## KB Synthesis

## The `strongsub` Guard: Accidental, Not Intentional

The KB is explicit on this. [INT-DELETE-SUBSPACE-ASYMMETRY] states directly:

> INSERT's protection is robust — it was designed intentionally (the source contains explanatory comments). DELETE's protection is accidental — **there is no comment suggesting awareness of the exponent guard as a subspace protection mechanism**.

[FC-SUBSPACE] (Finding 0055) draws the same contrast: INSERT uses `findaddressofsecondcutforinsert()` to compute an explicit second knife blade at the next subspace boundary `(N+1).1`. DELETE's knife is simply `[origin, origin + width]` — no subspace boundary calculation. The guard is incidental arithmetic, not design.

---

## When the Guard Fails

The guard in `strongsub` is: **if `b.exp < a.exp`, return `a` unchanged** (i.e., skip the subtraction).

[ST-DELETE] (Finding 0055) gives the concrete numbers for why it works in the normal case:
- Text deletion width: exp = −1 (e.g., `0.3` for 3 characters)
- Link position: exp = 0 (e.g., `2.1`)
- Guard: −1 < 0 → TRUE → link position unchanged ✓

The guard fails when **`width.exp ≥ link_pos.exp`**, i.e., when the width has exponent 0 or greater. This happens when a deletion spans a whole-unit V-range, producing a width like `1.0` (exp = 0).

**Concrete failure scenario:**

Delete from position `1.1` with width `1.0` (spanning the full space from text subspace into the link subspace boundary):

```
width = 1.0    (exp = 0)
link  = 2.1    (exp = 0)

strongsub(2.1, 1.0):
  b.exp (0) < a.exp (0)  → FALSE
  Subtraction proceeds: 2.1 − 1.0 = 1.1
  Link position shifts from 2.1 → 1.1
  Text content now occupies what was the link subspace position
```

The link has crossed from `2.x` into `1.x` — the invariant is violated. Nothing in the DELETE path prevents this. [PRE-DELETE] documents that DELETE has no subspace guard, and [FC-SUBSPACE] (Finding 0049, 0051) already established two other violation paths (INSERT at wrong subspace, REARRANGE across boundary). This is a third.

---

## The Structural Invariant Being Relied On

[INT-DELETE-SUBSPACE-ASYMMETRY] formalizes the implicit assumption: `∀ width, entry : different_subspace(width, entry) ==> width.exp < entry.vpos.exp`.

This holds under normal operation because:
1. Text content is addressed at character granularity within `1.x`, so widths are sub-unit (exp = −1)
2. Link positions are in `2.x` at integer precision (exp = 0)
3. No well-behaved deletion spans more than one subspace unit

But the system has **no enforcement of this invariant**. A caller specifying `DELETE(doc, pos=1.1, width=1.0)` — which syntactically looks like a large text deletion — would trigger the failure. The guard only works because of the implicit convention that text deletions are character-sized and link positions are integer-sized, not because `strongsub` was designed to enforce subspace isolation.

[INT-DELETE-SUBSPACE-ASYMMETRY] puts it plainly: "If `strongsub` were modified to handle cross-exponent subtraction correctly, DELETE would break subspace isolation while INSERT would remain safe" — confirming that INSERT's protection is structural and robust, while DELETE's is arithmetic and fragile.

---

## Code Exploration

I have everything I need. Here is the complete analysis.

---

## The `strongsub` Exponent Guard in DELETE: Intentional Isolation or Accident?

### The Guard

`strongsub` [tumble.c:534–565] computes `a - b` when `a > b` (called from `functiontumbleradd` [tumble.c:385] only after `abscmp` confirms this). The guard at lines 544–547:

```c
if (bptr->exp < aptr->exp) {
    movetumbler(aptr,cptr);
    return(0);
}
```

When `bptr` (the subtrahend) has a more negative exponent than `aptr` (the minuend), it silently returns `aptr` unchanged instead of computing any difference.

---

### The DELETE Call Chain

```
fns.c:341      getdeletevspan(taskptr, &docisa, &vspan)
fns.c:342      dodeletevspan(taskptr, &docisa, &vspan)
do1.c:163-166  → deletevspanpm(taskptr, docisaptr, docorgl, vspanptr)
orglinks.c:149 →   deletend((typecuc*)docorgl, &vspanptr->stream, &vspanptr->width, V)
edit.c:63      →     case 2: tumblersub(&ptr->cdsp.dsas[index], width, &ptr->cdsp.dsas[index])
tumble.c:427   →       tumbleradd(pos, -width, pos)
tumble.c:385   →         strongsub(pos, width, pos)   [when |pos| > |width|]
tumble.c:544   →           GUARD: if width.exp < pos.exp → return pos unchanged
```

Case 2 in `deletend` [edit.c:58–65] identifies crums whose left border is at or beyond `blades[1]` (the end of the deleted span) — i.e., nodes that lie entirely *after* the deletion. The adjustment `tumblersub(pos, width, pos)` is supposed to slide them backward to close the V-address gap.

---

### V-Address Exponent Structure

**Text content** in the document POOM is allocated starting at `"1.1"`:

```c
// orglinks.c:42-43, findvsatoappend:
tumblerincrement(vsaptr, 0, 1, vsaptr);  // → exp=0, mantissa=[1,...] = "1"
tumblerincrement(vsaptr, 1, 1, vsaptr);  // → exp=0, mantissa=[1,1,...] = "1.1"
```

Successive text crums are at `"1.1"`, `"1.6"`, `"1.11"` etc., all with **exp=0**.

**Text widths** in the POOM are built by `insertpm` [orglinks.c:115–117]:

```c
shift = tumblerlength(vsaptr) - 1;   // = 2-1 = 1  for "1.1" address
inc   = tumblerintdiff(&lwidth, &zero);
tumblerincrement(&zero, shift, inc, &crumwidth.dsas[V]);
// → exp = -shift = -1, mantissa=[inc,...]
```

So text crum **V-widths always have exp=−1**.

**Link ISA references** in the parent document's POOM are placed by `findnextlinkvsa` [do2.c:151–167] at V-addresses starting from `"2.1"`:

```c
tumblerincrement(&firstlink, 0, 2, &firstlink);  // → exp=0, mantissa=[2,...] = "2"
tumblerincrement(&firstlink, 1, 1, &firstlink);  // → exp=0, mantissa=[2,1,...] = "2.1"
```

These are **exp=0**, mantissa=[2,N,...] addresses.

**Link endpoint data** in the link's own POOM uses fixed VSAs from `setlinkvsas` [do2.c:169–183]:

```c
fromvsa = "1.1"  (exp=0, mantissa=[1,1,...])
tovsa   = "2.1"  (exp=0, mantissa=[2,1,...])
threevsa = "3.1" (exp=0, mantissa=[3,1,...])
```

All are **exp=0**.

---

### What the Guard Actually Does in the Normal Delete Case

When text is deleted — say from `"1.1"` to `"1.6"` (5 chars) — the width is computed as a tumbler difference of same-prefix addresses. Tracing `strongsub("1.6", "1.1")` [tumble.c:549–555]:

```c
answer.exp = aptr->exp = 0;
// Loop: i=0, mantissa[0]: 1 == 1 → --answer.exp → answer.exp = -1, i=1
// i=1, mantissa[1]: 6 != 1 → break
answer.mantissa[0] = 6 - 1 = 5;
// Result: exp=-1, mantissa=[5,...] = "0.5"
```

Deletion width: **exp=−1**.

Now adjusting a link crum at `"2.1"` [edit.c:63]:

```c
tumblersub(&ptr->cdsp.dsas[V], width, &ptr->cdsp.dsas[V])
// = tumblersub("2.1", "exp=-1, [5,...]", result)
// → tumbleradd("2.1", neg-width, result)
// → abscmp("2.1", "exp=-1, [5,...]"): "2.1".exp=0 > width.exp=-1 → GREATER
// → strongsub("2.1", "exp=-1, [5,...]", result)
//   → guard: bptr->exp(-1) < aptr->exp(0) → TRUE → return "2.1" unchanged ✓
```

The link ISA at `"2.1"` is not touched.

---

### Was This Intentional?

**It was a defensive precision check that happens to provide the right isolation — not a purposeful isolation design.**

Evidence for **precision check, not isolation design**:

1. The guard appears in `strongsub` whose contract is same-exponent exact subtraction (contrast with `weaksub` which explicitly handles exponent mismatches for less precise arithmetic). The guard is a safety net when that contract is violated — it returns the minuend unchanged rather than producing garbage.

2. The case-2 adjustment code in `deletend` [edit.c:62–65] and its comment `/* This will get set to modified in setwisp */` treats the shift as a real operation expected to produce a new value. If the isolation were intentional, `deletend` would simply not call `tumblersub` for dimension V at all.

3. `strongsub` is called from `functiontumbleradd` [tumble.c:384–389] in general arithmetic contexts (not just delete). The guard protects those contexts from exponent overflow too.

4. The function name "strong" vs "weak" in Xanadu's own terminology refers to precision, not protection. `strongsub` is exact; `weaksub` is approximate.

The alignment between the guard's firing condition and the semantically correct behavior — link V-addresses persist, text deletion widths are exp=−1, link positions are exp=0 — is a consequence of the V-address allocation scheme, not explicit guard design.

---

### Configurations Where the Guard Fails to Protect Link Subspace Positions

The guard fires only when `width.exp < pos.exp`. It does **not** fire when `width.exp >= pos.exp`. Specifically, width has exp=0 whenever the deletion spans across level-1 node boundaries (different leading mantissa digit).

**Configuration 1 — Cross-subspace deletion:**

A V-span deletion from `"1.5"` (text subspace, mantissa[0]=1) to `"2.2"` (link subspace, mantissa[0]=2) produces:

```c
// strongsub("2.2", "1.5", width):
// mantissa[0]: 2 != 1 → no --answer.exp
// answer.mantissa[0] = 2 - 1 = 1, answer.exp = 0
// width = exp=0, mantissa=[1,...] = "1"
```

The link ISA at `"2.3"` (case 2, beyond blade[1]="2.2") would then be adjusted:

```c
// tumblersub("2.3", "1", result) → strongsub("2.3", "1", result)
// bptr->exp(0) NOT < aptr->exp(0) → guard does NOT fire
// mantissa[0]: 2 != 1 → answer.mantissa[0] = 2-1 = 1, answer.exp = 0
// Result: "1.3" — link position silently corrupted from "2.3" to "1.3"
```

**Configuration 2 — Deletions targeting link subspace itself:**

Deleting a link ISA from `"2.1"` to `"2.2"` produces width exp=−1 (same-prefix subtraction, one `--answer.exp`), so the guard fires for adjacent link ISAs at `"2.2"`, `"2.3"`, etc. — they do NOT shift. This means link ISA positions in the parent document are **immovable** even after other link ISAs are deleted, creating persistent V-address gaps. This may or may not be the intended behavior, but it is not the guard "protecting" anything — it is simply failing to implement gap closure.

**Configuration 3 — Client-specified exp=0 width:**

The FEBE protocol allows clients to specify arbitrary V-spans to delete [fns.c:333–347]. A client providing a `typevspan` with `width.exp=0` directly bypasses the guard for any link position with `pos.exp=0`.

---

### Summary

The guard at `tumble.c:544–547` is a **defensive precision check** — added because `strongsub` cannot correctly compute a difference when `bptr` is more precise than `aptr`. Its effect as link-position isolation is an **accident that works** because normal text deletion widths (exp=−1) are always one level finer than link positions (exp=0), causing the guard to fire every time.

The guard **fails** when deletion produces exp=0 widths. This happens in any deletion spanning two different top-level V-nodes — most relevantly, a cross-subspace deletion from text to link space (`"1.x"` → `"2.y"`) produces an exp=0 width that bypasses the guard and shifts case-2 link ISA crums by incorrect amounts, corrupting their V-addresses in the parent document POOM.
