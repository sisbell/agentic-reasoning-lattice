## Question 20 [gregory]

> When a link is created with endsets spanning content that is later REARRANGED across a subspace boundary (e.g., text moved from V:1.x to V:2.x), do the link's I-address-based endsets remain fully intact in the spanfilade, and does `find_links` still discover the link from the content's new V-position?

## KB Synthesis

**Yes on both counts — endsets remain intact, and `find_links` still discovers the link — but for reasons that expose a fragile decoupling between the spanfilade and the POOM.**

## Why endsets survive intact

REARRANGE modifies only the V-dimension displacement of POOM crums via `tumbleradd(&ptr->cdsp.dsas[index], &diff[i], ...)` [ST-REARRANGE, Finding 0056]. The I-dimension (`dsas[I]`) is never touched. The spanfilade, which indexes link endsets by I-address, is a write-only structure with no deletion operation [INV-SPANF-WRITE-ONLY, Finding 0057]. Since REARRANGE calls no spanfilade function at all, the endset entries survive unchanged. This is the same invariant that makes REARRANGE identity-preserving: `∀ c : i_addr(c, after) = i_addr(c, before)` [INV-REARRANGE-IDENTITY].

## Why `find_links` still works

`find_links` operates purely in I-space: it converts the query V-span → I-span via the POOM, then searches the spanfilade by I-address [SS-FIND-LINKS, Finding 0028]. After cross-subspace rearrangement, the moved text's POOM crums now reside at V:2.x, but they still carry the original permascroll I-addresses. A query specifying the content at its new V:2.x position goes through:

```
V:2.x → vspanset2ispanset → POOM (still maps 2.x → permascroll I) → 
  spanfilade search → finds link (I-address entry unchanged)
```

The POOM lookup succeeds because the crum was displaced in-place, not deleted. The spanfilade lookup succeeds because REARRANGE never modified it.

## The caveat: convention violation is structurally tolerated

Finding 0051 explicitly confirms this scenario: `retrieve_contents` at V:2.x returns text bytes ("ABC") after a cross-subspace pivot. The backend treats it as valid. The subspace convention that V:2.x should contain only link orgl ISAs is a caller-enforced invariant [INV-SUBSPACE-CONVENTION, PRE-REARRANGE], not a storage-layer enforcement. `acceptablevsa()` is a no-op [Finding 0010].

So link discovery works, but the system is now in a state violating the subspace convention:

- Content at V:2.x is text (permascroll I-addresses), not a link orgl reference
- `find_links` discovers the original link ✓ (I-space unchanged)
- `compare_versions` would **not** find this content — it requires text-subspace input (V ≥ 1.x) [PRE-COMPARE-VERSIONS], and the rearranged content is now at 2.x
- `CREATENEWVERSION` would also miss the displaced content, since `retrievedocumentpartofvspanpm` returns only the text-subspace V-dimension [ST-VERSION-CREATE, Finding 0043]

The subspace-isolation mechanism that normally protects the 2.x subspace (INSERT's two-blade knife [SS-TWO-BLADE-KNIFE, FC-SUBSPACE]) does not apply to REARRANGE — REARRANGE has no equivalent guard [PRE-REARRANGE, Finding 0051]. The missing precondition is `all cuts must lie within the same subspace`.

---

## Code Exploration

Now I have everything needed. Let me trace the full execution path.

---

## Full Answer

### The Short Answer

**Yes, the link's I-address-based endsets remain fully intact in the spanfilade after a rearrangement.** And **yes, `find_links` does discover the link from the content's new V-position** — because `find_links` routes through the POOM (permutation matrix), which is the only structure rearrangement modifies. The spanfilade is never touched by rearrangement.

---

### Part 1: How a Link's Endsets Are Stored at Creation Time

`createlink()` [fns.c:100-112] → `docreatelink()` [do1.c:195-221]:

```c
bool docreatelink(typetask *taskptr, typeisa *docisaptr, typespecset fromspecset, ...)
{
    ...
    specset2sporglset(taskptr, fromspecset, &fromsporglset, NOBERTREQUIRED)  // V → I
    specset2sporglset(taskptr, tospecset,   &tosporglset,   NOBERTREQUIRED)  // V → I
    specset2sporglset(taskptr, threespecset, &threesporglset, NOBERTREQUIRED)
    ...
    insertendsetsinorgl(...)  // stores I-addresses in the link's own POOM
    insertendsetsinspanf(taskptr, spanf, linkisaptr, fromsporglset, tosporglset, threesporglset)
}
```
[do1.c:214-219]

The call to `specset2sporglset` converts the caller's V-addresses into **I-addresses (permascroll spans)** by traversing the document's POOM. The resulting sporglsets hold I-address data (`sporglorigin`, `sporglwidth`), not V-addresses.

`insertendsetsinspanf()` [do2.c:116-128] then calls `insertspanf` three times — once for FROM, TO, and THREE:

```c
insertspanf(taskptr, spanfptr, linkisaptr, fromsporglset, LINKFROMSPAN)
insertspanf(taskptr, spanfptr, linkisaptr, tosporglset,   LINKTOSPAN)
insertspanf(taskptr, spanfptr, linkisaptr, threesporglset, LINKTHREESPAN)
```

Inside `insertspanf()` [spanf1.c:15-54], for a `SPORGLID` item:

```c
movetumbler(&((typesporgl*)sporglset)->sporglorigin,  &lstream);       // I-address
movetumbler(&((typesporgl*)sporglset)->sporglwidth,   &lwidth);        // I-width
movetumbler(&((typesporgl*)sporglset)->sporgladdress, &linfo.homedoc); // home doc ISA
...
movetumbler(&lstream, &crumorigin.dsas[SPANRANGE]);   // I-address → SPANRANGE axis
movetumbler(&lwidth,  &crumwidth.dsas[SPANRANGE]);
insertnd(taskptr, (typecuc*)spanfptr, &crumorigin, &crumwidth, &linfo, SPANRANGE);
```
[spanf1.c:31-51]

The spanfilade is a 2D structure with:
- **ORGLRANGE axis**: `prefixtumbler(linkISA, LINKFROMSPAN/LINKTOSPAN, ...)` — the link's permanent ISA
- **SPANRANGE axis**: the content's **I-address** (permascroll address), completely independent of its V-position

This means from the moment of creation, the spanfilade contains only I-addresses. **V-addresses are nowhere in the spanfilade.**

---

### Part 2: What Rearrangement Does — and Does Not — Touch

`rearrange()` [fns.c:159-173] → `dorearrange()` [do1.c:34-43]:

```c
bool dorearrange(typetask *taskptr, typeisa *docisaptr, typecutseq *cutseqptr)
{
    findorgl(taskptr, granf, docisaptr, &docorgl, WRITEBERT)
    rearrangepm(taskptr, docisaptr, docorgl, cutseqptr)
}
```

`rearrangepm()` [orglinks.c:137-142]:

```c
bool rearrangepm(typetask *taskptr, tumbler *docisaptr, typeorgl docorgl, typecutseq *cutseqptr)
{
    rearrangend((typecuc*)docorgl, cutseqptr, V);  // <-- only the POOM, only the V dimension
    logbertmodified(docisaptr, user);
    return(TRUE);
}
```

`rearrangend()` [edit.c:78-160] operates exclusively on `cdsp.dsas[V]` — the V-displacement of crums within the POOM:

```c
case 1: case 2: case 3:
    tumbleradd(&ptr->cdsp.dsas[index], &diff[i], &ptr->cdsp.dsas[index]);
    ivemodified((typecorecrum*)ptr);
    break;
```
[edit.c:124-126], where `index == V`.

**Neither `dorearrange`, `rearrangepm`, nor `rearrangend` mentions `spanf`.** The spanfilade global is not touched. The I-addresses stored in the SPANRANGE axis of the spanfilade are completely unaffected.

The cross-subspace boundary concern (V:1.x → V:2.x) is irrelevant to the spanfilade because the spanfilade doesn't store V-addresses at all. Only the POOM's V-dimension changes.

---

### Part 3: How V:1.x Became V:2.x — The POOM After Rearrangement

After rearrangement, the POOM crums for the affected content have new `cdsp.dsas[V]` values. The I-dimension (`cdsp.dsas[I]`) of these crums is **not modified** — it still holds the same permascroll origin as when the content was first inserted. This is the permanent identity of the content.

The V↔I mapping invariant of the POOM is preserved: for any content atom, `cdsp.dsas[I]` = permascroll address, `cdsp.dsas[V]` = current version-space position. After rearrangement, `cdsp.dsas[V]` has changed but `cdsp.dsas[I]` has not.

---

### Part 4: How `find_links` Discovers the Link from the New V-Position

`findlinksfromtothree()` [fns.c:189-202] → `dofindlinksfromtothree()` [do1.c:348-353] → `findlinksfromtothreesp()` [spanf1.c:56-103]:

```c
bool findlinksfromtothreesp(typetask *taskptr, typespanf spanfptr,
    typespecset fromvspecset, ...)
{
    ...
    if (fromvspecset)
        specset2sporglset(taskptr, fromvspecset, &fromsporglset, NOBERTREQUIRED);
    ...
    if (fromvspecset) {
        sporglset2linkset(taskptr, (typecuc*)spanfptr, fromsporglset,
                          &fromlinkset, orglrange, LINKFROMSPAN);
        ...
    }
    intersectlinksets(taskptr, fromlinkset, tolinkset, threelinkset, linksetptr);
    return (TRUE);
}
```
[spanf1.c:70-103]

Step 1: `specset2sporglset(taskptr, fromvspecset, &fromsporglset, ...)` — this converts the **query's V-address** (the content's **new** V-position after rearrangement, e.g., V:2.x) to I-addresses by traversing the **current** POOM.

The conversion path: `specset2sporglset` → `specset2ispanset` [do2.c:14-46] → `vspanset2ispanset` [orglinks.c:397-402] → `permute(orgl, vspanset, V, ispanset, I)` [orglinks.c:404-422] → `span2spanset` [orglinks.c:425-454] → `retrieverestricted` [retrie.c:56-85].

`retrieverestricted` searches the POOM's V dimension for crums overlapping V:2.x. After rearrangement, the POOM crums for the content are exactly there (their `cdsp.dsas[V]` was updated by `rearrangend`). The search returns those crums' I-addresses — which are the **same I-addresses** that were stored in the spanfilade at link creation time.

Step 2: `sporglset2linkset(spanfptr, fromsporglset, &fromlinkset, ..., LINKFROMSPAN)` — searches the spanfilade's SPANRANGE axis for those I-addresses. Since the spanfilade contains exactly those I-addresses (stored when the link was created and never modified), the search succeeds.

**The link is found.**

---

### Summary of the Invariant Chain

| Structure | What's stored | Affected by rearrangement? |
|---|---|---|
| Document POOM | V↔I crum mapping | **Yes** — `cdsp.dsas[V]` adjusted by `rearrangend` |
| Spanfilade (SPANRANGE) | I-addresses of link endsets | **No** — never touched by `rearrangepm` |
| Spanfilade (ORGLRANGE) | Link ISA | **No** — link ISA is permanent |

The design guarantees correctness through the single POOM-as-mediator pattern:

1. Link creation: V → POOM → I → stored in spanfilade  
2. Rearrangement: POOM V-dimension updated, spanfilade untouched  
3. `find_links`: new V → updated POOM → same I → found in spanfilade → **link recovered**

The V-subspace boundary crossing (V:1.x → V:2.x) is simply a large displacement in `cdsp.dsas[V]`, handled the same as any other `tumbleradd` in `rearrangend` [edit.c:125]. The tumbler arithmetic is agnostic to subspace boundaries. The link's I-address endsets in the spanfilade are unaffected, and `find_links` succeeds from the new V-position.
