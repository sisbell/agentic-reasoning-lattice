## Question 19 [gregory]

> When `FOLLOWLINK` / `RETRIEVEENDSETS` returns a link's endsets and some referenced I-addresses exist in no current POOM, what exactly does `span2spanset` do during I→V conversion — does it silently drop the unreachable portions and return a truncated specset, or does it signal incompleteness?

## KB Synthesis

`span2spanset` silently drops unreachable portions and returns a truncated specset with no signal of incompleteness.

The mechanism is documented in [SS-FOLLOWLINK] / [INV-ITOV-FILTERING] (Finding 0048):

> `span2spanset()` uses `retrieverestricted()` against the document's orgl. If an I-address has no POOM mapping, `retrieverestricted` returns NULL and the I-address is **silently dropped** — no V-span is added to the result.

Code reference: `backend/orglinks.c:425-449`, lines 446-448.

This behavior is universal across all I→V conversion paths. [INV-ITOV-FILTERING] states it as a system-wide invariant:

> Unreferenced I-addresses are silently excluded from V-address results. No operation that performs I→V conversion will ever return a V-address for an unreferenced I-address.

The three observable outcome cases from [EC-GHOST-LINK] are:

| Endset state | Result |
|---|---|
| All I-addresses have POOM mappings | Full specset |
| Some I-addresses unreachable | Partial specset (live ones only) |
| All I-addresses unreachable | Empty `[]` — operation still returns success |

In no case does the operation signal incompleteness to the caller. A caller receiving a partial or empty result from FOLLOWLINK/RETRIEVEENDSETS cannot distinguish "the endset genuinely covers only this content" from "some content exists in I-space but has no current V-position mapping."

The formal invariant is: `result(op) ⊆ { v | ∃ i : poom.d(v) = i }` — results are always a subset of currently-mapped V-positions. There is no "truncation flag" or error code. Completeness verification requires the caller to independently check whether the returned specsets cover all expected I-address ranges, which requires knowledge of what those ranges should be.

---

## Code Exploration

Now I have everything I need. Let me trace the complete execution chain for both operations.

---

## Answer: What `span2spanset` Does When I-Addresses Are Unreachable

The answer is **silent drop with no incompleteness signal**. Here is the complete traced path.

---

### Call Chain: FOLLOWLINK

```
fns.c:followlink
  → dofollowlink [do1.c:223]
      → link2sporglset [sporgl.c:67]         # reads I-spans from link POOM
      → linksporglset2specset [sporgl.c:97]
          → linksporglset2vspec [sporgl.c:127]
              → sporglset2vspanset [sporgl.c:141]
                  → ispan2vspanset [orglinks.c:389]
                      → permute [orglinks.c:404]
                          → span2spanset [orglinks.c:425]   ← KEY FUNCTION
```

### Call Chain: RETRIEVEENDSETS

```
fns.c:retrieveendsets
  → doretrieveendsets [do1.c:369]
      → retrieveendsetsfromspanf [spanf1.c:190]
          → retrievesporglsetinrange [spanf1.c:237]     # reads from spanfilade
          → linksporglset2specset [sporgl.c:97]
              → linksporglset2vspec [sporgl.c:127]
                  → sporglset2vspanset [sporgl.c:141]
                      → ispan2vspanset [orglinks.c:389]
                          → permute [orglinks.c:404]
                              → span2spanset [orglinks.c:425]   ← SAME KEY FUNCTION
```

Both paths converge on the same I→V conversion machinery.

---

### The Critical Function: `span2spanset` [orglinks.c:425–454]

```c
typespanset *span2spanset(typetask *taskptr, typeorgl orgl, typespanset restrictionspanptr,
                          INT restrictionindex, typespanset *targspansetptr, INT targindex)
{
    typecontext *context, *c, *retrieverestricted();
    typespan foundspan;
    typespan *nextptr;

    context = retrieverestricted((typecuc*)orgl, restrictionspanptr, restrictionindex,
                                 (typespan*)NULL, targindex, (typeisa*)NULL);

    for (c = context; c; c = c->nextcontext) {
        context2span (c, restrictionspanptr, restrictionindex, &foundspan, targindex);
        nextptr = (typespan *)onitemlist (taskptr, (typeitem*)&foundspan, (typeitemset*)targspansetptr);
    }
    if(!context){
        return(targspansetptr);   // ← returns unchanged pointer, no error
    }
    contextfree (context);
    return (&nextptr->next);
}
```

The function calls `retrieverestricted` on the link's POOM (ORGL), restricted to the I-span in question, asking for V-dimension output.

---

### What `retrieverestricted` Returns for Unmapped I-Addresses

`retrieverestricted` [retrie.c:56–85] delegates to `retrieveinarea` → `findcbcinarea2d` [retrie.c:229–268]:

```c
int findcbcinarea2d(..., typecontext **headptr, ...) {
    for (; crumptr; crumptr = getrightbro(crumptr)) {
        if (!crumqualifies2d(...)) {
            continue;                // skip non-intersecting crums
        }
        if (crumptr->height != 0) {
            findcbcinarea2d(findleftson(...), ...);   // recurse
        } else {
            context = makecontextfromcbc(...);
            incontextlistnd(headptr, context, index1);  // only appended when found
        }
    }
}
```

`headptr` is initialized to `NULL` before the call [retrie.c:93]. If no POOM crum has an I-coordinate range overlapping the queried I-span, **no `incontextlistnd` call ever fires** and `headptr` stays NULL. `retrieverestricted` returns NULL.

---

### What Happens Back in `span2spanset` When Context Is NULL

```c
context = retrieverestricted(...);        // returns NULL — I-span has no V-mapping

for (c = context; c; c = c->nextcontext) {  // loop body never executes
    ...
}
if(!context){
    return(targspansetptr);   // ← returns the UNMODIFIED output list pointer
}
```

`targspansetptr` is returned without any new span appended. **No V-span is added for the unreachable portion. No error is raised.**

---

### What Happens Further Up the Chain

**`permute` [orglinks.c:404–422]** iterates over all input I-spans and calls `span2spanset` for each. Spans that map to nothing are silently skipped. The final return value is `save` — the original head of the output list:

```c
typespanset *permute(...) {
    save = targspansetptr;
    for (; restrictionspanset; restrictionspanset = restrictionspanset->next) {
        targspansetptr = span2spanset(...);  // may add nothing for this span
    }
    return (save);   // may be partially or fully empty
}
```

**`sporglset2vspanset` [sporgl.c:141–176]** does not check whether `ispan2vspanset` added anything:

```c
vspansetptr = ispan2vspanset(taskptr, orgl, &ispan, vspansetptr);  // return ignored
```

**`linksporglset2vspec` [sporgl.c:127–137]** initializes `vspanset` to NULL, then calls `sporglset2vspanset`. If the I→V conversion finds nothing, the field stays NULL and no error is raised:

```c
specptr->vspanset = NULL;
sporglset2vspanset(taskptr, homedoc, sporglsetptr, &specptr->vspanset, type);
// specptr->vspanset may remain NULL — no check
```

**`linksporglset2specset` [sporgl.c:97–123]** always returns TRUE regardless of whether the conversion produced any V-addresses:

```c
bool linksporglset2specset(...) {
    *specsetptr = NULL;
    for (; sporglset; ...) {
        specset = taskalloc(..., sizeof(typevspec));
        ...
        linksporglset2vspec(...);    // may produce empty vspanset
        ...
        *specsetptr = specset;       // the shell VSPEC is installed anyway
        ...
    }
    return (TRUE);   // always TRUE
}
```

**`retrieveendsetsfromspanf` [spanf1.c:190–235]** and **`dofollowlink` [do1.c:223–232]** both propagate a TRUE success status unconditionally when the structural operations succeed, regardless of whether the resulting specsets are empty.

---

### Conclusion: Silent Drop, No Incompleteness Signal

When `span2spanset` encounters I-addresses that have no V-mapping in the POOM:

1. **`retrieverestricted` returns NULL** — the 2D tree search finds no qualifying crums [retrie.c:93, 97, 107].
2. **`span2spanset` returns `targspansetptr` unchanged** [orglinks.c:446–448] — the `if(!context)` guard exits with no entries added, no error.
3. **`permute` returns a partially or fully empty V-span set** [orglinks.c:421] — missing I-spans silently produce no output.
4. **`linksporglset2vspec` leaves `vspanset = NULL`** [sporgl.c:135] if nothing mapped.
5. **`linksporglset2specset` returns TRUE** [sporgl.c:122] with a VSPEC shell whose `vspanset` is NULL.
6. **The top-level FOLLOWLINK/RETRIEVEENDSETS handlers report success** — `putfollowlink` / `putretrieveendsets` are called with a specset that may contain endset entries with empty vspansets [fns.c:124, fns.c:358].

There is **no error code, no partial-result flag, no callback, and no way for the caller to distinguish** "this I-span had a V-mapping that was returned" from "this I-span had no V-mapping and was silently dropped." The returned specset is simply truncated — shorter than what the stored I-spans would imply — with no annotation indicating the gap.
