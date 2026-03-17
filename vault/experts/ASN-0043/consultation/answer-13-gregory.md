## Question 13 [gregory]

> What are the cardinality constraints on an individual endset — can an endset contain zero spans, exactly one span, or an unbounded number of spans, and does this differ between source, target, and type?

## KB Synthesis

## Endset Cardinality

Endsets have variable cardinality at all three endpoints, with distinct mechanisms driving each bound.

---

### Zero spans — when and why

An endset returns zero spans when its stored I-addresses have no POOM mapping in the queried document. The filtering is silent: `linksporglset2specset` → `span2spanset` → `retrieverestricted` drops any I-address that returns NULL from the POOM lookup, with no error [SS-FOLLOWLINK, Finding 0048].

This occurs in two scenarios:

1. **Content deleted**: All content at the endpoint has been removed from the document. [EC-GHOST-LINK] documents this as a "ghost link" — the link orgl is intact and FOLLOWLINK succeeds, but the result is `[]`.

2. **Querying from the wrong document**: FOLLOWLINK resolves I-addresses through a caller-specified `homedoc`. If that document's POOM has no mappings for the endset I-addresses, the result is empty [SS-FOLLOWLINK, Finding 0048].

The [EC-ORPHANED-LINK] behavior matrix (Finding 0024) shows the full picture:
- Source deleted → source endset = `[]`
- Target deleted → target endset = `[]`
- Both deleted → type endset also becomes `[]` (anomalous — see below)

---

### One span — the normal case

At creation time, endpoints require width >= 1; zero-width crashes [PRE-ZERO-WIDTH, Finding 0028]. Content inserted from a single, contiguous source maps to a single contiguous I-span, producing one sporgl and thus one V-span in the endset.

---

### Multiple spans — causes

The endset structure is `set<Sporgl>` where `|Endset| >= |input_vspans|` [SS-LINK-ENDPOINT, Finding 0037]. Three distinct mechanisms produce multiple spans:

**1. Multi-source transclusion at link creation** [ST-LINK-CREATE, Finding 0037]: If the V-span used to define the endpoint covers content from multiple source documents, `vspanset2sporglset` splits it into one sporgl per contiguous I-address region. Example: document C contains "AA" (I-addresses from doc A) and "BB" (I-addresses from doc B); creating a link on "AABB" produces 2 sporgls despite 1 input V-span.

**2. Rearrangement/pivot fragmentation** [EC-PIVOT-LINK-FRAGMENTATION, Finding 0019]: After a pivot on linked content, the endset can fragment — a 2-character link can produce 4 spans, and `find_links` may return the link twice.

**3. Multi-span link creation** [EC-MULTISPAN-LINK-DUPLICATION, Finding 0019]: Creating a link with multiple source spans (e.g., "First" and "second") produces more spans than provided at creation — 3 spans observed from 2 input spans, with duplication.

---

### Differences between source, target, and type

**Source and target** endsets follow the same rules: zero to unbounded, determined by I-address resolvability and content I-address contiguity.

**Type** endsets behave differently:
- Normally return **exactly one span**, pointing to a specific address in the bootstrap document's type registry at `1.0.2.x` [SS-LINK-ENDPOINT, Finding 0024]. The type subspace uses tumbler containment to encode hierarchy (`1.0.2.6.2` is a subtype of `1.0.2.6`).
- The bootstrap document is not deleted by user operations, so the type endset should always resolve.
- **Exception**: When both source and target endpoints are deleted, the type endset also returns empty — "either a bug or an undocumented dependency of type resolution on endpoint resolution" [EC-ORPHANED-LINK, Finding 0024]. This is anomalous since the type references the permanently available bootstrap document.

---

### Summary

| Endpoint | Zero? | One? | Many? |
|----------|-------|------|-------|
| Source | Yes — when endpoint I-addresses unresolvable | Yes — normal | Yes — multi-source transclusion, rearrangement, multi-span creation |
| Target | Yes — same mechanism | Yes — normal | Yes — same mechanisms |
| Type | Yes — anomalously, when both source+target also empty | Yes — normal case | Not documented |

---

## Code Exploration

Now I have everything I need for a complete, cited answer.

---

## Endset Cardinality in udanax-green

### Data Model

An endset is represented as a `typesporglset` — a NULL-terminated singly-linked list of `typesporgl` items [xanadu.h:115-127]:

```c
typedef struct structsporgl {
    struct structsporgl *next;       // linked list chain
    typeitemid  itemid;
    tumbler sporglorigin;
    tumbler sporglwidth;
    typeisa sporgladdress;
} typesporgl;

typedef typesporglitem * typesporglset;  // xanadu.h:127
```

There is no `count` field and no min/max constraint on the list. Cardinality is determined purely by how many nodes are chained through `next`.

---

### Zero Spans

**Write side — allowed silently.** Both insertion functions use a simple `for (; sporglset; ...)` loop that does nothing if the pointer is NULL:

`insertspanf` [spanf1.c:25-53]:
```c
for (; sporglset; sporglset = (typesporglset)((typeitemheader *)sporglset)->next) {
    ...
}
return (TRUE);  // always returns TRUE
```

`insertpm` [orglinks.c:99-133]:
```c
logbertmodified(orglisa, user);  // always called
for (; sporglset; sporglset = (typesporglset) sporglset->xxxxsporgl.next) {
    ...
}
return (TRUE);
```

If `sporglset` is NULL, nothing is inserted into the spanfilade or POOM, but the function returns TRUE. Even `logbertmodified` fires on an empty endset, marking the link as modified.

**Read side — followlink returns FALSE.** `link2sporglset` [sporgl.c:83-94] uses an `if (context = retrieverestricted(...))` idiom — if the enfilade has no crums in the queried region (because nothing was ever inserted), `context` is NULL, the if-block is skipped, and the function returns FALSE:

```c
if (context = retrieverestricted((typecuc*)orgl, &vspan, V, (typespan*)NULL, I, (typeisa*)NULL)) {
    for (c = context; c; c = c->nextcontext) { ... }
    return (TRUE);
} else {
    return (FALSE);  // no spans → FALSE
}
```

Since `dofollowlink` [do1.c:228-231] short-circuits on FALSE:
```c
return (
    link2sporglset(taskptr, linkisaptr, &sporglset, whichend, NOBERTREQUIRED)
    && linksporglset2specset(...));
```
…a zero-span endset causes `followlink` to fail.

**Conclusion for zero:** A zero-span endset is *structurally writable* but yields a followlink failure. There is no creation-time rejection guard.

---

### Exactly One Span

The common and fully-supported case. One entry in the sporglset linked list is inserted once and retrieved once. No special handling required.

---

### Unbounded Multiple Spans

All code paths are list-iterating loops with no upper bound.

**Conversion** from vspansets to sporglsets in `vspanset2sporglset` [sporgl.c:47-64] is a double loop — one iteration per vspan, one per resulting ispan — producing one sporgl per ispan with no limit:

```c
for (; vspanset; vspanset = vspanset->next) {
    (void) vspanset2ispanset(taskptr, orgl, vspanset, &ispanset);
    for (; ispanset; ispanset = ispanset->next) {
        sporglset = (typesporgl *) taskalloc(taskptr, sizeof(typesporgl));
        ...
        *sporglsetptr = (typesporglset)sporglset;
        sporglsetptr = (typesporglset *)&sporglset->next;
    }
}
```

**Insertion** via `insertspanf` [spanf1.c:25-52] calls `insertnd` once per sporgl, appending a crum to the spanfilade for each span — unbounded.

**Retrieval** via `link2sporglset` [sporgl.c:84-89] allocates one `typesporgl` per context item returned by `retrieverestricted`, and chains them:

```c
for (c = context; c; c = c->nextcontext) {
    sporglptr = (typesporgl *)taskalloc(taskptr, sizeof(typesporgl));
    contextintosporgl((type2dcontext*)c, (tumbler*)NULL, sporglptr, I);
    *sporglsetptr = (typesporglset)sporglptr;
    sporglsetptr = (typesporglset *)&sporglptr->next;
}
```

And `linksporglset2specset` [sporgl.c:103-121] similarly iterates all sporgls to produce the returned specset. No cap anywhere.

**Conclusion for multiple:** Unbounded. The entire architecture is linked-list traversal at every stage.

---

### Source vs. Target vs. Type

The three endsets are distinguished by constants defined in [xanadu.h:36-38]:

```c
#define LINKFROMSPAN    1   // source
#define LINKTOSPAN      2   // target
#define LINKTHREESPAN   3   // type
```

These are used only as V-subspace prefixes in `setlinkvsas` [do2.c:169-182] and as spantype arguments to `insertspanf`. They determine *where* in the spanfilade each endset's spans are stored, not *how many* spans they may contain.

**Structural symmetry at insertion:** `insertendsetsinspanf` [do2.c:116-128] and `insertendsetsinorgl` [do2.c:130-148] call the same functions for all three:

```c
// insertendsetsinspanf:
insertspanf(taskptr, spanfptr, linkisaptr, fromsporglset, LINKFROMSPAN)
insertspanf(taskptr, spanfptr, linkisaptr, tosporglset,   LINKTOSPAN)
if (threesporglset)
    insertspanf(taskptr, spanfptr, linkisaptr, threesporglset, LINKTHREESPAN)

// insertendsetsinorgl:
insertpm(taskptr, linkisaptr, link, fromvsa, fromsporglset)
insertpm(taskptr, linkisaptr, link, tovsa,   tosporglset)
if (threevsa && threesporglset)
    insertpm(taskptr, linkisaptr, link, threevsa, threesporglset)
```

**The only asymmetry:** The type endset (`LINKTHREESPAN`) is guarded by a null check in both insertion functions. Source and target are called unconditionally. This means:
- Source and target endsets are **required** (with NULL/empty sporglset silently creating empty endsets as described above)
- Type endset is **optional** — if `NULL` is passed, it is simply skipped

**At retrieval:** `dofollowlink` [do1.c:223-232] uses `whichend` (1=from, 2=to, 3=type) to pass to `link2sporglset`, which translates it directly into the V-range query. The retrieval logic is identical for all three endset types.

---

### Summary Table

| Property | Source | Target | Type |
|---|---|---|---|
| Zero spans storable | Yes (silent) | Yes (silent) | Yes (silent) |
| Zero spans followable | No (returns FALSE) | No (returns FALSE) | No (returns FALSE) |
| One span | Yes | Yes | Yes |
| N spans (unbounded) | Yes | Yes | Yes |
| Optional at creation | No | No | **Yes** |
| Span-handling code | `insertspanf` / `insertpm` | same | same |
| Wire discriminator | `LINKFROMSPAN = 1` | `LINKTOSPAN = 2` | `LINKTHREESPAN = 3` |

The only cardinality difference between endset types is that the type endset is *optionally present* at the link level, while source and target are always structurally instantiated. Once present, all three endsets are subject to identical constraints: zero-to-unbounded spans, with zero being silent-but-unfollowable and N being architecturally unlimited.
