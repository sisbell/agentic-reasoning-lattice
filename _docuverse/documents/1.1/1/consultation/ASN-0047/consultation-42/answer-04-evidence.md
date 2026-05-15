## Question 4 [evidence]

> In udanax-green, are all entity addresses (nodes, accounts, documents) produced exclusively via inc(·, k) within the parent's ownership domain, and are all link addresses produced via inc(·, 0) on the link allocator's frontier under the home document's link prefix — or are non-conforming allocation paths possible?

## KB Synthesis

## Address Allocation in udanax-green

### Standard allocation mechanism

All allocation — documents, versions, links — uses the same stateless `findpreviousisagr` + increment pattern [SS-ADDRESS-ALLOC, Finding 0021, 0077]:

1. Compute an upper bound from the parent hint: `tumblerincrement(hintisa, depth-1, 1)`
2. Find the current maximum address below that bound via `findpreviousisagr`
3. Truncate to the appropriate depth and increment by 1 at `rightshift=0`
4. If no children exist yet, allocate the first child as `hintisa.0.1`

This is indeed `inc(frontier, 0)` within the parent's domain — no global counter, no session-local counter [Finding 0077]. The choice of `depth` controls which hierarchy level is crossed (depth=2 for ACCOUNT→DOCUMENT, depth=1 for DOCUMENT→DOCUMENT).

### Document and entity addresses: conforming path

For accounts, documents, and owned-document versions, allocation stays within the parent's domain. The containment check added after Bug 0013 explicitly enforces this: after `findpreviousisagr` returns a candidate, the system verifies prefix containment via `tumblertruncate` + `tumblereq` before using it [PRE-ADDRESS-ALLOC, Finding 0021]. Without that check, the prior-maximum search could escape account boundaries and seed allocation in the wrong namespace.

### Link addresses: conforming path

Link I-addresses follow the same `inc(frontier, 0)` pattern, but scoped to the home document's link subspace [ST-ADDRESS-ALLOC, Finding 0065]:

- Upper bound: `docISA.2.3` (element field 3, exclusive upper boundary of the `.0.2.x` link prefix)
- First link: `docISA.2.2.1` (hardcoded first-child convention under element field 2)
- Subsequent links: `tumblerincrement(lowerbound, 0, 1, isaptr)` from the current maximum

Each document maintains an independent link allocation counter. MAKELINK on document B after MAKELINK on document A allocates from `B.0.2.x` — independent of A's frontier [Finding 0065 concrete example].

### Non-conforming path: VERSION of unowned documents

One documented, intentional departure from the "child under source" model: when a user versions a document they do not own, the ownership check `tumbleraccounteq(isaptr, wheretoputit) && isthisusersdocument(isaptr)` fails, and allocation falls back to `makehint(ACCOUNT, DOCUMENT, 0, wheretoputit, &hint)` [SS-VERSION-ADDRESS, Finding 0068]. This is identical to CREATE behavior — the version lands under the creating user's account, not under the source document.

```
User A owns doc 1.1.0.1.0.1:
  VERSION → 1.1.0.1.0.1.1   (child of source — conforming)

User B (account 1.1.0.2) versions A's doc:
  VERSION → 1.1.0.2.0.1     (under B's account — non-conforming to "child" model)
```

This breaks the address-hierarchy encoding of version lineage: for cross-user versions, there is no structural address relationship between source and version [Finding 0068]. The spec must handle both allocation rules, conditioned on the ownership predicate.

### Summary

| Entity | Path | Conforming? |
|--------|------|-------------|
| Document under account | `inc(max_child(account), 0)` within account prefix | Yes |
| Version of owned document | `inc(max_child(source_doc), 0)` within source prefix | Yes |
| Version of unowned document | `inc(max_child(user_account), 0)` under creator's account | **Non-conforming** |
| Link under home document | `inc(max_link(home_doc.0.2), 0)` within `.0.2.x` | Yes |

The granfilade is stateless with respect to allocation: `next_addr = max_iaddr(granf_subtree) + 1` in all cases. The sole non-conforming allocation path is the ownership-conditional VERSION dispatch, which is a designed behavioral branch, not a bug [SS-VERSION-ADDRESS]. Bug 0013 (pre-fix cross-account escape) no longer applies [PRE-ADDRESS-ALLOC].

---

## Code Exploration

I now have a complete trace. Here is the full analysis.

---

## Address Allocation in udanax-green: A Source Trace

### 1. The Central Allocator: `findisatoinsertgr`

All entity and atom ISA creation routes through:

```
createorglingranf  [granf1.c:50]
  → createorglgr   [granf2.c:111]
      → findisatoinsertgr [granf2.c:130]
```

`findisatoinsertgr` [granf2.c:130–156] dispatches on `subtype`:

```c
if (hintptr->subtype == ATOM) {
    findisatoinsertmolecule(fullcrumptr, hintptr, isaptr);
} else {
    findisatoinsertnonmolecule(fullcrumptr, hintptr, isaptr);
}
tumblerjustify(isaptr);
```

---

### 2. Entity Addresses: `findisatoinsertnonmolecule`

**All nodes, accounts, and documents** arrive here [granf2.c:203–242].

```c
static int findisatoinsertnonmolecule(typecuc *fullcrumptr, typehint *hintptr, typeisa *isaptr)
{
    depth = hintptr->supertype == hintptr->subtype ? 1 : 2;  // [granf2.c:209]
    hintlength = tumblerlength(&hintptr->hintisa);             // [granf2.c:211]

    tumblerincrement(&hintptr->hintisa, depth - 1, 1, &upperbound);  // [granf2.c:213]
    findpreviousisagr((typecorecrum*)fullcrumptr, &upperbound, &lowerbound);  // [granf2.c:217]

    if (iszerotumbler(&lowerbound) || !lowerbound_under_hint) {
        tumblerincrement(&hintptr->hintisa, depth, 1, isaptr);  // [granf2.c:237]  ← first child
    } else {
        tumblertruncate(&lowerbound, hintlength + depth, isaptr);
        tumblerincrement(isaptr, tumblerlength(isaptr)==hintlength ? depth : 0, 1, isaptr);  // [granf2.c:240]
    }
}
```

**Allocation is exclusively via `tumblerincrement`** — the `inc(·, k)` operation. The depth parameter `k` is:
- **`k = depth` = 1**: same-level allocation (NODE→NODE, DOCUMENT→DOCUMENT)
- **`k = depth` = 2**: cross-level allocation (ACCOUNT→DOCUMENT)

For subsequent items, `k = 0` if the truncated lower bound already reaches hint+depth, otherwise `k = depth`. In practice, once children exist, it degenerates to `k = 0` (incrementing the last digit of the previous sibling).

The search is bounded by `tumblerincrement(hintisa, depth-1, 1, &upperbound)` [granf2.c:213], which confines `findpreviousisagr` to addresses strictly within the hint's immediate subtree. The resulting ISA is always prefixed by `hintisa`.

---

### 3. Hint Construction and Ownership Domain

`makehint` [do2.c:78–84] simply copies fields into a `typehint`:

```c
int makehint(INT typeabove, INT typebelow, INT typeofatom, typeisa *isaptr, typehint *hintptr)
{
    hintptr->supertype = typeabove;
    hintptr->subtype   = typebelow;
    hintptr->atomtype  = typeofatom;
    movetumbler(isaptr, &hintptr->hintisa);
}
```

The `hintisa` determines the ownership domain. Call sites:

| Operation | Call site | `hintisa` source | Domain |
|---|---|---|---|
| `docreatenewdocument` | [do1.c:239] | `taskptr->account` | Current session's account |
| `docreatenewversion` (same account + owns it) | [do1.c:271] | `isaptr` (original doc) | Under the existing document |
| `docreatenewversion` (foreign doc) | [do1.c:275] | `wheretoputit` | Target account |
| `docreatenode_or_account` | [do1.c:251] | client-supplied tumbler | **Unchecked** |
| `docreatelink` (link atom) | [do1.c:207] | `docisaptr` | Home document |
| `doinsert` (text atom) | [do1.c:117] | `docisaptr` | Home document |

**The ownership domain holds** for documents and atoms — the hint is always the session account or an open document. **It does not hold for `CREATENODE_OR_ACCOUNT`**: `getcreatenode_or_account` [get1.c:208–212] reads any client-supplied tumbler with no ownership validation:

```c
int getcreatenode_or_account(typetask *taskptr, tumbler *tp)
{
    gettumbler(taskptr, tp);   // raw tumbler from wire, no check
    return(TRUE);
}
```

The backend then creates a child under that arbitrary address.

---

### 4. Link ISA Addresses: `findisatoinsertmolecule`

**Link atoms** (`LINKATOM = 2`) are handled by [granf2.c:158–181]:

```c
static int findisatoinsertmolecule(typecuc *fullcrumptr, typehint *hintptr, typeisa *isaptr)
{
    tumblerincrement(&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound);  // [granf2.c:162]
    findpreviousisagr((typecorecrum*)fullcrumptr, &upperbound, &lowerbound);       // [granf2.c:164]
    ...
    } else if (hintptr->atomtype == LINKATOM) {
        tumblerincrement(&hintptr->hintisa, 2, 2, isaptr);           // [granf2.c:171] base = hintisa.0.2
        if (tumblercmp(&lowerbound, isaptr) == LESS)
            tumblerincrement(isaptr, 1, 1, isaptr);                   // [granf2.c:173] first: hintisa.0.2.1
        else
            tumblerincrement(&lowerbound, 0, 1, isaptr);              // [granf2.c:175] next: inc(frontier, 0)
    }
```

The link ISA prefix within a document is `hintisa.0.2` (LINKATOM=2, two zeros of right-shift). The search upper bound is `hintisa.0.3` [granf2.c:162], so link ISAs are strictly within `[hintisa.0.2, hintisa.0.3)`.

**The first link ISA is `hintisa.0.2.1`** (rightshift=1 from the `.0.2` base).  
**Subsequent links use `inc(frontier, 0)`**: `tumblerincrement(&lowerbound, 0, 1, isaptr)` [granf2.c:175] — increment the last significant digit of the previous link.

So links go: `hintisa.0.2.1`, `hintisa.0.2.2`, `hintisa.0.2.3`, … This IS `inc(·, 0)` on the link ISA frontier under the document's link prefix.

---

### 5. Link VSA Addresses: `findnextlinkvsa`

Link **virtual stream addresses** (VSAs — positions in a document's V-stream) are computed differently [do2.c:151–167]:

```c
bool findnextlinkvsa(typetask *taskptr, typeisa *docisaptr, tumbler *vsaptr)
{
    tumblerclear(&firstlink);
    tumblerincrement(&firstlink, 0, 2, &firstlink);   // firstlink = 2  [do2.c:157]
    tumblerincrement(&firstlink, 1, 1, &firstlink);   // firstlink = 2.1 [do2.c:158]

    doretrievedocvspan(taskptr, docisaptr, &vspan);
    tumbleradd(&vspan.stream, &vspan.width, &vspanreach);
    if (tumblercmp(&vspanreach, &firstlink) == LESS)
        movetumbler(&firstlink, vsaptr);              // at least 2.1
    else
        movetumbler(&vspanreach, vsaptr);             // or end of existing content
}
```

The link VSA is `max(2.1, document_vspan_reach)`. There is **no dedicated link VSA allocator** — the "frontier" is the end of all existing document content. The `2.x` subspace (VSA ≥ `2.1`) is the link subspace; text content occupies `1.x`.

This is **not** `inc(·, 0)` on a stored frontier. It's recomputed from the document's live V-span on every call.

`setlinkvsas` [do2.c:169–183] assigns **fixed relative offsets** within a link document's own V-space:
- from endpoint: `1.1`
- to endpoint: `2.1`
- three endpoint: `3.1`

These are hardcoded, not incrementally allocated.

---

### 6. Bootstrap: The Zero Account

In xumain (single-user) mode, `getaccount` [task.c:28–32] hardcodes the session account to zero:

```c
bool getaccount(typetask *taskptr, typeisa *accountptr)
{
    tumblerclear(accountptr);
    return(TRUE);
}
```

The zero tumbler is **not produced by `tumblerincrement`** — it is the root of the entire address space. Every document in xumain mode falls under the zero-account domain. `tumbleraccounteq` [tumble.c:38–70] treats any document as "under" the zero account (two consecutive zeros at the mantissa start terminate the account prefix match immediately), so `isthisusersdocument` always returns true in xumain mode.

In daemon mode, the account is read from the network via `getxaccount` [get1.c:190–204], using `gettumbler` — the client asserts its own account address, and there is no server-side proof of ownership.

---

### 7. Non-Conforming Paths

**Dead code — `klugefindisatoinsertnonmolecule`** [granf2.c:183–201]:

```c
static int klugefindisatoinsertnonmolecule(...)
{
#ifdef UnDeFIned
    tumblercopy(&hintptr->hintisa, isaptr);  // would copy parent addr as new entity addr
#endif
    tumblercopy(&hintptr->hintisa, isaptr);  // active: also copies parent addr!
}
```

This function is defined but **never called** — `findisatoinsertgr` [granf2.c:143–152] always calls `findisatoinsertnonmolecule` for non-atom types. However the function body itself (outside the `#ifdef`) would copy `hintisa` unchanged — placing the new entity at its parent's address. It is dead but present.

---

### Summary

| Claim | Verdict |
|---|---|
| Entity ISAs produced exclusively via `inc(·, k)` | **True.** All entity creation routes through `findisatoinsertnonmolecule` [granf2.c:203], which calls only `tumblerincrement`. k=depth (1 or 2) for the first child; k=0 for subsequent siblings. |
| Always within parent's ownership domain | **Conditionally true.** Documents: yes, hint is always the session account or an opened document. Nodes/accounts: **no** — hint is an arbitrary client-supplied tumbler with no ownership check [get1.c:208–212]. |
| Link ISAs via `inc(·, 0)` on frontier under home document's link prefix | **True** for subsequent links [granf2.c:175]. First link uses rightshift=1 from the `hintisa.0.2` base [granf2.c:173]. The prefix `hintisa.0.2` is the link allocator floor. |
| Link VSAs via `inc(·, 0)` on frontier | **False.** `findnextlinkvsa` [do2.c:151–167] computes VSA as `max(2.1, vspan_reach)` — derived from document content extent, not an explicit allocator state. |
| Non-conforming paths possible | **Yes.** (1) Dead kluge code [granf2.c:183–201] copies parent addr as new addr. (2) Bootstrap account is hardcoded zero, not `inc`-allocated [task.c:31]. (3) `CREATENODE_OR_ACCOUNT` accepts unchecked client-supplied hints [get1.c:208–212]. |
