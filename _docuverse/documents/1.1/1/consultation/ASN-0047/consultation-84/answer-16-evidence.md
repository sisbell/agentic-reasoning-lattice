## Question 16 [evidence]

> What is the first content address and first link address that udanax-green produces under a freshly created document — does the implementation deterministically emit `[d.0.1.1]` and `[d.0.2.1]`, or can the first emission vary?

## KB Synthesis

## First Link Address: Deterministic at `d.0.2.1`

Yes — the first link address is deterministically `d.0.2.1`. The allocation algorithm in `findisatoinsertmolecule` queries the granfilade for the highest existing link I-address below an upper bound scoped to the document. On an empty link subspace, the sentinel test `lowerbound < docISA.2.2` succeeds and the result is always the first child: `docISA.0.2.1` [SS-ADDRESS-ALLOC Finding 0065, concrete example].

```
Document 1.1.0.1.0.1 → first link: 1.1.0.1.0.1.0.2.1
Document 1.1.0.1.0.2 → first link: 1.1.0.1.0.2.0.2.1
```

Independent per-document, monotonically allocated, never influenced by cross-document activity [SS-ADDRESS-ALLOC Finding 0065].

---

## First Content Address: NOT `d.0.1.1` — KB Evidence Points to Element Field 3

The KB cannot confirm `d.0.1.1` for text content. Two sources contradict it:

**Finding 0065** [SS-ADDRESS-ALLOC] explicitly states: *"element_field is 2 for links and 3 for text."*

**Finding 0077** [SS-ADDRESS-SPACE] diagrams the first content I-address for document `1.1.0.1.0.1` as `1.1.0.1.0.1.3.0.1.1` (field-3 structure, not `d.0.1.N`).

**Finding 0033** [SS-ADDRESS-SPACE] gives the concrete allocation sequence: before any inserts the highest I-address in the document's content region is `D.3.0`; first insert produces `D.3.1`. The field-3 pattern appears consistently.

---

## The Inconsistency Worth Flagging

There is a structural inference that would predict `d.0.1.1`. The upper-bound computation [SS-ADDRESS-ALLOC Finding 0065] uses `tumblerincrement(docISA, rightshift=2, atomtype+1)`:

| Type | atomtype | bint | Effective field below bound |
|------|----------|------|-----------------------------|
| TEXTATOM | 1 | 2 | field 1 → `d.0.1.N` |
| LINKATOM | 2 | 3 | field 2 → `d.0.2.N` ✓ |

By this logic, text should emit `d.0.1.1`. But this contradicts Finding 0065's explicit "field 3 for text" and the concrete `D.3.N` examples in Findings 0033 and 0077. The KB is inconsistent on this point — either there is a labeling error in Finding 0065's field-numbering claim, or text allocation uses a different `makehint` depth that bypasses the `.0.X.N` pattern.

**Bottom line:** `d.0.2.1` for first link — confirmed. First content address — the KB evidence points to element field 3 (`d.3.0.1.1` or `D.3.1` in the concrete examples), not field 1. The `d.0.1.1` hypothesis cannot be confirmed from the KB.

---

## Code Exploration

I now have full code coverage and empirical confirmation. Here is the complete analysis.

---

## Answer: First Content and Link Address Generation in udanax-green

**Short answer:** Yes — fully deterministic. A freshly created document always receives first content ISA `[d.0.1.1]` and first link ISA `[d.0.2.1]`, where `d` is the document's address. These values are hardwired by the constants `TEXTATOM=1` and `LINKATOM=2` in `xanadu.h:145-146`, with no counters, randomization, or file-system state that can alter them.

---

## Constants

`backend/xanadu.h:140-146`:
```c
#define NODE      1
#define ACCOUNT   2
#define DOCUMENT  3
#define ATOM      4

#define TEXTATOM  1
#define LINKATOM  2
```

These are the only inputs that vary between a text insertion and a link creation.

---

## Call Chain: First Content Insertion

```
fns.c:84    insert()
do1.c:117     makehint(DOCUMENT, ATOM, TEXTATOM, docisaptr, &hint)
do1.c:118     inserttextingranf(taskptr, granf, &hint, textset, &ispanset)
granf2.c:83     inserttextgr(...)
granf2.c:92       findisatoinsertgr(fullcrumptr, hintptr, &lsa)
granf2.c:130        → hintptr->subtype == ATOM (4) → findisatoinsertmolecule(...)
```

**`findisatoinsertmolecule`** [`granf2.c:158-181`]:

```c
static int findisatoinsertmolecule(typecuc *fullcrumptr, typehint *hintptr, typeisa *isaptr)
{
  typeisa upperbound, lowerbound;

    tumblerincrement (&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound);
    // TEXTATOM+1 = 2 → upperbound = docisa.0.2 (two places right of last digit)

    clear (&lowerbound, sizeof(lowerbound));
    findpreviousisagr ((typecorecrum*)fullcrumptr, &upperbound, &lowerbound);
    // Finds last ISA in granfilade strictly < docisa.0.2
    // For a fresh document, the only entry is the document orgl at docisa itself

    if (tumblerlength (&hintptr->hintisa) == tumblerlength (&lowerbound)) {
    // docisa and lowerbound are the same tumbler → lengths equal → TRUE
        tumblerincrement (&lowerbound, 2, hintptr->atomtype, isaptr);  // docisa.0.1
        tumblerincrement (isaptr, 1, 1, isaptr);                       // docisa.0.1.1
```

**Trace for `d = 1.1.0.1.0.1`** (6 digits, last nonzero at mantissa index 5):

| Step | Call | Result |
|------|------|--------|
| 1 | `tumblerincrement(docisa, 2, TEXTATOM=1, isaptr)` | `mantissa[5+2] += 1` → `1.1.0.1.0.1.0.1` |
| 2 | `tumblerincrement(isaptr, 1, 1, isaptr)` | `mantissa[7+1] += 1` → `1.1.0.1.0.1.0.1.1` |

**First content ISA = `docisa.0.1.1` = `[d.0.1.1]`** [`granf2.c:166-167`].

---

## Call Chain: First Link Creation

```
fns.c:100   createlink()
do1.c:207     makehint(DOCUMENT, ATOM, LINKATOM, docisaptr, &hint)
do1.c:209     createorglingranf(taskptr, granf, &hint, linkisaptr)
granf2.c:111    createorglgr(...)
granf2.c:117      findisatoinsertgr(fullcrumptr, hintptr, isaptr)
granf2.c:130        → subtype == ATOM → findisatoinsertmolecule(...)
```

Same function, `atomtype = LINKATOM = 2`.

**Path A — fresh document (no content yet):**

- `upperbound = tumblerincrement(docisa, 2, LINKATOM+1=3)` → `docisa.0.3`
- `findpreviousisagr(docisa.0.3)` → finds `docisa` (only entry)
- `tumblerlength(docisa) == tumblerlength(lowerbound=docisa)` → TRUE → first branch:

```c
tumblerincrement (&lowerbound, 2, hintptr->atomtype, isaptr);  // LINKATOM=2 → docisa.0.2
tumblerincrement (isaptr, 1, 1, isaptr);                       // docisa.0.2.1
```
[`granf2.c:166-167`]

**Path B — content was inserted first:**

- `findpreviousisagr(docisa.0.3)` → finds text ISA at `docisa.0.1.N` (which sorts before `docisa.0.3`)
- `tumblerlength(docisa.0.1.N) ≠ tumblerlength(docisa)` → FALSE → LINKATOM branch:

```c
tumblerincrement (&hintptr->hintisa, 2, 2, isaptr);  // docisa.0.2
if (tumblercmp (&lowerbound, isaptr) == LESS)         // docisa.0.1.N < docisa.0.2 → TRUE
    tumblerincrement (isaptr, 1, 1, isaptr);          // docisa.0.2.1
```
[`granf2.c:171-173`]

Both paths yield the same result.

**Trace for `d = 1.1.0.1.0.1`** (mantissa index 5 is last nonzero):

| Step | Call | Result |
|------|------|--------|
| 1 | `tumblerincrement(docisa, 2, LINKATOM=2, isaptr)` | `mantissa[5+2] += 2` → `1.1.0.1.0.1.0.2` |
| 2 | `tumblerincrement(isaptr, 1, 1, isaptr)` | `mantissa[7+1] += 1` → `1.1.0.1.0.1.0.2.1` |

**First link ISA = `docisa.0.2.1` = `[d.0.2.1]`** [`granf2.c:166-167` or `granf2.c:173`].

---

## Empirical Confirmation from Golden Tests

`golden/links/create_link.json:63`:
```json
{ "op": "create_link", ..., "result": "1.1.0.1.0.1.0.2.1" }
```
Document = `1.1.0.1.0.1`, link ISA = `1.1.0.1.0.1.0.2.1` = docisa + `.0.2.1`. ✓

`golden/links/multiple_links_same_doc.json:34,40`:
```json
{ "op": "create_link", ..., "result": "1.1.0.1.0.1.0.2.1" }  // first link
{ "op": "create_link", ..., "result": "1.1.0.1.0.1.0.2.2" }  // second link
```
Each subsequent link increments the final digit: `.0.2.N`.

---

## Why the Fresh-Document Condition Always Holds

`findisatoinsertgr` [`granf2.c:135-141`] requires the document orgl to already exist in the granfilade before accepting an insert or link creation:

```c
if (hintptr->subtype == ATOM) {
    if (!isaexistsgr (fullcrumptr, &hintptr->hintisa)) {
        fprintf (stderr,"nothing at hintisa for atom\n");
        return (FALSE);
    }
    findisatoinsertmolecule (fullcrumptr, hintptr, isaptr);
```

`createorglingranf` (called by `docreatenewdocument` at `do1.c:240`) plants the orgl in the granfilade before any insert is possible. Therefore `findpreviousisagr(docisa.0.{2,3})` always finds at least `docisa`, making the tumbler-length comparison — and hence the address — deterministic.

---

## The `tumblerincrement` Mechanics

`tumble.c:599-623`:
```c
int tumblerincrement(tumbler *aptr, INT rightshift, INT bint, tumbler *cptr)
{
    ...
    for (idx = NPLACES; aptr->mantissa[--idx] == 0 && idx > 0;);
    // idx = index of last non-zero digit
    cptr->mantissa[idx + rightshift] += bint;
    tumblerjustify(cptr);
}
```

`rightshift=2` opens a gap of two zero slots after the document's last digit; `bint=TEXTATOM=1` or `bint=LINKATOM=2` fills the first of those slots. A second call with `rightshift=1, bint=1` appends the `.1` suffix. The two-step construction is:

```
docisa . 0 . ATOMTYPE . 1
         ↑             ↑
    rightshift=2   rightshift=1 from newly placed digit
```

This schema encodes the atom type directly into the ISA hierarchy. There is no way for these values to vary without changing `TEXTATOM` or `LINKATOM` in `xanadu.h:145-146`.

---

## Conclusion

The implementation **deterministically emits**:

- **First content ISA: `[d.0.1.1]`** — hardwired via `TEXTATOM=1` at `granf2.c:166`
- **First link ISA: `[d.0.2.1]`** — hardwired via `LINKATOM=2` at `granf2.c:166` (or `granf2.c:171`)

No global counter, no session state, no disk-ordering artifact can change these values. The `.0.1` and `.0.2` sub-namespaces are structurally encoded in the atom-type constants, and the trailing `.1` is the fixed initial index within each sub-namespace.
