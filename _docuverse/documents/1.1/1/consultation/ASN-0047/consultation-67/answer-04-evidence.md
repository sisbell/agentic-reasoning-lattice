## Question 4 [evidence]

> Are TEXTATOM=1 and LINKATOM=2 in xanadu.h hardcoded in a way that other parts of the protocol depend on these specific values (e.g., sort order, dispatch tables), or are they configurable constants whose specific numerical values are incidental?

## KB Synthesis

The KB provides enough evidence to give a definitive answer, though with one important nuance.

## TEXTATOM=1 and LINKATOM=2 Are Load-Bearing, Not Incidental

### Where the values are structurally consumed

**I-address allocation bounds** — the critical site is in `findisatoinsertmolecule` [SS-ADDRESS-SPACE, Finding 0065]:

```c
tumblerincrement(&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound)
```

With LINKATOM=2, `atomtype + 1 = 3`, so the upper bound becomes `docISA.0.3` — confining link allocation to element field 2. If LINKATOM were changed to 3, the upper bound would shift to field 4, and links would collide with text's element field 3. The specific value **determines which I-address element field links occupy**.

**ENF0 predicate** [PRE-ENF0-PLACEMENT-GAP, Finding 0049]:

```c
may-modify(orgl) ≡ element-type(orgl) ≠ LINKATOM
```

This guard that protects link orgls from mutation compares against the literal constant — it would need updating if the value changed.

### Alignment with V-subspace convention

The V-subspace mantissa[0] values (1 = text, 2 = links, 3 = type endpoints) are **independently hardcoded** in `setlinkvsas()` and `findnextlinkvsa()` [SS-SUBSPACE-CONVENTION, Finding 0038; SS-TWO-BLADE-KNIFE, Finding 0054], not derived from TEXTATOM/LINKATOM. The two-blade knife computes `(N+1).1` dynamically from the insertion position's first digit, never consulting these constants.

However, the alignment is intentional: LINKATOM=2 maps to V-subspace 2.x and I-address element field 2. Changing one without the other would break the correspondence between where links live in V-space and where their orgls are allocated in I-space.

### No dispatch tables

The KB documents no dispatch tables or sort operations that index on TEXTATOM/LINKATOM values numerically. The command dispatch table at `backend/init.c:requestfns` uses FEBE opcodes, not atom type constants [SS-VERSION-ADDRESS, Finding 0032].

### Summary

The values are **not freely configurable** — LINKATOM=2 is structurally entailed by the I-address allocation formula and must agree with the hardcoded V-subspace and element-field conventions. Changing either constant without auditing the `atomtype + 1` arithmetic in `granf2.c` and the hardcoded subspace digits in `do2.c` would break allocation correctness. They are not a dispatch-table key, but they are a load-bearing numeric constant embedded in arithmetic.

---

## Code Exploration

I have everything needed to give a definitive answer. Here it is:

---

## TEXTATOM=1 and LINKATOM=2: Load-Bearing Values

**Short answer:** The specific numeric values are load-bearing. They cannot be changed without corrupting on-disk ISA address arithmetic and breaking the validator. The comment says so, and the code proves it.

---

### Definition

**`backend/xanadu.h:144-146`:**
```c
/* atom types - don't change these */
#define TEXTATOM  1
#define LINKATOM  2
```

The comment "don't change these" is accurate. Here is why.

---

### 1. The Values Drive Tumbler Arithmetic Directly

In `findisatoinsertmolecule`, the integer values of `TEXTATOM` and `LINKATOM` are fed directly as numeric operands into tumbler arithmetic that computes the ISA (permanent address) for a new atom in the granfilade:

**`backend/granf2.c:162`:**
```c
tumblerincrement (&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound);
```

This computes the upper-bound ISA for the search range. The third argument `hintptr->atomtype + 1` evaluates to:
- `2` when atomtype is TEXTATOM (1)
- `3` when atomtype is LINKATOM (2)

**`backend/granf2.c:166`:**
```c
tumblerincrement (&lowerbound, 2, hintptr->atomtype, isaptr);
```

This computes the final ISA address for the new atom. The third argument is `hintptr->atomtype` verbatim — `1` for text atoms, `2` for link atoms. This value is added into the mantissa of the tumbler at position `idx + 2`, so the resulting ISA address *encodes* the atom type's numeric value. The on-disk address layout is directly derived from these constants.

**`backend/granf2.c:171`** (inside the `LINKATOM` branch):
```c
tumblerincrement (&hintptr->hintisa, 2, 2, isaptr);
```

Here the literal `2` appears hardcoded instead of the symbolic `LINKATOM`. It is not coincidental — it mirrors the constant's value, confirming that the numeric value is what matters, not just the symbolic identity.

**Consequence:** If you swapped the values (TEXTATOM=2, LINKATOM=1), the ISA addresses calculated for all existing atoms would shift. Any pre-existing granfilade on disk would be misread. The numeric values are therefore embedded in the on-disk data format, not merely in logic.

---

### 2. The Validator Hardcodes the Literal `2`, Not the Symbol

**`backend/do2.c:93-97`:**
```c
|| (hintptr->atomtype < 0)
|| (hintptr->atomtype > 2)
|| (hintptr->subtype < hintptr->supertype)
|| ((hintptr->subtype - hintptr->supertype) > 1)
|| ((hintptr->subtype == ATOM) == !hintptr->atomtype) ) {
```

The upper-bound check at line 94 uses the literal `2`, not `LINKATOM`. This means the validator has a second, independent encoding of the same bound. If you were to add a third atom type at value 3 by defining `THIRDATOM 3`, the validator would reject it without a separate code change.

The expression `!hintptr->atomtype` at line 97 uses C boolean coercion (zero = false, nonzero = true). It checks that `atomtype` is nonzero when `subtype == ATOM`. This works because both current atom types are nonzero, but it also implies a specific assumption about the zero-vs-nonzero boundary.

---

### 3. No Wire Protocol Transmission

The `typehint` structure (which carries `atomtype`) is **never serialized over the FEBE wire**. Searching `get1fe.c`, `get2fe.c`, `put.c`, and `putfe.c` finds zero references to `atomtype` or `hint`. The hint is constructed internally:

- Text insertions: `makehint(DOCUMENT, ATOM, TEXTATOM, docisaptr, &hint)` — **`backend/do1.c:117`**
- Link creation (2-end): `makehint(DOCUMENT, ATOM, LINKATOM, docisaptr, &hint)` — **`backend/do1.c:180`**
- Link creation (3-end): `makehint(DOCUMENT, ATOM, LINKATOM, docisaptr, &hint)` — **`backend/do1.c:207`**

The distinction between text and link atom types is determined by which operation the client calls (insert vs. createlink), not by any value the client transmits.

---

### 4. No Dispatch Tables — If-Else Chains Only

There are no switch statements or arrays indexed by atom type. The branching in `granf2.c:168-175` is:

```c
} else if (hintptr->atomtype == TEXTATOM) {
        tumblerincrement (&lowerbound, 0, 1, isaptr);
} else if (hintptr->atomtype == LINKATOM) {
    tumblerincrement (&hintptr->hintisa, 2, 2, isaptr);
    ...
}
```

The dispatch is symbolic (`==` comparison), but the arithmetic inside each branch uses the literal `2` (mirroring LINKATOM's value), tying the behavior to the specific numeric value.

---

### Verdict

| Claim | Status |
|---|---|
| Values are used in ISA tumbler arithmetic | **Yes** — `granf2.c:162,166` use `atomtype` as an integer operand |
| Literal `2` appears separately from the symbol | **Yes** — `granf2.c:171`, `do2.c:94` |
| Values are transmitted over the wire | **No** — hint is constructed internally |
| Sort-order dependency on TEXTATOM < LINKATOM | **Yes** — the arithmetic produces different sub-ranges in the ISA space |
| Dispatch tables indexed by value | **No** — if-else chains, not arrays |

TEXTATOM=1 and LINKATOM=2 are **not** incidental. The numeric values are embedded in the granfilade address-space arithmetic at `granf2.c:162` and `granf2.c:166`, reproduced as bare literals at `granf2.c:171` and `do2.c:94`, and would corrupt any existing on-disk data if changed. The comment "don't change these" reflects genuine engineering necessity.
