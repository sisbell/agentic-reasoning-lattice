# Consultation Answers — Tumbler Baptism

**Inquiry:** What does it mean to baptize a new position in the tumbler hierarchy? What invariants govern the set of baptized positions across all levels?
**Date:** 2026-03-15 09:37
**Questions:** 12 (6 nelson, 6 gregory)

---

## Question 1 [nelson]

> Must newly baptized positions always extend beyond all previously baptized positions at the same level, or can gaps in the position space ever be filled retroactively?

### Nelson's Answer

[No answer]

---

## Question 2 [nelson]

> What is the relationship between baptizing a position at one level of the hierarchy and the existence of a baptized position at the level above it?

### Nelson's Answer

[No answer]

---

## Question 3 [nelson]

> Can a position be baptized but never used — and if so, must the system distinguish between "registered but empty" and "never registered"?

### Nelson's Answer

[No answer]

---

## Question 4 [nelson]

> Does baptizing a position at any level carry a permanent commitment about the range of positions available beneath it for future baptism?

### Nelson's Answer

[No answer]

---

## Question 5 [nelson]

> If two independent acts of baptism occur at the same level of the hierarchy, what guarantees prevent them from producing the same position?

### Nelson's Answer

[No answer]

---

## Question 6 [nelson]

> Is there a design limit on how many positions can be baptized beneath a single parent position, or must the addressing scheme support unbounded growth at every level?

### Nelson's Answer

[No answer]

---

## Question 7 [gregory]

> What constitutes "baptizing" a tumbler position — is it the first successful allocation at that level via query-and-increment, or is there a distinct registration step that precedes allocation?

### Gregory's Answer

## KB Synthesis

The KB does not use the term "baptism" explicitly, so I'll synthesize what the allocation evidence implies about when a tumbler position becomes "established" in the system.

## The Allocation Mechanism Is the Only Registration Step

Based on the evidence in the KB, there is no distinct registration step prior to allocation. The query-and-increment write into the granfilade **is** the singular act that establishes a tumbler position:

**Document addresses** — `createorglingranf` calls `findisatoinsertnonmolecule`, which:
1. Computes upper bound via `tumblerincrement(hintisa, depth-1, 1)`
2. Calls `findpreviousisagr` to find the highest existing address below that bound
3. Checks containment under the parent (Bug 0013 fix)
4. Writes the new orgl node into the granfilade tree

The moment the node is written, the address exists in the tree and influences all subsequent allocations in that range. [SS-ADDRESS-ALLOC]

**Content I-addresses** — `inserttextingranf` similarly calls `findisatoinsertmolecule`, finds the previous maximum, increments by 1, then writes. [SS-ADDRESS-SPACE / Finding 0061]

**Link I-addresses** — `domakelink` uses the same pattern scoped to `docISA.2.2–docISA.2.3`. [SS-ADDRESS-ALLOC / Finding 0065]

## Why There Is No Separate Registration

Three properties make a prior registration step unnecessary:

1. **Stateless allocation** — There is no cached "next available" pointer. Every allocation queries the live granfilade tree for the current maximum. The tree itself is the canonical registry. [Finding 0061]

2. **Monotonic uniqueness** — Because allocation always takes `max + 1` and the granfilade is append-only, no address is ever reused. Existence in the tree is both necessary and sufficient for an address to be "established." [INV-MONOTONIC, INV-NO-IADDR-REUSE]

3. **Partitioned namespaces** — Each tumbler range (document addresses, text I-addresses, link I-addresses) is allocated independently via `findisatoinsertgr` dispatching to molecule vs. non-molecule paths. Each partition's "baptism" is scoped: `next_doc_addr(granf, parent)` and `next_content_addr(granf, doc)` are independent functions of tree state. [Finding 0077]

## The Distinction That May Matter

What could be called "baptism" at the account/document hierarchy level is the first-child allocation: when no children exist under a parent, the algorithm allocates `parent.0.1` rather than incrementing from a prior maximum. This first-child creation is the only structurally distinct case — subsequent allocations simply increment the sibling counter. [SS-ADDRESS-ALLOC / Finding 0021]

```
Parent account 1.1.0.2, no existing documents:
  findpreviousisagr returns nothing under parent
  → allocates 1.1.0.2.0.1  ← "baptism": first child
  
Same account, existing document 1.1.0.2.0.1:
  findpreviousisagr returns 1.1.0.2.0.1
  → allocates 1.1.0.2.0.2  ← ordinary increment
```

The granfilade write is the single moment of establishment in both cases — the query-and-increment process has no predecessor registration step separate from the write itself.

---

## Code Exploration

Now I have everything needed for a complete answer. Here it is:

---

## "Baptizing" a Tumbler Position in udanax-green

The word **"baptize" does not appear anywhere in the source code.** However, the concept maps precisely onto the two-phase address allocation + insertion sequence. Here is the exact code trace.

---

### Phase 0: Hint Construction — The Pre-Condition

Before any address is computed, the caller constructs a `typehint` that encodes *where* the new item should live and *what kind of thing* it is.

**`do2.c:78`** — `makehint`:
```c
int makehint(INT typeabove, INT typebelow, INT typeofatom, typeisa *isaptr, typehint *hintptr)
{
    hintptr->supertype = typeabove;
    hintptr->subtype = typebelow;
    hintptr->atomtype = typeofatom;
    movetumbler (isaptr, &hintptr->hintisa);
}
```

`typehint` is defined at **`xanadu.h:148-153`**:
```c
typedef struct {
    INT supertype;
    INT subtype;
    INT atomtype;
    typeisa hintisa;
} typehint;
```

`hintisa` is the *parent address* — the account or document under which the new item will be allocated. For example:

- `do1.c:239` — creating a new document: `makehint(ACCOUNT, DOCUMENT, 0, &taskptr->account, &hint)` — parent is the current account
- `do1.c:117` — inserting text: `makehint(DOCUMENT, ATOM, TEXTATOM, docisaptr, &hint)` — parent is the open document
- `do1.c:251` — creating a node: `makehint(NODE, NODE, 0, &isa, &hint)` — parent is the node itself

This is **not** allocation. It sets up the context for the forthcoming query.

---

### Phase 1: Address Computation — Query-and-Increment

The entry point is **`granf2.c:130`** — `findisatoinsertgr`:

```c
bool findisatoinsertgr(typecuc *fullcrumptr, typehint *hintptr, typeisa *isaptr)
{
    if (hintptr->subtype == ATOM) {
        if (!isaexistsgr (fullcrumptr, &hintptr->hintisa)) {
            return (FALSE);
        }
        findisatoinsertmolecule (fullcrumptr, hintptr, isaptr);
    } else {
        findisatoinsertnonmolecule (fullcrumptr, hintptr, isaptr);
    }
    tumblerjustify(isaptr);   // granf2.c:154
    return (TRUE);
}
```

#### For documents/accounts/nodes — `findisatoinsertnonmolecule` (`granf2.c:203`)

```c
depth = hintptr->supertype == hintptr->subtype ? 1 : 2;  // :209
hintlength = tumblerlength (&hintptr->hintisa);           // :211
tumblerincrement (&hintptr->hintisa, depth - 1, 1, &upperbound); // :213 — compute search ceiling
clear (&lowerbound, sizeof(lowerbound));                  // :215
findpreviousisagr ((typecorecrum*)fullcrumptr, &upperbound, &lowerbound); // :217 — QUERY
```

`findpreviousisagr` (`granf2.c:255`) descends the tree to find the **highest existing address** strictly below `upperbound`. Nothing is written here.

Then, at `granf2.c:235-241`, the new address is computed:
```c
if (iszerotumbler(&lowerbound) || !lowerbound_under_hint) {
    // Nothing exists under this parent yet — first child
    tumblerincrement(&hintptr->hintisa, depth, 1, isaptr);   // :237
} else {
    tumblertruncate (&lowerbound, hintlength + depth, isaptr); // :239
    tumblerincrement(isaptr, tumblerlength(isaptr)==hintlength ? depth : 0, 1, isaptr); // :240
}
```

`tumblerincrement` (`tumble.c:599`) is the arithmetic primitive:
```c
int tumblerincrement(tumbler *aptr, INT rightshift, INT bint, tumbler *cptr)
{
    if (iszerotumbler (aptr)) {           // :603
        tumblerclear (cptr);
        cptr->exp = -rightshift;
        cptr->mantissa[0] = bint;
        return(0);
    }
    // ...
    cptr->mantissa[idx + rightshift] += bint;  // :621
    tumblerjustify (cptr);                     // :622
}
```

**At this point, the address exists only as bits in a local variable `isaptr`.** Nothing has been written to the granfilade tree.

#### For text/link atoms — `findisatoinsertmolecule` (`granf2.c:158`)

Same pattern: `tumblerincrement` computes an `upperbound`, `findpreviousisagr` queries the tree for the highest existing atom, then a `tumblerincrement` on the result yields the new address. Still nothing is written.

---

### Phase 2: Insertion — The Moment of "Baptism"

The address returned by `findisatoinsertgr` is not yet real. It becomes real only when it is *inserted* into the enfilade.

#### For documents and links — `createorglgr` (`granf2.c:111`):

```c
bool createorglgr(typetask *taskptr, typegranf fullcrumptr, typehint *hintptr, typeisa *isaptr)
{
    if (!findisatoinsertgr ((typecuc*)fullcrumptr, hintptr, isaptr))  // :117 — compute address
        return (FALSE);
    locinfo.infotype = GRANORGL;
    locinfo.granstuff.orglstuff.orglptr = createenf (POOM);           // :120 — create new POOM
    ...
    insertseq ((typecuc*)fullcrumptr, isaptr, &locinfo);              // :125 — WRITE to tree
    ...
}
```

`insertseq` at `:125` is the actual insertion into the granfilade. This is the moment the address is committed — it can now be found by `findpreviousisagr` or `isaexistsgr`.

#### For text — `inserttextgr` (`granf2.c:83`):

```c
bool inserttextgr(...) {
    if (!findisatoinsertgr (..., hintptr, &lsa))  // :92 — compute starting address
        return (FALSE);
    movetumbler (&lsa, &spanorigin);
    for (; textset; textset = textset->next) {
        locinfo.infotype = GRANTEXT;
        ...
        insertseq ((typecuc*)fullcrumptr, &lsa, &locinfo);              // :99 — WRITE each chunk
        tumblerincrement (&lsa, 0, textset->length, &lsa);             // :100 — advance address
    }
    ...
}
```

The starting address is computed once; each chunk is inserted via `insertseq` at an address that advances by `textset->length` after each call.

---

### The Direct Answer

**There is no distinct "registration step" that precedes allocation.** The sequence is:

1. `makehint` — builds context (parent ISA, type relationship)
2. `findisatoinsertgr` → `findisatoinsertnonmolecule` / `findisatoinsertmolecule` — **query-and-increment**: reads the tree, computes the next available address, returns it in a local variable. Nothing is written.
3. `insertseq` (called from inside `createorglgr` or `inserttextgr`) — **writes the node** at the computed address into the granfilade tree.

**"Baptism" is `insertseq`, not the query-and-increment.** The query-and-increment produces a *candidate* address that exists only in memory. If you called `findisatoinsertgr` twice without `insertseq` in between, both calls would return the **same address** — because the tree has not changed and `findpreviousisagr` would find the same highest existing node both times.

The address is not a permanent, system-visible fact until it is inserted into the enfilade at `granf2.c:99` (text) or `granf2.c:125` (orgl). That insertion is what makes the address discoverable by all subsequent queries — it is the act that "baptizes" the position into the coordinate space.

---

## Question 8 [gregory]

> Must baptism at a child level (e.g., `1.1.0.2`) be preceded by baptism of the parent position (`1.1`) — is there a strict hierarchical prerequisite chain?

### Gregory's Answer

## KB Synthesis

Based on the KB, the allocation algorithm does **not** enforce a strict hierarchical prerequisite chain where each ancestor must be formally registered before a child can be created. Here is what the evidence supports:

## How Address Allocation Actually Works

The allocation algorithm (`findisatoinsertnonmolecule`, [SS-ADDRESS-ALLOC] Finding 0021) takes the intended parent address as a **boundary hint**, not as a required existing entry:

1. Compute `upperbound = tumblerincrement(hintisa, depth-1, 1)` — the next sibling of the parent
2. Call `findpreviousisagr` to find the highest address in the **existing** granfilade tree below that bound
3. If nothing is found under the parent: allocate first child as `parent.0.1`
4. If something is found: truncate and increment to produce the next sibling

The critical point: `findpreviousisagr` searches the existing tree for entries in the bounded range. If no entries exist under `1.1` yet, the search returns nothing and `1.1.0.1` is allocated as the first child — without requiring `1.1` to itself be present as a granfilade entry.

## What Bug 0013 Reveals

The containment-check fix documented in [PRE-ADDRESS-ALLOC] Finding 0021 shows the algorithm operates purely on **tumbler arithmetic and tree search**, not on ancestor existence:

> When allocating under account `1.1.0.2`, the search found `1.1.0.1.0.1` (under a different account) and incorrectly incremented from it, producing `1.1.0.1.0.2`.

The bug was in *cross-boundary* search, not in missing-ancestor detection. The fix adds a prefix-match check on the *found* candidate — it does not add any check that the parent address exists.

## Implicit Dependencies That Do Exist

The KB does document *some* prerequisites, but they are operational rather than structural:

- **Session account context** ([SS-SESSION-STATE] Finding 0022): To allocate under an account, your session must have that account set. This is access control, not a granfilade-existence check.
- **Source document existence for VERSION** ([ST-VERSION-OWNERSHIP] Finding 0068): `docreatenewversion` calls `findorgl` on the source document, which does require the document to exist as an open orgl. But this is because you are *copying* from it, not merely naming it as a parent.
- **Ownership check for VERSION** ([SS-VERSION-ADDRESS] Finding 0068): The `tumbleraccounteq && isthisusersdocument` check determines allocation path (child-of-doc vs. child-of-account), but failure does not reject the operation — it redirects to a different parent.

## What the KB Does Not Address

The KB has no findings that document:
- A formal "account creation" or "node registration" operation that would constitute baptism of a parent address
- Any check in `findisatoinsertnonmolecule` or `findisatoinsertmolecule` that verifies ancestor existence
- Any notion of an address being "invalid" simply because its parent has no granfilade entry

## Summary

The allocation mechanism is **tolerant of unregistered ancestors**. Allocating `1.1.0.2` requires only that the session context names `1.1` as the intended parent — not that `1.1` appears as an entry in the granfilade. The tree search simply finds no existing children and allocates `1.1.0.1` as the first, with no error or prerequisite check. A strict hierarchical prerequisite chain of baptisms is **not required** by the implementation as documented in the KB.

---

## Code Exploration

I now have a complete picture. Here is the full answer.

---

## Does Child-Level Baptism Require Prior Parent Baptism?

The word "baptism" does not appear in the udanax-green source. The concept maps to **granfilade entry creation** — the moment an entity receives a permanent tumbler address in the granfilade tree. The answer is: **it depends on the type of entity being created, and the check is asymmetric.**

---

### The Two Allocation Paths

All baptism flows through `findisatoinsertgr` in `granf2.c:130-156`, which branches immediately on whether the new entity is an ATOM (content: text or links) or a structural entity (DOCUMENT, ACCOUNT, NODE):

```c
// granf2.c:135-153
if (hintptr->subtype == ATOM) {
    if (!isaexistsgr (fullcrumptr, &hintptr->hintisa)) {
        fprintf (stderr,"nothing at hintisa for atom\n");
        return (FALSE);                           // HARD GATE: parent doc must exist
    }
    findisatoinsertmolecule (fullcrumptr, hintptr, isaptr);
} else {
    findisatoinsertnonmolecule (fullcrumptr, hintptr, isaptr); // NO parent check
}
```

**ATOM path** (content insertion): `isaexistsgr` is called on `hintptr->hintisa` — the owning document's address. If that document is not registered in the granfilade, the call returns `FALSE` immediately. **The parent must exist.**

**Non-ATOM path** (document/account/node creation): `findisatoinsertnonmolecule` is called with no such check. The parent address in `hintptr->hintisa` is used purely as an **arithmetic anchor** for computing the child's address — it is never verified to exist.

---

### How `findisatoinsertnonmolecule` Allocates Without a Parent Check

`granf2.c:203-242`:

```c
depth = hintptr->supertype == hintptr->subtype ? 1 : 2;
hintlength = tumblerlength (&hintptr->hintisa);
tumblerincrement (&hintptr->hintisa, depth - 1, 1, &upperbound);
clear (&lowerbound, sizeof(lowerbound));
findpreviousisagr ((typecorecrum*)fullcrumptr, &upperbound, &lowerbound);

// BUG FIX #2: lowerbound must be under hintisa, not from another account
lowerbound_under_hint = FALSE;
if (!iszerotumbler(&lowerbound)) {
    tumblertruncate(&lowerbound, hintlength, &truncated);
    lowerbound_under_hint = tumblereq(&truncated, &hintptr->hintisa);
}

if (iszerotumbler(&lowerbound) || !lowerbound_under_hint) {
    tumblerincrement(&hintptr->hintisa, depth, 1, isaptr); // → hintisa.0.1
} else {
    tumblertruncate (&lowerbound, hintlength + depth, isaptr);
    tumblerincrement(isaptr, tumblerlength(isaptr)==hintlength?depth:0, 1, isaptr);
}
```

For an `ACCOUNT→DOCUMENT` creation (depth=2) with `hintisa = 1.1`:
- `upperbound = tumblerincrement(1.1, 1, 1)` = `1.1.1` (the search ceiling)
- `findpreviousisagr` finds the largest granfilade entry strictly below `1.1.1`
- If nothing is under `1.1` (i.e., `1.1` itself has never been registered), BUG FIX #2 catches it and produces: `tumblerincrement(1.1, 2, 1)` = `1.1.0.1`
- On the second call: the existing `1.1.0.1` is found → result is `1.1.0.2`

The BUG FIX #2 comment [granf2.c:224-226] is explicit about this scenario:
> "Also check if lowerbound is actually under hintisa. If the found item is from a different account (e.g., 1.1.0.1.0.1 when creating under 1.1.0.2), treat it as if nothing was found."

This confirms `1.1.0.2` is treated as an account address in this codebase, and the system explicitly handles the case where nothing yet exists under it — without ever requiring `1.1.0.2` to be pre-registered.

---

### The `makehint` Setup: No Existence Validation

`makehint` at `do2.c:78-84` simply copies the hint's tumbler fields:

```c
int makehint(INT typeabove, INT typebelow, INT typeofatom, typeisa *isaptr, typehint *hintptr)
{
    hintptr->supertype = typeabove;
    hintptr->subtype = typebelow;
    hintptr->atomtype = typeofatom;
    movetumbler (isaptr, &hintptr->hintisa);   // just copies, no existence check
}
```

`validhint` [do2.c:86-108] validates the *type* fields (e.g., subtype must be ≥ supertype, difference ≤ 1), but never queries the granfilade for the `hintisa` address.

---

### Three Creation Functions and What They Require

**`docreatenewdocument`** [do1.c:234-241]:
```c
makehint (ACCOUNT, DOCUMENT, 0, &taskptr->account, &hint);
return (createorglingranf (taskptr, granf, &hint, isaptr));
```
Hint: `hintisa = taskptr->account`. No check that the account exists in the granfilade.

**`docreatenode_or_account`** [do1.c:243-258]:
```c
makehint (NODE, NODE, 0, &isa, &hint);
result = createorglingranf (taskptr, granf, &hint, &isa);
```
Hint: `hintisa = isa` (client-supplied address). No check that the parent node exists. `depth = 1` (NODE→NODE).

**`docreatenewversion`** [do1.c:260-299]:
```c
if (tumbleraccounteq(isaptr, wheretoputit) && isthisusersdocument(isaptr)) {
    makehint (DOCUMENT, DOCUMENT, 0, isaptr, &hint);   // hintisa = source doc
} else {
    makehint (ACCOUNT, DOCUMENT, 0, wheretoputit, &hint); // hintisa = target account
}
if (!createorglingranf(taskptr, granf, &hint, newisaptr)) return FALSE;
if (!doretrievedocvspanfoo (taskptr, isaptr, &vspan)) return FALSE;  // ← implicit gate
```

Here there IS an implicit dependency: `doretrievedocvspanfoo` calls `findorgl` [granf1.c:17-41], which calls `checkforopen` [bert.c:52-87]. The **source document must be open in BERT** or the operation fails. But this is a gate on the *source document being open*, not on any ancestor being baptized.

---

### `isthisusersdocument` and `tumbleraccounteq`

`xumain.c:198-201`:
```c
int isthisusersdocument(tumbler *tp) {
    return tumbleraccounteq(tp, &taskptrx->account);
}
```

`tumbleraccounteq` [tumble.c:38-70] checks whether `tp` (a document address) **falls within** the account's address space by comparing the account's non-zero mantissa positions. This is a **namespace containment check**, not a "parent is registered" check. The account address is just a prefix that defines ownership semantics.

---

### Conclusion

**No, there is no strict hierarchical prerequisite chain for structural entity baptism (documents, accounts, nodes).** The granfilade allocation logic in `findisatoinsertnonmolecule` [granf2.c:203-242] treats the parent's hint address purely arithmetically — it is never verified to exist via `isaexistsgr`. BUG FIX #2 specifically hardens this against the case where the parent position is empty: if nothing has been allocated under the hint yet, the allocator computes `hintisa.0.1` directly.

**There IS a prerequisite chain for content (ATOM) insertion** [granf2.c:135-140]: inserting text or links requires the owning document to already exist in the granfilade (`isaexistsgr` is called and returns `FALSE` if it does not). This means the practical FEBE sequence — create account → create document → insert content — does impose ordering, but only at the ATOM level, and it is the document (not its parent account) that must pre-exist.

The baptism of `1.1.0.2` (an account address) requires only that you invoke `docreatenode_or_account` or a similar creation function with `hintisa = 1.1` and the right type flags. Whether `1.1` itself has previously been baptized is irrelevant to the granfilade allocator.

---

## Question 9 [gregory]

> Is the set of baptized positions at any given level always a contiguous prefix (1 through N with no gaps), or can gaps exist between baptized positions?

### Gregory's Answer

## KB Synthesis

## Baptized Positions: Contiguous Prefix or Gapped?

Within a **single, homogeneous allocation namespace**, baptized positions always form a contiguous prefix 1 through N with no gaps. Within **mixed-type namespaces**, gaps can appear.

---

### Why contiguous within a homogeneous namespace

The allocation algorithm in [SS-ADDRESS-ALLOC] / [ST-ADDRESS-ALLOC] (Finding 0021) guarantees this structurally:

1. **First allocation is always `.1`** — if nothing exists under the parent, `findisatoinsertnonmolecule` places the first child at `parent.0.1`
2. **Each subsequent allocation is `max_existing + 1`** — `findpreviousisagr` finds the highest existing address under the parent, then `tumblerincrement` steps it by 1
3. **Truncation handles deeper entities** — if the highest address found is a sub-entity (e.g., content within document 1), it is truncated to the target depth before incrementing, so it yields the correct sibling, not a gap

For example, allocating version 2 of `1.1.0.2.0.1` when version 1 already has content at `1.1.0.2.0.1.1.3.0.1.5`:
- Found max: `1.1.0.2.0.1.1.3.0.1.5`
- Truncated to version depth (length 6): `1.1.0.2.0.1.1`
- Incremented: `1.1.0.2.0.1.2` — no gap

[INV-MONOTONIC] (Findings 0033, 0061, 0065, 0068) and [INV-NO-IADDR-REUSE] (Finding 0061) reinforce this: the granfilade is append-only ([FC-GRANF-ON-DELETE]), so all previously baptized addresses remain in the tree permanently and continue to anchor the allocation sequence. There is no free-list and no address reuse, so the sequence cannot develop retroactive holes.

Version addresses specifically: "[d]eleting a version does not remove its address from the granfilade... the next version will be allocated after the deleted one" — creating `.1`, deleting it, then creating again yields `.2`, not `.1` reused. [SS-VERSION-ADDRESS] (Finding 0068).

---

### Where gaps do appear

Gaps exist when **different entity types share the same bounded allocation subspace**. The canonical case is documented in [INT-LINK-INSERT] (Finding 0063):

- INSERT "ABC" → text I-addresses `I.1, I.2, I.3`
- CREATELINK → link orgl allocated at `~I.2.0` (same granfilade region, different element field)
- INSERT "DEF" → text I-addresses `I.2.1+` (non-contiguous with ABC)

`compare_versions` reports two span pairs because the text-only I-address subsequence has a gap caused by the intervening link orgl allocation.

This occurs because `findisatoinsertmolecule` searches the granfilade maximum regardless of entity type — it sees the link orgl's address as the new maximum and allocates above it. [SS-ADDRESS-ALLOC] (Finding 0077): "Both query the same granfilade tree but search different subtrees" — but only when allocation bounds are properly partitioned. Text and link content I-addresses have separate bounds (`docISA.3.x` vs `docISA.2.x`) per Finding 0065, which prevents cross-type pollution for link-vs-text allocation within a document.

---

### Summary

| Namespace | Contiguous? | Evidence |
|-----------|-------------|----------|
| Document addresses under an account | Yes | [ST-ADDRESS-ALLOC] (0021), [INV-MONOTONIC] |
| Version addresses under a document | Yes | [SS-VERSION-ADDRESS] (0068), [INV-NO-IADDR-REUSE] |
| Link I-addresses under a document | Yes | [SS-ADDRESS-ALLOC] (0065) — bounded to `docISA.2.x` |
| Text content I-addresses (when no links created) | Yes | [INV-MONOTONIC] (0033) |
| Text content I-addresses (when links interleaved) | **No** | [INT-LINK-INSERT] (0063) — link orgl allocation creates gaps |

---

## Code Exploration

I now have everything needed for a complete answer. Here is the full analysis with code citations:

---

## Answer: Baptized Positions Are Always a Contiguous Prefix — No Gaps

The set of baptized positions at any given level is **always a contiguous prefix 1 through N**. The allocation algorithm guarantees this by construction, and there is no mechanism that could produce gaps.

---

### What "Baptism" Is

In udanax-green, "baptizing" a position means assigning a new ISA (Internal Storage Address, represented as a tumbler) to a new object (document, link, text atom, etc.) in the granfilade. The assignment is permanent — once an ISA is issued, it is never revoked or reused.

There are two allocation paths depending on the kind of object being created.

---

### Path 1: Non-atom objects (documents, nodes, versions)

`findisatoinsertnonmolecule` [**granf2.c:203–242**] handles documents, accounts, and nodes.

```c
static int findisatoinsertnonmolecule(typecuc *fullcrumptr, typehint *hintptr, typeisa *isaptr)
{
  typeisa upperbound, lowerbound, truncated;
  INT depth, hintlength;
  bool lowerbound_under_hint;

    depth = hintptr->supertype == hintptr->subtype ? 1 : 2;   // [209]
    hintlength = tumblerlength (&hintptr->hintisa);            // [211]
    tumblerincrement (&hintptr->hintisa, depth - 1, 1, &upperbound); // [213]
    clear (&lowerbound, sizeof(lowerbound));
    findpreviousisagr ((typecorecrum*)fullcrumptr, &upperbound, &lowerbound); // [217]

    lowerbound_under_hint = FALSE;
    if (!iszerotumbler(&lowerbound)) {
        tumblertruncate(&lowerbound, hintlength, &truncated);  // [231]
        lowerbound_under_hint = tumblereq(&truncated, &hintptr->hintisa); // [232]
    }

    if (iszerotumbler(&lowerbound) || !lowerbound_under_hint) {
        tumblerincrement(&hintptr->hintisa, depth, 1, isaptr); // [237]: first child → hintisa.0.1
    } else {
        tumblertruncate (&lowerbound, hintlength + depth, isaptr);  // [239]
        tumblerincrement(isaptr, tumblerlength(isaptr)==hintlength?depth:0, 1, isaptr); // [240]: max+1
    }
}
```

The two branches are:
- **Empty tree**: first baptized position is `hintisa.0.1` [granf2.c:237] — i.e., position 1 under the hint.
- **Items exist**: new position is `truncate(highest_existing, depth) + 1` [granf2.c:239–240] — i.e., the next sequential value after the current maximum.

The inner search is `findpreviousisagr` [**granf2.c:255–278**], which walks the granfilade tree to find the strict maximum under the upper bound:

```c
int findpreviousisagr(typecorecrum *crumptr, typeisa *upperbound, typeisa *offset)
{
    if (crumptr->height == 0) {
        findlastisaincbcgr ((typecbc*)crumptr, offset);  // [264]: bottom: report ISA
        return(0);
    }
    for (ptr = findleftson((typecuc*)crumptr); ptr; ptr = findrightbro(ptr)) {
        if ((tmp = whereoncrum(ptr, offset, upperbound, WIDTH)) == THRUME
        ||  tmp == ONMYRIGHTBORDER
        ||  !ptr->rightbro) {
            findpreviousisagr (ptr, upperbound, offset); // [272]: descend into rightmost child
            return(0);
        } else {
            tumbleradd(offset, &ptr->cwid.dsas[WIDTH], offset); // [275]: accumulate width
        }
    }
}
```

This recursively descends into the rightmost child at each level [granf2.c:272], accumulating widths [granf2.c:275] until it reaches the bottom crum, where `findlastisaincbcgr` [granf2.c:280–284] returns the address of the rightmost atom:

```c
int findlastisaincbcgr(typecbc *ptr, typeisa *offset)
{
    if (ptr->cinfo.infotype == GRANTEXT)
        tumblerincrement (offset, 0, (INT) ptr->cinfo.granstuff.textstuff.textlength - 1, offset); // [283]
}
```

The result is the true maximum ISA in the subtree. There is no case where a value is skipped.

---

### Path 2: Atom objects (text content, links)

`findisatoinsertmolecule` [**granf2.c:158–181**] handles text atoms and link atoms. It also calls `findpreviousisagr` [granf2.c:164] to find the current maximum, then increments from it:

```c
tumblerincrement (&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound); // [162]
findpreviousisagr (..., &upperbound, &lowerbound);                            // [164]
if (tumblerlength (&hintptr->hintisa) == tumblerlength (&lowerbound)) {
    tumblerincrement (&lowerbound, 2, hintptr->atomtype, isaptr);             // [166]
    tumblerincrement (isaptr, 1, 1, isaptr);                                  // [167]: +1
} ...
```

Again: find current maximum, add 1.

---

### The Increment Primitive

`tumblerincrement` [**tumble.c:599–623**] always adds a fixed integer `bint` (always `1` in the allocation calls) at a specific digit position — never randomly, never with gaps:

```c
int tumblerincrement(tumbler *aptr, INT rightshift, INT bint, tumbler *cptr)
{
    ...
    for (idx = NPLACES; aptr->mantissa[--idx] == 0 && idx > 0;);  // [611]: find last non-zero
    cptr->mantissa[idx + rightshift] += bint;  // [621]: add 1 at next position
    tumblerjustify (cptr);
}
```

---

### Why No Gaps Can Appear

**1. Allocation is always max+1.** Every new ISA is computed as: find the current highest, add 1 at the correct depth. There is no skipping, no random assignment, no reservation.

**2. Granfilade objects are never deleted.** The FEBE protocol has no `deletedocument`, `deletelink`, or equivalent operation. `dodeletevspan` [do1.c] removes virtual content from a document's POOM/spanfilade, not the document's ISA entry from the granfilade. Since granfilade entries are never removed, `findpreviousisagr` always returns the true historical maximum, never a value below it.

**3. The `lowerbound_under_hint` check prevents false maxima.** The bug fix at [granf2.c:228–233] ensures that if `findpreviousisagr` returns an address from a different parent (e.g., from account 1.1.0.1 when allocating under 1.1.0.2), it is ignored and the first-child address (.0.1) is used instead. This prevents contamination but does not create gaps — it produces the correct position 1 in a fresh namespace.

**4. No free-list, no recycling.** There is no data structure that tracks available or freed position slots. No function searches for holes to fill.

---

### Concrete Example

Under account `1.1`:
- `docreatenewdocument` calls `makehint(ACCOUNT, DOCUMENT, ...)` [do1.c:239], setting depth=2
- First document: `findpreviousisagr` finds nothing → first address is `1.1.0.1` [granf2.c:237]
- Second document: `findpreviousisagr` finds `1.1.0.1` → new address is `1.1.0.2` [granf2.c:239–240]
- Third document: `findpreviousisagr` finds `1.1.0.2` → new address is `1.1.0.3`

The document namespace under any account is always `1.1.0.1`, `1.1.0.2`, ..., `1.1.0.N` — a perfect contiguous prefix. Versions follow the same pattern under their parent document address.

---

### Conclusion

**Baptized positions at every level are always a contiguous prefix `1` through `N` with no gaps.**

The allocation algorithm (`findisatoinsertnonmolecule`, `findisatoinsertmolecule`) invariably finds the current maximum and assigns max+1. No mechanism exists to skip positions, and no mechanism exists to reclaim or free positions once assigned. The granfilade never loses a baptized entry, so the maximum is always accurately reported to subsequent allocations.

---

## Question 10 [gregory]

> Does the `.0.` digit separator play a structural role in baptism (e.g., marking a level boundary that baptism must respect), or is it purely a conventional interpretation of an unconstrained digit sequence?

### Gregory's Answer

## KB Synthesis

The `.0.` separator is **not a first-class structural token** in the tumbler representation — it is an artifact of the allocation arithmetic at a specific depth. But it does play a real structural role in baptism, through the `depth` parameter in `makehint`.

## What the representation layer knows about zeros

From [SS-TUMBLER] Findings 0001 and 0031: tumblers are unconstrained digit sequences. Zero is just digit value 0. The "zero-separator convention is semantic, not structural — the data type itself does not enforce hierarchy boundaries." No runtime code checks for `.0.` as a boundary marker during insertion, containment, or retrieval.

## How `.0.` enters baptism

The allocation mechanism in `findisatoinsertnonmolecule` ([SS-ADDRESS-ALLOC] Finding 0021) computes the upper bound as:

```
upperbound = tumblerincrement(hintisa, depth-1, 1)
```

The `depth-1` parameter is the rightshift — it controls *where* in the mantissa the increment lands.

- `depth=2` (ACCOUNT→DOCUMENT): `tumblerincrement(hintisa, 1, 1)` increments at the second-to-last position. For a parent like `1.1.0.2`, this produces `1.1.0.3` as the upper bound, and the first child is allocated at `1.1.0.2.0.1` — the `.0.` appears because the search finds nothing under the parent and falls back to constructing `parent.0.1`.
- `depth=1` (DOCUMENT→DOCUMENT, versions): `tumblerincrement(hintisa, 0, 1)` increments the last position. First child is `parent.1` — no `.0.` boundary crossed.

The `.0.` in `parent.0.1` is therefore produced by the first-child fallback path in `findisatoinsertnonmolecule`, not by any zero-recognition logic.

## Containment check uses prefix matching, not zero detection

[SS-TUMBLER-CONTAINMENT] confirms: the containment predicate is pure length-and-equality — truncate A to the length of B, compare. The code does not scan for `.0.` boundaries; it only cares about digit-sequence prefix. The hierarchy structure implied by `.0.` fields is real, but it is maintained by the *allocation invariant* (depth controls how deep a new address sits), not by any special handling of the zero digit itself.

## Summary

The `.0.` separator plays a structural role in baptism **indirectly**: `makehint` encodes the hierarchy level as a depth integer, and the allocation arithmetic at depth=2 produces addresses with `.0.` boundaries as a consequence. But the tumbler type is agnostic to zero — nothing in the allocation, containment, or storage code treats 0 as a level-boundary sentinel. The structural meaning lives in the depth parameter and the address-allocation convention, not in the digit value 0 itself.

---

## Code Exploration

Now I have enough to answer the question with full citations. Here is the complete analysis:

---

## Does `.0.` Play a Structural Role in Baptism?

**Short answer: Yes, it is structural — mechanically enforced by the type hierarchy, semantically interpreted by account containment, and load-bearing in the address allocation algorithm. It is not a free convention.**

---

### 1. What a Tumbler Actually Is

A tumbler is a flat array of 16 unsigned integers (`tdigit`) stored in `mantissa[NPLACES]` [`common.h:53–65`]:

```c
#define NPLACES 16
typedef struct structtumbler {
    humber xvartumbler;
    char varandnotfixed;
    char sign  BIT ;
    short exp;
    tdigit mantissa[NPLACES];
} tumbler;
```

There is no explicit separator token. A zero value at position `k` *is* the `.0.` — it's just `mantissa[k] == 0`. The human notation `1.1.0.1.0.1` maps directly to `mantissa = [1, 1, 0, 1, 0, 1, 0, ...]`.

---

### 2. Baptism: `findisatoinsertnonmolecule`

Baptism — assigning a permanent address to a new document, node, or account — happens in `findisatoinsertnonmolecule` [`granf2.c:203–242`]:

```c
static int findisatoinsertnonmolecule(typecuc *fullcrumptr, typehint *hintptr, typeisa *isaptr)
{
  typeisa upperbound, lowerbound, truncated;
  INT depth, hintlength;
  bool lowerbound_under_hint;

    depth = hintptr->supertype == hintptr->subtype ? 1 : 2;      // [granf2.c:209]

    hintlength = tumblerlength (&hintptr->hintisa);               // [granf2.c:211]

    tumblerincrement (&hintptr->hintisa, depth - 1, 1, &upperbound); // [granf2.c:213]
    ...
    if (iszerotumbler(&lowerbound) || !lowerbound_under_hint) {
        /* Nothing under this hint - create first child as hintisa.0.1 */
        tumblerincrement(&hintptr->hintisa, depth, 1, isaptr);    // [granf2.c:237]
    } else {
        tumblertruncate (&lowerbound, hintlength + depth, isaptr);
        tumblerincrement(isaptr,tumblerlength(isaptr)==hintlength?depth:0,1,isaptr); // [granf2.c:240]
    }
}
```

The `depth` variable is computed directly from the **type hierarchy**, not from parsing any separator:

| Call site | supertype | subtype | depth | separator? |
|---|---|---|---|---|
| `ACCOUNT → DOCUMENT` (`do1.c:239`) | 2 | 3 | **2** | **yes — `.0.`** |
| `ACCOUNT → DOCUMENT` (version, `do1.c:275`) | 2 | 3 | **2** | **yes — `.0.`** |
| `DOCUMENT → DOCUMENT` (new version, `do1.c:271`) | 3 | 3 | **1** | no |
| `NODE → NODE` (`do1.c:251`) | 1 | 1 | **1** | no |

When `depth = 2`, the call `tumblerincrement(&hintptr->hintisa, 2, 1, isaptr)` [`granf2.c:237`] produces the first child address by placing a `1` two positions to the right of the parent's last nonzero digit — leaving one slot zero. That is the `.0.`.

---

### 3. How `tumblerincrement` Mechanically Inserts the Zero

`tumblerincrement(aptr, rightshift, bint, cptr)` [`tumble.c:599–623`]:

```c
int tumblerincrement(tumbler *aptr, INT rightshift, INT bint, tumbler *cptr)
{
    register INT idx;
    ...
    for (idx = NPLACES ; aptr->mantissa[--idx] == 0 && idx > 0;);
    // idx is now the position of the LAST non-zero digit

    cptr->mantissa[idx + rightshift] += bint;   // [tumble.c:621]
    tumblerjustify (cptr);
}
```

For `hintisa = 1.1.0.1` (`mantissa = [1,1,0,1,0,...]`), `idx=3`. With `rightshift=2`:
- writes `1` to `mantissa[5]`
- leaves `mantissa[4] = 0` untouched
- result: `[1,1,0,1,0,1,...]` = `1.1.0.1.0.1`

This is exactly what the comment says: *"create first child address as hintisa.0.1"* [`granf2.c:220,236`].

With `rightshift=1` (`depth=1`, same-type), the zero slot is NOT skipped — no `.0.` separator appears.

---

### 4. `tumbleraccounteq` Interprets the Zero as a Boundary

The zero digit is not just produced by baptism — it is actively interpreted by `tumbleraccounteq` [`tumble.c:38–70`], the function that tests whether a document address falls within an account's namespace:

```c
bool tumbleraccounteq(tumbler *aptr, tumbler *bptr)
{
    /* Compare until account (bptr) terminates with two zeros.
       Key insight: When account has a zero, it marks the boundary of the
       account's address space. */
    for (j_b = 0, i = 0; i < NPLACES; i++) {
        if (bptr->mantissa[i] == 0) {
            if (++j_b == 2) {
                return(TRUE);  /* Account terminated, document is under this account */
            }
            /* First zero in account - document can have any value here */
        } else {
            if (aptr->mantissa[i] != bptr->mantissa[i]) {
                return(FALSE);
            }
        }
    }
    return (TRUE);
}
```

For the default account `1.1.0.1` [`be.c:37`]:
```c
tumbler defaultaccount = {0,0,0,0, 1,1,0,1,0,0,0,0}; /* 1.1.0.1 */
```

Its mantissa is `[1, 1, 0, 1, 0, 0, ...]`. The two trailing zeros terminate the account's range. A document at `1.1.0.1.0.1` (`[1,1,0,1,0,1,...]`) passes `tumbleraccounteq` because:
- position 0: account=1, doc=1 ✓
- position 1: account=1, doc=1 ✓
- position 2: account=0 → first zero, skip (doc may differ)
- position 3: account=1, doc=1 ✓
- position 4: account=0 → second zero → return TRUE

**The zero at position 2 is the `.0.` inside the account address itself.** `tumbleraccounteq` treats it as a "wildcard" slot — documents under this account may have any value there. This function would fail entirely if the zero separator were omitted.

---

### 5. The `hintlength` Guard in Address Allocation

The increment logic at [`granf2.c:240`]:

```c
tumblerincrement(isaptr, tumblerlength(isaptr)==hintlength ? depth : 0, 1, isaptr);
```

This tests whether the found lower bound (truncated to `hintlength+depth` digits) has the same length as the parent's address. If `tumblerlength == hintlength`, the lower bound didn't yet have a child at this depth, so we must increment by `depth` (spanning the zero gap). Otherwise we're already at child depth and increment by `0` (in-place). This comparison directly encodes the fact that `depth` positions (including the zero slot) separate parent from child.

---

### 6. The Commented-Out `klugefindisatoinsertnonmolecule`

The old buggy implementation [`granf2.c:183–201`] simply copied `hintisa` unchanged to `isaptr`:

```c
static int klugefindisatoinsertnonmolecule(...) {
    tumblercopy(&hintptr->hintisa, isaptr);
}
```

The bug report comment explains why this was wrong: *"the first document get the account address itself (1.1.0.1 instead of 1.1.0.1.0.1)"* [`granf2.c:151`]. The `.0.1` suffix is mandatory — without it, the document was created at its parent's address, corrupting the granfilade.

---

### Conclusion

The `.0.` zero digit is **structural**, not merely conventional, for three independent reasons:

1. **It is mechanically enforced by the type system.** `depth = (supertype == subtype) ? 1 : 2` [`granf2.c:209`] determines whether a zero slot is inserted. This is not a configuration or convention — it is computed from the types passed to `makehint` at every call site. Crossing a type boundary (ACCOUNT→DOCUMENT) always requires `depth=2` and therefore always produces a `.0.`.

2. **It is semantically interpreted by `tumbleraccounteq`.** [`tumble.c:38–70`] The zero positions in an account tumbler mark its namespace boundary — they are treated as wildcards during containment tests. An account without these zero separators would fail containment testing entirely.

3. **Baptism's correctness depends on measuring `hintlength` against the zero boundary.** [`granf2.c:209–242`] The algorithm uses `tumblertruncate(..., hintlength + depth, ...)` and the comparison `tumblerlength == hintlength` to detect whether it is still at the parent's level or has crossed into child space. This arithmetic is only correct because the zero digit at position `hintlength` (when `depth=2`) marks the exact boundary.

What is NOT structurally fixed: the `.0.` is not an independently parsed separator token. The tumbler representation has no special encoding for it — it is simply `mantissa[k] == 0`. You could imagine a universe where zeros are numerically equivalent to any other digit and level boundaries are tracked differently. But in *this* implementation, the zero position is load-bearing: baptism must place it at every type-level crossing, or both address allocation and account containment break.

---

## Question 11 [gregory]

> Are there different baptism invariants for different hierarchy levels — for instance, do element-level positions follow different rules than the levels above them in the tumbler tree?

### Gregory's Answer

## KB Synthesis

Yes. The allocation invariants differ meaningfully between hierarchy levels, driven by different code paths (`findisatoinsertnonmolecule` vs `findisatoinsertmolecule`) and different increment strategies.

## Document-level and above (non-molecules)

Handled by `findisatoinsertnonmolecule` [SS-ADDRESS-ALLOC]. The core invariant is:

**Allocated address = max child under parent + 1, with containment check.**

The depth parameter encodes crossing `.0.` field boundaries [SS-ADDRESS-SPACE Finding 0021]:

| Supertype → Subtype | Depth | Pattern |
|---------------------|-------|---------|
| NODE → NODE | 1 | `1.1.0.1.1`, `1.1.0.1.2` |
| ACCOUNT → DOCUMENT | 2 | `1.1.0.2.0.1`, `1.1.0.2.0.2` |
| DOCUMENT → DOCUMENT (version, owned) | 1 | `1.1.0.1.0.1.1`, `1.1.0.1.0.1.2` |

The containment check is **mandatory** at these levels — Bug 0013 showed that without it, `findpreviousisagr` crosses account boundaries and allocates under the wrong parent [PRE-ADDRESS-ALLOC]. The increment is a truncate-at-depth then increment, producing the next sibling.

## Element level (molecules)

Handled by `findisatoinsertmolecule` [SS-ADDRESS-SPACE Finding 0065, 0061, 0033]. The core invariant is:

**Allocated address = max address in document's element subspace + 0.1.**

The critical difference: instead of a containment check, molecule allocation uses an **explicit upperbound** to pre-scope the search:

```
upperbound = tumblerincrement(docISA, 2, atomtype + 1)
```

For TEXTATOM (=1): upperbound = `docISA.2.2`  
For LINKATOM (=2): upperbound = `docISA.2.3`

This creates independent, non-overlapping sub-namespaces under each document. Text atoms accumulate in `docISA.3.x` (approximately `docISA.2.1+` range before link space), link orgls in `docISA.2.2–2.3`. Because the search is bounded by construction, no containment check is needed — it cannot stray outside the target document's element namespace [SS-ADDRESS-SPACE Finding 0077].

The increment at element level is always `tumblerincrement(&lowerbound, 0, 1, ...)` — increment at position 0 (rightshift=0), producing `+0.1` steps, not sibling-level steps [ST-INSERT Finding 0031].

## Key invariant distinctions

| Level | Allocation function | Boundary enforcement | Increment |
|-------|--------------------|--------------------|-----------|
| Node/account/doc | `findisatoinsertnonmolecule` | Post-search containment check | Truncate-at-depth, +1 |
| Element (text, link) | `findisatoinsertmolecule` | Pre-search upperbound | Position-0 increment (+0.1) |

The formal model therefore cannot use a single `Σ.next` counter or a single allocation rule. It requires two families of functions partitioned by entity kind [SS-ADDRESS-SPACE Finding 0077]:

```
next_doc_addr(granf, parent)     = max_child(granf, parent) + 1
next_content_addr(granf, doc)    = max_iaddr_in_namespace(granf, doc, type) + 0.1
```

The owned-vs-unowned distinction for VERSION adds a third variant: when the creating user doesn't own the source document, the allocation falls back to `ACCOUNT→DOCUMENT` depth=2 behavior rather than `DOCUMENT→DOCUMENT` depth=1, placing the version under the user's account instead of the source document [SS-VERSION-ADDRESS Finding 0068].

---

## Code Exploration

Now I have everything I need to give a complete, fully-cited answer.

---

## Baptism Invariants by Hierarchy Level in udanax-green

**Yes — definitively different rules apply at different hierarchy levels.** The code encodes three distinct baptism regimes, controlled by the `hint` struct and the `depth` variable.

---

### The Hierarchy Type Constants

`backend/xanadu.h:140-146` defines the four levels:

```c
#define NODE      1
#define ACCOUNT   2
#define DOCUMENT  3
#define ATOM      4

#define TEXTATOM  1
#define LINKATOM  2
```

This ordered numeric sequence is not cosmetic — the ordering is enforced by `validhint` [do2.c:95-96], which rejects any hint where `subtype < supertype` (you can't go up the hierarchy) or `subtype - supertype > 1` (you can't skip a level). Every address creation call must stay on adjacent rungs of the ladder.

---

### The `makehint` Entry Point

All baptism flows through `makehint` [do2.c:78-84]:

```c
int makehint(INT typeabove, INT typebelow, INT typeofatom, typeisa *isaptr, typehint *hintptr)
{
    hintptr->supertype = typeabove;
    hintptr->subtype = typebelow;
    hintptr->atomtype = typeofatom;
    movetumbler (isaptr, &hintptr->hintisa);
}
```

The `(supertype, subtype)` pair is the primary dispatch mechanism. Callers in `do1.c` use it to encode what level they are creating at:

| Call site | `(supertype, subtype)` | What is being baptized |
|---|---|---|
| `docreatenewdocument` [do1.c:239] | `(ACCOUNT, DOCUMENT)` | new document under account |
| `docreatenode_or_account` [do1.c:251] | `(NODE, NODE)` | node or account peer |
| `docreatenewversion` [do1.c:271] | `(DOCUMENT, DOCUMENT)` | version sibling within same document |
| `docreatenewversion` [do1.c:275] | `(ACCOUNT, DOCUMENT)` | version in a different account |
| text insert [do1.c:117] | `(DOCUMENT, ATOM, TEXTATOM)` | text content within a document |
| link create [do1.c:180,207] | `(DOCUMENT, ATOM, LINKATOM)` | link object within a document |

---

### Regime 1: NODE / ACCOUNT / DOCUMENT Level — `findisatoinsertnonmolecule`

`granf2.c:203-242` handles all non-ATOM baptisms. The critical variable is `depth`:

```c
depth = hintptr->supertype == hintptr->subtype ? 1 : 2;
```
[granf2.c:209]

- **depth = 1** when `supertype == subtype` (e.g., `NODE→NODE` or `DOCUMENT→DOCUMENT`): the new sibling is placed one tumbler digit to the right of the hint address.
- **depth = 2** when crossing a boundary (e.g., `ACCOUNT→DOCUMENT`): two digits of separation are interposed.

The **first child** case:
```c
tumblerincrement(&hintptr->hintisa, depth, 1, isaptr);
```
[granf2.c:237]

This uses `tumblerincrement`'s `rightshift` parameter [tumble.c:599-622] to place the new digit exactly `depth` positions to the right of the last significant digit of the parent address:

```c
int tumblerincrement(tumbler *aptr, INT rightshift, INT bint, tumbler *cptr)
{
    // ...
    cptr->mantissa[idx + rightshift] += bint;
    tumblerjustify (cptr);
}
```

So `ACCOUNT → first DOCUMENT` yields `accountaddr.0.0.1` (depth=2 zeros inserted), while `DOCUMENT → first VERSION` yields `docaddr.0.1` (depth=1).

The **subsequent sibling** case:
```c
tumblertruncate (&lowerbound, hintlength + depth, isaptr);
tumblerincrement(isaptr, tumblerlength(isaptr)==hintlength ? depth : 0, 1, isaptr);
```
[granf2.c:239-240]

This truncates the previous sibling's address to `hintlength + depth` digits, then increments either at position `depth` (if truncation landed exactly at the parent boundary) or at position 0 (last digit). The depth value is thus baked into the truncation length — siblings one level apart are always exactly `depth` digits deeper than their parent.

---

### Regime 2: ATOM Level — `findisatoinsertmolecule`

`granf2.c:158-181` handles ATOM baptism. It does **not** use `depth` at all. Instead, `atomtype` (TEXTATOM=1, LINKATOM=2) drives different increment strategies.

**Boundary condition** first — the parent document must already exist:
```c
if (hintptr->subtype == ATOM) {
    if (!isaexistsgr (fullcrumptr, &hintptr->hintisa)) {
        return (FALSE);  // no parent document, no atom address
    }
    findisatoinsertmolecule (fullcrumptr, hintptr, isaptr);
```
[granf2.c:135-142]

This guard has no analogue at the non-atom levels. Only ATOM baptism requires an existing parent to be validated before address generation proceeds.

Inside `findisatoinsertmolecule`:

```c
tumblerincrement (&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound);
```
[granf2.c:162]

The upper bound search is set 2 positions to the right, with value `atomtype + 1` (TEXTATOM=2, LINKATOM=3). This is a different offset than either `depth=1` or `depth=2`.

When the lower bound matches the parent's length exactly (same-level sibling found):
```c
tumblerincrement (&lowerbound, 2, hintptr->atomtype, isaptr);  // position 2 right, value=atomtype
tumblerincrement (isaptr, 1, 1, isaptr);                        // then one more right
```
[granf2.c:166-167]

When no same-level atom exists yet, **TEXTATOM** and **LINKATOM** diverge further:

- **TEXTATOM**: `tumblerincrement (&lowerbound, 0, 1, isaptr)` [line 169] — simple increment of the last digit
- **LINKATOM**: `tumblerincrement (&hintptr->hintisa, 2, 2, isaptr)` [line 171] — jump 2 positions right with value 2, then conditionally add one more

These are structurally different from each other and from either non-atom regime. **Text content and link objects receive addresses via different algorithms even though both are ATOM-level entities.**

---

### Regime 3: Character / Byte Position — Sequential Increment

Within a text atom, individual characters are positioned purely sequentially — no search, no hint lookup:

```c
insertseq ((typecuc*)fullcrumptr, &lsa, &locinfo);
tumblerincrement (&lsa, 0, textset->length, &lsa);
```
[granf2.c:99-100]

`rightshift=0` means increment the last (rightmost) significant digit by `textset->length`. This is flat sequential addressing with no structural depth computation whatsoever — the character stream is a raw linear span within the atom's location.

---

### The Account Boundary Invariant

`tumbleraccounteq` [tumble.c:38-70] enforces a cross-cutting structural invariant that applies regardless of which regime minted an address:

```c
for (j_b = 0, i = 0; i < NPLACES; i++) {
    if (bptr->mantissa[i] == 0) {
        if (++j_b == 2) {
            return(TRUE);  // second zero: account boundary exhausted, document is contained
        }
        // first zero: document may continue with any digit
    } else {
        if (aptr->mantissa[i] != bptr->mantissa[i]) {
            return(FALSE);  // non-zero mismatch: definitely a different account
        }
    }
}
```

Account addresses terminate with a **double-zero suffix**. Any document or atom address that was correctly baptized under that account must be a numeric extension of the account's prefix. This invariant spans all hierarchy levels — it is the containment constraint that makes the tumbler tree coherent across levels, not a per-level rule, but a universal prefix-containment rule enforced at query time.

---

### The `levelpush` Non-Invariant

`levelpush` [genf.c:263-294] reorganizes the enfilade tree when a level fills up, but crucially **preserves all existing addresses unchanged**:

```c
new = createcrum(fullcrumptr->height, fullcrumptr->cenftype);
transferloaf(fullcrumptr, new);  // move children
fullcrumptr->height++;
adopt((typecorecrum*)new, SON, (typecorecrum*)fullcrumptr);
```

The old children and their addresses are simply moved to a new intermediate node. No re-baptism occurs. `levelpull` [genf.c:318-342] is entirely stubbed out (`return(0)`).

---

### Summary

| Hierarchy level | Entry function | Key variable | Increment position | Requiresparent check? |
|---|---|---|---|---|
| NODE → NODE, DOCUMENT → DOCUMENT | `findisatoinsertnonmolecule` | `depth = 1` | rightshift = 1 | No |
| ACCOUNT → DOCUMENT, DOCUMENT → DOCUMENT (cross-account) | `findisatoinsertnonmolecule` | `depth = 2` | rightshift = 2 | No |
| DOCUMENT → TEXTATOM | `findisatoinsertmolecule` | `atomtype = 1` | rightshift = 0 or 2 | Yes — `isaexistsgr` |
| DOCUMENT → LINKATOM | `findisatoinsertmolecule` | `atomtype = 2` | rightshift = 1 or 2 | Yes — `isaexistsgr` |
| Characters within text | `inserttextgr` direct | `textset->length` | rightshift = 0 always | No (sequential) |

The `depth` variable is the clearest expression of level-specific baptism logic: it encodes how many tumbler digits must separate a parent address from its children at that level of the hierarchy. `depth=1` for same-level creation, `depth=2` for cross-level creation. Atom-level creation abandons `depth` entirely and switches to `atomtype`-driven logic with a mandatory parent-existence guard that no other level carries.

---

## Question 12 [gregory]

> Can two concurrent sessions race to baptize the same position, and if so, does the single-threaded event loop serialization fully prevent duplicate baptism, or is there additional guarding?

### Gregory's Answer

## KB Synthesis

**The single-threaded event loop fully prevents racing. No additional guarding exists or is needed.**

## Analysis

**What baptism is architecturally**

Baptism allocates a new tumbler address by writing an orgl entry to the granfilade via `createorglingranf` → `findisatoinsertnonmolecule`. The allocation queries the granfilade tree for the highest existing address under the parent, then increments — a stateless query-and-increment [SS-ADDRESS-ALLOC Finding 0061].

**Why two sessions cannot race**

[INV-SEQUENTIAL-DISPATCH] and [INV-ATOMICITY] are the decisive facts. The `bed.c` event loop calls `xanadu(&task)` for one request at a time. The entire operation — request parsing, all state mutations, response transmission, memory cleanup — runs to completion before `select()` returns for the next file descriptor. There are no threads, no preemptive signal handlers modifying shared state, and no yield points within an operation.

From Finding 0042:
> I-address allocation via `findisatoinsertgr()` uses a global search-and-increment to find fresh addresses. **This is safe without locking because the single-threaded event loop guarantees no concurrent allocations.**

**The allocation function is stateless with respect to sessions**

[SS-ADDRESS-SPACE Finding 0061] confirms the allocation function is `next_iaddr(granf) = max_iaddr(granf) + 1` — a pure function of granfilade state with no session-local counter. When session B executes after session A, `findpreviousisagr` will find A's newly allocated address in the tree and increment past it. There is no window between "find max" and "write new entry" because the entire operation is atomic.

**No additional guarding exists**

[PRE-CONCURRENT-INSERT] notes that *unsafe* concurrent insertions *would* corrupt shared pointers and `numberofsons` counters — confirming that the serialization is the *sole* protection mechanism, not one layer among several. There are no mutexes, no optimistic concurrency checks, no address reservations. The architecture trusts the event loop entirely.

**Summary**

| Concern | Answer |
|---|---|
| Can two sessions race to baptize the same position? | No — sequential dispatch prevents any interleaving |
| Is the event loop serialization sufficient? | Yes — it is the only mechanism and it is complete |
| Is there additional guarding (locks, reservations, etc.)? | No — none exists, none is needed given single-threaded dispatch |

---

## Code Exploration

Now I have everything I need. Let me compile the full answer.

---

## Can Two Sessions Race to Baptize the Same Position?

### The Event Loop: Run-to-Completion Serialization

`bed.c:103–148` is the entire event loop:

```c
for (;;) {
    // ...
    inputfds2 = inputfds;
    if (select(nfds+1, &inputfds2, 0, 0, &timeout) < 0) { ... }
    else {
        for (i = 0; i <= nfds; i++) {           // bed.c:118
            if ((1<<i) & inputfds2) {
                user = fdtoplayer[i];
                task.inp = player[user].inp;
                task.outp = player[user].outp;
                task.account = player[user].account;
                // ...
                xanadu(&task);                   // bed.c:128
            }
        }
    }
```

`xanadu()` at `bed.c:153–172` is fully synchronous:

```c
int xanadu(typetask *taskptr) {
    // ...
    if (getrequest(taskptr, &request)) {
        (*requestfns[request])(taskptr);         // bed.c:162 — dispatch to handler
        sendresultoutput(taskptr);
    }
    tfree(taskptr);
}
```

The process is **single-threaded**. `select()` is the only inter-session switch point, and it only switches **between complete requests** — never within one. When `xanadu()` returns at `bed.c:128`, the entire request handler has finished.

---

### The "Baptism" Sequence: Read-Compute-Write

The term "baptism" does not appear in the source code. The concept maps directly to tumbler address assignment during object creation. The canonical path is:

**`docreatenewdocument()` → `createorglingranf()` → `createorglgr()` → `findisatoinsertgr()` → `findisatoinsertnonmolecule()` → `insertseq()`**

#### Step 1: Hint seeding

`do1.c:239`:
```c
makehint(ACCOUNT, DOCUMENT, 0, &taskptr->account, &hint);
return (createorglingranf(taskptr, granf, &hint, isaptr));
```

The caller's account tumbler becomes the address-space hint.

#### Step 2: Address computation

`granf2.c:203–242`, `findisatoinsertnonmolecule()`:

```c
findpreviousisagr((typecorecrum*)fullcrumptr, &upperbound, &lowerbound); // granf2.c:217 — READ
// ...
if (iszerotumbler(&lowerbound) || !lowerbound_under_hint) {
    tumblerincrement(&hintptr->hintisa, depth, 1, isaptr);               // granf2.c:237 — COMPUTE (first child)
} else {
    tumblertruncate(&lowerbound, hintlength + depth, isaptr);            // granf2.c:239 — COMPUTE (next sibling)
    tumblerincrement(isaptr, tumblerlength(isaptr)==hintlength?depth:0,1,isaptr); // granf2.c:240
}
```

This is a **read-highest / increment / return** pattern — a classic check-then-act.

#### Step 3: Atomic insertion

`granf2.c:117–126`, `createorglgr()`:

```c
if (!findisatoinsertgr((typecuc*)fullcrumptr, hintptr, isaptr))          // granf2.c:117 — READ+COMPUTE
    return FALSE;
// ...
insertseq((typecuc*)fullcrumptr, isaptr, &locinfo);                      // granf2.c:125 — WRITE
```

The computed address is immediately committed to the granfilade in the same synchronous call. There is no intermediate "pending" state.

---

### Can Two Sessions Collide?

**No, and here is why.**

In a multi-threaded or async system, the sequence at `granf2.c:217–240` would be a TOCTOU hazard: session A reads the highest address, session B reads the same highest address, both compute the same next address, both write.

But this system has no threads and no async yields. The call chain:

```
xanadu() [bed.c:162]
  → (*requestfns[request])(taskptr)      // e.g. docreatenewdocument
    → createorglingranf()                // granf1.c
      → createorglgr() [granf2.c:111]
        → findisatoinsertgr() [granf2.c:130]
          → findisatoinsertnonmolecule() [granf2.c:203]   // READ
        → insertseq() [granf2.c:125]                      // WRITE
```

…runs to completion without ever returning to the `select()` loop. Session B cannot be scheduled until `xanadu()` for session A has returned at `bed.c:128`. By that time, session A's address is already inserted in the granfilade.

One subtlety: the inner `for` loop at `bed.c:118–142` iterates over **all fds ready in one `select()` pass**. If sessions A and B are both ready simultaneously, they are processed one after the other within the same loop iteration — A's `xanadu()` completes before B's begins. This is still fully serialized.

---

### Is There Additional Guarding?

**No additional guarding exists, and none is needed.**

- There are no mutexes, semaphores, or atomic compare-and-swap operations anywhere in the baptism path.
- There is no duplicate-address check after insertion.
- There is no "did someone else take this address between my read and write?" guard.

The design places **total reliance** on the single-threaded event loop as the sole serialization primitive. This is correct by construction — the invariant "only one request executes at a time" is enforced structurally by the `select()`-then-sequential-dispatch loop at `bed.c:103–148`.

If the process were ever made multi-threaded or given async handlers that could yield mid-request, `findisatoinsertnonmolecule`'s read-compute-write would become a genuine race with no protection.

---

### Summary

| Property | Evidence |
|---|---|
| Single-threaded process | `bed.c:47` `int main(void)` — one process, no `fork`/`pthread` |
| Single-threaded event loop | `bed.c:128` `xanadu(&task)` called synchronously in inner for-loop |
| Address assignment is synchronous | `granf2.c:117–125`: `findisatoinsertgr` + `insertseq` in one call, no I/O between them |
| No additional guards | No mutex/semaphore in `granf2.c`, `granf1.c`, or `do1.c` |
| Edge case: two fds ready simultaneously | Still serialized by `bed.c:118–142` inner for-loop — A completes before B starts |

**Two concurrent sessions cannot race to baptize the same position. The single-threaded event loop provides complete serialization. There is no additional guarding because none is required by the architecture.**
