## Question 11 [evidence]

> When FINDLINKSFROMTOTHREE is given all four bounding sets, must each returned link's source endset overlap the from-set AND its target endset overlap the to-set AND its type endset overlap the third-set simultaneously (conjunctive intersection), or are the slots matched disjunctively?

## KB Synthesis

**Conjunctive (AND).** All non-NOSPECS bounding sets must be simultaneously satisfied.

The clearest KB evidence is the cross-endpoint search matrix from [ST-FIND-LINKS] (Finding 0029):

> `find_links()` uses AND semantics when called with multiple criteria. When both source and target specs are provided, both endpoints must have V-stream presence for the link to be found.
>
> `find_links(source_spec, target_spec)` ≡ `find_links(source_spec) ∩ find_links(target_spec)`

The matrix confirms this directly:

| Source | Target | Search(source, target) |
|--------|--------|------------------------|
| Intact | Intact | Found |
| Deleted | Intact | Not found |
| Intact | Deleted | Not found |
| Deleted | Deleted | Not found |

When searching by source alone, a deleted target doesn't matter; when searching by both, both must be intact.

The implementation mechanism is described in [ST-FIND-LINKS] (Finding 0035): `intersectlinksets()` at `backend/spanf2.c:46-120` performs O(n×m) or O(n×m×p) intersection across the result sets from each independently-queried endset type. The spanfilade maintains separate ORGLRANGE subspaces LINKFROMSPAN=1, LINKTOSPAN=2, LINKTHREESPAN=3 (per [SS-RETRIEVE-ENDSETS]), and each is searched independently, with the results intersected.

Passing NOSPECS for any slot simply removes that constraint from the intersection—it contributes the universal set rather than the empty set.

---

## Code Exploration

I now have all the code I need. Here is the complete, citation-grounded answer.

---

## FINDLINKSFROMTOTHREE: Conjunctive (AND) Matching

**The matching is strictly conjunctive.** When all three bounding sets are provided, a link must satisfy all three constraints simultaneously. No link passes unless its source endset overlaps the from-set AND its target endset overlaps the to-set AND its type endset overlaps the third-set.

---

### Call Chain

**`fns.c:189–202`** — FEBE handler `findlinksfromtothree()`:
```c
if (
   getfindlinksfromtothree (taskptr, &fromvspecset, &tovspecset, &threevspecset, &homeset)
&& dofindlinksfromtothree (taskptr, fromvspecset, tovspecset, threevspecset, (typeispan*)NULL, &linkset))
    putfindlinksfromtothree (taskptr, linkset);
```

**`do1.c:348–353`** — `dofindlinksfromtothree()` is a thin wrapper:
```c
return findlinksfromtothreesp(taskptr, spanf, fromvspecset, tovspecset, threevspecset, orglrangeptr, linksetptr);
```

---

### Core Logic: `findlinksfromtothreesp` (`spanf1.c:56–103`)

This function processes each filter independently, then intersects the three resulting link sets:

**Step 1 — Per-slot lookup with early-exit on empty** (`spanf1.c:70–99`):

```c
if (fromvspecset) {
    sporglset2linkset(..., &fromlinkset, orglrange, LINKFROMSPAN);
    if (!fromlinkset) { *linksetptr = NULL; return (TRUE); }   // ← AND semantics: if from-filter matches nothing, result is empty
}
if (tovspecset) {
    sporglset2linkset(..., &tolinkset, orglrange, LINKTOSPAN);
    if (!tolinkset) { *linksetptr = NULL; return (TRUE); }      // ← same
}
if (threevspecset) {
    sporglset2linkset(..., &threelinkset, orglrange, LINKTHREESPAN);
    if (!threelinkset) { *linksetptr = NULL; return (TRUE); }   // ← same
}
```

Each `sporglset2linkset` call uses a distinct span type constant (`LINKFROMSPAN`, `LINKTOSPAN`, `LINKTHREESPAN`) — these address different structural slots of the link record. If any one filter set is non-null but produces zero matching links, the whole result is immediately `NULL`. That is AND semantics: a miss in any slot kills the entire result.

**Step 2 — Intersection** (`spanf1.c:100`):
```c
intersectlinksets(taskptr, fromlinkset, tolinkset, threelinkset, linksetptr);
```

---

### `intersectlinksets` (`spanf2.c:46–120`)

When all three linksets are non-null, the function uses a triple-nested loop with a compound AND condition (`spanf2.c:106–118`):

```c
for (; temp1; temp1 = temp1->next) {
    for (temp2 = linkset2; temp2; temp2 = temp2->next) {
        for (temp3 = linkset3; temp3; temp3 = temp3->next) {
            if (tumblereq (&temp1->address, &temp2->address)
                && tumblereq (&temp2->address, &temp3->address)) {
                linkset4 = makelinkitem (taskptr, &temp1->address);
                *linkset4ptr = linkset4;
                linkset4ptr = &linkset4->next;
            }
        }
    }
}
```

A link's tumbler address must appear in all three independently-computed linksets: `temp1->address == temp2->address AND temp2->address == temp3->address`. Disjunction is not possible here — there is no OR branch.

The earlier degenerate cases (`spanf2.c:63–71`) only fire when fewer than two of the three linksets are non-null (i.e., when fewer than two filter slots were specified), passing through the single non-null set unchanged. This is not OR logic; it is the identity case for an absent filter.

---

### Summary

| Condition | Result |
|---|---|
| Any provided filter set matches zero links | Entire result is `NULL` (early exit, `spanf1.c:78–98`) |
| All three filter sets provided | Triple intersection: link must be in all three match sets (`spanf2.c:109–110`) |
| Two filter sets provided | Pairwise intersection: link must be in both match sets (`spanf2.c:96–104`) |
| One filter set provided | That set returned unmodified (`spanf2.c:64–69`) |

**The matching is conjunctive.** The three slots (from-endset, to-endset, type-endset) are evaluated independently against different structural positions of each link record — `LINKFROMSPAN`, `LINKTOSPAN`, `LINKTHREESPAN` — and a link is returned only when it satisfies every non-null constraint simultaneously.
