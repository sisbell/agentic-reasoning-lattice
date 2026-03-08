## Question 16 [gregory]

> In the POOM's 2D enfilade, the I-dimension index enables reverse lookup (given an I-address, find V-positions). When multiple V-positions map to the same I-address (self-transclusion), does `incontextlistnd` return ALL matching V-positions in a single traversal, or does it require multiple queries?

## KB Synthesis

**A single traversal returns all matching V-positions.**

The definitive evidence is in [SS-POOM-MULTIMAP] (Finding 0039):

> The search algorithm `findcbcinarea2d()` traverses all siblings at each B-tree level and recursively descends into **all qualifying subtrees**, accumulating every matching leaf node. The accumulation function `incontextlistnd()` inserts each found context into a sorted linked list, **never replacing existing entries**.

The concrete example from that entry confirms this:

```
Document has "B" at V-positions 1.2, 1.4, and 1.5, all referencing I-address i_B.

ispan2vspanset(poom, i_B) = {
  VSpan(1.2, width=0.1),
  VSpan(1.4, width=0.1),
  VSpan(1.5, width=0.1)
}
Result set cardinality = 3 (one per V-position referencing i_B)
```

The mechanism works because `findcbcinarea2d()` does not stop at the first match — it continues traversing all siblings via `getrightbro` and all qualified subtrees, invoking `incontextlistnd()` per leaf. `incontextlistnd()` performs insertion-sort into the accumulated list rather than replacement, so each V-position referencing the queried I-address gets a distinct context entry.

The ordering guarantee from [SS-CONTEXT-LIST] (Finding 0078) applies: the returned list is sorted by V-address regardless of tree structure or insertion order, as a property of the insertion-sort in `incontextlistnd()`.

This single-traversal, all-results behavior is also confirmed by [INV-RETRIEVAL-TREE-INDEPENDENCE] — the result set is independent of how the POOM tree is structured internally, meaning the completeness property holds for any tree shape, not just pathological or simple cases.

**Summary:** One call to `ispan2vspanset` (via `findcbcinarea2d` + `incontextlistnd`) returns all V-positions mapping to a given I-address, sorted by V-address, in a single traversal.

---

## Code Exploration

I have all the code I need. Here is the complete answer.

---

## Answer: `incontextlistnd` is a single-insertion function; all V-positions are collected in one traversal pass

### The POOM's 2D structure

Each POOM bottom crum (`type2dcbc`) holds a 2D displacement/width pair indexed by `I=0` and `V=1` [`wisp.h:19-20`]:

```
/* wid and dsp indexes for pm */
#define I  0
#define V  1
```

Every bottom crum occupies a rectangle in the I×V space. Self-transclusion means multiple such crums share the same I-extent but differ in their V-coordinate — the same I-content appears at more than one V-position.

---

### The reverse-lookup call chain (I → V)

`ispan2vspanset` [orglinks.c:389-393] is the public entry point:

```c
typevspanset *ispan2vspanset(typetask *taskptr, typeorgl orgl, typeispan *ispanptr, typevspanset *vspansetptr)
{
    return permute(taskptr, orgl, ispanptr, I, vspansetptr, V);
}
```

`permute` [orglinks.c:404-422] iterates over every span in the restriction set and calls `span2spanset` for each:

```c
for (; restrictionspanset; restrictionspanset = restrictionspanset->next) {
    targspansetptr = span2spanset(taskptr, orgl, restrictionspanset, restrictionindex, targspansetptr, targindex);
}
```

`span2spanset` [orglinks.c:425-454] drives the actual tree traversal and then iterates the resulting context list:

```c
context = retrieverestricted((typecuc*)orgl, restrictionspanptr, restrictionindex,
                              (typespan*)NULL, targindex, (typeisa*)NULL);  // [orglinks.c:435]

for (c = context; c; c = c->nextcontext) {                                 // [orglinks.c:439]
    context2span (c, restrictionspanptr, restrictionindex, &foundspan, targindex);
    nextptr = (typespan *)onitemlist (taskptr, (typeitem*)&foundspan, (typeitemset*)targspansetptr);
}
```

`retrieverestricted` [retrie.c:56-85] → `retrieveinarea` [retrie.c:87-110] → `findcbcinarea2d` [retrie.c:229].

---

### `findcbcinarea2d`: the full-tree traversal that collects all matches

```c
for (; crumptr; crumptr = getrightbro (crumptr)) {          // [retrie.c:252]
    if (!crumqualifies2d (...)) continue;
    if (crumptr->height != 0) {
        dspadd (offsetptr, &crumptr->cdsp, &localoffset, (INT)crumptr->cenftype);
        findcbcinarea2d (findleftson ((typecuc*)crumptr), &localoffset,
                         span1start, span1end, index1,
                         span2start, span2end, index2, headptr, infoptr); // [retrie.c:259]
    } else {
        context = makecontextfromcbc ((typecbc*)crumptr, (typewid*)offsetptr); // [retrie.c:262]
        incontextlistnd (headptr, context, index1);                            // [retrie.c:263]
    }
}
```

Three things to note:

1. **The outer `for` loop iterates all right-siblings at each level** — it does not stop at the first match.
2. **`findcbcinarea2d` recurses into every qualifying upper crum** — depth-first, touching every qualifying subtree.
3. **`incontextlistnd` is called once per qualifying bottom crum** — it is a list-*insertion* function, not a query function.

`crumqualifies2d` [retrie.c:270-305] checks whether a crum's I-extent overlaps the query I-span. When `span2` is null (no V restriction — the case for a pure I→V lookup), `iszerotumbler(span2end)` returns `TOMYRIGHT` [retrie.c:292], meaning every crum qualifies on the V axis. All bottom crums whose I-extent overlaps the query are found, regardless of their V-position.

---

### `incontextlistnd`: sorted list insertion, not a query

```c
int incontextlistnd(typecontext **clistptr, typecontext *c, INT index)   // [context.c:75]
{
    prologuecontextnd (c, &grasp, (typedsp*)NULL);
    c->nextcontext = NULL;
    clist = *clistptr;
    if (!clist) {                                          /* 1st insertion */
        *clistptr = c;
        return(0);
    }
    if (whereoncontext (clist, &grasp.dsas[index], index) < THRUME) {
        c->nextcontext = clist;                            /* on beginning */
        *clistptr = c;
        return(0);
    } else {
        for (; nextc = clist->nextcontext; clist = nextc) {
            if ((whereoncontext (clist, ...) > ONMYLEFTBORDER)
             && (whereoncontext (nextc, ...) < ONMYLEFTBORDER)) {
                c->nextcontext = nextc;                    /* in middle */
                clist->nextcontext = c;
                return(0);
            }
        }
    }
    clist->nextcontext = c;                                /* on end */
}
```

`whereoncontext` for `POOM` type [context.c:137-139]:

```c
case POOM:
    movetumbler (&ptr->totaloffset.dsas[index], &left);
    tumbleradd (&left, &ptr->contextwid.dsas[index], &right);
```

The position comparison constants [common.h:86-90]:

```
TOMYLEFT=-2, ONMYLEFTBORDER=-1, THRUME=0, ONMYRIGHTBORDER=1, TOMYRIGHT=2
```

`incontextlistnd` inserts `c` into the linked list sorted by I-position. It makes no attempt to deduplicate, merge, or suppress entries with the same I-address. Every qualifying crum that `findcbcinarea2d` discovers is inserted unconditionally.

---

### Self-transclusion: what happens

For self-transclusion — say two bottom crums `A` and `B` both covering I-span `[5, 10)` but at V-positions `3` and `7` respectively — `findcbcinarea2d` will:

1. Visit crum `A` (qualifies on I), call `incontextlistnd` → list is `[A]`
2. Continue the sibling loop, visit crum `B` (also qualifies on I), call `incontextlistnd` → list is `[A, B]` (or `[B, A]` depending on I-sort order, which is the same here)

After the traversal, `span2spanset` loops over `[A, B]` [orglinks.c:439] and converts each to a V-span via `context2span`, appending both to the result span-set. Both V-positions — 3 and 7 — appear in the output.

---

### Conclusion

**`incontextlistnd` returns nothing — it inserts one context per call.** The function that does the actual "finding" is `findcbcinarea2d`, which performs a complete recursive walk over the POOM tree in a single traversal, calling `incontextlistnd` once for every qualifying bottom crum it encounters. All crums whose I-extent overlaps the query I-address are collected into the sorted context list before the traversal returns. The caller (`span2spanset`) then iterates the complete list and emits a V-span for each entry.

**Self-transclusion requires no additional queries.** All V-positions that map to the same I-address are found and returned in the single call to `retrieverestricted` / `findcbcinarea2d`. The context list handed back to `span2spanset` already contains all of them, sorted by I-position.
