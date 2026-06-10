## Question 4 [evidence]

> Does udanax-green's versioning or link machinery allow a document to have multiple direct successors, and does anything in the code prevent cyclic successor/link structures?

## KB Synthesis

## Multiple Direct Successors

Yes — a document can have arbitrarily many direct successors. The version allocation rule in `findisatoinsertnonmolecule` simply finds the highest existing child address under the source document and increments it. The resulting addresses are siblings:

```
1.1.0.1.0.1          (original)
├── 1.1.0.1.0.1.1    (first version)
├── 1.1.0.1.0.1.2    (second version, independent)
└── 1.1.0.1.0.1.3    (third version, independent)
```

[ST-CROSS-SESSION-VERSIONING] confirms this experimentally: two sessions calling `create_version(original)` receive `version_a` and `version_b` with distinct addresses, both sharing content identity with the original. [SS-VERSION-ADDRESS] Finding 0068 shows the allocation postcondition is `allocated = max_child(source_doc, granf) + 1` — purely monotonic, with no uniqueness gate that would block a second call.

The version tree is an **unbounded branching tree**, not a chain.

---

## Cyclic Successor (Version) Structures

**Prevented structurally, not by code.** There is no explicit cycle-detection guard anywhere in `docreatenewversion` or the allocation path. Cycles are prevented by an invariant of the tumbler address arithmetic:

A version's address is a **strict child** of its source: `prefix(version_addr, len(source_addr)) = source_addr` [SS-TUMBLER-CONTAINMENT, SS-VERSION-ADDRESS]. For a cycle to exist, document A would need to be a version of B (meaning A's address extends B's) while B is also a version of A (meaning B's address extends A's) — mutual prefix containment, which is impossible for distinct tumblers.

The monotonicity invariant from [INV-MONOTONIC] / Finding 0068 reinforces this: each allocation produces a strictly greater address, so address ancestry is a strict partial order with no cycles.

---

## Cyclic Link Structures

**Permitted and tested.** From [EC-LINK-TOPOLOGY] (Finding 0026), circular link topologies were explicitly exercised:

| Pattern | Result |
|---------|--------|
| A → B → C → A (3 links) | All links discoverable |
| Bidirectional A ⟷ B | Both links discoverable |
| Diamond A → B, A → C, B → D, C → D | All links discoverable |

No error, no hang, no duplicate artifacts. This is a direct consequence of how `find_links` works: it converts a query V-span to I-addresses and does a **set intersection** against the spanfilade index [SS-FIND-LINKS, INT-SPORGL-LINK-INDEX]. It never traverses the link graph — it has no path-following logic that could loop. Each call is a single bounded lookup.

[INV-LINK-PERMANENCE] and the link-space model [SS-LINK-SPACE] further explain why: links are independent objects in the spanfilade, not embedded in documents. Their topology has no effect on the storage layer's operation.

---

## Summary

| Structure | Multiple successors? | Cycles possible? | Prevented by? |
|-----------|---------------------|-----------------|---------------|
| Version tree | Yes (fan-out supported) | No | Tumbler prefix arithmetic |
| Link graph | N/A | Yes | Nothing — explicitly tested and supported |

---

## Code Exploration

I now have enough data to give a complete, code-cited answer.

---

## Does udanax-green allow multiple direct successors, and does anything prevent cyclic structures?

### 1. Versioning machinery: multiple direct successors are fully permitted

The entry point is `fns.c:289-299` (`createnewversion`), which calls `docreatenewversion` at `do1.c:260` with no guard against the same original being versioned more than once.

`docreatenewversion` allocates a new ISA by calling:

```
createorglingranf → createorglgr (granf2.c:111) → findisatoinsertgr (granf2.c:130)
  → findisatoinsertnonmolecule (granf2.c:203)
```

`findisatoinsertnonmolecule` simply finds the next available sequential ISA address under the hint and increments it:

```c
// granf2.c:235-241
if (iszerotumbler(&lowerbound) || !lowerbound_under_hint) {
    tumblerincrement(&hintptr->hintisa, depth, 1, isaptr);  // first child
} else {
    tumblertruncate (&lowerbound, hintlength + depth, isaptr);
    tumblerincrement(isaptr, tumblerlength(isaptr)==hintlength?depth:0, 1, isaptr); // next sequential
}
```

The hint is set to `DOCUMENT, DOCUMENT` at `do1.c:271`, making `depth=1` (same-type supertype==subtype path in `granf2.c:209`). Each call to `createnewversion` on the same original document `X` allocates `X.0.1`, `X.0.2`, `X.0.3`, etc. — sequential sibling ISAs under the original's address. Nothing checks for an existing successor; no counter, no sentinel, no lookup.

**Conclusion: calling `createnewversion` N times on the same document produces N independent, equally-valid successor documents.**

---

### 2. Cyclic successor structures through versioning: structurally impossible

The ISA assignment mechanism makes version cycles structurally impossible. `findisatoinsertnonmolecule` (`granf2.c:203`) always allocates an ISA that is numerically a strict child of the original. In tumbler arithmetic, a child address has a longer representation (more mantissa digits) than its parent, enforced by `tumblerincrement` at position `lastNonZero + depth` (`tumble.c:599-622`). You can never make a new version whose ISA is an ancestor of the original's ISA in the tumbler prefix hierarchy.

There is also no stored predecessor/successor graph. The `bertentry` struct at `bert.c:13-19` tracks only `{documentid, connection, created, modified, count}` — nothing about ancestry. The `typeorgl`/`typecuc`/`typecorecrum` nodes in `genf.c` are pure enfilade tree nodes with no version-ancestry pointers. The versioning relationship is *implicit in the address space hierarchy only*.

---

### 3. Link machinery: cycles are completely unguarded

`docreatelink` at `do1.c:195` (FEBE entry via `fns.c:100-112`) creates a 3-ended link by:

1. `createorglingranf` — allocate a new ISA for the link orgl
2. `docopy` — copy the link's ISA into the document's virtual space
3. `specset2sporglset` — resolve the from/to/three specsets into ispan addresses
4. `insertendsetsinorgl` — store the endpoint sets in the link's orgl
5. `insertendsetsinspanf` / `insertspanf` (`spanf1.c:15-53`) — insert the sporgl spans into the spanfilade

None of these steps check:
- Whether `fromspecset == tospecset` (self-loop)
- Whether `fromspecset` already has a link to `tospecset` (duplicate)
- Whether following the new link would complete a cycle with existing links

`insertspanf` at `spanf1.c:51` calls `insertnd(taskptr, (typecuc*)spanfptr, &crumorigin, &crumwidth, &linfo, SPANRANGE)` — a pure tree-insertion operation with no semantic validation whatsoever. `acceptablevsa` at `do2.c:110-113` also provides no real check: it unconditionally returns `TRUE`.

A link where from and to reference the same document spans, or A→B plus B→A forming a cycle, are equally valid to the backend. There is no cycle-detection pass in `findlinksfromtothreesp` (`spanf1.c:56-103`), `dofollowlink` (`do1.c:223-232`), or anywhere in the link-following path.

---

### Summary

| Question | Answer | Where |
|---|---|---|
| Can a document have multiple direct successors? | **Yes — no guard exists.** Each `createnewversion` call allocates the next sequential child ISA. | `do1.c:260`, `granf2.c:203` |
| Can version succession form a cycle? | **No — structurally impossible.** Child ISAs are always numerically deeper than parents; the address space is a strict tree. | `granf2.c:235-241`, `tumble.c:599` |
| Is predecessor/successor tracked anywhere? | **No.** Only implicit via ISA address hierarchy. | `bert.c:13-19`, `genf.c` |
| Can link structures form cycles? | **Yes — nothing prevents it.** No cycle detection at any layer of link creation, insertion, or following. | `do1.c:195-221`, `spanf1.c:15-53`, `do2.c:110-113` |
