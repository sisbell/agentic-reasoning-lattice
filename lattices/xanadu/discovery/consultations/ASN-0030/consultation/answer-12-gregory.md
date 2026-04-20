## Question 12 [gregory]

> When `findisatoinsertmolecule` allocates a fresh I-address by querying the granfilade for `max + 1`, can a DELETE that removed content from a POOM ever cause that max to decrease, leading to I-address reuse in a subsequent INSERT?

## KB Synthesis

No. DELETE cannot cause I-address reuse.

The allocation mechanism in `findisatoinsertmolecule` queries the **granfilade** for the current maximum I-address via `findpreviousisagr`, then increments by 1 [SS-ADDRESS-SPACE, Finding 0061]. The critical property is that DELETE never touches the granfilade.

[FC-GRANF-ON-DELETE] establishes this explicitly: DELETE modifies only the POOM (the document's V-to-I mapping via `deletevspanpm` → `deletend`). No delete path calls any granfilade insertion or deletion function. The granfilade is append-only — its entries are permanent.

Because the deleted I-addresses remain in the granfilade tree, `findpreviousisagr` will still find them as the maximum when the next INSERT runs. The max never decreases. [INV-MONOTONIC] (Finding 0061) states this directly: "deleted content's I-addresses remain in the granfilade tree and continue to influence allocation. Interleaved INSERT-DELETE-INSERT sequences produce contiguous, gap-free I-address sequences: INSERT 'AAA' allocates I.1–I.3, DELETE removes a character (V-space only), INSERT 'BBB' allocates I.4–I.6 (not reusing I.2)."

[INV-NO-IADDR-REUSE] summarizes the invariant: "Deleted I-addresses are never reused. Since the granfilade is never modified by DELETE, and allocation always queries the granfilade for the current maximum, 'gaps' in V-space created by DELETE do not create 'gaps' in I-space. The I-address space grows strictly monotonically and permanently."

So: the POOM may have gaps (V-positions removed), but the granfilade max is monotonically non-decreasing, and no subsequent INSERT can obtain an I-address that was previously allocated.

---

## Code Exploration

Now I have everything I need. Here is the definitive answer:

---

## I-Address Reuse via `findisatoinsertmolecule` — Definitive Analysis

### Short answer

**No.** A DELETE cannot cause the granfilade max to decrease, and therefore cannot cause I-address reuse via `findisatoinsertmolecule`. The granfilade is structurally append-only: no FEBE operation in the codebase ever calls `deleteseq` on the granfilade. The DELETE path operates exclusively on the POOM (V-space), never on the granfilade (I-space).

---

### 1. How `findisatoinsertmolecule` computes the new I-address

`granf2.c:158-181`:

```c
static int findisatoinsertmolecule(typecuc *fullcrumptr, typehint *hintptr, typeisa *isaptr)
{
  typeisa upperbound, lowerbound;

    tumblerincrement (&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound);
    clear (&lowerbound, sizeof(lowerbound));
    findpreviousisagr ((typecorecrum*)fullcrumptr, &upperbound, &lowerbound);  // line 164
    if (tumblerlength (&hintptr->hintisa) == tumblerlength (&lowerbound)) {
        tumblerincrement (&lowerbound, 2, hintptr->atomtype, isaptr);
        tumblerincrement (isaptr, 1, 1, isaptr);  // "max + 1"
    } ...
```

`findpreviousisagr` (`granf2.c:255-278`) walks the granfilade tree, accumulating each node's `cwid.dsas[WIDTH]` (`granf2.c:275`) until it finds the rightmost leaf. At height 0 it calls `findlastisaincbcgr` (`granf2.c:264`) which adjusts for text atom length. The resulting `lowerbound` is the highest existing I-address; the new allocation is `lowerbound + 1`.

The "max" lives in the granfilade's node widths (`cwid.dsas[WIDTH]`), which are computed cumulatively up the tree by `setwidseq`.

---

### 2. The only function that can reduce a granfilade node's `cwid`

`edit.c:16-28` — comment says "use with GRAN":

```c
/* use with GRAN */
int deleteseq(typecuc *fullcrumptr, tumbler *address, INT index)
{
    context = retrievecrums (fullcrumptr, address, index);
    ptr = (typecbc *) context->corecrum;
    freecrum ((typecorecrum*)&context->corecrum);   // removes leaf from tree
    crumcontextfree(context);
    setwispupwards(findfather((typecorecrum*)ptr), 1);  // line 26 — recomputes cwid upward
    recombine(findfather((typecorecrum*)ptr));
}
```

`setwispupwards` (`wisp.c:83-111`) calls `setwisp` repeatedly. For GRAN nodes, `setwisp` dispatches to `setwidseq` (`wisp.c:127-128`):

```c
case GRAN:
    return (setwidseq ((typecuc*)ptr));
```

`setwidseq` (`wisp.c:150-168`) recomputes `cwid` as the **sum of living children** only:

```c
clear (&sum, sizeof (sum));
for (ptr = findleftson (father); ptr; ptr = getrightbro (ptr)){
    widopseq (&sum, &ptr->cwid, &sum);   // line 161 — sum only present children
}
...
movewisp (&sum, &father->cwid);          // line 165 — overwrites parent cwid
```

If a leaf had been freed, it is no longer in the child list, so its span is excluded from the sum — the parent's `cwid.dsas[WIDTH]` **would decrease**.

**But `deleteseq` is dead code.** A grep for `deleteseq` across the entire `backend/` directory returns exactly one hit: its own definition in `edit.c`. It is never called.

---

### 3. What DELETE actually does — the POOM path only

`do1.c:158-167`:

```c
bool dodeletevspan(typetask *taskptr, typeisa *docisaptr, typevspan *vspanptr)
{
    return (
       findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
    && deletevspanpm (taskptr, docisaptr, docorgl, vspanptr)
    );
}
```

`orglinks.c:145-152`:

```c
bool deletevspanpm(typetask *taskptr, tumbler *docisaptr, typeorgl docorgl, typevspan *vspanptr)
{
    if (iszerotumbler(&vspanptr->width))
        return (FALSE);
    deletend((typecuc*)docorgl, &vspanptr->stream, &vspanptr->width, V);  // line 149
    logbertmodified(docisaptr, user);
    return (TRUE);
}
```

`deletend` (`edit.c:31`) is labeled "use with SPAN and POOM". It operates on `docorgl` (a POOM enfilade, looked up from the granfilade at `findorgl`) in the **`V` dimension** (virtual address space). It calls `setwispupwards` (`edit.c:74`) and `recombine` (`edit.c:75`) on the POOM father — not on any granfilade node.

For POOM nodes, `setwisp` dispatches to `setwispnd` (`wisp.c:131`), not `setwidseq`. `setwispnd` (`wisp.c:171-228`) computes a bounding box over V-space children — it has nothing to do with the granfilade's I-space widths.

---

### 4. Structural separation: granfilade vs. POOM

The granfilade (`granf`, type `GRAN`) and the POOM (type `POOM`) are separate enfilade trees:

- The **granfilade** maps I-addresses → content atoms (text, orgls). Its `cwid.dsas[WIDTH]` encodes the cumulative I-address span. Only `inserttextgr` (`granf2.c:83`) and `createorglgr` (`granf2.c:111`) write to it — both via `insertseq` (`granf2.c:99`, `125`), which adds new leaves and calls `setwispupwards` upward, causing the `cwid` sum to **increase only**.
- The **POOM** maps V-addresses → I-spans (version content). `deletend` operates here with `V` dimension, reshaping V-space. The granfilade is read-only from DELETE's perspective — it is consulted only via `findorgl` to locate the POOM.

No FEBE operation ever calls `deleteseq` on the granfilade. No `freecrum` is ever called on a granfilade leaf in any delete path.

---

### 5. Conclusion

The granfilade's node widths (`cwid.dsas[WIDTH]`) are a running sum of allocated I-address spans and are **strictly non-decreasing**. The DELETE path (`dodeletevspan` → `deletevspanpm` → `deletend`) operates solely on the POOM in V-space and never touches the granfilade. `deleteseq`, the only function that could reduce a granfilade node's `cwid`, is dead code — it appears in `edit.c` but is never called from anywhere in the backend.

Therefore: `findisatoinsertmolecule` always finds a max that is at least as large as any previously allocated I-address. **I-address reuse via granfilade max decrease is not possible.**
