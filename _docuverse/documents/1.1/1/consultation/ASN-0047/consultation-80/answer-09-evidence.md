## Question 9 [evidence]

> Does udanax-green's procedural distinction between `docreatenewdocument` and `docreatenewversion` correspond to different K.δ sub-cases (k=0 vs k=1), and which procedure does the implementation characterize as "fork"?

## KB Synthesis

The KB addresses the procedural distinction partially but does not use "K.δ sub-cases" notation or the word "fork" for either procedure.

## What the KB does establish

**Address allocation is the structural discriminator** [SS-VERSION-ADDRESS, Finding 0032]:

- `docreatenewversion` uses `makehint(DOCUMENT, DOCUMENT, depth=1)` → child address. Doc at `1.1.0.1.0.1` yields version at `1.1.0.1.0.1.1`. No `.0.` boundary is crossed.
- New document creation uses `makehint(ACCOUNT, DOCUMENT, depth=2)` → sibling address. Yields `1.1.0.1.0.2` under the same account. One `.0.` boundary is crossed.

**Content copy semantics also differ** [ST-VERSION-CREATE, Finding 0032]:

- `docreatenewversion` is atomic: allocate orgl, retrieve vspanset, `docopyinternal` in one handler invocation — no observable intermediate state.
- CREATEDOCUMENT + COPY is non-atomic: empty document exists as an intermediate state.

**Ownership-sensitive branching** [SS-VERSION-ADDRESS, Finding 0068]:

When the user does NOT own the source document, `docreatenewversion` falls back to `makehint(ACCOUNT, DOCUMENT, depth=2)` — identical to new-document allocation. Owned versions produce child addresses; unowned versions produce account-sibling addresses.

## What is not answerable from the KB

The KB contains no mention of "K.δ sub-cases," k=0 vs k=1 formalism, or the label "fork" applied to either procedure. Whether the implementation or its documentation characterizes one of these as a "fork" cannot be determined from the entries above.

---

## Code Exploration

Now I have everything I need. Here is the complete answer.

---

## `docreatenewdocument` vs `docreatenewversion`: K.δ Sub-Cases and the "Fork" Label

### 1. The Implementation Vocabulary

The C source uses no theoretical notation (no K.δ, k=0/k=1, or "sub-case"). The distinction is encoded structurally through the `typehint` system (`do2.c:78–84`, `xanadu.h:148–153`) and a single depth computation in the allocator.

---

### 2. `docreatenewdocument` — No Ancestor (k=0 analog)

```c
// do1.c:234-241
bool docreatenewdocument(typetask *taskptr, typeisa *isaptr)
{
  typehint hint;
  bool createorglingranf();
    makehint (ACCOUNT, DOCUMENT, 0, &taskptr->account, &hint);
    return (createorglingranf (taskptr, granf, &hint, isaptr));
}
```

- `makehint(ACCOUNT, DOCUMENT, ...)` sets `supertype=ACCOUNT(2)`, `subtype=DOCUMENT(3)`.
- In `findisatoinsertnonmolecule` [granf2.c:209]:  
  `depth = (hintptr->supertype == hintptr->subtype) ? 1 : 2;`  
  → `(2 == 3) ? 1 : 2` → **depth = 2**
- The anchor tumbler is `taskptr->account`. The allocator crosses **two** `.0.` field boundaries from the account to reach the document level: first child is `account.0.1` [granf2.c:237].
- No content is copied. The new orgl (enfilade node) is created empty via `createorglgr` [granf2.c:111–128].

There is no ancestor document — the new document is a **root entry under the account**.

---

### 3. `docreatenewversion` — One Ancestor (k=1 analog)

```c
// do1.c:260-299
bool docreatenewversion(typetask *taskptr, typeisa *isaptr,
                        typeisa *wheretoputit, typeisa *newisaptr)
{
  ...
  if (tumbleraccounteq(isaptr, wheretoputit) && isthisusersdocument(isaptr)) {
      makehint (DOCUMENT, DOCUMENT, 0, isaptr/*wheretoputit*/, &hint);   // Sub-case A
  } else {
      /* This does the right thing for new version of someone else's document, as it
         duplicates the behavior of docreatenewdocument */
      makehint (ACCOUNT, DOCUMENT, 0, wheretoputit, &hint);              // Sub-case B
  }
```

**Sub-case A (own document):**

- `makehint(DOCUMENT, DOCUMENT, ...)` sets `supertype=DOCUMENT(3)`, `subtype=DOCUMENT(3)`.
- `depth = (3 == 3) ? 1 : 2` → **depth = 1** [granf2.c:209]
- Anchor is `isaptr` — the **original document itself**. The allocator crosses only **one** `.0.` field boundary, producing an address like `original.0.1` — a child of the original document in the address space.
- Confirmed by finding 0007: "Original: `1.1.0.1.0.1` → Version: `1.1.0.1.0.1.1`"
- Content is then cloned: `doretrievedocvspanfoo` retrieves the original's vspan [do1.c:281], `docopyinternal` copies it into the new doc [do1.c:293].

**Sub-case B (someone else's document):**

- Falls back to `makehint(ACCOUNT, DOCUMENT, ...)` — **identical hint to `docreatenewdocument`**, as the comment at [do1.c:273–274] explicitly states: *"duplicates the behavior of docreatenewdocument"*.
- depth = 2, allocates under `wheretoputit` (the calling user's account).
- Content is still copied from the source document — address allocation is k=0, but content inheritance is k=1. This is a hybrid not cleanly captured by a binary k distinction.

---

### 4. The Depth Encoding Summarized

| Call site | `makehint` args | depth | Address relation |
|-----------|----------------|-------|-----------------|
| `docreatenewdocument` | `ACCOUNT, DOCUMENT` | 2 | child of account |
| `docreatenewversion` (own doc) | `DOCUMENT, DOCUMENT` | 1 | child of document |
| `docreatenewversion` (other's doc) | `ACCOUNT, DOCUMENT` | 2 | child of account |

Finding 0021 (address-allocation-mechanism.md) documents this table directly.

---

### 5. Which Procedure Is Called "Fork"?

**The word "fork" does not appear anywhere in the C source** — not in `do1.c`, `granf2.c`, `fns.c`, `bert.c`, or any other `.c` or `.h` file. The grep across the entire backend returns zero matches.

"Fork" appears only in `docs/tumbler-technical.md:55`:

> Any digit can "fork" into sub-digits: `2 → 2.1 → 2.1.3 …`

That document lists "Documents spawning versions" as one instance of forking [tumbler-technical.md:67]. Structurally, `docreatenewversion` Sub-case A is the implementation of that pattern: depth=1 from `makehint(DOCUMENT, DOCUMENT, ...)` causes the allocator to produce an address that is literally a sub-digit of the ancestor document's address. `docreatenewdocument` does not fork a document; it creates a new root entry two levels beneath the account — closer to what tumbler-technical.md would call "Accounts spawning sub-accounts" (except the new entity is a document, not an account).

---

### 6. Does This Correspond to K.δ Sub-Cases?

The K.δ notation is not present in the implementation. If we map it onto the code:

- **k=0 (no document ancestor):** `docreatenewdocument` — `makehint(ACCOUNT, DOCUMENT)`, depth=2, allocates under account, empty content.
- **k=1 (one document ancestor):** `docreatenewversion` sub-case A — `makehint(DOCUMENT, DOCUMENT)`, depth=1, allocates under ancestor document, content copied from ancestor.

The binary `depth = (supertype == subtype) ? 1 : 2` switch at [granf2.c:209] is the implementation's mechanical encoding of exactly this distinction. Sub-case B of `docreatenewversion` is a mixed case (k=0 address allocation, k=1 content inheritance) with no clean mapping.

The implementation does **not** assign the label "fork" to either procedure. If any routine corresponds to the theoretical "fork" operation (a document spawning a child-addressed version), it is `docreatenewversion` Sub-case A exclusively.
