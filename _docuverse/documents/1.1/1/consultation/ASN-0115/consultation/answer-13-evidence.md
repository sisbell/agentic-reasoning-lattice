## Question 13 [evidence]

> For a VSpec whose V-range maps to non-contiguous I-addresses (e.g. across a CREATELINK allocation gap), is the returned content split into multiple segments or concatenated as one contiguous byte run?

## KB Synthesis

## Content Retrieval Across I-Address Gaps

**Short answer: multiple segments, one per contiguous I-address run.**

### The retrieval path

`doretrievev` (FEBE opcode 5) executes a two-step pipeline [PRE-RETRIEVE-CONTENTS]:

1. `specset2ispanset` — walks the POOM to convert V-addresses to I-addresses. When the V-range covers two POOM crums with non-contiguous I-address origins (e.g. crum₁: V 1.1–1.3 → I α.1–α.3, crum₂: V 1.4–1.6 → I β.1–β.3), the result is **two I-spans**.

2. `ispanset2vstuffset(taskptr, granf, ispanset, vstuffsetptr)` — dereferences each I-span independently from the permascroll B-tree and deposits separate `typegrantext` atoms into the `vstuffset` [SS-GRANF-OPERATIONS]. There is no concatenation step in this function.

### Why the gap is preserved

The CREATELINK operation allocates a link-orgl I-address between the two text insertions, advancing the global allocation counter [INT-LINK-INSERT, INV-MONOTONIC]. This leaves the two text blocks at non-adjacent I-address ranges, even though their V-addresses are contiguous.

The POOM stores separate crums for each contiguous (V, I) block. `specset2ispanset` iterates the POOM contexts and emits one I-span per contiguous run — the same splitting logic that operates during link creation [ST-LINK-CREATE, Finding 0037]: *"one I-span per contiguous I-address region."*

### Corroborating evidence

- [INT-LINK-INSERT] / Finding 0063: INSERT "ABC" → CREATELINK → INSERT "DEF" produces **two shared span pairs** under `compare_versions`, not one. The I-address discontinuity is semantically observable and preserved through all downstream operations.
- [SS-SPECSET]: *"Retrieve concatenates content in VSpec order"* — concatenation is defined **across VSpecs** in a SpecSet, not within a single VSpec across I-space gaps.
- [INV-VSPAN-CONSOLIDATION]: The POOM consolidates *V-space* adjacency, not I-space adjacency. A V-range 1.1–1.6 returns as one V-span, but its underlying I-spans are not merged.

### What the client receives

The `vstuffset` preserves the segment structure. The FEBE protocol returns it as a collection of content atoms. For V-range [1.1, 1.6) mapping to I {α.1–α.3, β.1–β.3}, the client receives two content items — "ABC" and "DEF" — not one "ABCDEF".

---

## Code Exploration

I have all the evidence. Here is the full answer:

---

## Answer: Multiple Segments, Not Concatenated

When a VSpec's V-range maps to non-contiguous I-addresses, the backend returns **multiple separate text items in a linked list** — one per contiguous region — with no concatenation at any stage of the pipeline.

---

## Full Execution Trace

### 1. Entry point — `fns.c:175`

```c
void retrievev(typetask *taskptr)
{
  typespecset specset;
  typevstuffset vstuffset;
  ...
  if (getretrievev(taskptr, &specset)
  && doretrievev(taskptr, specset, &vstuffset))
      putretrievev(taskptr, &vstuffset);
```

`doretrievev` assembles the result into `vstuffset`; `putretrievev` serializes it.

---

### 2. V→I address mapping — `orglinks.c:397`

```c
typeispanset *vspanset2ispanset(typetask *taskptr, typeorgl orgl,
    typevspanset vspanptr, typeispanset *ispansetptr)
{
    return permute(taskptr, orgl, vspanptr, V, ispansetptr, I);
}
```

`permute` (`orglinks.c:404`) iterates each vspan and calls `span2spanset` (`orglinks.c:425`), which calls `retrieverestricted` to walk the POOM enfilade and collect every I-address region that the V-range covers. If the V-range spans a CREATELINK allocation gap, the POOM walk produces **multiple disjoint `typespan` entries** — one per contiguous I-region. These are linked together into `ispanset` as separate items.

---

### 3. I-span → vstuff expansion — `granf1.c:58`

```c
bool ispanset2vstuffset(typetask *taskptr, typegranf granfptr,
    typeispanset ispanset, typevstuffset *vstuffsetptr)
{
    *vstuffsetptr = NULL;
    for (; ispanset; ispanset = ispanset->next) {
        vstuffsetptr = ispan2vstuffset(taskptr, granfptr, ispanset, vstuffsetptr);
    }
    return (TRUE);
}
```

Each I-span is processed separately. There is no merging step.

---

### 4. Per-span granfilade retrieval — `granf2.c:286`

```c
typevstuffset *ispan2vstuffset(typetask *taskptr, typegranf fullcrumptr,
    typeispan *ispanptr, typevstuffset *vstuffsetptr)
{
    ...
    context = retrieveinspan((typecuc*)fullcrumptr, &lowerbound, &upperbound, WIDTH);

    for (temp = context; temp; temp = temp->nextcontext) {
        if (context2vstuff(taskptr, temp, ispanptr, &vstuffset)) {
            *vstuffsetptr = vstuffset;
            vstuffsetptr = (typevstuffset *)&((typeitemheader *)vstuffset)->next;
        }
    }
    contextfree(context);
    return (vstuffsetptr);
}
```

`retrieveinspan` returns a linked list of `typecontext` nodes (one per leaf crum that intersects the span). Each is converted to a separate vstuff item and chained via `->next`. **No concatenation occurs.**

---

### 5. Enfilade traversal that produces the context list — `retrie.c:307`

```c
int findcbcinspanseq(typecorecrum *crumptr, typewid *offsetptr,
    tumbler *spanstart, tumbler *spanend, typecontext **headptr)
{
    movewisp(offsetptr, &localoffset);
    for (; crumptr; crumptr = getrightbro(crumptr)) {
        if (!crumintersectsspanseq(crumptr, (tumbler*)&localoffset, spanstart, spanend)) {
            dspadd(&localoffset, &crumptr->cwid, &localoffset, (INT)crumptr->cenftype);
            continue;                        // skip: gap or out-of-range
        }
        if (crumptr->height == 0) {
            context = makecontextfromcbc((typecbc*)crumptr, offsetptr);
            oncontextlistseq(headptr, context); // append separate segment
        } else {
            findcbcinspanseq(findleftson((typecuc*)crumptr), &localoffset,
                spanstart, spanend, headptr);
        }
        dspadd(&localoffset, &crumptr->cwid, &localoffset, (INT)crumptr->cenftype);
    }
}
```

Every leaf crum that intersects the span gets its own `typecontext` appended via `oncontextlistseq` (`context.c:113`). Crums outside the span (i.e. the allocation gap) are silently skipped with `continue`. The gap does not produce a placeholder, a zero-fill, or any kind of merged output — it simply means the two adjacent crums produce two separate context entries.

---

### 6. Serialization — `putfe.c:270`, `put.c:60`

```c
// putfe.c:270
int putretrievev(typetask *taskptr, typevstuffset *vstuffsetptr)
{
    putnumber(taskptr->outp, RETRIEVEV);
    putitemset(taskptr, (typeitemset)*vstuffsetptr);
}

// put.c:60 — putitemset iterates the linked list, calling puttext per item
for (; itemset; itemset = (typeitemset)((typeitemheader *)itemset)->next) {
    putitem(taskptr, itemset);
    if (!(next && itemid == TEXTID && next->itemid == TEXTID))
        putc('\n', taskptr->outp);
}
```

Note the newline-suppression condition (`put.c:68`): between consecutive TEXTID items, the protocol omits the newline delimiter. Each segment's raw bytes are still written individually via `puttext` → `write(fileno(taskptr->outp), textptr->string, textptr->length)` (`put.c:125`). This formatting quirk means adjacent text segments are emitted back-to-back on the wire without a separator, but they remain **distinct items in the vstuffset linked list** — the client receives and parses them as separate entries.

---

## Summary

| Stage | Behavior |
|---|---|
| POOM permute (`orglinks.c:404`) | One I-span per contiguous V-region; gap produces split here |
| `ispanset2vstuffset` (`granf1.c:58`) | Iterates I-spans separately, no merge |
| `findcbcinspanseq` (`retrie.c:307`) | Leaf crums across gap become separate `typecontext` nodes |
| `ispan2vstuffset` (`granf2.c:302`) | Each context → separate vstuff item chained via `->next` |
| `putitemset` (`put.c:66`) | Serializes each item; no byte-merging, only newline suppression between adjacent TEXTID items |

**The returned content is split into multiple segments** — one per contiguous I-address run — returned as a linked list of `typetext` items. The gap itself produces no output (no zero-fill, no placeholder). There is no concatenation at any point in `do2.c`, `granf1.c`, `granf2.c`, `retrie.c`, or `put.c`.
