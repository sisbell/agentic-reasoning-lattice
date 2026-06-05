## Question 1 [evidence]

> In udanax-green, is `docopy` ever invoked as a non-final sub-step inside a larger atomic transaction, or is it always issued as a standalone operation?

## KB Synthesis

`docopy` is invoked as a non-final sub-step inside at least two larger compound operations, not only as a standalone call.

**Inside `doinsert` (INSERT)**

[ST-INSERT] (Finding 0036) documents the call chain: `doinsert` → `inserttextingranf` → `docopy` → `insertpm` + `insertspanf(..., DOCISPAN)`. Here `docopy` is a middle step — `inserttextingranf` runs first to allocate fresh I-addresses, then `docopy` places them and registers the DOCISPAN entry. The INSERT operation cannot be split at this boundary; [INV-ATOMICITY] (Finding 0042) confirms the entire chain runs to completion within a single `xanadu(&task)` invocation before any response is sent.

**Inside `docreatelink` (CREATELINK)**

[ST-CREATE-LINK] (Finding 0012) makes this explicit: link creation is a three-step compound transition — (1) `createorglingranf` allocates the link orgl, (2) `docopy` writes the ISA into the document's 2.x subspace, (3) `insertendsetsinspanf` indexes the endpoints in the spanf. `docopy` is step 2 of 3; `insertendsetsinspanf` still follows. [ST-CREATE-LINK] (Finding 0052) confirms the same path: `docreatelink` → `docopy` → `insertpm` → `insertnd`.

**Inside `docreatenewversion` (VERSION)**

[ST-VERSION-CREATE] (Finding 0032) notes that `docreatenewversion` calls `docopyinternal` as its third step, after allocating a new orgl and retrieving the source vspanset.

**When called for standalone VCOPY**

Even a user-level COPY/VCOPY issues `docopy` directly, but `docopy` itself is compound — it calls both `insertpm` (granf mutation) and `insertspanf` (spanf mutation) [FC-CONTENT-SPANF-ISOLATION] (Finding 0036). So even in the "standalone" case there is no sense in which `docopy` is an atomic primitive; it is itself a two-enfilade compound operation.

**Summary:** `docopy` is a shared sub-routine invoked as a non-final step inside INSERT, CREATELINK, and VERSION, and as the principal (but still internally compound) step in user-level VCOPY. It is never the outermost atomic boundary.

---

## Code Exploration

## Answer: Is `docopy` ever a non-final sub-step inside a larger atomic operation?

**Yes.** `docopy` is called as a non-final intermediate step inside both `domakelink()` and `docreatelink()`. It is also the final/only step in `doinsert()` and the standalone `COPY` FEBE handler.

---

### The standalone handler

`fns.c` exposes `copy()` as the FEBE `COPY` request handler:

```c
// fns.c ~line 35
void copy(typetask *taskptr)
{
    typeisa docisa, vsa;
    typespecset localspecset;
    bool getcopy(), docopy();

    if (   getcopy (taskptr, &docisa, &vsa, &localspecset)
        && docopy (taskptr, &docisa, &vsa, localspecset))
        putcopy (taskptr);
    else
        putrequestfailed (taskptr);
}
```

Here `docopy` is the sole substantive operation — entirely standalone.

---

### `doinsert()` — `docopy` as final step

In `do1.c` around line 119, `doinsert()` calls `inserttextingranf` to allocate content, then calls `docopy` as the **concluding** step to register that content in the document's virtual span structure:

```c
// do1.c ~line 119
ret = (inserttextingranf(taskptr, granf, &hint, textset, &ispanset)
    && docopy (taskptr, docisaptr, vsaptr, ispanset)
    /* no ht stuff here, 'cause it's taken care of in docopy */);
return(ret);
```

`docopy` is the last operation — so still "final."

---

### `docreatelink()` / `domakelink()` — `docopy` as a **non-final** sub-step

This is where the answer changes. In both `domakelink()` (~line 185) and `docreatelink()` (~line 212), `docopy` is called mid-chain with **substantial work following it**:

```c
// do1.c ~line 185 (domakelink, two-endpoint variant)
return (
     createorglingranf (taskptr, granf, &hint, linkisaptr)
  && tumbler2spanset (taskptr, linkisaptr, &ispanset)
  && findnextlinkvsa (taskptr, docisaptr, &linkvsa)
  && docopy (taskptr, docisaptr, &linkvsa, ispanset)          // <-- NOT the final step
  && findorgl (taskptr, granf, linkisaptr, &link, WRITEBERT)
  && specset2sporglset (taskptr, fromspecset, &fromsporglset, NOBERTREQUIRED)
  && specset2sporglset (taskptr, tospecset, &tosporglset, NOBERTREQUIRED)
  && setlinkvsas (&fromvsa, &tovsa, NULL)
  && insertendsetsinorgl (taskptr, linkisaptr, link, &fromvsa, fromsporglset,
                          &tovsa, tosporglset, NULL, NULL)     // written after docopy
  && insertendsetsinspanf (taskptr, spanf, linkisaptr,
                           fromsporglset, tosporglset, NULL)   // written after docopy
);
```

And the three-endpoint variant at ~line 212 follows the same pattern:

```c
// do1.c ~line 212 (docreatelink, three-endpoint variant)
return (
     createorglingranf (taskptr, granf, &hint, linkisaptr)
  && tumbler2spanset (taskptr, linkisaptr, &ispanset)
  && findnextlinkvsa (taskptr, docisaptr, &linkvsa)
  && docopy (taskptr, docisaptr, &linkvsa, ispanset)          // <-- NOT the final step
  && findorgl (taskptr, granf, linkisaptr, &link, NOBERTREQUIRED)
  && specset2sporglset (taskptr, fromspecset, &fromsporglset, NOBERTREQUIRED)
  && specset2sporglset (taskptr, tospecset, &tosporglset, NOBERTREQUIRED)
  && specset2sporglset (taskptr, threespecset, &threesporglset, NOBERTREQUIRED)
  && setlinkvsas (&fromvsa, &tovsa, &threevsa)
  && insertendsetsinorgl (taskptr, linkisaptr, link, &fromvsa, fromsporglset,
                          &tovsa, tosporglset, &threevsa, threesporglset)
  && insertendsetsinspanf (taskptr, spanf, linkisaptr,
                           fromsporglset, tosporglset, threesporglset)
);
```

**What `docopy` does at this position:** it takes the newly-allocated link atom (identified by `linkisaptr`) and registers it at `linkvsa` in the document's version span structure — i.e., it "plants the link in the doc's address space." What follows writes the link's internal endpoint data into the granfilade and spanfilade. Both phases are part of the same single FEBE request.

---

### `docopyinternal()` — variant used in `docreatenewversion()`

There is also a private variant `docopyinternal()` at `do1.c` ~line 66, used inside `docreatenewversion()`. It performs the same operations as `docopy` but with `if (!...) return FALSE` guards instead of `&&` chaining. It is likewise a non-final sub-step within the version-creation sequence.

---

### Transaction boundaries

The event loop in `bed.c` processes exactly one FEBE request per iteration:

```c
// bed.c ~line 153
xanadu(&task);  // dispatch one request, then loop back to select()
```

Within `xanadu()`, `tfree(taskptr)` is called at the end — there is no cross-request batching or rollback mechanism. Everything within a single call to `docreatelink()` or `domakelink()` is therefore **de facto atomic** (it either runs to completion or short-circuits via `&&`), but it is a single-request atomic unit, not a multi-request transaction.

---

### Summary

| Call site | `docopy` position | Atomic unit |
|-----------|------------------|-------------|
| `fns.c:copy()` | Sole operation | Single FEBE `COPY` request |
| `do1.c:doinsert()` | Final step | Single FEBE `INSERT` request |
| `do1.c:domakelink()` | **Non-final** — endpoint data written after | Single FEBE `CREATELINK` request |
| `do1.c:docreatelink()` | **Non-final** — endpoint data written after | Single FEBE `CREATELINK` request |
| `do1.c:docopyinternal()` | Non-final inside `docreatenewversion()` | Single FEBE `CREATENEWVERSION` request |

**Conclusion:** `docopy` is a non-final sub-step inside link creation and new-version creation. In those contexts it stakes out the link's address in the document's version structure, while subsequent operations write the link's endpoint content. All of this occurs within a single FEBE request (one `&&`-chained function body), so the containing operation is atomic — but `docopy` is definitively not always the final step.
