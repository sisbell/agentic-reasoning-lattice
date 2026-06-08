## Question 1 [evidence]

> Does udanax-green's FINDNUMOFLINKSFROMTOTHREE include links of arity greater than three when their first three endsets match, or does it filter to exactly-three-endset links?

## KB Synthesis

The KB does not support the premise of the question — udanax-green links do not have variable arity. All links have exactly three endsets, corresponding to the three fixed ORGLRANGE subspaces in the spanfilade: LINKFROMSPAN=1 (from/source), LINKTOSPAN=2 (to/target), and LINKTHREESPAN=3 (three/type) [SS-RETRIEVE-ENDSETS, ST-CREATE-LINK Finding 0012].

`FINDNUMOFLINKSFROMTOTHREE` is a trivial wrapper that calls `findlinksfromtothreesp()` and counts the resulting list — there is no arity filtering because there is no concept of a link with more than three endsets [SS-FIND-LINKS Finding 0035]. The search is purely I-address intersection in the spanfilade against the three fixed endset subspaces; any link matching on the specified from/to/three I-address ranges is returned.

The KB cannot answer whether arity > 3 links exist, because no finding documents such a concept.

---

## Code Exploration

I now have all the evidence needed. Here is the definitive answer.

---

## FINDNUMOFLINKSFROMTOTHREE: Arity Filtering Analysis

**Short answer:** The system architecturally caps link arity at 3. Links of arity > 3 cannot exist, and `FINDNUMOFLINKSFROMTOTHREE` contains no "exactly-three" filter — it queries by span index, not by arity count.

---

### 1. Entry Point — `fns.c:204-217`

```c
void findnumoflinksfromtothree(typetask *taskptr)
{
    ...
    if (getfindnumoflinksfromtothree(taskptr, &fromvspecset, &tovspecset, &threevspecset, &homeset)
    &&  dofindnumoflinksfromtothree(taskptr, fromvspecset, tovspecset, threevspecset, homeset, &numberoflinks))
        putfindnumoflinksfromtothree(taskptr, numberoflinks);
    else
        putrequestfailed(taskptr);
}
```

Calls into `dofindnumoflinksfromtothree` → `findnumoflinksfromtothreesp` → `findlinksfromtothreesp`.

---

### 2. Link Retrieval — `spanf1.c:56-103`

The function queries the spanfilade using exactly three named span-type constants:

```c
if (fromvspecset)
    sporglset2linkset(taskptr, spanfptr, fromsporglset, &fromlinkset, orglrange, LINKFROMSPAN);   // line 77
if (tovspecset)
    sporglset2linkset(taskptr, spanfptr, tosporglset,  &tolinkset,   orglrange, LINKTOSPAN);      // line 85
if (threevspecset)
    sporglset2linkset(taskptr, spanfptr, threesporglset, &threelinkset, orglrange, LINKTHREESPAN); // line 93
intersectlinksets(taskptr, fromlinkset, tolinkset, threelinkset, linksetptr);                     // line 100
```

These constants are defined in `xanadu.h:36-38`:
```c
#define LINKFROMSPAN    1
#define LINKTOSPAN      2
#define LINKTHREESPAN   3
```

**There is no `LINKFOURSPAN`.** The defined constants stop at 3.

---

### 3. Intersection Logic — `spanf2.c:46-120`

`intersectlinksets` accepts three linksets and returns their intersection by tumbler address equality:

```c
// lines 95-118
if (!linkset3) {
    // two-way intersection: temp1 ∩ linkset2
    for (; temp1; temp1 = temp1->next)
        for (temp2 = linkset2; temp2; temp2 = temp2->next)
            if (tumblereq(&temp1->address, &temp2->address)) ...
} else {
    // three-way intersection: temp1 ∩ linkset2 ∩ linkset3
    for (; temp1; temp1 = temp1->next)
        for (temp2 = linkset2; temp2; temp2 = temp2->next)
            for (temp3 = linkset3; temp3; temp3 = temp3->next)
                if (tumblereq(&temp1->address, &temp2->address)
                 && tumblereq(&temp2->address, &temp3->address)) ...
}
```

**No arity check whatsoever.** A link passes the filter if its tumbler address appears in the intersection of the requested span-indexed sets. The function has no knowledge of how many total endsets a link has.

---

### 4. Storage Architecture Caps Arity at 3 — `do2.c:116-128`

`insertendsetsinspanf` is the only function that writes link endsets into the spanfilade:

```c
bool insertendsetsinspanf(..., fromsporglset, tosporglset, threesporglset)
{
    insertspanf(taskptr, spanfptr, linkisaptr, fromsporglset, LINKFROMSPAN);  // always
    insertspanf(taskptr, spanfptr, linkisaptr, tosporglset,   LINKTOSPAN);    // always
    if (threesporglset)
        insertspanf(taskptr, spanfptr, linkisaptr, threesporglset, LINKTHREESPAN); // optional
    return (TRUE);
}
```

The function signature accepts exactly three endset parameters — `from`, `to`, `three`. There is no fourth parameter, no loop over additional endsets, and no `LINKFOURSPAN` call site anywhere in the codebase. A link of arity > 3 is physically unrepresentable in the storage model.

---

### Conclusion

`FINDNUMOFLINKSFROMTOTHREE` does **not** contain an explicit "exactly three endsets" filter. The intersection logic in `intersectlinksets` [`spanf2.c:95-118`] operates purely on tumbler address equality across the three span-type-indexed queries — it does not inspect or constrain the total endset count of any link.

However, the premise of the question is architecturally unreachable: **links of arity > 3 cannot exist in udanax-green.** The only endset insertion path [`do2.c:116-128`] writes at most three span entries (`LINKFROMSPAN=1`, `LINKTOSPAN=2`, `LINKTHREESPAN=3`), and no fourth span type is defined [`xanadu.h:36-38`]. There is no storage mechanism for a fourth endset, so no link with arity > 3 can ever be created, stored, or retrieved.

The operation filters by content match across up to three named endset positions — not by a count of how many endsets a link possesses.
