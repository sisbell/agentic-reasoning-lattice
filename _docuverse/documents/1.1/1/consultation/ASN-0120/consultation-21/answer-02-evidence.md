## Question 2 [evidence]

> When a from or to V-span set passed to CREATELINK resolves to an empty sporgl set (all named positions deleted), does the implementation reject the call or store the link with an empty endset, as the implementation note records for the type slot?

## KB Synthesis

The KB does not explicitly document this case, but the evidence points toward **silent storage with an empty endset**, not rejection. Here is what the KB records, assembled from multiple threads:

---

## What the KB records

### Zero-width spans cause a crash — but this is different

[PRE-ZERO-WIDTH] and [PRE-LINK-CREATE] (Finding 0028) record that passing a **zero-width V-span** to CREATELINK crashes the backend (Bug 0017). But the question concerns a **non-zero-width V-span** whose positions have been deleted from the POOM — a structurally distinct case.

---

### The V→I conversion path silently returns empty on deleted positions

[ST-LINK-CREATE] (Finding 0037) and [SS-FOLLOWLINK] (Finding 0048) both document the conversion chain used at CREATELINK time:

```
V-span → vspanset2ispanset → permute → span2spanset → retrieverestricted
       → one I-span per contiguous I-address region
       → one sporgl per I-span
```

[SS-FOLLOWLINK] records the key behavior of `span2spanset`:

> "If an I-address has no POOM mapping, `retrieverestricted` returns NULL and the I-address is silently dropped — no V-span is added to the result."

[INV-ITOV-FILTERING] generalizes this as a universal invariant: **unreferenced I-addresses are silently excluded from V-address results across all operations.** Critically, this is stated as a property of the conversion layer, not of any specific operation.

If the V-span's positions have been deleted from the POOM, `permute`/`retrieverestricted` in the V→I direction finds no contexts, and `vspanset2sporglset` returns an empty sporgl set.

---

### No documented rejection gate for empty sporgl sets in domakelink

[ST-LINK-CREATE] (Finding 0037) records that `domakelink` (`do1.c:173-197`) proceeds by converting the input V-spans to sporgls, then calling `insertendsetsinspanf`. [SS-SPANF-OPERATIONS] and [SS-DOCISPAN] record that `insertspanf` loops over the sporgl set making one `insertnd` call per item. With an empty sporgl set, it makes zero calls — and the KB records no guard in `domakelink` that checks for emptiness and aborts.

---

### The type endset anomaly is the closest documented analog

The question notes "as the implementation note records for the type slot." [EC-ORPHANED-LINK] (Finding 0024) documents the behavior matrix for orphaned links and the anomaly:

> "`follow_link(link_id, LINK_TYPE)` returns empty even though the type references the bootstrap document, which was not deleted. This is either a bug or an undocumented dependency of type resolution on endpoint resolution."

This occurs when both source and target endpoints are deleted **after** creation. The link orgl still exists; the type endset was stored at creation time. This demonstrates that the system can hold and return links with endsets that resolve to empty — the storage layer does not enforce non-empty endsets as an invariant.

---

## What the KB cannot confirm

The KB does not record a finding that explicitly tests CREATELINK with a from or to V-span that resolves to an empty sporgl set at call time (i.e., content deleted *before* the link is created). The type endset anomaly and orphaned link behaviors all arise from content deleted *after* successful link creation.

---

## Synthesis

Based on [INV-ITOV-FILTERING], [ST-LINK-CREATE], [SS-FOLLOWLINK], and [EC-ORPHANED-LINK]:

The implementation almost certainly **stores the link with an empty endset** rather than rejecting the call. The silent-drop behavior is systemic across the conversion path, no rejection guard is documented in `domakelink`, and the system demonstrably holds links whose endsets resolve to empty (the type slot anomaly). What you would get is a link object with a permanent I-address, a POOM entry at 2.x in the home document, but zero spanfilade entries for that endset — functionally equivalent to an orphaned link from birth.

This is **not fully answerable from the KB** with certainty, because no finding explicitly tests this path. I am synthesizing from adjacent documented behaviors.

---

## Code Exploration

I now have a complete trace through all layers. Here is the full answer.

---

## Answer: CREATELINK With an Empty Resolved Sporgl Set

The implementation **does not reject the call**. It stores the link with an empty endset and returns success. Every function in the chain silently skips the insertion loop when the sporgl set is NULL and returns TRUE. Here is the exact execution path:

---

### 1. Entry: `fns.c` → `docreatelink`

`createlink` [fns.c:100-112] calls `docreatelink` via a short-circuit `&&` chain. If `docreatelink` returns TRUE, `putcreatelink` is called and the client receives the link's ISA. There is no guard between the specset conversion and link storage.

Both the 2-endset variant `domakelink` [do1.c:169-193] and the 3-endset `docreatelink` [do1.c:195-221] follow the identical structure:

```c
return (
     createorglingranf (taskptr, granf, &hint, linkisaptr)    // link node allocated in granfilade
  && tumbler2spanset (...) && findnextlinkvsa (...) && docopy (...)  // V-space set up
  && findorgl (taskptr, granf, linkisaptr, &link, NOBERTREQUIRED)
  && specset2sporglset (taskptr, fromspecset, &fromsporglset, NOBERTREQUIRED)
  && specset2sporglset (taskptr, tospecset,   &tosporglset,   NOBERTREQUIRED)
  && setlinkvsas (&fromvsa, &tovsa, &threevsa)
  && insertendsetsinorgl (...)
  && insertendsetsinspanf (...)
);
```

The link orgl is **created and its V-space is populated before** `specset2sporglset` is ever called. There is no validity check on the resulting sporgl set between conversion and insertion.

---

### 2. V-span → Sporgl Conversion: `specset2sporglset` / `vspanset2sporglset`

`specset2sporglset` [sporgl.c:14-33] iterates over the specset. For each VSPECID element it calls:

```c
sporglsetptr = vspanset2sporglset(taskptr, &((typevspec*)specset)->docisa,
                                  ((typevspec*)specset)->vspanset, sporglsetptr, type);
if (!sporglsetptr) return (FALSE);
```

`vspanset2sporglset` [sporgl.c:35-65] returns NULL **only if `findorgl` fails** (document not found):

```c
if (!findorgl(taskptr, granf, docisa, &orgl, type))
    return (NULL);            // only failure path — document missing
for (; vspanset; vspanset = vspanset->next) {
    (void) vspanset2ispanset(taskptr, orgl, vspanset, &ispanset);
    for (; ispanset; ispanset = ispanset->next) {   // skipped entirely when ispanset == NULL
        sporglset = (typesporgl *) taskalloc(...);
        ...
        *sporglsetptr = (typesporglset)sporglset;
        sporglsetptr = (typesporglset *)&sporglset->next;
    }
}
return (sporglsetptr);        // returns unchanged sporglsetptr — non-NULL
```

When the document exists but all named positions are deleted, `vspanset2ispanset` → `permute` → `span2spanset` [orglinks.c:425-454] gets a NULL context from `retrieverestricted` and takes the early return at [orglinks.c:446-448]:

```c
if(!context){
    return(targspansetptr);   // appends nothing; ispanset stays NULL
}
```

So `ispanset` is NULL, the inner loop body never executes, no sporgl nodes are created, and `vspanset2sporglset` returns `sporglsetptr` unchanged — a non-NULL pointer to the output slot. `specset2sporglset` then sets `*sporglsetptr = NULL` [sporgl.c:30] and returns TRUE. The result is: `fromsporglset = NULL` (an empty, NULL-terminated list), and the function signals success.

---

### 3. POOM Insertion: `insertendsetsinorgl` → `insertpm`

`insertendsetsinorgl` [do2.c:130-149] calls:

```c
insertpm(taskptr, linkisaptr, link, fromvsa, fromsporglset)
```

`insertpm` [orglinks.c:75-134] has exactly one early-FALSE guard — a zero VSA check [orglinks.c:86-91]:

```c
if (iszerotumbler(vsaptr)) return (FALSE);
```

The VSA was set non-zero by `setlinkvsas` [do2.c:169-183] (from-endset VSA = 0.1.1, to-endset = 0.2.1). So this guard passes. Then:

```c
logbertmodified(orglisa, user);           // bert is marked modified regardless
for (; sporglset; sporglset = ...) {      // sporglset == NULL: loop never executes
    unpacksporgl(...);
    insertnd(taskptr, (typecuc*)orgl, ...);   // never called
}
return (TRUE);                            // unconditional success
```

`insertnd` is **never called**. No node is written into the POOM enfilade. The function returns TRUE.

---

### 4. Spanfilade Insertion: `insertendsetsinspanf` → `insertspanf`

`insertendsetsinspanf` [do2.c:116-128] calls:

```c
insertspanf(taskptr, spanfptr, linkisaptr, fromsporglset, LINKFROMSPAN)
```

`insertspanf` [spanf1.c:15-54]:

```c
for (; sporglset; sporglset = (typesporglset)((typeitemheader*)sporglset)->next) {
    // sporglset == NULL: loop never executes
    insertnd(taskptr, (typecuc*)spanfptr, &crumorigin, &crumwidth, &linfo, SPANRANGE);
}
return (TRUE);    // spanf1.c:53 — unconditional
```

Again `insertnd` is never called. No reverse-lookup entry is written into the spanfilade. Returns TRUE.

---

### Summary: What the Implementation Does

| Step | Outcome when V-span resolves to empty |
|------|--------------------------------------|
| `findorgl` on *document* | Succeeds (document exists) |
| `vspanset2ispanset` | Returns NULL ispan (no context from retrieval) |
| `specset2sporglset` | Returns TRUE; sporglset = NULL |
| `insertpm` (POOM) | Loop skipped; returns TRUE; no `insertnd` called |
| `insertspanf` (spanfilade) | Loop skipped; returns TRUE; no `insertnd` called |
| `docreatelink` overall | Returns TRUE |
| Client response | `putcreatelink` sends the new link ISA |

**The call succeeds.** The link node is fully allocated in the granfilade and has its document V-space established via `docopy`. But for the empty endpoint, no entries exist in the POOM enfilade (so link following via that endset retrieves nothing) and no entries exist in the spanfilade (so `FIND` queries that filter by that endset's content see nothing). The link is stored with an empty endset exactly as the implementation note records for the type slot — not rejected, not errored, silently stored.

The only scenario that causes rejection is if the **document itself is not found** by `findorgl` [sporgl.c:44-46], which makes `vspanset2sporglset` return NULL → `specset2sporglset` return FALSE → `docreatelink` chain fail → `putrequestfailed` to client. A document that exists but has had all its content deleted at the named positions is a different case: the document is found, V↔I permutation produces no entries, and the chain proceeds silently to success.
