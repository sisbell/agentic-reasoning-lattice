# Revision Consultation — ASN-0043

**Review:** review-14.md
**Date:** 2026-03-22 22:52

## Summary

2 REVISE items analyzed: 1 internal, 1 consulted (0 nelson, 1 gregory)

## Consultation Results

### Issue 2: L12 prose contradicts the formal model on link arrangement

**Category:** GREGORY
**Reason:** The formal model excludes links from arrangements (S3 + L0), but the prose references "Vstream removal" as the deletion mechanism. Whether links have any Vstream/arrangement presence in the implementation — and if so, how deletion works — requires checking the udanax-green code.

**Gregory question:** In udanax-green, do links have entries in the document's Vstream/permutation matrix, and if so, how does link deletion (or hiding) work mechanically — is it Vstream removal, granfilade marking, or something else?

**Gregory's Answer:**

## KB Synthesis

## Links in the V-stream and Deletion Mechanics

### Yes — links have POOM entries

Each link created via `CREATELINK` gets a V-position entry in the home document's POOM at subspace `2.x` (internally). The first link lands at `2.1`, subsequent links at `2.2`, `2.3`, etc. The POOM entry maps that V-position → the link orgl's ISA (I-address). This is how the link appears in `retrieve_vspanset` output (reported as `0.x` when text is also present due to output normalization, or as `2.x` when links only). [SS-LINK-SUBSPACE], [SS-DUAL-ENFILADE]

### Three independent storage layers

Links exist simultaneously in three layers with different mutability: [SS-THREE-LAYER-MODEL]

| Layer | What's stored | Mutability |
|-------|--------------|------------|
| **I-space** (granfilade) | Link orgl at a permanent I-address (e.g., `1.1.0.1.0.1.0.2.1`) | Permanent — never deleted |
| **Spanfilade** | DOCISPAN index entries mapping link I-addresses → document | Append-only — never deleted |
| **POOM** | V-position `2.x` → link ISA mapping in the document | Mutable — only layer that changes |

### Link deletion = POOM removal only

`DELETEVSPAN(2.x)` calls `deletevspanpm` → `deletend`, which removes only the POOM crum covering that V-position. The granfilade link orgl is untouched. The spanfilade entries are untouched. [ST-DELETE], [FC-LINK-DELETE-ISOLATION]

```
Before DELETEVSPAN(2.1):
  POOM:        V:2.1 → link ISA  (present)
  I-space:     link orgl at ISA  (permanent)
  Spanfilade:  ISA → document    (permanent)
  vspanset:    shows link span

After DELETEVSPAN(2.1):
  POOM:        V:2.1 removed
  I-space:     link orgl at ISA  (unchanged)
  Spanfilade:  ISA → document    (unchanged)
  vspanset:    no link span
  find_links(source_specs) → still finds the link
  follow_link(link_id, SOURCE) → still works
```

This produces a **"reverse orphan"** state — the link no longer appears in the document's vspanset but remains fully discoverable via `find_links` and followable via `follow_link`. [EC-REVERSE-ORPHAN], [INV-LINK-PERMANENCE]

### No hiding mechanism exists

There is no `DELETELINK` opcode, no granfilade marking, no tombstone. The only "hiding" available is POOM removal via `DELETEVSPAN`, and even that is partial — the link survives in I-space and the spanfilade index. Once created, a link is permanently discoverable from any document sharing its endpoint's content identity. [INV-LINK-PERMANENCE], [FC-LINK-PERSISTENCE]

The POOM check is explicitly the only gate: `pre_delete(D, addr, width) ≡ width ≠ 0` — no subspace guard, no link-protection rule. [PRE-DELETE]

---

## Code Exploration

Now I have everything I need to write a complete, fully-cited answer.

---

## Links in the Vstream: Storage, Endpoints, and Deletion in udanax-green

### TL;DR

Links **do** have entries in the document's V-space (Vstream/permutation matrix). They are stored in the document's 2D orgl (enfilade) at V-addresses ≥ 2.1, occupying a distinct partition of V-space above text content. Link deletion is **hard matrix removal** via `deletend` — there is no soft hiding, no granfilade marking, and no separate link-deletion operation.

---

### 1. The V-Space Partition

The document's permutation matrix (orgl) partitions V-space into two regions:

**Text lives at V < 2; link references live at V ≥ 2.1.**

This boundary is enforced in `findvsatoappend` [backend/orglinks.c:37]:

```c
tumblerincrement (&linkspacevstart, 0, 2, &linkspacevstart);
```

This sets `linkspacevstart` to tumbler value `2`. The function then checks whether the document's V-space reach is `< 2` (text only), `≥ 2` without crossing 2 (no links yet), or spanning the boundary, and navigates accordingly [orglinks.c:41–48].

When a new link is created, its V-address in the document is found by `findnextlinkvsa` [backend/do2.c:151–167]:

```c
tumblerincrement (&firstlink, 0, 2, &firstlink);   // firstlink = 2
tumblerincrement (&firstlink, 1, 1, &firstlink);   // firstlink = 2.1
```

The first link in a document gets V-address `2.1`. Subsequent links are placed at the end of the document's current V-span reach, continuing above 2.1.

---

### 2. Link Creation: Two Distinct Structures

`docreatelink` [backend/do1.c:195–221] creates **two** separate structures for each link:

**A. The link's own orgl** — a private permutation matrix for its endpoints:

```c
createorglingranf (taskptr, granf, &hint, linkisaptr)   // [do1.c:209]
```

`createorglingranf` calls `createorglgr` [backend/granf2.c:111–128], which allocates a `GRANORGL` leaf in the granfilade and creates a new POOM enfilade:

```c
locinfo.infotype = GRANORGL;
locinfo.granstuff.orglstuff.orglptr = createenf (POOM);   // [granf2.c:120]
```

The link's own orgl stores its endpoint sporgl-sets at fixed V-addresses assigned by `setlinkvsas` [backend/do2.c:169–183]:

| Endpoint | V-address in link's orgl |
|----------|--------------------------|
| FROM     | 1.1                      |
| TO       | 2.1                      |
| THREE    | 3.1                      |

These are inserted via `insertendsetsinorgl` [do2.c:130–148] → `insertpm` (twice or three times).

**B. The link's entry in the *document's* orgl** — the actual Vstream entry:

```c
tumbler2spanset (taskptr, linkisaptr, &ispanset)        // [do1.c:210]
findnextlinkvsa (taskptr, docisaptr, &linkvsa)           // [do1.c:211]
docopy (taskptr, docisaptr, &linkvsa, ispanset)          // [do1.c:212]
```

`docopy` inserts the link's I-span (its ISA as an I-space interval) into the document at `linkvsa` (≥ 2.1). This is what makes the link a *resident* of the document's V-space — the link's ISA tumbler is literally woven into the document's permutation matrix alongside text I-spans.

**C. The spanfilade index** for endpoint traversal:

```c
insertendsetsinspanf (taskptr, spanf, linkisaptr, fromsporglset, tosporglset, threesporglset)  // [do1.c:219]
```

This calls `insertspanf` three times [backend/do2.c:116–128] — once each for `LINKFROMSPAN`, `LINKTOSPAN`, and `LINKTHREESPAN` — recording the endpoints in the global spanfilade for reverse traversal.

---

### 3. Link Deletion: Hard Matrix Removal, Not Hiding

There is **no `deletelink` FEBE command**. The only deletion primitive is `deletevspan`, which operates on any V-span in any document orgl.

The FEBE handler [backend/fns.c:333–347]:

```c
void deletevspan(typetask *taskptr)
{
  typeisa docisa;
  typespan vspan;
  bool getdeletevspan(), dodeletevspan();

  (void) getdeletevspan (taskptr, &docisa, &vspan);
  putdeletevspan (taskptr);                            // ACK sent BEFORE executing
  if (!dodeletevspan (taskptr, &docisa, &vspan))
    fprintf(stderr,"deletevspan failed \n");           // failure only logged
}
```

Note the **fire-and-forget** pattern: unlike `createlink` [fns.c:106–111] which gates the response on success, `deletevspan` acknowledges unconditionally at [fns.c:340] and only logs failure. The commented-out predecessor at [fns.c:317–332] was atomic (`putrequestfailed` on failure); the current live version is not.

`dodeletevspan` [backend/do1.c:158–167]:

```c
bool dodeletevspan(typetask *taskptr, typeisa *docisaptr, typevspan *vspanptr)
{
  typeorgl docorgl;
  return (
     findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
  && deletevspanpm (taskptr, docisaptr, docorgl, vspanptr)
  );
}
```

`deletevspanpm` [backend/orglinks.c:145–152]:

```c
bool deletevspanpm(typetask *taskptr, tumbler *docisaptr, typeorgl docorgl, typevspan *vspanptr)
{
  if (iszerotumbler(&vspanptr->width))
    return (FALSE);
  deletend((typecuc*)docorgl, &vspanptr->stream, &vspanptr->width, V);
  logbertmodified(docisaptr, user);
  return (TRUE);
}
```

`deletend` removes nodes from the enfilade whose V-coordinates intersect `[stream, stream+width)`. This is a structural tree edit — nodes are split at the boundary and the interior is excised. **No "hidden" flag is set. No granfilade entry is marked.** The V-span is gone from the matrix.

To delete a link from a document, a client would call `deletevspan` with the link's V-address (e.g., `stream=2.1, width=0.1` for the first link). This removes the link's I-span from the document's orgl. However — and this is important — the link's **own orgl** (its private endpoint matrix) is **not destroyed** by this operation. Only the document's reference to the link is removed. The link object itself persists in the granfilade, orphaned.

---

### 4. BERT: Orthogonal Concurrency Control

BERT is the Backend Edit Records Table — a concurrency guard, not a storage system. The `bertentry` struct tracks which connection has opened which document and in what mode (READBERT / WRITEBERT / NOBERTREQUIRED). BERT is invoked at [orglinks.c:99] (`logbertmodified`) and [do1.c:164] (`WRITEBERT` in `findorgl`). It is relevant to link operations only in that creating or deleting a link requires WRITEBERT on the target document. It does not store or affect link content.

---

### Summary Table

| Question | Answer |
|---|---|
| Do links have Vstream entries? | **Yes** — inserted at V ≥ 2.1 in the document's orgl via `docopy` [do1.c:212] |
| Where do link endpoints live? | In the **link's own private orgl** at V=1.1 (from), 2.1 (to), 3.1 (three) [do2.c:169–183] |
| What does spanfilade index? | Endpoint sporgl-sets for reverse traversal (LINKFROMSPAN/TOSPAN/THREESPAN) [do2.c:116–128] |
| How is a link deleted? | `deletevspan` → `deletend` on the document orgl — hard removal, no hiding [orglinks.c:149] |
| Is there a granfilade "hidden" mark? | **No** — no such mechanism exists in the code |
| What happens to the link's own orgl on deletion? | It **persists** — only the document's Vstream reference is removed |
| Is BERT involved in link storage? | No — BERT is edit locking only [bert.c passim] |
