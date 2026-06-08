## Question 19 [evidence]

> When INSERT modifies a document that other documents transclude (sharing I-addresses), is the mutation confined to the target document's single `fullcrumptr`, leaving every other document's POOM and reported content unchanged?

## KB Synthesis

Yes on cross-document isolation, but INSERT touches more than just the target document's `fullcrumptr`.

## What INSERT confines to the target document's POOM

[FC-INSERT-IADDR] is the direct answer: "INSERT does not modify the I-address of any pre-existing content, in the target document or in any other document... all existing V→I mappings outside the target document are completely untouched." Each document has its own POOM tree (rooted at its own `fullcrumptr`), and [SS-POOM-MUTABILITY] confirms these trees are mutated in-place but are structurally independent — no document shares POOM nodes with another.

Within the target POOM, [ST-INSERT / Finding 0054] adds a bounded-shift guarantee: only POOM entries in `[blade[0], blade[1])` shift, where `blade[1]` is the next subspace boundary — entries outside this range are untouched, including link subspace entries.

## What INSERT also modifies beyond the target POOM

INSERT is **not** confined to `fullcrumptr` alone. [ST-INSERT / Finding 0036] shows the full call chain:

1. **Granfilade** (`granf`): `inserttextingranf` allocates fresh I-addresses — a global append to the shared permascroll.
2. **Spanfilade** (`spanf`): `insertspanf(..., DOCISPAN)` creates a new DOCISPAN entry mapping the fresh I-addresses → target document.

These are global structures shared across all documents ([SS-DUAL-ENFILADE], [FC-CONTENT-SPANF-ISOLATION]).

## Effect on other documents' reported content

Zero. Since other documents' POOMs are untouched and [INV-IADDR-IMMUTABILITY] guarantees content bytes at any I-address never change, every other document's `retrieve_contents` result is identical before and after the INSERT. Transclusion relationships ([INT-TRANSCLUSION / Finding 0030]) survive unaffected because they bind to I-addresses, not V-positions.

**Summary**: INSERT confines POOM mutations to the single target document's tree (isolated from all other `fullcrumptr` trees), but also appends to the global granfilade and spanfilade — three structures touched, only one of which is per-document.

---

## Code Exploration

I now have all the source code I need. Let me compile the complete answer.

---

## Answer: INSERT Mutation Isolation in udanax-green

**Short answer: Yes.** An INSERT is completely confined to the target document's single `fullcrumptr`. No other document's POOM or reported content is touched. Here is the full trace with citations.

---

### Architecture: Two Levels, One Append-Only

Udanax-green separates content storage from document structure at two levels:

1. **Granfilade** — a global, sequential, append-only content store keyed by I-address. New text is always appended at freshly allocated I-addresses; existing I-addresses are never rewritten.

2. **POOM enfilade per document** (`orgl` / `fullcrumptr`) — maps V-addresses → I-addresses for exactly one document. Each document has its own independent POOM tree, fetched by ISA.

INSERT touches both levels, but only appends to the granfilade and only modifies the target document's POOM tree.

---

### The Call Chain

#### 1. `fns.c:92` — FEBE handler

```c
void insert(typetask *taskptr)
{
    (void) getinsert(taskptr, &docisa, &vsa, &textset);
    putinsert(taskptr);
    if (!doinsert(taskptr, &docisa, &vsa, textset))  /* line 92 */
        ...
}
```

`docisa` is the target document's tumbler ISA. It is passed down every subsequent call.

---

#### 2. `do1.c:117–119` — `doinsert`

```c
makehint(DOCUMENT, ATOM, TEXTATOM, docisaptr, &hint);   /* line 117 */
ret = (inserttextingranf(taskptr, granf, &hint, textset, &ispanset)
    && docopy(taskptr, docisaptr, vsaptr, ispanset)      /* line 119 */
);
```

Two sequential operations:

- `inserttextingranf` — allocates new I-addresses in the granfilade and writes the text bytes there. The hint embeds `docisaptr` so the allocator (`findisatoinsertmolecule`, `granf2.c:158–181`) knows which account's I-address sub-space to use. Existing I-addresses are untouched; `insertseq` is strictly append.
- `docopy` — records the V→I mapping in the target document's POOM.

---

#### 3. `do1.c:53–65` — `docopy`: the document is chosen here and only here

```c
bool docopy(typetask *taskptr, typeisa *docisaptr, tumbler *vsaptr, typespecset specset)
{
    return (
        specset2ispanset(taskptr, specset, &ispanset, NOBERTREQUIRED)  /* line 54 */
    && findorgl(taskptr, granf, docisaptr, &docorgl, WRITEBERT)        /* line 55 */
    && acceptablevsa(vsaptr, docorgl)                                  /* line 56 */
    && insertpm(taskptr, docisaptr, docorgl, vsaptr, ispanset)         /* line 60 */
    && insertspanf(taskptr, spanf, docisaptr, ispanset, DOCISPAN)      /* line 62 */
    );
}
```

`findorgl` (`granf1.c:39`, calls `fetchorglgr` in `granf2.c:22`) resolves `docisaptr` to exactly one POOM root pointer. `docorgl` is that pointer; it is the only POOM tree handed to any subsequent call. No other document's POOM is fetched or even examined.

`insertspanf` (`spanf1.c`) similarly takes `docisaptr` as a key and updates only that document's spanfilade record.

---

#### 4. `orglinks.c:75–134` — `insertpm`: per-document POOM modification

```c
bool insertpm(typetask *taskptr, tumbler *orglisa, typeorgl orgl, tumbler *vsaptr, typesporglset sporglset)
{
    ...
    logbertmodified(orglisa, user);                             /* line 99 */
    for (; sporglset; sporglset = sporglset->xxxxsporgl.next) {
        ...
        insertnd(taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);  /* line 130 */
        tumbleradd(vsaptr, &crumwidth.dsas[V], vsaptr);
    }
    return (TRUE);
}
```

`logbertmodified(orglisa, user)` at line 99 marks only this document ISA dirty. `insertnd` at line 130 receives only `orgl` — the single POOM root returned by `findorgl` above. The loop iterates over `sporglset` (the list of I-spans being inserted), not over a list of documents.

---

#### 5. `insertnd.c:15–111` — `insertnd`: operates on one tree, root to leaf

```c
int insertnd(typetask *taskptr, typecuc *fullcrumptr, ...)
{
    ...
    switch (fullcrumptr->cenftype) {
      case POOM:
        makegappm(taskptr, fullcrumptr, origin, width);        /* line 54 */
        ...
        bothertorecombine = doinsertnd(fullcrumptr, ...);      /* line 57 */
        break;
    }
    if (bothertorecombine || ...)
        recombine(fullcrumptr);                                /* line 76 */
}
```

Every call — `makegappm`, `doinsertnd`, `recombine` — receives only the one `fullcrumptr` that was passed in. There is no loop, no table walk, no call that fetches a second document's tree.

`makegappm` (`insertnd.c:124–172`) descends into `fullcrumptr` to split crums at the insertion point. The for-loop at line 151 iterates over `findleftson(father)` — the children of one internal node inside this tree. It does not consult any other document.

---

#### 6. `insertnd.c:242–275` — `insertcbcnd`: new crums are born privately

When `insertnd` reaches a height-1 node (bottom of the POOM), it calls `insertcbcnd`:

```c
INT insertcbcnd(typecuc *father, typedsp *grasp, typewid *origin, typewid *width, type2dbottomcruminfo *infoptr)
{
    for (ptr = findleftson(father); ptr; ptr = findrightbro(ptr)) {
        if (isanextensionnd((typecbc*)ptr, grasp, origin, infoptr)) {
            dspadd(&ptr->cwid, width, &ptr->cwid, ...);  /* extend existing crum */
            ...
            return(FALSE);
        }
    }
    new = createcrum(0, (INT)father->cenftype);   /* line 260 */
    reserve(new);                                  /* line 261 */
    adopt(new, SON, (typecorecrum*)father);        /* line 262 */
    ...
    adopt(new, SON, father)
}
```

`createcrum` allocates a fresh node. `reserve` pins it in core. `adopt` wires it into the tree whose root is `fullcrumptr`. `father` was reached solely by descending from that root — it belongs to this document's tree only.

---

#### 7. `genf.c:419–520` — `adopt`: pointer surgery, no COW, no sharing

```c
int adopt(typecorecrum *new, INT relative, typecorecrum *old)
{
    ...
    if (left) {
        left->rightbro = new;              /* line 504 */
        new->leftbroorfather = left;       /* line 505 */
        new->isleftmost = FALSE;
    } else {
        father->leftson = new;             /* line 508 */
        new->leftbroorfather = (typecorecrum *)father;
        new->isleftmost = TRUE;
    }
    new->rightbro = right;                 /* line 513 */
    if (right) right->leftbroorfather = new;
    ++father->numberofsons;                /* line 519 */
}
```

`adopt` is pure pointer surgery: it links a new node into the sibling-linked tree via `leftbroorfather` / `rightbro` / `leftson`. There is no copy-on-write, no reference counting, and no way a node adopted into Document A's tree can simultaneously appear in Document B's tree. Nodes are not shared across documents.

---

### What Transclusion Actually Means

Other documents that transclude content from Document A hold a V-spec referencing Document A's ISA and a V-span. When they call `doretrievev` (`do1.c:338–346`), it calls `specset2ispanset` → `vspanset2ispanset` → `permute` → `span2spanset` → `retrieverestricted` on Document A's POOM. That is a **read-only traversal**; no write path is entered.

The transclusion is therefore **by V-address reference**, not by shared POOM node pointer. INSERT into Document A:

- Appends new bytes at new I-addresses in the granfilade.
- Shifts V-addresses in Document A's POOM to open a gap at the insertion point (this is what `makegappm` does to existing crums at `insertnd.c:162`, incrementing their `cdsp.dsas[V]` displacement).
- Adds a new POOM node mapping the new V-span → new I-span in Document A's tree.

Document B's V-spec for its transclusion of Document A still refers to the same V-span it always did. If that V-span is below the insertion point, the V→I mapping in Document A's POOM is unchanged for those addresses (only higher-V crums have their displacements shifted). If it is above the insertion point, Document B's V-span will now resolve to different V-positions within Document A — but **Document B's own POOM is not touched**, and Document B's own content is completely unchanged. The shift only affects what Document B sees when it retrieves Document A's content by V-address, which is an expected consequence of insertion.

---

### Summary of Isolation

| Layer | What INSERT does | Other documents affected? |
|-------|-----------------|--------------------------|
| Granfilade (`granf2.c:83–109`) | Appends new text at new I-addresses via `insertseq` | No — existing I-addresses are immutable |
| Target document POOM (`insertnd.c`, `orglinks.c`) | Adds new crums, shifts cdsp on existing crums after insertion point | No — each document has its own `fullcrumptr`; `findorgl` fetches exactly one |
| Spanfilade (`spanf1.c`) | Adds I-span entry keyed by `docisaptr` | No — keyed by document ISA |
| Bert table (`bert.c`) | `logbertmodified` marks `orglisa` dirty | No — other ISAs are not marked |

**The mutation is fully confined to the target document's single `fullcrumptr`.** No other document's POOM enfilade, V-address mapping, or reported content is structurally altered by an INSERT operation.
