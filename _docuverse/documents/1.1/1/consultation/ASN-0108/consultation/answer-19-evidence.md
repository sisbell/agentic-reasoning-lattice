## Question 19 [evidence]

> When the EC-FIND-LINKS-GLOBAL behavior (`TRUE||!homeset` override with hardcoded width 100) is in effect, does the ignored orgl-range parameter affect the windowed enumeration order or only the global membership of the result set?

## KB Synthesis

The KB is sufficient to answer this directly.

**The ignored orgl-range parameter affects neither membership nor ordering.**

[EC-FIND-LINKS-GLOBAL] and [PRE-FIND-LINKS] (Finding 0069) establish the mechanism: `sporglset2linkset()` unconditionally replaces the caller's orgl-range with a hardcoded constant `{stream: 0, width: 100}` before the actual spanfilade search executes. The substitution happens upstream of all traversal — both the membership predicate and any accumulation ordering are computed against this fixed constant, not the caller's argument.

Concretely:
- **Membership** is determined solely by span-dimension (I-address) intersection, since the orgl range is always the same wide constant regardless of input.
- **Enumeration order** is produced by `incontextlistnd()` [SS-CONTEXT-LIST], which insertion-sorts results by the queried span-dimension address during B-tree traversal. The orgl-range plays no role in that sort key.

For pagination specifically, [SS-PAGINATE-LINKS] confirms that FINDNEXTNLINKSFROMTOTHREE re-executes the full `findlinksfromtothreesp()` search on every call. Since that search always uses the hardcoded orgl range, both the result-set membership and the list ordering it produces are deterministic and independent of the caller's orgl-range argument. A different orgl-range value produces an identical linked list — no difference in which links appear, and no difference in the order the cursor walks them.

---

## Code Exploration

I now have everything I need. Here is my complete analysis.

---

## EC-FIND-LINKS-GLOBAL: Does the Ignored Orgl-Range Affect Enumeration Order or Only Membership?

### The Complete Call Chain

**Step 1 — `fns.c:197-198`**: For `FINDLINKSFROMTOTHREE`, the client's homeset is already discarded at the FEBE handler before any orgl logic runs:

```c
getfindlinksfromtothree (taskptr, &fromvspecset, &tovspecset, &threevspecset, &homeset)
&& dofindlinksfromtothree (taskptr, fromvspecset, tovspecset, threevspecset, (typeispan*)NULL/*homeset*/, &linkset))
```

The comment `/*homeset*/` confirms this is intentional suppression. The client's orgl-range is gone before `sporgl.c` is even reached.

**Step 2 — `do1.c:352`**: `dofindlinksfromtothree` is a thin wrapper that passes the NULL straight through:

```c
return findlinksfromtothreesp(taskptr, spanf, fromvspecset, tovspecset, threevspecset, orglrangeptr, linksetptr);
```

**Step 3 — `spanf1.c:77, 85, 93`**: `findlinksfromtothreesp` passes `orglrange` (NULL) to all three end-type calls:

```c
sporglset2linkset (taskptr, (typecuc*)spanfptr, fromsporglset, &fromlinkset, orglrange, LINKFROMSPAN);
sporglset2linkset (taskptr, (typecuc*)spanfptr, tosporglset, &tolinkset, orglrange, LINKTOSPAN);
sporglset2linkset (taskptr, (typecuc*)spanfptr, threesporglset, &threelinkset, orglrange, LINKTHREESPAN);
```

**Step 4 — `sporgl.c:227-233`**: The override fires unconditionally:

```c
if (TRUE||!homeset) {
    tumblerclear (&nullhomeset.stream);
    tumblerclear (&nullhomeset.width);
    nullhomeset.width.mantissa[0] = 100;
    nullhomeset.next = NULL;
    homeset = &nullhomeset;
}
```

The `TRUE||` short-circuits any null check. The incoming `homeset` — NULL or otherwise — is **unconditionally replaced** with a synthetic span `{stream=0, width=100}`. For `FINDLINKSFROMTOTHREE` specifically the parameter was already NULL at `fns.c:198`; the `TRUE||` makes the override redundant but absolute.

**Step 5 — `sporgl.c:234-236`**: The loop iterates over only the one synthetic element:

```c
for (; homeset; homeset = homeset->next) {
    sporglset2linksetinrange (taskptr, spanfptr, sporglset, linksetptr, homeset, spantype);
}
```

**Step 6 — `sporgl.c:256-259`**: Inside `sporglset2linksetinrange`, the synthetic orglrange constructs the spanfilade lookup range:

```c
if (orglrange) {
    prefixtumbler(&orglrange->stream, spantype, &range.stream);
    prefixtumbler (&orglrange->width, 0, &range.width);
    context = retrieverestricted (spanfptr, (typespan*)sporglset, SPANRANGE, &range, ORGLRANGE, (typeisa*)infoptr);
```

`prefixtumbler` (`tumble.c:641`) prepends `bint` as the high-order element:

```c
temp1.mantissa[0] = bint;
movetumbler (aptr, &temp2);
if (!iszerotumbler (&temp2))
    temp2.exp -= 1;
tumbleradd (&temp1, &temp2, cptr);
```

With `nullhomeset.stream=0` and `nullhomeset.width=100`:
- `range.stream = prefixtumbler(0, spantype)` → `spantype` (1, 2, or 3 depending on FROM/TO/THREE)
- `range.width = prefixtumbler(100, 0)` → effectively width 100 in tumbler space

This range is the ORGLRANGE restriction passed to `retrieverestricted`. It defines which link ISAs the spanfilade will visit.

**Step 7 — `spanf2.c:26-44`** (`onlinklist`): Contexts returned by `retrieverestricted` are appended to the link list in traversal order — tail-append:

```c
for (temp = *linksetptr; nextlink = temp->next; temp = nextlink) {
    if (tumblereq (&temp->address, linkisaptr)) return(0);
}
temp->next = linkset;
```

Order is strictly determined by the order `retrieverestricted` emits contexts — which is enfilade traversal order (tumbler-sorted within the ORGLRANGE window).

**Step 8 — `spanf2.c:96-103`** (`intersectlinksets`): When only one end-set is queried (e.g., FROM only), the list is returned as-is (`*linkset4ptr = linkset1`). When two or three intersect, the loop at lines 96-104 iterates `temp1` in its existing order and emits matches — so output order follows `temp1` (the FROM set), which follows enfilade traversal order.

**Step 9 — `spanf1.c:126-146`** (`findnextnlinksfromtothreesp`): Windowed enumeration is a linear scan through the assembled linkset, starting from `lastlinkisaptr`:

```c
for (; linkset; linkset = linkset->next) {
    if (tumblereq (&linkset->address, lastlinkisaptr)) {
        *nextlinksetptr = linkset->next;
        break;
    }
}
```

The cursor is a link ISA tumbler address (not a position in orglrange). The order of the scan is whatever order `sporglset2linksetinrange` produced — enfilade traversal order within the synthetic [spantype, spantype+100) window.

---

### Answer

**The ignored orgl-range parameter affects neither the windowed enumeration order nor the global membership of the result set.**

The `TRUE||!homeset` guard at `sporgl.c:227` unconditionally intercepts and discards the incoming parameter. The original parameter — already forced to NULL at `fns.c:198` for `FINDLINKSFROMTOTHREE` — is replaced with a hardcoded synthetic span `{stream=0, width=100}` before it can influence anything.

The **global membership** of the result set is determined solely by the synthetic `{stream=0, width=100}` orglrange passed to `retrieverestricted`. This defines a fixed ORGLRANGE window of tumbler width 100, prefixed by `spantype`, regardless of what the client sent.

The **windowed enumeration order** is determined by enfilade traversal order within that fixed window. `retrieverestricted` visits link ISAs in tumbler order; `onlinklist` appends them in that order; `intersectlinksets` preserves the FROM-set order; `findnextnlinksfromtothreesp` does a linear cursor scan through the resulting ordered list. None of these steps reference the original orgl-range parameter at all — it was discarded before step 4.

In short: the `TRUE||!homeset` override makes the orgl-range parameter **a write-only input** — it can be read from the protocol wire but has zero downstream effect on what the backend retrieves or in what order. Both membership and order are fully determined by the hardcoded width-100 synthetic span.
