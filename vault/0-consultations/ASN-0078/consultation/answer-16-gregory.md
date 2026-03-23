## Question 16 [gregory]

> The link's I-address allocation advances past the text range, creating gaps for subsequent text inserts — is this because link and text I-addresses share a single allocation namespace under `docISA.0.1.x` vs `docISA.0.2.x`, or is the gap an artifact of how `findisatoinsertmolecule` scans?

## KB Synthesis

Both factors are at play, but the scan behavior of `findisatoinsertmolecule` is the proximate cause.

## Address Structure: Separate Element Subspaces

Link and text I-addresses do occupy different element_field subspaces within the document's content region [SS-ADDRESS-SPACE Finding 0065]:

- Links: `docISA.0.2.x` (element_field = 2)
- Text: `docISA.0.3.x` (element_field = 3, based on Finding 0033's `2.1.0.1.0.1.3.x` pattern)

So the `docISA.0.1.x` vs `docISA.0.2.x` framing in the question is close but off by one — it's element_field 2 (links) vs element_field 3 (text). They are nominally in different subspaces.

## Why the Gap Occurs Anyway

The gap is an artifact of the scan. Both text INSERT and CREATELINK call `findisatoinsertmolecule` on the **same global granfilade** [INT-LINK-INSERT, Finding 0063]. The mechanism is stateless query-and-increment: `findpreviousisagr` finds the highest existing I-address **below the caller's upper bound**, then increments by 1.

The critical detail [SS-ADDRESS-SPACE Finding 0077]:

> Allocation is stateless query-and-increment on **different tumbler ranges** via `findpreviousisagr`.

For MAKELINK, the upper bound is computed as `tumblerincrement(docISA, 2, atomtype+1)` where LINKATOM = 2, giving an upper bound in the element_field 3 region — i.e., the same upper bound range that text allocation uses [SS-ADDRESS-SPACE Finding 0065, code]. This means the text allocator's upper bound scan **encompasses the link element subspace** (element_field 2 is below element_field 3 in tumbler order).

After CREATELINK allocates at, say, `docISA.0.2.3`, `findpreviousisagr` for the next text INSERT finds `docISA.0.2.3` as the highest I-address below the text upper bound. It increments to `docISA.0.2.4` — now squarely in the link subspace, and non-contiguous with the previous text run at `docISA.0.3.x`.

The KB states this directly [INT-LINK-INSERT, Finding 0063]:

> "link orgls and text characters share the same allocation sequence... all allocations (text and non-text) draw from the same monotonically increasing sequence"

And [INV-MONOTONIC, Finding 0063]:

> `text_contiguous(insert_a, insert_b) ⟺ ¬∃ alloc_c : time(a) < time(c) < time(b) ∧ alloc_c ∈ content_allocations`

The content allocation set is `{INSERT, COPY, CREATELINK}` — both TEXTATOM and LINKATOM allocations are in scope. CREATENEWVERSION, by contrast, does **not** call `findisatoinsertmolecule` for content (it only allocates a document address via `findisatoinsertnonmolecule`), which is why it does not break text contiguity [INV-MONOTONIC, Finding 0077].

## Summary

The subspaces are nominally distinct (element_field 2 vs 3), so this is not a case of sharing one flat namespace. The gap arises because the text allocator's upper bound for `findpreviousisagr` is set broadly enough to include the link I-address subspace. After CREATELINK, `findpreviousisagr` legitimately finds the link orgl as the current maximum within the scan range and increments from there — a scan artifact, not a shared-counter artifact [SS-ADDRESS-SPACE Finding 0077, INV-MONOTONIC Finding 0063, INT-LINK-INSERT Finding 0063].

---

## Code Exploration

Now I have everything I need. Let me compile the complete answer from the code analysis and empirical data.

---

## Answer

The question contains a partially correct premise. Here is the full picture, traced from the code.

---

### The Namespace Structure: `docISA.0.1.x` for Text, `docISA.0.2.x` for Links

Both text atoms and link atoms are stored in the **same global `granf`** and both go through `findisatoinsertmolecule` [granf2.c:158–181]. The **only** architectural distinction is `hint.atomtype`:

- Text insert [`do1.c:117`]: `makehint(DOCUMENT, ATOM, TEXTATOM, docisaptr, &hint)` → `atomtype = 1`
- Link creation [`do1.c:207`]: `makehint(DOCUMENT, ATOM, LINKATOM, docisaptr, &hint)` → `atomtype = 2`

Both values are defined in [`xanadu.h:145–146`]:
```c
#define TEXTATOM  1
#define LINKATOM  2
```

Inside `findisatoinsertmolecule` [`granf2.c:162`], the **upperbound** for the `findpreviousisagr` scan is:

```c
tumblerincrement (&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound);
```

With `docISA = 1.1.0.1.0.1` (mantissa `[1,1,0,1,0,1,0,…]`, last non-zero at position 5 = idx):

| atomtype | rightshift | bint | upperbound | formula |
|----------|-----------|------|------------|---------|
| TEXTATOM=1 | 2 | 2 | mantissa[7]=2 → `1.1.0.1.0.1.0.2` | `docISA.0.2` |
| LINKATOM=2 | 2 | 3 | mantissa[7]=3 → `1.1.0.1.0.1.0.3` | `docISA.0.3` |

The scan boundaries are separated by exactly one tumbler digit.

---

### How the First Address in Each Subspace Is Assigned

**First text character** — the granfilade is empty except for the doc orgl at `docISA`. `findpreviousisagr` with upper bound `docISA.0.2` returns `lowerbound = docISA` (the doc orgl itself). `tumblerlength(docISA) == tumblerlength(lowerbound)` (both 6), so the **first branch** fires [`granf2.c:165–167`]:

```c
tumblerincrement (&lowerbound, 2, hintptr->atomtype, isaptr);   // docISA.0.1 (atomtype=1)
tumblerincrement (isaptr, 1, 1, isaptr);                        // docISA.0.1.1
```

Tracing: idx=5 in `docISA`, rightshift=2, bint=1 → mantissa[7]=1 → `1.1.0.1.0.1.0.1`. Then rightshift=1, bint=1 → idx=7, mantissa[8]=1 → **`1.1.0.1.0.1.0.1.1`** = `docISA.0.1.1`.

Subsequent text characters increment from lowerbound via `tumblerincrement(&lowerbound, 0, 1, isaptr)` [`granf2.c:169`]: each successive insert yields `docISA.0.1.2`, `docISA.0.1.3`, `docISA.0.1.4`, …

**First link** — after "ABC" at `docISA.0.1.{1,2,3}`, `findpreviousisagr` with upper bound `docISA.0.3` returns `lowerbound = docISA.0.1.3`. `tumblerlength` is 9 ≠ 6, so the **LINKATOM branch** fires [`granf2.c:171–175`]:

```c
tumblerincrement (&hintptr->hintisa, 2, 2, isaptr);   // docISA.0.2
if (tumblercmp (&lowerbound, isaptr) == LESS)          // docISA.0.1.3 < docISA.0.2? YES (pos7: 1<2)
    tumblerincrement (isaptr, 1, 1, isaptr);           // docISA.0.2.1
```

idx=7 (value 2 in `docISA.0.2`), rightshift=1, bint=1 → mantissa[8]=1 → **`1.1.0.1.0.1.0.2.1`** = `docISA.0.2.1`.

This matches the empirically confirmed link ISA in the golden test [`golden/internal/insert_link_insert_iaddress_gap.json:17`]:
```json
"result": "1.1.0.1.0.1.0.2.1"
```
and in Finding 0065's table (L1 in doc `1.1.0.1.0.1` → ISA `1.1.0.1.0.1.0.2.1`).

---

### Does Link Allocation Create a Gap for Subsequent Text?

**No.** This is where the question's premise needs correction.

After CREATELINK inserts the link orgl at `docISA.0.2.1`, the **text allocator's upper bound is still `docISA.0.2`**. The link orgl at `docISA.0.2.1` satisfies:

```
docISA.0.2.1  vs  docISA.0.2:
  mantissa[0..7] equal ([1,1,0,1,0,1,0,2])
  mantissa[8]: 1 > 0  → docISA.0.2.1 > docISA.0.2
```

The link orgl is **above** the text upper bound. `findpreviousisagr` for the next text insert finds only the text chars at `docISA.0.1.x` (all < `docISA.0.2`) and the doc orgl at `docISA` — not the link. The result:

```
lowerbound = docISA.0.1.3  (last text char, ABC)
tumblerincrement(docISA.0.1.3, 0, 1) → docISA.0.1.4  (next text ISA)
```

**Text allocation resumes contiguously at `docISA.0.1.4`.** The link at `docISA.0.2.1` is invisible to the text allocator.

---

### Then Why Does `compare_versions` Show 2 Span Pairs?

The 2-pair result in the golden test is a **V-space artifact**, not evidence of an I-address gap.

After CREATELINK, the document's vspanset is consolidated to include the link subspace (V-position 2.x). `findnextlinkvsa` [`do2.c:151–167`] computes the document's full vspan reach:

```c
(void) doretrievedocvspan (taskptr, docisaptr, &vspan);
tumbleradd (&vspan.stream, &vspan.width, &vspanreach);
if (tumblercmp (&vspanreach, &firstlink) == LESS)
    movetumbler (&firstlink, vsaptr);
else
    movetumbler (&vspanreach, vsaptr);
```

The `retrievedocvspanset` output after CREATELINK is `[{start: 0, width: 0.1}, {start: 1, width: 1}]` (per Finding 0038). The document's total V-reach is now ~2.x. When the test inserts "DEF" "at end", the client places it at V-position ~2 (beyond the link reference at 2.1). "DEF" in the **source** document ends up at V-positions in the 2.x range, while in the version **dest** (without the link), "DEF" sits at V-position 1.4.

`compare_versions` maps shared I-spans back to V-positions in each document. With DEF at different V-positions (source: 2.x, dest: 1.4), the return is two span pairs — one for ABC, one for DEF — even though the underlying I-addresses `docISA.0.1.1`–`docISA.0.1.6` are fully contiguous in the granfilade.

---

### Summary

| Question | Answer |
|----------|--------|
| Do text and link I-addresses share a single allocation namespace? | **Yes** — both go through `findisatoinsertmolecule` in the global `granf` |
| Are they in distinct subspaces? | **Yes** — text at `docISA.0.1.x`, links at `docISA.0.2.x`, encoded by `atomtype` directly into the ISA |
| Is the subspace assignment a `findisatoinsertmolecule` artifact? | They are the same thing — the scan's atomtype-dependent upperbound [`granf2.c:162`] **is** the namespace structure |
| Does link allocation create a gap for subsequent text? | **No** — the text upperbound `docISA.0.2` fences out `docISA.0.2.x` (link subspace), so text continues monotonically in `docISA.0.1.x` |
| What causes the 2-span-pair result in compare_versions? | V-space displacement — "at end" text inserts land at V-position 2.x (after the link reference), creating a V-space gap between ABC (1.x) and DEF (2.x) in the source document |

The mechanism is a **shared namespace with strict subspace isolation** — both framings in the question describe the same design. The `atomtype` field (TEXTATOM=1, LINKATOM=2) is injected into the ISA at mantissa position 7 via [`granf2.c:162`]'s `tumblerincrement`, creating non-overlapping ranges. `findisatoinsertmolecule`'s bounded scan enforces that isolation on every allocation. The "gap" the question observes is in V-space (POOM), not in the granfilade I-address sequence.
