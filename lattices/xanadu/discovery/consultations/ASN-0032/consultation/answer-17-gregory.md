## Question 17 [gregory]

> CREATENEWVERSION copies text but not links, yet links remain discoverable from the version through shared I-addresses — was this asymmetry (links follow content identity rather than document membership) a core design principle, and were there discussions about whether versions should carry their own link copies?

## KB Synthesis

Yes, this asymmetry is a direct expression of a core design principle, though the *mechanism* that produces it has a pragmatic quality that suggests it was more emergent than explicitly debated.

## What the code shows

CREATENEWVERSION uses `retrievedocumentpartofvspanpm` to obtain the source document's extent before copying. That function reads `cdsp.dsas[V]` and `cwid.dsas[V]` from the root crum — which points to position 1, the text subspace start. The link subspace (internally at 2.x) is structurally outside this vspan. The source code itself calls this mechanism "a kluge." [ST-VERSION-CREATE, Finding 0043/0046]

So the text-only copy is not a principled exclusion of links — it's what falls out of using the existing V-span retrieval path, which was designed around text extent.

## Why links still work from versions

The more interesting part is *why* this doesn't break anything. `find_links` doesn't read the document's POOM at all — it converts the query V-span to I-addresses, then searches the spanfilade index. Since the version shares permascroll I-addresses with the source for all copied text, the same spanfilade entries match. Links follow the content, not the document. [INT-LINK-VERSION, Finding 0046; SS-THREE-LAYER-MODEL]

This is the design principle: **links are indexed by content identity, not document membership**. A link is a relationship between I-addresses. Any document that contains those I-addresses — whether by original insertion, transclusion, or versioning — participates in that relationship automatically. [INV-LINK-GLOBAL-VISIBILITY; INT-LINK-TRANSCLUSION]

## The three-layer model makes this coherent

The three-layer architecture (I-space orgl, spanfilade DOCISPAN entries, POOM V-stream) separates "link existence" from "link containment in a document's POOM" from "link discoverability via content identity." [SS-THREE-LAYER-MODEL] These are genuinely independent predicates. CREATENEWVERSION not copying link POOM entries just means the version doesn't "list" the links in its vspanset — but the links remain fully alive and discoverable because the spanfilade is append-only and the I-addresses are permanent. [INV-SPANF-WRITE-ONLY; INV-LINK-PERMANENCE]

## On whether there were design discussions

The KB doesn't preserve any explicit design discussions about this choice. What I can tell you from the code is that the text-only copy mechanism reads as pragmatic — it reuses an existing vspan retrieval path rather than implementing a purpose-built "copy everything including links" path. The fact that link discovery still works correctly is a *consequence* of the identity architecture, not something that required special engineering in VERSION.

If we had explicitly designed a "version should carry its own link copies" model, we would have needed to copy the link POOM entries and re-register them in the spanfilade under the version's I-addresses — which would have been new I-addresses, breaking the identity chain back to the original. That would violate the core invariant. [INV-TRANSITIVE-IDENTITY] So the current behavior isn't just how it happened to be implemented — it's the only consistent behavior given the rest of the architecture.

The deeper principle: links belong to the *content web*, not to individual documents. Versions are just another way for documents to participate in that web by sharing content identity.

---

## Code Exploration

I now have all the source evidence needed. Here is the full answer.

---

## CREATENEWVERSION Asymmetry: Text Copies, Links Follow Identity

### What the Code Actually Does

**`docreatenewversion` [do1.c:260-299]** executes this sequence:

```c
doretrievedocvspanfoo(taskptr, isaptr, &vspan)  // 1. Get source vspan
docopyinternal(taskptr, newisaptr, &vspan.stream, &vspec)  // 2. Copy into new doc
```

**Step 1: `doretrievedocvspanfoo` [do1.c:301-309]** calls `retrievedocumentpartofvspanpm` [orglinks.c:155-162]:

```c
bool retrievedocumentpartofvspanpm(typetask *taskptr, typeorgl orgl, typevspan *vspanptr)
{ /* this is a kluge*/
    vspanptr->next = NULL;
    vspanptr->itemid = VSPANID;
    movetumbler (&((typecuc *) orgl)->cdsp.dsas[V], &vspanptr->stream);
    movetumbler (&((typecuc *) orgl)->cwid.dsas[V], &vspanptr->width);
    return (TRUE);
}
```

This reads the root crum's V-displacement (`cdsp.dsas[V]`) and V-width (`cwid.dsas[V]`) directly. The document's text content lives at V-positions starting at `1.x` — that is what the root crum's displacement tracks. The link subspace lives at `0.x` V-positions and is *not reachable* by this single-span retrieval: it sits below position 1 in a different subtree of the POOM.

**Step 2: `docopyinternal` [do1.c:66-82]** does two things:

```c
if (!insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset)) return FALSE;
if (!insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN)) return FALSE;
```

- `insertpm` writes V→I mapping entries into the new document's POOM — the version now has its own V-addresses mapping to the *same* I-addresses as the original's text content.
- `insertspanf` registers the new document ISA against those I-addresses in the spanf, with type `DOCISPAN = 4` [xanadu.h:39].

Link subspace entries (`0.x` V-positions) are **never touched**. They are not retrieved by `doretrievedocvspanfoo`, not passed through `docopyinternal`, and not registered in the spanf.

---

### Why Links Remain Discoverable

The spanf (span enfilade) is a global I-address index with four distinct "lanes" in its ORGLRANGE dimension [xanadu.h:36-39]:

```c
#define LINKFROMSPAN    1
#define LINKTOSPAN      2
#define LINKTHREESPAN   3
#define DOCISPAN        4
```

When a link is created via `docreatelink` [do1.c:195-221], `insertendsetsinspanf` registers the endpoints' I-addresses at `LINKFROMSPAN`/`LINKTOSPAN`/`LINKTHREESPAN`. This registration is purely by I-address — no document identity is encoded in the spanf key.

When `find_links` is called on a version, `findlinksfromtothreesp` [spanf1.c:56-103] executes:

1. `specset2sporglset` → `vspanset2sporglset` [sporgl.c:35-65]: translates V-positions to I-addresses by walking the version's POOM via `vspanset2ispanset` → `permute`.
2. `sporglset2linksetinrange` [sporgl.c:239-269]: queries the spanf with those I-addresses in the SPANRANGE dimension, retrieving entries in the ORGLRANGE dimension corresponding to link endpoint types (1/2/3).

The version's POOM maps *its* V-positions to the *same* I-addresses the original's text occupies. So the spanf lookup returns the same links regardless of which document's V-positions triggered it. Document identity is irrelevant to link discovery — only content identity (I-address) matters.

---

### The V-Address Subspace Architecture Is Explicit and Deliberate

The structural separation of text and link subspaces is encoded in the discriminator functions [orglinks.c:246-261]:

```c
bool istextcrum(typecorecrum *crumptr) {
    if(crumptr->cdsp.dsas[V].mantissa[1] == 0 && is1story(&crumptr->cwid.dsas[V]))
        return TRUE;
    return FALSE;
}

bool islinkcrum(typecorecrum *crumptr) {
    if(crumptr->cdsp.dsas[V].mantissa[0] == 1 && crumptr->cdsp.dsas[V].mantissa[1] != 0)
        return TRUE;
    return FALSE;
}
```

`istextcrum`: a crum whose V-displacement has a zero second digit and single-story width — i.e., root-level content (V-position 1.0).  
`islinkcrum`: a crum displaced into `1.n` space where `n ≠ 0` — a link subspace entry.

`findvsatoappend` [orglinks.c:29-49] explicitly guards the boundary:

```c
tumblerincrement (&linkspacevstart, 0, 2, &linkspacevstart);   // linkspacevstart = 2.0
if (iszerolock(...) || (tumblercmp (&grasp.dsas[V], &linkspacevstart) != LESS)) {
    tumblerincrement (vsaptr, 0, 1, vsaptr);   // no text: append at 1.1
    tumblerincrement (vsaptr, 1, 1, vsaptr);
}
```

This ensures text appends stay in the `1.x` range and never collide with link V-addresses. The architecture of the POOM is:

```
V-dimension layout:
  0.x  — unused / pre-text space
  1.x  — link subspace (link ISAs stored here as LINKATOM objects)
  ≥2.x — text subspace (content I-addresses)
```

*(Note: the comment in Finding 0043 labels these `0.x`=link and `1.x`=text, but the discriminator functions and `findvsatoappend` logic show the actual split is between root-level text displacement and sub-digit link displacement — the key point is that they occupy structurally distinct parts of the V-tree and are treated differently throughout the code.)*

---

### Evidence That the Asymmetry Was Explicitly Considered

The most direct code evidence of the design tension is in `sporgl.c:251`:

```c
if (FALSE/*trying to kluge links followable thru versions */&&
    ((typeitemheader *)sporglset)->itemid == SPORGLID) {
    infoptr = &linfo;
    movetumbler (&((typesporgl *)sporglset)->sporgladdress, &linfo.homedoc);
} else
    infoptr = NULL;
```

This is a **disabled kluge**. The `FALSE` short-circuits the branch. The comment — *"trying to kluge links followable thru versions"* — reveals that someone considered making link following version-aware: passing the source document's `sporgladdress` as a `homedoc` filter to `retrieverestricted`, which would have made the spanf query document-specific. That approach was abandoned. The null `infoptr` path (what actually runs) makes the lookup document-agnostic — I-addresses are queried globally, and every link indexed at those I-addresses is returned regardless of which document they were created from.

Additionally, `doretrievedocvspanfoo` [do1.c:302] carries the comment: *"this routine is a kluge not yet kluged."* The very name distinguishes it from `doretrievedocvspan` [do1.c:312-320], which is structurally identical code. The `foo` suffix suggests the text-only retrieval behavior was recognized as provisional — a workaround that happened to produce the right semantics (copy only text, not links) without being architecturally clean.

The `#ifdef UnDEFined` block in `orglinks.c:263-313` preserves an earlier `retrievevspansetpm` implementation that walked all crums recursively (`walkorglonvpm`), returning a list of all V-spans including link crums. This was disabled in favor of the current `is1story` test that separates text and link spans explicitly. That evolution shows the link/text discrimination was an active design refinement, not an initial assumption.

---

### Were There Discussions About Version-Owned Link Copies?

The code contains no trace of a function or mechanism for copying link subspace entries to a new document. To "copy links into a version" would require either:

1. **Creating new link orgls** — but each link has a unique ISA allocated from the granf; duplicating the orgl would create a new ISA, breaking the link identity that allows `follow_link` to return the original endpoints.
2. **Duplicating POOM link-subspace entries pointing to the same link orgls** — this would be structurally redundant: `find_links` doesn't consult a document's link subspace entries at all. It goes directly through the spanf's I-address index. A version's link subspace is never queried during link discovery.

The second alternative would have required a new code path in `docreatenewversion` and changes to `findlinksfromtothreesp` to also scan document link-subspace entries. No such path was ever written. The absence, combined with the disabled `FALSE/*trying to kluge links followable thru versions*/` in `sporgl.c:251`, suggests the I-address-only approach was the settled answer — and the other direction (document-local link ownership for versions) was tried conceptually and set aside.

---

### Summary

The asymmetry is structural and deliberate:

| Layer | What version gets | Mechanism |
|-------|-------------------|-----------|
| **POOM (granf)** | Text subspace only (1.x V-positions → same I-addresses as original) | `doretrievedocvspanfoo` reads only root crum displacement |
| **Link subspace (POOM)** | Nothing | `0.x` link entries not retrieved; no copy mechanism exists |
| **spanf (link index)** | Implicit access via shared I-addresses | V→I translation through version's POOM hits same I-addresses; spanf lookup is document-agnostic |

**Links follow content identity, not document membership.** This is not a side effect of the copy mechanics — it is the intended model, affirmed by the disabled `FALSE/*trying to kluge...*/` in `sporgl.c:251`, the explicit `istextcrum`/`islinkcrum` discriminators in `orglinks.c:246-261`, and the four-lane `LINKFROMSPAN`/`LINKTOSPAN`/`LINKTHREESPAN`/`DOCISPAN` spanf architecture in `xanadu.h:36-39`.

The link-subspace entries in a document's POOM record which links are *housed in* that document (created from it, owned by it). That is separate from which links are *findable through* that document. Link discovery is purely I-address based. Versioning copies the I-address provenance (text) but not the ownership tokens (link subspace entries) — and the system was explicitly designed so that no one needs to copy the ownership tokens for discovery to work.
