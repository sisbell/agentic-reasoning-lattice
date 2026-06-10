## Question 6 [evidence]

> What filter arguments does udanax-green's link-retrieval operation (find-links-from-to-three) take, and does matching require each *specified* specset (from/to/type) to intersect its corresponding endset slot — conjunctive per-slot matching, with unspecified slots unconstrained — rather than any single slot meeting any filter?

## KB Synthesis

## Filter Arguments and Matching Semantics of `find_links_from_to_three`

### Arguments

The operation takes four filter parameters:

1. **from-specset** — V-spans matched against the link's FROM (source) endset slot
2. **to-specset** — V-spans matched against the link's TO (target) endset slot
3. **three-specset** — V-spans matched against the link's THREE (type) endset slot
4. **homedocids** — I-spans scoping by link home document (accepted syntactically, not enforced — see below)

Each specset is converted to I-addresses via the POOM; a slot accepts `NOSPECS` to leave it unconstrained. [SS-FIND-LINKS (Finding 0028)]

### Matching Semantics: Conjunctive Per-Slot

Yes, matching is conjunctive and per-slot. Each *specified* specset must produce a non-empty I-address intersection with its *corresponding* endset slot. Unspecified slots (NOSPECS) are unconstrained. [SS-FIND-LINKS (Finding 0029)]:

> `find_links(source_spec, target_spec) ≡ find_links(source_spec) ∩ find_links(target_spec)`

The internal implementation calls `intersectlinksets()` — O(n·m) or O(n·m·p) depending on how many slots are specified — which intersects the per-slot result sets. [SS-FIND-LINKS (Finding 0035)]

The search table from Finding 0029 makes this concrete:

| Source State | Target State | Search by Source | Search by Target |
|---|---|---|---|
| Intact | Intact | Found | Found |
| Deleted | Intact | Not found | Found |
| Intact | Deleted | Found | Not found |

Specifying both `source_spec` and `target_spec` requires *both* to have surviving V-stream presence — AND, not OR. [FC-LINK-DELETE-ISOLATION]

### Caveats on Specific Slots

**THREE (type) slot is non-functional.** `find_links(source, NOSPECS, type_spec)` returns empty results even when unfiltered search finds links of those types. This is a pre-existing implementation issue. [EC-TYPE-FILTER-NONFUNCTIONAL]

**homedocids filter is non-functional.** `sporglset2linkset()` contains a `TRUE||!homeset` guard that always evaluates true, replacing whatever orgl range the caller provides with a hardcoded width-100 range starting at zero. All `find_links` calls are therefore global across the orgl dimension. [EC-FIND-LINKS-GLOBAL, EC-HOMEDOCIDS-FILTER-BROKEN, PRE-FIND-LINKS (Finding 0069)]

### Summary

The operation is designed as: return all links L such that, for every *specified* (non-NOSPECS) slot k, `I-addresses(filter_k) ∩ I-addresses(L.endset_k) ≠ ∅`. That is: conjunctive intersection per slot, with unspecified slots unconstrained. In practice: the FROM and TO slots work correctly; the THREE slot is broken; and homedocids scoping is disabled entirely. [SS-FIND-LINKS, SS-SPANF-OPERATIONS]

---

## Code Exploration

I have the complete picture. Here is the full answer.

---

## `find-links-from-to-three`: Filter Arguments and Matching Semantics

### Wire Arguments (FEBE Protocol)

`getfindlinksfromtothree` in `get1.c:110–124` reads four arguments off the wire in this order:

| Prompt | Variable | Type |
|---|---|---|
| `"fromset\n"` | `fromvspecset` | `typespecset` |
| `"toset\n"` | `tovspecset` | `typespecset` |
| `"threeset\n"` | `threevspecset` | `typespecset` |
| `"home documents\n"` | `homeset` | `typeispanset` |

Each of the first three is a **specset** — a linked list of virtual-address specs (either `VSPECID` items encoding a document ISA plus virtual span set, or raw `ISPANID` items). The fourth (`homeset`) is parsed but is **explicitly discarded** in the call at `fns.c:198`:

```c
// fns.c:197-198
getfindlinksfromtothree (taskptr, &fromvspecset, &tovspecset, &threevspecset, &homeset)
&& dofindlinksfromtothree (taskptr, fromvspecset, tovspecset, threevspecset, (typeispan*)NULL/*homeset*/, &linkset)
```

The comment `/*homeset*/` confirms the intent: the `homeset` parameter is dead on this code path.

---

### Execution Path

```
findlinksfromtothree (fns.c:189)
  → dofindlinksfromtothree (do1.c:348)
    → findlinksfromtothreesp (spanf1.c:56)
```

`dofindlinksfromtothree` is a one-liner pass-through (`do1.c:348–353`).

---

### Core Matching Logic: `findlinksfromtothreesp` (`spanf1.c:56–103`)

```c
// spanf1.c:69-100
fromlinkset = tolinkset = threelinkset = NULL;

if (fromvspecset)
    specset2sporglset(taskptr, fromvspecset, &fromsporglset, NOBERTREQUIRED);
if (tovspecset)
    specset2sporglset(taskptr, tovspecset, &tosporglset, NOBERTREQUIRED);
if (threevspecset)
    specset2sporglset(taskptr, threevspecset, &threesporglset, NOBERTREQUIRED);

if (fromvspecset) {
    sporglset2linkset(taskptr, spanfptr, fromsporglset, &fromlinkset, orglrange, LINKFROMSPAN);
    if (!fromlinkset) { *linksetptr = NULL; return (TRUE); }   // short-circuit
}
if (tovspecset) {
    sporglset2linkset(taskptr, spanfptr, tosporglset, &tolinkset, orglrange, LINKTOSPAN);
    if (!tolinkset)   { *linksetptr = NULL; return (TRUE); }   // short-circuit
}
if (threevspecset) {
    sporglset2linkset(taskptr, spanfptr, threesporglset, &threelinkset, orglrange, LINKTHREESPAN);
    if (!threelinkset){ *linksetptr = NULL; return (TRUE); }   // short-circuit
}

intersectlinksets(taskptr, fromlinkset, tolinkset, threelinkset, linksetptr);
```

Three constants govern which endset slot each specset is matched against (`xanadu.h:36–38`):

```c
#define LINKFROMSPAN  1
#define LINKTOSPAN    2
#define LINKTHREESPAN 3
```

`sporglset2linkset` in `sporgl.c:222–237` calls `sporglset2linksetinrange` (`sporgl.c:239–269`) which uses `retrieverestricted` to walk the spanfilade and collect all link ISAs whose endset in the **named slot** intersects the supplied physical span set. The slot is passed explicitly; a from-specset is only looked up in slot 1, a to-specset only in slot 2, a three-specset only in slot 3. There is no cross-slot comparison.

---

### Final Set Intersection: `intersectlinksets` (`spanf2.c:46–120`)

```c
// spanf2.c:63-78 — pass-through when only one set is non-NULL
if  (linkset1 && !linkset2 && !linkset3)  *linkset4ptr = linkset1;
else if (!linkset1 && linkset2 && !linkset3)  *linkset4ptr = linkset2;
else if (!linkset1 && !linkset2 && linkset3)  *linkset4ptr = linkset3;
else *linkset4ptr = NULL;

if (*linkset4ptr) return;   // single-set result, done

// spanf2.c:95-118 — two-set or three-set intersection by tumbler equality
if (!linkset3) {
    for (temp1 ...) for (temp2 ...)
        if (tumblereq(&temp1->address, &temp2->address))
            emit link;
} else {
    for (temp1 ...) for (temp2 ...) for (temp3 ...)
        if (tumblereq(&temp1->address, &temp2->address)
            && tumblereq(&temp2->address, &temp3->address))
            emit link;
}
```

A link address must appear in **every non-NULL slot result set** to pass.

---

### Answer to the Question

**Yes — the matching is conjunctive per-slot, with unspecified slots unconstrained.**

Specifically:

1. **Each specified specset is matched exclusively against its own slot.** The from-specset is intersected only with `LINKFROMSPAN` (1) storage; the to-specset only with `LINKTOSPAN` (2); the three-specset only with `LINKTHREESPAN` (3). There is no cross-slot matching at any level.

2. **A link must satisfy every specified filter simultaneously.** After each slot query, only links that appeared in *all* non-NULL per-slot result sets survive `intersectlinksets`. This is a conjunction: *from-matches* ∩ *to-matches* ∩ *three-matches*.

3. **Unspecified slots are completely unconstrained.** If a specset argument is `NULL`, its corresponding per-slot query is skipped entirely (`spanf1.c:70–99`, guarded by `if (fromvspecset)` etc.) and a NULL linkset is passed to `intersectlinksets`, which treats it as "no constraint from this slot" (`spanf2.c:63–69`).

4. **Early exit on empty per-slot results.** If a specified specset has no matching links in its slot, the function immediately returns an empty result without querying the remaining slots (`spanf1.c:78–82`, `86–90`, `94–98`). This is a short-circuit optimization, not a semantic difference.

5. **`homeset` is inoperative.** The fourth wire argument (`home documents`) is parsed but hardwired to `NULL` before being passed to `dofindlinksfromtothree` (`fns.c:198`). It has no effect on the query.
