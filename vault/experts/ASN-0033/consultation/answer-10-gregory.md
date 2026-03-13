## Question 10 [gregory]

> What tumbler structure identifies a node — is a node always a single non-zero digit (e.g., `1`), or can node addresses be multi-digit (e.g., `1.3`), and how many tumbler fields does the node occupy before the first `.0.` separator?

## KB Synthesis

## Node Tumbler Structure

Nodes **can be multi-digit** — the node address is not constrained to a single digit. It grows by appending digits **without** any `.0.` separator as you descend the node hierarchy.

### How node nesting works

From [SS-ADDRESS-SPACE] Finding 0021, the `makehint` table:

| supertype | subtype | depth | Meaning |
|-----------|---------|-------|---------|
| NODE | NODE | 1 | Node under node |
| ACCOUNT | DOCUMENT | 2 | Document under account |

`depth = (supertype == subtype) ? 1 : 2`

Depth=1 means no `.0.` boundary is crossed. Each nested node level appends one more digit sequentially:

- Top-level: `1`, `2`, `3` ...
- Under node `1`: `1.1`, `1.2`, `1.3` ...
- Under node `1.1`: `1.1.1`, `1.1.2` ...
- Under node `1.1.1`: `1.1.1.1` ...

Examples from Finding 0021:
> "Nodes under a node: `1.1.0.1.1`, `1.1.0.1.2` (no `.0.` boundary)"

### Field count before the first `.0.`

The node occupies **all leading digits up to (but not including) the first `.0.` separator**. From the docuverse convention ([SS-TUMBLER] Finding 0001):

> The `.0.` field dividers give the pattern `Node.0.User.0.Doc.0.Element`

So in `1.1.0.2.0.1`:
- Node: `1.1` (2 digits)
- Account: `2` (1 digit after first `.0.`)
- Document: `1` (1 digit after second `.0.`)

In `1.1.0.1.0.1.0.2.1` from [SS-ADDRESS-SPACE] Finding 0065:
- Node: `1.1` (2 digits)
- Account: `1`
- Document: `1`
- Element (link 2, number 1): `2.1`

The node field length is unbounded — it equals the depth of the node in the node-under-node hierarchy, with no upper limit other than the tumbler's 16-mantissa-digit capacity ([SS-TUMBLER] Finding 0031).

### Containment check

[SS-TUMBLER-CONTAINMENT] Finding 0021 confirms the prefix-match semantics apply: `tumblertruncate(A, length(B))` then compare. Whether `1.1.0.1.1` is under `1.1.0.1` is determined by truncating `1.1.0.1.1` to length 5 and comparing with `1.1.0.1` — yielding `1.1.0.1.1` ≠ `1.1.0.1`, so **no** (node siblings are not contained in each other). But `1.1.0.1.0.1` truncated to length 5 = `1.1.0.1.0` ≠ `1.1.0.1` — also no. Only addresses that have `1.1.0.1` as an exact prefix (same digits at the same positions) satisfy containment.

---

## Code Exploration

Now I have all the information needed. Let me compile the complete answer.

---

## Answer: Tumbler Structure of a Node Address

### 1. The `tumbler` Struct

Defined in `backend/common.h:59-65`:
```c
typedef struct structtumbler {
    humber xvartumbler;
    char varandnotfixed;
    char sign  BIT;  /* 1 if negative, otherwise 0 */
    short exp;
    tdigit mantissa[NPLACES];
} tumbler;
```

Where `NPLACES = 16` [`common.h:53`] and `tdigit = UINT = uint32_t` [`common.h:57`, `defs.h:12`]. Each mantissa slot is one "digit" (story) in the tumbler. A value of `0` in a mantissa slot is the `.0.` separator in string notation.

---

### 2. Is a Node Always a Single Non-Zero Digit?

**Yes — each node creation appends exactly ONE mantissa digit to the parent address.**

From `backend/do1.c:251` and `granf2.c:209-241`:

```c
// do1.c:251
makehint(NODE, NODE, 0, &isa, &hint);
result = createorglingranf(taskptr, granf, &hint, &isa);
```

```c
// granf2.c:209
depth = hintptr->supertype == hintptr->subtype ? 1 : 2;
```

When `supertype == NODE` and `subtype == NODE`, `depth = 1`. The first allocation path is:

```c
// granf2.c:237
tumblerincrement(&hintptr->hintisa, depth, 1, isaptr);
```

`tumblerincrement(aptr, rightshift, bint, cptr)` at `tumble.c:599-623` places `bint` at the slot `lastNonZero(aptr) + rightshift`. With `depth=1` and `rightshift=1`, it appends `1` at exactly **one position** beyond the last non-zero digit of the parent address.

For subsequent nodes (when something already exists), `granf2.c:239-240`:
```c
tumblertruncate(&lowerbound, hintlength + depth, isaptr);
tumblerincrement(isaptr, tumblerlength(isaptr)==hintlength?depth:0, 1, isaptr);
```

This increments the last existing slot by 1 — still one digit.

**Golden test evidence** (`golden/accounts/create_multiple_nodes.json`):
```
Account: 1.1.0.1
Node 1:  1.1.0.1.1   ← parent + digit 1
Node 2:  1.1.0.1.2   ← parent + digit 2 (same slot incremented)
Node 3:  1.1.0.1.3   ← parent + digit 3
```

Each node is exactly **one additional mantissa slot**. The digit is always a single `uint32_t` value ≥ 1. It can be any positive integer (e.g., `3`), but it always occupies **one slot** — never a multi-digit sequence like `.1.3`.

Contrast with document allocation, where `depth = 2` (ACCOUNT → DOCUMENT, different types), which inserts a `.0.` separator then the document number — two additional slots.

---

### 3. How Many Fields Before the First `.0.` Separator?

**Two fields.** In every observed address in this system, mantissa positions 0 and 1 are both non-zero (both `= 1`), and position 2 is the first zero.

For example:
| Address | mantissa |
|---|---|
| `1.1.0.1` (account) | `[1, 1, 0, 1, 0, 0, ...]` |
| `1.1.0.1.1` (node) | `[1, 1, 0, 1, 1, 0, ...]` |
| `1.1.0.1.0.1` (document) | `[1, 1, 0, 1, 0, 1, ...]` |
| `1.1.0.1.1.0.1` (doc under node) | `[1, 1, 0, 1, 1, 0, 1, ...]` |

The `1.1` prefix (two mantissa fields) before the first `.0.` is the **network/host node identifier** — the Xanadu global node address identifying this server in the wider network. All addresses within this backend share the same `1.1` prefix.

This two-field prefix is confirmed by `tumbleraccounteq` at `tumble.c:54-68`, which scans past zeros in the account address. For account `1.1.0.1` (mantissa = `[1,1,0,1,0,0,...]`), the first zero at position 2 is encountered, counted once; the terminating second zero is found at the trailing positions. The scan logic confirms the first separator `.0.` is at slot index 2.

Also confirmed by `Address.split()` in `febe/client.py:201-205`:
```python
def split(self):
    """For a global address, return the docid and local components."""
    delim = len(self.digits) - 1
    while self.digits[delim] != 0: delim = delim - 1
    return Address(self.digits[:delim]), Address(self.digits[delim+1:])
```

Splitting `1.1.0.1.0.1` at its **last** `.0.` yields `docid = 1.1.0.1`, `local = 1`. The first `.0.` (at position 2) separates the host-node prefix `1.1` from the rest.

---

### Summary

| Question | Answer | Source |
|---|---|---|
| Node mantissa slots added per level | **1** — single digit appended | `granf2.c:209, 237` — `depth=1` for NODE→NODE |
| Can a node be multi-digit (e.g. `.1.3`)? | **No** — always exactly one slot | `tumblerincrement` with `rightshift=1` |
| Fields before first `.0.` | **2** (the host/network node `1.1`) | `common.h:53`, `tumble.c:54-68`, golden tests |
| `.0.` role | Separates hierarchy levels — inserted only when crossing type boundaries (depth=2) | `granf2.c:209` |

The two fields before `.0.` (`1.1` in this implementation) are the **Xanadu network node address** — a two-level global identifier for this backend instance. Everything within the system (accounts, documents, nodes, content) is addressed within that prefix. Nodes in the `NODE` type sense each occupy exactly **one additional mantissa digit** beyond their parent, with no `.0.` separator — that separator only appears between the account/node level and the document level (`depth=2`, ACCOUNT→DOCUMENT).
