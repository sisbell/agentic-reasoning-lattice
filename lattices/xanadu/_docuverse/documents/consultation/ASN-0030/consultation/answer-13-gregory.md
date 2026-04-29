## Question 13 [gregory]

> After DELETE removes a V→I mapping from a document's POOM, does `retrieveendsets` on a link referencing those I-addresses still return the full I-address spans, or does the spanfilade lookup itself degrade when no POOM references the I-addresses?

## KB Synthesis

The answer requires tracing two separate phases of `retrieveendsets`: the spanfilade lookup and the I→V conversion.

## Phase 1: Spanfilade lookup — does NOT degrade

The spanfilade is write-only [INV-SPANF-WRITE-ONLY]. DELETE removes V→I mappings from the POOM but **never touches the spanfilade** [ST-DELETE, Finding 0057]:

> `dodeletevspan` calls only `deletevspanpm` (granf) and `logbertmodified` — there is no call to any spanf function.

The link's endpoint I-addresses remain indexed in the spanfilade exactly as they were at link creation. `RETRIEVEENDSETS` searches the spanfilade via `retrievesporglsetinrange()` with SPANRANGE/ORGLRANGE restrictions [SS-RETRIEVE-ENDSETS], and this search succeeds — the spanfilade finds the matching I-address entries and returns them as a sporglset.

This is the INT-DELETE-SPANF-DIVERGENCE state: the index claims the document contains those I-addresses even though the POOM no longer maps them.

## Phase 2: I→V conversion — degrades silently

After the spanfilade returns the link's endpoint I-addresses as sporgls, `RETRIEVEENDSETS` calls `linksporglset2specset()` to convert back to V-addresses [SS-RETRIEVE-ENDSETS]. This path is:

```
linksporglset2specset → sporglset2vspanset → ispan2vspanset → permute → span2spanset → retrieverestricted
```

At `span2spanset()`, `retrieverestricted()` searches the **querying document's POOM** for the I-address. Since DELETE removed those I-address mappings from the POOM, `retrieverestricted()` returns NULL — and per [INV-ITOV-FILTERING]:

> unreferenced I-addresses are silently excluded from V-address results with no error

Each unresolvable I-address is dropped. The final result is empty or partial depending on how many of the link's endpoint I-addresses still have POOM mappings.

## Summary

| Layer | State after DELETE | Effect on RETRIEVEENDSETS |
|---|---|---|
| Spanfilade | Unchanged (I-addrs still indexed) | Lookup succeeds, returns sporglset |
| POOM | I→V mapping removed | I→V conversion silently drops unreferenced I-addrs |
| Result | — | Empty or partial V-span result; operation still returns success |

This is the same mechanism documented for FOLLOWLINK in [EC-GHOST-LINK]: the link structure is intact in permanent storage, the spanfilade search finds it, but endpoint resolution through the POOM produces empty spans. The distinction between "spanfilade found it" and "POOM resolved it" is what makes these "ghost links" — permanently existent and discoverable in the index, but resolving to nothing in V-space.

---

## Code Exploration

I have everything needed. Here is the complete answer.

---

## Answer

**Short answer:** The spanfilade lookup itself does not degrade. The degradation occurs one step later, in `linksporglset2specset`, which always attempts to convert the stored I-addresses back to V-spans via the POOM. When the POOM has no V-mappings for those I-addresses, the result is a `VSPECID` specset with a NULL `vspanset` — an empty version-space result. The raw I-address spans are not surfaced to the caller.

---

### The Call Chain

`retrieveendsets` [fns.c:350] → `doretrieveendsets` [do1.c:369] → `retrieveendsetsfromspanf` [spanf1.c:190].

Inside `retrieveendsetsfromspanf`, three sequential operations matter:

```c
specset2sporglset (taskptr, specset, &sporglset, NOBERTREQUIRED)
&& retrievesporglsetinrange(taskptr, sporglset, &fromspace, &fromsporglset)
&& linksporglset2specset (taskptr, &((typevspec *)specset)->docisa, fromsporglset, fromsetptr, NOBERTREQUIRED)
```
[spanf1.c:222–224]

---

### Step 1 — `specset2sporglset` [sporgl.c:14]

Converts the input specset (which identifies the link document) into a sporglset.

```c
if (((typeitemheader *)specset)->itemid == ISPANID) {
    *sporglsetptr = (typesporglset)specset;            // raw I-span: pass-through, no POOM
} else if (((typeitemheader *)specset)->itemid == VSPECID) {
    sporglsetptr = vspanset2sporglset(taskptr, &docisa, vspanset, sporglsetptr, type);
    // ↑ calls findorgl → vspanset2ispanset → POOM V→I lookup
}
```
[sporgl.c:20–28]

If the link is specified by I-address directly, the POOM is not touched here.

---

### Step 2 — `retrievesporglsetinrange` [spanf1.c:237]

Queries the **spanfilade** (not the granfilade/POOM) for the link's endpoint sporgls:

```c
context = retrieverestricted((typecuc*)spanf,
    (typespan*)sporglptr, SPANRANGE,
    whichspace, ORGLRANGE,
    (typeisa*)NULL /*kluge to make links show thru to versions*/);
```
[spanf1.c:245]

This is a pure spanfilade query. It searches for crums that match the link's I-address in `SPANRANGE` and `LINKFROMSPAN`/`LINKTOSPAN`/`LINKTHREESPAN` in `ORGLRANGE`. **The POOM is not consulted here.** The spanfilade itself is unchanged by `dodeletevspan` — it still holds the link's endpoint I-address data. This step succeeds.

---

### Step 3 — `linksporglset2specset` [sporgl.c:97] — where the degradation occurs

```c
if (iszerotumbler(&((typesporgl *)sporglset)->sporgladdress)) {
    // sporgladdress == 0: return raw I-span (ISPANID)
    ((typeitemheader *)specset)->itemid = ISPANID;
    movetumbler(&sporglset->sporglorigin, &((typeispan *)specset)->stream);
    movetumbler(&sporglset->sporglwidth,  &((typeispan *)specset)->width);
} else {
    // sporgladdress != 0: convert I→V through the POOM
    linksporglset2vspec(taskptr, homedoc, &sporglset, (typevspec*)specset, type);
}
```
[sporgl.c:105–117]

`sporgladdress` is set from `context->context2dinfo.homedoc` via `contextintosporgl` [sporgl.c:209], which gets its value from `linfo.homedoc` set during `insertspanf`. For document-referencing link endpoints, this is always the document ISA — non-zero. So the `else` branch is always taken for normal links, driving a POOM lookup.

---

### The POOM I→V Lookup After Deletion

`linksporglset2vspec` [sporgl.c:127] calls `sporglset2vspanset` [sporgl.c:141], which calls:

```c
vspansetptr = ispan2vspanset(taskptr, orgl, &ispan, vspansetptr);
```
[sporgl.c:157]

`ispan2vspanset` [orglinks.c:389] calls `permute(taskptr, orgl, ispanptr, I, vspansetptr, V)` [orglinks.c:404], which calls `span2spanset` [orglinks.c:425]:

```c
context = retrieverestricted((typecuc*)orgl, restrictionspanptr, restrictionindex, (typespan*)NULL, targindex, (typeisa*)NULL);
for (c = context; c; c = c->nextcontext) {
    context2span(c, ...);
    nextptr = (typespan *)onitemlist(taskptr, ...);
}
if (!context) {
    return(targspansetptr);   // ← no V-spans appended; return unchanged
}
```
[orglinks.c:435–448]

**After `dodeletevspan`**, `deletevspanpm` called `deletend((typecuc*)docorgl, &vspanptr->stream, &vspanptr->width, V)` [orglinks.c:149]. This removed the POOM crums at those V-positions. Since the crums are the shared 2D records encoding V↔I, their removal means those I-addresses no longer appear in any POOM traversal. `retrieverestricted` returns NULL context. `span2spanset` returns `targspansetptr` unmodified. `permute` returns `save` — the original, still-empty `vspansetptr`. Back in `linksporglset2vspec`:

```c
specptr->vspanset = NULL;
sporglset2vspanset(taskptr, homedoc, sporglsetptr, &specptr->vspanset, type);
// vspanset remains NULL
```
[sporgl.c:135–136]

---

### Conclusion

| Stage | What happens | POOM involved? |
|---|---|---|
| `retrievesporglsetinrange` [spanf1.c:237] | Spanfilade query succeeds; I-addresses of link endpoints retrieved correctly | No |
| `linksporglset2specset` [sporgl.c:97] | Branches on non-zero `sporgladdress` → calls POOM I→V lookup | **Yes** |
| `span2spanset` [orglinks.c:425] | `retrieverestricted` on POOM returns NULL (crums deleted); no V-spans appended | **Yes, fails silently** |

**The spanfilade does not degrade.** It correctly stores and returns the I-addresses of link endpoints regardless of POOM state. The degradation is entirely in the back-conversion: `linksporglset2specset` always attempts to resolve I-addresses to V-spans via the POOM, and when `deletend(V)` has removed the relevant crums, `span2spanset` silently returns no spans [orglinks.c:446-448]. The caller receives a `VSPECID` specset with `vspanset = NULL` — an empty version-space result — with a `TRUE` return code and no error. The raw I-address spans are never surfaced.
