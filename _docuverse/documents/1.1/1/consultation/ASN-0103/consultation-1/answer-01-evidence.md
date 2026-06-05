## Question 1 [evidence]

> When CREATENEWDOCUMENT allocates the next document address under an account, does udanax-green scan all child entities (versions included) or advance a dedicated document-chain frontier that excludes version addresses?

## KB Synthesis

## CREATENEWDOCUMENT Address Allocation: Full Scan, Not Frontier

The allocation scans **all descendant entities** under the account — documents and their version children alike. There is no dedicated document-chain frontier.

---

### The allocation algorithm

[SS-ADDRESS-ALLOC] Finding 0021 describes `findisatoinsertnonmolecule`:

1. Compute `upperbound = tumblerincrement(account, depth-1=1, 1)` — the **next sibling account** (e.g., `1.1.0.2` for account `1.1.0.1`)
2. Call `findpreviousisagr` to find the highest address **strictly below** that bound and under the account
3. Truncate to document level, increment → new address

The search range spans everything from the account address up to (but not including) the next sibling account. This includes:

```
1.1.0.1.0.1       (document 1)
1.1.0.1.0.1.1     (version 1 of doc 1)   ← included in scan
1.1.0.1.0.1.2     (version 2 of doc 1)   ← included in scan
1.1.0.1.0.1.1.1   (version of version)   ← included in scan
```

### Why versions fall in the scan range

[SS-VERSION-ADDRESS] Finding 0068: owned-document versions are allocated as **children** of their source document, not as siblings under the account. By tumbler total order [INV-TUMBLER-TOTAL-ORDER], `1.1.0.1.0.1.1 < 1.1.0.1.0.2` — a version sorts *below* the next document sibling, so it falls within the account search window.

[SS-TUMBLER-CONTAINMENT]: containment is prefix-match only. `1.1.0.1.0.1.1` truncated to length 4 gives `1.1.0.1`, which equals the account → it passes the containment check.

### The truncation step normalizes past versions

If `findpreviousisagr` returns `1.1.0.1.0.1.2` (7 digits, a version), the algorithm truncates to document depth:

- Account `1.1.0.1` has 4 digits; depth=2 means documents live at length 6 (`account.0.N`)
- Truncate `1.1.0.1.0.1.2` → `1.1.0.1.0.1`, increment → `1.1.0.1.0.2`

This is directly confirmed by Finding 0068's example for VERSION (depth=1): "Truncate to length 7: `1.1.0.1.0.1.1`, increment: `1.1.0.1.0.1.2`." The same truncate-and-increment pattern applies at every depth.

### No dedicated document frontier

[SS-ADDRESS-ALLOC] Finding 0077 is explicit: "There is no single global 'next' counter. Allocation is stateless query-and-increment on different tumbler ranges via `findpreviousisagr`." The granfilade tree is queried fresh on every allocation — no cached frontier, no version-aware counter, no separation between document and version address chains.

---

**Summary:** CREATENEWDOCUMENT runs a single `findpreviousisagr` scan that sweeps all descendants of the account (documents and versions alike), finds the maximum address in that range, then truncates to document depth and increments. Version addresses are traversed but neutralized by the truncation step.

---

## Code Exploration

I have everything I need. Here is the complete analysis.

---

## How CREATENEWDOCUMENT Allocates the Next Document Address

### Short Answer

There is **no dedicated document-chain frontier**. The code does scan all entities under the account — including versions and their content atoms — but a **truncation step** projects any found address back to document depth before incrementing, making version/atom addresses invisible to document allocation.

---

### Call Chain

```
createnewdocument() [fns.c:276]
  └─ docreatenewdocument() [do1.c:234]
       └─ createorglingranf() [granf1.c:50]
            └─ createorglgr() [granf2.c:111]
                 └─ findisatoinsertgr() [granf2.c:130]
                      └─ findisatoinsertnonmolecule() [granf2.c:203]
                           └─ findpreviousisagr() [granf2.c:255]
```

---

### Step 1 — `docreatenewdocument` builds the hint

```c
// do1.c:239
makehint (ACCOUNT, DOCUMENT, 0, &taskptr->account, &hint);
```

`makehint` [do2.c:78] copies four fields into a `typehint`:

```c
hintptr->supertype = ACCOUNT;   // 2
hintptr->subtype   = DOCUMENT;  // 3
hintptr->atomtype  = 0;
hintptr->hintisa   = taskptr->account;  // e.g. 1.1.0.1
```

The hint travels down to `findisatoinsertgr`.

---

### Step 2 — `findisatoinsertgr` routes to the non-molecule path

```c
// granf2.c:130-156
if (hintptr->subtype == ATOM) {
    findisatoinsertmolecule(...);
} else {
    findisatoinsertnonmolecule(...);   // ← taken here, subtype=DOCUMENT
}
tumblerjustify(isaptr);
```

---

### Step 3 — `findisatoinsertnonmolecule` does the actual allocation

```c
// granf2.c:203-242
depth = hintptr->supertype == hintptr->subtype ? 1 : 2;
// ACCOUNT(2) ≠ DOCUMENT(3)  →  depth = 2

hintlength = tumblerlength(&hintptr->hintisa);
// e.g. 4 for account 1.1.0.1

tumblerincrement(&hintptr->hintisa, depth - 1, 1, &upperbound);
// rightshift = 1; adds 1 to mantissa[idx+1] where idx = last non-zero
// account 1.1.0.1 (mantissa[3]=1) → upperbound = 1.1.0.1.1

findpreviousisagr((typecorecrum*)fullcrumptr, &upperbound, &lowerbound);
```

**`findpreviousisagr` [granf2.c:255] searches the granfilade for the highest ISA strictly less than `upperbound`.** It walks the enfilade tree comparing against `1.1.0.1.1` and records whatever entity it finds last. It does **not** filter by entity type.

Every entity allocated under account `1.1.0.1` — documents, versions, text atoms, link atoms — has an ISA less than `1.1.0.1.1`, so all are candidates. The function returns whichever has the lexicographically greatest tumbler address.

---

### Step 4 — The `lowerbound_under_hint` guard

```c
// granf2.c:228-233
tumblertruncate(&lowerbound, hintlength, &truncated);
lowerbound_under_hint = tumblereq(&truncated, &hintptr->hintisa);
```

Before doing anything with the found address, the code truncates it to the account length (4) and checks it still equals the account address. This guards against `findpreviousisagr` returning an entity from a neighboring account (e.g. `1.1.0.2.0.1`) when the current account has no children yet.

---

### Step 5 — Truncation projecting to document depth, then increment

```c
// granf2.c:239-240
tumblertruncate(&lowerbound, hintlength + depth, isaptr);
// hintlength(4) + depth(2) = 6 — truncate to document depth

tumblerincrement(isaptr, tumblerlength(isaptr)==hintlength ? depth : 0, 1, isaptr);
// If truncated length = 6 ≠ hintlength(4): rightshift=0, bumps last digit
```

**This truncation is everything.** Consider what happens for any entity under account `1.1.0.1`:

| `lowerbound` from `findpreviousisagr` | After `tumblertruncate(·, 6)` | After increment |
|---|---|---|
| `1.1.0.1.0.3` (document 3) | `1.1.0.1.0.3` | `1.1.0.1.0.4` |
| `1.1.0.1.0.3.2` (version 2 of doc 3) | `1.1.0.1.0.3` (position 6 zeroed) | `1.1.0.1.0.4` |
| `1.1.0.1.0.3.0.1.15` (text atom 15 under doc 3) | `1.1.0.1.0.3` (positions 6–8 zeroed) | `1.1.0.1.0.4` |
| `1.1.0.1.0.3.2.0.1.15` (text atom under version 2 of doc 3) | `1.1.0.1.0.3` (positions 6–9 zeroed) | `1.1.0.1.0.4` |

Every sub-document entity under document 3 collapses to `1.1.0.1.0.3` when truncated to 6 positions, because those entities' mantissa positions 4 and 5 always match the document-level prefix, and positions 6+ get zeroed out.

The first document (empty account) case uses the explicit path at `granf2.c:237`:

```c
if (iszerotumbler(&lowerbound) || !lowerbound_under_hint) {
    tumblerincrement(&hintptr->hintisa, depth, 1, isaptr);
    // tumblerincrement(1.1.0.1, 2, 1) → adds 1 to mantissa[idx+2]
    // → 1.1.0.1.0.1
}
```

---

### Why Version Addresses Don't Advance the Document Counter

Versions of a same-user document are allocated via:

```c
// do1.c:271
makehint (DOCUMENT, DOCUMENT, 0, isaptr, &hint);
```

With `depth = 1` (supertype == subtype), version ISAs are at `DOCUMENT.N` — e.g. `1.1.0.1.0.1.1`, `1.1.0.1.0.1.2`. These sort **higher** than the document itself in tumbler order, but **lower** than the next document: `1.1.0.1.0.1.N < 1.1.0.1.0.2` for any N. The version allocation's `upperbound` is `1.1.0.1.0.2` (the next document's address), so version searches never cross document boundaries.

When document allocation encounters a version address as the highest entity, the truncation-to-6 removes the version component and yields the correct document prefix, then increments it — exactly as if only the document existed.

---

### Summary

**`docreatenewdocument` scans all child entities** (documents, versions, content atoms) within the account's address space by calling `findpreviousisagr` with an upper bound of `account.1`. There is no dedicated document-chain frontier counter.

The mechanism that prevents version addresses from contaminating document allocation is **`tumblertruncate(lowerbound, hintlength + depth)` at `granf2.c:239`**: this projects whatever entity was found (at any nesting depth) back to the document-address depth before the increment. The document counter is therefore an emergent property — derived on the fly from the highest document-level prefix in the granfilade, not stored or advanced separately.
