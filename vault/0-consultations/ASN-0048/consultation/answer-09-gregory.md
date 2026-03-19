## Question 9 [gregory]

> When `findisatoinsertmolecule` allocates I-addresses for new text, does it scan the entire granfilade subtree under the document's I-address range, or does it use a cached high-water mark — and if it scans, what happens if a CREATELINK has advanced the allocation past the text subrange?

## KB Synthesis

## `findisatoinsertmolecule`: Scan, Not Cache — and CREATELINK Disrupts It

### It scans the tree on every call

`findisatoinsertmolecule` has no session-local high-water mark. Each INSERT performs a live tree traversal of the granfilade via `findpreviousisagr`, which walks the B-tree to find the highest existing I-address below a document-scoped upper bound, then increments by 1 [SS-ADDRESS-SPACE Finding 0061]:

> *"The allocation is purely derived from current tree state — there is no cached 'next available' pointer. This means allocation is stateless with respect to the session: any session querying the same granfilade tree will allocate identically."*

The upper bound is computed per call from the document ISA hint, scoping the search to the document's allocation subspace [SS-ADDRESS-ALLOC Finding 0065, Finding 0021]. The algorithm: scan down to the bound, take the max, increment by 1. Same pattern for every INSERT, every time.

### CREATELINK advances the text allocation past the text subrange

Link orgls and text characters **share the same monotonic I-address sequence** within a document's allocation space [INT-LINK-INSERT Finding 0063]:

> *"CREATELINK allocates an orgl in the granfilade via `createorglingranf`... This allocation advances the granfilade's maximum I-address. When the next INSERT calls `findpreviousisagr`, it finds the link orgl's I-address as the highest and allocates above it — creating a gap in the text I-address sequence."*

The interaction predicate the KB formalizes: `post(create_link) ⟹ next_text_iaddr > pre(create_link).next_text_iaddr + link_width`.

**Observable consequence**: INSERT "ABC" → CREATELINK → INSERT "DEF" yields **2 shared span pairs** from `compare_versions`, because the I-addresses for "ABC" and "DEF" are non-contiguous — the link orgl occupies the gap between them. Compare with INSERT "ABC" → INSERT "DEF" (no CREATELINK): **1 shared span pair**, contiguous I-addresses.

### VERSION does not disrupt

This is the explicit contrast in [INV-MONOTONIC Finding 0077]:

> *"`CREATENEWVERSION` does NOT break I-address contiguity for subsequent text INSERTs. Unlike CREATELINK, which allocates a link orgl in the content region of the granfilade, VERSION allocates only a document address in a separate tumbler range. The content allocation counter is unaffected."*

Test evidence: INSERT "ABC" → VERSION → INSERT "XYZ" → `compare_versions` returns **1 shared span pair** (contiguous), confirming VERSION doesn't touch `findisatoinsertmolecule`'s allocation space.

### Summary

| Property | Answer |
|----------|--------|
| Cache vs scan | Scan — `findpreviousisagr` on every INSERT |
| CREATELINK effect on text allocation | Disrupts — link orgl advances the granfilade max, gap created |
| VERSION effect on text allocation | None — allocates in a separate document-address range |
| Why | Text and link orgls compete for the same monotonic I-address sequence in the document's granfilade subtree |

Relevant entries: [SS-ADDRESS-SPACE Finding 0061], [SS-ADDRESS-ALLOC Finding 0065], [INT-LINK-INSERT Finding 0063], [INV-MONOTONIC Finding 0077], [ST-INSERT Finding 0033].

---

## Code Exploration

I have everything I need. Here is the full answer:

---

## How `findisatoinsertmolecule` Allocates I-Addresses

### Short answer

**It scans — not with a cached high-water mark.** Every call does a live traversal of the granfilade tree via `findpreviousisagr`. But it is *not* a full subtree scan: it descends a single root-to-leaf path in O(tree-height) time. And CREATELINK cannot contaminate text allocation because the two subranges are bounded by non-overlapping `upperbound` values computed at call time.

---

### 1. The allocation path: always a live scan

`findisatoinsertgr` [granf2.c:130] calls `findisatoinsertmolecule` for all `ATOM`-subtype hints:

```c
// granf2.c:142
findisatoinsertmolecule (fullcrumptr, hintptr, isaptr);
```

Inside `findisatoinsertmolecule` [granf2.c:158-181]:

```c
static int findisatoinsertmolecule(typecuc *fullcrumptr, typehint *hintptr, typeisa *isaptr)
{
  typeisa upperbound, lowerbound;

    tumblerincrement (&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound);  // line 162
    clear (&lowerbound, sizeof(lowerbound));                                       // line 163
    findpreviousisagr ((typecorecrum*)fullcrumptr, &upperbound, &lowerbound);      // line 164
    ...
```

`lowerbound` is zeroed fresh every call [granf2.c:163]. There is no field read from a cache or from the crum/node structure. The result comes entirely from `findpreviousisagr`.

---

### 2. What `findpreviousisagr` actually does (single path, not full subtree)

`findpreviousisagr` [granf2.c:255-278]:

```c
int findpreviousisagr(typecorecrum *crumptr, typeisa *upperbound, typeisa *offset)
{ RECURSIVE
  INT tmp;
  typecorecrum *ptr, *findleftson();

    if (crumptr->height == 0) {
        findlastisaincbcgr ((typecbc*)crumptr, offset);   // line 264 — leaf: finalize
        return(0);
    }
    for (ptr = findleftson((typecuc*)crumptr); ptr; ptr = findrightbro(ptr)) {
        if (
         (tmp= whereoncrum (ptr, (typewid*)offset, upperbound, WIDTH)) == THRUME
        || tmp == ONMYRIGHTBORDER
        || !ptr->rightbro) {
            findpreviousisagr (ptr, upperbound, offset);   // line 272 — descend and return
            return(0);
        } else {
            tumbleradd(offset, &ptr->cwid.dsas[WIDTH], offset);  // line 275 — accumulate
        }
    }
}
```

The loop at each internal node walks children left to right:
- If a child's span is entirely to the **left** of `upperbound` (below it), its width is added to `offset` [line 275] and we advance to the next sibling.
- As soon as a child's span **straddles** `upperbound` (`THRUME`) or **borders** it (`ONMYRIGHTBORDER`), or there is no right sibling (`!ptr->rightbro`), we recurse into that child [line 272] and immediately return.

At the leaf, `findlastisaincbcgr` [granf2.c:280-284] adds `textlength - 1` to `offset` if the crum is a `GRANTEXT` node, so `offset` ends up pointing at the last character of the last text run straddling `upperbound`.

This is a **single root-to-leaf descent** — O(tree height) — not a full subtree scan. All siblings to the right of the descent path are skipped; only siblings to the left are accumulated into `offset`.

---

### 3. How the `upperbound` is computed — and why subranges don't cross

The constants [xanadu.h:145-146]:
```c
#define TEXTATOM  1
#define LINKATOM  2
```

`tumblerincrement(&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound)` [granf2.c:162] places `atomtype + 1` two levels below `hintisa` in the tumbler hierarchy (rightshift=2 means appending two more sub-levels):

| Call context | atomtype | `upperbound` |
|---|---|---|
| Text insert (`doinsert`, `do1.c:117`) | TEXTATOM = 1 | `docisa.0.2` |
| Link create (`docreatelink`, `do1.c:207`) | LINKATOM = 2 | `docisa.0.3` |

Actual allocated addresses:
- First text atom: `docisa.0.1.1` (TEXTATOM=1 at depth+2, then +1 at depth+3)
- Subsequent text: `docisa.0.1.2`, `docisa.0.1.3`, …
- First link: `docisa.0.2.1` (LINKATOM=2 at depth+2, then +1 at depth+3)
- Subsequent links: `docisa.0.2.2`, `docisa.0.2.3`, …

In tumbler ordering, with `docisa` ending at mantissa position `L`:
- Text items have mantissa[L+1]=1, mantissa[L+2]=N → all less than `docisa.0.2` (which has mantissa[L+1]=2, mantissa[L+2]=0)
- Link items have mantissa[L+1]=2, mantissa[L+2]=M → all greater than `docisa.0.2`

Therefore the text `upperbound` (`docisa.0.2`) sits exactly at the **seam** between the two subranges: every text address is below it, every link address is above it.

---

### 4. What happens if CREATELINK has advanced allocation past the text subrange

**Nothing.** The text `upperbound` is not derived from any state — it is always `hintisa.0.2`, computed fresh from the document's own I-address. Link addresses at `docisa.0.2.M` are all strictly greater than `docisa.0.2`. When `findpreviousisagr` runs for a text insert with `upperbound = docisa.0.2`, it will never descend into or accumulate past any node whose span lies in `docisa.0.2.*`, because `whereoncrum` will return `TOMYRIGHT` for those nodes (they start after `upperbound`).

The text allocator is structurally blind to the link subrange.

---

### 5. The LINKATOM branch handles the cross-range `lowerbound` explicitly

Because the link `upperbound` is `docisa.0.3` (above both subranges), `findpreviousisagr` for a link allocation *can* return a text address as `lowerbound` if no links exist yet. The LINKATOM branch in `findisatoinsertmolecule` [granf2.c:170-175] accounts for this:

```c
} else if (hintptr->atomtype == LINKATOM) {
    tumblerincrement (&hintptr->hintisa, 2, 2, isaptr);    // tentative = docisa.0.2
    if (tumblercmp (&lowerbound, isaptr) == LESS)
        tumblerincrement (isaptr, 1, 1, isaptr);            // first link → docisa.0.2.1
    else
        tumblerincrement (&lowerbound , 0, 1, isaptr);      // next link → lowerbound+1
}
```

- `tentative = docisa.0.2` — the start of the LINKATOM subrange [granf2.c:171]
- If `lowerbound < tentative` (e.g., `lowerbound` is a text address), it means no links exist yet → first link gets `docisa.0.2.1` [granf2.c:172-173]
- If `lowerbound >= tentative` (it's already a link address), next link gets `lowerbound + 1` [granf2.c:175]

So even though LINKATOM's `upperbound` encompasses the text subrange, the allocation logic re-anchors to `docisa.0.2` as the base of the link subrange, correctly ignoring any text addresses returned by the scan.

---

### Summary

| Question | Answer | Evidence |
|---|---|---|
| Cached high-water mark? | No. `lowerbound` is zeroed on every call. | `granf2.c:163` |
| Full subtree scan? | No. Single O(height) root-to-leaf descent. | `granf2.c:267-277` |
| What does the scan traverse? | The rightmost path straddling `upperbound`; left siblings are accumulated, right siblings skipped. | `granf2.c:275` vs `granf2.c:272` |
| Can CREATELINK advance text allocation? | No. Text `upperbound = docisa.0.2`; link addresses are all > `docisa.0.2`. | `granf2.c:162`, `xanadu.h:145-146` |
| Does LINKATOM search see text addresses? | Yes (its `upperbound = docisa.0.3`), but the branch logic discards them by re-anchoring to `docisa.0.2`. | `granf2.c:171-175` |
