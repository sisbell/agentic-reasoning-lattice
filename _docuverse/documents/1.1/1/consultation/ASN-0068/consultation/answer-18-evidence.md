## Question 18 [evidence]

> For the `correspond.c` link-subspace crash [EC-COMPARE-CRASH], does the crash occur during I-address extraction from link orgls, or during the V-position back-mapping phase when link I-addresses fail the permascroll lookup?

## KB Synthesis

The crash occurs in the **intersection/back-mapping phase** inside `correspond.c`, not during I-address extraction.

Here's why:

**I-address extraction succeeds silently.** The `vspanset2ispanset` → `permute` → `retrieverestricted` pipeline is type-agnostic [SS-SUBSPACE-CONVENTION, Finding 0010]. It extracts link orgl ISAs from the `2.x` V-subspace just as happily as permascroll addresses from `1.x`. No error is raised at this stage.

**The crash is structural, not a lookup failure.** Finding 0009 [EC-COMPARE-VERSIONS-LINK-CRASH, PRE-COMPARE-VERSIONS] identifies two failure modes in `correspond.c`'s nested loop:

1. Link orgl ISAs occupy a completely different address range from permascroll I-addresses. They will **never intersect** with text I-addresses from the other document. `correspond.c` does not handle the resulting empty-intersection case gracefully — the loop assumes some match exists and crashes when none is found.

2. The nested loop assumes each ispan matches **at most one vspec**. The link subspace structure violates this assumption, breaking the loop invariant.

The permascroll lookup failure path [PRE-RETRIEVE-CONTENTS] is a distinct phenomenon: that's `ispanset2vstuffset` trying to dereference a link ISA in the permascroll (producing garbage), which is a **silent** corruption, not a crash. `correspond.c` crashes earlier, before any permascroll content lookup would occur, because the intersection logic itself cannot cope with the empty or structurally unexpected I-span results.

The fix implied by [PRE-COMPARE-VERSIONS] (Finding 0015) is a pre-filter step — strip the `2.x` subspace before entering `correspond.c` — confirming the crash site is the intersection logic, not the extraction or lookup phases.

---

## Code Exploration

Now I have everything needed. Let me synthesize the full answer from direct code reading.

---

## EC-COMPARE-CRASH: Crash Site Analysis

The crash occurs **during the V-position back-mapping phase**, not during I-address extraction. Here is the precise execution trace from source.

---

### Phase A: I-Address Extraction — Does NOT Crash

`specset2ispanset()` [`do2.c:36`] calls `vspanset2ispanset()` on the full document vspanset, which includes the normalized link span `at 0 for 0.1`. This calls `permute()` → `span2spanset()` [`orglinks.c:425`]:

```c
// orglinks.c:435
context = retrieverestricted((typecuc*)orgl, restrictionspanptr, restrictionindex,
                              (typespan*)NULL, targindex, (typeisa*)NULL);
// orglinks.c:446-448
if(!context){
    return(targspansetptr);   // ← safe exit, no crash
}
```

The link V-span `[0, 0.1)` (normalized display artifact from `retrievevspansetpm()`, `orglinks.c:197-203`) maps to **nothing** in the POOM. Link crums are stored internally at V-positions `1.n` (FROM) and `2.n` (TO), per `setlinkvsas()` [`do2.c:169-183`] and `islinkcrum()` [`orglinks.c:257`]:

```c
// orglinks.c:257 — link crums have mantissa[0]=1, mantissa[1]≠0
bool islinkcrum(typecorecrum *crumptr) {
    if(crumptr->cdsp.dsas[V].mantissa[0] == 1 && crumptr->cdsp.dsas[V].mantissa[1] != 0)
        return TRUE;
```

No crum has V-displacement in `[0, 0.1)`. `retrieverestricted()` returns NULL context. `span2spanset()` hits the guard at `orglinks.c:446-448` and returns `targspansetptr` unchanged — **safe, no crash**.

Result: the original document's ispanset contains **only text I-spans**. The common ispanset is therefore also purely text I-spans. Link ISA I-addresses never appear in it.

---

### Phase B: V-Position Back-Mapping — THIS IS THE CRASH SITE

`restrictspecsetsaccordingtoispans()` [`correspond.c:26`] calls `restrictvspecsetovercommonispans()`, which executes:

```c
// correspond.c:73-81
docvspanset = NULL;
if(ispan2vspanset(taskptr,versionorgl,ispanset,&docvspanset)){   // Bug 2
    s1=(typevspec *)taskalloc(taskptr,sizeof(typevspec ));
    s1->itemid = VSPECID;
    *newspecsetptr = (typespecset)s1;
    movetumbler (&((typevspec *)specset)->docisa, &s1->docisa);
    s1->vspanset = docvspanset;    // ← may be NULL
    newspecsetptr = (typespecset *)&s1->next;
}
```

**Bug 2** [`bugs/0009-compare-versions-crashes-with-links-ROOT-CAUSE.md`]: `ispan2vspanset()` returns `permute()`'s `save` value, which is `targspansetptr = &docvspanset` — a stack address, **never NULL**:

```c
// orglinks.c:389-394
typevspanset *ispan2vspanset(..., typevspanset *vspansetptr) {
    return permute(taskptr, orgl, ispanptr, I, vspansetptr, V);
}
// orglinks.c:408
save = targspansetptr;   // = &docvspanset (stack address)
...
return (save);           // always non-NULL
```

The `if` at `correspond.c:74` **always evaluates true**, even when `docvspanset` is NULL. A `typevspec` is created at `correspond.c:75-80` with `s1->vspanset = NULL`.

This NULL vspanset then propagates to `removespansnotinoriginal()` at `correspond.c:30`, which calls:

```c
// correspond.c:116 (pre-fix)
if (intersectspansets (taskptr,
    ((typevspec *)new)->vspanset,    // ← NULL
    ((typevspec *)old)->vspanset,
    &newspanset, VSPANID)) {
```

Pre-fix, `intersectspansets()` was not guarded for NULL inputs. The call with a NULL `set1` triggered `gerror("")` → `abort()` → **SIGABRT**.

The Bug 009 fix at `correspond.c:164-168` added the guard:

```c
// Bug 009 fix: NULL inputs are now handled gracefully
if (!set1 || !set2) {
    return (TRUE);
}
```

---

### Why "Link I-Addresses Fail the Permascroll Lookup" Is Phase B, Not Phase A

The permascroll lookup failure happens inside `ispan2vspanset()` during Phase B: `span2spanset()` calls `retrieverestricted()` at `orglinks.c:435` searching the POOM for crums whose I-dimension falls within the common I-span. When the specset contains a vspec whose `docisa` is a link orgl ISA (rather than a document orgl ISA), `findorgl()` at `correspond.c:67` returns the **link's POOM**, not the document's POOM. The link POOM contains only link endpoint crums with link ISA I-addresses — not permascroll text I-addresses — so `retrieverestricted()` returns NULL context. The guard at `orglinks.c:446-448` fires, `docvspanset` stays NULL, and Bug 2 allows a NULL vspanset through.

---

### Summary of Crash Path

| Step | Location | Event |
|------|----------|-------|
| Phase A | `orglinks.c:446` | NULL context from link V-span → safe early return |
| Phase B entry | `correspond.c:74` | `ispan2vspanset()` called |
| Permascroll lookup | `orglinks.c:435` | `retrieverestricted()` returns NULL for link I-addresses |
| Safe guard | `orglinks.c:446-448` | `targspansetptr` returned unchanged; `docvspanset` stays NULL |
| **Bug 2** | `correspond.c:74` | `if(ispan2vspanset(...))` always TRUE — NULL `docvspanset` passes the gate |
| Vspec creation | `correspond.c:79` | `s1->vspanset = NULL` |
| **Crash site** | `correspond.c:116` | `intersectspansets()` called with NULL set1 → `gerror("")` → abort |

The crash is unambiguously in **Phase B (V-position back-mapping)** at `correspond.c:74-79` via Bug 2's return-value misuse. Phase A's null-context path is correctly guarded at `orglinks.c:446-448` and does not crash.
