## Question 8 [evidence]

> Does udanax-green's content-emission path always produce content addresses with first element-field s_C, and is there any code path that can emit content into a non-s_C subspace?

## KB Synthesis

## Content Emission and Subspace Placement in udanax-green

The answer splits across two independent address spaces: I-addresses (where content bytes are allocated in the permascroll) and V-addresses (where those I-addresses are referenced within a document's POOM).

### I-address allocation: s_C is enforced

For text insertion, `doinsert` calls `makehint(DOCUMENT, ATOM, TEXTATOM, docisaptr, &hint)` before invoking `inserttextingranf`. This hint hardwires element-type TEXTATOM, causing allocation to target the document's text I-address subspace (element_field 3, e.g., `doc.3.0.1.x`). The allocation mechanism (`findisatoinsertmolecule`) uses a document-scoped upper bound that keeps all text allocations within this subspace. [SS-ADDRESS-SPACE, PRE-ENF0-PLACEMENT-GAP]

CREATELINK uses LINKATOM, which allocates into element_field 2 (`doc.2.2.x`). Text and link I-address allocations are partitioned by the hint's element-type and never interleave. [SS-ADDRESS-SPACE, SS-LINK-SUBSPACE]

So in I-space: text content always lands in the 3-subspace, link orgls always in the 2-subspace. The hint mechanism enforces this.

### V-address placement: s_C is NOT enforced

The V-position where a content I-address is stored in the POOM is **unconstrained**. `acceptablevsa()` at `do2.c:110-113` unconditionally returns `TRUE`. [SS-SUBSPACE-CONVENTION, PRE-INSERT]

Two confirmed violation paths exist:

**Via INSERT**: Text content can be placed at V-position 2.x (the link subspace). Finding 0049 demonstrates INSERT at V:2.1 with text succeeds — the TEXTATOM I-address is allocated in element_field 3 (correct), but `docopy` places it at the link subspace V-position (violation). `acceptablevsa` is the intended guard but is a stub. [PRE-ENF0-PLACEMENT-GAP, PRE-INSERT]

**Via REARRANGE**: Pivot or swap with cut points spanning a subspace boundary displaces content from 1.x into 2.x. `rearrangend()` calls `tumbleradd` on V-displacements with no subspace check. Finding 0051 confirms "ABC" correctly at V:1.1–1.3 ends up at V:2.2–2.4 after pivot `[1.1, 1.4, 2.5]`. [PRE-REARRANGE, SS-SUBSPACE-CONVENTION]

INSERT at text positions is protected from *shifting* link-subspace entries by the two-blade knife (`findaddressofsecondcutforinsert` always sets `blade[1] = (N+1).1`), so existing 2.x entries are never accidentally shifted. But this does not prevent *placing* new text at 2.x. [SS-TWO-BLADE-KNIFE, FC-SUBSPACE]

### Summary

| Path | I-address subspace | V-address subspace | Enforced? |
|------|-------------------|-------------------|-----------|
| `doinsert` (normal) | element_field 3 ✓ | 1.x (text) | I-addr yes; V-addr no |
| `doinsert` at wrong V | element_field 3 ✓ | 2.x (link) — violation | No |
| REARRANGE cross-subspace | unchanged ✓ | may cross to 2.x — violation | No |
| CREATELINK | element_field 2 ✓ | 2.x (link) ✓ | Yes (by convention) |

The convention `∀ v ∈ doc.vspan : type(content_at(v)) == TEXT ⟹ v.head == 1` must appear as a `requires` clause on every operation in the formal spec; the backend provides no runtime enforcement of it. [INV-SUBSPACE-CONVENTION, PRE-SUBSPACE-CONVENTION]

---

## Code Exploration

I now have everything needed for a complete answer. Let me synthesize the code findings.

---

## Answer: Content-Emission Path and s_C Subspace

### What "first element-field s_C" means in this codebase

In T4 tumbler notation, addresses have four `.0.`-separated fields:

```
1.1  .0.  1  .0.  1  .0.  1.1
Node      Acct     Doc     Element
```

For content I-addresses (granfilade ISAs), the **element field** (4th field) encodes both type and position. Its **first sub-component** identifies the type subspace:
- `1` = TEXTATOM = text/content subspace (`s_C`)
- `2` = LINKATOM = link-orgl subspace

This directly parallels V-space subspaces (Finding 0038): text at V-position `1.x`, links at `2.x`. `s_C = 1` is the content subspace.

---

### The content-emission path: always s_C

The full chain for `doinsert`:

**`do1.c:117`** — `makehint` hardcodes `TEXTATOM = 1`:
```c
makehint(DOCUMENT, ATOM, TEXTATOM, docisaptr, &hint);
```
`hint.atomtype = 1`. This flows directly into `findisatoinsertmolecule`.

**`granf2.c:162`** — upper-bound calculation uses `atomtype + 1`:
```c
tumblerincrement(&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound);
// For TEXTATOM: position idx+2, value 2 → docisa.0.2
// Searches granfilade below docisa.0.2
```

**`granf2.c:165-167`** — branch when document already exists (normal case):
```c
if (tumblerlength(&hintptr->hintisa) == tumblerlength(&lowerbound)) {
    tumblerincrement(&lowerbound, 2, hintptr->atomtype, isaptr);  // docisa.0.1
    tumblerincrement(isaptr, 1, 1, isaptr);                       // docisa.0.1.N
}
```

**`granf2.c:168-169`** — TEXTATOM branch for subsequent inserts:
```c
} else if (hintptr->atomtype == TEXTATOM) {
    tumblerincrement(&lowerbound, 0, 1, isaptr);  // increment from last text ISA
}
```

**Result for document `1.1.0.1.0.1`:**
- First text insert → ISA = `1.1.0.1.0.1.0.1.1` (element field = `1.1`)
- Subsequent text → `1.1.0.1.0.1.0.1.2`, `.0.1.3`, etc.
- Element field always starts with `1` = TEXTATOM = s_C ✓

---

### Link orgls: deliberately NOT s_C

`docreatelink` at **`do1.c:207`** hardcodes `LINKATOM = 2`:
```c
makehint(DOCUMENT, ATOM, LINKATOM, docisaptr, &hint);
```

In `findisatoinsertmolecule` at **`granf2.c:170-175`** (LINKATOM branch):
```c
} else if (hintptr->atomtype == LINKATOM) {
    tumblerincrement(&hintptr->hintisa, 2, 2, isaptr);  // docisa.0.2
    if (tumblercmp(&lowerbound, isaptr) == LESS)
        tumblerincrement(isaptr, 1, 1, isaptr);         // docisa.0.2.N
    else
        tumblerincrement(&lowerbound, 0, 1, isaptr);
}
```

**Link ISA = `1.1.0.1.0.1.0.2.1`** (element field = `2.1`). This is confirmed by every golden test:
```json
"result": "1.1.0.1.0.1.0.2.1"  // golden/links/create_link.json
```

This is intentional — link orgls are in a separate type subspace from text content.

---

### Can any code path emit content into a non-s_C subspace?

**No, not through the content-emission path.** Three lines that prevent it:

1. **`do1.c:117`** — `atomtype = TEXTATOM` is a literal constant, not a caller parameter. There is no FEBE operation that calls `inserttextingranf` with any atomtype other than `TEXTATOM`.

2. **`granf2.c:130-156`** — `findisatoinsertgr` only ever calls `findisatoinsertmolecule` or `findisatoinsertnonmolecule`. Neither can place text at `atomtype = 2` when called from the text path, because the hint's atomtype is fixed before entering these functions.

3. **`granf2.c:154`** — `tumblerjustify(isaptr)` normalizes the result but cannot change its subspace component.

**Critical distinction (Finding 0049 re-examined):**

The FEBE INSERT operation does NOT validate the V-position against the subspace. `acceptablevsa()` at `do2.c:110` always returns TRUE:
```c
bool acceptablevsa(tumbler *vsaptr, typeorgl orglptr) {
    return (TRUE);
}
```

This means a client CAN insert text at **V-position `2.1`** (link subspace virtual address) — confirmed by `golden/links/insert_text_at_link_subspace.json`:
```json
{ "op": "insert", "address": "2.1", "text": "TextAtLinkPosition", "succeeded": true }
```

**However, this is a V-space placement, not an I-space subspace violation.** The text's **I-address** is still allocated by `findisatoinsertmolecule` with `TEXTATOM = 1`, placing the content at `docisa.0.1.X` in the granfilade — still in s_C. Only the V→I mapping is placed in the "wrong" V-subspace. The text bytes themselves remain in s_C at the I-address level.

---

### Summary

| Operation | I-address subspace | V-subspace |
|-----------|-------------------|------------|
| `doinsert` | Always s_C (TEXTATOM=1) | Caller-controlled; **no validation** |
| `docreatelink` | Always s_L (LINKATOM=2) | 2.x (link positions), correctly enforced |

**The content-emission path (`doinsert` → `inserttextingranf` → `findisatoinsertmolecule`) invariably produces I-addresses with first sub-component of the element field = 1 (= TEXTATOM = s_C)**, because `atomtype` is hardcoded at `do1.c:117` and propagates unchanged through every allocator branch.

No code path exists that emits text content into the LINKATOM (2) subspace at the I-address level. The apparent "subspace violation" in Finding 0049 is a V-space placement anomaly only — the content identity address remains in s_C regardless of what V-position the caller specifies.

**Code citations:**
- Atomtype hardcoded: `do1.c:117`
- I-address upper bound search: `granf2.c:162`
- TEXTATOM allocation branches: `granf2.c:165-169`
- LINKATOM allocation branches: `granf2.c:170-175`
- V-position validation stub: `do2.c:110-113`
- Link ISA evidence: `golden/links/create_link.json:63`
- V-space subspace injection possible: `golden/links/insert_text_at_link_subspace.json:39-43`
