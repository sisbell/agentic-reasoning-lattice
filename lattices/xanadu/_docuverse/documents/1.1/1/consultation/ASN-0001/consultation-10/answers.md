# Revision Consultation — ASN-0001

**Review:** ASN-0001-review-10.md
**Date:** 2026-03-01 19:14

## Summary

3 REVISE items analyzed: 1 internal, 2 consulted (0 nelson, 2 gregory)

## Consultation Results

### Issue 1: TA7a verification for ⊖ rests on a false claim about the divergence point

**Category:** GREGORY
**Reason:** The fix requires knowing what operands are actually passed to `strongsub` during V-space editing shifts — whether they are full tumblers or element-relative positions — which determines where the divergence point falls and whether the current proof structure is salvageable.

**Gregory question:** When DELETE shifts V-space positions backward, what are the actual operands passed to `strongsub` — full tumblers with the document prefix, or element-relative positions within a subspace context?

**Gregory's Answer:**

## KB Synthesis

The KB gives us two complementary pieces of evidence.

**What `strongsub` actually receives**

The code at `edit.c:63` is:
```c
tumblersub(&ptr->cdsp.dsas[index], width, &ptr->cdsp.dsas[index])
```
[ST-DELETE, Finding 0053; Finding 0055]

The operands are:
- `ptr->cdsp.dsas[V]` — the POOM crum's V-dimension **displacement field**
- `width` — the deletion width tumbler

**These are NOT full document-prefixed tumblers.**

[SS-POOM-BOTTOM-CRUM] Finding 0076 is explicit: V-addresses in POOM crums use **2-digit short tumblers** ("Crum V-origin: 0.5 (2 digits)"), while I-addresses use 6–9 digits. Document ISA prefixes like `1.1.0.1.0.1` never appear in the V-dimension displacement field.

**The relative-addressing layer**

[SS-ENFILADE-TREE] Finding 0066 adds a further refinement: 2D enfilades (including POOM) store children's `cdsp` values as **relative displacements from the parent**, not as absolute V-positions. The root absorbs the minimum address via `setwispnd`; children's `cdsp.dsas[V]` values are the delta from the parent's grasp. So the value arriving at `strongsub` as operand `a` is a parent-relative offset, not even a document-absolute V-position.

**Why the exponent check works**

[SS-TUMBLER] Finding 0055 gives the concrete picture:

| Crum | `cdsp.dsas[V]` | exp | Deletion width exp | `strongsub` result |
|------|---------------|-----|--------------------|--------------------|
| Text crum | `0.4` | -1 | -1 | Subtraction proceeds → shifted |
| Link crum | `2.1` | 0 | -1 | Guard fires (b.exp < a.exp) → unchanged |

Text V-displacements have exp=-1 (positions like `0.4`, `1.5` within the element-relative coordinate frame). Link V-displacements live in the `2.x` subspace and have exp=0. Since the deletion width for a text-subspace operation also has exp=-1, `strongsub`'s guard `if (bptr->exp < aptr->exp)` triggers for the link crum and returns it unchanged. This is the accidental arithmetic guard [FC-SUBSPACE, Finding 0055; INT-DELETE-SUBSPACE-ASYMMETRY].

**Summary**

The operands passed to `strongsub` during DELETE's V-shifting are **short (2-digit), parent-relative V-displacement tumblers** — element-space values inside the POOM's coordinate system, not document-ISA-prefixed global addresses. The exponent of these displacement tumblers (exp=-1 for text subspace content, exp=0 for link subspace content) is what makes the `strongsub` exponent guard provide incidental subspace isolation, as distinguished from INSERT's deliberate structural guard via the two-blade knife [SS-TWO-BLADE-KNIFE].

---

## Code Exploration

I now have all the pieces needed for a complete, source-cited answer. Here is the full analysis:

---

## Answer: What Are the Actual Operands Passed to `strongsub` During Delete?

### TL;DR

They are **element-relative positions within a subspace context** — specifically, V-space displacement tumblers relative to the POOM fullcrum's grasp. They are **not** full document-qualified tumblers.

---

### The Complete Call Chain

```
fns.c:deletevspan          [fns.c:333]
  → do1.c:dodeletevspan    [do1.c:158]
    → orglinks.c:deletevspanpm [orglinks.c:145]
      → edit.c:deletend    [edit.c:31]
        → tumblersub       [edit.c:63]
          → tumbleradd     [tumble.c:428]
            → strongsub    [tumble.c:385]
```

---

### Step 1: `deletevspanpm` — What Gets Passed to `deletend`

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

`deletend` receives:
- `origin` = `vspanptr->stream` — the V-space start of the deleted region (a V-stream position, e.g., `1.5`)
- `width` = `vspanptr->width` — the V-space size of the deleted region (a simple magnitude, e.g., `0.3`)
- `index` = `V` (the V dimension of the POOM)

These are both pure V-space magnitudes. No document prefix.

---

### Step 2: `deletend` — The Structural Fact That Determines Everything

```c
// edit.c:31-76
int deletend(typecuc *fullcrumptr, tumbler *origin, tumbler *width, INT index)
{
    clear (&offset, sizeof(offset)); /* fullcrum always has zero offset */
    prologuend ((typecorecrum*)fullcrumptr, &offset, &grasp, &reach);
    ...
    makecutsnd (fullcrumptr, &knives);
    newfindintersectionnd (fullcrumptr, &knives, &father, &foffset);   // <-- KEY
    prologuend ((typecorecrum*)father, &foffset, &fgrasp, (typedsp*)NULL);
    for (ptr = (typecuc *) findleftson (father); ptr; ptr = next) {
        ...
        case 2:
            tumblersub (&ptr->cdsp.dsas[index], width, &ptr->cdsp.dsas[index]);  // <-- SHIFT
```

### Step 3: The Stub That Fixes `father` = fullcrum, Always

```c
// ndinters.c:38-42
int newfindintersectionnd(typecuc *fullcrumptr, typeknives *knives, typecuc **ptrptr, typewid *offset)
{
    *ptrptr = fullcrumptr;        // ALWAYS the fullcrum
    clear (offset, sizeof(*offset)); // foffset = 0
}
```

The original recursive `findintersectionnd` (commented out above this at `ndinters.c:18-36`) would descend the tree to find the lowest common ancestor of both cut points. The replacement stub is a **simplification**: it always returns the fullcrum. This means:
- `father` = `fullcrumptr` (always)
- `foffset` = zero vector
- `fgrasp` = `prologuend(fullcrumptr, 0)` = `0 + fullcrumptr->cdsp` = `fullcrumptr->cdsp`
- The loop iterates over **direct children of the fullcrum**

---

### Step 4: What `ptr->cdsp.dsas[V]` Contains

`prologuend` [retrie.c:334-339] defines the coordinate semantics:

```c
int prologuend(typecorecrum *ptr, typedsp *offset, typedsp *grasp, typedsp *reach)
{
    dspadd (offset, &ptr->cdsp, grasp, (INT)ptr->cenftype);  // grasp = offset + cdsp
    if (reach)
        dspadd (grasp, &ptr->cwid, reach, (INT)ptr->cenftype); // reach = grasp + cwid
}
```

A crum's `cdsp` is a **relative displacement from parent's accumulated grasp**, not an absolute address. This is confirmed by `insertcbcnd` [insertnd.c:263]:

```c
dspsub (origin, grasp, &new->cdsp, (INT)father->cenftype);
// new->cdsp = absolute_insert_vsa - parent_grasp
```

After `setwispnd` normalization [wisp.c:192-211], the minimum child displacement is absorbed upward into the parent:

```c
// wisp.c:200,211
dspadd (&father->cdsp, &mindsp, &newdsp, (INT)father->cenftype);  // min goes up
dspsub (&ptr->cdsp, &mindsp, &ptr->cdsp, (INT)ptr->cenftype);     // children adjusted down
```

Result: after normalization, the leftmost child of the fullcrum has `cdsp.dsas[V] = 0`, and all other children have `cdsp.dsas[V]` = V-space offset from the leftmost child's position. These are simple, sub-document-local magnitudes.

**`DSPSIZEPM = 2`** [wisp.h:26] — the POOM displacement is a 2-tumbler lock (I-slot and V-slot). `ptr->cdsp.dsas[V]` is a **single tumbler** holding only the V-space component.

---

### Step 5: The `strongsub` Call Path

The shift at `edit.c:63`:

```c
tumblersub (&ptr->cdsp.dsas[index], width, &ptr->cdsp.dsas[index]);
```

Inside `tumblersub` [tumble.c:406-440]:

```c
movetumbler (bptr, &temp);
temp.sign = !temp.sign;       // negate width
tumbleradd (aptr, &temp, cptr); // = crum_disp + (-width)
```

Inside `functiontumbleradd` [tumble.c:365-404]:

```c
// aptr = ptr->cdsp.dsas[V]  (positive, sign=0)
// bptr = -width              (negative, sign=1)
// different signs → check magnitudes
} else if (abscmp (aptr, bptr) == GREATER) {
    strongsub (aptr, bptr, cptr);    // line 385
    cptr->sign = aptr->sign;
```

`strongsub` [tumble.c:534-565] works purely on `mantissa[]` and `exp`, ignoring the sign field. It computes |aptr| − |bptr| digit by digit.

---

### The Actual Operands

| Operand | Source | Content |
|---------|--------|---------|
| `aptr` | `ptr->cdsp.dsas[V]` | V-space displacement of the crum from the fullcrum's grasp — a **relative intra-document V-space magnitude** |
| `bptr` | `-width` (negated) | The delete span width, also a **pure V-space magnitude** |

**Neither operand contains a document prefix.** The document ISA (a multi-story tumbler like `account.node.version`) is an I-space address managed by the granfilade. V-space coordinates are stream positions within a document's virtual space — they start at `1` for text content, never embed the document identifier.

---

### Concrete Example

Document with characters at V-positions 1–5. Delete width=2 starting at V=2.

After `setwispnd` normalization:
- `fullcrum->cdsp.dsas[V]` = `{mantissa[0]=1}` (leftmost V-position)
- Child crums have `cdsp.dsas[V]` = `{0}`, `{1}`, `{2}`, `{3}`, `{4}` respectively

Delete removes V=2 and V=3 (width=2). Crums at V=4 and V=5 fall in case 2:
- For crum at cdsp=3: `tumblersub({3}, {2}, result)` → `strongsub({3}, {2}, result)` → `{1}`
- For crum at cdsp=4: `tumblersub({4}, {2}, result)` → `strongsub({4}, {2}, result)` → `{2}`

`strongsub` receives `{mantissa[0]=3}` and `{mantissa[0]=2}` — **simple one-story V-space tumblers with no document prefix**.

---

### Summary

`strongsub` during delete receives **element-relative positions within a V-space subspace context**, not full document-qualified tumblers.

Specifically:
1. **`aptr`** = `ptr->cdsp.dsas[V]`: the V-space displacement of a direct child of the POOM fullcrum, measured from the fullcrum's own V-position (itself a cumulative minimum absorbed from descendants by `setwispnd`). This is a sub-document-local magnitude, never containing the document ISA prefix.

2. **`bptr`** = the negated delete width: also a pure V-space magnitude.

This follows structurally from three facts:
- `newfindintersectionnd` [ndinters.c:38-42] always sets `father = fullcrumptr`, so only direct children are shifted
- `cdsp` is defined as a relative offset from the parent's grasp [retrie.c:334-339, insertnd.c:263]
- V-space and I-space are completely separate tumbler dimensions; `DSPSIZEPM = 2` [wisp.h:26] gives the POOM 2 separate tumbler slots, and `cdsp.dsas[V]` is the V-slot only — the document's ISA lives in I-space, never embedded in V-space coordinates

### Issue 2: V-space position representation is ambiguous

**Category:** GREGORY
**Reason:** The ASN presents conflicting representations (full tumblers vs simple counters) and the implementation evidence would definitively show how V-positions are stored and manipulated in the enfilade's V-dimension.

**Gregory question:** In the 2D enfilade's V-dimension, are V-space displacements and positions represented as full tumblers (including document prefix and subspace identifier) or as element-local values relative to a document/subspace context?

**Gregory's Answer:**

## KB Synthesis

The KB gives a clear, multi-source answer on this.

**V-space displacements and positions are element-local relative values — short tumblers, not full document-qualified addresses.**

## What the storage looks like

[SS-POOM-BOTTOM-CRUM] documents the concrete representation directly. POOM bottom crums store dual-space coordinates with **asymmetric precision**:

- **I-addresses**: 6-9 tumbler digits (e.g., `0.0.0.0.0.0.0.0.11`) — full hierarchical addresses including document prefix
- **V-addresses**: 2 tumbler digits (e.g., `0.5`, `1.1`) — short, element-local values

The examples throughout the KB confirm this: V-positions appear as `1.1`, `1.3`, `2.1`, `3.1` — never as `1.1.0.1.0.1.1.3` or any document-qualified form.

## The subspace identifier is the first digit

[SS-SUBSPACE-CONVENTION] / [SS-TWO-BLADE-KNIFE] establish that the V-address structure is `N.x` where:
- `N = 1` → text subspace
- `N = 2` → link orgl subspace  
- `N = 3` → link type endpoint subspace

The subspace identifier is baked into the first digit of the V-address itself. No document prefix surrounds it.

## Relative addressing within each POOM

[SS-ENFILADE-RELATIVE-ADDRESSING] (Finding 0066) is the key structural finding. POOM nodes do **not** store absolute V-positions — they store displacements relative to the parent:

> `absolute_grasp(node) = absolute_grasp(parent) + node.cdsp`

`setwispnd` maintains this invariant after every modification: it finds `mindsp` (minimum displacement across children), absorbs it into the root's `cdsp`, then subtracts it from every child's `cdsp`. The root's `cdsp` becomes the minimum V-address in the tree (the absolute base); all other nodes store relative offsets from that base.

[SS-WHEREONCRUM] shows the runtime reconstruction: `left = offset + cdsp`, where `offset` is accumulated through ancestor traversal.

## Why this is per-document, not globally qualified

Each document has its own POOM orgl, accessed via `findorgl(docisa)`. Once you're operating inside a specific document's POOM, the V-address space is inherently local to that document. There is no need to embed document identity into V-positions — the POOM itself is the document-scoped container.

[SS-INSERT-VWIDTH-ENCODING] confirms the local character: when INSERT encodes V-width, `shift = tumblerlength(vsaptr) - 1`. For a typical text position `1.1` (tumblerlength = 2), this yields `shift = 1`, giving V-width `exp = -1` — a 2-digit-scale tumbler. The V-address length drives the encoding, and V-addresses stay short.

## Summary

V-space displacements and positions in the POOM are:

1. **Short (2 digits)**: `N.x` form, not full hierarchical addresses
2. **Element-local**: scoped to the document whose POOM orgl is being queried
3. **Relatively addressed**: stored as parent-relative offsets; absolute position requires accumulating ancestor displacements
4. **Subspace-encoded**: the first digit encodes content type (1=text, 2=links, 3=type endpoints) per [SS-TWO-BLADE-KNIFE]

This contrasts sharply with I-addresses, which are full hierarchical tumblers that survive across document boundaries because they live in the global granfilade.

---

## Code Exploration

I now have enough evidence to give a complete, cited answer. Let me compile the findings.

---

## Answer

### V-space positions in the 2D enfilade are **document-local** — they are NOT full tumblers encoding a global document prefix or subspace identifier.

Here is the evidence from source, layer by layer.

---

### 1. The tumbler type and coordinate layout

`common.h:59-65` defines the tumbler:
```c
typedef struct structtumbler {
    humber xvartumbler;
    char varandnotfixed;
    char sign  BIT;
    short exp;
    tdigit mantissa[NPLACES];  /* NPLACES = 16 */
} tumbler;
```

`wisp.h:19-21` defines the per-crum `cdsp` / `cwid` fields as an array of tumblers indexed by dimension:
```c
#define I  0
#define V  1
```

The POOM crum (`enf.h:109-131`) stores both as:
```c
typewid cwid;   /* { tumbler dsas[2] } — width in I and V */
typedsp cdsp;   /* { tumbler dsas[2] } — displacement in I and V */
```

These two fields hold the **V-position** as `cdsp.dsas[V]` and `cwid.dsas[V]`.

---

### 2. What VSA values actually look like

`do2.c:151-166` (`findnextlinkvsa`):
```c
tumblerclear (&firstlink);
tumblerincrement (&firstlink, 0, 2, &firstlink);  /* firstlink = 2 */
tumblerincrement (&firstlink, 1, 1, &firstlink);  /* firstlink = 2.1 */
```

`do2.c:169-182` (`setlinkvsas`):
```c
/* from-end in link doc: */
tumblerincrement (fromvsaptr, 0, 1, fromvsaptr); /* = 1 */
tumblerincrement (fromvsaptr, 1, 1, fromvsaptr); /* = 1.1 */
/* to-end in link doc: */
tumblerincrement (tovsaptr, 0, 2, tovsaptr);     /* = 2 */
tumblerincrement (tovsaptr, 1, 1, tovsaptr);     /* = 2.1 */
/* three-end in link doc: */
tumblerincrement (threevsaptr, 0, 3, threevsaptr); /* = 3 */
tumblerincrement (threevsaptr, 1, 1, threevsaptr); /* = 3.1 */
```

`orglinks.c:41-43` (`findvsatoappend`) — first VSA for a new document:
```c
tumblerincrement (vsaptr, 0, 1, vsaptr); /* no text in doc */
tumblerincrement (vsaptr, 1, 1, vsaptr); /* = 1.1 */
```

These are **2-story tumblers** with values like `1.1`, `2.1`, `3.1`. They carry no document-ID prefix. Compare to a full document ISA, which looks like `1.1.0.1` (node.account.0.docnum) — a completely different length and structure.

---

### 3. V-space is organized into document-local subspace tiers

`orglinks.c:37` — the text/link boundary:
```c
tumblerincrement (&linkspacevstart, 0, 2, &linkspacevstart); /* = 2 */
```

The link-space boundary in a host document is simply `V = 2`. The V-space layout is:

| Absolute V position | Content |
|---|---|
| `1.1` → `< 2` | Text content in document |
| `2.1` and above | Link-end references embedded in document |
| `0` | Invalid (never inserted) |

In link documents (the link's own POOM orgl):

| Position | Role |
|---|---|
| `1.1` | FROM endpoint |
| `2.1` | TO endpoint |
| `3.1` | THREE endpoint |

The classification functions confirm this. `orglinks.c:246-260`:
```c
bool istextcrum(typecorecrum *crumptr)
{
    if(crumptr->cdsp.dsas[V].mantissa[1] == 0  && is1story(&crumptr->cwid.dsas[V])){ 
        return TRUE;
    }
    return FALSE;
}

bool islinkcrum(typecorecrum *crumptr)
{
    if(crumptr->cdsp.dsas[V].mantissa[0] == 1 && crumptr->cdsp.dsas[V].mantissa[1] != 0){
        return TRUE;
    }
    return FALSE;
}
```

After the enfilade's `setwispnd` normalization, a crum's stored `cdsp.dsas[V]` is a **relative** offset from its parent's absolute position. `islinkcrum` detects that a crum (after normalization against a text-anchored parent) carries a relative offset of the form `1.n` — which corresponds to an absolute position in the link-space tier when the parent is anchored at `1.x`. These tests are on small 1- or 2-digit tumblers, never on full document-ID tumblers.

---

### 4. Crums store RELATIVE displacements, not absolute positions

`insertnd.c:263` (`insertcbcnd`) — when a new bottom crum is created:
```c
dspsub(origin, grasp, &new->cdsp, (INT)father->cenftype);
```

The stored displacement is `origin − grasp`: the absolute VSA minus the accumulated offset from traversing the tree to this node. The crum does NOT store the absolute V-address.

`retrie.c:355-356` (`whereoncrum`) — how absolute position is recovered at query time:
```c
tumbleradd(&offset->dsas[index], &ptr->cdsp.dsas[index], &left);
```

Absolute position = parent-accumulated `offset` + crum's local `cdsp`. This must be computed dynamically by walking down the tree.

`retrie.c:334-338` (`prologuend`):
```c
int prologuend(typecorecrum *ptr, typedsp *offset, typedsp *grasp, typedsp *reach)
{
    dspadd(offset, &ptr->cdsp, grasp, (INT)ptr->cenftype);
    if (reach)
        dspadd(grasp, &ptr->cwid, reach, (INT)ptr->cenftype);
}
```

Each traversal step accumulates displacements. The V-coordinate of any leaf is: `sum of all cdsp.dsas[V] along the path from root to that leaf`.

`wisp.c:192-215` (`setwispnd`) — periodic re-centering:
```c
dspadd(&father->cdsp, &mindsp, &newdsp, (INT)father->cenftype);
// ...
dspsub(&ptr->cdsp, &mindsp, &ptr->cdsp, (INT)ptr->cenftype);
```

When the subtree bounding box shifts, `setwispnd` moves the minimum child offset into the parent and zeroes the minimum child. Children's `cdsp` values are kept as offsets relative to the minimum, not as absolute addresses. The absolute position is always reconstructed by summing the chain.

---

### 5. `docidandvstream2tumbler` is output-only, not internal

`tumble.c:685-699`:
```c
int docidandvstream2tumbler(tumbler *docid, tumbler *vstream, tumbler *tumbleptr)
{
    movetumbler(docid, tumbleptr);
    for (i = NPLACES-1; i >= 0; i--) {
        if (tumbleptr->mantissa[i]) { ++i; break; }
    }
    for (j = 0; i < NPLACES && j < NPLACES;)
        tumbleptr->mantissa[++i] = vstream->mantissa[j++];
}
```

This function concatenates a document ISA with a V-stream position into one large tumbler. But it is called **only** in `correspond.c:357-358` (`makespanpair`), which constructs the `typespanpairset` result returned by `doshowrelationof2versions` (compare_versions). It is not called anywhere in the V-coordinate insertion or retrieval path. The POOM stores document-local V-positions; the full `docid + vstream` concatenation is an output encoding for the compare_versions API response only.

---

### Summary

V-dimension positions and widths in the 2D enfilade (POOM/orgl) are **document-local, small tumblers** — typically 1- or 2-story tumblers encoding a subspace tier (mantissa[0]) and an ordinal position within that tier (mantissa[1]). They carry no document-ID prefix or global subspace identifier.

The document-local V-space is laid out as:
- **Text subspace**: `1.1`, `1.2`, … (all content appended sequentially)
- **Link-reference subspace**: `2.1`, `2.2`, … (link records embedded in a host document)
- **Link endpoint subspaces** (within a link's own orgl): from-end at `1.1`, to-end at `2.1`, three-end at `3.1`

Crums store **relative** V-displacements (`cdsp.dsas[V]`), not absolute positions. Absolute position is reconstructed during traversal by accumulating offsets from root to leaf. The function `docidandvstream2tumbler` (`tumble.c:685`) which does combine a full document ISA with a V-stream is used only to format the external output of `compare_versions`, not for internal storage.
