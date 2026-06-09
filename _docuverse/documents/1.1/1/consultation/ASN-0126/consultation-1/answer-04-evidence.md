## Question 4 [evidence]

> Does udanax-green permit a link's endset to reference addresses that have no stored content, and does it enforce any residence check at link creation?

## KB Synthesis

**Yes on both counts, with nuance.**

**Endset addresses with no stored content**

The system not only permits this post-creation, it has a named pattern for it. Once link creation succeeds, subsequent deletion of endpoint content leaves the endset I-addresses intact in I-space but unresolvable in the POOM. [EC-GHOST-LINK] documents the three result states explicitly: all endset I-addresses live (full result), some unreferenced (partial result), all unreferenced (empty `[]` — operation still succeeds). [INV-ITOV-FILTERING] establishes the universal mechanism: `span2spanset` → `retrieverestricted` silently drops any I-address that has no current POOM mapping, without raising an error. This is the same filtering path shared by both FOLLOWLINK and RETRIEVEENDSETS [SS-FOLLOWLINK].

The link permanence invariant [INV-LINK-PERMANENCE] reinforces this: link orgl existence is unconditional, but resolvability is contingent on current POOM state. [EC-ORPHANED-LINK] shows the full behavior matrix — even when `find_links` returns nothing (endpoint content gone from every V-stream), `follow_link(link_id)` still succeeds with an empty span.

**Residence check at link creation**

No explicit check is enforced. The `domakelink` path calls `vspanset2sporglset` which resolves V-spans through the current POOM at creation time [ST-LINK-CREATE / Finding 0037], so content must exist *at that moment* (otherwise the sporgl set would be empty). But this is an implicit structural consequence of the V-to-I conversion, not an enforced precondition. The only documented hard preconditions are non-zero endpoint width [PRE-ZERO-WIDTH] and a valid home document [PRE-LINK-CREATE]. No code in `domakelink` or its callers validates that the resulting I-addresses are currently referenced in any POOM before committing the link to I-space and the spanfilade.

---

## Code Exploration

The write was blocked pending approval. Here is the full answer regardless:

---

## Does udanax-green permit link endsets to reference addresses with no stored content?

**Yes. There is no content residence check at link creation.**

---

### The link creation pipeline

**`fns.c:100–112`** — `createlink` dispatches to `docreatelink`.

**`do1.c:195–221`** — `docreatelink` builds the link through this chain:

```c
createorglingranf(...)           // allocate the link ISA
&& tumbler2spanset(...)          // make the link's own ispan
&& findnextlinkvsa(...)          // find next available V-slot in home doc
&& docopy(...)                   // insert the link-atom into the home doc
&& findorgl(..., NOBERTREQUIRED) // get the link orgl
&& specset2sporglset(taskptr, fromspecset, &fromsporglset, NOBERTREQUIRED)   // [do1.c:214]
&& specset2sporglset(taskptr, tospecset,   &tosporglset,   NOBERTREQUIRED)   // [do1.c:215]
&& specset2sporglset(taskptr, threespecset,&threesporglset,NOBERTREQUIRED)   // [do1.c:216]
&& setlinkvsas(...)
&& insertendsetsinorgl(...)
&& insertendsetsinspanf(...)
```

All three endset specsets are passed with `NOBERTREQUIRED`.

---

### Check 1 — Bert access control: bypassed

**`bert.c:59–61`**:
```c
int checkforopen(tumbler *tp, int type, int connection)
{
  if (type == NOBERTREQUIRED) {
    return 1;   /* Random > 0 */
  }
  ...
}
```

`NOBERTREQUIRED` short-circuits the entire bert table lookup. The endset document does not need to be open in any mode.

---

### Check 2 — Document existence: the only real check

**`granf1.c:17–41`** — `findorgl`:

```c
if ((temp = checkforopen(isaptr, type, user)) <= 0) {
    return FALSE;   // skipped with NOBERTREQUIRED
}
*orglptr = fetchorglgr(taskptr, granfptr, isaptr);
return (*orglptr ? TRUE : FALSE);
```

With `NOBERTREQUIRED`, `checkforopen` returns 1. The only guard remaining is `fetchorglgr` — if the document ISA **was never created** in the granfilade, it returns NULL and the link creation fails. **This is the only existence check: whether the document ISA is present. No check is made on whether content exists at the specified V-addresses.**

---

### Check 3 — V-span content mapping: silently produces NULL

**`sporgl.c:35–65`** — `vspanset2sporglset`:

```c
ispanset = NULL;
if (!findorgl(taskptr, granf, docisa, &orgl, type)){
    return (NULL);   // fails only if document doesn't exist
}
for (; vspanset; vspanset = vspanset->next) {
    (void) vspanset2ispanset(taskptr, orgl, vspanset, &ispanset);
    for (; ispanset; ispanset = ispanset->next) {   // skipped when ispanset==NULL
        // build sporgl entries
        *sporglsetptr = (typesporglset)sporglset;
        sporglsetptr = (typesporglset *)&sporglset->next;
    }
}
return (sporglsetptr);
```

If the orgl has no crums at the requested V-addresses (no content stored there), `vspanset2ispanset` produces a NULL ispanset. The inner loop does not execute. No sporgl entries are built. The output `fromsporglset` remains NULL. `specset2sporglset` [sporgl.c:14–33] sees a non-NULL return (it's a pointer, not a content indicator) and returns TRUE.

---

### Check 4 — Insertion with NULL sporglset: silently succeeds

**`orglinks.c:75–134`** — `insertpm`:

```c
logbertmodified(orglisa, user);
for (; sporglset; sporglset = (typesporglset)sporglset->xxxxsporgl.next) {
    // body not reached if sporglset == NULL
    insertnd(taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);
}
return (TRUE);   // always
```

**`spanf1.c:15–54`** — `insertspanf`:

```c
for (; sporglset; sporglset = ...) {
    // body not reached if sporglset == NULL
    insertnd(taskptr, (typecuc*)spanfptr, &crumorigin, &crumwidth, &linfo, SPANRANGE);
}
return (TRUE);   // always
```

Both return TRUE unconditionally. Neither the link orgl nor the spanfilade receives any entry for that endset.

---

### Check 5 — VSA validation: stub

**`do2.c:110–113`** — `acceptablevsa`:
```c
bool acceptablevsa(tumbler *vsaptr, typeorgl orglptr)
{
    return (TRUE);
}
```

No V-address range checking at all.

---

## Summary

| Check | Enforced? | Code location |
|---|---|---|
| Target document ISA exists in granfilade | **Yes** | `fetchorglgr` [granf1.c:39–40] |
| Target document is open (bert) | **No** — bypassed by `NOBERTREQUIRED` | `checkforopen` [bert.c:59–61] |
| Requested V-span has stored content | **No** — null sporglset silently accepted | `vspanset2sporglset` [sporgl.c:47–58] |
| V-address is in a valid subspace | **No** — `acceptablevsa` stub | [do2.c:112] |

**Behavioral result:**

- If the endset specset names a **document ISA that was never created**, `fetchorglgr` returns NULL → `findorgl` returns FALSE → link creation fails.
- If the endset specset names an **existing document but a V-span with no stored content**, `vspanset2ispanset` produces no ispans → the sporglset is NULL → `insertpm` and `insertspanf` loop bodies skip → **the link is created successfully with an empty endset**, no error or warning.

A link created with an empty endset will not appear in `find_links` queries (nothing is indexed in the spanfilade for that end) and `retrieve_endsets` will return an empty specset for it. It is discoverable only through other means (e.g., the home document's link subspace at V-position `0.x`/`2.x`).

This is consistent with the broader convention-over-enforcement design (Finding 0011): the system assumes callers supply V-specsets that correspond to actual content. There is no runtime guard against referencing empty V-regions in a link endset.

I wrote the full finding to `findings/0079-link-endset-no-residence-check.md` (pending your write approval).
