## Question 15 [evidence]

> If a slot's bounding set is left empty or unconstrained, does that slot match all links (wildcard), match no links, or short-circuit the conjunction?

## KB Synthesis

**NOSPECS acts as a wildcard — it drops that slot from the conjunction entirely.**

## Evidence

**Direct behavioral evidence:** [ST-FIND-LINKS] Finding 0005 documents the two search modes explicitly:

> `find_links(source_specs)` finds links by source content identity; `find_links(NOSPECS, target_specs)` finds links by target content identity. Both endpoints participate symmetrically in discovery.

When one slot receives NOSPECS, the operation succeeds and returns links matched by the *other* slot(s) only.

**AND-semantics with wildcard identity:** [FC-LINK-DELETE-ISOLATION] Finding 0029 formalizes this:

> `find_links(source_spec, target_spec)` ≡ `find_links(source_spec) ∩ find_links(target_spec)`

NOSPECS contributes the universal set to the intersection: `find_links(S, NOSPECS) = find_links(S) ∩ ALL_LINKS = find_links(S)`. It short-circuits that slot's constraint, not the conjunction itself.

**Deletion behavior confirms wildcard semantics:** [FC-LINK-DELETE-ISOLATION] Finding 0029's deletion matrix is decisive:

| Source State | Target State | `find_links(source, NOSPECS)` | `find_links(NOSPECS, target)` |
|---|---|---|---|
| Deleted | Intact | Not found | **Found** |
| Intact | Deleted | **Found** | Not found |

If NOSPECS meant "match no links," both columns would be empty. Instead, NOSPECS allows discovery through the surviving slot — confirming wildcard, not empty-intersection, behavior.

**Implementation note:** [EC-FIND-LINKS-GLOBAL] Finding 0069 shows the orgl-range dimension is also effectively unconstrained (hardcoded to width 100 from zero due to a `TRUE||` guard), so the global wildcard property extends to the orgl dimension as well.

## Summary

Passing NOSPECS for a slot is a **wildcard** that contributes the universal set to the AND conjunction. The result is the intersection of only the constrained slots. Passing NOSPECS for all three slots would return all links in the system (no KB evidence contradicts this, and [EC-FIND-LINKS-GLOBAL] suggests as much).

---

## Code Exploration

I now have all the information I need. The answer is definitively in `spanf1.c:56-103` and `spanf2.c:46-120`.

---

## Answer

**A slot with a NULL (empty/unconstrained) specset acts as a wildcard — it is skipped entirely and contributes no constraint to the conjunction.**

---

### Trace through `findlinksfromtothreesp` [`spanf1.c:56-103`]

The function receives three specsets: `fromvspecset`, `tovspecset`, `threevspecset`. Each slot is independently guarded:

```c
fromlinkset = tolinkset = threelinkset = NULL;   // spanf1.c:69

if (fromvspecset)                                // spanf1.c:70
        specset2sporglset(taskptr, fromvspecset, &fromsporglset, NOBERTREQUIRED);
if (tovspecset)                                  // spanf1.c:72
        specset2sporglset(taskptr, tovspecset, &tosporglset, NOBERTREQUIRED);
if (threevspecset)                               // spanf1.c:74
        specset2sporglset(taskptr, threevspecset, &threesporglset, NOBERTREQUIRED);
```

A NULL specset is **never passed to `specset2sporglset`**. Its corresponding link set stays NULL. The slot is invisible to the rest of the function.

---

### What `intersectlinksets` does with NULL slots [`spanf2.c:46-79`]

```c
/* If only one linkset is non-null, then just use it */    // spanf2.c:63
if (linkset1 && !linkset2 && !linkset3)
        *linkset4ptr = linkset1;                           // spanf2.c:64-65
else if (!linkset1 && linkset2 && !linkset3)
        *linkset4ptr = linkset2;                           // spanf2.c:66-67
else if (!linkset1 && !linkset2 && linkset3)
        *linkset4ptr = linkset3;                           // spanf2.c:68-69
else
        *linkset4ptr = NULL;                               // spanf2.c:70-71
```

**One constrained slot, two unconstrained (NULL):** hits the first `if` branch — returns that slot's link set directly. The two unconstrained slots added no restriction. This is the wildcard behavior.

**Two or three constrained slots:** falls to `else`, sets `*linkset4ptr = NULL`, then proceeds to the O(n²) or O(n³) intersection loops [`spanf2.c:95-118`] to find common link ISAs.

---

### The short-circuit case (distinct from wildcard)

A slot that *is* constrained (non-NULL specset) but whose specset resolves to zero matching links causes an early return:

```c
if (fromvspecset) {
        sporglset2linkset(taskptr, (typecuc*)spanfptr, fromsporglset, &fromlinkset, orglrange, LINKFROMSPAN);
        if (!fromlinkset) {                   // spanf1.c:78
                *linksetptr = NULL;
                return (TRUE);                // spanf1.c:80-81
        }
}
```

The same pattern repeats for the `to` slot [`spanf1.c:84-91`] and `three` slot [`spanf1.c:92-99`]. If any constrained slot matches no links, the function short-circuits and returns empty without evaluating the remaining slots. This is a **conjunction short-circuit on zero**, not a wildcard.

---

### Edge case: all three slots unconstrained

If all three specsets are NULL, all three link sets remain NULL. `intersectlinksets(NULL, NULL, NULL)` hits the `else` branch at `spanf2.c:70-71` and sets `*linkset4ptr = NULL`. The intersection loop body never executes (its iterators are NULL). **Result: empty set — no links returned.** All-unconstrained is not "return everything"; it's "no constraint specified → empty."

---

### Summary

| Slot state | Behavior |
|---|---|
| `specset == NULL` (unconstrained) | Wildcard — slot is skipped, contributes no constraint |
| `specset != NULL`, resolves to empty ispan/sporgl set | Short-circuits conjunction — returns empty immediately |
| `specset != NULL`, resolves to non-empty set | Participates in intersection with other constrained slots |
| All three slots unconstrained | Returns empty (not all-links) — `intersectlinksets(NULL,NULL,NULL)` → `NULL` [`spanf2.c:70-71`] |

The conjunction semantics are: **intersect only the non-NULL slots; if any non-NULL slot is empty, the whole result is empty.** `acceptablevsa` [`do2.c:110-113`] is entirely irrelevant — it always returns `TRUE` unconditionally and is never part of the link-filter path.
