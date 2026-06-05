## Question 17 [evidence]

> Unlike FOLLOWLINK's silent filtering of unreferenced (DEL5) I-addresses during I→V conversion, does a direct read of the link orgl return the full endset I-spans without filtering against current POOM state?

## KB Synthesis

Yes. The KB describes a clean two-phase split within FOLLOWLINK that answers this directly.

**Phase 1 — direct orgl read (unfiltered):**

`link2sporglset()` extracts I-addresses from the link orgl via `retrieverestricted()` at the requested endset position (0.1, 0.2, or 0.3). The KB is explicit: **"no POOM check occurs at this stage"** [SS-FOLLOWLINK, Finding 0048]. The full endset I-spans are returned as-is from permanent I-space, regardless of whether those I-addresses are currently mapped in any document's POOM.

**Phase 2 — I→V conversion (filtered):**

`linksporglset2specset()` then converts those I-spans to V-addresses by searching the specified `homedoc`'s POOM via `span2spanset()` → `retrieverestricted()`. I-addresses with no current POOM mapping are **silently dropped** — this is the DEL5 filtering described in [INV-ITOV-FILTERING] and [EC-GHOST-LINK].

The filtering you're asking about belongs entirely to phase 2, not to the orgl read itself. [PRE-FOLLOWLINK] confirms: "There is no precondition requiring that endset I-addresses be currently referenced in any POOM. The operation succeeds even when all endset I-addresses are unreferenced, returning an empty result rather than an error." The empty result comes from phase 2 dropping everything, not from phase 1 returning nothing.

So: a direct read of the link orgl returns the complete, unfiltered I-spans. The current POOM state is irrelevant until phase 2 conversion, which is where [INV-ITOV-FILTERING] applies universally across FOLLOWLINK, RETRIEVEENDSETS, and all other I→V conversion paths.

---

## Code Exploration

Now I have everything I need. Let me trace both paths precisely from the source.

---

## Answer

The question rests on a distinction between two internal steps that FOLLOWLINK conflates: (1) reading the raw I-spans from the link orgl, and (2) converting those I-spans to V-spans. The filtering happens only in step 2.

---

### What lives in the link orgl

Each link has its own granfilade node (orgl) in the POOM. When `docreatelink` is called [`do1.c:195–221`], it calls:

```c
insertendsetsinorgl(taskptr, linkisaptr, link, &fromvsa, fromsporglset, &tovsa, tosporglset, &threevsa, threesporglset)
```

which calls `insertpm` [`orglinks.c:75–134`] for each endset. `insertpm` inserts a **2D crum** into the link's orgl, with:
- V dimension = the endset slot address (`fromvsa` = `0.1`, `tovsa` = `0.2`, etc.)
- I dimension = the raw I-origin and I-width from the sporglset
- `linfo.homedoc` = the home document ISA

The orgl stores the raw I-addresses as-written. No filtering occurs at write time.

---

### `link2sporglset` — the "direct orgl read" [`sporgl.c:67–95`]

FOLLOWLINK's first step is `link2sporglset`:

```c
bool link2sporglset(typetask *taskptr, typeisa *linkisa, typesporglset *sporglsetptr, INT whichend, int type)
{
    if (!findorgl(taskptr, granf, linkisa, &orgl, type))
        return (FALSE);
    tumblerincrement(&zero, 0, whichend, &vspan.stream);  // endset slot position
    tumblerincrement(&zero, 0, 1, &vspan.width);
    if (context = retrieverestricted((typecuc*)orgl, &vspan, V, (typespan*)NULL, I, (typeisa*)NULL)) {
        for (c = context; c; c = c->nextcontext) {
            sporglptr = (typesporgl *)taskalloc(...);
            contextintosporgl((type2dcontext*)c, (tumbler*)NULL, sporglptr, I);
            ...
        }
    }
}
```

`retrieverestricted` is called on the **link's own orgl** restricted to V-space (the endset slot), returning the I-dimension. [`sporgl.c:83`]

`contextintosporgl` then packs the result into a sporgl: [`sporgl.c:205–220`]
```c
movetumbler(&context->context2dinfo.homedoc, &sporglptr->sporgladdress); // home doc ISA
movetumbler(&context->totaloffset.dsas[I],   &sporglptr->sporglorigin);  // raw I-origin
movetumbler(&context->contextwid.dsas[I],    &sporglptr->sporglwidth);   // raw I-width
```

**At this point — after `link2sporglset` but before `linksporglset2specset` — the sporglset contains unfiltered raw I-addresses exactly as stored in the orgl.** If an I-address was valid when the link was created but the content has since been deleted (no current V-mapping), it is still present in this intermediate sporglset.

---

### `linksporglset2specset` — where filtering occurs [`sporgl.c:97–176`]

FOLLOWLINK's second step calls `linksporglset2specset`:

```c
bool linksporglset2specset(typetask *taskptr, typeisa *homedoc, typesporglset sporglset, typespecset *specsetptr, int type)
{
    for (; sporglset; sporglset = ...) {
        if (iszerotumbler(&((typesporgl*)sporglset)->sporgladdress)) {
            // Zero homedoc: return raw ISPANID, no conversion
            ((typeitemheader*)specset)->itemid = ISPANID;
            movetumbler(&sporglset->sporglorigin, &((typeispan*)specset)->stream);
            movetumbler(&sporglset->sporglwidth,  &((typeispan*)specset)->width);
        } else {
            linksporglset2vspec(taskptr, homedoc, &sporglset, (typevspec*)specset, type);
        }
    }
}
```

For any sporgl with a non-zero `sporgladdress` (the normal case for all link endsets written with a home document), it calls `linksporglset2vspec` [`sporgl.c:127–137`] → `sporglset2vspanset` [`sporgl.c:141–176`]:

```c
int sporglset2vspanset(typetask *taskptr, typeisa *homedoc, typesporglset *sporglsetptr, typevspanset *vspansetptr, int type)
{
    (void) findorgl(taskptr, granf, homedoc, &orgl, type);  // home doc's POOM
    movetumbler(&sporglptr->sporglorigin, &ispan.stream);
    movetumbler(&sporglptr->sporglwidth,  &ispan.width);
    vspansetptr = ispan2vspanset(taskptr, orgl, &ispan, vspansetptr);  // line 157
    ...
}
```

`ispan2vspanset` [`orglinks.c:389–394`] calls `permute(I→V)` [`orglinks.c:404–422`] → `span2spanset` [`orglinks.c:425–454`] → `retrieverestricted` on the **home document's POOM**:

```c
context = retrieverestricted((typecuc*)orgl, restrictionspanptr, I, (typespan*)NULL, V, (typeisa*)NULL);
for (c = context; c; c = c->nextcontext) {
    context2span(c, restrictionspanptr, I, &foundspan, V);
    nextptr = (typespan*)onitemlist(taskptr, (typeitem*)&foundspan, (typeitemset*)targspansetptr);
}
if (!context) {
    return(targspansetptr);  // no context = no output = silently dropped
}
```

If the I-address has no V-mapping in the current POOM state (content deleted, DEL5), `retrieverestricted` returns NULL context. The I-span produces no V-span and disappears silently.

---

### RETRIEVEENDSETS path [`spanf1.c:190–235`]

RETRIEVEENDSETS does **not** read the link's own orgl. It reads the **spanfilade** instead:

```c
bool retrieveendsetsfromspanf(typetask *taskptr, typespecset specset, typespecset *fromsetptr, ...)
{
    specset2sporglset(taskptr, specset, &sporglset, NOBERTREQUIRED)          // V→I on doc orgl
    && retrievesporglsetinrange(taskptr, sporglset, &fromspace, &fromsporglset)  // query spanfilade
    && linksporglset2specset(taskptr, &((typevspec*)specset)->docisa,
                             fromsporglset, fromsetptr, NOBERTREQUIRED)      // I→V, same filter
    ...
}
```

`retrievesporglsetinrange` [`spanf1.c:237–267`] queries `spanf` (not `granf`) with `retrieverestricted` restricted to the FROM/TO/THREE slot range, returning the raw I-addresses stored there at link-creation time.

Then `linksporglset2specset` applies **identical I→V filtering** via the same `ispan2vspanset` path.

The spanfilade stores the same I-addresses as the link orgl (both were written at link creation time by `docreatelink`), so the raw data before filtering is the same. After filtering, both FOLLOWLINK and RETRIEVEENDSETS silently drop any I-addresses that have no current V-mapping.

---

### Direct answer to the question

| Stage | FOLLOWLINK | RETRIEVEENDSETS |
|---|---|---|
| Source | Link's own orgl (POOM) via `link2sporglset` | Spanfilade via `retrievesporglsetinrange` |
| Intermediate sporglset | **Unfiltered raw I-spans** | **Unfiltered raw I-spans** |
| Output specset | Filtered via `ispan2vspanset` | Filtered via `ispan2vspanset` (same) |

**The link orgl stores the complete, unfiltered endset I-spans** — exactly as written at creation time. `link2sporglset` reads them back as raw I-addresses without filtering. At the sporglset level, after step 1 of FOLLOWLINK, the DEL5 I-addresses are still present.

**But there is no FEBE operation that delivers this unfiltered sporglset to the client.** `dofollowlink` [`do1.c:223–232`] always chains `link2sporglset` directly into `linksporglset2specset`, applying I→V filtering before the result leaves the backend. RETRIEVEENDSETS reads from a different data structure (the spanfilade) but applies the same filter.

The filtering is not about marking I-addresses as invalid — it is structural: `permute(I→V)` calls `retrieverestricted` on the home document's POOM, and if a crum for that I-address no longer exists (because `deletend` was called), no context is returned and the I-address is simply absent from the output. Nothing in the output signals that a filtering took place.
