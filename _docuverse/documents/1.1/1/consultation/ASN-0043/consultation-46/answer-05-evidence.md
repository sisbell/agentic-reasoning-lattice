## Question 5 [evidence]

> Does `docreatelink` (or any other code path) ever produce a link with only two endsets stored, or is the third endset always populated even when the "conditional" branch is taken?

## KB Synthesis

The KB does not contain a finding that directly inspects the conditional branching logic inside `docreatelink`/`domakelink` for the THREE endset. Here is what the KB does establish:

**Evidence that all three endsets are always stored:**

- [SS-DUAL-ENFILADE] Finding 0038: `setlinkvsas()` "hardcodes digit-0 values of 1, 2, and 3 for the FROM, TO, and THREE endpoints respectively" — all three V-positions (2.x for FROM/TO, 3.x for type) are constructed together.
- [ST-CREATE-LINK] Finding 0012: `docreatelink` calls `insertendsetsinspanf()` described as indexing "all link endpoints."
- [SS-RETRIEVE-ENDSETS] Finding 0035: The spanfilade is organized with three distinct ORGLRANGE prefixes (LINKFROMSPAN=1, LINKTOSPAN=2, LINKTHREESPAN=3), and `retrieveendsetsfromspanf()` searches all three.

**A complicating observation:**

- [SS-RETRIEVE-ENDSETS] Finding 0035 notes "the three-endset is conditionally retrieved (only if requested)" — but this refers to the retrieval side, not to whether it was stored at creation.

**Circumstantial evidence it is always stored:**

- [EC-ORPHANED-LINK] Finding 0024 shows that `follow_link(link_id, TYPE)` returns *empty* (unexpectedly) when both source and target are deleted — implying the TYPE endset was stored, and the failure is an unresolved anomaly in its resolution, not an absence of storage.
- [EC-TYPE-FILTER-NONFUNCTIONAL] shows type-based search is broken, not that the endset is absent.

**Conclusion:** The KB has no finding examining whether a conditional branch inside `docreatelink` can skip storing the THREE endset. Based on available evidence, all three endsets appear to always be populated at creation. If the question arises from reading the source directly, it is not answered by the KB.

---

## Code Exploration

I now have all the pieces needed. Let me assemble the full answer.

---

## Answer

### `docreatelink` Can Produce a Two-Endset Link — The Third Is Not Unconditionally Stored

---

### The Call Chain in `docreatelink` (`do1.c:195–221`)

```c
bool docreatelink(typetask *taskptr, typeisa *docisaptr,
    typespecset fromspecset, typespecset tospecset,
    typespecset threespecset, typeisa *linkisaptr)
{
  tumbler linkvsa, fromvsa, tovsa, threevsa;
  typesporglset fromsporglset, tosporglset, threesporglset;
  ...
  return (
       createorglingranf(...)
    && tumbler2spanset(...)
    && findnextlinkvsa(...)
    && docopy(...)
    && findorgl(...)
    && specset2sporglset(taskptr, fromspecset,   &fromsporglset, NOBERTREQUIRED)   // [do1.c:214]
    && specset2sporglset(taskptr, tospecset,     &tosporglset,   NOBERTREQUIRED)   // [do1.c:215]
    && specset2sporglset(taskptr, threespecset,  &threesporglset, NOBERTREQUIRED)  // [do1.c:216]
    && setlinkvsas(&fromvsa, &tovsa, &threevsa)                                    // [do1.c:217]
    && insertendsetsinorgl(taskptr, linkisaptr, link,
           &fromvsa, fromsporglset, &tovsa, tosporglset,
           &threevsa, threesporglset)                                              // [do1.c:218]
    && insertendsetsinspanf(taskptr, spanf, linkisaptr,
           fromsporglset, tosporglset, threesporglset)                            // [do1.c:219]
  );
}
```

---

### Gate 1: `setlinkvsas` (`do2.c:169–183`)

```c
bool setlinkvsas(tumbler *fromvsaptr, tumbler *tovsaptr, tumbler *threevsaptr)
{
    tumblerclear(fromvsaptr);
    tumblerincrement(fromvsaptr, 0, 1, fromvsaptr);    // fromvsa  = 0.1.1
    tumblerincrement(fromvsaptr, 1, 1, fromvsaptr);
    tumblerclear(tovsaptr);
    tumblerincrement(tovsaptr, 0, 2, tovsaptr);        // tovsa    = 0.2.1
    tumblerincrement(tovsaptr, 1, 1, tovsaptr);
    if (threevsaptr) {                                 // [do2.c:177]
        tumblerclear(threevsaptr);
        tumblerincrement(threevsaptr, 0, 3, threevsaptr);  // threevsa = 0.3.1
        tumblerincrement(threevsaptr, 1, 1, threevsaptr);
    }
    return (TRUE);
}
```

`docreatelink` passes `&threevsa` — a pointer to a stack-allocated `tumbler`. This is **always non-NULL**, so the `if (threevsaptr)` guard at `do2.c:177` is **always taken** from `docreatelink`. `threevsa` is always initialized to `0.3.1`.

Contrast with `domakelink` (`do1.c:189`), which passes `NULL` here — explicitly opting into the two-endset model.

---

### Gate 2: `insertendsetsinorgl` (`do2.c:130–149`) — The Critical Branch

```c
bool insertendsetsinorgl(typetask *taskptr, tumbler *linkisaptr,
    typeorgl link,
    tumbler *fromvsa, typesporglset fromsporglset,
    tumbler *tovsa,  typesporglset tosporglset,
    tumbler *threevsa, typesporglset threesporglset)
{
    if (!(insertpm(taskptr, linkisaptr, link, fromvsa, fromsporglset)
       && insertpm(taskptr, linkisaptr, link, tovsa,   tosporglset))) {
        return (FALSE);
    }
    if (threevsa && threesporglset) {                  // [do2.c:136]
        if (!insertpm(taskptr, linkisaptr, link, threevsa, threesporglset))
            return (FALSE);
    } else {
#ifndef DISTRIBUTION
        fprintf(stderr, "leaving INSERTENDSETSINORGL 4\n");    // [do2.c:142]
        fprintf(stderr, " threevsa ptr= %x threesporglset ptr = %x ...",
                threevsa, threesporglset);
        dumptumbler(threevsa);
#endif
    }
    return (TRUE);
}
```

This checks **both** `threevsa` AND `threesporglset`. From `docreatelink`, `threevsa` is always non-NULL (initialized above). So the outcome depends entirely on whether `threesporglset` is NULL or not.

The `else` branch (debug print at `do2.c:142`) is the path where **no third endset is stored in the granfilade**. It is not an error — the function still returns `TRUE`.

---

### Gate 3: `insertendsetsinspanf` (`do2.c:116–128`)

```c
bool insertendsetsinspanf(typetask *taskptr, typespanf spanfptr,
    typeisa *linkisaptr,
    typesporglset fromsporglset,
    typesporglset tosporglset,
    typesporglset threesporglset)
{
    if (!(insertspanf(taskptr, spanfptr, linkisaptr, fromsporglset, LINKFROMSPAN)
       && insertspanf(taskptr, spanfptr, linkisaptr, tosporglset,   LINKTOSPAN)))
        return (FALSE);
    if (threesporglset) {                              // [do2.c:122]
        if (!insertspanf(taskptr, spanfptr, linkisaptr, threesporglset, LINKTHREESPAN))
            return (FALSE);
    }
    return (TRUE);
}
```

Same story: if `threesporglset` is NULL, the spanfilade insertion of the third endset is skipped silently.

---

### When Is `threesporglset` NULL?

Traced through `specset2sporglset` (`sporgl.c:14–33`):

```c
bool specset2sporglset(typetask *taskptr, typespecset specset,
    typesporglset *sporglsetptr, int type)
{
    *sporglsetptr = NULL;           // [sporgl.c:18] — initializes to NULL
    for (; specset; ...) {          // [sporgl.c:19] — only runs if specset is non-empty
        ...
    }
    *sporglsetptr = NULL;           // [sporgl.c:30] — terminates linked list
    return (TRUE);
}
```

If `threespecset` is a NULL pointer (empty specset), the loop never executes, `threesporglset` remains `NULL`, and the function returns `TRUE` — no error.

`getspecset` (`get2fe.c:147–180`) reads a count from the wire:

```c
if (num == 0)
    return (TRUE);   // [get2fe.c:158–159] — returns TRUE with *specsetptr == NULL
```

**The FEBE client can legally send a zero-count specset for the three-endset.** When it does, `threespecset` is NULL, `threesporglset` is NULL, and both guard conditions in `insertendsetsinorgl` and `insertendsetsinspanf` skip the third storage step.

---

### Summary

| Scenario | `threesporglset` | Third endset in orgl? | Third endset in spanfilade? |
|---|---|---|---|
| `docreatelink` with non-empty `threespecset` | non-NULL | **Yes** — `insertpm` called [`do2.c:137`] | **Yes** — `insertspanf` called [`do2.c:123`] |
| `docreatelink` with empty `threespecset` (count=0) | NULL | **No** — `else` branch at [`do2.c:140`] | **No** — skipped at [`do2.c:122`] |
| `domakelink` (old two-endset API) | NULL (explicitly) | **No** | **No** |

**`docreatelink` can absolutely produce a link with only two endsets stored.** This happens whenever the client passes an empty third specset. The guard `if (threevsa && threesporglset)` at `do2.c:136` is the decisive conditional, and it short-circuits silently (with a debug stderr print in non-distribution builds) rather than returning an error. The third endset is **not** unconditionally stored — it is gated on the sporglset being non-NULL, which depends on the three-endset specset being non-empty on the wire.
