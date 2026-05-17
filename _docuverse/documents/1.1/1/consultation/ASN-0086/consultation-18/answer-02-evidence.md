## Question 2 [evidence]

> In udanax-green, what are the literal first-element-field subspace identifiers for content addresses and link addresses (i.e., what are the concrete values of `s_C` and `s_L` in the substrate's tumbler conventions)?

## KB Synthesis

The concrete values are:

- **`s_C` = 1** — the text/content subspace occupies V-addresses `1.x`
- **`s_L` = 2** — the link-orgl-reference subspace occupies V-addresses `2.x`
- There is a third: **`s_T` = 3** — the link type-endpoint subspace occupies V-addresses `3.x`

These values are encoded in mantissa[0] of the V-address tumbler. [SS-SUBSPACE-CONVENTION] (Finding 0038) states the three-subspace convention explicitly: `1` = text, `2` = link, `3` = link type endpoint, hardcoded in `setlinkvsas()` at `do2.c:169-183`.

[SS-DUAL-ENFILADE] (Finding 0009) confirms: `findnextlinkvsa()` constructs the first link position at `2.1`. [SS-TWO-BLADE-KNIFE] (Finding 0054) reveals the structural enforcement — INSERT at `N.x` places `blade[1]` at `(N+1).1`, so:
- INSERT at `1.x` → shift region `[1.x, 2.1)` → text only
- INSERT at `2.x` → shift region `[2.x, 3.1)` → links only

Note these are **V-space** subspace identifiers. The I-address (element-field) assignments are reversed: element-field `2` = links, element-field `3` = text, per [SS-ADDRESS-SPACE] (Finding 0065).

---

## Code Exploration

## Answer

In udanax-green, the literal first-element-field subspace identifiers are:

> **s_C = 1** (content/text)  
> **s_L = 2** (link)

These values appear consistently at two levels of the system.

---

### Level 1: V-space (within a document's POOM)

Text content occupies V-positions whose first mantissa element is **1** (the `1.x` subspace). Link references occupy V-positions whose first mantissa element is **2** (the `2.x` subspace).

**`findnextlinkvsa` in `do2.c:151-167`:**
```c
tumblerclear (&firstlink);
tumblerincrement (&firstlink, 0, 2, &firstlink);  // → 2
tumblerincrement (&firstlink, 1, 1, &firstlink);  // → 2.1
```
The first link reference in any document is placed at V = `2.1`. mantissa[0] = **2**.

**`findvsatoappend` in `orglinks.c:29-48`:**
```c
tumblerincrement (vsaptr, 0, 1, vsaptr);  // → 1
tumblerincrement (vsaptr, 1, 1, vsaptr);  // → 1.1
```
Text content in an empty document starts at V = `1.1`. mantissa[0] = **1**.

**`islinkcrum` in `orglinks.c:255-260`:**
```c
if (crumptr->cdsp.dsas[V].mantissa[0] == 1 && crumptr->cdsp.dsas[V].mantissa[1] != 0) {
    /* tumbler is a 1.n tumbler where n != 0 */
    return TRUE;
}
```
The `1.n` (n≠0) V-displacement pattern for link crums arises because their *absolute* V-position is `2.x`, but their *relative displacement* from the end of the text region (which ends near `1.n`) is `1.something`. The first mantissa digit of the absolute V-position is still **2**.

**`istextcrum` in `orglinks.c:246-252`:**
```c
if (crumptr->cdsp.dsas[V].mantissa[1] == 0 && is1story(&crumptr->cwid.dsas[V])) {
    return TRUE;
}
```
Text crums have a single-element V-displacement (mantissa[1]==0), consistent with living in the `1.x` range.

---

### Level 2: I-space (granfilade ISAs)

The atom type constants are declared in `xanadu.h:144-146`:
```c
#define TEXTATOM  1
#define LINKATOM  2
```

`findisatoinsertmolecule` in `granf2.c:158-181` uses these to partition the granfilade address space relative to each document ISA:

```c
tumblerincrement (&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound);
// TEXTATOM (1): upperbound = docISA.0.0.2
// LINKATOM (2): upperbound = docISA.0.0.3
```

For **LINKATOM** (link creation), the starting address is computed explicitly:
```c
} else if (hintptr->atomtype == LINKATOM) {
    tumblerincrement (&hintptr->hintisa, 2, 2, isaptr);   // → docISA.0.0.2
    if (tumblercmp (&lowerbound, isaptr) == LESS)
        tumblerincrement (isaptr, 1, 1, isaptr);           // → docISA.0.0.2.1
    ...
}
```
The `2` (LINKATOM) is the first digit of the extension — the link subspace element.

For **TEXTATOM** (text content), atoms are allocated from the global granfilade floor up to the `docISA.0.0.2` boundary, with no explicit subspace prefix written — the bound enforcer is still `2` as the ceiling.

**Golden-test confirmation** — from `golden/links/create_link.json`:
```json
{"op": "create_document", "result": "1.1.0.1.0.1"},
{"op": "create_link",     "result": "1.1.0.1.0.1.0.2.1"}
```
The link ISA extends the document ISA (`1.1.0.1.0.1`) by `.0.2.1`. The `.0` is the separator (two positions of tumblerincrement right-shift); the **2** is the LINKATOM subspace field; the **1** is the serial number within that subspace. First mantissa element of the extension: **2**.

Finding 0038 (`findings/0038-poom-subspace-independence.md`) codifies this explicitly:
> "mantissa[0] = 1 → text subspace; mantissa[0] = 2 → link subspace"

---

### Summary

| Subspace | Symbol | Concrete value | Code constant | Address form (I-space) | Address form (V-space) |
|---|---|---|---|---|---|
| Content (text) | s_C | **1** | `TEXTATOM 1` [`xanadu.h:145`] | `docISA … ≤ .0.0.2` ceiling | `1.x` |
| Link | s_L | **2** | `LINKATOM 2` [`xanadu.h:146`] | `docISA.0.0.2.serial` | `2.x` |

The distinction is concrete and mechanical: every link ISA embeds the digit `2` two positions after the owning document's ISA terminus (`granf2.c:171`), and every link V-position in a document POOM starts with mantissa[0] = 2 (`do2.c:157`).
