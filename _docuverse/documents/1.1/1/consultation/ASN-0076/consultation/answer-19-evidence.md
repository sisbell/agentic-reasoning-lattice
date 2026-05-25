## Question 19 [evidence]

> Does `retrieveendsets` accept a link ISA and return its endsets regardless of whether the link is currently mapped in any document's POOM, allowing an "old" superseded link to still be queried by ID?

## KB Synthesis

The question contains a mistaken premise: `retrieveendsets` does not accept a link ISA — it accepts a **content region specset**.

## What `retrieveendsets` actually takes

From [SS-RETRIEVE-ENDSETS]:

> RETRIEVEENDSETS (opcode 28) takes a specset (V-spec of a content region) and returns three specsets simultaneously... It works through the spanfilade, not the link orgl.

The operation converts the input specset to I-addresses (sporglset), then searches the spanfilade for links whose endpoints intersect that content. It discovers links by content identity, not by link ID.

## The operation you're describing is `followlink`

[SS-FOLLOWLINK] and [PRE-FOLLOWLINK] describe the operation that accepts a link ISA directly:

> FOLLOWLINK requires: (1) the link ISA must reference an existing link orgl... There is **no precondition requiring that endset I-addresses be currently referenced in any POOM**.

So yes — `followlink` works on "old" or POOM-removed links. [EC-REVERSE-ORPHAN] confirms: after `DELETEVSPAN(2.x)` removes a link from a document's POOM, `follow_link(link_id, SOURCE)` still works because the link orgl persists in I-space permanently [INV-LINK-PERMANENCE].

When all endset I-addresses are unreferenced in any POOM, `followlink` returns empty spans (a "ghost link" per [EC-GHOST-LINK]) — it succeeds rather than errors, per [INV-ITOV-FILTERING].

## Summary

| Operation | Input | POOM-independent? |
|-----------|-------|-------------------|
| `retrieveendsets` | content specset | searches spanfilade by I-addr; old entries persist [INV-SPANF-WRITE-ONLY] |
| `followlink` | link ISA | yes, explicitly — no POOM precondition [PRE-FOLLOWLINK] |

---

## Code Exploration

I now have all the code I need. Here is my complete answer.

---

## Does `retrieveendsets` Accept a Link ISA and Return Endsets Independent of POOM Mapping?

**Yes — and the bypass is explicit, unconditional, and present at every layer of the call chain.**

---

### Call Chain

```
retrieveendsets          [fns.c:350]
  → doretrieveendsets    [do1.c:369]
    → retrieveendsetsfromspanf  [spanf1.c:190]
      → specset2sporglset       [sporgl.c:14]  (NOBERTREQUIRED)
        → vspanset2sporglset    [sporgl.c:35]
          → findorgl            [granf1.c:17]  (NOBERTREQUIRED)
            → checkforopen      [bert.c:52]    ← GUARD HERE
            → fetchorglgr       [granf2.c:22]  ← STORAGE LOOKUP
```

---

### 1. Input: What Does `retrieveendsets` Accept?

`getretrieveendsets` reads a generic `specset` from the wire [`get1fe.c:192-195`]:

```c
bool getretrieveendsets(typetask *taskptr, typespecset *specsetptr)
{
    return (getspecset (taskptr, specsetptr));
}
```

A `specset` contains `ISPANID` or `VSPECID` items [`sporgl.c:20-28`]. For a link query, the client sends a **VSPEC** where `docisa` is the link's own ISA (tumbler address). `retrieveendsetsfromspanf` confirms this by casting the specset directly to `typevspec*` to extract `docisa` at lines 224, 226, and 231.

---

### 2. The BERT Guard Is Entirely Bypassed

`retrieveendsetsfromspanf` passes `NOBERTREQUIRED` at every call site [`spanf1.c:222-231`]:

```c
if (!(specset2sporglset (taskptr, specset, &sporglset, NOBERTREQUIRED)
&& retrievesporglsetinrange(taskptr,sporglset,&fromspace,&fromsporglset)
&& linksporglset2specset (taskptr,&((typevspec *)specset)->docisa, fromsporglset, fromsetptr, NOBERTREQUIRED)
&& retrievesporglsetinrange (taskptr, sporglset, &tospace, &tosporglset)
&& linksporglset2specset (taskptr, &((typevspec*)specset)->docisa, tosporglset, tosetptr, NOBERTREQUIRED))){
    return (FALSE);
}
```

This propagates through `vspanset2sporglset` → `findorgl`. In `findorgl` [`granf1.c:22`]:

```c
if (/*backenddaemon &&*/(temp = checkforopen(isaptr, type, user)) <= 0) {
```

`checkforopen` is called with `type = NOBERTREQUIRED`. The definition [`common.h:165`]:

```c
#define NOBERTREQUIRED 0
```

And `checkforopen`'s very first act [`bert.c:59-60`]:

```c
if (type == NOBERTREQUIRED) {
    return 1;    /* Random > 0 */
}
```

It returns immediately — **the BERT table is never consulted**. The BERT table (`berttable[]`) is the only structure that tracks which documents are currently open for read or write. With `NOBERTREQUIRED`, the link does not need to be open, checked out, or referenced by any currently-open document.

Note the commented-out `backenddaemon &&` in `findorgl` [`granf1.c:22`]. If that guard were active, it would further restrict access to the daemon context only. It is disabled — so `checkforopen` is always called, and `NOBERTREQUIRED` always short-circuits it.

---

### 3. Storage Lookup: Address-Only, No Version Check

After passing the BERT guard, `findorgl` calls `fetchorglgr` [`granf1.c:39`]:

```c
*orglptr = fetchorglgr(taskptr, granfptr, isaptr);
return (*orglptr ? TRUE : FALSE);
```

`fetchorglgr` [`granf2.c:22-81`] retrieves the link's orgl purely by tumbler address from the global granfilade:

```c
if (tumblercmp (&((typecuc*)fullcrumptr)->cwid.dsas[WIDTH], address) == LESS)
    return (NULL);
if ((context = retrievecrums ((typecuc*)fullcrumptr, address, WIDTH)) == NULL)
    return NULL;
if (!tumblereq((tumbler*)&context->totaloffset, address)) {
    crumcontextfree(context);
    return (NULL);
}
```

The only failure conditions are:
- The ISA is beyond the granfilade's width (line 31) — the link was never allocated
- `retrievecrums` can't find a crum at that address (line 34) — storage corruption
- The crum's totaloffset doesn't match the address (line 37) — no exact hit

There is **no version check**. There is no "is this link still live?" check. There is no check that the link is referenced by any document's POOM. If the ISA was ever written to the granfilade, it is retrievable.

---

### 4. Endset Subspace Layout

`retrieveendsetsfromspanf` defines three hardcoded subspaces within the link's orgl [`spanf1.c:210-217`]:

```c
fromspace.stream.mantissa[0] = LINKFROMSPAN;
fromspace.width.mantissa[0] = 1;

tospace.stream.mantissa[0] = LINKTOSPAN;
tospace.width.mantissa[0] = 1;

threespace.stream.mantissa[0] = LINKTHREESPAN;
threespace.width.mantissa[0] = 1;
```

These are the three endsets of a ternary link, stored at fixed offsets within the link's own orgl. They are retrieved by `retrievesporglsetinrange` without any reference to the originating document's POOM.

---

### Answer

**`retrieveendsets` is unconditionally BERT-free**: `NOBERTREQUIRED` bypasses `checkforopen` at [`bert.c:59-60`] before the BERT table is consulted. There is no guard requiring the link to be open, checked out, or mapped in any document's POOM.

**Old and superseded links are fully queryable**: `fetchorglgr` at [`granf2.c:22`] looks up the link's orgl in the persistent global granfilade by ISA address alone. As long as the ISA exists in granf storage — which it does for any link that was ever successfully created — the endsets are returned. The existence of a newer version of the link's originating document is irrelevant: the link ISA is a permanent, immutable address in the granfilade.

The only way `retrieveendsets` fails is if the link ISA was never written to storage (i.e., the link was never created, or the ISA is invalid). Once a link is created and its ISA committed to the granfilade, its endsets are permanently and unconditionally accessible via `retrieveendsets`.
