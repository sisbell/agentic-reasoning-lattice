## Question 13 [evidence]

> Does `docreatelink` (or any other link-creation path in udanax-green) ever produce a link with empty from-endset or empty to-endset, and what does the implementation do if asked to?

## KB Synthesis

## Link Creation with Empty or Zero-Width Endsets

### Zero-width endpoints: crash

The KB is explicit on this case. `create_link` with a zero-width VSpec for either endpoint crashes the backend (Bug 0017):

> "create_link(home, source=Span(1.1, 0.0), target=Span(1.12, 0.0), type=T) → CRASH"

The implementation performs no graceful rejection — it aborts. The minimum valid width for any link endpoint is 1 character. [PRE-ZERO-WIDTH], [PRE-LINK-CREATE]

### Non-zero width referencing absent content: not documented

The formal precondition for `create_link` includes "source content exists AND target content exists" [PRE-LINK-CREATE]. The conversion chain `domakelink` → `vspanset2sporglset` → `vspanset2ispanset` → `permute` → `retrieverestricted` would silently drop any I-address with no POOM mapping [SS-FOLLOWLINK], [ST-LINK-CREATE]. However, the KB contains **no finding** documenting what `docreatelink` does if that conversion produces an empty sporglset — whether it proceeds to `insertendsetsinspanf` with an empty set (creating a link with a vacuous endset) or whether it crashes or errors. This case is not answerable from the KB as provided.

### Summary

| Input | Implementation behavior |
|---|---|
| `width = 0` on source or target | Crash (Bug 0017) [PRE-ZERO-WIDTH] |
| Non-zero width, content absent from POOM | Not documented in KB |

The KB confirms the precondition `link.source.width >= 1 ∧ link.target.width >= 1` [PRE-LINK-CREATE], and that the from/to endsets are indexed by I-address into the spanfilade [ST-CREATE-LINK], but says nothing about what happens when the sporgl conversion yields an empty result at creation time.

---

## Code Exploration

I now have all the evidence needed for a complete answer.

---

## Does `docreatelink` Accept Empty From/To Endsets?

**Yes, unambiguously.** There is no guard at any layer — protocol, dispatch, or storage — that rejects an empty from-endset or to-endset. The operation silently "succeeds" and creates what I will call a **phantom link**: a link node that exists in the granfilade but has no reachable endpoints.

---

## Complete Execution Trace

### 1. Protocol Layer: Empty Specset Is a Valid Message

`getspecset` at `get2fe.c:147-180`:

```c
bool getspecset(typetask *taskptr, typespecset *specsetptr)
{
    *specsetptr = NULL;
    if (!getnumber (taskptr, &num)) { return (FALSE); }
    if (num == 0)
        return (TRUE);   // ← num=0 → *specsetptr=NULL, returns TRUE
    ...
}
```

A client that sends `0` as the specset count for `fromspecset` or `tospecset` is fully accepted. `getcreatelink` at `get1fe.c:75-84` reads exactly this:

```c
return (
   gettumbler (taskptr, docisaptr)
&& getspecset (taskptr, fromspecsetptr)    // num=0 accepted
&& getspecset (taskptr, tospecsetptr)      // num=0 accepted
&& getspecset (taskptr, threespecsetptr)); // num=0 accepted
```

**No validation that any endset is non-empty.**

---

### 2. `docreatelink` at `do1.c:195-221`: No Guard for Empty Specsets

The function proceeds through the full link-creation pipeline regardless of whether `fromspecset` or `tospecset` is NULL:

```c
bool docreatelink(typetask *taskptr, typeisa *docisaptr, typespecset fromspecset,
                  typespecset tospecset, typespecset threespecset, typeisa *linkisaptr)
{
    ...
    return (
         createorglingranf (taskptr, granf, &hint, linkisaptr)       // allocates link node
      && tumbler2spanset (taskptr, linkisaptr, &ispanset)
      && findnextlinkvsa (taskptr, docisaptr, &linkvsa)
      && docopy (taskptr, docisaptr, &linkvsa, ispanset)             // records link ISA in doc POOM
      && findorgl (taskptr, granf, linkisaptr, &link, NOBERTREQUIRED)
      && specset2sporglset (taskptr, fromspecset, &fromsporglset, NOBERTREQUIRED)  // no NULL check!
      && specset2sporglset (taskptr, tospecset, &tosporglset, NOBERTREQUIRED)      // no NULL check!
      && specset2sporglset (taskptr, threespecset, &threesporglset, NOBERTREQUIRED)
      && setlinkvsas (&fromvsa, &tovsa, &threevsa)
      && insertendsetsinorgl (taskptr, linkisaptr, link, &fromvsa, fromsporglset,
                              &tovsa, tosporglset, &threevsa, threesporglset)
      && insertendsetsinspanf (taskptr, spanf, linkisaptr, fromsporglset,
                               tosporglset, threesporglset)
    );
}
```

---

### 3. `specset2sporglset` at `sporgl.c:14-33`: NULL Specset → NULL Sporglset, Returns TRUE

```c
bool specset2sporglset(typetask *taskptr, typespecset specset, typesporglset *sporglsetptr, int type)
{
    *sporglsetptr = NULL;
    for (; specset; specset = (typespecset)((typeitemheader*)specset)->next) {
        ...                     // loop body never executes when specset==NULL
    }
    *sporglsetptr = NULL;
    return (TRUE);              // always succeeds
}
```

An empty specset produces a NULL sporglset without error.

---

### 4. `insertendsetsinorgl` at `do2.c:130-148`: From/To Are Unconditional; Three Is Not

```c
bool insertendsetsinorgl(typetask *taskptr, tumbler *linkisaptr, typeorgl link,
    tumbler *fromvsa, typesporglset fromsporglset,
    tumbler *tovsa, typesporglset tosporglset,
    tumbler *threevsa, typesporglset threesporglset)
{
    if (!( insertpm(taskptr, linkisaptr, link, fromvsa, fromsporglset)  // UNCONDITIONAL
        && insertpm(taskptr, linkisaptr, link, tovsa, tosporglset))) {  // UNCONDITIONAL
            return (FALSE);
    }
    if (threevsa && threesporglset) {   // ← three-endset HAS a null guard
        if (!insertpm (taskptr, linkisaptr, link, threevsa, threesporglset)){
            return (FALSE);
        }
    } else {
        fprintf(stderr,"leaving INSERTENDSETSINORGL 4\n");  // debug print only
    }
    return (TRUE);
}
```

There is a deliberate asymmetry: `fromsporglset` and `tosporglset` are passed to `insertpm` unconditionally, but `threesporglset` is guarded by `if (threevsa && threesporglset)`. The debug print in the `else` branch confirms the implementer knew the three-endset could be legitimately absent, but the absence of a guard for from/to implies that path was either intended to be unreachable, or the silent no-op behavior of `insertpm` on a NULL sporglset was acceptable.

---

### 5. `insertpm` at `orglinks.c:75-134`: NULL Sporglset → Marks Link as Modified but Writes Nothing

```c
bool insertpm(typetask *taskptr, tumbler *orglisa, typeorgl orgl,
              tumbler *vsaptr, typesporglset sporglset)
{
    if (iszerotumbler (vsaptr)) {
        return (FALSE);         // guard: only rejects vsaptr==0, NOT sporglset==NULL
    }
    ...
    logbertmodified(orglisa, user);    // ← SIDE EFFECT: link marked modified in bert
    for (; sporglset; sporglset = (typesporglset) sporglset->xxxxsporgl.next) {
        unpacksporgl (sporglset, &lstream, &lwidth, &linfo);
        ...
        insertnd (taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);  // NOT called
        tumbleradd (vsaptr, &crumwidth.dsas[V], vsaptr);
    }
    return (TRUE);              // succeeds even with sporglset==NULL
}
```

`setlinkvsas` (`do2.c:169-183`) sets `fromvsa` = 1.1 and `tovsa` = 2.1, both non-zero. So `iszerotumbler(vsaptr)` is FALSE for both calls. `logbertmodified` fires — the link is marked dirty in bert — but the `for` loop iterates zero times and `insertnd` is never called. **No POOM entries are written for the empty endset.**

---

### 6. `insertendsetsinspanf` at `do2.c:116-128`: Same Asymmetry

```c
bool insertendsetsinspanf(..., typesporglset fromsporglset,
    typesporglset tosporglset, typesporglset threesporglset)
{
    if (!(
        insertspanf(taskptr,spanfptr,linkisaptr,fromsporglset,LINKFROMSPAN)  // UNCONDITIONAL
        && insertspanf(taskptr,spanfptr,linkisaptr,tosporglset,LINKTOSPAN))) // UNCONDITIONAL
            return (FALSE);
    if (threesporglset) {   // three-endset has null guard
        ...
    }
    return(TRUE);
}
```

`insertspanf` (`spanf1.c:15-54`) with a NULL sporglset iterates zero times and returns TRUE. **No spanfilade entries are written for the empty endset.**

---

### 7. Consequence: `followlink` Fails on an Empty Endset

`dofollowlink` at `do1.c:223-232` calls `link2sporglset` (`sporgl.c:67-95`):

```c
bool link2sporglset(typetask *taskptr, typeisa *linkisa, typesporglset *sporglsetptr,
                    INT whichend, int type)
{
    if (!findorgl (taskptr, granf, linkisa, &orgl, type)) { return (FALSE); }
    tumblerclear (&zero);
    tumblerincrement (&zero, 0, whichend, &vspan.stream);  // look at V-pos whichend (1, 2, or 3)
    tumblerincrement (&zero, 0, 1, &vspan.width);
    if (context = retrieverestricted((typecuc*)orgl, &vspan, V, (typespan*)NULL, I, (typeisa*)NULL)) {
        // builds sporglset from POOM entries found there
        return (TRUE);
    } else {
        return (FALSE);    // ← no POOM entries for that endset → NULL context → FALSE
    }
}
```

For a link with an empty from-endset, there are no POOM entries at V=1.x. `retrieverestricted` returns NULL. `link2sporglset` returns FALSE. `dofollowlink` returns FALSE. `fns.c:123-126`:

```c
if (... && dofollowlink (taskptr, &linkisa, &specset, whichend)) {
    putfollowlink (taskptr, specset);
} else
    putrequestfailed (taskptr);    // ← this fires
```

**`followlink` on either end of a phantom link returns request-failed.**

Similarly, `findlinksfromtothreesp` (`spanf1.c:56-103`) will not find the link when searching by the empty endset because no spanfilade entries exist for that end.

---

## Summary Table

| Layer | Code location | Empty from/to endset behavior |
|---|---|---|
| Protocol parsing | `get2fe.c:158` | `num=0` → `*specsetptr=NULL`, returns TRUE |
| `getcreatelink` | `get1fe.c:75-84` | No validation, passes NULL through |
| `docreatelink` | `do1.c:195-221` | No validation, full pipeline runs |
| `specset2sporglset` | `sporgl.c:14-33` | NULL specset → NULL sporglset, returns TRUE |
| `insertendsetsinorgl` | `do2.c:130-148` | from/to called unconditionally; three is NULL-guarded |
| `insertpm` | `orglinks.c:86-133` | vsaptr≠0 guard passes; NULL sporglset → `logbertmodified` fires, loop skipped, returns TRUE |
| `insertendsetsinspanf` | `do2.c:116-128` | from/to called unconditionally; three is NULL-guarded |
| `insertspanf` | `spanf1.c:25-52` | NULL sporglset → loop no-op, returns TRUE |
| `followlink` (later) | `sporgl.c:83-94` | `retrieverestricted` returns NULL → request-failed |

---

## Conclusion

**`docreatelink` will accept an empty from-endset or empty to-endset without error and return success.** No layer in the stack validates that endsets are non-empty. The result is a phantom link:

- A link node is allocated in the granfilade (`createorglingranf`)
- The link's ISA is written into the host document's POOM (`docopy`)
- The link is marked as modified in bert (`logbertmodified`) — a side-effect that persists
- **But no POOM entries are written for the empty endset in the link's own orgl**
- **And no spanfilade entries are written for the empty endset**

The link is structurally present but semantically headless. Any subsequent `followlink` on the empty end will fail with request-failed (because `link2sporglset` at `sporgl.c:83-94` finds no POOM entries and returns FALSE). `findlinksfromtothree` will also fail to index the link via its empty endset since there are no spanfilade entries for it.

Note the implementation asymmetry: `threespecset` (the "three-endset") has explicit NULL guards in both `insertendsetsinorgl` (`do2.c:136`) and `insertendsetsinspanf` (`do2.c:122`), confirming the implementer accepted a null three-endset as a normal, valid case. The from and to endsets have no such guards — their null-sporglset path is a silent no-op rather than an explicit design decision.
