## Question 4 [evidence]

> Among T4-valid (zeros=3) tumblers, does `θ ≼ c` force the subspace identifier to agree (`E(c)₁ = E(θ)₁`) by field-segment agreement on positions `1..#θ`, and is `T4b`'s `E`-projection defined only on T4-valid tumblers — so that "extension preserves `E₁`" holds for content addresses but fails for T4-invalid extensions like `θ.0.x`?

## KB Synthesis

## Answer

The question turns on three separable claims. Here is what the KB can and cannot confirm.

---

### Claim 1: Among T4-valid tumblers, θ ≼ c forces E(c)₁ = E(θ)₁

**Yes, by the mechanics of containment.** The containment predicate is defined by prefix truncation and equality [SS-TUMBLER-CONTAINMENT]:

```
tumblertruncate(c, tumblerlength(θ)) == θ
```

This means c's first `#θ` digits are identical to θ's digits. A T4-valid tumbler (three `.0.` zero-separator boundaries in the digit sequence, giving the pattern `Node.0.User.0.Doc.0.Element`) has its subspace identifier digit at a fixed position: immediately after the third zero in the mantissa [SS-TUMBLER Finding 0001, SS-DUAL-ENFILADE Finding 0038]. Call that position p.

If both θ and c are T4-valid and θ ≼ c, then `c[p] = θ[p]`, so `E(c)₁ = E(θ)₁`. Field-segment agreement on positions 1..#θ is exactly what the prefix relation enforces.

**Concrete example from the KB** [SS-ADDRESS-SPACE Finding 0065]: document `1.1.0.1.0.1` has its link elements at `1.1.0.1.0.1.0.2.1`, `1.1.0.1.0.1.0.2.2`, etc. Every address under the element-field prefix `1.1.0.1.0.1.0.2` shares `E₁ = 2` (link subspace). Text elements similarly share `E₁ = 1`, and type endpoints `E₁ = 3` [SS-SUBSPACE-CONVENTION Finding 0038].

---

### Claim 2: E-projection is defined only on T4-valid tumblers

**Yes, but by convention, not runtime enforcement.** The KB is explicit that the subspace convention is caller-enforced; `acceptablevsa()` unconditionally returns TRUE [SS-SUBSPACE-CONVENTION Finding 0010, PRE-INSERT Finding 0011]. The storage layer is fully type-agnostic — it stores tumblers without checking whether they have the right number of `.0.` boundaries [SS-DUAL-ENFILADE Finding 0011].

The E-projection (extracting digit p, the first element-field digit) is semantically meaningful only for addresses that have crossed exactly three `.0.` boundaries. A document-level tumbler like `1.1.0.1.0.2` has only two `.0.` boundaries and carries no element field [SS-TUMBLER Finding 0001]. Applying E to it would read a digit that is not an element-subspace identifier but a doc-field digit — the result is not undefined in the arithmetic sense, but it is semantically meaningless in the T4 scheme.

**The spec must make this explicit** because the implementation does not [PRE-SUBSPACE-CONVENTION].

---

### Claim 3: "Extension preserves E₁" holds for content addresses but fails for T4-invalid extensions like θ.0.x

This requires distinguishing two kinds of extension:

**T4-valid extension (no new `.0.` boundary):** If θ is T4-valid (e.g., `1.1.0.1.0.1.0.2`) and c = `θ.k` for some digit k (e.g., `1.1.0.1.0.1.0.2.1`), then c is still T4-valid, θ ≼ c, and `E(c)₁ = E(θ)₁ = 2`. Preservation holds. This is confirmed by the monotonic allocation pattern [SS-ADDRESS-SPACE Finding 0033, Finding 0065]: sequential content I-addresses stay within the same element-field subspace.

**T4-invalid extension (adds a new `.0.` boundary):** If θ = `1.1.0.1.0.1.0.2.1` (T4-valid) and the extension is `θ.0.x` = `1.1.0.1.0.1.0.2.1.0.x`, the result has **four** `.0.` boundaries. It is T4-invalid by definition. The E-projection is undefined on T4-invalid tumblers (Claim 2 above), so the question "does E₁ agree?" cannot be posed. There is no E(`θ.0.x`)₁ to compare against E(θ)₁.

This is not a vacuous dodge: the KB documents real addresses in this form. Version addresses like `1.1.0.1.0.1.1` are document-level children (depth=1, no new `.0.` boundary) [SS-VERSION-ADDRESS Finding 0032], but sub-element addresses like `1.1.0.1.0.1.0.2.1.0.x` would be depth-5 addresses that the system never generates in practice. The `makehint` dispatch [SS-ADDRESS-SPACE Finding 0021] only produces depths 1 and 2, constraining all allocated addresses to T4-valid or shallower forms.

---

### Summary Table

| Case | θ T4-valid? | c T4-valid? | θ ≼ c | E(c)₁ = E(θ)₁? |
|---|---|---|---|---|
| Content address extension (θ.k) | Yes | Yes | Yes | Yes — field-segment agreement |
| Version/sibling address | Shallower than T4 | Shallower than T4 | Yes | E undefined on both |
| θ.0.x extension | Yes | **No** (T4-invalid) | Yes | E(θ.0.x) undefined — question doesn't apply |
| Arbitrary c with θ ≼ c | Yes | Yes | Yes | Yes — by prefix truncation |

**Conclusion:** Within the T4-valid stratum, θ ≼ c entails `E(c)₁ = E(θ)₁` by the prefix property of containment [SS-TUMBLER-CONTAINMENT]. The E-projection is a convention-bound, not enforcement-bound, function restricted to T4-valid tumblers [SS-SUBSPACE-CONVENTION, PRE-SUBSPACE-CONVENTION]. For T4-invalid extensions like θ.0.x, E-projection is simply undefined — the question of preservation collapses, not because preservation fails, but because its domain condition is not met. This asymmetry matters for the spec: preservation must be stated as `(T4-valid(θ) ∧ T4-valid(c) ∧ θ ≼ c) ⟹ E(c)₁ = E(θ)₁`, not as a universally quantified claim over all tumblers.

---

## Code Exploration

Now I have all the source evidence needed. Let me synthesize the complete answer.

---

## Analysis: T4-valid Tumblers, Prefix Ordering, and E-Projection

### 1. Tumbler Structure and the T4 Address Scheme

The tumbler is defined at `common.h:59-65`:

```c
typedef struct structtumbler {
    humber xvartumbler;
    char varandnotfixed;
    char sign BIT;
    short exp;
    tdigit mantissa[NPLACES];   // NPLACES = 16 (common.h:53)
} tumbler;
```

`tdigit` is `UINT` (`uint32_t` — `defs.h:12-13`). Each mantissa "digit" is a 32-bit unsigned integer; zeros in the mantissa encode hierarchical level boundaries. The `exp` field is always ≤ 0 (`tumblercheckptr` at `tumble.c:174-176` rejects `exp > 0`); negative `exp` means leading zeros printed before the mantissa (see `puttumbler`, `put.c:36-37`).

The Xanadu global address hierarchy (ISAs) uses zeros as level separators:

| Level | Address form | Interior zeros |
|-------|-------------|----------------|
| Node | `N` | 0 |
| Account | `N.0.A` | 1 |
| Document | `N.0.A.0.D` | 2 |
| Content | `N.0.A.0.D.0.S.x` | **3** |

where `N`, `A`, `D`, `S`, `x` are one or more non-zero digits. A **T4-valid** tumbler (zeros=3) is a complete content address. The subspace identifier **E₁ = S** is the first digit after the third zero separator. Concretely:

- `TEXTATOM = 1` → S = 1, content at `…0.1.x` (`xanadu.h:145`)
- `LINKATOM = 2` → S = 2, content at `…0.2.x` (`xanadu.h:146`)

The allocation code in `findisatoinsertmolecule` (`granf2.c:158-181`) confirms this:

```c
// upperbound = hintisa.0.(atomtype+1) — always crosses third zero
tumblerincrement(&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound);
```

For a document ISA (zeros=2), `rightshift=2` in `tumblerincrement` (`tumble.c:599-623`) places the increment two positions right of the last non-zero digit, which creates exactly one more zero separator followed by the subspace digit. The first content ISA is always `docISA.0.S.1`, preserving zeros=3. This is consistent with real observed addresses: `1.1.0.1.0.1.0.2.1` (a link ISA, zeros at mantissa positions 2, 4, 6; `S=2` at position 7, Finding 0038).

### 2. The Prefix Ordering θ ≼ c

The prefix ordering is not a named function but is implemented as the combination of `tumblertruncate` + `tumblereq`. From `findisatoinsertnonmolecule` (`granf2.c:228-232`):

```c
tumblertruncate(&lowerbound, hintlength, &truncated);
lowerbound_under_hint = tumblereq(&truncated, &hintptr->hintisa);
```

`tumblertruncate(c, n, result)` (`tumble.c:625-639`) zeroes every mantissa position ≥ n and justifies:

```c
for (; bint < NPLACES; ++bint)
    answer.mantissa[bint] = 0;
tumblerjustify(&answer);
```

So `θ ≼ c` ≡ `tumblertruncate(c, #θ) = θ`, where `#θ = tumblerlength(θ)` (`tumble.c:259-262`). This is exactly **field-segment agreement on positions 1..#θ**: the first `#θ` digits of `c`'s mantissa are identical to θ's.

### 3. Does θ ≼ c Force E(c)₁ = E(θ)₁?

**Yes, for T4-valid c.** Here is why:

Let θ be T4-valid (zeros=3). Its third interior zero is at some mantissa index `p3` (the exact position depends on the digit-group lengths of `N`, `A`, `D`). Then `E(θ)₁ = θ.mantissa[p3+1]`, which is `S` (the subspace identifier). Since `p3 + 1 < #θ` (the element field digit is within θ's significant length), position `p3+1` is within the range `1..#θ`.

If `θ ≼ c`, then `c.mantissa[i] = θ.mantissa[i]` for all `i < #θ`. In particular:

```
c.mantissa[p3+1] = θ.mantissa[p3+1]
```

Therefore `E(c)₁ = E(θ)₁`. The field-segment agreement at positions `1..#θ` is sufficient to force subspace agreement — no further argument is needed.

The comparison machinery that enforces this is in `abscmp` (`tumble.c:99-111`), which compares mantissa arrays element-by-element; `tumblertruncate` zeros positions ≥ #θ without touching anything before them.

### 4. Is T4b's E-Projection Defined Only on T4-Valid Tumblers?

**Yes.** The E-projection locates `E₁` by finding the third interior zero. Its position `p3` in the mantissa array is `tumblerlength(docISA) + 1` — it depends on the length of the *document address* prefix, which is only knowable from the hint structure (`hintptr->hintisa` in `granf2.c:162,165`). There is no fixed mantissa index for `E₁`.

Critically, the backend has **no general function that counts zeros** to validate T4 structure. The commented-out `nzeroesintumbler` (`tumble.c:264-276`) was removed; `tumblercheckptr` (`tumble.c:169-227`) only validates:
- `exp ≤ 0`
- Non-negative digits
- No non-zero digits in an otherwise-zero mantissa

It does **not** check that zeros=3 or that the digit at position `p3+1` is a valid subspace identifier. The T4 structure is a pure convention enforced by allocation logic, not by the type system — consistent with Finding 0011 (Convention over Enforcement).

Therefore:

- For a T4-valid tumbler: `p3` is well-defined, `E₁ = mantissa[p3+1]` is meaningful.
- For a T4-invalid tumbler (zeros ≠ 3): `p3` is wrong or absent; `E₁` is either undefined or points to the wrong position in the mantissa array.

The extraction function is not robust to wrong zeros counts. T4b's E-projection has **T4-valid tumblers as its domain**.

### 5. Does "Extension Preserves E₁" Fail for T4-Invalid Extensions θ.0.x?

Let θ = `N.0.A.0.D.0.S.x` be a T4-valid content address (zeros=3, `E(θ)₁ = S`).

**Valid extension:** c = `N.0.A.0.D.0.S.x.y` (additional digit `y ≠ 0`)
- c has zeros at the same positions p1, p2, p3 as θ
- c is still T4-valid (zeros=3)
- `E(c)₁ = c.mantissa[p3+1] = S = E(θ)₁` ✓

This is the pattern the system actually uses. In `inserttextgr` (`granf2.c:99-101`):

```c
// Advance I-address by text length — stays in same subspace
tumblerincrement(&lsa, 0, textset->length, &lsa);
```

`rightshift=0` extends the final digit group without crossing a zero separator, keeping the tumbler T4-valid.

**Invalid extension:** c = `N.0.A.0.D.0.S.x.0.y` (zero then `y` appended)
- c has zeros at positions p1, p2, p3, and now a new `p4`
- c is **T4-invalid** (zeros=4): it would represent a "fifth level" sub-content address
- T4b E-projection is **undefined on c**: the domain condition fails

If one forces the projection anyway (apply third-zero rule to a 4-zero tumbler), the third zero is still at `p3`, and `c.mantissa[p3+1] = S`. Naively, E₁ appears preserved. But:

1. The tumbler is outside T4b's domain — the proposition "extension preserves E₁" isn't well-formed for c.
2. The system **never creates** such addresses. `findisatoinsertmolecule` always uses `rightshift=2` from a document ISA (`granf2.c:162`), never from a content ISA. `tumblerincrement` with `rightshift=1` creates sub-digit positions (like `1.1` → `1.1.5`) but only within `insertpm`/`inserttextgr` where the starting point is already a valid content address — extending the content position, not the hierarchy.
3. The `tumbler2spanset` function (`do2.c:48-61`) places the ISA in a span using `tumblerlength(isa)-1` as rightshift:
   ```c
   tumblerincrement(&spanptr->width, tumblerlength(tumblerptr)-1, 1, &spanptr->width);
   ```
   A T4-invalid ISA with an extra `.0.y` suffix would have the wrong `tumblerlength`, producing a malformed span width.

The "failure" for θ.0.x is therefore not that `E₁` changes (numerically, it doesn't, since the third zero position is unchanged by appending `.0.y` at the end). The failure is that:

- **θ.0.x exits the domain of T4b E-projection**
- The proposition "E(θ.0.x)₁ = S" is undefined, not false
- The system's downstream code (`findisatoinsertmolecule`, `tumblertruncate`-based containment checks, `retrievecrums` in `retrie.c`) would misinterpret such an address because they assume zeros=3 for content ISAs

The `tumbleraccounteq` function (`tumble.c:38-70`) gives a clue about how robust the zero-counting assumption is: it specifically looks for "two consecutive zeros" to find the account boundary, not a general count. If a T4-invalid address had a fourth interior zero, the traversal logic in `findpreviousisagr` (`granf2.c:255-278`) would cross into the wrong subtree.

---

### Summary

| Question | Answer | Key Evidence |
|----------|--------|-------------|
| Does θ ≼ c force E(c)₁ = E(θ)₁ for T4-valid c? | **Yes** — field-segment agreement on 1..#θ forces it; E₁ sits at p3+1 < #θ | `tumble.c:625-639`, `granf2.c:228-232` |
| Is T4b E-projection defined only on T4-valid tumblers? | **Yes** — E₁ position depends on zeros count; no zeros=3 check exists in the type system; convention-only enforcement | `granf2.c:158-181`, `tumble.c:169-227` |
| Does "extension preserves E₁" fail for θ.0.x? | **Fail by domain**: E is undefined on 4-zero tumblers; the system never creates them; downstream code misinterprets them | `granf2.c:99-101,162`, `do2.c:48-61`, `tumble.c:599-623` |

The deeper point: the T4 address convention is enforced by allocation discipline (`findisatoinsertmolecule` always originates from a document ISA, always adds `atomtype` at `rightshift=2`), not by the tumbler type. A T4-invalid extension θ.0.x is representable as a bit pattern but falls outside the semantic domain — making "extension preserves E₁" vacuously inapplicable, not literally false.
