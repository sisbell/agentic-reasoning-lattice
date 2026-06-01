## Question 1 [evidence]

> Does udanax-green's link sub-allocator (spanf / CREATELINK) only ever emit the next sibling on a home's `inc(·,0)` chain, or can it produce an off-chain child address (e.g. via a `max`-of-homed-set that is itself off-chain) — i.e. is "produced by `A_L(d)`" a hard gating precondition on link emission?

## KB Synthesis

## Link Sub-Allocator: Sibling Chain vs. Off-Chain Children

The link allocator in udanax-green **always emits the next sibling on the home document's `inc(·,0)` chain** by construction. There is no mechanism capable of producing an off-chain child address in this path.

### Mechanism

From [SS-ADDRESS-ALLOC] Finding 0065 (Essential):

The CREATELINK path calls `findisatoinsertmolecule` (the *molecule* path, not the *non-molecule* structural-allocation path used for documents/versions). The core step is:

```c
tumblerincrement(&lowerbound, 0, 1, isaptr)
// rightshift=0, increment=1
```

`rightshift=0` means "increment at the most-significant free digit," which produces the next sequential sibling — precisely the `inc(·, 0)` operation. The non-molecule path used for documents/versions uses `depth > 0` to produce child addresses (`hintisa.0.1` first child, then `.0.2` etc.); the molecule path never does. The allocator is structurally incapable of emitting a depth-increased address.

### Bounds enforcement

Two mechanisms confine emission to the canonical chain `docISA.0.2.1`, `docISA.0.2.2`, …:

1. **Upper bound scoping**: `tumblerincrement(&hintptr->hintisa, 2, LINKATOM+1, &upperbound)` restricts `findpreviousisagr` to the document's link element subspace `[docISA.0.2.x, docISA.0.3)`. This is independent of other documents' link ranges [INV-MONOTONIC].

2. **Lower-bound fallback**: If `findpreviousisagr` returns a value below `docISA.0.2.2` (nothing yet allocated), the allocator unconditionally falls back to the canonical first address `docISA.0.2.1`. This is the sentinel that ensures the chain always starts at the correct root.

Subsequent calls find the previous chain member and produce `prev + 1` at rightshift=0, yielding the strict sequence `…0.2.1`, `…0.2.2`, `…0.2.3`, … [INV-MONOTONIC], [SS-ADDRESS-ALLOC].

### Could `findpreviousisagr` return an off-chain address?

In a well-formed system, no. The only entities that write into `[docISA.0.2.1, docISA.0.3)` are CREATELINK calls on the same home document, which are themselves on-chain by this very argument. The [INV-SUBSPACE-CONVENTION] / [SS-SUBSPACE-CONVENTION] guarantee (enforced by caller convention, not storage layer) ensures text and version allocations do not contaminate the link element subspace. Document-version addresses land at `docISA.1`, `docISA.2`, … (depth-1 children via non-molecule path), never inside the element subspace [SS-ADDRESS-ALLOC] Finding 0068, [SS-ADDRESS-SPACE] Finding 0077.

If a contaminating address *did* exist in-range due to a convention violation [SS-SUBSPACE-CONVENTION], the lower-bound check only resets when the range is empty; it would not prevent `inc(off-chain, 0)` from producing a shifted-off-chain address. But [SS-SUBSPACE-CONVENTION] plus [INV-SUBSPACE-CONVENTION] jointly rule this out in the well-formed case.

### Is `A_L(d)` a hard gate?

It is **structural**, not a runtime assertion: the algorithm cannot emit off-chain children because `tumblerincrement(..., 0, 1)` produces only next-siblings and the molecule allocation path has no `depth` parameter. The bounds and fallback together ensure the range is restricted to `docISA.0.2.*`. There is no explicit `requires address ∈ A_L(d)` guard, but the emission is provably confined to the chain as a postcondition of the allocation algorithm alone — per-document, monotonically increasing, sequential sibling-only. [SS-ADDRESS-ALLOC], [SS-ADDRESS-SPACE] Finding 0065, [INV-MONOTONIC], [INV-NO-IADDR-REUSE].

---

## Code Exploration

I now have everything needed. Here is the complete answer with all citations.

---

## Link Sub-Allocator Address Emission in udanax-green

### Bottom line

The LINKATOM allocator **only ever emits addresses on the strict `inc(·,0)` chain** `d.0.2.1`, `d.0.2.2`, `d.0.2.3`, … for home document `d`. "Produced by A\_L(d)" is a hard, self-enforcing gate: every emitted address was produced by this same allocator, and the max of the homed set is always one of those addresses (or `d` itself when the set is empty). No off-chain child address can appear.

---

### Constants

`TEXTATOM = 1`, `LINKATOM = 2` [backend/xanadu.h:145–146]:

```c
#define TEXTATOM  1
#define LINKATOM  2
```

---

### Call chain

`docreatelink` [backend/do1.c:195–232] builds the hint and calls:

```c
makehint(DOCUMENT, ATOM, LINKATOM, docisaptr, &hint);   // do1.c:207
createorglingranf(taskptr, granf, &hint, linkisaptr)     // do1.c:209
```

`createorglgr` [backend/granf2.c:111–128] calls `findisatoinsertgr` to obtain the address, then calls `insertseq` to commit it. The only code that writes link addresses into the granf is this path — no other path touches `d.0.2.*`.

`findisatoinsertgr` [backend/granf2.c:130–156] dispatches to `findisatoinsertmolecule` for `ATOM` sub-types:

```c
if (hintptr->subtype == ATOM) {
    if (!isaexistsgr(fullcrumptr, &hintptr->hintisa)) return FALSE;
    findisatoinsertmolecule(fullcrumptr, hintptr, isaptr);   // granf2.c:142
```

---

### The allocator: `findisatoinsertmolecule` [backend/granf2.c:158–181]

```c
tumblerincrement(&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound);  // 162
clear(&lowerbound, sizeof(lowerbound));                                        // 163
findpreviousisagr((typecorecrum*)fullcrumptr, &upperbound, &lowerbound);      // 164
if (tumblerlength(&hintptr->hintisa) == tumblerlength(&lowerbound)) {          // 165
    tumblerincrement(&lowerbound, 2, hintptr->atomtype, isaptr);               // 166
    tumblerincrement(isaptr, 1, 1, isaptr);                                    // 167
} else if (hintptr->atomtype == TEXTATOM) {                                    // 168
    tumblerincrement(&lowerbound, 0, 1, isaptr);                               // 169
} else if (hintptr->atomtype == LINKATOM) {                                    // 170
    tumblerincrement(&hintptr->hintisa, 2, 2, isaptr);                        // 171  ← sentinel = d.0.2
    if (tumblercmp(&lowerbound, isaptr) == LESS)
        tumblerincrement(isaptr, 1, 1, isaptr);                                // 173  Path A
    else
        tumblerincrement(&lowerbound, 0, 1, isaptr);                           // 175  Path B
}
```

For the LINKATOM case (`hintptr->atomtype == 2`, `hintptr->hintisa == d`):

**Search bound** — `upperbound = d.0.3` (LINKATOM+1=3).  
**Sentinel** — `isaptr = d.0.2` (line 171: rightshift=2, value=2=LINKATOM, hardcoded).

`findpreviousisagr` [backend/granf2.c:255–277] returns the **maximum address** in the granf strictly less than `d.0.3`. Concretely, within document `d`'s sub-tree, only these items exist:
- `d` itself (the document orgl at `GRANORGL`)
- Text atoms at `d.0.1.*` (TEXTATOM=1, all numerically less than `d.0.2`)
- Previously allocated link atoms at `d.0.2.K` (LINKATOM=2, in `[d.0.2, d.0.3)`)

---

### Two emission paths, both on-chain

**Path A — `lowerbound < d.0.2` (line 172–173):**  
Triggered when no links exist yet; `lowerbound` is `d` or a text atom. Result:

```c
tumblerincrement(d.0.2, 1, 1, isaptr)   // rightshift=1: append child → d.0.2.1
```

Produces `d.0.2.1` — the first and only possible first link address.

**Path B — `lowerbound >= d.0.2` (line 174–175):**  
Triggered for every subsequent link; `lowerbound = d.0.2.N` (a prior allocation). Result:

```c
tumblerincrement(d.0.2.N, 0, 1, isaptr)   // rightshift=0: increment last component
```

`tumblerincrement(aptr, 0, bint, cptr)` [backend/tumble.c:599–622] finds `idx` = index of the last non-zero mantissa component and does `cptr->mantissa[idx] += bint`. For `d.0.2.N` the last non-zero component is `N`; adding 1 gives `d.0.2.(N+1)`. This is **the next sibling**, not a child.

---

### Why off-chain addresses cannot become `lowerbound`

The critical closure argument: `findpreviousisagr` can only return what is already in the granf. The only items ever inserted at `d.0.2.*` are those produced by this same allocator via `createorglgr → insertseq`. Since the allocator only ever produces `d.0.2.1`, `d.0.2.2`, …, the max of the homed set is always `d.0.2.N` for some N ≥ 0. An address like `d.0.2.N.M` (child of a link) never enters the granf, so it cannot become `lowerbound`, and Path B cannot jump off-chain.

The `findisatoinsertnonmolecule` function [backend/granf2.c:203–242] has an explicit `lowerbound_under_hint` guard (lines 228–233) to protect against stray lowerbound values leaking across accounts. The molecule path does not need this guard because the upperbound `d.0.(LINKATOM+1)` already geometrically confines the search to `d`'s atom sub-space, and the only items there are products of A\_L(d) itself.

---

### Summary

| Situation | `lowerbound` | Emitted address | On `inc(·,0)` chain? |
|---|---|---|---|
| First link (empty doc) | `d` | `d.0.2.1` | Yes — first element |
| First link (text exists) | `d.0.1.X` | `d.0.2.1` | Yes — first element |
| N-th link | `d.0.2.N` | `d.0.2.(N+1)` | Yes — next sibling |

**"Produced by A\_L(d)" is a hard gating precondition on link emission.** The allocator forms a closed induction: it emits `d.0.2.1` initially, and each subsequent call takes the predecessor's output as `lowerbound` and emits its increment. There is no code path — not via the max-of-homed-set, not via a `lowerbound` from another atom type, not via any other insertion — that can cause the LINKATOM allocator to produce an address outside `{d.0.2.K : K ≥ 1}`.
