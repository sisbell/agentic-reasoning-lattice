## Question 14 [gregory]

> Does REARRANGE create, modify, or remove any spanfilade entries, or does it exclusively mutate the document's POOM while leaving the spanfilade and granfilade completely untouched?

## KB Synthesis

REARRANGE exclusively mutates the document's POOM and leaves both the spanfilade and the granfilade's content layer completely untouched.

**What REARRANGE actually does**

REARRANGE operates on the POOM by computing displacement offsets from the cut positions and applying them via `tumbleradd` to the V-address component (`cdsp.dsas[V]`) of affected orgl entries [ST-REARRANGE]. The I-address component (`cdsp.dsas[I]`) is never modified. No new I-addresses are allocated, no permascroll entries are created, and no enfilade nodes are freed or replaced — only V-position values shift [INV-REARRANGE-IDENTITY].

**Spanfilade: completely untouched**

The spanfilade contains two structures: the link endpoint index (I-address → link ISA) and the DOCISPAN index (I-address → document ISA). REARRANGE calls neither `insertspanf` nor any removal function from the spanf codebase. This matches the general pattern established for all non-insert operations: `rearrangend` (like `deletend`) operates exclusively on the document's orgl enfilade (POOM layer) with no calls to spanf functions [INV-SPANF-WRITE-ONLY, FC-CONTENT-SPANF-ISOLATION].

Because I-addresses are unchanged, the DOCISPAN entries correctly continue to assert that the document contains those I-addresses — no entries become stale, and no new entries are needed. Link endpoint entries likewise remain valid since the links reference I-addresses, not V-positions [INV-REARRANGE-LINK-SURVIVAL].

**Granfilade content: completely untouched**

The granfilade's content layer (permascroll text atoms, link orgls) is frame-preserved by REARRANGE. The explicit frame condition is: `∀ op ∈ {DELETE, REARRANGE} : granf_content_after(op) = granf_content_before(op)` [FC-GRANF-ON-DELETE]. REARRANGE is grouped with DELETE in this invariant — neither creates new I-addresses, neither frees permascroll content. This is observable: `compare_versions` before and after a rearrange reports all content as shared (same I-addresses), confirming zero granfilade change [INV-REARRANGE-IDENTITY, Finding 0018].

**Implication for link discovery**

Since the spanfilade is unmodified, `find_links` results are invariant under REARRANGE. Links bound to rearranged content remain discoverable because they are indexed by I-address, which REARRANGE never changes [INV-REARRANGE-LINK-SURVIVAL]. The V-position rendering of link endpoints will shift (resolved through the updated POOM), but the underlying link objects and their I-address-based discoverability are unaffected.

**Summary**

| Layer | Effect of REARRANGE |
|-------|-------------------|
| POOM (V→I mappings) | Modified — V-displacements shifted |
| Granfilade content (permascroll/orgls) | Unchanged — no allocation or deletion |
| Spanfilade link index | Unchanged — no insertspanf calls |
| Spanfilade DOCISPAN index | Unchanged — no insertspanf calls |

---

## Code Exploration

I now have all the evidence needed. Here is the complete analysis.

---

## Answer: REARRANGE Exclusively Mutates the POOM

REARRANGE does **not** create, modify, or remove any spanfilade or granfilade entries. It is a pure POOM mutation. Here is the proof by complete call-chain tracing.

---

### 1. The Entry Point: `dorearrange` — No Spanfilade Touch

`do1.c:34-43`:
```c
bool dorearrange(typetask *taskptr, typeisa *docisaptr, typecutseq *cutseqptr)
{
  typeorgl docorgl;
  bool findorgl(), rearrangepm();;

    return (
       findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
    && rearrangepm (taskptr, docisaptr, docorgl, cutseqptr)
    /*&& TRUE*/ /* ht stuff */  );
}
```

Compare this to `docopy` at `do1.c:53-65`, which explicitly calls **both** `insertpm` (POOM) and `insertspanf` (spanfilade), or `docreatelink` at `do1.c:219` which calls `insertendsetsinspanf`. `dorearrange` calls neither. There is no reference to `spanf` at this level.

---

### 2. `rearrangepm` — Calls Only `rearrangend` on the POOM

`orglinks.c:137-142`:
```c
bool rearrangepm(typetask *taskptr, tumbler *docisaptr, typeorgl docorgl, typecutseq *cutseqptr)
{
    rearrangend((typecuc*)docorgl, cutseqptr, V);
    logbertmodified(docisaptr, user);
    return (TRUE);
}
```

`docorgl` is the **POOM enfilade root** returned from `findorgl(taskptr, granf, ...)`. It is passed directly to `rearrangend`. There is no `spanf` reference anywhere in this function.

Compare to `deletevspanpm` immediately below at `orglinks.c:145-152`, which calls `deletend((typecuc*)docorgl, ...)` on the same POOM root. Neither delete nor rearrange touches the spanfilade; only insert/copy operations do.

---

### 3. `rearrangend` — Operates Entirely Within the Passed POOM Tree

`edit.c:78-160`. The function signature:
```c
int rearrangend(typecuc *fullcrumptr, typecutseq *cutseqptr, INT index)
```

`fullcrumptr` is `docorgl` — the POOM root. Every operation inside touches only this tree:

| Operation | Where | What it touches |
|---|---|---|
| `makecutsnd(fullcrumptr, &knives)` | `ndcuts.c:15` | Splits POOM crums at cut boundaries |
| `newfindintersectionnd(fullcrumptr, ...)` | `ndinters.c:38-42` | Returns `fullcrumptr` itself (trivially) |
| `rearrangecutsectionnd(ptr, ...)` | `edit.c:191` | Classifies POOM child nodes |
| `tumbleradd(&ptr->cdsp.dsas[index], ...)` | `edit.c:125` | Adjusts V-axis offsets in POOM nodes |
| `ivemodified((typecorecrum*)ptr)` | `edit.c:127` | Marks POOM nodes dirty |
| `setwispupwards(father, 1)` | `edit.c:137` | Propagates POOM wid sums upward |
| `recombine(fullcrumptr)` | `edit.c:139` | Merges POOM nodes |
| `splitcrumupwards(fullcrumptr)` | `edit.c:141` | Splits over-full POOM nodes |

There is no reference to `spanf`, `granf`, or any other global enfilade pointer within `rearrangend`.

---

### 4. `findfullcrum` Cannot Escape the POOM Apex

`makecutsnd` at `ndcuts.c:24` loops using `findfullcrum`:
```c
for (fullcrumptr = findfullcrum((typecorecrum*)fullcrumptr); sonsarecut(...); ...)
```

`findfullcrum` is defined at `genf.c:89-95`:
```c
typecuc *findfullcrum(typecorecrum *descendant)
{
    for (ptr = (typecuc*)descendant; !isfullcrum((typecorecrum*)ptr); ptr = findfather((typecorecrum*)ptr));
    return (ptr);
}
```

And `isfullcrum` is defined at `enf.h:176`:
```c
#define isfullcrum(x) ((bool)((typecorecrum *)(x))->isapex)
```

`docorgl` is the POOM apex (`isapex == TRUE`). `findfullcrum` called on it returns immediately — the loop never walks upward into a parent structure. All `makecutsnd` iterations stay within the POOM tree rooted at `docorgl`.

---

### 5. `splitcrum` and `recombine` Dispatch on `cenftype` — Stay POOM

`recombine` at `recombine.c:22-34` dispatches:
```c
case POOM:
    recombinend (father);
```

`splitcrum` at `split.c:49-66` dispatches:
```c
case POOM:
    splitcrumpm(father);
```

`splitcrumpm` at `split.c:117-128` calls `peelcrumoffnd`, which creates new crums via `createcrum((INT)father->height, (INT)father->cenftype)` — the `cenftype` is `POOM`, so all newly created crums are POOM crums, adopted into the POOM tree.

Similarly `makecutsbackuptohere` at `ndcuts.c:80` creates new crums with `createcrum((INT)ptr->height, (INT)ptr->cenftype)` — same `cenftype` inheritance, all POOM.

---

### Conclusion

REARRANGE is a **pure POOM mutation**. It repositions sections of content within the document's V-space by:
1. Slicing the POOM at the specified cut positions (`makecutsnd`)
2. Adjusting the V-axis displacement (`cdsp.dsas[V]`) of the nodes that fall in each cut section (`tumbleradd`)
3. Rebalancing the POOM tree (`recombine`, `splitcrumupwards`)

The spanfilade records which I-spans (permascroll addresses) are endpoints of which links in which documents. REARRANGE changes where content sits in V-space but does **not** change the underlying permascroll addresses — the I-spans are stable. Therefore it is both mechanically correct (no `spanf` pointer is ever referenced) and semantically correct (the spanfilade's invariants are not disturbed) that the spanfilade and granfilade are completely untouched.
