## Question 11 [evidence]

> When FINDNUMOFLINKSFROMTOTHREE counts matching links, is it counting distinct link orgls or counting spanfilade DOCISPAN entries, and can a single link with a multi-span endset be counted more than once?

## KB Synthesis

FINDNUMOFLINKSFROMTOTHREE counts **link orgl ISAs** — not DOCISPAN entries — and **yes, a single link with a multi-span endset can be counted more than once**.

## What is being counted

From [SS-FIND-LINKS] (Finding 0035): FINDNUMOFLINKSFROMTOTHREE is a trivial wrapper that calls `findlinksfromtothreesp()` to materialize a linked list of matching links, then walks the list counting elements. The spanfilade maps I-addresses to link ISAs (link orgl identities); DOCISPAN entries are a separate type-4 sub-index for document-content discovery and play no role here [SS-DOCISPAN, SS-SPANF-OPERATIONS].

## Whether a multi-span link is counted multiple times

It can be. A link's endset is stored as a set of I-spans (sporgls), not a single contiguous range [SS-LINK-ENDPOINT, Finding 0037]. When the query I-address range overlaps multiple I-spans of the same link, the link ISA can appear multiple times in the result list before `findlinksfromtothreesp()` returns it. The KB has two direct observations of this:

- [EC-PIVOT-LINK-FRAGMENTATION] (Finding 0019): after a pivot rearranges linked content, `find_links` returns the same link **duplicated**.
- [EC-MULTISPAN-LINK-DUPLICATION] (Finding 0019): creating a link with multiple source spans causes `retrieve_endsets` to return duplicate spans for a single link ISA.

The `intersectlinksets()` function performs an O(n·m) or O(n·m·p) intersection [SS-FIND-LINKS, Finding 0035] but is not described as deduplicating its output. Since FINDNUMOFLINKSFROMTOTHREE simply counts the list elements linearly, any duplicates in the list inflate the count.

## Summary

| Question | Answer |
|----------|--------|
| What is counted? | Link orgl ISAs in `findlinksfromtothreesp()` result list |
| DOCISPAN entries? | No — separate sub-index, unrelated |
| Multi-span link counted twice? | Yes — documented by [EC-PIVOT-LINK-FRAGMENTATION] and [EC-MULTISPAN-LINK-DUPLICATION] |

---

## Code Exploration

I have all the source I need. Here is my complete, fully-cited answer.

---

## FINDNUMOFLINKSFROMTOTHREE: Counting Unit and Multi-Span Behavior

### TL;DR

It counts **link ORGL addresses** (nodes in a `typelinkset`), not DOCISPAN entries. However, **a single link with a multi-span endset CAN be counted more than once** due to a deduplication bug in `onlinklist`.

---

### Call Chain

```
findnumoflinksfromtothree      fns.c:204
  dofindnumoflinksfromtothree  do1.c:355
    findnumoflinksfromtothreesp  spanf1.c:105
      findlinksfromtothreesp     spanf1.c:56
        sporglset2linkset        sporgl.c:222
          sporglset2linksetinrange  sporgl.c:239
            onlinklist           spanf2.c:26
      intersectlinksets          spanf2.c:46
```

---

### The Counting Line

`spanf1.c:112`:
```c
for (n = 0; linkset; linkset = linkset->next, ++n);
```

This walks a `typelinkset` linked-list and counts **nodes**. Each node is a `typelink` holding a single `.address` tumbler — the ORGL address of one link. This is unambiguously counting link ORGLs, not spanfilade entries.

---

### How the Linkset Is Built

`findlinksfromtothreesp` (`spanf1.c:56`) converts each of the three vspecsets to a sporglset (`specset2sporglset`, lines 70–75), then calls `sporglset2linkset` three times (`spanf1.c:77, 85, 93`) — once per endset role (FROM/TO/THREE) — then intersects the results (`spanf1.c:100`).

Inside `sporglset2linksetinrange` (`sporgl.c:239`), for each sporgl in the sporglset:

`sporgl.c:259`:
```c
context = retrieverestricted(spanfptr, (typespan*)sporglset, SPANRANGE, &range, ORGLRANGE, (typeisa*)infoptr);
```

`sporgl.c:263–265`:
```c
for (c = context; c; c = c->nextcontext) {
    beheadtumbler(&c->totaloffset.dsas[ORGLRANGE], &linksa);
    onlinklist(taskptr, linksetptr, &linksa);
}
```

Each context entry is one spanfilade hit. For a link whose FROM endset covers *N* spans, a matching query can produce *N* context entries — all with the same `linksa` address, since they're all entries for the same link ORGL. The `onlinklist` call is supposed to deduplicate.

---

### The Deduplication Bug in `onlinklist`

`spanf2.c:26–44`:
```c
onlinklist(typetask *taskptr, typelinkset *linksetptr, typeisa *linkisaptr)
{
  typelink *linkset, *temp, *nextlink;
  typelink *makelinkitem();

    linkset = makelinkitem(taskptr, linkisaptr);

    if (*linksetptr == NULL) {
        *linksetptr = linkset;
        return(0);
    }

    for (temp = *linksetptr; nextlink = temp->next; temp = nextlink) {
        if (tumblereq(&temp->address, linkisaptr))
            return(0);
    }

    temp->next = linkset;   /* appends without checking the last node */
}
```

The loop condition is `nextlink = temp->next` — it iterates only while `temp->next != NULL`. When the loop exits, `temp` IS the last node, but its address has **never been compared** to `linkisaptr`. The append happens unconditionally.

**Consequence for a 2-span endset:**

1. Span 1 match → list is empty → first branch fires, list becomes `[A]`.  
2. Span 2 match → list has one element; loop starts with `temp = A`, `nextlink = A.next = NULL` → exits immediately without checking `A` → appends → list becomes `[A, A]`.

For 3+ spans, span 3 onward does find `A` in the non-last position and returns without adding, so the count stays at 2 rather than climbing further.

**So the duplicate survives into `intersectlinksets`:**

`spanf2.c:96–104`:
```c
for (; temp1; temp1 = temp1->next) {
    for (temp2 = linkset2; temp2; temp2 = temp2->next) {
        if (tumblereq(&temp1->address, &temp2->address)) {
            linkset4 = makelinkitem(taskptr, &temp1->address);
            *linkset4ptr = linkset4;
            linkset4ptr = &linkset4->next;
        }
    }
}
```

No deduplication here. If `fromlinkset = [A, A]` and `tolinkset = [A]`, the intersection produces `[A, A]` — which the counting loop at `spanf1.c:112` returns as **2**, not **1**.

---

### Answers to Your Specific Questions

**1. Is it counting distinct link orgls or spanfilade DOCISPAN entries?**

It counts **distinct link ORGL addresses** — nodes in a `typelinkset`, each holding a tumbler address (`typelink.address`). The spanfilade DOCISPAN entries are the mechanism for *finding* those ORGLs, but the counted unit is the address, not the entry.

**2. Can a single link with a multi-span endset be counted more than once?**

**Yes.** When a link's endset covers 2 or more spans and the query overlaps with 2 or more of them, `sporglset2linksetinrange` calls `onlinklist` at least twice with the same ORGL address. The off-by-one bug in `onlinklist` (`spanf2.c:38–43`) fails to check the last node in the list, so the second call appends a duplicate. `intersectlinksets` performs no deduplication on its own, so the duplicate propagates to the final count. The result is that such a link is counted as **2** rather than **1**, regardless of how many spans beyond 2 also match.
