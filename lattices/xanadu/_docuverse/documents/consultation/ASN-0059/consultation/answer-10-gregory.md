## Question 10 [gregory]

> How does `findaddressofsecondcutforinsert` compute the second blade tumbler from the insertion V-address — does it increment the first mantissa digit (e.g., V:1.3 → blade at 2.0), or does it use a different rule when the insertion is deeper in the tumbler hierarchy (e.g., V:1.1.0.2.0.5)?

## KB Synthesis

## How `findaddressofsecondcutforinsert` Computes the Second Blade

The algorithm always produces `(N+1).1` where `N` is the **first mantissa digit** (the subspace digit) of the insertion address — regardless of how deep the tumbler is. [SS-TWO-BLADE-KNIFE]

### The Four-Step Algorithm

For an insertion at V-address `N.x` (where `.x` may be arbitrarily long, e.g., `1.1.0.2.0.5`):

1. **Increment first digit**: `N.x → (N+1).x`  
2. **Behead** (strip first digit to get fractional tail): `N.x → 0.x`  
3. **Subtract fractional part**: `(N+1).x − 0.x = (N+1).0`  
4. **Add 1 at second digit**: `(N+1).0 → (N+1).1`

Steps 2–3 strip the entire fractional tail regardless of its length. Only the first digit survives.

### Concrete Examples

| Insertion address | N | Second blade |
|---|---|---|
| `1.3` | 1 | `2.1` |
| `1.1.0.2.0.5` | 1 | `2.1` |
| `2.5` | 2 | `3.1` |
| `3.7` | 3 | `4.1` |

The source comment confirms the design intent: *"needs this to give it a place to find intersectionof for text is 2.1"* — for all text-subspace insertions (first digit = 1), the blade is always `2.1`, regardless of fractional depth. [SS-TWO-BLADE-KNIFE]

### Significance

This means the shift region `[blade[0], blade[1])` is always bounded to the current subspace. An insertion at `1.1.0.2.0.5` shifts only entries in `[1.1.0.2.0.5, 2.1)` — entirely within the text subspace — and never touches link entries at `2.x`. This is the structural mechanism behind [FC-SUBSPACE]'s subspace isolation guarantee for INSERT.

---

## Code Exploration

I have everything needed. Here is the complete answer.

---

## How `findaddressofsecondcutforinsert` computes the second blade

### The function (insertnd.c:174–183)

```c
int findaddressofsecondcutforinsert(tumbler *position, tumbler *secondcut)
{    /*needs this to give it a place to find intersectionof for text is 2.1*/
  tumbler zero, intpart;

       tumblerclear (&zero);
       tumblerincrement (position, -1, 1, secondcut);   // line 179
       beheadtumbler (position, &intpart);              // line 180
       tumblerincrement(secondcut,0,-tumblerintdiff(&intpart,&zero),secondcut); // line 181
       tumblerincrement (secondcut, 1, 1, secondcut);   // line 182
}
```

Called from `makegappm` [insertnd.c:145] which places the first blade at the raw insertion V-address and asks this function to compute the second. The caller:

```c
movetumbler (&origin->dsas[V], &knives.blades[0]);
findaddressofsecondcutforinsert(&origin->dsas[V],&knives.blades[1]);
```

---

### Tumbler representation

`mantissa[0]` is the most-significant digit (highest level), `mantissa[1]` the next, etc. `exp = 0` for normal addresses. `nstories` = index of last non-zero digit + 1. So V:1.3 → `mantissa=[1,3,0,…]`, V:1.1.0.2.0.5 → `mantissa=[1,1,0,2,0,5,0,…]`.

`tumblerincrement(aptr, rightshift, bint, cptr)` [tumble.c:599–622]:
- Finds `idx` = index of the last non-zero mantissa digit [tumble.c:611]
- Adds `bint` to `mantissa[idx + rightshift]` [tumble.c:621]
- `rightshift = -1` → modifies the digit **one slot left** of the last digit (the parent level)
- `rightshift = 0` → modifies the last digit itself
- `rightshift = +1` → writes a **new sub-digit** one slot right of the last digit

`beheadtumbler(aptr, bptr)` [tumble.c:673–683]: strips the first digit, returning the remainder. For V:1.3 → returns 3. For V:1.1.0.2.0.5 → returns 1.0.2.0.5.

`tumblerintdiff(aptr, bptr)` [tumble.c:591–597]: returns `(a−b).mantissa[0]`, i.e. the first digit of the difference. Used here with `bptr = zero`, so it just returns `intpart.mantissa[0]` = the second digit of `position`.

---

### Step-by-step trace for V:1.3

`position = [1, 3, 0, …]`, `idx` of last non-zero = 1.

**Line 179** — `tumblerincrement(position, −1, 1, secondcut)`:
- `idx = 1`, add 1 to `mantissa[1−1] = mantissa[0]`
- `secondcut = [2, 3, 0, …]` = V:2.3

**Line 180** — `beheadtumbler(position, &intpart)`:
- Zeros `mantissa[0]` of position, justifies → `intpart = [3, 0, …]` = 3
- `tumblerintdiff(intpart, zero)` = 3

**Line 181** — `tumblerincrement(secondcut, 0, −3, secondcut)`:
- `secondcut = [2, 3, 0, …]`, `idx = 1`
- Add −3 to `mantissa[1]`: 3 − 3 = 0
- `secondcut = [2, 0, …]` = 2

**Line 182** — `tumblerincrement(secondcut, +1, 1, secondcut)`:
- `secondcut = [2, 0, …]`, `idx = 0`
- Add 1 to `mantissa[1]`
- `secondcut = [2, 1, 0, …]` = V:2.1

**Result: V:1.3 → second blade at V:2.1**, matching the embedded comment.

For any two-level address V:M.N (any N): line 179 increments `mantissa[0]` to M+1 (because rightshift=-1 on idx=1 hits index 0); line 181 then subtracts exactly N from the last digit, zeroing it; line 182 appends .1. **The final digit N is always cancelled out.** The result is V:(M+1).1 regardless of N.

---

### Step-by-step trace for V:1.1.0.2.0.5

`position = [1, 1, 0, 2, 0, 5, 0, …]`, last non-zero at `idx = 5`.

**Line 179** — `tumblerincrement(position, −1, 1, secondcut)`:
- `idx = 5`, add 1 to `mantissa[5−1] = mantissa[4]`
- `mantissa[4]` was 0, becomes 1
- `secondcut = [1, 1, 0, 2, 1, 5, 0, …]`

**Line 180** — `beheadtumbler([1,1,0,2,0,5,…], &intpart)`:
- Zeros `mantissa[0]`, justifies: `intpart = [1, 0, 2, 0, 5, …]` = 1.0.2.0.5
- `tumblerintdiff(intpart, zero)` = **1** (= `position`'s second digit, `d₂`)

**Line 181** — `tumblerincrement(secondcut, 0, −1, secondcut)`:
- `secondcut = [1, 1, 0, 2, 1, 5, …]`, `idx = 5`
- Add −1 to `mantissa[5]`: 5 − 1 = 4
- `secondcut = [1, 1, 0, 2, 1, 4, 0, …]`

**Line 182** — `tumblerincrement(secondcut, +1, 1, secondcut)`:
- `idx = 5`, add 1 to `mantissa[6]`
- `secondcut = [1, 1, 0, 2, 1, 4, 1, 0, …]`

**Result: V:1.1.0.2.0.5 → second blade at V:1.1.0.2.1.4.1**

This is a 7-level tumbler. The algorithm does **not** touch the first digit at all for deep tumblers.

---

### General rule for a k-level tumbler V:d₁.d₂.d₃…dₖ

Let `idx = k−1` (zero-based index of last non-zero digit).

| Step | Operation | Net effect on mantissa |
|---|---|---|
| Line 179 | `rightshift=−1` on idx | `mantissa[k−2] += 1` (penultimate digit++) |
| Line 180 | behead position | `intpart.mantissa[0] = d₂` |
| Line 181 | `rightshift=0`, add `−d₂` | `mantissa[k−1] −= d₂` (last digit adjusted) |
| Line 182 | `rightshift=+1`, add 1 | new `mantissa[k] = 1` (new sub-digit appended) |

The second blade is:

```
V: d₁ . d₂ . … . d_{k-2} . (d_{k-1}+1) . (d_k − d₂) . 1
```

(with a special case when `d_k − d₂ = 0`: the zero digit collapses and the .1 lands one level higher.)

For **two-level** V:M.N: `d₁=M`, `d₂=N`, `k=2`, `d_{k−1}=d₁=M`, `d_k=d₂=N`:
- Penultimate = `mantissa[0]` → M+1
- Last digit: N − N = 0 (collapses)
- Appended .1 lands at index 1
- **Result: V:(M+1).1** — the last digit is always erased, first digit incremented

For **deep** V:1.1.0.2.0.5: `d₂=1`, penultimate `d₅=0→1`, last `d₆=5→4`, appended .1:
- **Result: V:1.1.0.2.1.4.1** — the first digit is untouched; the second-to-last digit is bumped, the last digit shrinks by `d₂`, then `.1` is appended

### Summary

The function does **not** simply increment the first mantissa digit. The "increment first digit, reset to .1" shorthand is only accurate for two-level (one-dot) tumblers. For deeper tumblers the rule is: **increment the penultimate digit, subtract the second digit from the last digit, append .1**. The amount subtracted at line 181 is always `d₂` — the digit immediately after the top-level digit of the original insertion address. For deep tumblers where `d₂ < d_k`, this creates a compound sub-address at the end rather than collapsing it cleanly to .1.
