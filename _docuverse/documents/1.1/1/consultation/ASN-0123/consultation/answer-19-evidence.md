## Question 19 [evidence]

> Does CREATENEWVERSION take or check a BERT on the source document (read access) and on the newly allocated version, and at what point in `docreatenewversion` does the ownership check that selects the allocation hint occur relative to any response sent to the client?

## KB Synthesis

## CREATENEWVERSION: BERT Checking and Ownership Check Timing

### What the KB Answers

**Ownership check placement inside `docreatenewversion`:**

[ST-VERSION-OWNERSHIP] (Finding 0068) places the ownership check explicitly at `do1.c:272-280` — inside `docreatenewversion` itself. The predicate is `tumbleraccounteq(isaptr, wheretoputit) && isthisusersdocument(isaptr)`, and it selects between two `makehint` calls that determine the allocation depth.

This is the `doXXX` phase. Per the general pattern established by [EC-RESPONSE-BEFORE-CHECK] (Finding 0050), `putXXX()` is sent before `doXXX()` executes for most state-modifying operations — meaning the ownership check occurs **after** the client response for those operations. However, [EC-RESPONSE-BEFORE-CHECK] names `createlink` as the only explicit exception to this pattern; CREATENEWVERSION is not named in either category. **The KB does not resolve whether VERSION follows the general (response-before-check) pattern or the exception pattern.**

### What the KB Does Not Answer

**BERT on the source document:** The KB does not state whether `doretrievedocvspanfoo` (at `do1.c:305-313`, the vspanset read from the source) calls `findorgl` with READBERT or uses NOBERTREQUIRED. [SS-BERT] establishes that NOBERTREQUIRED bypasses the table for internal operations, and `docreatenewversion` is an internal compound operation, but no KB entry confirms which path it takes.

**BERT on the new version:** The version document is freshly allocated by `createorglingranf` — no BERT entry exists for it at the time of `docopyinternal`. Whether `docopyinternal` invokes `findorgl(..., WRITEBERT)` on the destination (as the public `docopy` does per [PRE-INSERT] Finding 0036) or bypasses BERT as an internal call is not documented in the KB.

### Summary

The KB establishes that the ownership check is inside `docreatenewversion` (post-allocation hint logic, `do1.c:272-280`), but the relationship of that check to the client response and the BERT behavior on both source and destination documents are not answerable from the existing entries.

---

## Code Exploration

I have all the information needed. Here is the complete answer:

---

## CREATENEWVERSION: BERT Checking and Ownership Analysis

### Call chain in `fns.c:289-300`

```c
void createnewversion(typetask *taskptr)
{
  typeisa originaldocisa, newdocisa;
  ...
    if (
       getcreatenewversion (taskptr, &originaldocisa)          // 1. parse request
    && docreatenewversion (taskptr, &originaldocisa, &originaldocisa, &newdocisa))  // 2. do work
            putcreatenewversion (taskptr, &newdocisa);         // 3. send response
      else
            putrequestfailed (taskptr);
}
```

`getcreatenewversion` (`get1.c:76-80`) simply reads a document ISA from the client — it performs no BERT check at all. All access control logic lives in step 2.

---

### 1. BERT check on the SOURCE document

**There is no BERT check on the source document.** Inside `docreatenewversion`, the source document is read via `doretrievedocvspanfoo` [`do1.c:281`]:

```c
if (!doretrievedocvspanfoo (taskptr, isaptr, &vspan)) {
    return FALSE;
}
```

`doretrievedocvspanfoo` at `do1.c:301-309` calls:
```c
findorgl (taskptr, granf, docisaptr, &docorgl, NOBERTREQUIRED)
```

`findorgl` in `granf1.c:22` calls `checkforopen(isaptr, type, user)`. With `NOBERTREQUIRED`, `checkforopen` immediately returns 1 with no BERT validation whatsoever [`bert.c:59-61`]:

```c
if (type == NOBERTREQUIRED) {
    return 1;   /* Random > 0 */
}
```

Compare this to `doretrievedocvspan` (the non-`foo` variant, `do1.c:312-320`), which passes `READBERT` — that variant **would** require a read BERT. The `foo` variant used by `docreatenewversion` deliberately skips it. Any connection can create a new version from any document regardless of ownership.

---

### 2. Ownership check for the allocation hint — FIRST thing in `docreatenewversion`

At `do1.c:268-276`, the very first lines of the function body:

```c
/* ECH 7-13 introduced test for ownership to do right thing for explicit creation
   of new version of someone else's document */
if (tumbleraccounteq(isaptr, wheretoputit) && isthisusersdocument(isaptr)) {
    makehint (DOCUMENT, DOCUMENT, 0, isaptr/*wheretoputit*/, &hint);
} else {
    /* This does the right thing for new version of someone else's document, as it
       duplicates the behavior of docreatenewdocument */
    makehint (ACCOUNT, DOCUMENT, 0, wheretoputit, &hint);
}
```

`isthisusersdocument(tp)` at `socketbe.c:197-201` compares the document's account prefix to the current connection's account:

```c
int isthisusersdocument(tumbler *tp)
{
    return tumbleraccounteq(tp, &(player[user].account));
}
```

`tumbleraccounteq` (`tumble.c:38-70`) checks whether `bptr`'s non-zero mantissa digits all match `aptr`'s, treating a run of two zeros as the account-space terminator — i.e., it tests whether `aptr` (the document) falls within `bptr`'s (the account's) address prefix.

When called from `fns.c:296`, both `isaptr` and `wheretoputit` point to `&originaldocisa` — the same address — so `tumbleraccounteq(isaptr, wheretoputit)` is always TRUE. The sole discriminator becomes `isthisusersdocument`:

- **User's own document** → `DOCUMENT`-level hint: allocate the new version near the source document in tumbler-space.
- **Someone else's document** → `ACCOUNT`-level hint: allocate the new version in the user's own account space, mirroring `docreatenewdocument` behavior.

(When `docreatenewversion` is called internally from `doopen` at `bert.c:274`, it is called as `docreatenewversion(taskptr, tp, &taskptr->account, newtp)` — `isaptr = tp`, `wheretoputit = taskptr->account` — so `tumbleraccounteq` may differ; but for the direct CREATENEWVERSION command the two args are always identical.)

---

### 3. BERT on the newly allocated version

There is **no** `checkforopen` call for the new version. After `createorglingranf` allocates the new tumbler [`do1.c:277`], the code inserts the new document into the BERT table directly [`do1.c:290-295`]:

```c
/* Skip doopen ownership check - we just created this document so we own it.
   Add directly to bert table instead. */
addtoopen(newisaptr, user, TRUE, WRITEBERT);
docopyinternal(taskptr, newisaptr, &vspan.stream, &vspec);
/* Mark as modified so removefromopen doesn't delete the newly created version */
logbertmodified(newisaptr, user);
doclose(taskptr, newisaptr, user);
```

`addtoopen` registers a WRITE BERT with `created=TRUE`. `logbertmodified` sets `bert->modified = TRUE` before `doclose` calls `removefromopen`. This is required because `removefromopen` at `bert.c:173` would delete a document for which `created && !modified` — the "created but never written" garbage-collection rule. Setting `modified=TRUE` prevents deletion of the freshly populated version on close.

---

### 4. Timing: ownership check vs. response to client

Full sequence inside `docreatenewversion`:

| Step | Line | Action |
|------|------|--------|
| 1 | `do1.c:270` | **Ownership check** (`isthisusersdocument`) — selects allocation hint |
| 2 | `do1.c:271` or `275` | `makehint` — record hint |
| 3 | `do1.c:277` | `createorglingranf` — allocate new tumbler |
| 4 | `do1.c:281` | `doretrievedocvspanfoo` — read source (no BERT) |
| 5 | `do1.c:292` | `addtoopen(..., WRITEBERT)` — register new doc, bypassing `checkforopen` |
| 6 | `do1.c:293` | `docopyinternal` — copy content |
| 7 | `do1.c:295` | `logbertmodified` — mark modified |
| 8 | `do1.c:296` | `doclose` — close and remove from BERT table |
| 9 | `fns.c:297` | `putcreatenewversion` — **response sent to client** |

The ownership check (`isthisusersdocument`) is the **very first operation** in `docreatenewversion` and precedes the response by the entire cost of allocation, content retrieval, copying, and closing. The client receives no response — and specifically does not learn the new tumbler — until all of that work has completed and `docreatenewversion` returns TRUE.
