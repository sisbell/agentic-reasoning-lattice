## Question 14 [gregory]

> Can a single endset span I-addresses originating from multiple documents (i.e., a source endset referencing content created in doc A and content created in doc B), or must each endset be confined to a single document's I-address range?

## KB Synthesis

A single endset can reference I-addresses originating from multiple documents. There is no confinement to a single document's I-address range.

The mechanism is documented in [ST-LINK-CREATE] / [SS-LINK-ENDPOINT] (Finding 0037). When `domakelink` receives a V-span that maps to non-contiguous I-addresses from multiple sources, `vspanset2sporglset` walks every I-span returned by `vspanset2ispanset` and creates a **separate sporgl per contiguous I-address region**. Each sporgl independently carries:

- `sporglorigin` — the I-address of that region
- `sporglwidth` — its width
- `sporgladdress` — the **document** where that content resides

So if content in document C consists of "AA" transcluded from A and "BB" transcluded from B, selecting that entire V-span as a link endpoint produces two sporgls in the endset: one pointing into A's permascroll range, one into B's. The endset type is `set<Sporgl>`, not `set<ISpan>` — provenance is per-sporgl, not per-endset [SS-SPORGL].

The cardinality rule from [SS-LINK-ENDPOINT]: `|Endset| >= |input_vspans|`. When the input V-span covers content from N distinct source documents (or N disjoint I-address regions), the endset contains at least N sporgls.

This is also why [EC-LINK-PARTIAL-SURVIVAL] holds: if document A is deleted but document B survives, the endset retains the B-originated sporgl intact while the A-originated sporgl becomes unresolvable. Partial survival is per-sporgl.

The constraint that does exist is the inverse: each **sporgl** within an endset is confined to a single contiguous I-address region from a single document. Multi-document I-address mixing within one sporgl is structurally impossible — a sporgl has exactly one `sporgladdress`.

---

## Code Exploration

Now I have everything I need to answer comprehensively. Here is my analysis:

---

## Can a Single Endset Reference I-Addresses From Multiple Documents?

**Yes.** The code imposes no restriction confining an endset to a single document's I-address range. The architecture explicitly supports multi-document endsets at every level.

---

### 1. The Data Type Is Already Multi-Document

The `typespecset` type is a **linked list of `typespec`**, and each `typespec` is either:

```c
// xanadu.h:78-89
typedef struct structtypevspec {
    struct structtypevspec *next;
    typeitemid itemid;
    typeisa docisa;          // ← document-specific ISA
    typevspanset vspanset;   // ← V-spans within that document
} typevspec;

typedef union {
    typevspec xxxvspec;
    typeispan xxxispan;
} typespec;
typedef typespec * typespecset;
```

A `typespecset` passed as a from/to/three endset to `docreatelink` [do1.c:195] can therefore be a list of `typevspec` nodes each with a **distinct `docisa`**. Nothing in the type prevents it.

---

### 2. Link Creation Iterates the Entire Multi-Document Specset

In `docreatelink` [do1.c:195-221], for each endset:

```c
specset2sporglset(taskptr, fromspecset, &fromsporglset, NOBERTREQUIRED)
```

`specset2sporglset` [sporgl.c:14-33] loops over every element:

```c
for (; specset; specset = (typespecset)((typeitemheader*)specset)->next) {
    if (((typeitemheader *)specset)->itemid == VSPECID) {
        sporglsetptr = vspanset2sporglset(taskptr,
            &((typevspec *)specset)->docisa,   // ← each element's own docisa
            ((typevspec *)specset)->vspanset,
            sporglsetptr, type);
    }
}
```

For each `typevspec`, `vspanset2sporglset` [sporgl.c:35-65] looks up the ORGL for *that document*, translates its V-spans to I-spans, and creates `typesporgl` entries:

```c
sporglset->sporgladdress = *docisa;  // source document for this I-span
sporglset->sporglorigin  = ispanset->stream;
sporglset->sporglwidth   = ispanset->width;
```

So the output `fromsporglset` is a **flat linked list whose entries may carry different `sporgladdress` values** if the input specset referenced multiple documents. No filtering, no validation, no error.

---

### 3. Insertion Into the Spanfilade Processes Each Sporgl Independently

`insertendsetsinspanf` [do2.c:116-128] calls `insertspanf` per endset type. Inside `insertspanf` [spanf1.c:15-54]:

```c
for (; sporglset; sporglset = ...) {
    if (itemid == SPORGLID) {
        movetumbler(&sporglset->sporglorigin,  &lstream);
        movetumbler(&sporglset->sporglwidth,   &lwidth);
        movetumbler(&sporglset->sporgladdress, &linfo.homedoc);  // per-entry doc
    }
    ...
    insertnd(taskptr, (typecuc*)spanfptr, &crumorigin, &crumwidth, &linfo, SPANRANGE);
}
```

Each sporgl is inserted into the spanfilade with its own `homedoc`. The enfilade crum for a span from Doc A carries Doc A's ISA as `homedoc`; a span from Doc B carries Doc B's ISA. They are stored as separate crums because `isanextensionnd` [insertnd.c:301-309] requires matching `homedoc` before merging adjacent crums:

```c
bool isanextensionnd(typecbc *ptr, typedsp *offsetptr, typedsp *originptr,
                     type2dbottomcruminfo *infoptr)
{
    if (!tumblereq(&infoptr->homedoc, &((type2dcbc *)ptr)->c2dinfo.homedoc))
        return (FALSE);   // ← different doc = never merged, but never rejected
    ...
}
```

Critically: **different-doc crums are rejected from merging but are never rejected from insertion**. They simply live in the spanfilade as separate crums.

---

### 4. Insertion Into the Link's Own POOM Also Accepts Multi-Document Sporgls

`insertendsetsinorgl` [do2.c:130-149] calls `insertpm` [orglinks.c:75-134] for each endset. Inside `insertpm`:

```c
for (; sporglset; sporglset = ...) {
    unpacksporgl(sporglset, &lstream, &lwidth, &linfo);
    // linfo.homedoc = sporglset->sporgladdress (per-entry doc)
    ...
    insertnd(taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);
    tumbleradd(vsaptr, &crumwidth.dsas[V], vsaptr);
}
```

`unpacksporgl` [sporgl.c:178-203] sets `infoptr->homedoc` from each sporgl's `sporgladdress`. Each I-span from each source document gets its own V-address slot in the link's POOM, tagged with that document's ISA. No single-document constraint is checked.

---

### 5. Retrieval Also Handles Multi-Document Endsets

When `dofollowlink` [do1.c:223] or `doretrieveendsets` [do1.c:369] reconstructs an endset, `link2sporglset` [sporgl.c:67-95] retrieves the sporgl list from the link's POOM. `linksporglset2specset` [sporgl.c:97-122] then calls `linksporglset2vspec` → `sporglset2vspanset` [sporgl.c:141-176], which groups consecutive sporgls by matching `sporgladdress`:

```c
if (!tumblereq(&((typesporgl *)sporglptr)->sporgladdress,
               &((typesporgl *)(*sporglsetptr))->sporgladdress))
    return(0);  // stop this vspec group, new document begins
```

Different-document sporgls are recovered as **separate `typevspec` entries** in the returned `typespecset` — one per source document. The reconstructed endset is a multi-element specset, exactly parallel to what was inserted.

---

### Summary

| Stage | File | Lines | Behavior |
|---|---|---|---|
| Type definition | `xanadu.h` | 78-89 | `typespecset` is a linked list; each `typevspec` carries its own `docisa` |
| Specset → sporglset | `sporgl.c` | 14-33 | Iterates all specset elements; calls `vspanset2sporglset` per element with its own `docisa` |
| Sporgl carries doc ISA | `sporgl.c` | 35-65 | Each `typesporgl.sporgladdress` = source document |
| Spanfilade insert | `spanf1.c` | 25-51 | Each sporgl inserted with its own `linfo.homedoc`; no cross-document validation |
| Crum extension check | `insertnd.c` | 301-309 | Different-doc spans not merged, but also **not rejected** |
| Link POOM insert | `orglinks.c` | 100-131 | Each sporgl inserted independently with its own `homedoc` |
| Follow/retrieve | `sporgl.c` | 141-176 | Consecutive same-doc sporgls group into one `typevspec`; doc boundary stops the group |

**A single endset (from, to, or three) can reference I-addresses originating in multiple documents.** The `typespecset` input is a linked list of per-document specs; `specset2sporglset` expands them all into a flat sporglset; and both the spanfilade and the link's POOM store each resulting I-span tagged with its source document's ISA. No validation anywhere in the pipeline enforces single-document confinement. On retrieval, the spans are reconstituted as a multi-element specset, one `typevspec` per source document.
