## Question 19 [gregory]

> Does the `strongsub` exponent guard that provides subspace isolation during DELETE operate symmetrically — that is, does a delete in the link subspace (V-position `2.x`) also leave text subspace entries (`1.x`) unchanged, or does the guard only protect higher-exponent entries from lower-exponent widths?

## KB Synthesis

The guard operates symmetrically in **effect** — a delete in the link subspace (2.x) leaves text entries (1.x) unchanged — but through a **different mechanism** than the reverse direction. The two directions are protected by entirely different parts of the code.

---

## Direction 1: DELETE in text subspace (1.x) → link entries (2.x) unchanged

This is the case documented in [FC-SUBSPACE] / Finding 0055. Link crums sit at V-displacement exp=0 (e.g., `2.1`). The text deletion width (e.g., `0.3`) has exp=−1. `deletecutsectionnd` classifies link crums as Case 2 (after the deletion range), so `tumblersub(2.1, 0.3)` is called — but `strongsub` fires its exponent guard:

```
b.exp (−1) < a.exp (0)  →  TRUE  →  returns 2.1 unchanged
```

Protection is **arithmetically accidental**: the exponent mismatch prevents subtraction. There is no design comment indicating awareness of this as a subspace guard.

---

## Direction 2: DELETE in link subspace (2.x) → text entries (1.x) unchanged

Text crums sit at V-positions like `1.5` (exp=−1), which are numerically less than any 2.x address. The DELETE knife blades for a link-subspace operation are `[2.1, 2.2]`. `deletecutsectionnd` classifies text crums as **Case 0** (TOMYLEFT of blade[0]):

```
text_vpos (1.5) < blade[0] (2.1)  →  Case 0  →  no shift, no subtraction
```

`strongsub` is **never called** on text entries at all. Protection is **positional**: text lives below the deletion range. The exponent guard plays no role.

---

## Verification: Finding 0040 directly confirms the symmetric result

[SS-THREE-LAYER-MODEL] / Finding 0040 provides empirical confirmation: after `DELETEVSPAN(2.1)`, the resulting vspanset shows `{"start": "1.1", "width": "0.11"}` — the text subspace is completely unchanged.

---

## Summary

| Delete direction | Other subspace protected? | Mechanism |
|---|---|---|
| Text (1.x) delete | Link (2.x) entries safe | `strongsub` exponent guard: b.exp(−1) < a.exp(0) |
| Link (2.x) delete | Text (1.x) entries safe | Positional classification: text < blade[0], Case 0 |

The guard is **not symmetric in mechanism**. INSERT achieves symmetry through a deliberate structural guard (two-blade knife with subspace boundary at `(N+1).1`). DELETE achieves it through two independent and unrelated properties — an arithmetic accident for one direction, and ordinary positional ordering for the other. As [INT-DELETE-SUBSPACE-ASYMMETRY] notes, the arithmetic protection is fragile: if `strongsub` were ever modified to handle cross-exponent subtraction, text-subspace deletes would break link subspace isolation, while the positional protection for the reverse direction would remain intact.

---

## Code Exploration

I now have all the evidence needed. Here is the complete analysis.

---

## Does the `strongsub` exponent guard operate symmetrically in DELETE?

**Short answer: No. The two directions of subspace isolation use entirely different mechanisms.** The guard protects link-subspace crums from text-subspace deletions. Text-subspace crums are protected from link-subspace deletions by spatial ordering alone — the guard never fires in that direction because `tumblersub` is never called on them.

---

### The delete path

`dodeletevspan` [do1.c:158-167] → `deletevspanpm` [orglinks.c:145-152] → `deletend` [edit.c:31-76].

`deletend` plants two knife blades:

```c
// edit.c:40-43
movetumbler (origin, &knives.blades[0]);
tumbleradd (origin, width, &knives.blades[1]);
```

Then iterates over children of the spanning father node and classifies each crum via `deletecutsectionnd` [edit.c:235-248]:

- **Case 0**: crum is entirely to the LEFT of blade[0] — before the deletion. No action.
- **Case 1**: crum's left edge falls between blade[0] and blade[1] — within the deletion. `disown` + `subtreefree`.
- **Case 2**: crum's left edge is at or after blade[1] — entirely to the right of the deletion. `tumblersub` is called:

```c
// edit.c:63
tumblersub (&ptr->cdsp.dsas[index], width, &ptr->cdsp.dsas[index]);
```

`tumblersub` [tumble.c:406-439] negates `width.sign` and calls `tumbleradd`, which dispatches to **`strongsub`** [tumble.c:534-565] when `abscmp(crum_disp, width) == GREATER`.

---

### The exponent guard in `strongsub`

```c
// tumble.c:544-546
if (bptr->exp < aptr->exp) {
    movetumbler(aptr,cptr);
    return(0);
}
```

`aptr` = the crum's V-displacement, `bptr` = the deletion width (as a magnitude). When `bptr->exp` is more negative (finer-grained) than `aptr->exp`, the guard fires and returns `aptr` unchanged.

---

### V-space layout: what exponents look like

**Text subspace** crums are inserted at V-positions 1.1, 1.2, … via `findvsatoappend` [orglinks.c:42-43]:

```c
tumblerincrement (vsaptr, 0, 1, vsaptr);   // → 1
tumblerincrement (vsaptr, 1, 1, vsaptr);   // → 1.1
```

These tumblers have `exp=0`, `mantissa=[1,1,0,…]`.

**Link subspace** crums are inserted starting at 2.1 via `findnextlinkvsa` [do2.c:157-158]:

```c
tumblerincrement (&firstlink, 0, 2, &firstlink);  // → 2
tumblerincrement (&firstlink, 1, 1, &firstlink);  // → 2.1
```

Tumblers with `exp=0`, `mantissa=[2,1,0,…]`.

**Deletion widths** for a typical intra-subspace cut are computed via `strongsub`. Deleting [1.x, 1.y) or [2.x, 2.y):

`strongsub([1,y,…], [1,x,…])` [tumble.c:534-565]:

- `exp` starts at 0; mantissa[0] matches (both 1), so `--answer.exp` makes it **-1**
- `answer.mantissa[0] = y - x`
- Result: **`exp = -1`, `mantissa = [y-x, 0, …]`**

All intra-subspace deletion widths have `exp = -1`.

---

### Direction 1: Delete in text subspace → effect on link crums

Delete at `[1.1, 1.4)`. Blade[0] = `[1,1,…] exp=0`, blade[1] = `[1,4,…] exp=0`, width = `[3,0,…] exp=-1`.

A link crum at absolute V-position `2.1` has V-displacement (relative to root at 0): `[2,1,…] exp=0`.

- `whereoncrum(link_crum, offset, blade[1]=[1,4,…])`: link left edge `2.1 > 1.4` → blade is **TOMYLEFT** of the link crum → `cmp <= ONMYLEFTBORDER` → **case 2**.
- `tumblersub([2,1,… exp=0], [3,… exp=-1])` is called.
- → `tumbleradd([2,1,…], -[3,… exp=-1])` → `abscmp`: `aptr.exp=0 > bptr.exp=-1` → GREATER → `strongsub`:

```c
// tumble.c:544-546
if (bptr->exp(-1) < aptr->exp(0))   // TRUE
    movetumbler(aptr, cptr);         // link displacement returned unchanged
    return(0);
```

**Link crum displacement is unchanged. The guard fires.** ✓

---

### Direction 2: Delete in link subspace → effect on text crums

Delete at `[2.1, 2.4)`. Blade[0] = `[2,1,…] exp=0`, blade[1] = `[2,4,…] exp=0`.

A text crum at V-position `1.1`, right edge `1.2`.

`deletecutsectionnd` [edit.c:235-248]:

- i=1, `whereoncrum(text_crum, offset, blade[1]=[2,4,…])`:
  - left = `1.1 < 2.4`, right = `1.2 < 2.4` → blade is TOMYRIGHT of crum (address > right edge) → returns **TOMYRIGHT**
  - Not THRUME, not `<= ONMYLEFTBORDER` → continue.
- i=0, `whereoncrum(text_crum, offset, blade[0]=[2.1])`:
  - Same: right edge `1.2 < 2.1` → **TOMYRIGHT** → continue.
- Loop ends. Return **0**.

**Case 0: `tumblersub` is never called on the text crum.** The guard is never reached. Text crums at `1.x` are always to the LEFT of any `2.x` knife boundary — `whereoncrum` returns TOMYRIGHT for both blades, landing in case 0 every time.

---

### The asymmetry, precisely stated

| Scenario | Mechanism | Guard fires? |
|---|---|---|
| Delete `[1.x, 1.y)` → link crum at `2.z` | `strongsub` exponent guard: `bptr.exp=-1 < aptr.exp=0` → crum unchanged | **Yes** |
| Delete `[2.x, 2.y)` → text crum at `1.z` | `deletecutsectionnd` case 0 → `tumblersub` never called | **Never reached** |

The guard is **not symmetric**. It operates in only one direction — protecting integer-exponent (`exp=0`) V-displacements from sub-integer (`exp=-1`) deletion widths. The other direction of isolation is provided entirely by the spatial ordering of V-space: since all text positions (`1.x`) are numerically less than all link positions (`2.x`), text crums always fall to the LEFT of any link-subspace cut (`deletecutsectionnd` case 0), and the `tumblersub`/`strongsub` call chain is never entered for them.

The guard can be said to protect "higher-exponent entries from lower-exponent widths" (your framing is correct for the direction it covers). It does not need to protect in the reverse direction — and structurally cannot, since text crums are never candidates for case 2 shifting during link-space deletions.
