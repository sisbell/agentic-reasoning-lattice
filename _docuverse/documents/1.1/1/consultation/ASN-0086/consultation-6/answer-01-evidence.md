## Question 1 [evidence]

> In udanax-green, can a link address appear as a strict prefix of another link address (i.e., does the implementation ever spawn a link under an existing link via `inc(linkAddr, 1)`), or is `dom(L)` always flat with respect to prefix-ordering?

## KB Synthesis

## Link address domain is flat — no prefix nesting

The KB entries make this definitive.

**Allocation produces strictly sequential siblings**

[SS-ADDRESS-ALLOC, Finding 0065] gives the concrete mechanism. For document D, link addresses are allocated as:

```
D.0.2.1, D.0.2.2, D.0.2.3, ...
```

The key is the increment call: `tumblerincrement(&lowerbound, 0, 1, isaptr)` with `rightshift=0`. At `rightshift=0` the increment touches only the last significant digit, producing `.2.1 → .2.2 → .2.3` — these are siblings, never children.

**No depth-1 allocation under an existing link**

[SS-ADDRESS-SPACE, Finding 0021] distinguishes the two allocation paths:
- `findisatoinsertnonmolecule` — used for document/version addresses; `depth` parameter controls hierarchy (depth=1 creates a child, depth=2 crosses an `.0.` boundary).
- `findisatoinsertmolecule` — used for links ([SS-ADDRESS-ALLOC, Finding 0065]). This path **only ever** does `rightshift=0` increments; there is no mechanism by which it places an address under an existing link's address.

**Prefix check confirms no nesting**

[SS-TUMBLER-CONTAINMENT] defines containment as: truncate A to the length of B, compare for equality. `D.0.2.1` truncated to its own length equals itself, which is ≠ `D.0.2.2`. The two addresses have the same tumbler length and differ in the last digit — neither is a prefix of the other.

For `D.0.2.1` to be a prefix of some link X, X would need the form `D.0.2.1.something` (strictly longer, matching on the prefix). This never occurs because the allocator never uses depth=1 under a link address.

**Concrete confirmation** [SS-LINK-HOME-DOCUMENT, Finding 0025]:

> "The first link under a home document gets suffix `.0.2.1`, subsequent links get `.0.2.2`, `.0.2.3`, etc."

**Answer:** `dom(L)` is always a flat antichain under the prefix order. The implementation never spawns a link under an existing link address; every link allocation is a sibling increment at the same tumbler depth.

---

## Code Exploration

Now I have everything needed. Here is the full answer with precise line citations.

---

## Link Address Prefix Structure in udanax-green

**Short answer: `dom(L)` is flat. No link ISA address is ever a strict prefix of another. The implementation never spawns a link under an existing link via `inc(linkAddr, 1)` or any other mechanism.**

---

### 1. How link ISA addresses are assigned — `docreatelink` in `do1.c:195`

Every link begins here:

```c
// do1.c:207
makehint (DOCUMENT, ATOM, LINKATOM, docisaptr, &hint);
// do1.c:209
createorglingranf (taskptr, granf, &hint, linkisaptr)
```

`makehint` fills a `typehint` struct (`xanadu.h:148-153`):
- `hint.supertype = DOCUMENT` (3)
- `hint.subtype = ATOM` (4)
- `hint.atomtype = LINKATOM` (2, defined at `xanadu.h:146`)
- `hint.hintisa = *docisaptr` — **the parent document's address, never a link's address**

This is the only call site for link creation. `hintisa` is hardwired to the document; there is no code path that sets `hintisa` to an existing link's ISA.

---

### 2. Address allocation inside the granfilade — `findisatoinsertmolecule` in `granf2.c:158`

Because `hint.subtype == ATOM`, `findisatoinsertgr` (`granf2.c:130`) routes to `findisatoinsertmolecule`. The LINKATOM branch is:

```c
// granf2.c:162  (atomtype = LINKATOM = 2, so atomtype+1 = 3)
tumblerincrement (&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound);
// upperbound = docaddr extended by 2 positions, value atomtype+1=3

clear (&lowerbound, sizeof(lowerbound));
findpreviousisagr (..., &upperbound, &lowerbound);   // highest existing link below upperbound

// granf2.c:165-176
if (tumblerlength (&hintptr->hintisa) == tumblerlength (&lowerbound)) {
    tumblerincrement (&lowerbound, 2, hintptr->atomtype, isaptr);  // line 166
    tumblerincrement (isaptr, 1, 1, isaptr);                        // line 167
} else if (hintptr->atomtype == TEXTATOM) {
    tumblerincrement (&lowerbound, 0, 1, isaptr);                   // line 169
} else if (hintptr->atomtype == LINKATOM) {
    tumblerincrement (&hintptr->hintisa, 2, 2, isaptr);             // line 171
    if (tumblercmp (&lowerbound, isaptr) == LESS)
        tumblerincrement (isaptr, 1, 1, isaptr);                    // line 173
    else
        tumblerincrement (&lowerbound, 0, 1, isaptr);               // line 175
}
```

Understanding `tumblerincrement` (`tumble.c:599-623`): `tumblerincrement(a, rightshift, bint, c)` finds the last nonzero mantissa index `idx` of `a` and adds `bint` at position `idx + rightshift`. A rightshift of 0 increments at the same depth; rightshift > 0 extends to a deeper digit position.

The three branches for LINKATOM:

| Condition | Result | What it means |
|---|---|---|
| `len(docaddr) == len(lowerbound)` (line 165) | `lowerbound` extended by 2, then +1 | No link found at right depth; allocates from lowerbound at docaddr depth+2 |
| LINKATOM, first link under this doc (line 171) | `docaddr` + rightshift 2, value 2 | Produces `docaddr.0.2` — first link |
| LINKATOM, subsequent link (line 175) | `lowerbound` + rightshift 0, value 1 | Increments last digit of previous link at the **same depth** |

In every branch, the result lives at exactly `tumblerlength(docaddr) + 2` digits deep. All links for a given document share the same tumbler depth. No branch derives a new link's address from a previous link's address with any positive rightshift, which would be required to create a child address.

---

### 3. Why `inc(linkAddr, 1)` is structurally impossible as a parent

For link L2 to be a child of L1, the code would need to call something equivalent to:

```c
makehint (DOCUMENT, ATOM, LINKATOM, linkisaptr, &hint);  // hintisa = L1's address
```

This never occurs. `docreatelink` (`do1.c:195`) always passes `docisaptr` — the document address — as the fourth argument to `makehint` (line 207). There is no variant that passes another link's ISA. The function signature enforces this: `docisaptr` is the document parameter, and the caller (`fns.c`) always provides it from the open-document context.

---

### 4. Link V-addresses are also flat — `findnextlinkvsa` in `do2.c:151`

Beyond the ISA (granfilade) addresses, the V-addresses assigned to links inside the document's virtual stream are also sequentially flat:

```c
// do2.c:156-165
tumblerclear (&firstlink);
tumblerincrement (&firstlink, 0, 2, &firstlink);  // firstlink = 0.0.2 (internal)
tumblerincrement (&firstlink, 1, 1, &firstlink);  // firstlink = 0.0.2.0.1
...
if (tumblercmp (&vspanreach, &firstlink) == LESS)
    movetumbler (&firstlink, vsaptr);   // first link gets firstlink
else
    movetumbler (&vspanreach, vsaptr);  // next link placed after current reach
```

Each new link is placed sequentially at or after the reach of the previous one — same depth, never nested.

---

### Conclusion

`dom(L)` is provably flat under prefix-ordering. Every link's ISA address is produced by extending the **document's** address by exactly 2 tumbler digits (`rightshift=2`); subsequent links at the same depth increment the last digit (`rightshift=0`). No call in any code path passes an existing link's address as `hintisa`, and `tumblerincrement` with `rightshift=0` never produces a child tumbler — it stays at the same depth. Therefore no link address is ever a strict prefix of another.
