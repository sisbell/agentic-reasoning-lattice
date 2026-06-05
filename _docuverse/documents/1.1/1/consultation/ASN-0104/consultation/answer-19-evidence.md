## Question 19 [evidence]

> Across the INV-ENFILADE-CONFLUENCE property, is a read by V-address guaranteed to return identical bytes regardless of the insertion order that produced the current tree shape, and does incontextlistnd participate in ordering the returned content?

## KB Synthesis

Yes on both counts, but through different mechanisms depending on enfilade type.

## Read-by-V-address and Insertion Order

For POOM (2D) reads, identical content is returned regardless of the physical tree shape produced by any insertion sequence. [INV-ENFILADE-QUERY-INDEPENDENCE] states explicitly: "Different insertion orderings produce different tree shapes (sibling ordering, split points, disk layout) but identical query results." [INV-ENFILADE-CONFLUENCE] extends this to concurrent additions: `add(add(σ, E1), E2)` and `add(add(σ, E2), E1)` produce the same `retrieve`/`retrieveinspan` results — confluence holds at the abstraction boundary, not the physical level.

This is reinforced by [INV-IADDR-IMMUTABILITY] and [INV-CONTENT-IMMUTABILITY]: once V→I mappings exist in the POOM and I-addresses are written to the granfilade, content at those addresses is immutable. Tree restructuring (splits, rebalances per [SS-ENFILADE-TREE]) rearranges crums but never changes what logical V-address maps to what I-address, nor what bytes live at that I-address.

The one caveat: confluence and tree-structure independence are properties of the query layer. The *logical* V→I state still depends on the *operation* sequence — INSERT "A" then INSERT "B" at the same position gives "BA" (LIFO semantics per [SS-ADDRESS-SPACE]), not "AB". What insertion order cannot change is the bytes returned for a *given* V→I mapping state.

## `incontextlistnd` and Result Ordering

Yes, `incontextlistnd` is the primary ordering mechanism for 2D enfilade (POOM) retrieval. [INV-RETRIEVAL-V-SORTED] describes it precisely: as `findcbcinarea2d` traverses the B-tree and discovers leaf contexts in tree-sibling order (which may not match V-order due to diagonal rebalancing per [ST-REBALANCE-2D]), `incontextlistnd` performs insertion-sort by `totaloffset.dsas[index]` — the left V-boundary — inserting each discovered context into a sorted linked list. The result is always V-ascending, independent of discovery order.

[INV-RETRIEVAL-TREE-INDEPENDENCE] formalizes the consequence: "The V-ordering of retrieval results is independent of the internal B-tree structure." Split/rebalance operations (which use diagonal ordering per [SS-ENFILADE-TREE]) do not affect result ordering because `incontextlistnd` re-sorts on every retrieval.

For 1D GRAN enfilade reads, the parallel function `oncontextlistseq` is used instead ([SS-CONTEXT-LIST]). It appends in traversal order rather than sorting, relying on the GRAN's structural property that sibling order reflects I-address sequence — so no re-sort is needed and traversal order *is* the correct sequential order.

---

## Code Exploration

Now I have everything I need to give a complete, cited answer. Here it is.

---

## INV-ENFILADE-CONFLUENCE: Read determinism and `incontextlistnd`'s role

### Short answer

Yes, a read by V-address returns identical bytes regardless of insertion order. `incontextlistnd` is the explicit ordering mechanism for the 2D (V→I translation) phase; it does not participate in the 1D content-retrieval phase.

---

### Full call chain

A FEBE `retrievev` request flows:

```
fns.c:retrievev()
  → do1.c:338  doretrievev(taskptr, specset, vstuffsetptr)
      → do2.c:14  specset2ispanset()          [V-spec → I-span list]
          → orglinks.c:permute()
              → orglinks.c:span2spanset()
                  → retrie.c:56  retrieverestricted()
                      → retrie.c:87  retrieveinarea()
                          → retrie.c:229  findcbcinarea2d()
                              → context.c:75  incontextlistnd()   ← PHASE 1 sort
      → granf1.c:58  ispanset2vstuffset()     [I-span → bytes]
          → granf2.c:286  ispan2vstuffset()
              → retrie.c:112  retrieveinspan()
                  → retrie.c:307  findcbcinspanseq()
                      → context.c:113  oncontextlistseq()         ← PHASE 2 append
```

There are **two distinct retrieval phases** with different ordering contracts.

---

### Phase 1 — V→I translation (POOM enfilade)

`findcbcinarea2d` [retrie.c:229] traverses POOM enfilade nodes in left-to-right sibling order (`for (; crumptr; crumptr = getrightbro(crumptr))`). For each qualifying leaf it calls:

```c
// retrie.c:262-263
context = makecontextfromcbc ((typecbc*)crumptr, (typewid*)offsetptr);
incontextlistnd (headptr, context, index1);
```

`incontextlistnd` is explicitly documented as a **sorted insert**:

```c
// context.c:74
/* put c on clist in index order */
int incontextlistnd(typecontext **clistptr, typecontext *c, INT index)
```

It calls `prologuecontextnd` to get the context's absolute offset [context.c:80], then inserts it at the correct sorted position using `whereoncontext` comparisons [context.c:90, 98-99]:

```c
// context.c:90
if (whereoncontext (clist, &grasp.dsas[index], index) < THRUME) {
    // insert at head
} else {
    for (; nextc = clist->nextcontext; clist = nextc) {
        // insert in middle when clist > address && nextc < address
    }
}
// insert at tail otherwise
```

The effect: regardless of what order `findcbcinarea2d` visits POOM leaf nodes (which depends on tree shape, which depends on insertion history), the output context list is always sorted ascending by the `index1` dimension. This is the confluence enforcement point for the 2D enfilade.

---

### Phase 2 — I-space content retrieval (granfilade, 1D)

`ispan2vstuffset` [granf2.c:286-297] calls `retrieveinspan` with I-space bounds derived from Phase 1:

```c
// granf2.c:295-297
movetumbler (&ispanptr->stream, &lowerbound);
tumbleradd(&lowerbound, &ispanptr->width, &upperbound);
context = retrieveinspan ((typecuc*)fullcrumptr, &lowerbound, &upperbound, WIDTH);
```

`retrieveinspan` [retrie.c:112] routes GRAN enfilades to `findcbcinspanseq` [retrie.c:122]. That traversal appends — it does **not** sort:

```c
// retrie.c:321-323
if (crumptr->height == 0) {
    context = makecontextfromcbc ((typecbc*)crumptr, offsetptr);
    oncontextlistseq (headptr, context);
```

`oncontextlistseq` [context.c:113-123] is a simple tail-append:

```c
// context.c:113
int oncontextlistseq(typecontext **clistptr, typecontext *c) {
    c->nextcontext = NULL;
    if (!*clistptr) { *clistptr = c; c->lastcontext = c; }
    else { (*clistptr)->lastcontext->nextcontext = c; (*clistptr)->lastcontext = c; }
}
```

No sort is needed here because the granfilade is a **1D sequential enfilade**: its tree invariant guarantees that left-to-right sibling traversal always visits leaves in ascending I-address order. The `cwid.dsas[WIDTH]` field of each internal node encodes exactly the width of its subtree's address range [retrie.c:352-353], and `findcbcinspanseq` advances its running offset with `dspadd(&localoffset, &crumptr->cwid, ...)` [retrie.c:317, 327] so it stays consistent. Tree reshaping (via `levelpush`/`levelpull`/`recombine` in `genf.c`) moves subtree pointers but does not reassign I-addresses, so traversal order is invariant to tree shape.

---

### Why confluence holds

1. **I-addresses are immutable.** Content is appended to the granfilade; existing I-positions never change. `findcbcinspanseq` always returns the same leaf nodes for the same I-span.

2. **The POOM enfilade maintains V→I mappings via `cdsp`/`cwid`.** Every insert updates these fields upward (`setwispupwards` in `genf.c:289`). Different insertion orders produce trees with different shapes but identical `cdsp`/`cwid` semantics for any given V-position.

3. **`incontextlistnd` canonicalizes context ordering post-traversal.** Because `findcbcinarea2d` may visit POOM nodes in arbitrary tree-shape-dependent order, `incontextlistnd` re-sorts the collected contexts by address before returning. The sorted list is thus independent of the traversal path.

4. **`oncontextlistseq` relies on the 1D invariant.** In the granfilade, sequential traversal is already address-order traversal; sorting would be redundant.

---

### Summary table

| Phase | Function | Ordering mechanism | Depends on tree shape? |
|---|---|---|---|
| V→I translation | `findcbcinarea2d` [retrie.c:229] | `incontextlistnd` [context.c:75] sorts by `index1` | No — sort corrects for shape |
| Content retrieval | `findcbcinspanseq` [retrie.c:307] | `oncontextlistseq` [context.c:113] appends | No — 1D invariant guarantees order |

**`incontextlistnd` participates in ordering the** *intermediate* **context list produced during V→I address translation.** It does not touch the final byte content — that is assembled by `context2vtext` [context.c:277] from the already-sorted I-span contexts. The two mechanisms together enforce INV-ENFILADE-CONFLUENCE: reads return identical bytes for any V-address regardless of the insertion sequence that produced the current enfilade tree shape.
