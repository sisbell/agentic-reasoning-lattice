## Question 18 [gregory]

> The spanfilade indexes one DOCISPAN entry per contiguous I-span at creation time — if a link's endset references I-addresses that were inserted as separate operations (producing multiple I-spans), does the spanfilade store multiple entries per endset, and does the search correctly aggregate them?

## KB Synthesis

Yes — multiple entries are stored, and search aggregates them correctly.

**Spanfilade storage per endset:**

When a link is created, [INT-SPORGL-LINK-INDEX] (Finding 0013) documents the path: `insertendsetsinspanf()` receives a sporglset and iterates over it, inserting one spanfilade entry per sporgl. A sporgl represents one contiguous I-address region. From [ST-LINK-CREATE] (Finding 0037):

> `vspanset2sporglset` calls `vspanset2ispanset` which walks the POOM to discover all I-address regions, producing one I-span per contiguous region. The front end sees a simple contiguous selection; the backend decomposes it into identity-preserving references.

So for a link whose endset V-span maps to N non-contiguous I-regions (e.g., content transcluded from multiple sources), N sporgls are created and N spanfilade entries are indexed. [SS-DOCISPAN] (Finding 0047) confirms the per-span granularity: `insertspanf` loops over the `ispanset` linked list making one `insertnd` call per `typeispan` struct.

**Search aggregation:**

The search operates over all spanning entries and aggregates by link ISA. From [SS-FIND-LINKS] (Finding 0035):

> `intersectlinksets()`: `backend/spanf2.c:46-120` — O(n*m) or O(n*m*p) intersection

The intersection finds the link if *any* of its indexed I-spans overlaps the query. [EC-LINK-PARTIAL-SURVIVAL] confirms this per-span independence directly:

> Because each I-span in a link endset independently tracks its content, partial survival is possible. If document A (source of "AA") is deleted but document B (source of "BB") remains, the link endset retains the I-span for "BB" while the I-span for "AA" becomes unresolvable. The link survives partially.

So yes to both parts: the spanfilade stores one entry per I-span in the endset (not one per endset), and the intersection-based search correctly returns the link if any constituent entry matches — with no additional aggregation logic needed because the link ISA is embedded in each entry.

---

## Code Exploration

I now have all the source I need. Here is the complete, citation-backed answer.

---

## Answer: Spanfilade Indexing of Multi-I-span Endsets

### Short answer

**Yes and yes.** When an endset references I-addresses from N separate insert operations (producing N I-spans), `insertspanf` stores N separate spanfilade entries — one per I-span. The search in `sporglset2linksetinrange` iterates over all query I-spans and unions the results before intersection, so all matching entries are found. There is one deduplication edge case (last-element check missing in `onlinklist`) noted below.

---

### 1. Insertion: one spanfilade entry per I-span

`insertspanf` [spanf1.c:15–53] receives a `sporglset` that may contain multiple items — one per contiguous I-span. The ORGLRANGE key (the link ISA prefixed with spantype) is fixed **before** the loop:

```c
// spanf1.c:22–23
prefixtumbler (isaptr, spantype, &crumorigin.dsas[ORGLRANGE]);
tumblerclear (&crumwidth.dsas[ORGLRANGE]);
```

Then for **each item** in the sporglset the SPANRANGE key is overwritten with that item's stream/width, and a separate `insertnd` is called:

```c
// spanf1.c:25–52
for (; sporglset; sporglset = (typesporglset)((typeitemheader *)sporglset)->next) {
    if (((typeitemheader *)sporglset)->itemid == ISPANID) {
        movetumbler (&((typeispan *)sporglset)->stream, &lstream);
        movetumbler (&((typeispan *)sporglset)->width, &lwidth);
        movetumbler (isaptr, &linfo.homedoc);
    } else if (((typeitemheader *)sporglset)->itemid == SPORGLID) {
        movetumbler (&((typesporgl *)sporglset)->sporglorigin, &lstream);
        movetumbler (&((typesporgl *)sporglset)->sporglwidth, &lwidth);
        movetumbler (&((typesporgl *)sporglset)->sporgladdress, &linfo.homedoc);
    } else if (((typeitemheader *)sporglset)->itemid == TEXTID) { ... }
    movetumbler (&lstream, &crumorigin.dsas[SPANRANGE]);
    movetumbler (&lwidth, &crumwidth.dsas[SPANRANGE]);
    insertnd(taskptr,(typecuc*)spanfptr,&crumorigin,&crumwidth,&linfo,SPANRANGE); // ← one call per I-span
}
```

So for a link whose from-endset covers text inserted in two separate operations (yielding I-spans A and B), `insertspanf` writes two distinct enfilade nodes:

| SPANRANGE key | ORGLRANGE key |
|---|---|
| A.stream / A.width | LINKFROMSPAN . linkISA |
| B.stream / B.width | LINKFROMSPAN . linkISA |

---

### 2. Three separate `insertspanf` calls — one per endset

`insertendsetsinspanf` [do2.c:116–128], called from `docreatelink` [do1.c:219], runs `insertspanf` once per endset:

```c
// do2.c:116–128
bool insertendsetsinspanf(...) {
    if (!(
        insertspanf(taskptr,spanfptr,linkisaptr,fromsporglset,LINKFROMSPAN)
     && insertspanf(taskptr,spanfptr,linkisaptr,tosporglset,LINKTOSPAN)))
        return (FALSE);
    if (threesporglset)
        if (!insertspanf(taskptr,spanfptr,linkisaptr,threesporglset,LINKTHREESPAN))
            return (FALSE);
    return(TRUE);
}
```

If the from-endset has N I-spans and the to-endset has M I-spans, the link contributes N+M (plus optional three-endset spans) entries to the spanfilade — all sharing the same ORGLRANGE key (`spantype . linkISA`) but each with a distinct SPANRANGE key.

---

### 3. Search: iterates each query I-span, unions results

`sporglset2linksetinrange` [sporgl.c:239–269] iterates the **query** sporglset — which also may contain multiple I-spans — calling `retrieverestricted` once per I-span:

```c
// sporgl.c:250–268
for (; sporglset; sporglset = (typesporglset)((typeitemheader *)sporglset)->next) {
    ...
    if (orglrange) {
        prefixtumbler(&orglrange->stream, spantype, &range.stream);
        prefixtumbler(&orglrange->width, 0, &range.width);
        context = retrieverestricted(spanfptr, (typespan*)sporglset, SPANRANGE,
                                     &range, ORGLRANGE, (typeisa*)infoptr);
    } else {
        context = retrieverestricted(spanfptr, (typespan*)sporglset, SPANRANGE,
                                     (typespan*)NULL, ORGLRANGE, (typeisa*)infoptr);
    }
    for (c = context; c; c = c->nextcontext) {
        beheadtumbler(&c->totaloffset.dsas[ORGLRANGE], &linksa);
        onlinklist(taskptr, linksetptr, &linksa);  // accumulate
    }
    contextfree(context);
}
```

The outer loop (`sporglset2linkset` at sporgl.c:234) iterates over the passed `homeset`:

```c
// sporgl.c:226–236 — note the unconditional override
if (TRUE||!homeset) {   // ← "TRUE" means homeset parameter is always ignored
    tumblerclear(&nullhomeset.stream);
    tumblerclear(&nullhomeset.width);
    nullhomeset.width.mantissa[0] = 100;
    nullhomeset.next = NULL;
    homeset = &nullhomeset;
}
for (; homeset; homeset = homeset->next)
    sporglset2linksetinrange(taskptr, spanfptr, sporglset, linksetptr, homeset, spantype);
```

The `if (TRUE||...)` unconditionally replaces the orglrange with a wide synthetic span (stream=0, width=100). After `prefixtumbler`, the ORGLRANGE restriction becomes `[spantype.0, spantype.0+100)` — wide enough to match any link ISA less than 100. This is a hardcoded kluge (the comment in the nearby falsy branch at sporgl.c:251 reads `"trying to kluge links followable thru versions"`). It means the orglrange passed from the FEBE layer is silently ignored at the spanfilade search level.

---

### 4. Deduplication via `onlinklist`

`onlinklist` [spanf2.c:26–44] is intended to deduplicate: if the same link ISA appears in the results of two separate `retrieverestricted` calls (because two I-spans in the query both matched the same link), the second occurrence should be dropped:

```c
// spanf2.c:38–44
for (temp = *linksetptr; nextlink = temp->next; temp = nextlink) {
    if (tumblereq(&temp->address, linkisaptr))
        return(0);  // already in list
}
temp->next = linkset;  // append
```

**Off-by-one bug:** the loop condition is `nextlink = temp->next`, which terminates when `temp` reaches the last element (its `->next` is NULL). The last element's address is never checked. If the ISA of the last-appended link matches the incoming ISA, a duplicate is silently added. In normal operation each `retrieverestricted` returns each matching link once, so duplicates across I-span iterations are the main risk path — and only the tail of the list is unguarded.

---

### 5. Per-endset results are intersected

`findlinksfromtothreesp` [spanf1.c:56–103] calls `sporglset2linkset` for each specified endset, with an early-exit optimization:

```c
// spanf1.c:76–100
if (fromvspecset) {
    sporglset2linkset(..., fromsporglset, &fromlinkset, orglrange, LINKFROMSPAN);
    if (!fromlinkset) { *linksetptr = NULL; return(TRUE); } // short-circuit
}
if (tovspecset) {
    sporglset2linkset(..., tosporglset, &tolinkset, orglrange, LINKTOSPAN);
    if (!tolinkset) { *linksetptr = NULL; return(TRUE); }
}
if (threevspecset) { ... }
intersectlinksets(taskptr, fromlinkset, tolinkset, threelinkset, linksetptr);
```

`intersectlinksets` [spanf2.c:46–120] computes the set intersection with a nested loop: O(N×M) for two sets, O(N×M×P) for three. Only link ISAs appearing in all queried per-endset results survive.

---

### Summary table

| Step | Location | What happens for multi-I-span endset |
|---|---|---|
| Link creation | `insertendsetsinspanf` [do2.c:116] | Calls `insertspanf` once per endset |
| Per-endset indexing | `insertspanf` [spanf1.c:25–52] | Loops: one `insertnd` call per I-span in the sporglset |
| 2D key layout | `insertspanf` [spanf1.c:22,49–50] | ORGLRANGE = `spantype . linkISA` (fixed); SPANRANGE = individual I-span (varies per entry) |
| Search per I-span | `sporglset2linksetinrange` [sporgl.c:250–267] | Loops: one `retrieverestricted` call per query I-span; accumulates results |
| Deduplication | `onlinklist` [spanf2.c:38–43] | Deduplicates link ISAs, but **last element unchecked** → potential tail duplicate |
| orglrange filter | `sporglset2linkset` [sporgl.c:227] | `if (TRUE\|\|...)` unconditionally ignores the passed orglrange; uses width=100 synthetic span |
| Final aggregation | `intersectlinksets` [spanf2.c:95–118] | N-way intersection across the three endset result lists |

**Bottom line:** The spanfilade does store one entry per I-span, not one per endset. The search iterates all query I-spans and unions matching link ISAs before intersection — so multi-I-span endsets are correctly found and aggregated. The `onlinklist` off-by-one is a latent deduplication bug that could produce duplicate entries in the per-endset result list in edge cases, but the final intersection still yields the correct set of matching links as long as duplicates don't suppress a needed entry.
