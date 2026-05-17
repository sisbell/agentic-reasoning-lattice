## Question 3 [evidence]

> Does udanax-green have any code path that can deposit a link address at a strict prefix-extension of an existing link address (i.e., as a descendant rather than a sibling), or does the implementation uniformly enforce the sibling-frontier discipline across all link-store-extending operations?

## KB Synthesis

## Link Address Allocation: Sibling-Frontier vs. Descendant Discipline

The implementation uniformly enforces the sibling-frontier discipline. There is no code path that can deposit a link orgl address as a strict prefix-extension (descendant) of an existing link orgl address under normal operation.

### How Link Allocation Works

From [SS-ADDRESS-ALLOC] Finding 0065, MAKELINK allocates via `findisatoinsertmolecule` with two bounds:

- **Upper bound:** `docISA.2.3` — constrains the search to the document's link element subspace
- **First-link case:** when `lowerbound < docISA.2.2`, allocates at `docISA.2.2.1`
- **Subsequent case:** `tumblerincrement(&lowerbound, 0, 1, isaptr)` — increment at `rightshift=0`

The `rightshift=0` parameter is the key mechanism. From [SS-ADDRESS-ALLOC] Finding 0031, `tumblerincrement(t, 0, 1)` adds 1 at the last significant digit of `t`. If the highest existing link is `docA.2.2.N`, the result is `docA.2.2.(N+1)` — a sibling, never a descendant.

### Concrete Address Sequence

From [SS-ADDRESS-SPACE] Finding 0065:
```
Document A = 1.1.0.1.0.1
First link:   1.1.0.1.0.1.0.2.1   (first-link case: allocate at docISA.2.2.1)
Second link:  1.1.0.1.0.1.0.2.2   (increment: docISA.2.2.1 + 1 = docISA.2.2.2)
Third link:   1.1.0.1.0.1.0.2.3
```

To deposit `1.1.0.1.0.1.0.2.1.1` (a descendant of the first link) would require `findpreviousisagr` to return `1.1.0.1.0.1.0.2.1.something` — an address deeper than the normal allocation depth — which cannot arise through any normal FEBE operation.

### Structural Asymmetry vs. Non-Molecule Allocation

There is a notable architectural asymmetry. The non-molecule allocator (`findisatoinsertnonmolecule`), used for document and version addresses, includes an **explicit truncation step** before incrementing, enforcing depth by construction [SS-ADDRESS-ALLOC] Finding 0021:

> "Otherwise, truncate the found item and increment to produce the next sibling."

The molecule allocator (`findisatoinsertmolecule`) used for link orgls has **no such truncation**. It relies on the invariant that all prior link addresses in the search range are already at the expected depth. This is maintained in practice because all link-creating paths use the same allocator with the same bounds, producing a closed monotonic sequence at a fixed depth. But it is a weaker structural guarantee — it is an invariant sustained by operational discipline rather than by the allocator's own mechanics.

### What Would Be Required for a Descendant

A descendant link address (e.g., `docISA.2.2.1.1`) could only arise if:
1. `findpreviousisagr` returned `docISA.2.2.1.something` within the search bounds, AND
2. The subsequent increment produced `docISA.2.2.1.something+1`

The access-controlled FEBE interface provides no operation that writes into the granfilade at an arbitrary address. All content paths go through `doinsert`/`docopy` (text, element field 3) or `docreatelink` (link orgls, element field 2), both of which use the same allocation mechanism. There is no back-door write path that could seed a spurious deep address.

### Conclusion

The sibling-frontier discipline is uniformly enforced across all link-store-extending operations. The `rightshift=0` increment in `findisatoinsertmolecule` is the mechanical guarantee: it always produces the next integer at the current depth, never a descendant [SS-ADDRESS-ALLOC] [SS-LINK-HOME-DOCUMENT] [SS-ADDRESS-SPACE]. The absence of explicit truncation in the molecule allocator is an architectural asymmetry relative to non-molecule allocation, but it does not create a violation path under the FEBE access model.

---

## Code Exploration

I now have all the source I need. Let me trace the complete analysis with exact line citations.

---

## Analysis: Link Address Descendant Placement in udanax-green

### Key Constants (`xanadu.h:140-146`)

```c
#define TEXTATOM  1
#define LINKATOM  2
#define DOCUMENT  3
#define ATOM      4
```

---

### Entry Points for Link Creation

Two link-creating entry points both converge on the same allocation path:

**`domakelink` (do1.c:169)** and **`docreatelink` (do1.c:195)** both call:

```c
createorglingranf(taskptr, granf, &hint, linkisaptr)    // do1.c:182,209
```

where `hint = makehint(DOCUMENT, ATOM, LINKATOM, docisaptr, &hint)` [do1.c:180,207].

**`createorglingranf` (granf1.c:50)** delegates directly to **`createorglgr` (granf2.c:111)**, which calls:

```c
findisatoinsertgr((typecuc*)fullcrumptr, hintptr, isaptr)    // granf2.c:117
```

**`findisatoinsertgr` (granf2.c:130)**:
```c
if (hintptr->subtype == ATOM) {
    if (!isaexistsgr(fullcrumptr, &hintptr->hintisa)) return FALSE;
    findisatoinsertmolecule(fullcrumptr, hintptr, isaptr);  // granf2.c:142
}
```

This is the sole allocation path for all link ISAs.

---

### The Allocation Function: `findisatoinsertmolecule` (granf2.c:158–181)

```c
static int findisatoinsertmolecule(typecuc *fullcrumptr, typehint *hintptr, typeisa *isaptr)
{
  typeisa upperbound, lowerbound;

    tumblerincrement(&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound);  // line 162
    clear(&lowerbound, sizeof(lowerbound));
    findpreviousisagr((typecorecrum*)fullcrumptr, &upperbound, &lowerbound);      // line 164
    if (tumblerlength(&hintptr->hintisa) == tumblerlength(&lowerbound)) {         // line 165
        tumblerincrement(&lowerbound, 2, hintptr->atomtype, isaptr);              // line 166
        tumblerincrement(isaptr, 1, 1, isaptr);                                   // line 167
    } else if (hintptr->atomtype == TEXTATOM) {
        tumblerincrement(&lowerbound, 0, 1, isaptr);                              // line 169
    } else if (hintptr->atomtype == LINKATOM) {
        tumblerincrement(&hintptr->hintisa, 2, 2, isaptr);                        // line 171
        if (tumblercmp(&lowerbound, isaptr) == LESS)
            tumblerincrement(isaptr, 1, 1, isaptr);                               // line 173
        else
            tumblerincrement(&lowerbound, 0, 1, isaptr);                          // line 175
    }
}
```

There are three allocation branches. Understanding each requires knowing `tumblerincrement`'s semantics.

---

### Tumbler Arithmetic (`tumble.c:599–622`)

```c
int tumblerincrement(tumbler *aptr, INT rightshift, INT bint, tumbler *cptr)
{
    if (iszerotumbler(aptr)) {
        cptr->exp = -rightshift;
        cptr->mantissa[0] = bint;      // produces a fresh 1-component tumbler
        return(0);
    }
    for (idx = NPLACES; aptr->mantissa[--idx] == 0 && idx > 0;);
    // idx = index of last non-zero mantissa position
    cptr->mantissa[idx + rightshift] += bint;  // line 621
    tumblerjustify(cptr);
}
```

`rightshift=0` modifies the last non-zero position (same depth — a sibling).  
`rightshift>0` places a new value beyond the last non-zero, creating a deeper address (potential descendant).

---

### Concrete Trace for a Typical Document

For a document ISA `D` with `nstories(D)=3` (e.g., mantissa `[1,0,1,0,...]`, length=3):

**First link (BRANCH 1, line 165–167):**  
`findpreviousisagr` returns `lowerbound = D` (the document itself, length=3).  
`tumblerlength(hintisa=D) == tumblerlength(lowerbound=D)` → **true**.

```
isaptr = tumblerincrement(D, 2, LINKATOM=2)  →  mantissa[idx_D+2] = 2  (depth 5)
isaptr = tumblerincrement(isaptr, 1, 1)       →  mantissa[idx_D+3] = 1  (depth 6)
```

Result: `D.0.0.2.1` in positional notation — a **child of D**, not of any link.

**Second link (BRANCH 3, line 170–175):**  
`lowerbound` = first link ISA (depth 6). `tumblerlength(D=3) ≠ tumblerlength(first_link=6)` → BRANCH 1 skipped.

```c
tumblerincrement(&hintptr->hintisa, 2, 2, &isaptr);  // base = D.0.0.2 (depth 5)
```

Comparison: `first_link > base` (first_link has mantissa[idx_D+3]=1, base has 0 there) → NOT LESS.

```c
tumblerincrement(&lowerbound, 0, 1, isaptr);  // line 175: increment LAST position of first_link
```

`rightshift=0` increments mantissa[idx_first_link+0], producing a tumbler at the **same depth as first_link** — a sibling.  
Third, fourth… links all proceed through line 175 in the same way.

---

### The Critical Guard That's Missing

`findisatoinsertnonmolecule` (granf2.c:203) received a bug fix [granf2.c:219–232] that guards against a lowerbound from the wrong parent context:

```c
/* BUG FIX #2: Also check if lowerbound is actually under hintisa... */
tumblertruncate(&lowerbound, hintlength, &truncated);               // line 231
lowerbound_under_hint = tumblereq(&truncated, &hintptr->hintisa);   // line 232

if (iszerotumbler(&lowerbound) || !lowerbound_under_hint) {
    tumblerincrement(&hintptr->hintisa, depth, 1, isaptr);
}
```

**`findisatoinsertmolecule` has no equivalent guard.** [granf2.c:158–181]

---

### The One Theoretical Descendant Path

BRANCH 1 at line 165 fires on `tumblerlength(hintisa) == tumblerlength(lowerbound)`. In normal single-account operation, `lowerbound` at this moment is the document ISA itself, and all subsequent calls hit BRANCH 3 (sibling discipline). However:

Consider a multi-account system where an account at ISA depth 4 exists. Its documents are allocated at depth 6 (since `depth=2`, `tumblerincrement(acct, 2, 1)` adds 2 positions beyond acct's last nonzero at index 3 → mantissa[5]=1 → depth 6). Link atoms from a **different** document at ISA depth 3 are also at depth 6. If such a foreign link ISA numerically falls within the range `[0, upperbound)` searched by `findpreviousisagr` when allocating atoms under a depth-6 document — and is the **greatest** entry below `upperbound` — then:

- `tumblerlength(hintisa=depth6_doc) == tumblerlength(lowerbound=foreign_link)` → **true**
- BRANCH 1 fires: `tumblerincrement(foreign_link, 2, LINKATOM=2)` then `tumblerincrement(result, 1, 1)`
- Result = `foreign_link.mantissa` with positions `idx+2=2` and `idx+3=1` appended
- `tumblertruncate(result, tumblerlength(foreign_link)) == foreign_link` → result **is a descendant** of `foreign_link`

This is the sole code path that can deposit a link address at a strict prefix-extension of an existing link address. It requires the missing guard (analogous to the BUG FIX #2 applied only to `findisatoinsertnonmolecule`) in `findisatoinsertmolecule`.

---

### V-Space Address (`findnextlinkvsa`, do2.c:151–167)

```c
tumblerclear(&firstlink);
tumblerincrement(&firstlink, 0, 2, &firstlink);    // firstlink = 2
tumblerincrement(&firstlink, 1, 1, &firstlink);    // firstlink = 2.0.1

doretrievedocvspan(taskptr, docisaptr, &vspan);
tumbleradd(&vspan.stream, &vspan.width, &vspanreach);
if (tumblercmp(&vspanreach, &firstlink) == LESS)
    movetumbler(&firstlink, vsaptr);   // minimum 2.0.1
else
    movetumbler(&vspanreach, vsaptr);  // end of document content
```

New link VSAs are placed at the end of the current document extent — monotonically increasing, never a descendant of a prior address. No descendant placement is possible through this path.

Also note: **`acceptablevsa` (do2.c:110–113) is a stub that always returns `TRUE`**, performing no validation:

```c
bool acceptablevsa(tumbler *vsaptr, typeorgl orglptr)
{
    return (TRUE);
}
```

There is no VSA-level guard against prefix-extension placement.

---

### Summary

| Scenario | Branch | Code Path | Result |
|----------|--------|-----------|--------|
| First link in a document | BRANCH 1 (granf2.c:166–167) | `tumblerincrement(doc, 2, 2)` + `tumblerincrement(result, 1, 1)` | Child of document, not of any link — **sibling discipline holds** |
| Subsequent links in same document | BRANCH 3 (granf2.c:175) | `tumblerincrement(prev_link, 0, 1)` | Sibling — **sibling discipline holds** |
| Cross-depth contamination (missing guard) | BRANCH 1 (granf2.c:166–167) with foreign-link lowerbound | Same math as above, applied to a link ISA | **Descendant of that foreign link** — sibling discipline violated |
| V-space link addresses | `findnextlinkvsa` (do2.c:151–167) | `tumbleradd(vspan.stream, vspan.width)` | Monotone frontier — **sibling discipline holds** |

**The implementation uniformly enforces sibling-frontier discipline under normal single-account operation.** In that regime, no code path can deposit a link address at a strict prefix-extension of an existing link address: first-link ISAs are always children of their owning document, and all subsequent ISAs are siblings of the previous link.

**The one theoretical exception** lies in BRANCH 1 of `findisatoinsertmolecule` (granf2.c:165–167). Because this function, unlike `findisatoinsertnonmolecule`, lacks a guard checking that `lowerbound` is actually under `hintisa`, a foreign link ISA from a numerically interleaved address space could appear as `lowerbound` at matching depth. In that case, the `tumblerincrement(lowerbound, 2, …)` at line 166 — using `rightshift=2` — extends beyond `lowerbound`'s last non-zero position, producing an address for which `tumblertruncate(result, tumblerlength(lowerbound)) == lowerbound`: a strict prefix-extension. This path requires multi-account ISA interleaving (accounts of ISA depth 4, whose depth-6 documents share an address-space depth with link atoms from depth-3 documents) and is an incidental consequence of the same cross-context contamination bug that BUG FIX #2 corrected in `findisatoinsertnonmolecule` but left unaddressed in `findisatoinsertmolecule`.
