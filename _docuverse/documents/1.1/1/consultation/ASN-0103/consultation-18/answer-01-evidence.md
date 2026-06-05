## Question 1 [evidence]

> When the implementation creates an account, does it activate/initialize that account's document sub-allocator (so the first CREATENEWDOCUMENT draws from an already-live allocator), or is the document allocator brought into being only at first document creation?

## KB Synthesis

The KB contains no description of an account creation operation that writes to the granfilade. Based on what is documented, the allocator is **lazy — it comes into being at first document creation**.

The mechanism is stateless query-and-increment against the single global granfilade tree [SS-ADDRESS-ALLOC / Finding 0021]:

1. `findisatoinsertnonmolecule` computes an upper bound: `tumblerincrement(account_isa, depth-1, 1)` — the next sibling of the account.
2. It calls `findpreviousisagr` to find the highest existing address below that bound.
3. **If nothing is found under the account prefix**, the first child is synthesized directly as `account_isa.0.1` — no prior initialization entry is required.
4. On subsequent calls, step 2 finds the previous high-water mark and increments from it.

Crucially, the KB documents the `account()` command as a **per-session state change only** — it sets the namespace context for the session but does not write anything to the granfilade [FC-SESSION-ACCOUNT-ISOLATION, SS-SESSION-STATE]. There is no granfilade-modifying "account create" operation listed anywhere in the operation classification tables [FC-GRANF-ON-VERSION, FC-GRANF-ON-DELETE].

The global granfilade is described as a single flat tree with no per-account sub-structure [SS-ADDRESS-ALLOC / Finding 0021]: `"The entire granf is a single flat tree; the allocation algorithm enforces hierarchical structure by bounding searches to the parent's address range."` There is nothing to pre-initialize.

**What the KB cannot answer:** It does not describe whether a `CREATEACCOUNT` or analogous operation exists at the protocol level that *does* write an account node into the granfilade as a placeholder. The KB simply never mentions such an operation. If one exists and pre-populates an account entry, the query in step 2 above would find it and proceed from there rather than using the first-child fallback — but the observable behavior of document allocation would be identical.

---

## Code Exploration

I now have all the code needed for a complete answer.

---

## Account Creation vs. Document Allocator Initialization

**Short answer:** The document allocator (a POOM enfilade, the document's orgl) is brought into being only at document creation time — not at account creation. Account creation creates its own independent POOM orgl for the account node's granfilade slot, but this is structurally separate from and plays no role in document allocation.

---

### System Startup

`initmagicktricks()` [`entexit.c:19`] creates two global enfilades — and only two:

```c
granf = (typegranf) createenf (GRAN);   // entexit.c:44
spanf = (typespanf) createenf (SPAN);   // entexit.c:45
```

There is no per-account or per-document sub-allocator initialized at startup. The default account tumbler `1.1.0.1` is set in the task struct at `be.c:88`, but this is just a tumbler value — no allocator structure is created.

---

### Account Creation (`CREATENODE_OR_ACCOUNT`)

Call chain:

1. `createnode_or_account()` [`fns.c:375`]  
2. → `docreatenode_or_account()` [`do1.c:243–258`]  
3. → `makehint(NODE, NODE, 0, &isa, &hint)` [`do1.c:251`] — supertype=NODE(1), subtype=NODE(1)  
4. → `createorglingranf()` → `createorglgr()` [`granf2.c:111`]

Inside `createorglgr()`:

```c
if (!findisatoinsertgr ((typecuc*)fullcrumptr, hintptr, isaptr))   // granf2.c:117
    return (FALSE);
locinfo.infotype = GRANORGL;
locinfo.granstuff.orglstuff.orglptr = createenf (POOM);            // granf2.c:120
reserve ((typecorecrum*)locinfo.granstuff.orglstuff.orglptr);      // granf2.c:121
locinfo.granstuff.orglstuff.orglincore = TRUE;
locinfo.granstuff.orglstuff.diskorglptr.diskblocknumber = DISKPTRNULL;
insertseq ((typecuc*)fullcrumptr, isaptr, &locinfo);               // granf2.c:125
rejuvinate ((typecorecrum*)locinfo.granstuff.orglstuff.orglptr);   // granf2.c:126
```

`createenf(POOM)` at `granf2.c:120` does create a live POOM enfilade — but this POOM is the orgl for the **account node's own slot** in the global granfilade (`granf`). It is a structural entry for the account node itself. It is not wired up as the allocator for subsequent documents.

---

### Document Creation (`CREATENEWDOCUMENT`)

Call chain:

1. `docreatenewdocument()` [`do1.c:234–241`]  
2. → `makehint(ACCOUNT, DOCUMENT, 0, &taskptr->account, &hint)` [`do1.c:239`]  
   — supertype=ACCOUNT(2), subtype=DOCUMENT(3), hintisa = account tumbler  
3. → `createorglingranf()` → `createorglgr()` [`granf2.c:111`]

Inside `createorglgr()`, the exact same code path executes:

- `findisatoinsertgr()` [`granf2.c:130`]: since `subtype == DOCUMENT` (not ATOM), it dispatches to `findisatoinsertnonmolecule()` [`granf2.c:203`], which scans `granf` for the highest existing ISA under the account tumbler and increments to allocate the next document ISA. **This search runs over the global granfilade — there is no per-account index to consult.**
- `createenf(POOM)` [`granf2.c:120`]: **Creates a brand-new POOM enfilade for this document's orgl — allocated fresh at this moment.**
- `insertseq(granf, isaptr, &locinfo)` [`granf2.c:125`]: Inserts the new document entry into the global granfilade.

`createenf(POOM)` [`credel.c:492`] builds a two-node apex tree (height-1 `typecuc` apex + height-0 leaf `type2dcbc`) from scratch:

```c
fullcrumptr = (typecuc *) createcrum(1, enftype);     // credel.c:497
adopt(ptr = createcrum(0, enftype), SON, ...);         // credel.c:501
```

No pre-existing structure is reused.

---

### The Relationship between Account Orgl and Document Orgl

Both account creation and document creation call the identical `createorglgr()` function. The only difference is the hint:

| Operation | `makehint` call | Hint interpretation |
|---|---|---|
| `CREATENODE_OR_ACCOUNT` | `makehint(NODE, NODE, 0, &isa, &hint)` | depth=1, allocate top-level slot |
| `CREATENEWDOCUMENT` | `makehint(ACCOUNT, DOCUMENT, 0, &account, &hint)` | depth=2, allocate under account ISA |

Each call to `createorglgr()` always invokes `createenf(POOM)` — creating an independent POOM orgl for that slot. The account's POOM is for the account node; the document's POOM is for the document. Neither is derived from the other, and neither is pre-allocated by the other.

The document's POOM orgl is subsequently retrieved (not re-created) by `findorgl()` [`granf1.c:17`] → `fetchorglgr()` [`granf2.c:22`] whenever text insertion, link insertion, or retrieval operations need the document's internal structure. Text positions are stored as GRANTEXT entries directly in the global granfilade under the document's ISA range via `inserttextgr()` [`granf2.c:83`], not inside the POOM orgl itself — the POOM orgl tracks the document's virtual structure (v-space) separately.

---

### Conclusion

The document allocator (the POOM enfilade serving as a document's orgl) is **brought into being at the moment `CREATENEWDOCUMENT` is processed**, inside `createorglgr()` at `granf2.c:120`. Account creation (`CREATENODE_OR_ACCOUNT`) allocates its own independent POOM for the account's granfilade slot, but this POOM plays no role in document-ISA allocation and is not "the document sub-allocator." The first `CREATENEWDOCUMENT` call draws from a freshly constructed POOM that did not exist before that call.
