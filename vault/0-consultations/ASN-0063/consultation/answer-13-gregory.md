## Question 13 [gregory]

> `findisatoinsertnonmolecule` allocates the link's I-address with a bounded upper limit (`docISA.2.3` for links) — what is the significance of that `2.3` bound, and does it mean link I-addresses and text I-addresses occupy non-overlapping ranges within the same document's I-space?

## KB Synthesis

## `docISA.2.3` Bound and I-Space Partitioning

### What the bound means

From [SS-ADDRESS-SPACE] Finding 0065, the upper bound is computed as:

```
tumblerincrement(docISA, 2, LINKATOM+1)  =  tumblerincrement(docISA, 2, 3)
```

This adds digit `3` at the 2nd position past the last significant digit of `docISA` in the mantissa, producing a tumbler like `docISA.0.3`. Because `LINKATOM = 2`, the value `LINKATOM+1 = 3` marks the boundary between link element field (2) and whatever follows. All link orgls for document `D` fall in `[docISA.0.2.1, docISA.0.3)`.

The per-document scoping is explicit: each document has an independent allocation counter within its own link subspace — the same `findisatoinsertmolecule` call bounds its search to `docISA.0.2.x`, so link allocations in document A (`1.1.0.1.0.2`) cannot interfere with link allocations in document B (`1.1.0.1.0.1`). [ST-ADDRESS-ALLOC Finding 0065]

### Do link and text I-addresses occupy non-overlapping ranges?

The concrete addresses in the KB suggest yes — their tumbler representations are in distinct subranges:

- **Link orgls**: `1.1.0.1.0.1.0.2.1`, `1.1.0.1.0.1.0.2.2`, ... — digit 0 at position 6, digit 2 at position 7 [SS-ADDRESS-SPACE Finding 0065]
- **Text content**: `1.1.0.1.0.1.3.0.1.1`, `1.1.0.1.0.1.3.0.1.2`, ... — digit 3 at position 6 [SS-ADDRESS-SPACE Finding 0077]

In the tumbler total order (`0 < 3` at position 6), link ISAs sort strictly below text ISAs for the same document. [SS-ADDRESS-SPACE] Finding 0077 explicitly states: "Both query the same granfilade tree but **search different subtrees**." The spec models this as two independent allocation functions, not a single `Σ.next` counter.

### The contiguity interaction from CREATELINK

There is a complication: [INT-LINK-INSERT] Finding 0063 states that CREATELINK breaks text I-address contiguity:

> `INSERT "ABC" → I.1, I.2, I.3 / CREATELINK → link orgl at ~I.2.0 / INSERT "DEF" → I.2.1+`
> `compare_versions reports 2 shared span pairs (gap between ABC and DEF I-addresses)`

This occurs because both text and link allocation call `findisatoinsertmolecule`, which queries `findpreviousisagr` against the same granfilade tree. Even though their nominal search subtrees are distinct, the link orgl's allocation advances the global maximum in a way that the text allocator observes, pushing subsequent text I-addresses past the link orgl's position.

The set of contiguity-breaking operations is therefore `{INSERT, CREATELINK}` — both call into `findisatoinsertgr` for content — while `CREATENEWVERSION` does not break contiguity because it allocates only a document address via `findisatoinsertnonmolecule`, leaving the content allocation maximum unchanged. [SS-ADDRESS-SPACE Finding 0077]

### Summary

| | Range | Allocated by |
|---|---|---|
| Link orgls | `[docISA.0.2.1, docISA.0.3)` | `findisatoinsertmolecule`, LINKATOM bound |
| Text content | `[docISA.0.1.1, docISA.0.2)` approx. | `findisatoinsertmolecule`, TEXTATOM bound |

The two ranges are non-overlapping in the tumbler address space (link ISAs are numerically below text ISAs for the same document), and `docISA.0.3` serves as the ceiling for the link subspace. However, the shared allocation mechanism means CREATELINK is "visible" to subsequent text allocations — link orgl allocation advances the allocation frontier that `findpreviousisagr` uses for text, causing the non-contiguity observed in `compare_versions`. [INT-LINK-INSERT Finding 0063, SS-ADDRESS-SPACE Finding 0077]

---

## Code Exploration

I now have everything. Here is the complete answer.

---

## The `docISA.2.3` Bound: What It Means and Why It Creates Non-Overlapping I-Space Ranges

### First: A Correction on the Function Name

The `docISA.2.3` bound does **not** live in `findisatoinsertnonmolecule`. That function handles non-ATOM types (DOCUMENT, ACCOUNT, NODE). Links are ATOM-typed and take a different path.

Trace the dispatch in `findisatoinsertgr` [`granf2.c:130-156`]:

```c
if (hintptr->subtype == ATOM) {
    ...
    findisatoinsertmolecule (fullcrumptr, hintptr, isaptr);   // links go HERE
} else {
    findisatoinsertnonmolecule (fullcrumptr, hintptr, isaptr); // documents go here
}
```

The hint for link creation is set in `domakelink`/`docreatelink` [`do1.c:180`, `do1.c:207`]:

```c
makehint (DOCUMENT, ATOM, LINKATOM, docisaptr, &hint);
```

`makehint` sets `hint.subtype = ATOM` [`do2.c:78-84`], so links always route to `findisatoinsertmolecule`, never to `findisatoinsertnonmolecule`.

---

### The `docISA.2.3` Bound in `findisatoinsertmolecule`

The relevant constants [`xanadu.h:144-146`]:

```c
/* atom types - don't change these */
#define TEXTATOM  1
#define LINKATOM  2
```

The comment "don't change these" is load-bearing — their integer values encode the I-space layout.

`findisatoinsertmolecule` [`granf2.c:158-181`]:

```c
static int findisatoinsertmolecule(typecuc *fullcrumptr, typehint *hintptr, typeisa *isaptr)
{
  typeisa upperbound, lowerbound;

    tumblerincrement (&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound);  // line 162
    clear (&lowerbound, sizeof(lowerbound));
    findpreviousisagr ((typecorecrum*)fullcrumptr, &upperbound, &lowerbound);
    if (tumblerlength (&hintptr->hintisa) == tumblerlength (&lowerbound)) {
        tumblerincrement (&lowerbound, 2, hintptr->atomtype, isaptr);
        tumblerincrement (isaptr, 1, 1, isaptr);
    } else if (hintptr->atomtype == TEXTATOM) {
            tumblerincrement (&lowerbound, 0, 1, isaptr);
    } else if (hintptr->atomtype == LINKATOM) {
        tumblerincrement (&hintptr->hintisa, 2, 2, isaptr);         // line 171
        if (tumblercmp (&lowerbound, isaptr) == LESS)
            tumblerincrement (isaptr, 1, 1, isaptr);                // line 173
        else
            tumblerincrement (&lowerbound , 0, 1, isaptr);
    }
}
```

#### What `tumblerincrement(x, rightshift, bint, out)` does

From `tumble.c:599-622`: it takes tumbler `x`, finds the index `idx` of its last non-zero mantissa word, then adds `bint` at position `idx + rightshift`. For a non-zero input tumbler, `rightshift=2` appends two additional dot-components (two zeros then the value). So:

- `tumblerincrement(docISA, 2, 3, &upperbound)` → `upperbound = docISA.0.0.3`
- `tumblerincrement(docISA, 2, 2, &isaptr)` → `isaptr = docISA.0.0.2`
- `tumblerincrement(docISA.0.0.2, 1, 1, &isaptr)` → `isaptr = docISA.0.0.2.0.1`

The notation "docISA.2.3" in the question is shorthand: *depth offset 2, value 3*.

---

### Why Each Part of `2.3` is Significant

**The `2` (rightshift = 2):** Every atom lives two sub-levels below its parent document. This `depth=2` is also why the granfilade search can unambiguously identify whether a found address is "inside" the document's atom space versus at the document level itself — a depth-2 child can never equal the parent.

**The `3` (= `LINKATOM + 1`):** This is an **exclusive** upper bound passed to `findpreviousisagr`. The function finds the greatest ISA strictly less than this bound. Using `atomtype + 1` means each atom type gets a private "lane" of width 1 at the 2-deep sub-level:

| atomtype | exclusive upper bound | effective lane |
|----------|----------------------|----------------|
| `TEXTATOM = 1` | `docISA.0.0.2` | `[docISA, docISA.0.0.2)` |
| `LINKATOM = 2` | `docISA.0.0.3` | `[docISA.0.0.2, docISA.0.0.3)` |

---

### Do Text and Link I-Addresses Overlap?

**No. They are structurally non-overlapping by the encoding of `atomtype`.**

For text insertion, `findisatoinsertmolecule` searches with `upperbound = docISA.0.0.2` and places new text at `lowerbound + 1` (at depth 0 relative to lowerbound, i.e., `rightshift=0`). Text ISA addresses are therefore strictly less than `docISA.0.0.2`.

For link insertion, the minimum candidate address is computed at [`granf2.c:171`]:
```c
tumblerincrement (&hintptr->hintisa, 2, 2, isaptr);  // = docISA.0.0.2
```
If no links exist yet (`lowerbound < docISA.0.0.2`), the first link gets [`granf2.c:173`]:
```c
tumblerincrement (isaptr, 1, 1, isaptr);  // = docISA.0.0.2.0.1
```

`docISA.0.0.2.0.1` is a child of `docISA.0.0.2` and in tumbler ordering is strictly **greater than** `docISA.0.0.2` (and thus strictly greater than any text ISA, which must be less than `docISA.0.0.2`). Subsequent links increment from the last link's address using `rightshift=0` (same depth), staying within `[docISA.0.0.2.0.1, docISA.0.0.3)`.

So the I-space partition within a document is:

```
[docISA]               — the document orgl itself (placed by findisatoinsertnonmolecule)
[docISA, docISA.0.0.2) — TEXT atom range (exclusive upper bound = docISA.0.0.2)
[docISA.0.0.2.0.1, docISA.0.0.3) — LINK atom range (starts at first child of docISA.0.0.2)
```

These ranges are non-overlapping. The gap between text's ceiling (`docISA.0.0.2`) and the link floor (`docISA.0.0.2.0.1`) is the address `docISA.0.0.2` itself — which is never assigned to either type, serving as a structural separator.

---

### Summary

The `docISA.2.3` bound encodes two design decisions simultaneously:
1. **Depth 2** (`rightshift=2`): atom I-addresses live two sub-levels below their document, ensuring no atom ISA can equal its containing document's ISA.
2. **Value 3** (`LINKATOM + 1`): the `atomtype` integer (with `TEXTATOM=1`, `LINKATOM=2`) is used as a partition key at that depth. The `+1` makes the search exclusive so each type gets its own lane. This is why `xanadu.h:144` says **"don't change these"** — changing `LINKATOM` or `TEXTATOM` would shift the partition boundaries and corrupt the layout of existing stored documents.
