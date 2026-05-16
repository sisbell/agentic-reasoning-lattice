## Question 9 [evidence]

> Does udanax-green allocate entity addresses of the form [N, 0, U, 0, D, k] (document address extended by one element-field component, zeros still = 2), and if so, what entity kind does this represent?

## KB Synthesis

Yes. The address form `N.0.U.0.D.k` — a document address with one additional component appended without a `.0.` separator — represents a **version document**.

From [SS-ADDRESS-ALLOC] Finding 0021, the depth encoding determines the separator structure:

| supertype | subtype | depth | separator |
|-----------|---------|-------|-----------|
| ACCOUNT | DOCUMENT | 2 | adds `.0.` boundary |
| DOCUMENT | DOCUMENT | 1 | no `.0.` boundary |

`makehint(DOCUMENT, DOCUMENT, 0, docisa, &hint)` at depth=1 appends directly: `N.0.U.0.D.k`.

This is confirmed by [SS-VERSION-ADDRESS] Findings 0007, 0032, and 0068:

```
Document:  1.1.0.1.0.1
Version 1: 1.1.0.1.0.1.1   (k=1)
Version 2: 1.1.0.1.0.1.2   (k=2)
Version of version: 1.1.0.1.0.1.1.1
```

The `k` value is allocated monotonically by the query-and-increment mechanism in `findisatoinsertnonmolecule` [SS-ADDRESS-ALLOC] Finding 0068. This allocation is purely a function of granfilade state — `findpreviousisagr` finds the highest existing child under `D`, truncates and increments.

**Ownership caveat**: This pattern only applies when the creating user owns document D. When they do not, `makehint(ACCOUNT, DOCUMENT, 0, wheretoputit, &hint)` (depth=2) places the version under the user's own account instead, producing `N.0.U'.0.k` — a sibling to other documents in U's account [SS-VERSION-ADDRESS] Finding 0068.

So `N.0.U.0.D.k` is unambiguously a **version document**, never a link orgl (which uses `N.0.U.0.D.0.2.k`) or a text atom.

---

## Code Exploration

Confirmed. The version golden test shows: document `1.1.0.1.0.1` → version `1.1.0.1.0.1.1` — exactly 7 components, still only 2 zeros. Now I have everything I need.

---

## Answer

**Yes — udanax-green does allocate entity addresses of the form [N, 0, U, 0, D, k] (zeros still = 2). They represent DOCUMENT VERSIONS created by the document's own owner.**

---

### The Evidence

#### 1. Entity type constants — `backend/xanadu.h:140–146`

```c
#define NODE      1
#define ACCOUNT   2
#define DOCUMENT  3
#define ATOM      4
                      /* atom types - don't change these */
#define TEXTATOM  1
#define LINKATOM  2
```

The `makehint` struct (`xanadu.h:148–153`) stores `supertype`, `subtype`, `atomtype`, and `hintisa`. For version creation the call is `DOCUMENT→DOCUMENT` — same type at both levels.

#### 2. Entry point — `backend/do1.c:260–276`

`docreatenewversion` contains the conditional that picks the allocation strategy:

```c
if (tumbleraccounteq(isaptr, wheretoputit) && isthisusersdocument(isaptr)) {
    makehint (DOCUMENT, DOCUMENT, 0, isaptr/*wheretoputit*/, &hint);  // line 271
} else {
    makehint (ACCOUNT, DOCUMENT, 0, wheretoputit, &hint);             // line 275
}
```

When the requester owns the document (`DOCUMENT→DOCUMENT`), the hint carries `supertype == subtype`. The `else` branch — creating a version of someone *else's* document — uses `ACCOUNT→DOCUMENT` and produces a fresh 6-component address in the requester's own account; that branch is irrelevant here.

#### 3. Depth calculation — `backend/granf2.c:209`

Inside `findisatoinsertnonmolecule`:

```c
depth = hintptr->supertype == hintptr->subtype ? 1 : 2;
```

`DOCUMENT == DOCUMENT` → `depth = 1`. This single value controls everything that follows.

#### 4. Upper bound — `backend/granf2.c:213`

```c
tumblerincrement (&hintptr->hintisa, depth - 1, 1, &upperbound);
```

`depth - 1 = 0`, so `rightshift = 0`: this just increments the *last* non-zero digit of `hintisa`. For document `1.1.0.1.0.1` (last non-zero at mantissa index 5), the upper bound is `1.1.0.1.0.2`. The search space is thus *within* the document's sibling range, not beyond it.

#### 5. New version address — `backend/granf2.c:235–241`

```c
if (iszerotumbler(&lowerbound) || !lowerbound_under_hint) {
    tumblerincrement(&hintptr->hintisa, depth, 1, isaptr);       // rightshift = 1
} else {
    tumblertruncate (&lowerbound, hintlength + depth, isaptr);   // keep hintlen+1 digits
    tumblerincrement(isaptr,
        tumblerlength(isaptr)==hintlength ? depth : 0, 1, isaptr);
}
```

**First version** (nothing yet allocated under the document): `rightshift = depth = 1`.

`tumblerincrement([1,1,0,1,0,1], rightshift=1, bint=1)`:
- last non-zero in mantissa at idx = 5
- add 1 at idx + 1 = **6** (one slot past the end of the document address)
- result mantissa: `[1,1,0,1,0,1,1,…]` → **`1.1.0.1.0.1.1`** (7 components, **2 zeros**, at indices 2 and 4)

**Subsequent versions**: `findpreviousisagr` returns the prior version (e.g., `1.1.0.1.0.1.1`, tumblerlength = 7 ≠ hintlength 6). `tumblertruncate` to `hintlength + depth = 7` keeps all 7 digits; `tumblerincrement` with `rightshift=0` then increments the last digit:
- `1.1.0.1.0.1.1` → `1.1.0.1.0.1.2`, then `.3`, etc.

All of these have exactly **2 zeros** (inherited from the parent document address).

#### 6. Confirmation from golden tests

`backend/granf2.c` `findisatoinsertmolecule` line 158 (ATOM allocation) uses `rightshift=2`, which adds *two* new slots and a fresh zero separator, producing 9-component addresses like `1.1.0.1.0.1.0.2.1`. That is a **different** structure (3 zeros). Document versions use `depth=1` / `rightshift=1` and produce the **zero-count-preserving** 7-component form.

Golden test `golden/versions/create_version.json`:
```
create_document → "1.1.0.1.0.1"   (6 comp, 2 zeros)
create_version  → "1.1.0.1.0.1.1" (7 comp, 2 zeros)  ✓
```

Golden test `golden/links/create_link.json`:
```
create_link → "1.1.0.1.0.1.0.2.1" (9 comp, 3 zeros — ATOM, not the same form)
```

---

### Summary

| Address form | Components | Zeros | Entity kind |
|---|---|---|---|
| `1.1.0.1.0.1` | 6 | 2 | Base document |
| `1.1.0.1.0.1.1`, `.2`, … | 7 | **still 2** | **Document version** (same-owner) |
| `1.1.0.1.0.1.0.1.1` | 9 | 3 | TEXTATOM (text content in granfilade) |
| `1.1.0.1.0.1.0.2.1` | 9 | 3 | LINKATOM (link orgl in granfilade) |

Addresses of the form **[N, 0, U, 0, D, k]** — a document address extended by one element-field component without adding a new zero separator — represent **document versions**. The version counter `k` starts at 1 and increments for each new version of the same document. This is the only allocation path that uses `depth=1` (`DOCUMENT→DOCUMENT` hint), causing `tumblerincrement` to be called with `rightshift=1` — enough to append one digit beyond the document address, but not enough to insert a new zero-separator between levels.
