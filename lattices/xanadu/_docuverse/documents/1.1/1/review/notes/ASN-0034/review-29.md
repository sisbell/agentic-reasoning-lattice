# Proof Verification: T7

Now I have the full T7 proof. Let me verify it carefully.

The proof splits into two cases based on whether `pₐ = pᵦ` (position of the first element-field component in each tumbler).

**Case 1** (`pₐ = pᵦ`): Straightforward — the tumblers differ at position `pₐ` because `Eₐ₁ ≠ Eᵦ₁`, so `a ≠ b` by T3. Sound.

**Case 2** (`pₐ ≠ pᵦ`): This is where the problem lies.

The proof's Case 2(ii) claims that when position `pₐ` in `b` is a field component (not a separator), then `b[pₐ − 1] > 0`. The parenthetical argues this by saying: "if `b[pₐ − 1]` were a separator, then `pₐ` would be the start of a field in `b`, but `pₐ < pᵦ` means `pₐ` is not the start of `b`'s element field, and the only field that starts after the third separator is the element field."

This reasoning fails to rule out `b[pₐ − 1]` being b's **first or second** separator. The parenthetical only addresses the third separator (element field start), but `pₐ` could be the start of b's user or document field.

**Concrete counterexample to the intermediate claim:**

```
a = [1, 0, 1, 0, 1, 0, 1, 2, 3, 4, 5]   (α=1, β=1, γ=1, δ=5)
    zeros at positions 2, 4, 6.  pₐ = 7.  Eₐ₁ = 1.

b = [1, 2, 3, 4, 5, 0, 1, 0, 1, 0, 2]   (α'=5, β'=1, γ'=1, δ'=1)
    zeros at positions 6, 8, 10. pᵦ = 11. Eᵦ₁ = 2.
```

Here `pₐ = 7 < 11 = pᵦ`. Position 7 in `b` is `b[7] = 1` (user field component), so we are in Case 2(ii). The proof claims `b[pₐ − 1] = b[6] > 0`, but `b[6] = 0` — it is b's **first** separator. Both `a[6] = 0` and `b[6] = 0`, so the proof's argument that they differ at position `pₐ − 1` fails.

(The tumblers are still distinct — they differ at position 2 where `a[2] = 0` and `b[2] = 2` — but the proof's stated reasoning doesn't establish this.)

```
RESULT: FOUND

**Problem**: Case 2(ii) incorrectly claims `b[pₐ − 1] > 0`. The parenthetical only rules out `b[pₐ − 1]` being the third separator (which would make `pₐ = pᵦ`), but `b[pₐ − 1]` can be b's first or second separator. Counterexample: `a = [1,0,1,0,1,0,1,2,3,4,5]` and `b = [1,2,3,4,5,0,1,0,1,0,2]` — both have `a[6] = 0 = b[6]`, defeating the argument at position `pₐ − 1 = 6`.

**Required**: Replace the Case 2(ii) argument. A correct approach: if `pₐ ≠ pᵦ`, the three zero-position sets of `a` and `b` cannot all agree (equal zero positions at `α+1, α+β+2, α+β+γ+3` would force `α=α', β=β', γ=γ'`, hence `pₐ = pᵦ`, contradicting the case hypothesis). Therefore there exists a position where one tumbler has a separator (0) and the other has a field component (> 0, by T4's positive-component constraint), giving `a ≠ b` by T3.
```
