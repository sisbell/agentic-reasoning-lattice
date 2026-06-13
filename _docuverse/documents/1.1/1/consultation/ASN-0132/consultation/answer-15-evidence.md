## Question 15 [evidence]

> With self-transclusion, where the same I-addresses appear at multiple V-positions inside the single document covered by the from-set, does `vspanset2sporglset` produce overlapping I-spans that cause the same link to be counted more than once?

## KB Synthesis

Yes, `vspanset2sporglset` can produce duplicate I-spans under self-transclusion, and this can cause the same link to be counted more than once. Here is the chain of reasoning from the KB.

## The Mechanism

**Step 1: The POOM is a multimap.**
[SS-POOM-MULTIMAP] documents that a single I-address can legitimately appear at multiple V-positions within the same document. The search function `findcbcinarea2d()` traverses all siblings, accumulating every matching leaf. `incontextlistnd()` inserts each found context into a sorted linked list and *never replaces existing entries*. So when a self-transclusion places I-addresses i₁..i₄ at both V 1.10 and V 1.19, the POOM contains two separate crums referencing those same I-addresses.

**Step 2: V→I conversion returns one I-span per contiguous I-address region.**
[ST-LINK-CREATE / Finding 0037] is explicit: `vspanset2sporglset` calls `vspanset2ispanset` → `permute` → `span2spanset` → `retrieverestricted`, which "finds all contiguous I-regions" by traversing the POOM context list. If the from-set V-span covers both V 1.10–1.13 and V 1.19–1.22, the POOM traversal yields **two** context entries both pointing to I-addresses i₁..i₄. These are two separate, non-consolidated context results because the POOM multimap returns each V-position hit independently.

**Step 3: The inner loop creates one sporgl per I-span, without deduplication.**
The inner loop at `sporgl.c:49-58` [ST-LINK-CREATE / Finding 0037] iterates over every `typeispan` struct in the ispanset and creates a distinct sporgl for each. There is no deduplication step. Two I-spans with identical origins produce two sporgls with identical `sporglorigin` values.

## The Consequence for Link Counting

When these two sporgls are fed into the spanfilade search (for `find_links`) or insertion (for `create_link`):

- **For `create_link`**: [SS-SPANF-OPERATIONS / Finding 0012] `insertspanf` makes one `insertnd` call per sporgl. Two identical sporgls produce two index entries for the same I-address range → same link ISA inserted twice under the same I-addresses.
- **For `find_links`**: [SS-FIND-LINKS / Finding 0028] The search converts the query specset to I-spans and checks intersection. Two overlapping I-spans in the query will each independently intersect the spanfilade entries, and `intersectlinksets` [EC-FIND-LINKS-GLOBAL / Finding 0069, also Finding 0035] processes each hit separately. The same link can appear in results twice.

## Observed Evidence of the Pattern

The KB documents this duplication concretely in adjacent scenarios:

- **[EC-PIVOT-LINK-FRAGMENTATION]** (Finding 0019): After a pivot rearranges linked content, `find_links` returns the *same link twice*, and `retrieve_endsets` returns duplicated spans. The KB notes this "may reflect the internal representation of fragmented spans."
- **[EC-MULTISPAN-LINK-DUPLICATION]** (Finding 0019): A link created with two source spans has endsets that return 3 spans where one span appears twice. The KB explicitly attributes this to the same internal fragmentation mechanism.

Both of those cases arise from the same root cause as self-transclusion: non-contiguous (or repeated) I-address regions in the input causing `vspanset2sporglset` to emit multiple sporgls covering the same I-address range.

## Summary

The KB does not describe a deduplication pass anywhere in the `vspanset2sporglset` → sporglset → spanfilade path. Given [SS-POOM-MULTIMAP]'s confirmation that the POOM's traversal accumulates all matching contexts without replacement, and [ST-LINK-CREATE / Finding 0037]'s confirmation that one sporgl is created per I-span in the result, the answer is: yes, when the from-set V-span covers V-positions that share I-addresses due to self-transclusion, `vspanset2sporglset` produces overlapping sporgls, and the same link can be returned more than once in `find_links` results — exactly the duplication already documented in [EC-MULTISPAN-LINK-DUPLICATION] and [EC-PIVOT-LINK-FRAGMENTATION].

---

## Code Exploration

I now have all the code I need. Here is the complete answer.

---

## Does `vspanset2sporglset` produce overlapping I-spans under self-transclusion?

**Yes.** There are four compounding failures in the call chain. No stage deduplicates the I-spans, and the one place that tries (`onlinklist`) has a loop bug that silently misses the most-recent entry.

---

### The scenario

Self-transclusion means the same permascroll I-addresses appear at two or more V-positions inside one document. A V-span query whose range covers both V-positions must map back to the same I-span twice. The question is whether any code notices and collapses that.

---

### Stage 1 — `findcbcinarea2d` produces two contexts for the same I-span

`vspanset2sporglset` [sporgl.c:35] calls `vspanset2ispanset` [orglinks.c:397], which calls `permute` [orglinks.c:404], which calls `span2spanset` [orglinks.c:425] for every V-span in the input.

`span2spanset` calls `retrieverestricted` on the POOM enfilade [orglinks.c:435], which calls `retrieveinarea` → `findcbcinarea2d` [retrie.c:229]. That function walks every height-0 POOM crum that qualifies in the 2D area and calls `makecontextfromcbc` + `incontextlistnd` [retrie.c:260–264]:

```c
} else {
    context = makecontextfromcbc ((typecbc*)crumptr, (typewid*)offsetptr);
    incontextlistnd (headptr, context, index1);
}
```

`incontextlistnd` [context.c:75] inserts the new context into a sorted list by offset. It does **not** check for contexts that describe the same I-range. Under self-transclusion, two leaf crums in the POOM are visited (same I-span, different V-positions); both produce a context entry, and both are inserted.

---

### Stage 2 — `span2spanset` / `onitemlist` appends without deduplication

Back in `span2spanset` [orglinks.c:439–445]:

```c
for (c = context; c; c = c->nextcontext) {
    context2span (c, restrictionspanptr, restrictionindex, &foundspan, targindex);
    nextptr = (typespan *)onitemlist (taskptr, (typeitem*)&foundspan, (typeitemset*)targspansetptr);
}
```

`context2span` [context.c:176] clips the found I-span to the requested V-intersection, producing an `ISPANID` item. For both contexts (the two transclusions), the clipping arithmetic yields the **same I-span**.

`onitemlist` [orglinks.c:464–536] for the `ISPANID` case:

```c
case ISPANID:
    newitem = (typeitem *) taskalloc(taskptr, sizeof(typeispan));
    movmem (itemptr, newitem, sizeof(typeispan));
    break;
```

…then unconditionally appends to the tail:

```c
((typeitemheader *)temp)->next = (typeitemheader *)newitem;
```

There is **no equality check** in `onitemlist`. The same I-span (identical `stream` and `width` tumblers) is appended twice. The returned `ispanset` contains the I-span duplicated.

---

### Stage 3 — `vspanset2sporglset` creates a sporgl node for every I-span, including duplicates

[sporgl.c:47–58]:

```c
for (; vspanset; vspanset = vspanset->next) {
    (void) vspanset2ispanset (taskptr, orgl, vspanset, &ispanset);
    for (; ispanset; ispanset = ispanset->next) {
       sporglset = (typesporgl *) taskalloc (taskptr, sizeof(typesporgl));
       sporglset->itemid = SPORGLID;
       sporglset->next = NULL;
       movetumbler (docisa, &sporglset->sporgladdress);
       movetumbler(&ispanset->stream, &sporglset->sporglorigin);
       movetumbler (&ispanset->width, &sporglset->sporglwidth);
       *sporglsetptr = (typesporglset)sporglset;
       sporglsetptr = (typesporglset *)&sporglset->next;
    }
}
```

Both I-span entries in `ispanset` get their own `typesporgl` node. The resulting sporglset contains two structurally identical entries (same `sporgladdress`, `sporglorigin`, `sporglwidth`).

---

### Stage 4 — `sporglset2linksetinrange` queries the spanfilade once per sporgl, hitting the same link twice

[sporgl.c:250–268]:

```c
for (; sporglset; sporglset = (typesporglset)((typeitemheader *)sporglset)->next) {
    ...
    context = retrieverestricted (spanfptr, (typespan*)sporglset, SPANRANGE, &range, ORGLRANGE, (typeisa*)infoptr);
    for (c = context; c; c = c->nextcontext) {
        beheadtumbler(&c->totaloffset.dsas[ORGLRANGE], &linksa);
        onlinklist (taskptr, linksetptr, &linksa);
    }
    contextfree (context);
}
```

With two identical sporgl entries, `retrieverestricted` is called twice with the same I-span coordinates. Both calls find the same link in the spanfilade. `onlinklist` is therefore called twice with the same `linksa` tumbler.

---

### Stage 5 — `onlinklist` fails to deduplicate when the match is the last element

[spanf2.c:26–44]:

```c
bool onlinklist(typetask *taskptr, typelinkset *linksetptr, typeisa *linkisaptr)
{
  typelink *linkset, *temp, *nextlink;
  typelink *makelinkitem();

    linkset = makelinkitem (taskptr, linkisaptr);   // allocated unconditionally

    if (*linksetptr == NULL) {
        *linksetptr = linkset;
        return(0);
    }

    for (temp = *linksetptr; nextlink = temp->next; temp = nextlink) {
        if (tumblereq (&temp->address, linkisaptr))
            return(0);
    }

    temp->next = linkset;
}
```

The loop condition is `nextlink = temp->next`. When `temp` is the **last element** (its `next` is `NULL`), the condition evaluates to `NULL` (falsy), and the loop exits — **without ever checking `temp->address`**. The dedup check only runs while there is a successor. So the most-recently added link is never checked.

Under self-transclusion: the first sporgl pass adds LINK to the list (list = `[LINK]`). The second pass enters `onlinklist` with the same `linkisaptr`:
- `temp = LINK`, `nextlink = LINK->next = NULL` → loop exits immediately
- `temp->next = linkset` — duplicate appended (list = `[LINK, LINK]`)

The dedup guard in `onlinklist` is sound for interior elements only. It systematically fails for the most-recent addition, which is exactly the case produced by duplicate sporgls.

---

### Effect on link counting

`dofindnumoflinksfromtothree` [do1.c:355] delegates to `findnumoflinksfromtothreesp` [spanf1.c:105–115]:

```c
for (n = 0; linkset; linkset = linkset->next, ++n);
*numptr = n;
```

It counts every node in the linkset. With `k` transcluded copies of the same I-span in the from-set, a link whose from-end touches those addresses is counted up to `k` times.

`intersectlinksets` [spanf2.c:46–119] provides no relief. When only `fromlinkset` is non-NULL it takes the early return path [spanf2.c:64–65]:

```c
if (linkset1 && !linkset2 && !linkset3)
    *linkset4ptr = linkset1;
```

…returning the list as-is. The cross-set intersection loops (lines 96–118) also do not deduplicate within a single set.

---

### Summary

| Stage | File | Lines | What happens |
|---|---|---|---|
| `findcbcinarea2d` walks two POOM crums | retrie.c | 252–264 | Produces 2 contexts for same I-range |
| `onitemlist` appends without check | orglinks.c | 516–534 | Duplicates I-span in `ispanset` |
| `vspanset2sporglset` inner loop | sporgl.c | 49–58 | Duplicates I-span into sporgl list |
| `sporglset2linksetinrange` outer loop | sporgl.c | 250–268 | Queries spanfilade twice for same I-span |
| `onlinklist` loop misses last element | spanf2.c | 38–43 | Dedup silently fails; link appended twice |
| `findnumoflinksfromtothreesp` counts nodes | spanf1.c | 112 | Overcounts by factor of `k` transclusions |

`vspanset2sporglset` does produce overlapping (identical) I-spans when the same permascroll addresses appear at multiple V-positions. No stage in the pipeline between that function and the final link count detects or collapses them. The same link is counted once per transcluded copy of the I-span in the from-set.
