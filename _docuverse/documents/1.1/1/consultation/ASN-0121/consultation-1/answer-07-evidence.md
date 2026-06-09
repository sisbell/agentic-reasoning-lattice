## Question 7 [evidence]

> When a search request supplies a constrained endset slot whose span-set is empty (coverage `∅`), does the back end treat it the same as a NOSPECS/wildcard slot, or does it yield an empty link-set for that slot — and is this distinct from the all-wildcard handling in `intersectlinksets` (Q15)?

## KB Synthesis

The KB does not contain sufficient evidence to answer this definitively. Here is what it does and does not establish:

**What the KB documents:**

NOSPECS is a distinct sentinel, not just an empty span-set. Single-endpoint search passes NOSPECS for the unconstrained slot, and the system skips that slot's constraint entirely — returning all links matching the other endpoint [SS-FIND-LINKS, Finding 0005]. The AND semantics of multi-criteria search require *all* constrained slots to match [SS-FIND-LINKS, Finding 0029].

The core mechanism converts each specset to I-addresses via `specset2ispanset`, then checks intersection with link endpoint I-addresses [SS-FIND-LINKS, Finding 0028]. An empty specset (∅ coverage) would produce an empty I-span set after conversion. Under strict AND semantics, a slot with an empty I-span set would intersect with nothing, yielding ∅ for that slot and propagating to the overall result.

**What the KB does not document:**

The KB mentions `intersectlinksets` only by name and complexity (O(n·m) or O(n·m·p)) [SS-FIND-LINKS, Finding 0035]. It does not document how `intersectlinksets` or `findlinksfromtothreesp` distinguish between a NULL/NOSPECS argument and an argument representing a non-NULL but zero-element span-set. Whether the code path for an empty specset ever short-circuits to wildcard behavior — or whether it collapses the result to ∅ — is not established by any finding in the KB.

**Conclusion:** Based solely on KB evidence, the mechanistic expectation is that ∅-coverage ≠ NOSPECS: an empty span-set converts to empty I-spans, finds no intersection, and yields ∅, while NOSPECS bypasses the slot entirely. But the `intersectlinksets` behavior on an empty input is not confirmed by any KB entry, and the question of whether a "Q15 all-wildcard" path exists inside that function is outside the KB's coverage.

---

## Code Exploration

I now have everything needed for a complete, cited answer.

---

## Answer

### Protocol encoding: two distinct cases

`getspecset` (`get2.c:162–192`) offers two fundamentally different encodings for a slot:

**Wildcard (NOSPECS):** client answers `FALSE` to *"any spans or vspecs?"*
```c
// get2.c:173–175
if (!any) {
    *specsetptr = NULL;
    return (TRUE);
}
```
Result: `fromvspecset == NULL`.

**Constrained slot with empty span-set (∅):** client answers `TRUE` (allocates a `typevspec`), supplies a `docisa`, then answers `FALSE` to *"any spans?"* inside `getspanset`:
```c
// get2.c:215–217
if (!any) {
    *spansetptr = NULL;
    return (TRUE);
}
```
Result: `fromvspecset != NULL`, but `fromvspecset->vspanset == NULL`.

---

### Execution paths diverge in `findlinksfromtothreesp`

The core of the find operation is `findlinksfromtothreesp` (`spanf1.c:56`).

#### Wildcard path (NULL specset)

```c
// spanf1.c:70–71
if (fromvspecset)
    specset2sporglset (taskptr, fromvspecset, &fromsporglset, NOBERTREQUIRED);
```

`if (fromvspecset)` is **false** — the entire block is skipped. `fromlinkset` stays `NULL` (initialised at `spanf1.c:69`). The slot is invisible. Execution falls through to:

```c
// spanf1.c:100
intersectlinksets(taskptr, fromlinkset, tolinkset, threelinkset, linksetptr);
```

In `intersectlinksets` (`spanf2.c:46`), with `linkset1 == NULL`:

```c
// spanf2.c:66–67
else if (!linkset1 && linkset2 && !linkset3)
    *linkset4ptr = linkset2;
```

If `tolinkset` is non-empty the TO slot's results **become the result** — the wildcard FROM slot is invisible and the other constrained slots drive the answer.

#### Empty span-set (∅) path

`if (fromvspecset)` is **true** (specset pointer is non-NULL). `specset2sporglset` (`sporgl.c:14`) is called:

```c
// sporgl.c:23–27  (inside specset2sporglset)
} else if (((typeitemheader *)specset)->itemid == VSPECID) {
    if (!(sporglsetptr = vspanset2sporglset (taskptr, &((typevspec *)specset)->docisa,
            ((typevspec *)specset)->vspanset, sporglsetptr, type))) {
        return (FALSE);
    }
}
```

Inside `vspanset2sporglset` (`sporgl.c:35`):

```c
// sporgl.c:47
for (; vspanset; vspanset = vspanset->next) { ... }
```

`vspanset == NULL` → **loop body never executes** → no sporgls are appended. The function returns `sporglsetptr` unchanged; `*sporglsetptr = NULL` (`sporgl.c:30`) terminates the list. `fromsporglset` is NULL.

`sporglset2linkset` (`sporgl.c:222`) is then called with that NULL sporglset:

```c
// sporgl.c:250  (inside sporglset2linksetinrange)
for (; sporglset; sporglset = (typesporglset)((typeitemheader *)sporglset)->next) {
```

`sporglset == NULL` → **loop never executes** → `fromlinkset` remains NULL.

Back in `findlinksfromtothreesp`:

```c
// spanf1.c:78–82
if (!fromlinkset) {
    *linksetptr = NULL;
    debug = olddebug;
    return (TRUE);    // ← SHORT-CIRCUIT
}
```

`intersectlinksets` is **never called**. The find returns `NULL` (empty link-set) regardless of what the other two slots contain.

---

### The semantic distinction

| Slot encoding | `intersectlinksets` reached? | Effect on result |
|---|---|---|
| NULL specset (wildcard) | Yes | Absent from intersection — other constrained slots drive result |
| Non-NULL specset, vspanset=∅ | **No** — short-circuits at `spanf1.c:78` | Forces entire find to ∅, regardless of other slots |

Empty ∅ behaves as a **universal zero element** (0 × anything = 0). A wildcard is a **unit element** (1 × anything = anything). These are distinct at the semantic level even though both ultimately yield a NULL link-set when the other slots are also unconstrained.

---

### Relation to the Q15 all-wildcard case in `intersectlinksets`

Q15 concerned what `intersectlinksets` does when all three slots are wildcard (all linksets NULL). With `linkset1=NULL, linkset2=NULL, linkset3=NULL`:

```c
// spanf2.c:63–71
/* If only one linkset is non-null, then just use it */
if (linkset1 && !linkset2 && !linkset3)          // false
    ...
else if (!linkset1 && linkset2 && !linkset3)      // false
    ...
else if (!linkset1 && !linkset2 && linkset3)      // false
    ...
else
    *linkset4ptr = NULL;                           // ← taken

if (*linkset4ptr) {                               // false — falls through
    return(0);
}
```

Code falls through to the two-way intersection loop (`spanf2.c:96`) with `temp1` **uninitialized** (no assignment when all three are NULL — `if (linkset1)` at line 83 is false). In practice the loop body does not execute and the result is NULL, but this is a latent undefined-behaviour path.

**The critical distinction from the ∅ case:** the all-wildcard Q15 scenario *does* enter `intersectlinksets`; the empty-span-set case *never reaches* `intersectlinksets`. They are mechanically disjoint even though the observable result is the same empty link-set.

---

### Summary

No — a constrained endset slot with empty span-set (∅) is **not** treated as a wildcard. The code at `spanf1.c:76–82` detects that a constrained slot produced no matching links (`!fromlinkset`) and **short-circuits the entire find to ∅**, bypassing `intersectlinksets` entirely. A wildcard (NULL specset) is instead silently omitted from the intersection at `spanf1.c:70`, leaving `intersectlinksets` free to use the remaining constrained slots. The Q15 all-wildcard case is a third distinct path — it enters `intersectlinksets` with all-NULL linksets, falling through to undefined-behaviour territory, but observationally returns ∅.
