## Question 1 [evidence]

> Is `findnextlinkvsa`'s hardcoded `2.1` first link VSA structurally fixed by the data format (like the LINKATOM=2 constants in `xanadu.h:144–146`), or is it a configurable convention?

## KB Synthesis

The `2.1` first link VSA is effectively structurally fixed, but through **code-level hardcoding** rather than storage-layer enforcement — placing it in the same category as `LINKATOM=2`, not in some softer "configurable convention" tier.

## Why it's fixed, not configurable

**It mirrors the I-address element field.** [SS-ADDRESS-SPACE] (Finding 0065) shows link I-addresses are allocated under element subspace `2` of their home document — the full structure is `docISA.0.2.N`. The V-space `2.x` convention directly mirrors this. Both are hardcoded in the allocation machinery (`makehint(DOCUMENT, ATOM, LINKATOM, ...)` with `LINKATOM=2`), so they move together or break.

**`setlinkvsas()` hardcodes it symmetrically with `LINKATOM`.** [SS-DUAL-ENFILADE] (Finding 0038) and [SS-LINK-SUBSPACE] (Finding 0052) confirm that `setlinkvsas()` hardcodes mantissa[0] values of 1, 2, and 3 for FROM, TO, and THREE endpoints respectively — the same numeric constants as `TEXTATOM=1`, `LINKATOM=2` in `xanadu.h:145–146`. The code comment in `findaddressofsecondcutforinsert` even names `2.1` explicitly: "needs this to give it a place to find intersection of for text is 2.1."

**The two-blade knife depends on it.** [SS-TWO-BLADE-KNIFE] and [FC-SUBSPACE] (Finding 0054) show that INSERT's subspace isolation is mechanically enforced because `findaddressofsecondcutforinsert()` computes blade[1] = `(N+1).1` for insertion at `N.x`. Text insertion at `1.x` gets blade[1] = `2.1` — the link subspace start — as its ceiling. Changing the link subspace from `2.x` to any other `N.x` would require coordinating changes to this blade computation.

## The key distinction from pure enforced structure

Unlike `LINKATOM=2` in a named header constant, the `2.1` first link VSA is *computed* at runtime via tumbler increment operations in `findnextlinkvsa()`. And [INV-SUBSPACE-CONVENTION] (Findings 0010, 0049) establishes that the storage layer is entirely type-agnostic — `acceptablevsa()` always returns `TRUE`, so nothing prevents a caller from placing text at `2.x` or links at `1.x`. The convention is caller-enforced.

**Bottom line:** The `2.1` first link VSA is hardcoded by the same mechanism as `LINKATOM=2` — embedded in call sequences and algorithms rather than a named constant — but equally non-configurable. Changing it requires coordinated changes to `findnextlinkvsa`, `setlinkvsas`, `findaddressofsecondcutforinsert`, the I-address allocation hint, and the spanf indexing subspace constants. It is convention, but a convention so deeply woven into the implementation's arithmetic that it is structurally fixed in practice.

---

## Code Exploration

I now have all the evidence needed. Here is the complete answer.

---

## Answer: `findnextlinkvsa`'s `2.1` is structurally fixed by the data format — but the linkage is implicit, not symbolic.

### The construction of `2.1`

`findnextlinkvsa` (`do2.c:151–167`) builds `firstlink = 2.1` as two successive `tumblerincrement` calls on a zero tumbler:

```c
// do2.c:156–158
tumblerclear(&firstlink);
tumblerincrement(&firstlink, 0, 2, &firstlink);  // sets mantissa[0] = 2  → tumbler "2"
tumblerincrement(&firstlink, 1, 1, &firstlink);  // sets mantissa[1] = 1  → tumbler "2.1"
```

Neither `2` nor `1` is referenced by name. They are bare integer literals.

---

### What fixes the `2`

`xanadu.h:144–146`:
```c
/* atom types - don't change these */
#define TEXTATOM  1
#define LINKATOM  2
```

The `/* don't change these */` comment is the explicit structural warning. `LINKATOM=2` is the atom-type discriminant used throughout the granfilade to partition the ISA address space:

- In `granf2.c:165–176`, `findisatoinsertmolecule` places a new molecule's ISA address at `hintptr->atomtype` in the third position:
  ```c
  // granf2.c:166–167
  tumblerincrement(&lowerbound, 2, hintptr->atomtype, isaptr);  // → atomtype at depth 2
  tumblerincrement(isaptr, 1, 1, isaptr);                       // → append .1
  ```
  For `LINKATOM`, `hintptr->atomtype = 2`, so new link atoms land at ISA addresses beginning with `2.x`.

- In `do1.c:180` and `do1.c:207`, `makehint(DOCUMENT, ATOM, LINKATOM, ...)` passes `LINKATOM` as `atomtype` into this very logic.

So the `2` in `findnextlinkvsa`'s floor is **the same `LINKATOM=2`** that partitions the granfilade ISA namespace: text atoms live at `1.x`, link atoms at `2.x`. The floor prevents a link from being allocated into the text partition of the parent document's VSA space.

Changing `LINKATOM` from 2 to any other value would require changing the `2` in `findnextlinkvsa` in lockstep — the data format enforces this even though the code does not.

---

### What fixes the `.1`

The `.1` is the **first valid sub-position** in the tumbler address space. Tumblers in udanax-green are 1-indexed at each level (you cannot have a `2.0` atom; the first item is `2.1`). This is confirmed independently by:

- `setlinkvsas` (`do2.c:169–183`), which assigns fixed VSA positions to a link's three end-sets:
  ```c
  // do2.c:172–173  (from end-set = 1.1)
  tumblerincrement(fromvsaptr, 0, 1, fromvsaptr);
  tumblerincrement(fromvsaptr, 1, 1, fromvsaptr);
  // do2.c:175–176  (to end-set = 2.1)
  tumblerincrement(tovsaptr, 0, 2, tovsaptr);
  tumblerincrement(tovsaptr, 1, 1, tovsaptr);
  // do2.c:179–180  (three end-set = 3.1)
  tumblerincrement(threevsaptr, 0, 3, threevsaptr);
  tumblerincrement(threevsaptr, 1, 1, threevsaptr);
  ```

- `granf2.c:167`: every new molecule ISA starts with `tumblerincrement(isaptr, 1, 1, isaptr)` — the `.1` sub-position is always appended as the first item.

- `insertnd.c:175`: the comment `/*needs this to give it a place to find intersectionof for text is 2.1*/` treats `2.1` as a known fixed landmark — it is the boundary where text space ends.

---

### Summary

| Component | Fixed by | Evidence |
|-----------|----------|---------|
| `2` | `LINKATOM=2` in `xanadu.h:146`, "don't change" annotation; granfilade ISA space partition | `granf2.c:166`, `do1.c:180,207` |
| `.1` | Tumbler 1-indexing convention; first sub-position at every ISA level | `granf2.c:167`, `setlinkvsas` at `do2.c:172–180` |

The `2.1` is **structurally fixed by the data format** — changing either component would corrupt the granfilade's atom-type partitioning or break the 1-indexed tumbler invariant. It is the same constraint as `LINKATOM=2`, just expressed as a bare literal instead of a named constant. Unlike `LINKATOM`, there is no `#define FIRSTLINKVSA` guarding the value — the coupling is implicit, which makes it more brittle, but no less fixed.
