## Question 17 [evidence]

> If the requested endset is empty or its content has been deleted such that nothing is currently referenced, does the operation return an empty spec-set without error rather than failing?

## KB Synthesis

Yes. The operation returns an empty spec-set without error.

This is established by three converging findings:

**[PRE-FOLLOWLINK]** (Finding 0048) states explicitly: "There is no precondition requiring that endset I-addresses be currently referenced in any POOM. The operation succeeds even when all endset I-addresses are unreferenced, returning an empty result rather than an error."

**[EC-GHOST-LINK]** (Finding 0048) documents three observable outcome cases:
1. All endset I-addresses live → full result
2. Some unreferenced → partial result (only live addresses converted)
3. All unreferenced → empty result `[]`, operation still succeeds (`works: true`)

The mechanism is explained by **[INV-ITOV-FILTERING]** (Finding 0048): the shared `linksporglset2specset()` → `span2spanset()` path silently drops any I-address for which `retrieverestricted()` returns NULL (no POOM mapping). This filtering is universal — it applies to both FOLLOWLINK and RETRIEVEENDSETS, and the caller receives whatever non-empty V-spans remain, which may be zero.

The design rationale: the back end returns what permanent I-space storage contains, and the I-to-V conversion layer filters based on current POOM state. Liveness of the referenced content is not a validity condition for the operation itself.

---

## Code Exploration

I have all the evidence needed. Here is the complete analysis.

---

## Answer: Empty Endset Behavior in `followlink` vs `retrieveendsets`

The answer **depends on which operation** you mean. The two endset-reading paths diverge sharply.

---

### Path 1: `followlink` — **FAILS**, does not return an empty spec-set

**Call chain:** `fns.c:followlink` → `do1.c:dofollowlink` → `sporgl.c:link2sporglset`

`dofollowlink` at `do1.c:228-231`:
```c
return (
   link2sporglset (taskptr, linkisaptr, &sporglset, whichend,NOBERTREQUIRED)
&& linksporglset2specset (taskptr,&((typesporgl *)sporglset)->sporgladdress,
                          sporglset, specsetptr, NOBERTREQUIRED));
```

`link2sporglset` at `sporgl.c:83-94`:
```c
if (context = retrieverestricted((typecuc*)orgl, &vspan ,V, (typespan*)NULL, I, (typeisa*)NULL)) {
    for (c = context; c; c = c->nextcontext) {
        /* build sporglset */
    }
    contextfree (context);
    return (TRUE);
} else{
    return (FALSE);   /* ← NULL context → failure */
}
```

`retrieverestricted` at `retrie.c:83-84` delegates to `retrieveinarea`, which initializes `context = NULL` at `retrie.c:93` and returns that NULL if `findcbcinarea2d` finds nothing. When `retrieverestricted` returns NULL, `link2sporglset` takes the `else` branch at `sporgl.c:93` and returns `FALSE`.

Because `dofollowlink` is a short-circuit AND, this FALSE propagates back to `fns.c:followlink` at line 125:
```c
if (
   getfollowlink (taskptr, &linkisa, &whichend)
&& dofollowlink (taskptr, &linkisa, &specset, whichend)){
    putfollowlink (taskptr, specset);
  }else
    putrequestfailed (taskptr);   /* ← what actually fires */
```

**Verdict for `followlink`:** If the requested endset position has no content (empty or deleted), `retrieverestricted` returns NULL → `link2sporglset` returns FALSE → `dofollowlink` returns FALSE → the backend sends `putrequestfailed`. There is **no empty spec-set response**; the operation fails.

---

### Path 2: `retrieveendsets` — **SUCCEEDS** with empty spec-sets

**Call chain:** `fns.c:retrieveendsets` → `do1.c:doretrieveendsets` → `spanf1.c:retrieveendsetsfromspanf` → `spanf1.c:retrievesporglsetinrange`

`retrievesporglsetinrange` at `spanf1.c:237-267`:
```c
bool retrievesporglsetinrange(typetask *taskptr, typesporglset sporglptr, typespan *whichspace, typesporglset *sporglsetptr)
{
  ...
        for (; sporglptr; ...) {
               context = retrieverestricted(...);
               for (c = context; c;) {
                        /* build sporglset only if context is non-NULL */
                        ...
               }
               contextfree(context);
        }
        return (TRUE);   /* ← ALWAYS returns TRUE */
}
```

There is no conditional on `context` — if `retrieverestricted` returns NULL, the inner `for (c = context...)` loop body never executes, `*sporglsetptr` is never written, and the function still returns TRUE at `spanf1.c:266`.

Then `linksporglset2specset` at `sporgl.c:102`:
```c
*specsetptr = NULL;
for (; sporglset; sporglset = ...) {   /* sporglset is NULL → loop skips entirely */
    ...
}
return (TRUE);
```

If `sporglset` is NULL (empty endset), `*specsetptr` is set to NULL and TRUE is returned. The caller, `retrieveendsetsfromspanf` at `spanf1.c:222-228`, gets TRUE from every step and returns TRUE.

Back in `fns.c:retrieveendsets` at line 355-361:
```c
if (
   getretrieveendsets (taskptr, &specset)
&& doretrieveendsets (taskptr, specset, &fromset, &toset, &threeset)){
    putretrieveendsets (taskptr, fromset, toset, threeset);   /* ← fires, with NULL sets */
 }else
    putrequestfailed (taskptr);
```

`putretrieveendsets` is called with NULL specsets — the protocol sends an empty spec-set response, not a failure.

**Verdict for `retrieveendsets`:** If the link's endset contains nothing (empty or deleted), `retrievesporglsetinrange` always returns TRUE, `linksporglset2specset` emits NULL (empty), and the operation succeeds with empty spec-sets.

---

### Summary Table

| Operation | Mechanism | Empty/Deleted Endset Behavior |
|---|---|---|
| `followlink` (`fns.c:114`) | `link2sporglset` → `retrieverestricted` → fail on NULL | **Fails** → `putrequestfailed` |
| `retrieveendsets` (`fns.c:350`) | `retrievesporglsetinrange` → always TRUE | **Succeeds** → empty spec-set |

### Root Cause of the Divergence

`link2sporglset` (`sporgl.c:83`) treats a NULL return from `retrieverestricted` as failure because it uses a conditional `if (context = ...)`. `retrievesporglsetinrange` (`spanf1.c:244`) calls the same `retrieverestricted` but does **not** gate on its result — it iterates `for (c = context; c; ...)` which simply skips when `context` is NULL, then unconditionally returns TRUE at `spanf1.c:266`.

So: `retrieveendsets` returns an empty spec-set without error when an endset is empty or its content has been deleted. `followlink` does **not** — it fails.
