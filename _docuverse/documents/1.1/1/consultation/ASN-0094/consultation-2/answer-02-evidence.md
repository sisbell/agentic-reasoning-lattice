## Question 2 [evidence]

> Does udanax-green enforce any single-active-duplicate constraint at the link-store layer for relation-like structures, or is duplicate-suppression handled entirely by callers above the link store?

## KB Synthesis

The KB is unambiguous: **no single-active-duplicate constraint exists at the link-store layer**. Duplicate suppression is entirely a caller responsibility.

## Link-Store Layer Has No Duplicate Checking

**At the spanf (link index):** `insertspanf` and `insertendsetsinspanf` add entries unconditionally — there is no lookup before insert to detect preexisting equivalent entries [SS-SPANF-OPERATIONS]. The spanf is a pure append-only index [INV-SPANF-WRITE-ONLY].

**At the POOM (document V-stream):** `insertpm` explicitly has no duplicate guard. `isanextensionnd()` checks only contiguity, never whether an I-address already exists elsewhere in the document [PRE-COPY]. The POOM is formally modeled as a **multimap** — a single I-address can and does map to multiple V-positions [SS-POOM-MULTIMAP]. Self-transclusion actively exercises this [EC-SELF-TRANSCLUSION].

**At link object creation:** `createorglingranf` allocates a fresh, unique ISA via monotonic increment [INV-MONOTONIC], [SS-ADDRESS-ALLOC]. This prevents duplicate *link objects*, but nothing prevents creating two distinct link objects with semantically identical source/target endpoint specs. The three-step creation sequence in `docreatelink` contains no pre-creation check for a preexisting link with the same endpoint I-addresses [ST-CREATE-LINK].

## Observable Evidence of No Deduplication

The KB records two cases where the system surfaces duplicates without suppression:

- `find_links` returns **the same link twice** after a pivot rearrangement [EC-PIVOT-LINK-FRAGMENTATION]
- `retrieve_endsets` returns **duplicate spans** for multi-span links [EC-MULTISPAN-LINK-DUPLICATION]

These are not treated as errors in the KB — they are observed behaviors.

## Summary

The link-store layer enforces one structural uniqueness property: each link object gets a unique ISA via monotonic allocation [INV-MONOTONIC]. Everything else — preventing semantically duplicate link relationships, deduplicating `find_links` results, suppressing duplicate endset entries — is a caller obligation above the link store. The implementation provides no machinery for it.

---

## Code Exploration

I've verified the key code. I also noticed a secondary bug in `onlinklist` worth flagging. Here is the full answer.

---

## Answer: No Single-Active-Duplicate Constraint at the Link-Store Layer

**Short answer:** udanax-green enforces **no duplicate constraint at the link-store layer**. The granfilade, spanfilade, and POOM structures accept repeated insertions of identical endpoint tuples without complaint. The only duplicate suppression exists at query-time result-set construction — one level above the store — and that code itself has a latent bug.

---

### 1. The Creation Path — No Existence Check

**`fns.c:100–112`** — the FEBE `createlink` handler:

```c
void createlink(typetask *taskptr)
{
    if (
       getcreatelink (taskptr, &docisa, &fromspecset, &tospecset, &threespecset)
    && docreatelink (taskptr, &docisa, fromspecset, tospecset, threespecset, &linkisa)){
        putcreatelink (taskptr, &linkisa);
    } else
        putrequestfailed (taskptr);
}
```

No guard. It calls `docreatelink` unconditionally.

**`do1.c:195–221`** — `docreatelink`:

```c
bool docreatelink(typetask *taskptr, typeisa *docisaptr, typespecset fromspecset,
                  typespecset tospecset, typespecset threespecset, typeisa *linkisaptr)
{
    makehint (DOCUMENT, ATOM, LINKATOM, docisaptr, &hint);
    return (
         createorglingranf (taskptr, granf, &hint, linkisaptr)   // allocates new ISA
      && tumbler2spanset    (taskptr, linkisaptr, &ispanset)
      && findnextlinkvsa    (taskptr, docisaptr,  &linkvsa)
      && docopy             (taskptr, docisaptr, &linkvsa, ispanset)
      && findorgl           (taskptr, granf, linkisaptr, &link, NOBERTREQUIRED)
      && specset2sporglset  (taskptr, fromspecset,   &fromsporglset, NOBERTREQUIRED)
      && specset2sporglset  (taskptr, tospecset,     &tosporglset,   NOBERTREQUIRED)
      && specset2sporglset  (taskptr, threespecset,  &threesporglset,NOBERTREQUIRED)
      && setlinkvsas        (&fromvsa, &tovsa, &threevsa)
      && insertendsetsinorgl(taskptr, linkisaptr, link, &fromvsa, fromsporglset,
                             &tovsa, tosporglset, &threevsa, threesporglset)
      && insertendsetsinspanf(taskptr, spanf, linkisaptr, fromsporglset,
                              tosporglset, threesporglset)
    );
}
```

The call to `createorglingranf` at `do1.c:209` allocates a fresh ISA unconditionally — there is no prior lookup to ask "does a link with this (from, to, three) already exist?" The function proceeds directly to inserting into the three stores.

---

### 2. The Store Layer — Raw Insertion, No Constraint

**`spanf1.c:15–54`** — `insertspanf`:

```c
bool insertspanf(typetask *taskptr, typespanf spanfptr, typeisa *isaptr,
                 typesporglset sporglset, INT spantype)
{
    ...
    for (; sporglset; sporglset = ...) {
        ...
        insertnd(taskptr, (typecuc*)spanfptr, &crumorigin, &crumwidth, &linfo, SPANRANGE);
    }
    return (TRUE);
}
```

`insertnd` (`edit.c`, the enfilade tree editor) is a raw structural insertion. There is no "already present?" test before or after it — `spanf1.c:51` calls it directly in a loop over all endpoint spans.

`insertendsetsinspanf` (called from `do1.c:219`) calls `insertspanf` for LINKFROMSPAN, LINKTOSPAN, and LINKTHREESPAN — all three are unconditional raw inserts.

The parallel path through `insertendsetsinorgl` → `insertpm` (orglinks.c) for the POOM structure is identical in character: pure structural insertion, no existence check.

---

### 3. Where Deduplication Actually Lives — Query-Time Result Set

**`spanf2.c:26–44`** — `onlinklist`, called when building a link result set during retrieval:

```c
bool onlinklist(typetask *taskptr, typelinkset *linksetptr, typeisa *linkisaptr)
{
    linkset = makelinkitem (taskptr, linkisaptr);

    if (*linksetptr == NULL) {
        *linksetptr = linkset;
        return(0);
    }

    for (temp = *linksetptr; nextlink = temp->next; temp = nextlink) {
        if (tumblereq (&temp->address, linkisaptr))
            return(0);    // skip duplicate
    }

    temp->next = linkset;
}
```

**`spanf2.c:16–23`** — `isinlinklist`, the predicate form:

```c
bool isinlinklist(typelinkset linkset, typeisa *linkisaptr)
{
    for (; linkset; linkset = linkset->next) {
        if (tumblereq (&linkset->address, linkisaptr))
            return (TRUE);
    }
    return (FALSE);
}
```

These operate on the **in-memory result list** being assembled during a query traversal — they are caller-level deduplication of query output, not store-layer invariants. The store itself is never consulted to prevent a duplicate from being written.

---

### 4. A Secondary Bug in `onlinklist`

The loop at `spanf2.c:38`:

```c
for (temp = *linksetptr; nextlink = temp->next; temp = nextlink) {
    if (tumblereq (&temp->address, linkisaptr))
        return(0);
}
temp->next = linkset;
```

The loop condition `nextlink = temp->next` exits the loop when `temp->next == NULL` — at which point `temp` is the **last element**, and its address is **never checked**. The `tumblereq` check at line 39 fires for all elements except the last one. After the loop, `temp->next = linkset` appends unconditionally, without checking whether `temp` (the tail) is already the item being added.

Consequence: if the same link ISA is added when the list has exactly one element (or appears only at the tail), `onlinklist` will silently insert a duplicate into the result list. The deduplication is incomplete even at the caller level.

---

### Summary

| Layer | Function | File | Duplicate Check? |
|---|---|---|---|
| FEBE handler | `createlink` | `fns.c:100` | None |
| Operation | `docreatelink` | `do1.c:195` | None |
| Granfilade | `createorglingranf` | `granf2.c` | None — unconditional `insertseq` |
| Spanfilade | `insertspanf` | `spanf1.c:15` | None — unconditional `insertnd` |
| POOM | `insertpm` | `orglinks.c` | None — unconditional enfilade insert |
| Query result (caller) | `onlinklist` | `spanf2.c:26` | Partial — misses tail element |
| Query result (caller) | `isinlinklist` | `spanf2.c:16` | Correct predicate, read-only |

**Conclusion:** The link store (granfilade + spanfilade + POOM) has no uniqueness constraint on (from, to, three) endpoint tuples. `createlink` called twice with identical arguments creates two distinct link ISAs, both fully inserted into all three store structures. The only deduplication is at query-time result-set construction in `onlinklist`/`isinlinklist`, one architectural layer above the store — and `onlinklist` itself has a loop bug that allows tail-position duplicates through.
