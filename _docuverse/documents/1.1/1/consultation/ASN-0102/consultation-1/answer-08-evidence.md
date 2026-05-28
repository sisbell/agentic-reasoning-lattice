## Question 8 [evidence]

> Does `insertspanf`/`docopy` coalesce I-adjacent, V-adjacent spans across distinct content references into a single entry, or always emit one span entry per resolved run regardless of inter-reference I-adjacency?

## KB Synthesis

**No coalescing across distinct content references.** `insertspanf` always emits one DOCISPAN entry per `typeispan` struct in the input list, and that list is built from individual POOM crums without cross-crum merging during retrieval.

The evidence chain:

**`insertspanf` is a pass-through loop.** [SS-DOCISPAN] Finding 0047: "`insertspanf` loops over the `ispanset` linked list and makes one `insertnd` call per `typeispan` struct." The granularity arriving at `insertspanf` determines the output count exactly — there is no merger step inside it.

**I-span count equals POOM crum count.** The input is produced by `vspanset2ispanset` → `permute` → `span2spanset`, which walks the POOM crum context list (sorted by V-position per [SS-CONTEXT-LIST] Finding 0078) and emits one I-span per crum. No crum-merging occurs on the retrieval path.

**POOM crums from distinct references are never merged.** [ST-VCOPY] Finding 0046: `isanextensionnd()` requires both same `homedoc` AND strict I/V contiguity before extending an existing crum during insertion. Crums from different source documents are structurally separate. Even same-homedoc crums created at non-contiguous cursor positions remain distinct.

**The coalescing that does exist is crum-internal and prior.** [ST-INSERT] Finding 0033 / Finding 0062: sequential inserts at the same cursor position are absorbed into one crum via the ONMYRIGHTBORDER + `isanextensionnd` path, so they appear as one I-span to `insertspanf`. But this is a POOM insertion-time effect, not a retrieval-time coalescing.

**Practical consequence:** Two COPY operations of I-numerically-adjacent source ranges (from different crums) produce two DOCISPAN entries. Only content that was inserted or copied in a single operation and consolidated into one POOM crum produces a single DOCISPAN entry. [SS-DOCISPAN] Finding 0047: "The granularity is determined by how `vspanset2ispanset` consolidates V-spans into I-spans before they reach `insertspanf`" — and that consolidation reflects POOM crum boundaries, not raw I-address adjacency.

---

## Code Exploration

I now have all the source verified. Here is the complete answer.

---

## Does `insertspanf`/`docopy` Coalesce Across Distinct Content References?

**No. The backend always emits one span crum per distinct content reference, regardless of I-adjacency or V-adjacency between runs. Coalescing is gated by a conjunctive check that fails if content references differ.**

---

### Execution Path

#### 1. `docopy` — `do1.c:45–65`

```c
bool docopy(typetask *taskptr, typeisa *docisaptr, tumbler *vsaptr, typespecset specset)
{
    return (
       specset2ispanset (taskptr, specset, &ispanset, NOBERTREQUIRED)    // line 54
    && findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)          // line 55
    && acceptablevsa (vsaptr, docorgl)                                    // line 56
    && insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset)           // line 60
    && insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN)        // line 62
    );
}
```

`docopy` converts the source specset to an ispanset and passes it to `insertspanf` without any pre-filtering or adjacency collapsing. The resolved ispanset preserves one entry per resolved run.

---

#### 2. `insertspanf` — `spanf1.c:15–54`

```c
bool insertspanf(typetask *taskptr, typespanf spanfptr, typeisa *isaptr,
                 typesporglset sporglset, INT spantype)
{
    prefixtumbler (isaptr, spantype, &crumorigin.dsas[ORGLRANGE]);  // line 22
    tumblerclear  (&crumwidth.dsas[ORGLRANGE]);                     // line 23
    clear (&linfo, sizeof(linfo));                                  // line 24

    for (; sporglset; sporglset = ...) {                            // line 25
        if (...ISPANID) {
            movetumbler (&..->stream,  &lstream);                   // line 27
            movetumbler (&..->width,   &lwidth);                    // line 28
            movetumbler (isaptr, &linfo.homedoc);                   // line 29  ← home doc = current doc
        } else if (...SPORGLID) {
            movetumbler (&..->sporglorigin,  &lstream);             // line 31
            movetumbler (&..->sporglwidth,   &lwidth);              // line 32
            movetumbler (&..->sporgladdress, &linfo.homedoc);       // line 33  ← home doc = source ref
        }
        movetumbler (&lstream, &crumorigin.dsas[SPANRANGE]);        // line 49
        movetumbler (&lwidth,  &crumwidth.dsas[SPANRANGE]);         // line 50
        insertnd(taskptr,(typecuc*)spanfptr,&crumorigin,&crumwidth,&linfo,SPANRANGE); // line 51
    }
}
```

**Critical observation:** Lines 25–51 show the loop iterates over every resolved run and issues an unconditional `insertnd` call for each one. There is **no look-ahead or look-back** to compare adjacent runs before dispatching. The content reference (`linfo.homedoc`) is set from `sporgladdress` for cross-document spans (`SPORGLID`, line 33) and from `isaptr` for intra-document spans (`ISPANID`, line 29). When two consecutive runs originate from different source documents, they carry different `homedoc` values.

---

#### 3. `insertcbcnd` → `isanextensionnd` — `insertnd.c:242–309`

This is where the only coalescing logic lives. `insertcbcnd` (`insertnd.c:242`) iterates the bottom-level crums and calls `isanextensionnd` before deciding whether to extend or create:

```c
INT insertcbcnd(typecuc *father, typedsp *grasp, typewid *origin,
                typewid *width, type2dbottomcruminfo *infoptr)
{
    for (ptr = findleftson(father); ptr; ptr = findrightbro(ptr)) {
        if (isanextensionnd((typecbc*)ptr, grasp, origin, infoptr)) {  // line 250
            dspadd(&ptr->cwid, width, &ptr->cwid, father->cenftype);   // line 251  ← extend
            ...
            return(FALSE);
        }
    }
    // No match: create a new crum
    new = createcrum(0, father->cenftype);                             // line 260
    ...
    move2dinfo(infoptr, &((type2dcbc *)new)->c2dinfo);                 // line 267
}
```

The extension-or-create decision is delegated entirely to `isanextensionnd`:

```c
bool isanextensionnd(typecbc *ptr, typedsp *offsetptr, typedsp *originptr,
                     type2dbottomcruminfo *infoptr)
{
    typedsp grasp, reach;
    if (!tumblereq(&infoptr->homedoc, &((type2dcbc *)ptr)->c2dinfo.homedoc))  // line 305
        return(FALSE);  // ← GATE 1: content references must match
    prologuend((typecorecrum*)ptr, offsetptr, &grasp, &reach);                 // line 307
    return(lockeq(reach.dsas, originptr->dsas, dspsize(ptr->cenftype)));       // line 308
    //           ← GATE 2: reach of existing crum == origin of new span (I-adjacent)
}
```

**Both gates must pass for coalescing to occur:**

| Gate | Check | Fails when |
|------|-------|-----------|
| Line 305 | `infoptr->homedoc == existing crum's homedoc` | Content references differ |
| Line 308 | `reach(existing crum) == origin(new span)` | Not I-adjacent |

If the content references differ — which is always the case when two runs come from distinct source documents (`sporgladdress` values differ, `linfo.homedoc` differs) — line 305 returns `FALSE` immediately. Gate 2 is never evaluated. A new crum entry is unconditionally created at line 260.

---

### Answer

`insertspanf`/`docopy` **always emits one span crum entry per distinct content reference**, regardless of whether adjacent runs are I-adjacent or V-adjacent in the target. Coalescing inside `insertcbcnd` (`insertnd.c:250`) requires **both** homedoc equality (`insertnd.c:305`) **and** I-adjacency (`insertnd.c:308`). Since distinct content references produce different `homedoc` values (set at `spanf1.c:33` for sporgls, `spanf1.c:29` for ispans), the first gate fails and a separate crum is always created. There is no cross-reference coalescing at any level of the call stack.
