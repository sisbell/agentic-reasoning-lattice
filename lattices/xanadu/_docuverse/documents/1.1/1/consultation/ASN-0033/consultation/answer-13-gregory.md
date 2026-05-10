## Question 13 [gregory]

> Does the node's tumbler prefix propagate into I-address space — i.e., does every I-address allocated under node `1` begin with `1.`, making the node recoverable from any I-address by inspecting the first field?

## KB Synthesis

## Yes — With Caveats on What the KB Directly States

The KB supports a **yes** answer through inference from the allocation mechanism, though it does not state this as an explicit principle.

### The Structural Argument

The allocation mechanism always creates new addresses as **children** of their parent, and "child" means **prefix containment** [SS-TUMBLER-CONTAINMENT]:

> "Containment of address A under prefix B is checked by truncating A to the length of B and comparing for equality."

Every allocation — documents, link orgls, text atoms — is bounded to a parent address:

- **Documents** under account `1.1.0.1` → allocates `1.1.0.1.0.1`, `1.1.0.1.0.2`, ... [SS-ADDRESS-ALLOC]
- **Link orgls** under document `1.1.0.1.0.1` → allocated at `1.1.0.1.0.1.0.2.1`, `1.1.0.1.0.1.0.2.2`, ... [SS-ADDRESS-SPACE/Finding 0065]
- **Text content** under document `1.1.0.1.0.1` → allocated at `1.1.0.1.0.1.3.0.1.1`, `1.1.0.1.0.1.3.0.1.2`, ... [SS-ADDRESS-SPACE/Finding 0077]

Since the allocator enforces `allocated ⊆ children(parent)` recursively all the way up to the node, every I-address in node `1`'s subtree begins with `1.`. The node is recoverable from any I-address by inspecting the first digit.

### Concrete Confirmation

Finding 0077 shows both document addresses and content I-addresses sharing the same node prefix:

```
1.1.0.1           (account under node 1)
├── 1.1.0.1.0.1   (document)
└── 1.1.0.1.0.1.3.0.1.1   (text I-address for that document)
```

Finding 0065 shows the same for link orgls: document `1.1.0.1.0.1` → link at `1.1.0.1.0.1.0.2.1`.

### The Two-Sort Distinction Does Not Contradict This

Finding 0009 notes permascroll I-addresses like `2.1.0.5.0.123` vs. link ISAs like `1.1.0.1.0.2`. This is not a special "permascroll node" — it reflects that the permascroll content was allocated under a document in the `2.x` account namespace. The `2` prefix comes from the owning account being under node 2, not from a separate permascroll region.

### What the KB Does Not State

The KB never explicitly asserts "the node is recoverable from any I-address by inspecting the first field" as a design principle. This is derivable from [SS-TUMBLER-CONTAINMENT] + [SS-ADDRESS-ALLOC], but the `findisatoinsertmolecule` / `findisatoinsertnonmolecule` code is documented as operating by prefix-bounded search — the node invariant is structural, not explicitly named.

**Summary:** Yes — the tumbler address hierarchy is strictly self-similar. Allocation is always prefix-contained, so the node prefix propagates into all descendant I-addresses. The node (and full containing path) is recoverable from any I-address by prefix truncation using the containment predicate in [SS-TUMBLER-CONTAINMENT].

---

## Code Exploration

Now I have everything needed for a complete, citation-backed answer.

---

## Does the node's tumbler prefix propagate into I-address space?

**Yes, unambiguously.** Every I-address allocated under node `1` begins with `1.`, and the node is recoverable from any I-address by inspecting `isa->mantissa[0]` (or `tumblertruncate(isa, tumblerlength(node_isa), &node)` for a multi-digit node address).

---

### 1. Tumbler encoding: printed fields map directly to mantissa slots

`common.h:53–64` defines the tumbler as a 16-slot `tdigit mantissa[NPLACES]` array. `put.c:26–46` (`puttumbler`) confirms the wire format:

```c
// put.c:41–45
for(i = 0; i <= place; ++i) {
    putnum(outfile, tumblerptr->mantissa[i]);
    if (i < place)
        putc('.', outfile);
}
```

Each dot-separated field in printed notation is exactly one mantissa slot. There are no hidden separators. The address `1.1.0.1.0.1` is stored as `mantissa = [1, 1, 0, 1, 0, 1, 0, ...]`.

---

### 2. `tumblerincrement` always creates a proper child

`tumble.c:599–623`:

```c
int tumblerincrement(tumbler *aptr, INT rightshift, INT bint, tumbler *cptr)
{
    // copies aptr to cptr first
    for (idx = NPLACES; aptr->mantissa[--idx] == 0 && idx > 0;);
    cptr->mantissa[idx + rightshift] += bint;   // [line 621]
    tumblerjustify(cptr);                        // [line 622]
}
```

For a non-zero `aptr`: finds the index `idx` of the last non-zero mantissa slot, then adds `bint` at `idx + rightshift`. The original content of `aptr` is untouched at positions 0..idx; the increment lands at `idx + rightshift`. **`aptr` is always a strict prefix of the result.**

Example: `tumblerincrement(1.1.0.1, rightshift=2, bint=1)` → `idx=3`, writes `1` at position `5` → `1.1.0.1.0.1`. ✓

---

### 3. All non-molecule allocation preserves the parent prefix

`granf2.c:203–242` (`findisatoinsertnonmolecule`), for creating nodes, accounts, and documents:

**When nothing yet exists under the hint** (lines 235–237):
```c
if (iszerotumbler(&lowerbound) || !lowerbound_under_hint) {
    tumblerincrement(&hintptr->hintisa, depth, 1, isaptr);
```
New ISA = `hintisa` with `depth` extra levels appended. Direct child, inherits entire prefix.

**When prior content exists** (lines 239–240):
```c
tumblertruncate(&lowerbound, hintlength + depth, isaptr);
tumblerincrement(isaptr, tumblerlength(isaptr)==hintlength ? depth : 0, 1, isaptr);
```
`lowerbound` has already been verified to begin with `hintisa`; truncating and incrementing preserves the prefix.

**Explicit cross-account guard** (lines 228–233):
```c
lowerbound_under_hint = FALSE;
if (!iszerotumbler(&lowerbound)) {
    tumblertruncate(&lowerbound, hintlength, &truncated);
    lowerbound_under_hint = tumblereq(&truncated, &hintptr->hintisa);
}
```
If the best lower-bound candidate belongs to a *different* account/node (e.g., searching under `1.1.0.2` finds `1.1.0.1.0.1`), it is rejected and treated as "nothing found." This prevents cross-contamination. The comment names it **BUG FIX #2** [granf2.c:224–226].

---

### 4. Molecule (text and link atom) allocation also preserves the prefix

`granf2.c:158–181` (`findisatoinsertmolecule`). In the case where the document's GRANORGL is the only existing lower bound (equal lengths):
```c
// lines 165–167
tumblerincrement(&lowerbound, 2, hintptr->atomtype, isaptr);
tumblerincrement(isaptr, 1, 1, isaptr);
```
Both steps append to `lowerbound` (which equals `hintisa` = the document ISA), so the result inherits the full document prefix.

In the case where a prior text ISA exists:
```c
// line 169
tumblerincrement(&lowerbound, 0, 1, isaptr);
```
Increments the last digit of `lowerbound`, which already started with the document prefix. Result: same prefix + 1.

---

### 5. The call chain: root node → account → document → atom

Every allocation call traces back through these `makehint` invocations:

| Call site | Hint construction | `depth` |
|-----------|-------------------|---------|
| `do1.c:251` `docreatenode_or_account` | `makehint(NODE, NODE, 0, parentNodeIsa, &hint)` | 1 |
| `do1.c:239` `docreatenewdocument` | `makehint(ACCOUNT, DOCUMENT, 0, &taskptr->account, &hint)` | 2 |
| `do1.c:271` `docreatenewversion` (same owner) | `makehint(DOCUMENT, DOCUMENT, 0, existingDoc, &hint)` | 1 |
| `do1.c:275` `docreatenewversion` (cross-owner) | `makehint(ACCOUNT, DOCUMENT, 0, wheretoputit, &hint)` | 2 |
| `do1.c:117` `doinsert` | `makehint(DOCUMENT, ATOM, TEXTATOM, docisaptr, &hint)` | — (molecule) |
| `do1.c:207` `docreatelink` | `makehint(DOCUMENT, ATOM, LINKATOM, docisaptr, &hint)` | — (molecule) |

`depth` is computed as `granf2.c:209`: `depth = hintptr->supertype == hintptr->subtype ? 1 : 2`.

At each step the new address extends the parent's address, never breaks away from it.

---

### 6. Empirical confirmation from golden tests

`golden/versions/version_address_allocation.json` records actual backend output with `DEFAULT_ACCOUNT = Address(1, 1, 0, 1)` (`febe/generate_golden.py:17`):

```
Account (pre-set):        1.1.0.1        ← mantissa[0]=1
Document 1:               1.1.0.1.0.1   ← mantissa[0]=1
Document 2:               1.1.0.1.0.2   ← mantissa[0]=1
Version of doc1:          1.1.0.1.0.1.1 ← mantissa[0]=1
Second version of doc1:   1.1.0.1.0.1.2 ← mantissa[0]=1
Version of version:       1.1.0.1.0.1.1.1 ← mantissa[0]=1
```

Every address at every depth begins with `1.`. The first mantissa field equals `1` throughout.

---

### 7. Recovering the node from any I-address

Because `tumblerincrement` always appends beyond the parent, the parent ISA is recoverable as a prefix:

```c
// Recover node from any ISA:
tumblertruncate(isa, tumblerlength(&node_isa), &recovered_node);
// recovered_node == node_isa by construction
```

For the specific case of root node `1` (a single-field tumbler), this reduces to reading `isa->mantissa[0]` — no truncation needed. The account-ownership check in `tumbleraccounteq` (`tumble.c:38–70`) relies on exactly this property: it scans the mantissa comparing field-by-field until the account address's trailing zeros signal its end, confirming prefix containment.

---

### Summary

**Yes.** The node prefix propagates into I-address space by design, not accident. `tumblerincrement` physically encodes parent-child by appending slots to the existing mantissa. `findisatoinsertnonmolecule` enforces this with an explicit "is lowerbound under hint?" guard. The entire allocation call chain from `doinsert` / `docreatenewdocument` / `docreatelink` preserves the chain back to the originating node. The first mantissa field of any I-address identifies its root node, and `tumblertruncate(isa, nodelen)` recovers the full node ISA.
