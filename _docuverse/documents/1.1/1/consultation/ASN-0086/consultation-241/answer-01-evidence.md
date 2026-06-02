## Question 1 [evidence]

> Does the granfilade exact-match guard (`tumblereq`, `granf2.c:37`) require a retraction's target address to already reside in the link store, or can a single operation allocate and retract a fresh address in one step?

## KB Synthesis

The KB cannot answer this question. Two reasons:

1. **"Retraction" is not a documented operation.** The KB covers INSERT, DELETE, REARRANGE, VCOPY, VERSION, CREATELINK, FOLLOWLINK, and FINDLINKS. No operation named "retract" or semantically equivalent to "allocate and retract in one step" appears in any finding.

2. **`granf2.c:37` is not described.** The KB references `granf2.c` at lines 158-181 (`findisatoinsertmolecule`), 203-242 (`findisatoinsertnonmolecule`), and 255-278 (`findpreviousisagr`), but line 37 with a `tumblereq` exact-match guard is not documented in any entry.

What the KB does establish is that the granfilade is **strictly append-only** — [INV-MONOTONIC], [INV-NO-IADDR-REUSE], [FC-GRANF-ON-DELETE] all confirm that no operation (including DELETE) removes or reuses allocated addresses. Any "retract" semantics would contradict this invariant, but whether such an operation exists or what `granf2.c:37` guards are not answerable from this KB.

---

## Code Exploration

Now I have everything I need. Let me trace the complete execution path and write the answer.

---

## Answer

### The Guard at `granf2.c:37`

```c
if (!tumblereq((tumbler*)&context->totaloffset, address)) {
    crumcontextfree(context);
    return (NULL);
}
```

`fetchorglgr` (granf2.c:22–81) calls `retrievecrums` (granf2.c:34), which invokes `findcbcseqcrum` (retrie.c:167–189). That function descends the enfilade tree, accumulating offsets as it traverses siblings, and at height 0 calls `createcrumcontext(ptr, offsetptr)` (retrie.c:187). `createcrumcontext` stores the running offset as `ret->totaloffset` (context.c:59). The guard then compares that accumulated left-boundary address against the requested address.

The cast `(tumbler*)&context->totaloffset` accesses `totaloffset.dsas[WIDTH]` — the granfilade dimension — because `typedsp` begins with its `dsas[0]` (WIDTH) member (enf.h:146).

**The guard passes if and only if the leaf found by `findcbcseqcrum` has its left boundary exactly equal to the requested address.** For a GRANORGL node (single-width, point entry), this means the node must have been inserted at exactly that address.

---

### Does a Fresh Address Satisfy the Guard?

The answer is **yes, immediately after `insertseq`** — and the `docreatelink` call sequence proves this in-source.

Trace `docreatelink` (do1.c:195–221):

**Step 1 — Allocation and insertion** (do1.c:209):
```c
createorglingranf (taskptr, granf, &hint, linkisaptr)
```
This calls `createorglgr` (granf1.c:50–55 → granf2.c:111–128):
1. `findisatoinsertgr` computes a fresh ISA and writes it to `*isaptr` (granf2.c:117).
2. `insertseq((typecuc*)fullcrumptr, isaptr, &locinfo)` physically inserts the GRANORGL crum into the in-memory granfilade tree at the allocated address (granf2.c:125).

**Step 5 — Retrieval of the just-allocated address** (do1.c:213):
```c
findorgl (taskptr, granf, linkisaptr, &link, NOBERTREQUIRED)
```
`NOBERTREQUIRED` short-circuits the bert check at bert.c:59–61:
```c
if (type == NOBERTREQUIRED) {
    return 1;   /* Random > 0 */
}
```
So `findorgl` proceeds to `fetchorglgr` (granf1.c:39). `retrievecrums` descends the same in-memory tree, now containing the freshly inserted node. For a GRANORGL crum (point-width), the leaf's left boundary equals the allocated address, so `tumblereq` returns TRUE and the guard passes.

**The critical structural fact:** `insertseq` mutates the in-memory enfilade directly and synchronously. There is no write-back delay, cache, or separate "store" that would leave the just-allocated address absent. The guard's requirement is "is this address in the granfilade tree right now?" — and `insertseq` satisfies that requirement before `fetchorglgr` is called.

---

### What Would Cause the Guard to Fail?

The guard returns NULL in two cases:

1. **Address not inserted**: If the requested ISA was never inserted via `insertseq`, `findcbcseqcrum` returns the nearest preceding leaf. That leaf's `totaloffset` won't match the requested address → guard fails (granf2.c:37–40).

2. **Address falls mid-span of a text leaf**: A GRANTEXT node spans `textlength` characters (xanadu.h). If `address` lands in the interior of a text span, `findcbcseqcrum` returns that text leaf, whose `totaloffset` is the *start* of the span — not the interior address → guard fails. `isaexistsgr` (granf2.c:244–253) uses the same `retrieve → tumblereq` pattern for exactly this purpose: to distinguish "address is the left boundary of an existing node" from "address is inside a span."

---

### Can a Single Operation Allocate and Retract a Fresh Address?

**Yes, within one compound protocol call**, but not in a single atomic step. The sequence within `docreatelink` (do1.c:195–221) is:

1. `createorglingranf` → `insertseq` — inserts the fresh address at granf2.c:125  
2. ... `tumbler2spanset`, `findnextlinkvsa`, `docopy` ...  
3. `findorgl` → `fetchorglgr` → guard at granf2.c:37 — retrieves the same address

The guard does **not** require the address to pre-date the current operation. It only requires that `insertseq` has run before `fetchorglgr` is called. Within a single `docreatelink` invocation, `createorglingranf` (step 1) guarantees this for the subsequent `findorgl` (step 3).

The distinction matters for the BERT layer: `domakelink` (do1.c:169–193) passes `WRITEBERT` instead of `NOBERTREQUIRED` to `findorgl` (do1.c:186). In that path, `checkforopen` (bert.c:52–87) would search the bert table for the fresh address — and since `createorglingranf` never calls `addtoopen`, `checkforopen` returns 0 (if the user owns the document and it's not yet opened), causing `findorgl` to fail at granf1.c:22–37. `docreatelink` avoids this by passing `NOBERTREQUIRED` (do1.c:213, with comment `/* ECH 7-1 */`).

---

### Summary

| Condition | `tumblereq` guard result |
|---|---|
| Address inserted by `insertseq` at that exact position | **PASSES** — `totaloffset` matches |
| Address never inserted (purely fresh, not yet in tree) | **FAILS** — nearest leaf's offset won't match |
| Address inside a text span (not a left boundary) | **FAILS** — text leaf's start offset differs |
| Address just allocated AND inserted in same call | **PASSES** — `insertseq` runs first, guard sees it |

The guard (`granf2.c:37`) enforces **granfilade membership** — not prior session history. A fresh address that has passed through `insertseq` satisfies it immediately. The bert open-table (`checkforopen`, bert.c:52–87) is the separate layer that enforces session-level document ownership, and `docreatelink` explicitly bypasses it for the newly created link via `NOBERTREQUIRED` (`do1.c:213`).
