## Question 17 [gregory]

> In the original multi-node design intent, was each node expected to carry a complete copy of its own content in its local granfilade, or could a node hold granfilade entries for content originating from other nodes (e.g., after a transclusion from a remote document)?

## KB Synthesis

The KB cannot answer this question. The knowledge base documents the single-node udanax-green implementation and does not contain findings about the multi-node design intent for content distribution or granfilade replication policy.

What the KB does establish that bears on this question:

**Address structure implies node-scoped I-addresses.** Tumbler addresses follow the pattern `Node.0.User.0.Doc.0.Element` [SS-TUMBLER, Finding 0001]. Permascroll I-addresses in the observed system start with `2.1.0.x...`, distinct from document orgl addresses under `1.1.0.x...`. The addressing scheme is hierarchical, but the KB does not explain whether the leading digits of I-addresses encode node identity such that a remote I-address would be distinguishable from a local one.

**The granfilade holds all content for the running node.** The granfilade stores the permascroll, all document orgls, link orgls, and V→I mappings in a single `enf.enf` file [SS-UNIFIED-STORAGE, Finding 0059]. There is no mechanism in the KB for fetching content from a remote granfilade — all I-address resolution (`findorgl`, `retrieverestricted`, `ispanset2vstuffset`) assumes content is locally present.

**I-address allocation is local and stateless.** `findisatoinsertmolecule` queries the local granfilade tree to find the highest existing I-address and increments [SS-ADDRESS-SPACE, Finding 0061]. There is no inter-node coordination in the allocation path.

**Transclusion assumes local content.** `docopy` [SS-DUAL-ENFILADE, Finding 0012] places I-spans directly into the destination document's POOM. Whether those I-addresses could reference content held on a remote node's granfilade — and whether the receiving node would cache a copy locally — is not addressed anywhere in the KB.

If you have EWD papers or Nelson's design documents describing the multi-node distribution model, those would be the right source. The KB only captures what the udanax-green C source demonstrates about the single-daemon implementation.

---

## Code Exploration

Now I have enough to compose a definitive answer from the code.

---

## Multi-Node Content in Udanax-Green: What the Code Actually Shows

The answer is **yes — a node's spanfilade and POOM could hold entries for content originating from other documents, potentially on other nodes.** The design is explicit and deliberate. Here is the evidence.

---

### 1. The SPORGL Item Type Is the Cross-Document Reference

`xanadu.h:115–121` defines the critical struct:

```c
typedef struct structsporgl{
    struct structsporgl *next;
    typeitemid  itemid;
    tumbler sporglorigin;   // where in I-space the transcluded content starts
    tumbler sporglwidth;    // how wide it is
    typeisa sporgladdress;  // the ISA of the source (home) document
} typesporgl;
```

A SPORGL is not local text. It is a pointer into another document's I-space, carrying the address of the source document in `sporgladdress`. A `typesporglset` (xanadu.h:127) is a heterogeneous list that can mix local `ISPANID` items and cross-document `SPORGLID` items.

---

### 2. Every 2D Crum Records Its Home Document

`wisp.h:107–109`:

```c
typedef struct struct2dbottomcruminfo {
    tumbler homedoc;
} type2dbottomcruminfo;
```

Every bottom-level crum in a spanfilade or POOM carries a `homedoc` tumbler. This is the provenance stamp: the ISA of the document that owns this particular content entry.

---

### 3. `insertspanf` Writes Cross-Document Provenance at Insertion Time

`spanf1.c:25–51` processes a `sporglset` and writes crums into the span file. The `homedoc` field is set based on item type:

```c
if (((typeitemheader *)sporglset)->itemid == ISPANID) {
    movetumbler (&((typeispan *)sporglset)->stream, &lstream);
    movetumbler (&((typeispan *)sporglset)->width, &lwidth);
    movetumbler (isaptr, &linfo.homedoc);            // local doc
} else if (((typeitemheader *)sporglset)->itemid == SPORGLID) {
    movetumbler (&((typesporgl *)sporglset)->sporglorigin, &lstream);
    movetumbler (&((typesporgl *)sporglset)->sporglwidth, &lwidth);
    movetumbler (&((typesporgl *)sporglset)->sporgladdress, &linfo.homedoc); // REMOTE doc
} else if (((typeitemheader *)sporglset)->itemid == TEXTID) {
    movetumbler(isaptr, &lstream);
    // ... width from length ...
    movetumbler(isaptr, &linfo.homedoc);             // local doc
}
insertnd(taskptr, (typecuc*)spanfptr, &crumorigin, &crumwidth, &linfo, SPANRANGE);
```

When the item is a SPORGL, `linfo.homedoc` is set to `sporgladdress` — the remote document's ISA — not the inserting document's ISA. That remote-provenance crum is then inserted into the local spanfilade via `insertnd`. The span file on this node now contains an entry whose `homedoc` points to a foreign document.

`unpacksporgl` (sporgl.c:187) confirms this is the intent: the comment reads `/* should be sourcedoc */`.

---

### 4. `isanextensionnd` Enforces Same-Origin Merging

`insertnd.c:301–309`:

```c
bool isanextensionnd(typecbc *ptr, typedsp *offsetptr, typedsp *originptr, type2dbottomcruminfo *infoptr)
{
    if (!tumblereq (&infoptr->homedoc, &((type2dcbc *)ptr)->c2dinfo.homedoc))
        return (FALSE);
    prologuend ((typecorecrum*)ptr, offsetptr, &grasp, &reach);
    return (lockeq (reach.dsas, originptr->dsas, (unsigned)dspsize(ptr->cenftype)));
}
```

Before the enfilade merges a new crum with an existing adjacent one, it checks that the two share the same `homedoc`. If the home documents differ (line 305), merge is refused and a new crum is created. This guarantees that content from different source documents remains **physically separated** in the tree, even when adjacent — but it is not forbidden from coexisting in the same enfilade.

---

### 5. Retrieval Filters by `homedoc` Across a Mixed Span File

`retrie.c:77–84` sets up the filter for a retrieval:

```c
if (docisaptr) {
    movetumbler(docisaptr, &info.homedoc /*shouldberestrictiondoc*/);
    infoptr = &info;
} else {
    infoptr = NULL;
}
temp = retrieveinarea(fullcrumptr, ...., (typebottomcruminfo*)infoptr);
```

`crumqualifies2d` (retrie.c:274–280) enforces it at the leaf level:

```c
if ((crumptr->height == 0) && infoptr && 
    !tumblereq(&infoptr->homedoc, &(((type2dcbc *)crumptr)->c2dinfo.homedoc))) {
    fprintf(stderr,"mumble homedoc");
    return (FALSE);
}
```

When `docisaptr` is provided, only crums whose `homedoc` matches are returned. When it is NULL, all crums — regardless of origin — are returned. The filter exists precisely *because* the span file is expected to contain entries from multiple source documents mixed together.

---

### 6. The Granfilade Itself Is Local; The Mapping Layers Are Not

There is an important distinction between the three enfilade layers:

- **Granfilade** (`granf2.c:83–109`): Stores actual byte content. `inserttextgr` allocates ISAs within the local hierarchy using `findisatoinsertgr`. The granfilade holds the raw bytes of locally-authored text. There is no `homedoc` on granfilade crums — they use `typegranbottomcruminfo`, which has no provenance field (`wisp.h:100–104`).

- **Spanfilade** and **POOM** (orglinks.c, spanf1.c): These are the *address-mapping* layers. They map virtual span addresses to I-space (granfilade) addresses. It is here that `type2dbottomcruminfo` with `homedoc` appears. These layers can and do hold entries referencing remote documents.

The granfilade belongs to a node; the spanfilade and POOM record how that node's documents are composed — including from remote sources.

---

### 7. `insertpm` Stores Cross-Document Mappings in the POOM

`orglinks.c:75–134`: `insertpm` drives POOM insertion. It calls `unpacksporgl` to extract `lstream`, `lwidth`, and `linfo` (with `linfo.homedoc` = source doc for SPORGLs), then calls `insertnd` with that info. For SPORGL items the POOM entry records a V→I mapping where the I-address belongs to a foreign document.

---

### Summary

| Layer | Contains remote content? | Evidence |
|---|---|---|
| Granfilade | No — byte storage is always local | `typegranbottomcruminfo` has no `homedoc` |
| Spanfilade | **Yes** — crums with remote `homedoc` are inserted | `spanf1.c:33`, `unpacksporgl` sporgl.c:187 |
| POOM | **Yes** — V→I mappings can point into remote I-space | `orglinks.c:101`, `insertpm` drives it |

The design is unambiguous: each node owns its own granfilade (raw text bytes are stored locally) but its spanfilade and POOM are explicitly designed to hold entries for content originating in any document — including documents on remote nodes — identified by the `sporgladdress` / `homedoc` tumbler. The `isanextensionnd` check (insertnd.c:305) and `crumqualifies2d` filter (retrie.c:274) are both *consequences* of this design: they exist to keep foreign-provenance crums from merging with local ones and to allow retrieval scoped to a single home document within the mixed tree. Transclusion from a remote node would produce exactly these cross-provenance crums, and the code is fully prepared to store and retrieve them.
