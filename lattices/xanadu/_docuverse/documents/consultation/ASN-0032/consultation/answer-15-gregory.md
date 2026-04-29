## Question 15 [gregory]

> Can a single link endset legitimately reference content from multiple different documents (e.g., source endset contains I-spans from doc A and doc B), and if so, what is the intended semantic — does such a link assert a relationship across a composite selection?

## KB Synthesis

Yes, a single link endset can legitimately reference content from multiple different documents. This is a direct, automatic consequence of transclusion composing content from multiple sources.

**The mechanism** [SS-LINK-ENDPOINT, Finding 0037]:

When `domakelink` receives a V-span covering content transcluded from multiple sources, `vspanset2sporglset` converts the span to I-spans by walking the POOM. Because transcluded content from different documents occupies non-contiguous I-address regions (from different permascroll allocations), the conversion produces one sporgl per contiguous I-address region. Each sporgl carries its own `sporglorigin`, `sporglwidth`, and `sporgladdress` (source document ISA). The front end does not need to pre-split — the decomposition is automatic.

**Concrete example** [ST-LINK-CREATE, Finding 0037]:

```
Document C contains "AABB" at V 1.1..1.4 where:
  "AA" was transcluded from document A (I-addresses from A's permascroll)
  "BB" was transcluded from document B (I-addresses from B's permascroll)

create_link(source = V-span 1.1 width 0.4 in doc C, ...)

Input:  1 V-span covering "AABB"
Output: 2 sporgls in source endset:
  sporgl₁: origin = iaddr(A,"AA"), width = 0.2, doc = C
  sporgl₂: origin = iaddr(B,"BB"), width = 0.2, doc = C
```

**The semantic** [SS-SPORGL, Finding 0013; SS-LINK-ENDPOINT, Finding 0004]:

The link treats the entire V-span selection as a single composite endpoint — it asserts a relationship against the union of all content identities in that selection, across all their provenance origins. The `sporgladdress` field records which document each piece came from, but the link binds to the I-addresses themselves, not the document positions. This is consistent with the broader model: link endpoints are content identity references, not positional references.

**Partial survival** [EC-LINK-PARTIAL-SURVIVAL]:

Because each sporgl in the endset independently tracks its content, the multi-document structure has a concrete behavioral consequence: if document A's content is deleted, the endset retains the sporgl for B's content. The link partially survives — `follow_link` returns only the surviving B-derived portion [INV-LINK-CONTENT-TRACKING].

**Summary**: A multi-document endset is the normal outcome whenever a link is placed on composite (transcluded) content. The semantic is that the link binds to all constituent content identities as a single endpoint, spanning their multiple origins. There is no restriction or special treatment — the system handles it transparently via the sporgl mechanism.

---

## Code Exploration

Now I have everything I need to give a complete, code-grounded answer.

---

## Can a Single Link Endset Reference Content from Multiple Documents?

**Yes — architecturally, yes. Operationally, yes with a caveat at retrieval.**

Here is the full trace.

---

### 1. The Data Model

Each link has three endsets: `from`, `to`, and `three`. Internally, an endset is stored as a linked list of `typesporgl` structs. The critical field is `sporgladdress`:

```c
// xanadu.h — typesporgl
typedef struct structsporgl {
    struct structsporgl *next;
    typeitemid      itemid;
    tumbler sporglorigin;   // I-span start (position in permascroll)
    tumbler sporglwidth;    // I-span width
    typeisa sporgladdress;  // The document this I-span belongs to
} typesporgl;
```

`sporgladdress` is a per-sporgl document ISA. It is not a property of the endset as a whole — it is per-element. The architecture explicitly provides a per-span document reference. This is the foundation for multi-document endsets.

---

### 2. Creation Path — No Cross-Document Constraint

`docreatelink` [do1.c:195-221] calls `specset2sporglset` for each endset:

```c
// do1.c:214-216
&& specset2sporglset (taskptr, fromspecset, &fromsporglset, NOBERTREQUIRED)
&& specset2sporglset (taskptr, tospecset,   &tosporglset,   NOBERTREQUIRED)
&& specset2sporglset (taskptr, threespecset, &threesporglset, NOBERTREQUIRED)
```

`specset2sporglset` [sporgl.c:14-33] iterates through the entire input specset, which is a linked list of items. Each `VSPECID` item has its own `docisa` field:

```c
// sporgl.c:19-28
for (; specset; specset = (typespecset)((typeitemheader*)specset)->next) {
    if (((typeitemheader *)specset)->itemid == ISPANID) {
        *sporglsetptr = (typesporglset)specset;
        ...
    } else if (((typeitemheader *)specset)->itemid == VSPECID) {
        if (!(sporglsetptr = vspanset2sporglset (taskptr,
            &((typevspec *)specset)->docisa,   // ← each vspec has its OWN docisa
            ((typevspec *)specset)->vspanset,
            sporglsetptr, type))) {
            return (FALSE);
        }
    }
}
```

A caller can pass a specset with multiple `VSPECID` items, each with a different `docisa`. There is **no check** anywhere in `specset2sporglset`, `vspanset2sporglset`, `insertendsetsinorgl` [do2.c:130-149], or `insertpm` [orglinks.c:75-134] that enforces same-document membership within an endset.

`vspanset2sporglset` [sporgl.c:35-65] faithfully records the source document in every sporgl it creates:

```c
// sporgl.c:53
movetumbler (docisa, &sporglset->sporgladdress);   // source doc stored per-sporgl
```

So **at creation time, a multi-document endset is accepted without complaint.**

---

### 3. Storage — Correct

`insertpm` [orglinks.c:100-131] iterates the sporglset and inserts each item into the link's orgl (POOM enfilade). It calls `unpacksporgl` which reads `sporgladdress` into `linfo.homedoc`:

```c
// sporgl.c:187
movetumbler (&((typesporgl *)sporglptr)->sporgladdress, &infoptr->homedoc);
```

`insertnd` then stores `linfo` in the crum's bottom-level info. Each crum in the link's enfilade carries its source document address. A multi-document endset produces correctly-labeled crums.

`insertspanf` [spanf1.c:15-54] — which indexes the endset into the spanfilade for link-lookup — also correctly stores per-sporgl addresses:

```c
// spanf1.c:33
movetumbler (&((typesporgl *)sporglset)->sporgladdress, &linfo.homedoc);  // correct
```

**Storage is faithful. Multi-document endsets are stored correctly at the crum level.**

---

### 4. Retrieval — Partially Broken for Multi-Document Endsets

`dofollowlink` [do1.c:223-232]:

```c
bool dofollowlink(typetask *taskptr, typeisa *linkisaptr, typespecset *specsetptr, INT whichend)
{
    typesporglset sporglset;
    return (
       link2sporglset (taskptr, linkisaptr, &sporglset, whichend, NOBERTREQUIRED)
    && linksporglset2specset (taskptr,
           &((typesporgl *)sporglset)->sporgladdress,   // ← FIRST sporgl's address only
           sporglset, specsetptr, NOBERTREQUIRED));
}
```

`link2sporglset` [sporgl.c:67-95] retrieves all sporgls from the endset via `contextintosporgl`, which correctly restores each sporgl's own `sporgladdress` from the crum's `homedoc`. So the sporglset coming out of `link2sporglset` is correct.

Then `linksporglset2specset` [sporgl.c:97-123] passes control to `linksporglset2vspec` [sporgl.c:127-137]:

```c
int linksporglset2vspec(typetask *taskptr, typeisa *homedoc, typesporglset *sporglsetptr,
                        typevspec *specptr, int type)
{
    specptr->itemid = VSPECID;
    specptr->next = NULL;
    movetumbler (homedoc/*&sporglset->sporgladdress*/, &specptr->docisa);  // LINE 134
    specptr->vspanset = NULL;
    sporglset2vspanset (taskptr, homedoc, sporglsetptr, &specptr->vspanset, type);
}
```

**Line 134 is the smoking gun.** The comment `/*&sporglset->sporgladdress*/` preserves the original intent: use each sporgl's own document address. The working code substitutes `homedoc` — the first sporgl's address passed in from `dofollowlink` — for all sporgls.

`sporglset2vspanset` [sporgl.c:141-176] compounds this: it calls `findorgl` with `homedoc` [line 152], and its inner loop [line 163] terminates as soon as a sporgl with a different `sporgladdress` is encountered:

```c
// sporgl.c:163
|| !tumblereq (&((typesporgl *)sporglptr)->sporgladdress,
               &((typesporgl *)(*sporglsetptr))->sporgladdress))
    return(0);   // stops at first sporgl from a different document
```

**Effect:** When following a link whose endset spans documents A and B, only the portion from document A (whichever happened to be first in the sporglset) is returned. The content from document B is silently dropped.

`retrieveendsetsfromspanf` [spanf1.c:190-235] — the alternative retrieval path — exhibits the same defect:

```c
// spanf1.c:224
&& linksporglset2specset (taskptr, &((typevspec *)specset)->docisa, fromsporglset, fromsetptr, NOBERTREQUIRED)
```

Here `homedoc` is the link's own document ISA rather than the first sporgl's address — equally wrong for multi-document endsets.

---

### 5. Intended Semantic

The architecture answers this directly through the data model. The `sporgladdress` field exists precisely to make endsets document-independent. An endset is not "content from document X" — it is "these I-spans, which happen to live in these documents." The I-span (permascroll address) is the primary identity; the document is secondary metadata needed to translate back to V-space.

The intended semantic of a multi-document endset is: **the link asserts a relationship across a composite selection drawn from multiple documents simultaneously.** The endpoint is not "some text in doc A" or "some text in doc B" — it is "this composite span of docuverse material, which happens to be transcluded into multiple documents." This is the core Xanadu model: links and transclusion operate on permanent, document-neutral I-addresses.

A link from {doc A para 1, doc B para 3} to {doc C section 2} would mean: the relationship holds between the combined selection of that paragraph and that passage on one side, and the section on the other. Useful for, e.g., linking two separately-sourced quotes that together support a claim.

---

### 6. Summary

| Layer | Multi-doc endset behavior |
|-------|--------------------------|
| API input | Accepted without restriction |
| `specset2sporglset` [sporgl.c:14] | Correctly converts each V-spec with its own `docisa` |
| `vspanset2sporglset` [sporgl.c:53] | Correctly stores source doc in each `sporgladdress` |
| `insertpm` / `insertnd` | Correctly stores `homedoc` per-crum |
| `insertspanf` [spanf1.c:33] | Correctly indexes by per-sporgl source doc |
| `link2sporglset` [sporgl.c:86] | Correctly reconstructs per-sporgl addresses via `contextintosporgl` |
| `linksporglset2vspec` [sporgl.c:134] | **Bug: uses first doc's address for all sporgls** |
| `sporglset2vspanset` [sporgl.c:163] | **Bug: stops at first cross-document sporgl** |

**Conclusion:** Multi-document endsets are legitimate by design — the `sporgladdress` field is the architectural provision for exactly this case. The intended semantic is a cross-docuverse composite selection: one link endpoint covers material from multiple documents as a unified whole. The implementation correctly stores such endsets, but the retrieval path in `linksporglset2vspec` [sporgl.c:134] and `sporglset2vspanset` [sporgl.c:152, 163] is broken — the commented-out `&sporglset->sporgladdress` code was replaced with a single `homedoc` reference, causing only the first document's content to be returned when following such a link.
