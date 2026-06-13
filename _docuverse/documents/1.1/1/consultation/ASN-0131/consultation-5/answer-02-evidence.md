## Question 2 [evidence]

> What is the structural form of the conventional retraction type address in udanax-green's nullification mechanism — does it sit at an element-level address in a dedicated non-content subspace, so that `coverage(R) ∩ dom(Σ.C) = ∅` holds structurally rather than by convention?

## KB Synthesis

The KB does not contain documentation of any "nullification mechanism" or "retraction type" as named features of udanax-green. I cannot answer this question from the available knowledge base.

What the KB does establish that is most relevant to your structural question:

**Type addresses live in content space, not a separate subspace.** Link types are stored as VSpec references into the bootstrap document at `1.0.2.x` addresses [SS-LINK-ENDPOINT, Finding 0024 — JUMP at `1.0.2.2`, QUOTE at `1.0.2.3`, FOOTNOTE at `1.0.2.6`, MARGIN at `1.0.2.6.2`]. These are element-level I-addresses inside the permascroll/granfilade — they are within `dom(Σ.C)`, not disjoint from it. A retraction type, if it existed as a link type, would follow the same pattern and its coverage would intersect `dom(Σ.C)`.

**The three-subspace V-model provides structural separation only in V-space.** Mantissa[0] values 1 (text), 2 (link), 3 (type endpoint) carve out disjoint V-subspaces within a document [SS-SUBSPACE-CONVENTION, Finding 0038]. INSERT's two-blade knife [SS-TWO-BLADE-KNIFE] enforces subspace isolation structurally for INSERTs. However, this is a document-local V-space partition, not an I-space or global address-space separation.

**The subspace convention is caller-enforced, not storage-enforced.** `acceptablevsa()` is a no-op [SS-SUBSPACE-CONVENTION, Finding 0010], so `coverage(R) ∩ dom(Σ.C) = ∅` holding "structurally rather than by convention" does not describe the actual enforcement model for any subspace in the system.

If you have a specific code path or protocol opcode in mind for the nullification mechanism, I can check whether it appears under a different name in the KB.

---

## Code Exploration

I now have everything I need to answer the question with precise code citations. Here is the complete analysis:

---

## Answer

### 1. No Nullification Mechanism Exists in udanax-green

A search across all `.c`, `.h`, `.md`, and `.py` files finds zero occurrences of "nullif", "retract", "notype", or any dedicated retraction operation. The system provides two mechanisms that together approximate nullification:

- **Permanent structural deletion** via `deletevspan` → `dodeletevspan` (`do1.c:158–167`) → `deletevspanpm` (`orglinks.c:145–152`) → `deletend` (`edit.c:31–76`). This permanently removes content from the permutation matrix; no retraction marker is left behind.
- **Version history** via BERT (`logbertmodified`, called from `orglinks.c:99`, `orglinks.c:140`, `orglinks.c:150`). Prior states survive as reachable versions, but with no explicit retraction address.

There is no "nullification mechanism" in the sense the question implies. What follows traces what WOULD happen if a retraction were expressed as a conventional three-ended link.

---

### 2. The V-Space Is Split Into Two Structurally Separated Subspaces

A document's permutation matrix (POOM/orgl) partitions its V-address space into exactly two regions:

**Text subspace `[1.x, 2.0)`** — text content starts here. From `findvsatoappend` (`orglinks.c:36–43`):

```c
tumblerclear (&linkspacevstart);
tumblerincrement (&linkspacevstart, 0, 2, &linkspacevstart);  // linkspacevstart = {mantissa[0]=2}
// ...
tumblerincrement (vsaptr, 0, 1, vsaptr);  /* no text in doc */
tumblerincrement (vsaptr, 1, 1, vsaptr);  // first text slot = 1.1
```

The guard at `orglinks.c:41` (`tumblercmp(&grasp.dsas[V], &linkspacevstart) != LESS`) ensures text VSA stays strictly below V=2. Confirmed by `filter_vspanset_to_text_subspace` (`do1.c:393–395`):

```c
tumblerincrement(&text_subspace_start, 0, 1, &text_subspace_start);
// text_subspace_start = {mantissa[0]=1}
// keeps only V >= 1
```

**Link subspace `[2.x, ∞)`** — link references start here. From `findnextlinkvsa` (`do2.c:156–158`):

```c
tumblerclear (&firstlink);
tumblerincrement (&firstlink, 0, 2, &firstlink);  // mantissa[0] = 2
tumblerincrement (&firstlink, 1, 1, &firstlink);  // mantissa[1] = 1 → firstlink = 2.1
```

This is the floor for any link reference placed into a document's POOM via `docopy` (`do1.c:212`). The critical comment in `do1.c:377–384`:

```c
/* Bug 009 SEMANTIC FIX: Filter vspanset to text subspace only (V >= 1.0).
 * Link references at V-position 0.x are document metadata, not
 * transcludable content. They have unique ISAs, not permascroll addresses,
 * so comparing them is semantically undefined.
 */
```

Finding 0038 (POOM Subspace Independence) confirms this split behaviorally: INSERT and DELETE operations in `1.x` do not shift V-positions in `2.x`, because the POOM tree is partitioned — there is no shared displacement path between the two regions.

The enfilade predicates codify the split. From `orglinks.c:246–261`:

```c
bool istextcrum(typecorecrum *crumptr)
{
    if(crumptr->cdsp.dsas[V].mantissa[1] == 0  && is1story(&crumptr->cwid.dsas[V])){
        return TRUE;  // single-story span in text position
    }
    return FALSE;
}

bool islinkcrum(typecorecrum *crumptr)
{
    // "if the whole crum is displaced into link space it is a link crum
    //  this is true if the tumbler is a 1.n tumbler where n!= 0"
    if(crumptr->cdsp.dsas[V].mantissa[0] == 1 && crumptr->cdsp.dsas[V].mantissa[1] != 0){
        return TRUE;
    }
    return FALSE;
}
```

The two predicates are mutually exclusive by construction: `istextcrum` requires `mantissa[1]==0`; `islinkcrum` requires `mantissa[1]!=0`. A crum cannot be both.

---

### 3. The "Type" Endpoint (Three-End) Is a Third Independent Subspace — But in the Link's Own Orgl

When a link is created (`docreatelink`, `do1.c:195–221`), the link gets its own orgl with three V-ranges assigned by `setlinkvsas` (`do2.c:169–183`):

```c
bool setlinkvsas(tumbler *fromvsaptr, tumbler *tovsaptr, tumbler *threevsaptr)
{
    tumblerincrement (fromvsaptr, 0, 1, fromvsaptr);   // from  → V = 1.1
    tumblerincrement (fromvsaptr, 1, 1, fromvsaptr);
    tumblerincrement (tovsaptr,   0, 2, tovsaptr);     // to    → V = 2.1
    tumblerincrement (tovsaptr,   1, 1, tovsaptr);
    if (threevsaptr) {
        tumblerincrement (threevsaptr, 0, 3, threevsaptr); // three → V = 3.1
        tumblerincrement (threevsaptr, 1, 1, threevsaptr);
    }
    return (TRUE);
}
```

In the link's own orgl: from-endpoint at V∈[1,2), to-endpoint at V∈[2,3), type-endpoint at V∈[3,4). These are read back by `link2sporglset` (`sporgl.c:67–95`):

```c
tumblerincrement (&zero, 0, whichend, &vspan.stream);  // whichend = 1|2|3
tumblerincrement (&zero, 0, 1,        &vspan.width);   // width = 1
```

With `LINK_SOURCE=1, LINK_TARGET=2, LINK_TYPE=3` (`client.py:595`).

The TYPE endpoint's CONTENT — whatever VSpec you supply as the "type" — is a VSpec pointing into some designated type document. From `client.py:597–608`:

```python
# Link type addresses - types are in document 1's link subspace (0.2)
# Local address within doc: version.0.link_subspace.type = 1.0.2.X
JUMP_TYPE    = VSpec(LINK_TYPES_DOC, [Span(Address(1, 0, 2, 2), Offset(0, 1))])
QUOTE_TYPE   = VSpec(LINK_TYPES_DOC, [Span(Address(1, 0, 2, 3), Offset(0, 1))])
FOOTNOTE_TYPE= VSpec(LINK_TYPES_DOC, [Span(Address(1, 0, 2, 6), Offset(0, 1))])
```

The address `Address(1, 0, 2, 2)` = `version=1, sep=0, subspace=2, element=2`. The `2` in the third component is the link subspace field (first digit of the element field), not the text subspace field (`1`). A "retraction type" would have the same format: `Address(1, 0, 2, RETRACTION_N)`.

---

### 4. Does `coverage(R) ∩ dom(Σ.C) = ∅` Hold Structurally or by Convention?

There are two places where this needs to hold:

**In the host document's POOM:** The retraction link REFERENCE is stored at V∈[2.x] (link subspace) by `findnextlinkvsa`. The host document's text content occupies V∈[1.x] (text subspace). The two ranges are disjoint by the `linkspacevstart=2` guard in `findvsatoappend` (`orglinks.c:37,41`). This is enforced by code logic, not by the type system — a client could call `insertpm` directly with a V-address in the wrong range and the backend would not reject it. So: **enforced by insertion logic, not by type structure**.

**In the type document's POOM:** The retraction TYPE ADDRESS points to V=2.N in the type document (link subspace). The type document's text content is at V∈[1.x]. Same argument: disjoint by insertion logic.

**In the ISA allocation:** Link atoms (LINKATOM=2) and text atoms (TEXTATOM=1) are allocated in different ISA ranges by `findisatoinsertmolecule` (`granf2.c:158–181`):

```c
if (hintptr->atomtype == TEXTATOM) {
    tumblerincrement (&lowerbound, 0, 1, isaptr);
} else if (hintptr->atomtype == LINKATOM) {
    tumblerincrement (&hintptr->hintisa, 2, 2, isaptr);
    // ...
}
```

TEXTATOM and LINKATOM allocate at different positions within the hint ISA's subtree (offset `atomtype` vs `2` at depth 2), making them occupy structurally disjoint ranges in the global granfilade I-address space. A link ISA (`1.1.0.1.0.1.0.2.1`) cannot coincide with a permascroll I-address (`2.1.0.5.0.123`) — they are rooted under different account/document paths. This disjointness holds at the I-address level, and since the document POOM maps V→I, the content at V∈[1.x] maps to permascroll addresses while V∈[2.x] maps to link ISAs — **two structurally different I-address families** that cannot intersect (Finding 0009, corrected by Finding 0038).

---

### 5. Direct Answer to the Structural Question

**The form:** A conventional retraction type address in udanax-green would be a VSpec pointing to `Address(version, 0, 2, N)` within a designated type document — i.e., an element-level address inside the link subspace (2.x), not the text subspace (1.x). The `2` in the element field's first component is the non-content subspace marker (see `client.py:604`, `xanadu.h:36–39`, `do2.c:156–158`).

**On the structural question:** `coverage(R) ∩ dom(Σ.C) = ∅` holds, but not purely structurally in the type-system sense. The disjointness is enforced by:

1. Insertion logic (`findnextlinkvsa`, `findvsatoappend`) that routes text to 1.x and links to 2.x — **code-enforced, not type-enforced**
2. ISA allocation logic (`findisatoinsertmolecule`, LINKATOM vs TEXTATOM) that produces I-address families that are rooted in different subtrees — **this part holds structurally** in the ISA space

The backend has no validation gate that rejects a MAKELINK command whose type VSpec points into the text subspace (1.x). The FEBE handlers in `fns.c`/`get1fe.c` accept any VSpec for the three-end without subspace checking. So the disjointness is maintained **by the client-side convention** (type addresses use 2.x, not 1.x) and **by the insertion code path** (links go through `findnextlinkvsa`, not `findvsatoappend`) — not by the backend enforcing an invariant at the API boundary.

The system chose Option B (uniform enfilade + convention) over Option A (type-aware enfilade), as documented in Finding 0009 (`findings/0009-document-address-space-structure.md:128–145`). The V-position itself serves as both a position identifier and a type discriminator — an overloaded role that the backend enforces softly through insertion routing rather than hard structural typing.
