# Revision Consultation — ASN-0002

**Review:** ASN-0002-review-2.md
**Date:** 2026-02-28 14:08

## Summary

9 REVISE items analyzed: 7 internal, 2 consulted (1 nelson, 1 gregory)

## Consultation Results

### Issue 8: Ghost address permanence is asserted but not derived

**Category:** NELSON
**Reason:** AP0 covers addresses in `dom.ispace`; AP4 covers allocation gaps. But ghost addresses occupy address-space positions assigned to servers, accounts, or documents — the permanence of those structural range assignments is a design intent question not answerable from the ASN or implementation alone.

**Nelson question:** In the tumbler address hierarchy, is the assignment of an address range to a server, account, or document intended to be permanent and irrevocable — i.e., once a range is committed to an entity, can that range never be reassigned to a different entity, even if the entity has no stored content?

**Nelson's Answer:**

## Answer: Yes — Address Range Assignment Is Permanent and Irrevocable

Nelson's design makes this clear through multiple converging lines of evidence, though he states it more as an architectural invariant than as an explicit prohibition on reassignment.

### Direct Evidence: Permanence of Addresses

The strongest direct statement:

> "New items may be continually inserted in tumbler-space while the other addresses remain valid. This means that any address of any document in an ever-growing network may be specified by a permanent tumbler address." [LM 4/19]

The word "permanent" here is unconditional. It does not say "permanent as long as content exists" — it says permanent, full stop.

### Ghost Elements: Empty Ranges Are Still Occupied

Nelson explicitly addresses the case of address ranges with no stored content:

> "While servers, accounts and documents logically occupy positions on the developing tumbler line, no specific element need be stored in tumbler-space to correspond to them. Hence we may call them ghost elements." [LM 4/23]

> "However, these elements are virtually present in tumbler-space, since links may be made to them which embrace all the contents below them." [LM 4/23]

> "It is possible to link to a node, or an account, even though there is nothing stored in the docuverse corresponding to them." [LM 4/23]

This is decisive. An address range assigned to a server or account remains "virtually present" in tumbler-space even when entirely empty. The system treats the range as occupied *conceptually* regardless of stored content. Reassignment would violate this: links made to ghost elements would break or resolve to the wrong entity.

### The Baptism Principle: Owned Numbers

From the forking mechanism:

> "The owner of a given item controls the allocation of the numbers under it." [LM 4/20]

> "One digit can become several by a forking or branching process. This consists of creating successive new digits to the right; we call these 'under' the previous digit." [LM 4/20]

Baptism is a one-way act. Nelson describes creation ("successive new digits being placed under"), never un-creation or re-baptism. The ownership tree grows; it does not restructure.

### The Tumbler Line as a Particular Tree

> "The tumbler line is an abstract representation of a particular tree." [LM 4/22]

> "The contents of the tumbler line are determined by the population of entities and relations on the tree it represents. Thus the tumbler line is not definite in the same way as the real line; the tumbler line is a flat mapping of a particular tree, finite but unlimited." [LM 4/22]

The tumbler line represents "a particular tree" — the actual historical tree of what was created. Reassigning a range would change the tree's structure retroactively, violating this identity between the tumbler line and the tree it maps.

### Structural Necessity: Why Reassignment Would Be Catastrophic

The system's fundamental guarantees depend on address permanence:

1. **Links point to I-space addresses.** If server range `1.3` were reassigned from Vendor A to Vendor B, every link in the docuverse pointing into that range would now resolve to wrong content or break entirely.

2. **Origin traceability is structural.** "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40] The I-address encodes origin. Reassignment would make traceability lie.

3. **Transclusion relies on permanent I-addresses.** Content included by reference from `1.3.X.Y` must always resolve to the original bytes. Reassignment would silently substitute different content.

4. **Ghost elements can be link targets.** If someone links to account `1.3.0.7` (a ghost element), and that range is later reassigned, the link now points to a different entity — violating link permanence.

### What About Abandoned Servers or Accounts?

Nelson does not discuss reassignment of abandoned ranges, which is itself evidence — if reassignment were contemplated, it would need extensive discussion given how many guarantees it would break.

For vendor failure, Nelson specifies orderly transition, not range reassignment:

> "Upon notice of cancellation, Storage Vendor will arrange for the orderly transition of all customer-stored materials to other Xanadu locations." [LM 5/16]

The content *migrates*; the addresses do not change. The server range remains assigned to its original position in the tree, even if a different vendor physically serves it.

### Summary

| Evidence | Source | What It Shows |
|----------|--------|---------------|
| "permanent tumbler address" | 4/19 | Addresses are permanent unconditionally |
| Ghost elements "virtually present" | 4/23 | Empty ranges are still occupied |
| Links to ghost elements valid | 4/23 | Empty ranges must remain stable for links |
| Baptism is one-way creation | 4/20 | No un-baptism or re-baptism mechanism |
| Tumbler line maps "a particular tree" | 4/22 | Tree structure is historical fact, not mutable |
| Vendor failure = migration, not reassignment | 5/16 | Physical custody changes; addresses don't |

**Once a range is committed to an entity — whether server, account, or document — that commitment is permanent and irrevocable, even if the entity contains no stored content.** This is not merely a policy choice but an architectural invariant on which permanence, link survivability, origin traceability, and transclusion all depend.

### Issue 9: CREATENEWVERSION — "does not enter `dom.ispace`" is asserted without formal grounding

**Category:** GREGORY
**Reason:** The ASN references a "document registry (a component of Σ outside ispace)" that is never defined. Formalizing the distinction between content addresses and document identity addresses, and specifying where document identities are recorded, requires evidence about the implementation's data structures beyond what the ASN currently cites.

**Gregory question:** When CREATENEWVERSION creates a new document, what data structure records the new document's existence and identity — is it a structure separate from the content store (granfilade), and what fields does that record contain?

**Gregory's Answer:**

## KB Synthesis

When CREATENEWVERSION runs, it calls `createorglingranf()` with a DOCUMENT-type hint. What comes back is a fresh **orgl** — an organization label — allocated inside the single global `granf` enfilade. There is no separate document registry or identity store; the granfilade IS the unified store for document structure, content atoms, and link orgls alike. [SS-DUAL-ENFILADE, SS-GRANF-OPERATIONS]

**What gets allocated**

The allocation dispatcher `findisatoinsertgr` routes to `findisatoinsertnonmolecule` for non-molecule (document-type) entities. That routine:

1. Computes an upper bound from the source document's ISA via `tumblerincrement(sourceISA, depth-1, 1)` — the next sibling of the source at depth=1 for an owned document.
2. Calls `findpreviousisagr` to find the highest existing child address under the source.
3. Allocates either `sourceISA.1` (first child) or `max_child + 1` (next sibling among children).

The result is a **tumbler ISA** — the version's permanent identity. For an owned document at `1.1.0.1.0.1`, the first version lands at `1.1.0.1.0.1.1`, the second at `1.1.0.1.0.1.2`, and so on. [SS-ADDRESS-ALLOC, SS-VERSION-ADDRESS, SS-ADDRESS-SPACE/Finding 0068]

**What that orgl contains**

The orgl is itself a **POOM enfilade tree** (type POOM, a 2D B-tree). Its root crum carries:

- `isapex = TRUE` — marks it as the tree root
- `height` — starts at 1 for a new tree
- `cdsp.dsas[V]` — V-dimension displacement, set to the text subspace start (position `1`) after `docopyinternal` copies the source's text
- `cwid.dsas[V]` — V-dimension width, the text extent
- `cdsp.dsas[I]` / `cwid.dsas[I]` — I-dimension displacement and width covering the shared I-address range

Bottom crums (height=0 nodes) hold the actual `(V-position → I-address)` mappings, with asymmetric tumbler precision: I-addresses use 6–9 digits, V-addresses use 2 digits. [SS-ENFILADE-TREE, SS-POOM-BOTTOM-CRUM, SS-INSERT-VWIDTH-ENCODING]

The disk loaf header wrapping each node includes `sizeofthisloaf`, `isapex`, `height`, `denftype` (POOM=2 for document orgls vs GRAN=0 for content atoms), `numberofcrums`, and a `refcount` for subtree sharing. [SS-UNIFIED-STORAGE]

**What CREATENEWVERSION does NOT do**

It allocates zero new content I-addresses. `docopyinternal` calls `insertpm` (updating the new orgl's POOM) and `insertspanf` (recording DOCISPAN entries) using the source document's existing I-addresses — sharing, not copying. The granfilade's content region is untouched. [ST-VERSION, FC-GRANF-ON-VERSION]

It also does NOT copy link subspace entries (V-position `2.x`). `doretrievedocvspanfoo` calls `retrievedocumentpartofvspanpm`, which reads only the V-dimension displacement/width from the root crum — a value that points to position `1` (the text subspace start). Link entries at `2.x` lie outside that span and are structurally excluded. [ST-VERSION-CREATE/Finding 0043, ST-VERSION-CREATE/Finding 0046]

**Summary**

The new document's existence is recorded as a POOM orgl node in the global `granf` enfilade, identified by its tumbler ISA address. That address encodes the version hierarchy directly (child of source for owned documents, child of creating account for unowned). No separate document table exists — the granfilade tree structure IS the document registry. [SS-DUAL-ENFILADE, SS-ADDRESS-SPACE/Finding 0077]

---

## Code Exploration

I now have everything I need. Here is the complete answer:

---

## What Records a New Document's Existence and Identity in CREATENEWVERSION

### Entry Point: The FEBE Handler

`createnewversion()` in `fns.c:289-300` is the FEBE protocol handler. It reads the source document ISA from the wire and calls `docreatenewversion()`:

```c
void createnewversion(typetask *taskptr)          // fns.c:289
{
  typeisa originaldocisa, newdocisa;
  ...
  getcreatenewversion (taskptr, &originaldocisa)
  && docreatenewversion (taskptr, &originaldocisa, &originaldocisa, &newdocisa))
      putcreatenewversion (taskptr, &newdocisa);   // returns the new ISA to client
```

---

### Step 1 — The Granfilade Entry: Where Existence Is Recorded

`docreatenewversion()` in `do1.c:260-299` calls `createorglingranf()` at `do1.c:277`:

```c
if (!createorglingranf(taskptr, granf, &hint, newisaptr)) {   // do1.c:277
    return (FALSE);
}
```

That thin wrapper (`granf1.c:50-55`) calls `createorglgr()` in `granf2.c:111-128`:

```c
bool createorglgr(typetask *taskptr, typegranf fullcrumptr, typehint *hintptr, typeisa *isaptr)
{
  typegranbottomcruminfo locinfo;
  ...
  if (!findisatoinsertgr ((typecuc*)fullcrumptr, hintptr, isaptr))   // granf2.c:117
      return (FALSE);
  locinfo.infotype = GRANORGL;                                        // granf2.c:119
  locinfo.granstuff.orglstuff.orglptr = createenf (POOM);            // granf2.c:120
  reserve ((typecorecrum*)locinfo.granstuff.orglstuff.orglptr);       // granf2.c:121
  locinfo.granstuff.orglstuff.orglincore = TRUE;                     // granf2.c:122
  locinfo.granstuff.orglstuff.diskorglptr.diskblocknumber = DISKPTRNULL; // granf2.c:123
  insertseq ((typecuc*)fullcrumptr, isaptr, &locinfo);               // granf2.c:125
```

This does two things:
1. **Computes the new document's tumbler address** (`*isaptr`/`*newisaptr`) via `findisatoinsertgr()` → `findisatoinsertnonmolecule()` (`granf2.c:203-242`), which walks the granfilade B-tree to find the next available address under the hint.
2. **Inserts a new bottom crum** into the granfilade B-tree via `insertseq()`, encoding the new ISA as the crum's key and the `typegranorgl` payload as its value.

The payload stored in the crum is a `typegranorgl` (`wisp.h:88-93`):

```c
typedef struct structgranorgl {        // wisp.h:88
    struct structcuc *orglptr;          // pointer to the new (empty) POOM enfilade
    typediskloafptr diskorglptr;        // disk block pointer — DISKPTRNULL (in-core)
    bool orglincore;                    // TRUE: content is in RAM
} typegranorgl;
```

The POOM enfilade itself is created empty by `createenf(POOM)` at `granf2.c:120` (`credel.c:492-516`): a two-level tree with one null-filled bottom crum.

The carrier node in the granfilade is a `typecbc` (core bottom crum, `enf.h:85-107`). Its fields of relevance are:

| Field | Type | Meaning |
|---|---|---|
| `cwid.dsas[WIDTH]` | `tumbler` | The document's ISA address (its permanent identity) |
| `cinfo.infotype` | `INT` | `GRANORGL` = 2 — marks this slot as a document orgl |
| `cinfo.granstuff.orglstuff.orglptr` | `typecuc *` | Pointer to the in-core POOM enfilade (the document's version content tree) |
| `cinfo.granstuff.orglstuff.diskorglptr` | `typediskloafptr` | Disk location of the orgl when paged out (`DISKPTRNULL` at creation) |
| `cinfo.granstuff.orglstuff.orglincore` | `bool` | Whether the orgl is currently loaded in RAM |

**The granfilade IS the content store.** The document's identity record lives inside it, not separately from it. The granfilade is a single unified B-tree that holds both raw text atoms (GRANTEXT crums) and document orgl pointers (GRANORGL crums). There is no separate document-existence registry apart from the granfilade.

---

### Step 2 — The Hint That Governs Address Assignment

Before `createorglgr()` is called, `docreatenewversion()` constructs a `typehint` at `do1.c:271-276`:

```c
typedef struct {               // xanadu.h:148
    INT supertype;             // ACCOUNT or DOCUMENT
    INT subtype;               // DOCUMENT
    INT atomtype;              // 0 (not an atom)
    typeisa hintisa;           // the parent address under which to place the new doc
} typehint;
```

Two code paths exist (`do1.c:270-276`):

- **Same account, own document**: `makehint(DOCUMENT, DOCUMENT, 0, isaptr, &hint)` — the new version is placed as a child of the original document's address (continuing a version chain under the same owner).
- **Different account, or someone else's document**: `makehint(ACCOUNT, DOCUMENT, 0, wheretoputit, &hint)` — the new version is placed under the caller's account (same behavior as `docreatenewdocument()`).

The hint controls what `findisatoinsertnonmolecule()` returns: it finds the highest existing child address under `hintisa` and increments it by one tumbler step (`granf2.c:239-241`).

---

### Step 3 — The Bert Table Entry: Session State, Not Persistent Identity

After `createorglingranf()` succeeds, `docreatenewversion()` calls `addtoopen()` at `do1.c:292`:

```c
addtoopen(newisaptr, user, TRUE, WRITEBERT);   // do1.c:292
```

`addtoopen()` inserts a `bertentry` into a separate in-memory hash table (`bert.c:29`: `static conscell *berttable[1327]`). The struct is:

```c
typedef struct {               // bert.c:13
    int connection;             // which client connection owns this open
    tumbler documentid;         // the ISA of the document
    char created;               // TRUE — newly created this session
    char modified;              // FALSE initially; set by logbertmodified()
    int type;                   // WRITEBERT
    int count;                  // 1 — reference count
} bertentry;
```

This is **separate from the granfilade** and is **transient** — it is discarded on close or crash. Its purpose is access control and session tracking: `checkforopen()` (`bert.c:52-87`) consults it before any `findorgl()` call to gate read/write access. The `created` flag is critical: if a session closes without modifying the document it created (`bert.c:173`: `status = bert->created && !bert->modified`), `deleteversion()` is called to clean it up.

---

### Summary

| What | Where | Persistent? | Fields that encode identity |
|---|---|---|---|
| `typecbc` bottom crum in the granfilade | Inside `granf` (the global `typegranf`) | Yes (written to disk) | `cwid.dsas[WIDTH]` (the ISA tumbler); `cinfo.infotype = GRANORGL`; `cinfo.granstuff.orglstuff.orglptr` (the POOM) |
| `bertentry` in `berttable[]` | Separate in-memory hash table in `bert.c` | No (session only) | `documentid` (ISA copy); `connection`; `created`; `modified`; `type`; `count` |

The granfilade entry is the document's **existence record** — there is no separate document registry. The document exists if and only if a `GRANORGL` crum is present at that ISA address in the granfilade tree. The bert table entry is a **session access-control overlay** that answers "is this document open, by whom, and for what purpose." Both structures carry the tumbler ISA (`typeisa`, aliased to `tumbler` at `xanadu.h:23`) as their identity key, and the ISA is what `putcreatenewversion()` returns to the client as proof of the new document's birth.
