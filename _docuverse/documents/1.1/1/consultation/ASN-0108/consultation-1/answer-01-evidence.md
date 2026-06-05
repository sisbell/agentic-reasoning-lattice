## Question 1 [evidence]

> When the insertion-sort builds the result list, does it break ties between two links matching the same content-endpoint boundary (e.g. by link address), or can two distinct links land at the same sort position?

## KB Synthesis

The KB does not answer this question.

[SS-CONTEXT-LIST] and [INV-RETRIEVAL-V-SORTED] document that `incontextlistnd()` builds a list sorted by left boundary (`totaloffset.dsas[index]`) via insertion-sort, and the stated invariant uses `<=` (not strict `<`), so ties at the same left boundary are structurally permitted. [SS-INTERVAL-CMP] documents that `intervalcmp` has a distinct `ONMYLEFTBORDER` return value for the equality case.

However, the KB captures only the four high-level cases of the insertion-sort and does not describe how `ONMYLEFTBORDER` is handled when two distinct contexts share the same left boundary — specifically, whether the algorithm inserts the newcomer before or after the existing entry, and whether link address or any other field breaks the tie. [FC-RETRIEVAL-TREE-INDEPENDENCE] and [INV-RETRIEVAL-TREE-INDEPENDENCE] confirm that tree traversal order does not affect result ordering, but say nothing about intra-position ordering.

The tie-breaking behavior is not answerable from the KB as it stands.

---

## Code Exploration

I now have everything needed to answer definitively. Here is my complete analysis.

---

## Answer: Tie-Breaking in the Link Result List

### The Insertion-Sort: `incontextlistnd`

The sort that builds the ordered context list is `incontextlistnd` in `context.c:75–111`:

```c
/* put c on clist in index order */
int incontextlistnd(typecontext **clistptr, typecontext *c, INT index)
{
  prologuecontextnd (c, &grasp, (typedsp*)NULL);   // grasp = c->totaloffset
  c->nextcontext = NULL;
  clist = *clistptr;

  if (!clist) {          /* 1st insertion */
      *clistptr = c;
      return(0);
  }
                         /* on beginning */
  if (whereoncontext (clist, &grasp.dsas[index], index) < THRUME) {
      c->nextcontext = clist;
      *clistptr = c;
      return(0);
  } else {
      for (; nextc = clist->nextcontext; clist = nextc) {
                         /* in middle */
          if ((whereoncontext (clist, &grasp.dsas[index], index) > ONMYLEFTBORDER)
              && (whereoncontext (nextc, &grasp.dsas[index], index) < ONMYLEFTBORDER)) {
              c->nextcontext = nextc;
              clist->nextcontext = c;
              return(0);
          }
      }
  }
                         /* on end */
  c->nextcontext = NULL;
  clist->nextcontext = c;
}
```

The sort key is `grasp.dsas[index]` — the start of the new crum's span on the chosen axis. The constants from `common.h:86–90` are:

```
TOMYLEFT = -2, ONMYLEFTBORDER = -1, THRUME = 0, ONMYRIGHTBORDER = 1, TOMYRIGHT = 2
```

`whereoncontext(ptr, address, index)` returns where `address` falls relative to `ptr`'s interval `[ptr.totaloffset, ptr.totaloffset + ptr.contextwid]` on axis `index`.

---

### Where `incontextlistnd` Is Called

The call site is `findcbcinarea2d` in `retrie.c:263`:

```c
context = makecontextfromcbc((typecbc*)crumptr, (typewid*)offsetptr);
incontextlistnd(headptr, context, index1);
```

Called with `index1 = SPANRANGE` in the link-find path (`sporglset2linksetinrange` in `sporgl.c:259`):

```c
context = retrieverestricted(spanfptr, (typespan*)sporglset, SPANRANGE, &range, ORGLRANGE, ...);
```

So the sort axis is **SPANRANGE** — the I-space content address — not ORGLRANGE (the link address). The list is ordered by the start of each matching crum's content span.

---

### Tie Analysis: Two Links with the Same Content-Endpoint Boundary

**Scenario**: Links L1 and L2 both have an endpoint span starting at I-address X (same content boundary). Their crums are produced in tree-traversal order (L1 first, then L2) by `findcbcinarea2d`.

#### L1 arrives first (list is empty):
```
incontextlistnd: !clist → insert at head.
List: [L1(start=X)]
```

#### L2 arrives second with same start X:

**Beginning check** (`context.c:90`):
```c
whereoncontext(L1, X, SPANRANGE)
```
L1's interval is `[X, X + L1.width]`. Address X equals the left boundary → returns `ONMYLEFTBORDER` (−1).

Condition: `ONMYLEFTBORDER < THRUME` = `−1 < 0` = **TRUE** → **L2 is prepended before L1**.

```
List: [L2(start=X), L1(start=X)]
```

The tie is resolved by a **prepend** — the second-found element goes *before* the first. There is no link-address comparison anywhere in this logic.

---

### Middle-Position Ties Are Different

Suppose the list already contains `[A(start=5), B(start=X)]` and new element C(start=X) arrives:

**Beginning check**: `whereoncontext(A(5), X, idx)` — X > A.start, so A.right may be ≤ X, giving `TOMYRIGHT (2)`. `2 < 0` = FALSE → no beginning insertion.

**Middle loop**, first iteration (clist=A, nextc=B):
- `whereoncontext(A(5), X, idx) > ONMYLEFTBORDER`: TRUE (A's start < X).
- `whereoncontext(B(X), X, idx) < ONMYLEFTBORDER`: B.start = X → `ONMYLEFTBORDER (−1)`. Condition `−1 < −1` = **FALSE**.
- Not inserted between A and B.

**End**: C is **appended after B**.

```
List: [A(5), B(X), C(X)]
```

So here, ties *in the middle* preserve traversal order (appended at end).

---

### No Secondary Sort Key — Ever

There is no fallback comparison on link address. After `incontextlistnd` produces the context list, `sporglset2linksetinrange` (`sporgl.c:263–266`) extracts link addresses and appends them to the result via `onlinklist` (`spanf2.c:26–44`):

```c
for (c = context; c; c = c->nextcontext) {
    beheadtumbler(&c->totaloffset.dsas[ORGLRANGE], &linksa);
    onlinklist(taskptr, linksetptr, &linksa);
}
```

`onlinklist` does only a duplicate-check by exact tumbler equality, then appends:

```c
for (temp = *linksetptr; nextlink = temp->next; temp = nextlink) {
    if (tumblereq(&temp->address, linkisaptr))
        return(0);   // skip duplicate
}
temp->next = linkset;   // append
```

No sort. No link-address comparison. The final result list reflects the context list order verbatim.

---

### What Determines the Traversal Order?

`findcbcinarea2d` walks the spanfilade depth-first, left-to-right through siblings via `getrightbro` (`retrie.c:252–265`). Two crums representing L1 and L2 at the same SPANRANGE start will be adjacent in the spanfilade tree, ordered by ORGLRANGE (their link-identity prefix). However, `incontextlistnd` ignores ORGLRANGE entirely — it only sorts by SPANRANGE.

---

### Conclusion

**Two distinct links whose endpoint spans start at the same I-address (same content-endpoint boundary) can land at the same sort position — and they do.**

There is **no tie-breaking by link address**. The relative order of tied links within the context list is:

- If they arrive at the head with no preceding smaller-start element already placed: the later-found element is **prepended** before the earlier-found one — reversing traversal order (`context.c:90–94`, `ONMYLEFTBORDER < THRUME`).
- If they arrive after a smaller-start element is already at the head: they are **appended in traversal order** (`context.c:98–99`, the strict `< ONMYLEFTBORDER` test excludes equal-start elements from middle insertion).

The traversal order itself is determined by the spanfilade's internal tree structure — an artifact of link-creation order, not link address. The asymmetry between the beginning and middle cases means the ordering of tied links is not consistently in any particular direction relative to link address, and it shifts depending on insertion history. There is no specification or code that would make ORGLRANGE (link address) serve as a tiebreaker.
