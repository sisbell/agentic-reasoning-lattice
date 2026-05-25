## Question 20 [evidence]

> For the "show deletions" feature, would the returned content need to be expressed as a sporglset (I-address spans with origin document) rather than a VSpec, given that the deleted content has no current V-position?

## KB Synthesis

Yes, deleted content must be expressed in I-address terms — a sporglset is the right choice, not a VSpec.

The core issue is that VSpec requires `(doc, start_V, width)`, and V-positions of deleted content no longer exist in any POOM. The I-to-V conversion path (`linksporglset2specset` → `span2spanset` → `retrieverestricted`) **silently drops** I-addresses with no current POOM mapping [INV-ITOV-FILTERING]. The normal pipeline cannot produce VSpecs for deleted content.

The sporgl is the correct representation here because it carries exactly what survives deletion:

- `sporglorigin` — the I-address (permanent, granfilade never removes it [FC-GRANF-ON-DELETE])
- `sporglwidth` — the byte count
- `sporgladdress` — which document originally placed it (DOCISPAN retains this permanently [SS-DOCISPAN, INV-SPANF-WRITE-ONLY])

All three fields are available post-deletion. The actual content bytes remain retrievable via `ispanset2vstuffset` against the granfilade.

The implementation pattern for "show deletions" would be:

1. Identify I-addresses in v1 not present in v2's POOM (these are deletions)
2. Express them as sporglsets — I-address + width + origin doc
3. Retrieve bytes directly via granfilade I-address lookup

This is structurally identical to how [EC-GHOST-LINK] / [SS-FOLLOWLINK] handle link endpoints pointing to deleted content: the operation succeeds at the I-address layer, but V-address resolution returns empty. The difference is that "show deletions" intentionally operates at I-address level rather than failing silently.

[INT-DELETE-SPANF-DIVERGENCE] confirms the information is available — after DELETE, the spanfilade still indexes the document against those I-addresses, providing the provenance half of the sporgl. The granfilade provides the content. No V-positions needed.

---

## Code Exploration

---

## Answer: Sporglset vs. VSpec for "Show Deletions"

**Yes — deleted content cannot be expressed as a VSpec. A sporglset (or bare ispanset) is the only viable representation.** Here is the full chain of evidence from the source.

---

### 1. What a VSpec requires

```c
// xanadu.h:78-83
typedef struct structtypevspec{
    struct structtypevspec *next;
    typeitemid      itemid;
    typeisa docisa;
    typevspanset vspanset;
} typevspec;
```

A `typevspec` is: *document ISA* + *set of V-positions in that document*. The V-positions point into the document's current POOM (permutation matrix enfilade). They have no meaning without live POOM entries.

---

### 2. What deletion does to the POOM

Deletion is dispatched through `dodeletevspan` → `deletevspanpm` → `deletend`:

```c
// do1.c:158-167
bool dodeletevspan(typetask *taskptr, typeisa *docisaptr, typevspan *vspanptr)
{
    return (
       findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
    && deletevspanpm (taskptr, docisaptr, docorgl, vspanptr));
}
```

```c
// orglinks.c:145-152
bool deletevspanpm(typetask *taskptr, tumbler *docisaptr, typeorgl docorgl, typevspan *vspanptr)
{
    if (iszerotumbler(&vspanptr->width))
        return (FALSE);
    deletend((typecuc*)docorgl, &vspanptr->stream, &vspanptr->width, V);
    logbertmodified(docisaptr, user);
    return (TRUE);
}
```

Inside `deletend` [edit.c:31-76], crums that fall within the deleted V-range are **physically removed**:

```c
// edit.c:58-60
case 1:
    disown ((typecorecrum*)ptr);
    subtreefree ((typecorecrum*)ptr);
    break;
```

`disown` + `subtreefree` removes those crums from the enfilade tree entirely. The V→I mappings they carried are gone. Crums *after* the deletion have their V-displacement shifted by `-width` [edit.c:63]:

```c
// edit.c:62-64
case 2:
    tumblersub (&ptr->cdsp.dsas[index], width, &ptr->cdsp.dsas[index]);
    break;
```

**Consequence:** the V-addresses of the deleted content no longer exist in the POOM. Any V-spans pointing into the deleted region are now stale/invalid.

---

### 3. V↔I translation requires live POOM entries

Both conversion functions go through the POOM:

```c
// orglinks.c:389-394
typevspanset *ispan2vspanset(typetask *taskptr, typeorgl orgl, typeispan *ispanptr, typevspanset *vspansetptr)
{
    return permute(taskptr, orgl, ispanptr, I, vspansetptr, V);
}

// orglinks.c:397-402
typeispanset *vspanset2ispanset(typetask *taskptr, typeorgl orgl, typevspanset vspanptr, typeispanset *ispansetptr)
{
    return permute(taskptr, orgl, vspanptr, V, ispansetptr, I);
}
```

`permute` → `span2spanset` → `retrieverestricted` [retrie.c:56-85] → `retrieveinarea` [retrie.c:87-110] → `findcbcinarea2d` walks the enfilade tree looking for crums that overlap the query span. After `deletend` has freed the relevant crums, this traversal finds nothing. Both directions of conversion silently return empty/NULL for deleted content.

---

### 4. What a sporglset is and why it survives deletion

```c
// xanadu.h:115-121
typedef struct structsporgl{
    struct structsporgl *next;
    typeitemid      itemid;
    tumbler sporglorigin;   /* I-space start */
    tumbler sporglwidth;    /* I-space width */
    typeisa sporgladdress;  /* origin document ISA */
} typesporgl;
```

A sporgl is: *I-span* (permascroll address) + *origin document*. It references content **by its permanent I-address**, not by V-position. The permascroll is write-once — content inserted into I-space is never removed. Only the POOM (which maps I-space to V-space) is modified by edits and deletions.

After `deletend` runs, the I-addresses of the deleted content are still valid in the granfilade (permascroll). Only the POOM crums that mapped those I-addresses to V-positions have been freed.

---

### 5. The link endpoint precedent confirms this design

When a link is created, endpoints are **always converted from VSpec to sporglset** before storage:

```c
// do1.c:195-221
bool docreatelink(...)
{
    ...
    specset2sporglset (taskptr, fromspecset, &fromsporglset, NOBERTREQUIRED)
    specset2sporglset (taskptr, tospecset, &tosporglset, NOBERTREQUIRED)
    ...
    insertendsetsinorgl (taskptr, linkisaptr, link, &fromvsa, fromsporglset, ...)
    insertendsetsinspanf (taskptr, spanf, linkisaptr, fromsporglset, ...)
}
```

`specset2sporglset` [sporgl.c:14-33] calls `vspanset2sporglset` [sporgl.c:35-65], which converts V-spans → I-spans using `vspanset2ispanset`, then records the document ISA as `sporgladdress`:

```c
// sporgl.c:50-57
sporglset->itemid = SPORGLID;
sporglset->next = NULL;
movetumbler (docisa, &sporglset->sporgladdress);   /* origin doc */
movetumbler(&ispanset->stream, &sporglset->sporglorigin);  /* I-span */
movetumbler (&ispanset->width, &sporglset->sporglwidth);
```

The reason links store sporglsets rather than VSpecs is precisely that I-addresses are **stable across edits and versions**, while V-addresses are not. The same reasoning applies to deleted content.

---

### 6. The follow-link path reveals what breaks when content is deleted

`dofollowlink` [do1.c:223-232] retrieves the sporglset from a link's POOM, then tries to convert back to a specset:

```c
// sporgl.c:97-123  (linksporglset2specset)
if (iszerotumbler (&((typesporgl *)sporglset)->sporgladdress)) {
    /* bare ispan — return directly */
    ((typeitemheader *)specset)->itemid = ISPANID;
    movetumbler(...stream...); movetumbler(...width...);
} else {
    linksporglset2vspec(taskptr, homedoc, &sporglset, (typevspec*)specset, type);
}
```

`linksporglset2vspec` → `sporglset2vspanset` → `ispan2vspanset` [sporgl.c:141-176] attempts to find a current V-position for the I-span. If the content has been deleted from that document's POOM, this returns nothing — you'd get a `typevspec` with a null `vspanset`. The content exists in I-space but cannot be located in V-space.

---

### Summary

| Representation | Requires live POOM entry? | Survives deletion? |
|---|---|---|
| `typevspec` (VSpec) | Yes — V-spans reference the current POOM | No |
| `typesporgl` (sporglset) | No — I-spans reference permascroll directly | Yes |
| `typeispan` (bare ispanset) | No — same as sporgl without origin doc | Yes (no origin doc) |

A "show deletions" feature would need to return a **sporglset**: `{sporglorigin, sporglwidth, sporgladdress}` — the permanent I-address range of the deleted content, together with the ISA of the document it was deleted from. This is exactly the information that survives `deletend`, and it is the form the system already uses internally everywhere that content references must outlast document edits (link endpoint storage, `specset2sporglset`, `contextintosporgl`).

A bare ispanset (no `sporgladdress`) would work if the caller only needs to retrieve content from the permascroll without knowing which document it came from. The sporgl form is richer and is the canonical representation when document provenance matters — as it would for "show deletions" (you need to know *which document* had the deletion).
