## Question 18 [gregory]

> When CREATENEWVERSION is called on a document that has had significant content DELETEd, does the version capture the current (post-delete) POOM state, and are the I-addresses of the deleted content permanently unreachable from the version's perspective even though they persist in the granfilade?

## KB Synthesis

Yes to both parts. Here is the synthesis:

---

## What CREATENEWVERSION Captures

CREATENEWVERSION reads the source document's **current POOM state** at call time. The call chain is:

`docreatenewversion` → `doretrievedocvspanfoo` → `retrievedocumentpartofvspanpm` → reads `cdsp.dsas[V]` and `cwid.dsas[V]` from the root node → `docopyinternal` → `specset2ispanset` → `insertpm` + `insertspanf`

The critical step is `specset2ispanset`, which converts the *current* V-span of the source document to I-spans by walking the source's POOM. Since DELETE removes bottom crums from the POOM via `disown` + `subtreefree` [ST-DELETE, Finding 0064, 0072], those V-to-I mappings simply do not exist when `specset2ispanset` executes. The version therefore receives only the surviving content's I-address mappings. [ST-VERSION-CREATE, Finding 0032, 0046]

Additionally, CREATENEWVERSION copies only the text subspace (1.x V-positions) — the link subspace is excluded because `retrievedocumentpartofvspanpm` returns the displacement pointing to position 1. [ST-VERSION-CREATE, Finding 0043]

---

## Are Deleted I-Addresses Permanently Unreachable from the Version?

**From the version's POOM:** Yes, permanently. The version's POOM was built by copying only the post-delete V-to-I mappings. The version has no entries mapping any V-position to the deleted I-addresses. [INV-IADDR-IMMUTABILITY], [FC-GRANF-ON-DELETE]

**From the granfilade:** The I-addresses persist unconditionally. The granfilade is append-only — DELETE never touches it. [FC-GRANF-ON-DELETE, Finding 0061, 0064] The content bytes remain at those I-addresses indefinitely.

**From the spanfilade (DOCISPAN):** The version's `insertspanf` call only registers DOCISPAN entries for the surviving content's I-addresses. The deleted I-addresses are not registered under the version's ISA. The *source* document retains stale DOCISPAN entries for the deleted I-addresses [INV-SPANF-WRITE-ONLY], so `find_documents(deleted_iaddr)` would still return the source document (as a ghost reference [EC-STALE-SPANF-REFERENCE]) — but not the version.

**Practical consequence:** `compare_versions(version, other_doc)` cannot report shared content for the deleted material, because the version's POOM has no I-span entries to intersect against. The version has no path from V-space to those I-addresses. [SS-COMPARE-VERSIONS]

---

## The One Exception: Reconstitution via VCOPY

The deleted I-addresses are unreachable **from the version as-is**, but not permanently destroyed. If another document (e.g., the source document before deletion, or any transclusion of it) still has POOM entries for those I-addresses, a VCOPY from that document into the version would restore the V-to-I mappings and make those I-addresses reachable again — because VCOPY shares existing I-addresses rather than allocating new ones. [ST-COPY, Finding 0064], [INV-DELETE-NOT-INVERSE]

This is precisely why CREATENEWVERSION before editing is the only identity-preserving snapshot mechanism: a version created post-delete cannot reconstruct pre-delete identity. [ST-VERSION-CREATE, Finding 0072]

---

## Code Exploration

I now have all the source data needed. Let me write the complete answer.

---

## Answer: CREATENEWVERSION After DELETE — POOM Snapshot and Granfilade Persistence

### Short Answer

**Yes** — CREATENEWVERSION captures the current post-delete POOM state. The new version's POOM contains only V→I mappings for content that survived the deletion. The deleted content's I-addresses remain orphaned in the granfilade, permanently unreachable from the new version (or from the original document itself) through any normal operation.

---

### 1. What DELETE Does to the POOM

**Call chain:**

`fns.c:333` `deletevspan()` → `do1.c:158` `dodeletevspan()` → `orglinks.c:145` `deletevspanpm()` → `edit.c:31` `deletend()`

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

`deletend()` [edit.c:31-76] places "knives" at the region boundaries, splits any straddling crums, then iterates over the POOM children and applies two cases:

```c
// edit.c:58-64
case 1:
    disown ((typecorecrum*)ptr);
    subtreefree ((typecorecrum*)ptr);   // ← physically frees POOM crum
    break;
case 2:
    tumblersub (&ptr->cdsp.dsas[index], width, &ptr->cdsp.dsas[index]);
    // ← shifts right-side crums' displacement left (closes the V-gap)
    break;
```

- **Case 1**: Any POOM crum that lies entirely within the deleted V-range is `disown()`ed and `subtreefree()`d — permanently removed from the enfilade tree and freed from memory. The V→I mapping it encoded is gone.
- **Case 2**: Crums to the right of the deleted region have their V-displacement reduced by `width`, closing the gap.

After the loop, `setwispupwards(father, 1)` [edit.c:74] propagates corrected aggregate widths up to the apex crum.

**Critical observation:** `deletend()` operates only on `docorgl` — the document's POOM enfilade. It never touches `granf`. There is no `deletend()` or `subtreefree()` call on the granfilade during a delete. The actual content bytes and their I-addresses in the granfilade are entirely untouched.

---

### 2. What CREATENEWVERSION Reads From the Post-Delete POOM

**Call chain:**

`fns.c:289` `createnewversion()` → `do1.c:260` `docreatenewversion()`

```c
// do1.c:260-299
bool docreatenewversion(typetask *taskptr, typeisa *isaptr, typeisa *wheretoputit, typeisa *newisaptr)
{
    typevspan vspan;
    typevspec vspec;
    ...
    if (!createorglingranf(taskptr, granf, &hint, newisaptr)) ...  // new empty POOM
    if (!doretrievedocvspanfoo (taskptr, isaptr, &vspan)) ...      // read source V-span
    
    vspec.docisa = *isaptr;          // line 287: source doc ISA
    vspec.vspanset = &vspan;         // current (post-delete) V-span
    
    addtoopen(newisaptr, user, TRUE, WRITEBERT);
    docopyinternal(taskptr, newisaptr, &vspan.stream, &vspec);     // copy into new version
    logbertmodified(newisaptr, user);
    doclose(taskptr, newisaptr, user);
    return (TRUE);
}
```

`doretrievedocvspanfoo` [do1.c:301-309] calls `retrievedocumentpartofvspanpm`:

```c
// orglinks.c:155-162
bool retrievedocumentpartofvspanpm(typetask *taskptr, typeorgl orgl, typevspan *vspanptr)
{ /* this is a kluge*/
    vspanptr->next = NULL;
    vspanptr->itemid = VSPANID;
    movetumbler (&((typecuc *) orgl)->cdsp.dsas[V], &vspanptr->stream);  // apex displacement
    movetumbler (&((typecuc *) orgl)->cwid.dsas[V], &vspanptr->width);   // apex width
    return (TRUE);
}
```

This reads the apex crum's `cwid.dsas[V]` directly. After `deletend()` + `setwispupwards()`, this width reflects the **current post-delete V-extent** — the deleted V-range has been subtracted. So `vspan` describes only the surviving content's V-space.

---

### 3. How V→I Translation Excludes Deleted Content

`docopyinternal` [do1.c:66-82] is the workhorse. It calls `specset2ispanset` [do2.c:14-46]:

```c
// do2.c:34-38
if (!(
  findorgl (taskptr, granf, &((typevspec *)specset)->docisa, &docorgl, type)
&& (ispansetptr = vspanset2ispanset (taskptr, docorgl, ((typevspec *)specset)->vspanset, ispansetptr)))){
       return (FALSE);
}
```

This finds the **original document's** orgl (the post-delete POOM), then calls `vspanset2ispanset` [orglinks.c:397-402]:

```c
// orglinks.c:397-402
typeispanset *vspanset2ispanset(..., typeorgl orgl, typevspanset vspanptr, ...)
{
    return permute(taskptr, orgl, vspanptr, V, ispansetptr, I);
}
```

`permute` [orglinks.c:404-422] → `span2spanset` [orglinks.c:425-453] → `retrieverestricted()` — which traverses the POOM enfilade looking for crums that overlap the given V-span restriction, collecting their corresponding I-coordinates.

**The key**: because `deletend()` physically removed the POOM crums encoding the deleted V→I mappings, `retrieverestricted()` finds no crums in those V-ranges. No I-spans are produced for the deleted content. Only the surviving crums — with their shifted V-displacements — yield I-spans.

`insertpm` [orglinks.c:75-134] then writes those I-spans into the new version's POOM, at the surviving V-addresses. The new version's POOM is a faithful copy of the post-delete POOM of the source.

---

### 4. Granfilade Persistence of Deleted I-Addresses

When `inserttextgr` [granf2.c:83-109] originally inserted text, it allocated a permanent I-address in the granfilade and stored the bytes there:

```c
// granf2.c:83-109
bool inserttextgr(..., typetextset textset, typeispanset *ispansetptr)
{
    findisatoinsertgr (..., &lsa);   // find I-address to insert at
    movetumbler (&lsa, &spanorigin);
    for (; textset; textset = textset->next) {
        locinfo.infotype = GRANTEXT;
        locinfo.granstuff.textstuff.textlength = textset->length;
        movmem(textset->string, locinfo.granstuff.textstuff.textstring, ...);
        insertseq ((typecuc*)fullcrumptr, &lsa, &locinfo);  // put in granfilade
        tumblerincrement (&lsa, 0, textset->length, &lsa);
    }
    // record ispanset of the allocated I-range
}
```

These granfilade crums hold the content permanently. Nothing in the delete path removes them. After deletion:

- The **POOM** (document enfilade) no longer contains crums encoding V→I mappings for the deleted V-range.
- The **granfilade** still contains the GRANTEXT crums for those I-addresses.
- No document — including the new version — has a POOM crum pointing to those I-addresses.
- `ispan2vstuffset` [granf2.c:286-318], the only other way to access granfilade content, takes an I-span and retrieves text; but without a POOM to map V→I, no client operation naturally produces those I-spans.

The deleted content is **orphaned**: its I-addresses are permanently allocated and occupy storage in the granfilade, but are semantically invisible — unreachable through any document's V→I lookup chain.

---

### Summary Table

| Question | Answer | Key Lines |
|---|---|---|
| Does CREATENEWVERSION snapshot post-delete state? | **Yes** — reads apex `cwid.dsas[V]` which was updated by `setwispupwards` after delete | `orglinks.c:159-160`, `edit.c:74` |
| Are deleted V→I mappings in the new version's POOM? | **No** — `retrieverestricted` finds no POOM crums for freed V-ranges | `edit.c:59-61`, `orglinks.c:435` |
| Does deleted content persist in the granfilade? | **Yes** — `deletend` touches only POOM, never `granf` | `edit.c:31-76`, `orglinks.c:149` |
| Are the orphaned I-addresses reachable from the new version? | **No** — no POOM crum in either original or new version maps to them | `do2.c:34-38`, `orglinks.c:404` |
| Are the orphaned I-addresses reachable from the *original* document? | **No** — the source document's POOM also had those crums freed | `edit.c:59-61` |

### Implication

The architecture makes DELETE semantically permanent from a document perspective, even though the granfilade is structurally append-only. The POOM is the sole indexing structure for V→I navigation; once a POOM crum is `subtreefree()`d, its content becomes granfilade dark matter — present in storage, indexed by a permanent I-address, but unreachable through any versioned document view. CREATENEWVERSION faithfully inherits this darkness: it copies the current (reduced) POOM state, not any historical snapshot.
