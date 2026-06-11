## Question 1 [evidence]

> Does udanax-green's account-creation path ever emit, or its retrieval path ever accept, addresses whose user field has more than one component, and more broadly do its allocators ever produce addresses outside the shape node-lineage-under-1, single-component user field, `#E = 2`?

## KB Synthesis

## Account-Creation Path and User Field Structure

The KB does not contain a finding that directly tests or observes multi-component user fields in allocated addresses, but the available evidence points to a clear answer.

### What the allocation arithmetic produces

From [SS-ADDRESS-ALLOC] (Finding 0021), `findisatoinsertnonmolecule` generates account addresses by:

1. Computing upper bound: `tumblerincrement(node_hint, depth-1=1, 1)` — e.g., `1.2` for parent node `1.1`
2. Finding highest existing ISA below that bound via `findpreviousisagr`
3. Truncating the found ISA to its current significant length and incrementing at `rightshift=0` (the last significant digit)

All documented examples show single-component user fields: `1.1.0.1`, `1.1.0.2`, `1.1.0.3`. The allocation is purely positional arithmetic — it has no awareness of the `.0.` field-separator convention layered on top. No KB entry documents a test with 10+ accounts under one node. However, from [SS-TUMBLER] (Finding 0031), each mantissa position is a base-10 digit (0–9), so `tumblerincrement` on the last digit of `1.1.0.9` (mantissa `[1,1,0,9]`) would carry into the adjacent position, producing `[1,1,1,0]` — tumbler `1.1.1.0`. This address has no `.0.` field separator at the conventional account boundary; it would be interpreted as node lineage `1.1.1` followed by a trailing zero, not as an account under node `1.1`.

**The KB does not document this boundary case.** All findings operate in the low-account-count regime. Whether the implementation handles this gracefully (e.g., via extended-width encoding) or silently misbehaves is not answerable from the KB.

### Retrieval path acceptance

From [PRE-SPECSET] (Finding 0001), the retrieval path (`specset2sporglset`) validates only that the referenced document exists — it does **not** enforce element-level tumbler structure. Non-standard address shapes are accepted without error. A specset containing an address with a multi-component user field would pass validation if the document ISA prefix resolved.

### Element field `#E = 2` (link orgls)

From [SS-ADDRESS-ALLOC] (Finding 0065), link orgl I-addresses are always allocated within `docISA.2.N` — element field `2` is hardcoded in both the allocation bound (`tumblerincrement(&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound)`) and in `setlinkvsas()` [SS-DUAL-ENFILADE] (Finding 0038). The allocator never produces link orgls at element field ≠ 2. Text content goes to element field `3` (element_number 3 in the `makehint(DOCUMENT, ATOM, TEXTATOM, ...)` path [PRE-INSERT] Finding 0036).

There is no documented path by which the allocator varies the element field value for a given entity type. `#E = 2` (link) and `#E = 3` (text) are fixed constants, not dynamically allocated values.

### Summary

| Claim | KB verdict |
|-------|-----------|
| Account-creation emits multi-component user fields | Not documented; arithmetic could carry-produce `1.1.1.0`-shape addresses after 9 accounts, but no finding covers this case |
| Retrieval accepts non-standard user-field addresses | **Yes** — [PRE-SPECSET] shows only document-existence is checked |
| Link allocator ever produces element field ≠ 2 | **No** — [SS-ADDRESS-ALLOC] (Finding 0065) and `setlinkvsas()` hardcode `2` |
| Text allocator ever produces element field ≠ 3 | **No** — `makehint(DOCUMENT, ATOM, TEXTATOM, ...)` hardcodes `3` |

The KB is silent on the overflow-past-9-accounts scenario, so whether the allocator ever produces addresses outside `node-lineage-under-1, single-component user field` is not answerable from current KB entries alone.

---

## Code Exploration

I now have all the evidence I need. Let me compile the complete answer.

---

## Answer

### Tumbler Structure and Address Representation

**`common.h:53-65`** defines the tumbler:
```c
#define NPLACES 16
typedef struct structtumbler {
    humber xvartumbler;
    char varandnotfixed;
    char sign BIT;
    short exp;
    tdigit mantissa[NPLACES];   // flat 16-element array
} tumbler;
```

The mantissa is a flat array; a dot-separated address like `1.1.0.0.1` maps directly to `mantissa = {1, 1, 0, 0, 1, 0, …}`. The `exp` field shifts the decimal point left (negative = sub-positions). `puttumbler` **[put.c:26-46]** serialises by emitting every position up to the last non-zero one, including internal zeros:

```c
place = NPLACES;
do {--place;} while (place > 0 && tumblerptr->mantissa[place] == 0);
for (i = 0; i <= place; ++i) {
    putnum(outfile, tumblerptr->mantissa[i]);
    if (i < place) putc('.', outfile);
}
```

So an address like `1.1.0.0.1` (account `1.1`, first document) is a legitimate emission: the two zero digits at positions 2 and 3 are a structural artifact of the two-level increment used for ACCOUNT→DOCUMENT creation, not corruption.

---

### Type Hierarchy Constants

**`xanadu.h:140-146`**:
```
NODE = 1, ACCOUNT = 2, DOCUMENT = 3, ATOM = 4
TEXTATOM = 1, LINKATOM = 2
```

---

### The `xaccount` Path — Account Is Client-Supplied, Not Allocated

**`fns.c:364-373`** dispatches to **`get1.c:190-204`** (`getxaccount`):

```c
bool getxaccount(typetask *taskptr, typeisa *accountptr)
{
    gettumbler(taskptr, accountptr)
    && validaccount(taskptr, accountptr);
    taskptr->account = *accountptr;
    return(TRUE);
}
```

`validaccount` has **two independent implementations** — both are stubs:

- **`get2.c:157-160`** (non-FE build): `return(TRUE);`
- **`get2fe.c:338-341`** (FE build): `return(TRUE);`

The account is read from the wire by **`get2fe.c:69-88`** (`gettumbler`):

```c
for (i = 0; gettdigit(taskptr, &value); i++) {
    if (i > NPLACES) {
        error(taskptr, "gettumbler overflow\n");
        return(FALSE);
    }
    tumblerptr->mantissa[i] = value;
}
```

This reads up to NPLACES=16 dot-separated digits without any shape constraint. A client sending `1.1.2` (three-component address) is accepted identically to `1.2` (two-component). The `xaccount` path **never emits an account address; it only ingests whatever the client transmits, with no validation beyond NPLACES overflow.**

---

### `docreatenode_or_account` — The Actual Allocator for Accounts/Nodes

**`fns.c:375-386`** → **`do1.c:243-258`**:

```c
bool docreatenode_or_account(typetask *taskptr, typeisa *isaptr)
{
    typeisa isa;
    typehint hint;
    tumblercopy(isaptr, &isa);            // seed from client
    makehint(NODE, NODE, 0, &isa, &hint);
    result = createorglingranf(taskptr, granf, &hint, &isa);
    if (result) { tumblercopy(&isa, isaptr); }
    return result;
}
```

The key branching is in **`granf2.c:209`**:

```c
depth = hintptr->supertype == hintptr->subtype ? 1 : 2;
```

Since `NODE == NODE` (both = 1), `depth = 1`. The first-ever allocation under a zero-or-absent tree takes the path at **`granf2.c:235-237`**:

```c
if (iszerotumbler(&lowerbound) || !lowerbound_under_hint) {
    tumblerincrement(&hintptr->hintisa, depth, 1, isaptr);
```

`tumblerincrement(aptr, rightshift, bint, cptr)` **[tumble.c:599-623]**:

```c
for (idx = NPLACES; aptr->mantissa[--idx] == 0 && idx > 0;);
cptr->mantissa[idx + rightshift] += bint;
```

For seed `1` (mantissa = `{1,0,…}`, idx=0, rightshift=depth=1):
→ `mantissa[0+1] = 1` → `1.1`

For the Nth subsequent allocation at **`granf2.c:239-240`**:
```c
tumblertruncate(&lowerbound, hintlength + depth, isaptr);
tumblerincrement(isaptr, tumblerlength(isaptr)==hintlength ? depth : 0, 1, isaptr);
```

With hintlength=1 and each previous address having tumblerlength=2 (≠ hintlength), the rightshift is 0, so `1.1` → `1.2` → `1.3`, etc. **The allocator, given seed `1`, exclusively produces `1.N` addresses: two-component, single-user-field, depth-2. This is the canonical shape.**

However: if the client passes seed `1.1` instead of `1`, the allocator produces `1.1.1`, `1.1.2`, …—depth-3 addresses with a two-component user field. The code contains no guard against this. The allocator is purely seed-driven.

---

### Document Allocation — Internal Zeros Are Structural

**`do1.c:234-241`** (`docreatenewdocument`):

```c
makehint(ACCOUNT, DOCUMENT, 0, &taskptr->account, &hint);
return (createorglingranf(taskptr, granf, &hint, isaptr));
```

`ACCOUNT (2) ≠ DOCUMENT (3)`, so `depth = 2` **[granf2.c:209]**. For account `1.1` (idx=1, rightshift=2):

```c
mantissa[1 + 2] = mantissa[3] += 1
```

Result: `{1, 1, 0, 0, 1, 0, …}` → wire output `1.1.0.0.1`.

The two zero slots at positions 2 and 3 are **not** extra user-field components — they are the depth-2 gap mandated by the ACCOUNT→DOCUMENT type distance. `tumbleraccounteq` **[tumble.c:47-68]** explicitly models this: it treats zeros in the account tumbler as scope boundaries and succeeds when two consecutive zeros have been seen in the account pattern:

```c
if (bptr->mantissa[i] == 0) {
    if (++j_b == 2) {
        return(TRUE);  /* account terminated */
    }
```

So `1.1.0.0.1` is legitimately "under account `1.1`" by the system's own equivalence definition.

The `#E = 2` shape (two non-zero, non-gap components before the structural zeros) is therefore respected in the document addresses the allocator produces, **as long as the client-supplied account has #E = 2**.

---

### Retrieval Path — No Shape Validation

**`do2.c:110-113`** (`acceptablevsa`):

```c
bool acceptablevsa(tumbler *vsaptr, typeorgl orglptr)
{
    return (TRUE);
}
```

This function is the only address-shape gate in the retrieval path (`docopy` at `do1.c:55`), and it is an unconditional stub. The retrieval path **accepts any address of any shape without checking depth, user-field width, or any structural property.**

Similarly, `isthisusersdocument` **[be.c:171-176]** uses `tumbleraccounteq` which, as shown above, only checks that the address falls under the account prefix — it does not enforce that the account itself has a single-component user field.

---

### Summary

| Question | Answer | Evidence |
|----------|--------|----------|
| Does `xaccount` emit multi-component user-field accounts? | It emits nothing — it reads any tumbler the client sends, validated by a stub that always returns TRUE. | `get2.c:157`, `get2fe.c:338`, `get2fe.c:69-88` |
| Does `docreatenode_or_account` produce multi-component user-field accounts? | **Not autonomously.** Given a seed of `1`, it produces only `1.1`, `1.2`, `1.3`, …, which are strictly single-component user fields at depth 2. | `do1.c:243-258`, `granf2.c:209`, `tumble.c:599-623` |
| Can the allocator be driven to produce deeper addresses? | **Yes.** The allocator is seed-driven with depth always relative to the seed. A client passing seed `1.1` as the node hint gets sub-nodes `1.1.1`, `1.1.2`, …—a two-component user field. Nothing in the code prevents this. | `do1.c:250`, `granf2.c:209,237` |
| Does the retrieval path enforce address shape? | **No.** `acceptablevsa` is a permanent stub returning TRUE. The wire parser accepts any tumbler up to NPLACES=16 digits. | `do2.c:110-113`, `get2fe.c:79-85` |
| Do document addresses contain the shape `account.0.0.N`? | **Yes** — always, because ACCOUNT→DOCUMENT depth=2 puts the counter two positions right of the last account digit. The zeros are structural separators. | `granf2.c:209,237`, `tumble.c:599-623`, `put.c:26-46` |
| Do the allocators ever autonomously produce addresses outside node-lineage-under-1, single-component user field, #E=2? | **No** — when operating on canonical inputs. The allocator arithmetic is deterministic: depth=1 for NODE→NODE, depth=2 for ACCOUNT→DOCUMENT. Starting from seed `1`, all generated accounts are `1.N` (depth 2, one user component). The constraint is not enforced — it is merely a consequence of the reference client always sending `1` as the node seed. |

The invariant "single-component user field at depth 2" is **not codified anywhere in the C source**. It is an emergent property of the reference client sending a depth-1 node seed. Any client that sends a deeper seed breaks it, and neither the account intake (`validaccount`), the retrieval gate (`acceptablevsa`), nor any guard in `findisatoinsertnonmolecule` would stop it.
