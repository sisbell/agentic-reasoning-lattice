## Question 2 [evidence]

> Does the udanax-green allocator ever produce child-depth tumblers (TA5(d) with k' > 0) for text content, or is sibling increment the exclusive allocation mode for byte-level text?

## KB Synthesis

## Allocator Mode for Text Content: KB Synthesis

The KB is consistent on this point. **Sibling increment (rightshift=0) is the exclusive allocation mode for byte-level text I-addresses.**

### Evidence

**`findisatoinsertmolecule` always uses rightshift=0:**

From [SS-ADDRESS-SPACE/Finding 0061]:
> `findpreviousisagr` returns the highest existing I-address, then `tumblerincrement(&lowerbound, 0, 1, isaptr)` increments by 1 at position 0 — the last significant digit. No depth expansion.

From [ST-INSERT/Finding 0031]:
> `tumblerincrement(&lsa, 0, textset->length, &lsa)` advances the I-address by the text byte count at rightshift=0.

From [SS-ADDRESS-SPACE/Finding 0065] (link atoms, same function, same mechanism):
> "Otherwise, increment from lowerbound by `0.1`" — still pure sibling increment.

### The Allocation/Non-Molecule Distinction

Depth-aware (`k' > 0`) allocation **only appears in `findisatoinsertnonmolecule`**, used for document and link-orgl addresses [SS-ADDRESS-ALLOC/Finding 0021]:
> `upperbound = tumblerincrement(hintisa, depth-1, 1)` — here `depth=2` for ACCOUNT→DOCUMENT, producing child-level addresses.

Text atoms use `findisatoinsertmolecule` with a document-scoped upper bound, then unconditionally apply `tumblerincrement(..., 0, 1, ...)`.

### The "First Atom" Case

[SS-ADDRESS-SPACE/Finding 0077] shows the resulting text address structure as `docISA.3.0.1.N` (e.g., `1.1.0.1.0.1.3.0.1.1`). The initial address for the first text atom is established by the hint mechanism in `makehint(DOCUMENT, ATOM, TEXTATOM, ...)`, but the KB does not document this bootstrap step using depth > 0 in the increment call itself — subsequent atoms monotonically increment from there at rightshift=0 [SS-ADDRESS-SPACE/Finding 0033].

### Conclusion

The KB contains no evidence of `findisatoinsertmolecule` ever producing child-depth tumblers (k' > 0) for text content. Sibling increment at the last significant digit is the sole documented allocation mechanism. The depth-expanding path is reserved for structural (non-molecule) entities: documents, versions, and link orgls [SS-ADDRESS-SPACE/Finding 0021, SS-ADDRESS-ALLOC/Finding 0068].

---

## Code Exploration

Now I have all I need. Here is the full answer.

---

## Does the Text Allocator Ever Produce Child-Depth Tumblers?

**Short answer: Yes — but only once per document, for the very first text insertion. All subsequent byte-level addressing uses sibling increment exclusively.**

---

### The Mechanism: `tumblerincrement` and `rightshift`

The pivot is `tumblerincrement` in `tumble.c:599`:

```c
int tumblerincrement(tumbler *aptr, INT rightshift, INT bint, tumbler *cptr)
```

At `tumble.c:621`:
```c
cptr->mantissa[idx + rightshift] += bint;
```

`idx` is the index of the most-significant non-zero mantissa position. `rightshift` slides the addition to a higher-index (less-significant) slot:

- **`rightshift = 0`** — adds at the same slot as the current tip → **sibling increment** (same tumbler depth, k' unchanged)
- **`rightshift > 0`** — adds at a deeper slot → **child-depth increment** (k' increases by `rightshift`)

This single parameter controls whether allocation descends in the address tree or advances laterally.

---

### The Call Chain for Text Insertion

```
fns.c: insert()
  └─ do1.c:117: makehint(DOCUMENT, ATOM, TEXTATOM, docisaptr, &hint)
  └─ do1.c:118: inserttextingranf() → granf2.c: inserttextgr()
       └─ granf2.c:92:  findisatoinsertgr()
            └─ granf2.c:135: if (hintptr->subtype == ATOM) → findisatoinsertmolecule()
       └─ granf2.c:100: tumblerincrement(&lsa, 0, textset->length, &lsa)  [byte advance]
```

The hint at `do1.c:117` fixes `subtype=ATOM` and `atomtype=TEXTATOM=1` (from `xanadu.h:143–145`). This routes the granfilade lookup exclusively through `findisatoinsertmolecule`.

---

### Inside `findisatoinsertmolecule` (granf2.c:158)

This function finds where in the ISA space to begin inserting. `upperbound` is set to `hintisa.0.0.(TEXTATOM+1)` — the ceiling of the text-atom range for this document. `findpreviousisagr` then scans the granfilade to find the highest existing ISA below that ceiling, returning it in `lowerbound`.

Three branches follow:

**Branch 1 — First-ever text insertion into a document (granf2.c:165–167):**

```c
if (tumblerlength (&hintptr->hintisa) == tumblerlength (&lowerbound)) {
    tumblerincrement (&lowerbound, 2, hintptr->atomtype, isaptr);   // rightshift=2 → CHILD
    tumblerincrement (isaptr, 1, 1, isaptr);                         // rightshift=1 → CHILD
}
```

Condition: the lowerbound has the same tumbler length as the document address — meaning `findpreviousisagr` never descended below the document level, so nothing has ever been allocated there. The code descends **two levels** (`rightshift=2`) then **one more** (`rightshift=1`) to produce the initial byte address. These are unambiguously child-depth increments (TA5(d) with k' > 0).

**Branch 2 — Subsequent text insertions, TEXTATOM (granf2.c:168–169):**

```c
} else if (hintptr->atomtype == TEXTATOM) {
    tumblerincrement (&lowerbound, 0, 1, isaptr);   // rightshift=0 → SIBLING
```

Condition: `lowerbound` is at greater depth than the document, meaning prior text exists. The next ISA is one sibling past the last existing byte. Pure sibling increment.

**Branch 3 — LINKATOM (granf2.c:170–175):** Not relevant to text; `LINKATOM=2` uses its own child calculation.

---

### Byte-Level Advance Within a Text Block (granf2.c:100)

After `findisatoinsertmolecule` sets the starting ISA, `inserttextgr` steps through multi-segment text:

```c
for (; textset; textset = textset->next) {
    insertseq ((typecuc*)fullcrumptr, &lsa, &locinfo);
    tumblerincrement (&lsa, 0, textset->length, &lsa);   // rightshift=0 → SIBLING
}
```

Each segment of length N advances `lsa` by N siblings. No depth change ever occurs here.

The same pattern appears in `findlastisaincbcgr` at `granf2.c:283`, which recomputes the last ISA of an existing text node:

```c
if (ptr->cinfo.infotype == GRANTEXT)
    tumblerincrement (offset, 0, (INT) ptr->cinfo.granstuff.textstuff.textlength - 1, offset);
```

Again `rightshift=0`.

---

### Summary Table

| Situation | Function | `rightshift` | Depth change |
|---|---|---|---|
| First text into fresh document | `findisatoinsertmolecule` L165–167 | 2, then 1 | **Child-depth** (k' > 0) |
| Next text insert (prior text exists) | `findisatoinsertmolecule` L169 | 0 | Sibling |
| Byte advance within a text block | `inserttextgr` L100 | 0 | Sibling |
| Recomputing last ISA of existing text | `findlastisaincbcgr` L283 | 0 | Sibling |

---

### Conclusion

Sibling increment is **not** the exclusive allocation mode. The allocator produces child-depth tumblers (TA5(d), k' > 0) for text content in exactly one case: **Branch 1 of `findisatoinsertmolecule`**, which fires when a document's text space has never been written. The two-step descent (`rightshift=2` then `rightshift=1`) produces the initial byte address by going deeper than the document node. Once that anchor exists, every subsequent text operation — whether finding the next available ISA or advancing through a multi-segment insert — is a `rightshift=0` sibling increment at the established depth.
