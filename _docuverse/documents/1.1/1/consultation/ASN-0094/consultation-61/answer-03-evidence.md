## Question 3 [evidence]

> In udanax-green, do document-level tumblers ever carry `zeros(d) > 2`, or does the implementation strictly maintain the four-field (N, U, D, E) hierarchy with two field-separator zeros at the document level — making the Step II.1 general additivity argument trivial at every substrate-reachable input?

## KB Synthesis

## Document-Level Tumbler Zero Count in udanax-green

The KB evidence supports: **document-level tumblers are strictly bounded to `zeros(d) = 2`**, and the four-field hierarchy is preserved at every substrate-reachable document address.

---

### The Zero-Count Structure by Address Type

**Accounts** — one zero separator:
> `1.1.0.2` — `Node.0.User`

**Documents under accounts** — two zero separators:
> `1.1.0.2.0.1` — `Node.0.User.0.Doc`

This is enforced by `makehint(ACCOUNT, DOCUMENT, depth=2, ...)`, which calls `tumblerincrement(hintisa, depth-1=1, 1)` — adding exactly one `.0.` crossing to produce the document field. [SS-ADDRESS-ALLOC], [SS-TUMBLER-CONTAINMENT]

**Versions** — still two zero separators:
> `1.1.0.1.0.1.1` (owned), `1.1.0.1.0.1.1.1` (version of version)

VERSION uses `makehint(DOCUMENT, DOCUMENT, depth=1, ...)`, which calls `tumblerincrement(hintisa, 0, 1)` — zero rightshift means the new digit appends to the document field *without* a `.0.` crossing. The pattern is `N.0.U.0.D.V.W...` with exactly two separators regardless of version chain depth. [SS-VERSION-ADDRESS], [SS-ADDRESS-SPACE]

**Unowned versions** — placed under the creating user's account as a new document sibling:
> User B (`1.1.0.2`) versions User A's doc → `1.1.0.2.0.1` — two zeros, same structure. [SS-VERSION-ADDRESS]

---

### The Element Level Breaks the Pattern — But Is Not a Document

Element-level tumblers (atoms, links) **do** have three zeros:
> `1.1.0.1.0.1.0.2.1` — `Node.0.User.0.Doc.0.ElementType.ElementNum`

From `makehint(DOCUMENT, ATOM, ...)`, which crosses into the element subspace with the third `.0.`. [SS-ADDRESS-SPACE]

But these are **not document orgls** — they are content/link entries. The granfilade dispatch in `findisatoinsertgr` explicitly bifurcates: non-molecule paths (documents, versions) use `findisatoinsertnonmolecule`; molecule paths (text atoms, link orgls) use `findisatoinsertmolecule`. [SS-ADDRESS-SPACE]

---

### Why `zeros(d) > 2` Cannot Arise at the Document Level

The `makehint` depth table exhausts all substrate-reachable document allocation cases:

| supertype | subtype | depth | `rightshift = depth-1` | `.0.` added? |
|-----------|---------|-------|------------------------|--------------|
| ACCOUNT | DOCUMENT | 2 | 1 | Yes — produces second `.0.` |
| DOCUMENT | DOCUMENT | 1 | 0 | No — appends to existing doc field |

There is no `(X, DOCUMENT, depth=3)` case. The allocator `findisatoinsertnonmolecule` only ever calls `tumblerincrement` with rightshift ∈ {0, 1} for document addresses, which means:

- rightshift=1 → crosses one additional `.0.` boundary (account→document)
- rightshift=0 → no boundary crossing (document→version)

No mechanism exists to produce a document-level ISA with three or more field separators. [SS-ADDRESS-ALLOC]

---

### Consequence for the Additivity Argument

Because every document-level tumbler reachable via the substrate has the form:

```
1.N.0.U.0.D[.V]*
```

with **exactly two `.0.` separators** preceding the document/version digits, the domain is structurally flat at the document level. The digit positions after the second `.0.` are a simple monotonic extension (version chain depth) with no intervening separators.

This means a Step II.1 additivity argument over document-level tumblers is indeed trivial: the two separator zeros partition the address into three fixed-depth components (Node, User, Doc/VersionChain), and arithmetic within the Doc/VersionChain component never escapes into a deeper subspace because `tumblerincrement` with rightshift=0 operates strictly within the last contiguous digit run.

The only potential complication — the `strongsub` exponent guard ([SS-TUMBLER], Finding 0055) — is also non-issue here: document addresses have exponent=0 (all digits in the integer range), so cross-exponent subtraction cannot occur between two document-level tumblers, and additivity holds without qualification.

---

## Code Exploration

I now have all the source evidence needed. Here is the complete answer.

---

## Answer: `zeros(d)` at the Document Level in udanax-green

### The Tumbler Representation

`common.h:59-65`:
```c
typedef struct structtumbler {
    humber xvartumbler;
    char varandnotfixed;
    char sign;
    short exp;
    tdigit mantissa[NPLACES];   /* NPLACES = 16 */
} tumbler;
```

`exp` is a non-positive short. `exp = -k` encodes `k` implicit leading zeros. Internal zero-valued positions in `mantissa[]` serve as field separators. `zeros(d)` — the count of separator zeros in the active region of a document-level tumbler — is determined by the structure of both the account and the offset added at document-creation time.

---

### The Default Account Has Exactly One Internal Zero

`be.c:37`:
```c
tumbler defaultaccount = {0,0,0,0,  1,1,0,1,0,0,0,0};  /* 1.1.0.1 */
```

`socketbe.c:35`:
```c
tumbler defaultaccount = {0,0,0,0,  1,1,0,14,0};        /* 1.1.0.14 */
```

Both have `exp=0`, `sign=0`, and a mantissa of the form `{N, U, 0, D, 0, 0, ...}` with exactly **one explicit zero separator** at index 2, followed by the last non-zero at index 3.

---

### Document Creation: `depth=2` Is the Key Invariant

`do1.c:239`:
```c
makehint(ACCOUNT, DOCUMENT, 0, &taskptr->account, &hint);
return (createorglingranf(taskptr, granf, &hint, isaptr));
```

`do2.c:78-83` — `makehint` sets `hint.supertype = ACCOUNT(2)`, `hint.subtype = DOCUMENT(3)`.

`granf2.c:209`:
```c
depth = hintptr->supertype == hintptr->subtype ? 1 : 2;
```

Since `ACCOUNT(2) != DOCUMENT(3)`, `depth = 2`.

`granf2.c:235-237` (first document under an account):
```c
if (iszerotumbler(&lowerbound) || !lowerbound_under_hint) {
    tumblerincrement(&hintptr->hintisa, depth, 1, isaptr);   /* depth == 2 */
```

`tumble.c:599-622` — `tumblerincrement(aptr, rightshift=2, bint=1, cptr)` for non-zero `aptr`:
```c
for (idx = NPLACES; aptr->mantissa[--idx] == 0 && idx > 0;);
cptr->mantissa[idx + rightshift] += bint;
tumblerjustify(cptr);
```

For account `{1,1,0,1,0,...}`, `idx=3` (last non-zero). The new digit lands at `mantissa[3+2] = mantissa[5]`. The result:

```
mantissa = {1, 1, 0, 1, 0, 1, 0, ...}
            N  U  ·  D  ·  E
               └────────────┘ zeros at [2] and [4]
```

This is `1.1.0.1.0.1` — **exactly two internal zeros**, at mantissa indices 2 and 4.

---

### Versions Also Maintain `zeros(d) == 2`

`do1.c:271`:
```c
makehint(DOCUMENT, DOCUMENT, 0, isaptr, &hint);
```

With `supertype == subtype`, `depth = 1` [`granf2.c:209`]. The version number appends at `mantissa[idx+1]` — no new zero separator is introduced. Result: `{1,1,0,1,0,1,v,...}` with zeros still at indices 2 and 4 only. `zeros(d) = 2`.

---

### The Critical Gap: `validaccount` Is a Stub

`get2.c:157-160`:
```c
bool validaccount(typetask *taskptr, typeisa *accountptr)
{
    return(TRUE);
}
```

`get2fe.c:338-341`:
```c
bool validaccount(typetask *taskptr, typeisa *accountptr)
{
    return (TRUE);
}
```

**Both implementations unconditionally return TRUE.** There is no structural check on the account tumbler received via the XACCOUNT command. A client sending an account like `1.1.0.1.0.1` (two internal zeros) would cause `tumblerincrement(..., depth=2, ...)` to place the first document at `{1,1,0,1,0,1,0,1,...}` — **three internal zeros**, `zeros(d) = 3`.

---

### The `nzeroesintumbler` Function Is Commented Out

`tumble.c:264-276`:
```c
/*  INT
nzeroesintumbler (tumblerptr)
  tumbler *tumblerptr;
{
  INT n, i, count;
  ...
  count -= tumblerptr->exp;
  return (count);
}*/
```

The function that would count internal zeros exists in the source as dead code. No runtime check on `zeros(d)` exists anywhere in the system.

---

### What `tumbleraccounteq` Actually Checks

`tumble.c:54-70`:
```c
for (j_b = 0, i = 0; i < NPLACES; i++) {
    if (bptr->mantissa[i] == 0) {
        if (++j_b == 2) {
            return(TRUE);
        }
    } else {
        if (aptr->mantissa[i] != bptr->mantissa[i]) {
            return(FALSE);
        }
    }
}
```

This returns TRUE upon finding the **second** zero in the account's mantissa. For the standard account `{1,1,0,1,0,...}`: zero at index 2 (`j_b=1`), then zero at index 4 (the first trailing zero after `mantissa[3]=1`, `j_b=2`) — TRUE. This function **assumes** accounts terminate with exactly one explicit zero followed by trailing zeros. It does not enforce it — it would silently misclassify documents under malformed accounts.

---

### Conclusion

**Within the set of tumblers allocated by the system** — i.e., for all document-level addresses produced by `docreatenewdocument`, `docreatenewversion`, or any path through `findisatoinsertnonmolecule` — `zeros(d) == 2` is a strict invariant. It is maintained mechanically by the hardcoded `depth = 2` at `ACCOUNT→DOCUMENT` transitions [`granf2.c:209`] and `depth = 1` at `DOCUMENT→DOCUMENT` transitions, with `tumblerincrement` placing the new digit at `idx+depth` without inserting intermediate zeros.

**At the protocol boundary, `zeros(d) > 2` is possible.** `validaccount` is a stub (`get2.c:159`, `get2fe.c:340`). Any client can register an account tumbler with 2+ internal zeros, and documents created under it will have 3+ zeros. No runtime guard enforces the N.U.D.E four-field structure.

**For the Step II.1 general additivity argument:** The argument holds trivially for every tumbler the system itself generates, because `depth=2` at document creation is the sole code path. All substrate-reachable document tumblers have the form `N.U.0.D.0.E.v...` with exactly two zero-separator positions and `exp=0`. The additivity properties depend on `tumbleraccounteq` correctly identifying account boundaries, which it does for this structure. However, the proof cannot be grounded in enforcement — it depends on the assumption that all account tumblers in the system adhere to the one-explicit-zero convention, which the code assumes but does not validate.
