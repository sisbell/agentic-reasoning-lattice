## Question 17 [gregory]

> Does a node have any mutable state of its own (e.g., a node-level counter, capability list, or configuration record), or is a node purely an address prefix whose existence is implied by the presence of accounts and documents beneath it?

## KB Synthesis

Not fully answerable from the KB.

The KB provides partial evidence but no definitive answer about whether nodes carry their own mutable state.

**What the KB does say:**

Nodes appear in the address hierarchy as the outermost prefix component. [SS-TUMBLER, Finding 0001] describes the docuverse address convention as `Node.0.User.0.Doc.0.Element` — e.g., `1.1` is a node, `1.1.0.2` is an account under that node, `1.1.0.2.0.1` is a document under that account.

[SS-ADDRESS-SPACE, Finding 0021] shows that the `makehint` dispatch table includes a `NODE | NODE | depth=1` case, meaning node-under-node allocation uses the same `findisatoinsertnonmolecule` mechanism as version-under-document and document-under-account allocation. This implies node addresses are allocated and tracked in the granfilade hierarchy just as document addresses are.

**What the KB does not say:**

The KB never describes a node orgl with its own POOM, content enfilade, link subspace, or any mutable state. `createorglingranf` is described as "used for documents and links" [SS-GRANF-OPERATIONS], with no mention of node orgls. No finding examines what, if anything, resides at a bare node address — whether it is a full orgl entry or simply a numeric prefix implied by the child addresses beneath it.

**Bottom line:** The KB establishes that nodes exist as address-space entities whose child-address allocation is tracked in the granfilade, but does not reveal whether they have their own orgl records with independent mutable state, or whether they are purely implicit address prefixes whose "existence" is inferred from the presence of accounts and documents beneath them. That question is not answerable from the KB as it stands.

---

## Code Exploration

I now have everything needed to give a definitive, source-grounded answer.

---

## Does a node have mutable state of its own?

**Short answer: No. A node is purely an address prefix. It carries no mutable state — no counter, no capability list, no configuration record — beyond a tumbler and an (empty) POOM enfilade allocated in the granfilade.**

---

### What the code actually shows

#### 1. Node creation allocates a tumbler and an empty POOM

`docreatenode_or_account` [do1.c:243–258]:

```c
bool docreatenode_or_account(typetask *taskptr, typeisa *isaptr) {
  typeisa isa;
  typehint hint;
  tumblercopy(isaptr, &isa);
  makehint(NODE, NODE, 0, &isa, &hint);           // hint: supertype=NODE, subtype=NODE
  result = createorglingranf(taskptr, granf, &hint, &isa);
  if (result) tumblercopy(&isa, isaptr);
  return result;
}
```

`createorglingranf` → `createorglgr` [granf2.c:111–128]:

```c
bool createorglgr(..., typehint *hintptr, typeisa *isaptr) {
  if (!findisatoinsertgr(fullcrumptr, hintptr, isaptr)) return FALSE;
  locinfo.infotype = GRANORGL;
  locinfo.granstuff.orglstuff.orglptr = createenf(POOM);   // empty POOM
  locinfo.granstuff.orglstuff.orglincore = TRUE;
  locinfo.granstuff.orglstuff.diskorglptr.diskblocknumber = DISKPTRNULL;
  insertseq(fullcrumptr, isaptr, &locinfo);
  return TRUE;
}
```

Everything stored for a node is: a tumbler address key + a `typegranorgl` record (`orglptr`, `diskorglptr`, `orglincore`). That is the same record type written for a document [wisp.h:88–92]. There is no separate node-specific data structure.

#### 2. The `typehint` is transient — it guides address placement, nothing more

`typehint` [xanadu.h:148–153]:

```c
typedef struct {
  INT supertype;
  INT subtype;
  INT atomtype;
  typeisa hintisa;
} typehint;
```

`NODE 1`, `ACCOUNT 2`, `DOCUMENT 3` [xanadu.h:140–142] are constants used only inside `findisatoinsertgr` [granf2.c:130–156] to decide which region of the tumbler address space to allocate into. After `createorglgr` returns the hint is gone; nothing about it persists in the granfilade leaf.

#### 3. No `struct node` exists anywhere in the codebase

A search across all headers confirms this. The only node-related type is:
- `NODEID 4` [xanadu.h:30] — an item type tag used in set operations, not a node-entity struct
- `typeboolsetnode` [xanadu.h:91–95] — a boolean-set operation node (linked-list node), completely unrelated to the Xanadu node concept

#### 4. BERT tracks documents, not nodes

The `bertentry` struct [bert.c:13–19]:

```c
typedef struct {
  int connection;
  tumbler documentid;
  char created, modified;
  int type;
  int count;
} bertentry;
```

`checkforopen` [bert.c:52–87] is called with a tumbler to see if a document is open. Nodes never appear as the subject of a BERT open/close. There is no parallel BERT-style table for node state.

#### 5. Access control is derived purely from tumbler prefix, not from a node record

`isthisusersdocument` [socketbe.c:197–200]:

```c
int isthisusersdocument(tumbler *tp) {
  return tumbleraccounteq(tp, &(player[user].account));
}
```

`tumbleraccounteq` [tumble.c:38–53] compares whether the account-prefix portion of a tumbler matches the current user's account tumbler. Ownership is encoded structurally in the address itself — not in any per-node record. A node is "owned" by whichever account contains its address prefix, and that is the account's address, not any stored node metadata.

---

### Summary

| Question | Answer | Evidence |
|---|---|---|
| Does a node have a `struct` of its own? | No | No `struct node` in any `.h` file |
| What is stored when a node is created? | A tumbler address + an empty POOM in the granfilade | `createorglgr` [granf2.c:111–128] |
| Is that representation different from a document's? | No — same `GRANORGL` record type | `wisp.h:88–92`, `granf2.c:119` |
| Does a node have its own capability list? | No | Access control uses `tumbleraccounteq` only |
| Does a node have BERT (open/close) state? | No | `bertentry.documentid`; no node-equivalent |
| Is node existence explicitly tracked? | Only as an address in the granfilade | `createorglgr` inserts into granf |

A node is purely an **address prefix** in the tumbler space. Its only physical manifestation is a granfilade leaf keyed by its tumbler, holding an empty POOM. Everything that would make a node "exist" in a richer sense — accounts, documents, links — is inferred from the presence of sub-addresses beneath it. The `NODE` constant is a routing tag used at creation time to choose the right address sub-range; it leaves no trace in the stored record.
