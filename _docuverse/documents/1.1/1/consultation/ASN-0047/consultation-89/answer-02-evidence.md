## Question 2 [evidence]

> Does udanax-green maintain a distinct per-document version allocator (analogous to the content and link sub-allocators) whose frontier is tracked across docreatenewversion emissions, or is version allocation dispatched through some other mechanism (e.g., a single global version frontier, or directly via inc on the prior version address)?

## KB Synthesis

Version allocation in udanax-green uses **stateless query-and-increment on the granfilade tree** — there is no distinct per-document version allocator, no single global version frontier, and no direct increment on the prior version address.

## Mechanism

`docreatenewversion` calls `findisatoinsertnonmolecule` via `createorglingranf` with a DOCUMENT→DOCUMENT hint at depth=1. Each allocation executes the same algorithm regardless of how many prior versions exist [SS-ADDRESS-ALLOC, Finding 0068]:

1. Compute upper bound: `tumblerincrement(source_doc, depth-1=0, 1)` — the next sibling of the source document (e.g., `1.1.0.1.0.2` for source `1.1.0.1.0.1`)
2. Call `findpreviousisagr` to traverse the granfilade tree and find the highest existing address strictly below that bound
3. Apply containment check: verify the found address is actually under the source document prefix
4. If no child exists: allocate `source_doc.1` (first version)
5. If a child exists: truncate to that child's length, increment by 1 (e.g., `1.1.0.1.0.1.1` → `1.1.0.1.0.1.2`)

## No Stored Frontier

[Finding 0061] and [Finding 0077] explicitly rule out a cached counter: "allocation is purely derived from current tree state — there is no cached 'next available' pointer." The granfilade itself is the frontier. Formally: `next_version_addr(granf, doc) = max_child(granf, doc) + 1` [SS-ADDRESS-SPACE, Finding 0077].

This also means deleted version addresses **persist in the granfilade** and continue to influence subsequent allocation — a deleted version at `.1` causes the next allocation to land at `.2`, never reusing `.1` [INV-MONOTONIC, Finding 0068].

## Ownership Branching

The hint construction is ownership-sensitive [ST-VERSION-OWNERSHIP, Finding 0068]:
- **User owns source doc**: `makehint(DOCUMENT, DOCUMENT, 0, isaptr, &hint)` → depth=1, version lands under the source document
- **User does not own source doc**: `makehint(ACCOUNT, DOCUMENT, 0, wheretoputit, &hint)` → depth=2, version lands under the creating user's account (same allocation path, different parent)

The same `findisatoinsertnonmolecule` function handles both branches; ownership only changes what tumbler prefix is used as the allocation parent.

## Key Code References

`do1.c:272-280` — ownership-sensitive hint creation in `docreatenewversion`  
`granf2.c:203-242` — `findisatoinsertnonmolecule`, the shared query-and-increment allocator  
`granf2.c:255-278` — `findpreviousisagr`, tree traversal finding the maximum existing child

---

## Code Exploration

Now I have all the evidence I need. Let me compile the complete answer.

---

## Answer: Version Allocation in udanax-green

**Short answer:** There is no per-document version allocator with a persistent frontier. Version address allocation is dispatched through the same `findisatoinsertnonmolecule` routine that handles all granfilade address allocation. The "frontier" is computed on-demand by querying the granfilade for what already exists in the document's child namespace.

---

### The Call Chain

`docreatenewversion` [do1.c:260] →  
`createorglingranf` [granf1.c:50] →  
`createorglgr` [granf2.c:111] →  
`findisatoinsertgr` [granf2.c:130] →  
`findisatoinsertnonmolecule` [granf2.c:203]

---

### Two Cases in `docreatenewversion`

The hint construction [do1.c:270–276] has a fork:

```c
if (tumbleraccounteq(isaptr, wheretoputit) && isthisusersdocument(isaptr)) {
    makehint(DOCUMENT, DOCUMENT, 0, isaptr, &hint);   // Case 1
} else {
    makehint(ACCOUNT, DOCUMENT, 0, wheretoputit, &hint); // Case 2
}
```

- **Case 1** (`DOCUMENT, DOCUMENT`): `hintisa` = the source document's own ISA (e.g., `1.1.0.1.0.1`). Used when versioning your own document within the same account.
- **Case 2** (`ACCOUNT, DOCUMENT`): `hintisa` = target account ISA. Identical to `docreatenewdocument`; the version gets a sibling address to existing documents in the target account, with no genealogical relationship to the source.

---

### How `findisatoinsertnonmolecule` Allocates the Version Address

The key is the `depth` field [granf2.c:209]:

```c
depth = hintptr->supertype == hintptr->subtype ? 1 : 2;
```

For **Case 1** (`DOCUMENT == DOCUMENT`): `depth = 1`.  
For **Case 2** (`ACCOUNT != DOCUMENT`): `depth = 2` (same as creating a new document).

For Case 1 the allocation proceeds [granf2.c:211–241]:

```c
// upperbound = one past the source document's own address (its next sibling)
tumblerincrement(&hintptr->hintisa, depth - 1, 1, &upperbound);
//  e.g. tumblerincrement(1.1.0.1.0.1, 0, 1) → 1.1.0.1.0.2

// Query the granfilade: what is the largest ISA strictly below upperbound?
findpreviousisagr((typecorecrum*)fullcrumptr, &upperbound, &lowerbound);

// Is that lowerbound actually under the source document?
tumblertruncate(&lowerbound, hintlength, &truncated);
lowerbound_under_hint = tumblereq(&truncated, &hintptr->hintisa);

if (iszerotumbler(&lowerbound) || !lowerbound_under_hint) {
    // Nothing allocated yet: first version = docisa.1
    tumblerincrement(&hintptr->hintisa, depth, 1, isaptr);
} else {
    // Something already there: truncate to hintlength+1, increment last digit
    tumblertruncate(&lowerbound, hintlength + depth, isaptr);
    tumblerincrement(isaptr, tumblerlength(isaptr)==hintlength ? depth : 0, 1, isaptr);
}
```

`findpreviousisagr` [granf2.c:255] does a tree scan to find the highest occupied address below the bound — it carries no stored state between calls.

---

### What the Address Scheme Produces

Confirmed by golden tests [golden/versions/version_address_allocation.json]:

| Source | Version N | Address |
|--------|-----------|---------|
| `1.1.0.1.0.1` | 1st | `1.1.0.1.0.1.1` |
| `1.1.0.1.0.1` | 2nd | `1.1.0.1.0.1.2` |
| `1.1.0.1.0.2` | 1st | `1.1.0.1.0.2.1` |
| `1.1.0.1.0.1.1` | 1st sub-version | `1.1.0.1.0.1.1.1` |

Versions are **direct children** of their source document in the tumbler address hierarchy — the ordinal is appended at `depth=1` (no zero separator). This is structurally distinct from the ACCOUNT→DOCUMENT two-level (`depth=2`) scheme, which inserts a zero separator (e.g., `1.1.0.1` → `1.1.0.1.0.1`).

Multiple sibling versions of the same source (`1.1.0.1.0.1.1`, `1.1.0.1.0.1.2`, …) are allocated by scanning for the highest child already in the granfilade, then incrementing. If version 1 has its own sub-versions (e.g., `1.1.0.1.0.1.1.1`), `findpreviousisagr` finds `1.1.0.1.0.1.1.1`, `tumblertruncate` cuts it back to one level deep (`1.1.0.1.0.1.1`), and incrementing that yields `1.1.0.1.0.1.2` correctly — so interleaved version chains don't corrupt the allocation.

---

### Contrast with Content and Link Sub-allocators

The **text content** allocator (`findisatoinsertmolecule` [granf2.c:158]) also uses `findpreviousisagr` — same mechanism, different hint geometry. The **link V-address** allocator (`findnextlinkvsa` [do2.c:151]) works differently: it retrieves the document's current vspan extent via `doretrievedocvspan`, then either uses `2.1` as the minimum or appends after the existing content extent. This is the only one that reads persistent document state (the vspan) rather than scanning the granfilade tree directly.

There is **no per-document version counter, no global version frontier register, and no `inc` on the prior version address**. The granfilade tree itself is the allocator's state. The next version ordinal is always derived from `findpreviousisagr` at call time.
