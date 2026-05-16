## Question 1 [evidence]

> Does udanax-green allocate node addresses as single-component identifiers, and does any code path enforce or assume single-component node addresses?

## KB Synthesis

## Node Address Allocation in udanax-green

The KB provides a partial but meaningful answer.

### Nodes use single-component (depth=1) allocation

[SS-ADDRESS-SPACE] Finding 0021 documents the `makehint` depth table:

| supertype | subtype | depth | Meaning |
|-----------|---------|-------|---------|
| NODE | NODE | 1 | Node under node |
| ACCOUNT | DOCUMENT | 2 | Document under account |
| DOCUMENT | DOCUMENT | 1 | Version under document |

Depth determines `.0.` boundary crossings. Depth=1 means **no `.0.` separator** — a child node under `1.1` gets address `1.1.1`, `1.1.2`, etc. Contrast with ACCOUNT→DOCUMENT at depth=2, which produces `1.1.0.2.0.1` (one `.0.` crossing).

The concrete examples confirm: `1.1.0.1` → next sibling node is `1.1.0.1.1` (single component appended, no `.0.`).

### How the assumption is encoded

The `makehint` function (at `do2.c:78-84`) copies the hint ISA and encodes the depth. For NODE→NODE, it sets `depth=1`, which flows into `findisatoinsertnonmolecule` via:

```
upperbound = tumblerincrement(hintisa, depth-1, 1)
```

At depth=1, `rightshift = 0`, so `tumblerincrement` increments at the current precision level — appending exactly one component without crossing a `.0.` boundary. The allocation is then `findpreviousisagr` + increment, producing the next sequential sibling.

### What the KB does not tell us

The KB lacks findings that directly inspect node-specific enforcement code beyond the `makehint` dispatch. There is no documented finding showing a runtime guard that *rejects* a multi-component node address, or code that *assumes* a fixed node-component count. The enforcement is structural — the depth=1 encoding in `makehint` is the only documented mechanism — not a runtime predicate check.

The containment check ([SS-TUMBLER-CONTAINMENT]) uses prefix matching (`tumblertruncate` + `tumblereq`), which would work correctly whether a node had one or multiple components, so it does not specifically enforce single-component node addresses.

**Summary:** Node addresses are allocated as single-component additions by the `makehint` depth=1 encoding [SS-ADDRESS-SPACE], but the KB provides no evidence of code that independently enforces or validates the single-component constraint on node addresses beyond that encoding.

---

## Code Exploration

I now have all the evidence needed from the source. Here is my complete finding:

---

## Node Address Allocation: Single-Component Analysis

**Short answer:** Node addresses are **not** single-component identifiers. They are multi-component tumblers that extend the parent account address by exactly one digit. No code path enforces or assumes single-component node addresses; the `is1story()` predicate exists but is only applied to content widths and POOM cuts.

---

### 1. Tumbler Structure

**`backend/common.h:53,59-65`**

```c
#define NPLACES 16  /* places in mantissa of tumbler - increased from 11 to support deeper version chains */

typedef struct structtumbler {
    humber xvartumbler;
    char varandnotfixed;
    char sign BIT;
    short exp;
    tdigit mantissa[NPLACES];
} tumbler;
```

A tumbler holds up to 16 mantissa components. The comment at line 53 is explicit: NPLACES was **expanded from 11 to 16** to accommodate deeper chains — the design always assumed multi-component addresses.

**`backend/xanadu.h:140-143`**

```c
#define NODE      1
#define ACCOUNT   2
#define DOCUMENT  3
#define ATOM      4
```

---

### 2. Node Allocation Entry Point

**`backend/fns.c:375-386`** — FEBE handler `createnode_or_account`:

```c
void createnode_or_account(typetask *taskptr)
{
  tumbler t;
  bool getcreatenode_or_account(), docreatenode_or_account();

    if(	getcreatenode_or_account(taskptr,&t)
         && docreatenode_or_account(taskptr,&t)) {
        putcreatenode_or_account(taskptr,&t);
    } else {
        putrequestfailed(taskptr);
    }
}
```

**`backend/get1.c:208-212`** — reads one tumbler from client as the allocation hint:

```c
int getcreatenode_or_account(typetask *taskptr, tumbler *tp)
{
  gettumbler(taskptr,tp);
  return(TRUE);
}
```

**`backend/do1.c:243-258`** — the core allocation:

```c
bool docreatenode_or_account(typetask *taskptr, typeisa *isaptr)
{
  typeisa isa;
  typehint hint;

    tumblercopy(isaptr, &isa);
    makehint (NODE, NODE, 0, &isa, &hint);
    result = createorglingranf (taskptr, granf, &hint, &isa);
    if (result) {
        tumblercopy(&isa, isaptr);
    }
    return result;
}
```

The client sends a hint tumbler (the account address); the backend passes it to `makehint(NODE, NODE, ...)`.

---

### 3. The `depth` Arithmetic in `findisatoinsertnonmolecule`

**`backend/granf2.c:203-242`** — the address-finding logic:

```c
static int findisatoinsertnonmolecule(typecuc *fullcrumptr, typehint *hintptr, typeisa *isaptr)
{
  typeisa upperbound, lowerbound, truncated;
  INT depth, hintlength;
  bool lowerbound_under_hint;

    depth = hintptr->supertype == hintptr->subtype ? 1 : 2;  // LINE 209

    hintlength = tumblerlength (&hintptr->hintisa);

    tumblerincrement (&hintptr->hintisa, depth - 1, 1, &upperbound);
    ...
    if (iszerotumbler(&lowerbound) || !lowerbound_under_hint) {
        /* Nothing under this hint - create first child as hintisa.0.1 */
        tumblerincrement(&hintptr->hintisa, depth, 1, isaptr);  // LINE 237
    } else {
        tumblertruncate (&lowerbound, hintlength + depth, isaptr);
        tumblerincrement(isaptr,tumblerlength(isaptr)==hintlength?depth:0,1,isaptr);  // LINE 240
    }
}
```

For `makehint(NODE, NODE, ...)`: `supertype == subtype` → **`depth = 1`** [line 209].

**`backend/tumble.c:599-623`** — `tumblerincrement(aptr, rightshift, bint, cptr)`:

```c
int tumblerincrement(tumbler *aptr, INT rightshift, INT bint, tumbler *cptr)
{
  register INT idx;
    ...
    for (idx = NPLACES; aptr->mantissa[--idx] == 0 && idx > 0;);
    if (idx + rightshift >= NPLACES) { gerror("overflow"); }
    cptr->mantissa[idx + rightshift] += bint;
    tumblerjustify(cptr);
}
```

With `rightshift = depth = 1`: adds `bint` at position `idx + 1`, where `idx` is the last non-zero mantissa position of `hintisa`. This appends **one new component** to the hint address.

**Concrete trace** for account `1.1.0.1` (mantissa `{1,1,0,1,0,...}`, idx=3):
- `idx + rightshift = 3 + 1 = 4`
- First node: `mantissa[4] = 1` → **`1.1.0.1.1`** (5 components)
- Second node: `mantissa[4] = 2` → **`1.1.0.1.2`**
- Third node: `mantissa[4] = 3` → **`1.1.0.1.3`**

---

### 4. Confirmed by Golden Tests

**`golden/accounts/create_node.json`**:
```json
{ "op": "account",      "account": "1.1.0.1" }
{ "op": "create_node",  "account": "1.1.0.1",  "result": "1.1.0.1.1" }
```

**`golden/accounts/create_multiple_nodes.json`**:
```json
{ "op": "create_node",  "result": "1.1.0.1.1" }
{ "op": "create_node",  "result": "1.1.0.1.2" }
{ "op": "create_node",  "result": "1.1.0.1.3" }
```

Node addresses are 5-component tumblers: the 4-component account prefix plus one serial digit. The serial digit is single-component, but the full node address is not.

---

### 5. `is1story()` — What It Actually Checks

**`backend/tumble.c:234-247`**:

```c
/* says whether there is no more than a single non-zero digit in mantissa */
bool is1story(tumbler *tumblerptr)
{
  INT i;
  for (i = 1; i < NPLACES; i++)
    if (tumblerptr->mantissa[i] != 0)
      return (FALSE);
  return (TRUE);
}
```

This predicate exists, but its call sites reveal it is **never applied to node ISAs**:

| Call site | What it checks |
|-----------|---------------|
| `orglinks.c:184` | `ccptr->cwid.dsas[V]` — V-dimension **width** of content crum |
| `orglinks.c:248` | `crumptr->cwid.dsas[V]` — same, in `istextcrum()` |
| `orglinks.c:284` | `crumptr->cwid.dsas[V]` — same, in `walkorglonvpm()` |
| `ndcuts.c:389` | `lockis1story(ptr->cwid.dsas, widsize(enftype))` — **POOM width** |
| `ndcuts.c:410` | `is1story(&localcut)` — POOM **cut** offset |
| `ndcuts.c:471` | Same POOM width assertion |
| `ndcuts.c:492` | Same POOM cut check |
| `makeroom.c:21` | Commented out |

**`backend/ndcuts.c:389-394`** — the only `gerror` enforcement via `is1story`:

```c
if (!lockis1story (ptr->cwid.dsas, (unsigned)widsize(enftype)))
#ifndef DISTRIBUTION
    gerror ("Not one story in POOM wid\n");
```

This asserts single-story for **POOM widths** — enfilade structure constraints — not for node addresses.

The `is1story` logic in content crums encodes a semantic distinction between text crums (single-story V-width → pure text) and link crums (multi-story V-width → link displacement). This is address-space partitioning within the virtual address dimension, not node address structure.

---

### 6. Address Hierarchy by `depth`

The `depth` formula (`supertype == subtype ? 1 : 2`) at `granf2.c:209` determines how many components are added per hierarchy level:

| `makehint(above, below, ...)` | depth | Components added |
|-------------------------------|-------|-----------------|
| `NODE, NODE` | 1 | 1 — nodes are flat siblings under account |
| `ACCOUNT, DOCUMENT` | 2 | 2 — docs are `account.0.N` |
| `DOCUMENT, DOCUMENT` | 1 | 1 — versions are `doc.N` |
| `DOCUMENT, ATOM` | — | `findisatoinsertmolecule`, separate logic |

Document `1.1.0.1.0.1` (from `golden/iaddress_allocation/consecutive_inserts_monotonic.json`) shows the two-component jump from account `1.1.0.1`: `.0.1` is the first document (depth=2, zero-then-one).

Node `1.1.0.1.1` shows the one-component jump (depth=1, just `.1`).

---

### Summary

1. **Node addresses are multi-component tumblers**, not single-component identifiers. The address `1.1.0.1.1` has 5 components.

2. **Allocation adds exactly one new component** (depth=1 for `NODE→NODE`), making each node's absolute address one digit longer than its parent account. The discriminating suffix is single-component, but the full address is not.

3. **No code path enforces single-component node addresses**. There are no assertions, guards, or `is1story()` calls anywhere in the ISA allocation or lookup paths.

4. **No code path assumes node addresses are single-component**. All node address operations (`tumblercmp`, `tumblereq`, `retrievecrums`, etc.) use generic tumbler arithmetic that handles arbitrary component counts.

5. **`is1story()` is exclusively a content-crum predicate** — it distinguishes text crums from link crums by their V-dimension width, and asserts structural invariants on POOM widths. It has no role in node address allocation or validation.
