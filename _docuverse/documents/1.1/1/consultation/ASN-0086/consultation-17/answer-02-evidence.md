## Question 2 [evidence]

> In udanax-green's link-emission code path (`docreatelink`, granfilade orgl tree extension, POOM update), does the substrate maintain an explicit per-allocator activation/realization state that is extended atomically when a link is emitted at an address whose enumeration index hasn't been reached yet, or does the implementation treat allocator addresses as purely logical (depositing at any address whose tumbler-algebra structure is admissible, without tracking activation state)?

## KB Synthesis

The KB is unambiguous: the implementation uses **purely logical, stateless address allocation** with no per-allocator activation or enumeration-index tracking.

## Allocation Mechanism

`docreatelink` calls `createorglingranf`, which dispatches to `findisatoinsertnonmolecule` (for the link orgl address) and `findisatoinsertmolecule` (for text/link content). Both operate identically [SS-ADDRESS-ALLOC, Finding 0077]:

1. Compute an upper bound from the parent/document ISA
2. Call `findpreviousisagr` — a live granfilade tree traversal finding the highest existing address below that bound
3. Increment by 1 from that maximum

There is **no cached "next" pointer, no activation record, no enumeration index**. [Finding 0061] is explicit: "The allocation function can be modeled as a pure function of the granfilade state: `next_iaddr(granf) = max_iaddr(granf) + 1`. No hidden session state participates in allocation."

[Finding 0077] further confirms: "There is no single global `Σ.next` counter. Allocation is stateless query-and-increment on different tumbler ranges via `findpreviousisagr`."

## Admissibility Check

The only constraint is tumbler-algebra admissibility — whether the candidate address falls within the correct range. For links, `upperbound = docISA.2.3`, bounding the search to the document's link subspace [Finding 0065]. No activation state is consulted; the address is valid iff it is the increment of the current maximum within that range.

## Atomicity

The entire emission — orgl creation in granf, V-stream update via `docopy` into the 2.x subspace, and endpoint indexing in spanf — executes as a single run-to-completion unit [INV-ATOMICITY, ST-CREATE-LINK]. But this atomicity is a property of the single-threaded event loop, not of any per-allocator state machine.

## Observable Consequence

Because all entities (text atoms, link orgls, document addresses) draw from the same monotonically growing granfilade tree, a `CREATELINK` **advances the maximum I-address**, breaking contiguity for subsequent text insertions — without any activation bookkeeping [INT-LINK-INSERT, Finding 0063]. This side-effect is purely arithmetic, not state-machine-driven.

**Conclusion:** The implementation deposits at any address whose tumbler-algebra structure is admissible (falls within the parent range, exceeds the current maximum). There is no activation/realization state to extend.

---

## Code Exploration

I have all the source citations needed. Here is the complete answer.

---

## Answer: Allocator Addresses Are Purely Logical — No Per-Allocator Activation State

The substrate does **not** maintain explicit per-allocator activation or realization state. Allocator addresses are treated as purely logical quantities, computed on demand from current tree topology and deposited without advancing any separate "reached" counter or activation list. Here is the complete trace.

---

### 1. `docreatelink` Entry Point [do1.c:195–221]

```c
bool docreatelink(typetask *taskptr, typeisa *docisaptr, typespecset fromspecset,
                  typespecset tospecset, typespecset threespecset, typeisa *linkisaptr)
{
  ...
  makehint (DOCUMENT, ATOM, LINKATOM, docisaptr, &hint);
  return (
       createorglingranf (taskptr, granf, &hint, linkisaptr)   // computes + inserts address
    && tumbler2spanset (taskptr, linkisaptr, &ispanset)
    && findnextlinkvsa (taskptr, docisaptr, &linkvsa)
    && docopy (taskptr, docisaptr, &linkvsa, ispanset)
    && findorgl (taskptr, granf, linkisaptr, &link, /*WRITEBERT ECH 7-1*/NOBERTREQUIRED)
    && specset2sporglset (...)
    && insertendsetsinorgl (...)
    && insertendsetsinspanf (...)
  );
}
```

No state machine, no pre-flight range check, no counter advanced before or after insertion. The link address is computed once in `createorglingranf` and then used unconditionally. The commented-out `WRITEBERT` at [do1.c:213] is access-control scaffolding, not allocation state.

---

### 2. Address Computation: `findisatoinsertmolecule` [granf2.c:158–181]

```c
static int findisatoinsertmolecule(typecuc *fullcrumptr, typehint *hintptr, typeisa *isaptr)
{
  typeisa upperbound, lowerbound;

  tumblerincrement (&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound); // bound this doc's link space
  clear (&lowerbound, sizeof(lowerbound));
  findpreviousisagr ((typecorecrum*)fullcrumptr, &upperbound, &lowerbound);    // find last allocated
  if (tumblerlength (&hintptr->hintisa) == tumblerlength (&lowerbound)) {
    tumblerincrement (&lowerbound, 2, hintptr->atomtype, isaptr);
    tumblerincrement (isaptr, 1, 1, isaptr);                                   // next = last + 1
  } else if (hintptr->atomtype == LINKATOM) {
    tumblerincrement (&hintptr->hintisa, 2, 2, isaptr);
    if (tumblercmp (&lowerbound, isaptr) == LESS)
      tumblerincrement (isaptr, 1, 1, isaptr);
    else
      tumblerincrement (&lowerbound , 0, 1, isaptr);
  }
}
```

The entire computation is: *find the highest existing link ISA under this document, then increment it*. No counter is consulted. No high-water mark is written back. No "enumeration index reached" flag is set. The result is a derived address — what the next admission into the Hilbert space of tumblers should be, given current tree state.

---

### 3. The One Structural Prerequisite: Parent Document Must Exist [granf2.c:130–156]

```c
bool findisatoinsertgr(typecuc *fullcrumptr, typehint *hintptr, typeisa *isaptr)
{
  if (hintptr->subtype == ATOM) {
    if (!isaexistsgr (fullcrumptr, &hintptr->hintisa)) {    // checks document ISA exists
      fprintf (stderr,"nothing at hintisa for atom\n");
      return (FALSE);
    }
    findisatoinsertmolecule (fullcrumptr, hintptr, isaptr);
  } else {
    findisatoinsertnonmolecule (fullcrumptr, hintptr, isaptr);
  }
  tumblerjustify(isaptr);
  return (TRUE);
}
```

For ATOM types (links and text), `isaexistsgr` [granf2.c:244–253] is called to confirm the **parent document** ISA exists in the tree. This is a structural prerequisite check — the document must have been created first. It is **not** tracking per-link enumeration index. There is no notion of "links 1 through N have been emitted; link N+1 is now the frontier."

---

### 4. Bounds Check on Retrieval: Tree Width, Not Activation State [granf2.c:31–32]

```c
typeorgl fetchorglgr(typetask *taskptr, typegranf fullcrumptr, typeisa *address)
{
  if (tumblercmp (&((typecuc*)fullcrumptr)->cwid.dsas[WIDTH], address) == LESS)
    return (NULL);
  ...
}
```

The only pre-retrieval guard is whether `address` is within the granfilade's cumulative `WIDTH`. This width is the total count of items currently inserted in the tree — it is a structural property of the tree, not a separately maintained activation register. An address is "reachable" iff it was inserted; the `WIDTH` simply reflects that insertion.

---

### 5. POOM Gap-Making: Insertion Beyond Current Extent Is Explicitly Supported [insertnd.c:140–143]

```c
int makegappm(typetask *taskptr, typecuc *fullcrumptr, typewid *origin, typewid *width)
{
  ...
  if (iszerotumbler (&fullcrumptr->cwid.dsas[V])
  || tumblercmp (&origin->dsas[V], &grasp.dsas[V]) == LESS
  || tumblercmp (&origin->dsas[V], &reach.dsas[V]) != LESS)
    return(0);    /* this if for extensions to bc without calling cut*/
  ...
}
```

When the insertion origin lies **outside** the current tree extent (`reach`), `makegappm` returns 0 without making any cuts. `insertnd` then proceeds directly to `doinsertnd` [insertnd.c:57], which deposits the new crum at the computed address. The comment "for extensions to bc without calling cut" confirms that depositing at addresses beyond the current tree is the designed, expected case — no activation gating prevents it.

---

### 6. `findorgl`'s Access Check Is Authorization, Not Allocation State [granf1.c:17–41]

```c
bool findorgl(typetask *taskptr, typegranf granfptr, typeisa *isaptr, typeorgl *orglptr, int type)
{
  if ((temp = checkforopen(isaptr, type, user)) <= 0) {
    ...
    return FALSE;
  }
  *orglptr = fetchorglgr(taskptr, granfptr, isaptr);
  return (*orglptr ? TRUE : FALSE);
}
```

`checkforopen` (in `bert.c`) verifies the calling user has the document open. This is access control, not allocation sequencing. It is the only guard between the caller and the tree, and it carries no information about which enumeration indices have been "reached."

---

## Summary

| Question | Answer |
|---|---|
| Per-allocator activation state? | **None.** No counter, list, or state machine tracks which addresses have been "activated." |
| Atomic extension on link emission? | **No.** `createorglingranf` derives an address from tree state and inserts it; nothing is "extended." |
| High-water mark? | **Absent.** The granfilade's `WIDTH` reflects cumulative insertions, not a managed frontier. |
| Address validation before emission? | **Structural only.** The parent document ISA must exist (`isaexistsgr`). No enumeration-index range check. |
| Deposit at any admissible tumbler address? | **Yes.** `makegappm` explicitly returns early for insertions beyond current tree extent, allowing deposit anywhere whose tumbler structure is arithmetically valid. |

The address space is the complete Hilbert space of valid tumblers. What exists is what has been inserted into the tree. The substrate knows nothing of "reached vs. unreached" enumeration indices — it computes the next address from `findpreviousisagr`, increments it, and deposits there, unconditionally (subject only to the document-existence prerequisite).
