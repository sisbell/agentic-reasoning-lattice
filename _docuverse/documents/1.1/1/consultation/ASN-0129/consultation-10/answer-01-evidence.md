## Question 1 [evidence]

> Does any read or link-creation operation in udanax-green test or enumerate bare content existence — e.g., validating that an endset's I-addresses hold stored content before depositing the link — or is content only ever reached through document arrangement (V→I) reads, with no content-store existence check anywhere on the query or gating path?

## KB Synthesis

No operation on any read or link-creation path tests bare content existence in the permascroll. Content bytes are reached only through the retrieval operation, and no gating or validation step anywhere else queries the content store for I-address occupancy.

## Link creation path

`docreatelink` performs three steps [ST-CREATE-LINK]:

1. Allocate a link orgl address via `createorglingranf()` — this writes to the granfilade structure, not content.
2. Copy the orgl ISA into the document's 2.x V-subspace via `docopy()`.
3. Index endpoint I-addresses in the spanfilade via `insertendsetsinspanf()`.

Step 3 is the key step. The endpoint V-spans are converted to I-addresses through `vspanset2sporglset()` → `vspanset2ispanset()` → POOM traversal [SS-VSPAN-TO-SPORGL]. This reads the document's enfilade to find *which I-addresses the V-positions currently map to*, then deposits those addresses directly into the spanfilade index. At no point is `ispanset2vstuffset()` called — no bytes are read from the permascroll to validate that content exists at those I-addresses.

## Link discovery and follow path

`find_links` converts the search specset to I-addresses and performs a set intersection against the spanfilade index [ST-FIND-LINKS]. The entire operation is I-address arithmetic — no content read.

`FOLLOWLINK` has two phases [SS-FOLLOWLINK]:

1. `link2sporglset()` extracts stored I-addresses from the link orgl via `retrieverestricted()` on the link orgl itself — reading address values, not content bytes.
2. `linksporglset2specset()` → `span2spanset()` → `retrieverestricted()` on the document's POOM — this is an I→V translation checking whether the I-address has a current V-position mapping.

The POOM check in phase 2 is the only existence-style gate, and it is a *document arrangement* check (does this I-address appear in a V-stream?) not a *content-store* check (do bytes exist at this I-address?). If the I-address has no POOM mapping, it is silently dropped with no error [INV-ITOV-FILTERING]. The permascroll is never queried.

## The only path to content bytes

`ispanset2vstuffset(taskptr, granf, ispanset, vstuffsetptr)` is the sole function that dereferences I-addresses into permascroll content bytes [SS-GRANF-OPERATIONS]. It is called only from `doretrievev` during `retrieve_contents` operations [PRE-RETRIEVE-CONTENTS]. It appears nowhere in the link creation chain, the spanfilade indexing chain, or the FOLLOWLINK chain.

## Why no check is needed

The design relies on a structural guarantee rather than explicit validation: I-addresses are only ever allocated when content is inserted (`inserttextingranf`), and the granfilade is strictly append-only [INV-IADDR-IMMUTABILITY]. If an I-address exists anywhere — in a POOM, in a spanfilade entry, in a link endset — the corresponding bytes necessarily exist in the permascroll because they were written before the address could propagate. The system treats this as an invariant to be maintained, not a precondition to be checked.

Concretely: every V→I entry in a POOM was written by either INSERT (which called `inserttextingranf` to allocate I-addresses and write bytes) or COPY (which copied existing I-addresses whose bytes were already present). The append-only granfilade means those bytes never disappear. So by the time any link creation or query operation sees an I-address, the content-store existence of its bytes is structurally guaranteed — no runtime check is warranted or performed.

---

## Code Exploration

I now have a complete trace of every relevant path. Here is the full answer.

---

## Does udanax-green check content existence on the query or link-creation path?

**No.** There is no content-store existence check anywhere on the query path or the link-creation gating path. Content is reached exclusively through V→I translation via the document POOM, and neither the I-addresses produced by that translation nor the resulting sporglset endsets are validated against the granfilade (content store).

---

### 1. `acceptablevsa` — the VSA validity guard is a stub

`do2.c:110-113`:
```c
bool acceptablevsa(tumbler *vsaptr, typeorgl orglptr)
{
    return (TRUE);
}
```
Every caller in `docopy` (`do1.c:56`) and `docopyinternal` (`do1.c:76`) hits this unconditional `TRUE`. No VSA is ever rejected on content grounds.

---

### 2. Link-creation path: `docreatelink` → `specset2sporglset` → `vspanset2sporglset`

`docreatelink` (`do1.c:195-221`) calls:

```c
specset2sporglset(taskptr, fromspecset, &fromsporglset, NOBERTREQUIRED)
specset2sporglset(taskptr, tospecset,   &tosporglset,   NOBERTREQUIRED)
specset2sporglset(taskptr, threespecset,&threesporglset, NOBERTREQUIRED)
```

Inside `specset2sporglset` (`sporgl.c:14-33`), for V-spec items it delegates to `vspanset2sporglset` (`sporgl.c:35-65`):

```c
// sporgl.c:44
if (!findorgl(taskptr, granf, docisa, &orgl, type))
    return NULL;   // ← only failure: document must exist in granfilade
for (; vspanset; vspanset = vspanset->next) {
    (void) vspanset2ispanset(taskptr, orgl, vspanset, &ispanset);  // ← return discarded
    for (; ispanset; ispanset = ispanset->next) {
        // build sporgl from ispanset fields — never executed if ispanset is NULL
    }
}
return sporglsetptr;   // ← always returns a valid pointer; no content check
```

The `(void)` cast on `vspanset2ispanset` discards the return value. If the V-span points to positions with no POOM crums, `ispanset` remains NULL, the sporgl-building loop does not execute, and the function returns the (valid, non-NULL) `sporglsetptr`. `specset2sporglset` sees a non-NULL return and reports success. **The link is deposited with empty or partial endsets — no error, no existence check.**

---

### 3. V→I translation produces silence, not failure, on missing content

`vspanset2ispanset` (`orglinks.c:397-402`) calls `permute` (`orglinks.c:404-422`), which calls `span2spanset` (`orglinks.c:425-454`) for each V-span:

```c
// orglinks.c:435
context = retrieverestricted((typecuc*)orgl, restrictionspanptr, restrictionindex,
                              (typespan*)NULL, targindex, (typeisa*)NULL);
for (c = context; c; c = c->nextcontext) {
    context2span(c, ...);
    nextptr = (typespan *)onitemlist(taskptr, &foundspan, targspansetptr);
}
if (!context) {
    return (targspansetptr);   // ← returns unchanged pointer — no error
}
```

`retrieverestricted` (`retrie.c:56-85`) → `retrieveinarea` → `findcbcinarea2d` (`retrie.c:229-268`): walks POOM crums looking for intersection with the V-span. If none intersect, `context = NULL`. `span2spanset` returns `targspansetptr` unchanged. `permute` returns `save` (the original target pointer, never NULL). No I-spans are added, no failure is signalled.

---

### 4. Read path: `doretrievev` also does no content-store check

`doretrievev` (`do1.c:338-346`):
```c
return
   specset2ispanset(taskptr, specset, &ispanset, READBERT)
&& ispanset2vstuffset(taskptr, granf, ispanset, vstuffsetptr);
```

`specset2ispanset` (`do2.c:14-46`) tests:
```c
if (!(findorgl(...) && (ispansetptr = vspanset2ispanset(...)))) return FALSE;
```

`vspanset2ispanset` returns `save`, which is the address of `ispansetptr` — a valid stack address, never NULL. The boolean condition is always true for existing documents. If V-spans map to nothing, `ispanset = NULL` and `specset2ispanset` still returns `TRUE`.

`ispanset2vstuffset` (`granf1.c:58-74`):
```c
for (; ispanset; ispanset = ispanset->next) {
    vstuffsetptr = ispan2vstuffset(taskptr, granfptr, ispanset, vstuffsetptr);
}
return (TRUE);   // ← always TRUE, even for NULL ispanset
```

`ispan2vstuffset` (`granf2.c:286-318`) calls `retrieveinspan` on the granfilade. If the I-addresses have no granfilade content, `context = NULL`, nothing is appended to `vstuffset`, and the function returns the pointer. No error.

**A retrieve against V-addresses with no corresponding content returns an empty vstuffset, not a failure.**

---

### 5. The one true content-existence check: `isaexistsgr` — insertion-only

`isaexistsgr` (`granf2.c:244-253`):
```c
bool isaexistsgr(typecuc *crumptr, typeisa *isaptr)
{
    context = retrieve(crumptr, isaptr, WIDTH);
    ret = tumblereq((tumbler*)&context->totaloffset, isaptr);
    contextfree(context);
    return ret;
}
```

This does a precise content-store lookup and returns TRUE only if that ISA exists at an exact address in the granfilade. But it is called from exactly one place:

`findisatoinsertgr` (`granf2.c:130-156`):
```c
if (hintptr->subtype == ATOM) {
    if (!isaexistsgr(fullcrumptr, &hintptr->hintisa)) {
        fprintf(stderr, "nothing at hintisa for atom\n");
        return FALSE;
    }
    findisatoinsertmolecule(fullcrumptr, hintptr, isaptr);
}
```

`findisatoinsertgr` is called only from `inserttextgr` → `inserttextingranf` (content insertion) and `createorglgr` → `createorglingranf` (organelle creation). Its purpose is to verify that a **parent document exists before inserting content inside it**. This is a structural insertion guard.

`isaexistsgr` is **never** called from:
- `specset2sporglset` / `vspanset2sporglset`
- `specset2ispanset`
- `doretrievev`
- `docreatelink`
- `dofollowlink`
- `link2sporglset`
- any spanfilade query function

---

### Summary

| Operation | Document existence check | Content existence at V-address | Content existence at I-address |
|-----------|--------------------------|-------------------------------|-------------------------------|
| `docreatelink` (endsets) | Yes — `findorgl` in `vspanset2sporglset` | No — `(void)` discards result; empty I-span = silent empty sporglset | Never checked |
| `doretrievev` | Yes — `findorgl` in `specset2ispanset` | No — empty I-span returns empty vstuffset, success | Never checked |
| `dofollowlink` | Yes — `findorgl` in `link2sporglset` | No — POOM walk; empty result returns FALSE but only because `link2sporglset` checks `context` | Never checked |
| `acceptablevsa` | — | Stub: `return TRUE` | — |
| `isaexistsgr` | — | — | Yes — **but only called during content insertion** |

The architecture's implicit assumption is that a POOM crum mapping V→I is authoritative: if the POOM says a V-address corresponds to I-address Y, Y is trusted to exist in the granfilade without verification. There is no defensive path that walks back from an I-address to confirm granfilade occupancy before depositing a link or returning a read result.
