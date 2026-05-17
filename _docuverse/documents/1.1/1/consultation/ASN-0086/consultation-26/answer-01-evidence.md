## Question 1 [evidence]

> In udanax-green, are `s_C` and `s_L` (or their concrete numeric equivalents in the granfilade/POOM code paths) assigned distinct constant values, and does any code path rely structurally on their inequality (e.g., subspace-dispatch in `findisatoinsertmolecule`)?

## KB Synthesis

Yes and yes, though the KB uses different names for what you're calling `s_C` / `s_L`, and the structural reliance has a significant caveat.

## Constant Identity

The KB records two distinct constant families, depending on which address space is in view.

**V-space (POOM):** The first mantissa digit encodes content type — `1` for text, `2` for link orgls, `3` for link type endpoints. These are hardcoded in `setlinkvsas()` which constructs those V-addresses by explicitly incrementing digit-0 to the corresponding value. [SS-SUBSPACE-CONVENTION, Finding 0038; SS-TWO-BLADE-KNIFE, Finding 0054]

**I-space (granfilade atom types):** `xanadu.h:145-146` defines `TEXTATOM=1` and `LINKATOM=2`. These are the constants the allocation dispatcher consumes. [SS-ADDRESS-SPACE, Finding 0065]

The KB does not record a variable named `s_C` or `s_L`; the closest concrete counterparts are the `atomtype` field values TEXTATOM/LINKATOM, and the V-address mantissa[0] conventions.

## Structural Reliance in `findisatoinsertmolecule`

Yes. Finding 0065 records the critical line:

```c
tumblerincrement(&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound)
```

This computes the upper-bound for the bounded `findpreviousisagr` search:
- TEXTATOM (1) → `atomtype + 1 = 2` → upper bound at element-field 2 of the document ISA
- LINKATOM (2) → `atomtype + 1 = 3` → upper bound at element-field 3

The formula only produces distinct bounded search regions *because* TEXTATOM ≠ LINKATOM. If they were equal, both would query the same sub-namespace — allocation isolation would collapse. This is structural reliance on inequality. [SS-ADDRESS-SPACE, Finding 0065]

INSERT also structurally relies on the V-space inequality: `findaddressofsecondcutforinsert()` computes the second knife blade at `(N+1).1` for any insertion at subspace `N.x`, mechanically relying on text-subspace (`1`) and link-subspace (`2`) being distinct so that the blade at `2.1` cleanly caps the text shift region. [SS-TWO-BLADE-KNIFE, Finding 0054; FC-SUBSPACE, Findings 0054, 0067]

## Important Caveat: Partial Isolation

The `atomtype + 1` bound only governs `findisatoinsertmolecule` (the molecule/content allocation path). Link-orgl creation goes through `createorglingranf` → `findisatoinsertnonmolecule`, which queries the *global* granfilade maximum without the per-type bound. The result is that a CREATELINK between two text INSERTs advances the global maximum I-address, causing the next text INSERT's `findpreviousisagr` to find the link-orgl address and allocate above it — breaking text I-address contiguity. This is directly observable: INSERT "ABC" → CREATELINK → INSERT "DEF" yields two shared span pairs rather than one. [FC-GRANF-ON-DELETE, Finding 0063; INV-MONOTONIC, Finding 0063]

So the inequality `s_C ≠ s_L` creates bounded sub-namespace structure *within* `findisatoinsertmolecule`, but does not prevent cross-type contamination through the non-molecule allocation path.

---

## Code Exploration

---

## Answer: `s_C` / `s_L` and Subspace Dispatch in udanax-green

### Named constants `s_C` and `s_L` do not exist in this codebase.

A thorough search of all `.c` and `.h` files in `backend/` finds no identifiers `s_C` or `s_L`. The theoretical subspace labels map to concrete `#define` constants under different names.

---

### Their Concrete Numeric Equivalents: `TEXTATOM` and `LINKATOM`

```c
// xanadu.h:144-146
/* atom types - don't change these */
#define TEXTATOM  1
#define LINKATOM  2
```

The comment **"don't change these"** is itself an explicit acknowledgment that these values are structurally load-bearing. `TEXTATOM = 1` corresponds to the content subspace (`s_C`); `LINKATOM = 2` to the link subspace (`s_L`).

---

### Does Any Code Path Rely Structurally on Their Inequality?

Yes — **`findisatoinsertmolecule`** in `granf2.c:158-181` depends on `TEXTATOM ≠ LINKATOM` in at least three distinct ways.

#### 1. `atomtype` as a numeric argument to compute the search upperbound (line 162)

```c
tumblerincrement (&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound);
```

`atomtype` is not just a tag here — it is the **numeric magnitude** passed to `tumblerincrement`. The third argument selects the subspace ceiling used in `findpreviousisagr`:

- TEXTATOM (1): upperbound = `hintisa + [depth=2, offset=2]`
- LINKATOM (2): upperbound = `hintisa + [depth=2, offset=3]`

If TEXTATOM == LINKATOM, both atom types would search the same tumbler range — collapsing two distinct address subspaces into one.

#### 2. `atomtype` as a numeric offset to compute the insertion address (line 166)

```c
tumblerincrement (&lowerbound, 2, hintptr->atomtype, isaptr);
```

In the branch where `tumblerlength(&hintptr->hintisa) == tumblerlength(&lowerbound)` (i.e., an existing atom of the same type was found), `atomtype` directly controls **which numeric slot** in the second tumbler dimension the new atom lands in:

- TEXTATOM (1): address lands at depth 2, offset 1
- LINKATOM (2): address lands at depth 2, offset 2

If the two constants were equal, text and link atoms would receive identical addresses.

#### 3. Explicit type-identity dispatch on the constant values (lines 168-175)

```c
} else if (hintptr->atomtype == TEXTATOM) {
    tumblerincrement (&lowerbound, 0, 1, isaptr);
} else if (hintptr->atomtype == LINKATOM) {
    tumblerincrement (&hintptr->hintisa, 2, 2, isaptr);
    if (tumblercmp (&lowerbound, isaptr) == LESS)
        tumblerincrement (isaptr, 1, 1, isaptr);
    else
        tumblerincrement (&lowerbound , 0, 1, isaptr);
}
```

This is a classic subspace-dispatch: the two atom types execute entirely different address-computation strategies when the fallback cases fire. If `TEXTATOM == LINKATOM`, only the first branch could ever match — the link-atom path would be structurally dead code.

---

### Validation Confirms the Two-Value Contract (do2.c:86-97)

```c
int validhint(typehint *hintptr)
{
    if (
          ...
       || (hintptr->atomtype < 0)
       || (hintptr->atomtype > 2)
       ...
       || ((hintptr->subtype == ATOM) == !hintptr->atomtype) ) {
```

`do2.c:94` bounds atomtype to `[0, 2]`. The guard at line 97 (`!hintptr->atomtype`) treats 0 as the "no atom" sentinel, trusting that both TEXTATOM (1) and LINKATOM (2) are truthy. The system thus has exactly three valid states: no-atom (0), content-atom (1), link-atom (2).

---

### Call Sites (do1.c)

```c
// do1.c:117 — text insertion
makehint(DOCUMENT, ATOM, TEXTATOM, docisaptr, &hint);

// do1.c:180,207 — link creation
makehint(DOCUMENT, ATOM, LINKATOM, docisaptr, &hint);
```

These are the two entry points that populate `hint.atomtype` before the granfilade dispatch fires.

---

### Summary

| Constant | Value | Role |
|----------|-------|------|
| `TEXTATOM` (`xanadu.h:145`) | 1 | Content subspace — text atoms |
| `LINKATOM` (`xanadu.h:146`) | 2 | Link subspace — link/orgl atoms |

The names `s_C` and `s_L` do not appear in this codebase. Their concrete equivalents are `TEXTATOM = 1` and `LINKATOM = 2`. Their inequality is structurally required by `findisatoinsertmolecule` (`granf2.c:162–175`) in three ways: (1) `atomtype + 1` as a numeric upperbound discriminator, (2) `atomtype` as a direct numeric slot selector for the insertion ISA, and (3) explicit `== TEXTATOM` / `== LINKATOM` dispatch selecting different address-computation strategies. The source comment at `xanadu.h:144` — *"atom types - don't change these"* — directly acknowledges this structural dependency.
