## Question 10 [gregory]

> Does the `.0.` digit separator play a structural role in baptism (e.g., marking a level boundary that baptism must respect), or is it purely a conventional interpretation of an unconstrained digit sequence?

## KB Synthesis

The `.0.` separator is **not a first-class structural token** in the tumbler representation — it is an artifact of the allocation arithmetic at a specific depth. But it does play a real structural role in baptism, through the `depth` parameter in `makehint`.

## What the representation layer knows about zeros

From [SS-TUMBLER] Findings 0001 and 0031: tumblers are unconstrained digit sequences. Zero is just digit value 0. The "zero-separator convention is semantic, not structural — the data type itself does not enforce hierarchy boundaries." No runtime code checks for `.0.` as a boundary marker during insertion, containment, or retrieval.

## How `.0.` enters baptism

The allocation mechanism in `findisatoinsertnonmolecule` ([SS-ADDRESS-ALLOC] Finding 0021) computes the upper bound as:

```
upperbound = tumblerincrement(hintisa, depth-1, 1)
```

The `depth-1` parameter is the rightshift — it controls *where* in the mantissa the increment lands.

- `depth=2` (ACCOUNT→DOCUMENT): `tumblerincrement(hintisa, 1, 1)` increments at the second-to-last position. For a parent like `1.1.0.2`, this produces `1.1.0.3` as the upper bound, and the first child is allocated at `1.1.0.2.0.1` — the `.0.` appears because the search finds nothing under the parent and falls back to constructing `parent.0.1`.
- `depth=1` (DOCUMENT→DOCUMENT, versions): `tumblerincrement(hintisa, 0, 1)` increments the last position. First child is `parent.1` — no `.0.` boundary crossed.

The `.0.` in `parent.0.1` is therefore produced by the first-child fallback path in `findisatoinsertnonmolecule`, not by any zero-recognition logic.

## Containment check uses prefix matching, not zero detection

[SS-TUMBLER-CONTAINMENT] confirms: the containment predicate is pure length-and-equality — truncate A to the length of B, compare. The code does not scan for `.0.` boundaries; it only cares about digit-sequence prefix. The hierarchy structure implied by `.0.` fields is real, but it is maintained by the *allocation invariant* (depth controls how deep a new address sits), not by any special handling of the zero digit itself.

## Summary

The `.0.` separator plays a structural role in baptism **indirectly**: `makehint` encodes the hierarchy level as a depth integer, and the allocation arithmetic at depth=2 produces addresses with `.0.` boundaries as a consequence. But the tumbler type is agnostic to zero — nothing in the allocation, containment, or storage code treats 0 as a level-boundary sentinel. The structural meaning lives in the depth parameter and the address-allocation convention, not in the digit value 0 itself.

---

## Code Exploration

Now I have enough to answer the question with full citations. Here is the complete analysis:

---

## Does `.0.` Play a Structural Role in Baptism?

**Short answer: Yes, it is structural — mechanically enforced by the type hierarchy, semantically interpreted by account containment, and load-bearing in the address allocation algorithm. It is not a free convention.**

---

### 1. What a Tumbler Actually Is

A tumbler is a flat array of 16 unsigned integers (`tdigit`) stored in `mantissa[NPLACES]` [`common.h:53–65`]:

```c
#define NPLACES 16
typedef struct structtumbler {
    humber xvartumbler;
    char varandnotfixed;
    char sign  BIT ;
    short exp;
    tdigit mantissa[NPLACES];
} tumbler;
```

There is no explicit separator token. A zero value at position `k` *is* the `.0.` — it's just `mantissa[k] == 0`. The human notation `1.1.0.1.0.1` maps directly to `mantissa = [1, 1, 0, 1, 0, 1, 0, ...]`.

---

### 2. Baptism: `findisatoinsertnonmolecule`

Baptism — assigning a permanent address to a new document, node, or account — happens in `findisatoinsertnonmolecule` [`granf2.c:203–242`]:

```c
static int findisatoinsertnonmolecule(typecuc *fullcrumptr, typehint *hintptr, typeisa *isaptr)
{
  typeisa upperbound, lowerbound, truncated;
  INT depth, hintlength;
  bool lowerbound_under_hint;

    depth = hintptr->supertype == hintptr->subtype ? 1 : 2;      // [granf2.c:209]

    hintlength = tumblerlength (&hintptr->hintisa);               // [granf2.c:211]

    tumblerincrement (&hintptr->hintisa, depth - 1, 1, &upperbound); // [granf2.c:213]
    ...
    if (iszerotumbler(&lowerbound) || !lowerbound_under_hint) {
        /* Nothing under this hint - create first child as hintisa.0.1 */
        tumblerincrement(&hintptr->hintisa, depth, 1, isaptr);    // [granf2.c:237]
    } else {
        tumblertruncate (&lowerbound, hintlength + depth, isaptr);
        tumblerincrement(isaptr,tumblerlength(isaptr)==hintlength?depth:0,1,isaptr); // [granf2.c:240]
    }
}
```

The `depth` variable is computed directly from the **type hierarchy**, not from parsing any separator:

| Call site | supertype | subtype | depth | separator? |
|---|---|---|---|---|
| `ACCOUNT → DOCUMENT` (`do1.c:239`) | 2 | 3 | **2** | **yes — `.0.`** |
| `ACCOUNT → DOCUMENT` (version, `do1.c:275`) | 2 | 3 | **2** | **yes — `.0.`** |
| `DOCUMENT → DOCUMENT` (new version, `do1.c:271`) | 3 | 3 | **1** | no |
| `NODE → NODE` (`do1.c:251`) | 1 | 1 | **1** | no |

When `depth = 2`, the call `tumblerincrement(&hintptr->hintisa, 2, 1, isaptr)` [`granf2.c:237`] produces the first child address by placing a `1` two positions to the right of the parent's last nonzero digit — leaving one slot zero. That is the `.0.`.

---

### 3. How `tumblerincrement` Mechanically Inserts the Zero

`tumblerincrement(aptr, rightshift, bint, cptr)` [`tumble.c:599–623`]:

```c
int tumblerincrement(tumbler *aptr, INT rightshift, INT bint, tumbler *cptr)
{
    register INT idx;
    ...
    for (idx = NPLACES ; aptr->mantissa[--idx] == 0 && idx > 0;);
    // idx is now the position of the LAST non-zero digit

    cptr->mantissa[idx + rightshift] += bint;   // [tumble.c:621]
    tumblerjustify (cptr);
}
```

For `hintisa = 1.1.0.1` (`mantissa = [1,1,0,1,0,...]`), `idx=3`. With `rightshift=2`:
- writes `1` to `mantissa[5]`
- leaves `mantissa[4] = 0` untouched
- result: `[1,1,0,1,0,1,...]` = `1.1.0.1.0.1`

This is exactly what the comment says: *"create first child address as hintisa.0.1"* [`granf2.c:220,236`].

With `rightshift=1` (`depth=1`, same-type), the zero slot is NOT skipped — no `.0.` separator appears.

---

### 4. `tumbleraccounteq` Interprets the Zero as a Boundary

The zero digit is not just produced by baptism — it is actively interpreted by `tumbleraccounteq` [`tumble.c:38–70`], the function that tests whether a document address falls within an account's namespace:

```c
bool tumbleraccounteq(tumbler *aptr, tumbler *bptr)
{
    /* Compare until account (bptr) terminates with two zeros.
       Key insight: When account has a zero, it marks the boundary of the
       account's address space. */
    for (j_b = 0, i = 0; i < NPLACES; i++) {
        if (bptr->mantissa[i] == 0) {
            if (++j_b == 2) {
                return(TRUE);  /* Account terminated, document is under this account */
            }
            /* First zero in account - document can have any value here */
        } else {
            if (aptr->mantissa[i] != bptr->mantissa[i]) {
                return(FALSE);
            }
        }
    }
    return (TRUE);
}
```

For the default account `1.1.0.1` [`be.c:37`]:
```c
tumbler defaultaccount = {0,0,0,0, 1,1,0,1,0,0,0,0}; /* 1.1.0.1 */
```

Its mantissa is `[1, 1, 0, 1, 0, 0, ...]`. The two trailing zeros terminate the account's range. A document at `1.1.0.1.0.1` (`[1,1,0,1,0,1,...]`) passes `tumbleraccounteq` because:
- position 0: account=1, doc=1 ✓
- position 1: account=1, doc=1 ✓
- position 2: account=0 → first zero, skip (doc may differ)
- position 3: account=1, doc=1 ✓
- position 4: account=0 → second zero → return TRUE

**The zero at position 2 is the `.0.` inside the account address itself.** `tumbleraccounteq` treats it as a "wildcard" slot — documents under this account may have any value there. This function would fail entirely if the zero separator were omitted.

---

### 5. The `hintlength` Guard in Address Allocation

The increment logic at [`granf2.c:240`]:

```c
tumblerincrement(isaptr, tumblerlength(isaptr)==hintlength ? depth : 0, 1, isaptr);
```

This tests whether the found lower bound (truncated to `hintlength+depth` digits) has the same length as the parent's address. If `tumblerlength == hintlength`, the lower bound didn't yet have a child at this depth, so we must increment by `depth` (spanning the zero gap). Otherwise we're already at child depth and increment by `0` (in-place). This comparison directly encodes the fact that `depth` positions (including the zero slot) separate parent from child.

---

### 6. The Commented-Out `klugefindisatoinsertnonmolecule`

The old buggy implementation [`granf2.c:183–201`] simply copied `hintisa` unchanged to `isaptr`:

```c
static int klugefindisatoinsertnonmolecule(...) {
    tumblercopy(&hintptr->hintisa, isaptr);
}
```

The bug report comment explains why this was wrong: *"the first document get the account address itself (1.1.0.1 instead of 1.1.0.1.0.1)"* [`granf2.c:151`]. The `.0.1` suffix is mandatory — without it, the document was created at its parent's address, corrupting the granfilade.

---

### Conclusion

The `.0.` zero digit is **structural**, not merely conventional, for three independent reasons:

1. **It is mechanically enforced by the type system.** `depth = (supertype == subtype) ? 1 : 2` [`granf2.c:209`] determines whether a zero slot is inserted. This is not a configuration or convention — it is computed from the types passed to `makehint` at every call site. Crossing a type boundary (ACCOUNT→DOCUMENT) always requires `depth=2` and therefore always produces a `.0.`.

2. **It is semantically interpreted by `tumbleraccounteq`.** [`tumble.c:38–70`] The zero positions in an account tumbler mark its namespace boundary — they are treated as wildcards during containment tests. An account without these zero separators would fail containment testing entirely.

3. **Baptism's correctness depends on measuring `hintlength` against the zero boundary.** [`granf2.c:209–242`] The algorithm uses `tumblertruncate(..., hintlength + depth, ...)` and the comparison `tumblerlength == hintlength` to detect whether it is still at the parent's level or has crossed into child space. This arithmetic is only correct because the zero digit at position `hintlength` (when `depth=2`) marks the exact boundary.

What is NOT structurally fixed: the `.0.` is not an independently parsed separator token. The tumbler representation has no special encoding for it — it is simply `mantissa[k] == 0`. You could imagine a universe where zeros are numerically equivalent to any other digit and level boundaries are tracked differently. But in *this* implementation, the zero position is load-bearing: baptism must place it at every type-level crossing, or both address allocation and account containment break.
