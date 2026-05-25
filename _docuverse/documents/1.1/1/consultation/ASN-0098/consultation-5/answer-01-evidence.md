## Question 1 [evidence]

> Does the udanax-green implementation allow a document's arrangement to reference link addresses (e.g., for link-subspace V-positions), and if so what referential-integrity invariant does it enforce across the subspaces?

## KB Synthesis

## Document Arrangement and Link-Subspace Referential Integrity

### Yes — the POOM stores link references in the 2.x subspace

When `docreatelink` executes, it places the link orgl's ISA into the document's POOM enfilade at a V-position in the `2.x` subspace (first link at `2.1`, subsequent links at successive positions). This is done via the same `docopy` / `insertpm` path used for text insertion. The POOM therefore contains both text mappings (`1.x → permascroll I-addresses`) and link-reference mappings (`2.x → link orgl ISAs`). [SS-DUAL-ENFILADE], [SS-LINK-SUBSPACE], [ST-CREATE-LINK]

---

### What the system enforces

**1. Subspace isolation under INSERT and DELETE**

INSERT at `1.x` constructs a two-blade knife with `blade[1] = 2.1`, so `insertcutsectionnd` classifies all `2.x` crums as case 2 (no shift). Text insertion structurally cannot displace link-subspace V-positions. [FC-SUBSPACE], [SS-TWO-BLADE-KNIFE]

DELETE at `1.x` achieves the same result accidentally: `tumblersub(2.1, width_0.x)` is a no-op because `strongsub` returns the minuend unchanged when `width.exp < entry.vpos.exp`. The exponent mismatch between fractional text widths and integer link positions prevents cross-subspace shifts. [FC-SUBSPACE, Finding 0055], [INT-DELETE-SUBSPACE-ASYMMETRY]

**2. Permanence of referenced link orgls**

Once a link orgl is created, it persists permanently in I-space. There is no DELETELINK operation. Consequently, any correctly-placed `2.x` POOM entry that points to a valid link ISA will always have a live referent. The system cannot create a dangling pointer to a link that was subsequently destroyed. [INV-LINK-PERMANENCE], [SS-THREE-LAYER-MODEL]

**3. POOM entry removal does not destroy the orgl**

`DELETEVSPAN(2.x)` removes the POOM entry but leaves the link orgl in I-space and the DOCISPAN entries in the spanfilade intact. This produces a "reverse orphan": the link is no longer visible in the document's vspanset but remains fully discoverable and followable. The referential relationship is severed at the POOM layer only. [EC-REVERSE-ORPHAN], [FC-LINK-DELETE-ISOLATION]

---

### What the system does NOT enforce

**The subspace convention is caller-enforced only.** `acceptablevsa()` unconditionally returns `TRUE`. There is no runtime check preventing:

- Text bytes placed at `2.x` via INSERT (confirmed experimentally) [PRE-ENF0-PLACEMENT-GAP, EC-RETRIEVE-VSPANSET-BOTH-SUBSPACES]
- Link ISAs placed at `1.x` positions [SS-SUBSPACE-CONVENTION]
- REARRANGE pivoting content across the subspace boundary [PRE-REARRANGE, Finding 0051]

ENF0 prevents modification of existing link orgls (`element-type ≠ LINKATOM`) but is a modification guard, not a placement guard — it does not prevent writing non-link data at `2.x`. [PRE-ENF0-PLACEMENT-GAP]

---

### The operative invariant

The intended invariant is:

```
∀ v ∈ poom(doc): v.mantissa[0] == 2 ⟹ content_at(v) is a valid link orgl ISA
∀ v ∈ poom(doc): v.mantissa[0] == 1 ⟹ content_at(v) is a permascroll I-address
```

This holds as a **global invariant only under complete caller cooperation** — it is not enforced by the storage layer. [INV-SUBSPACE-CONVENTION]

What the storage layer does guarantee unconditionally is the **forward permanence half**: if the convention was followed at link creation time, the link ISA stored at `2.x` will never become invalid in I-space, because link orgls are permanent. The weak form of referential integrity — "referenced link orgls exist" — holds without caller cooperation because link permanence is structural. The strong form — "all `2.x` entries are link orgls" — requires caller cooperation because placement is unenforced. [INV-LINK-PERMANENCE], [FC-LINK-PERSISTENCE]

---

## Code Exploration

I now have a complete picture from reading all the relevant source. Here is the full answer:

---

## Does udanax-green allow a document's arrangement to reference link addresses?

**Yes — in two architecturally distinct ways — and the invariant is enforced by allocation convention, not by a runtime guard.**

---

### 1. What is a "link address" in this codebase?

The tumbler structure [common.h:59–65] stores a variable-precision rational address in a 16-digit mantissa array. The Xanadu dot-notation `1.1` means `mantissa = {1, 1, 0, …}`.

`tumblerincrement(t, rightshift, bint, t)` [tumble.c:599–623] adds `bint` at position `lastNonZeroIdx + rightshift`. Starting from a zero tumbler:
- `tumblerincrement(t, 0, 2, t)` → `t = 2` (mantissa[0]=2)
- `tumblerincrement(t, 1, 1, t)` → `t = 2.1` (mantissa[0]=2, mantissa[1]=1)

Link-space V-addresses are multi-story tumblers of the form N.1 where N ∈ {1, 2, 3}.

---

### 2. The two subspaces inside every document

**`findvsatoappend`** [orglinks.c:29–48] governs where `appendpm` places new text:

```c
tumblerclear (&linkspacevstart);
tumblerincrement (&linkspacevstart, 0, 2, &linkspacevstart);  // 2.0
…
if (…) {
    tumblerincrement (vsaptr, 0, 1, vsaptr);  // 1.0
    tumblerincrement (vsaptr, 1, 1, vsaptr);  // → 1.1  ("no text in doc")
} else if (tumblercmp (&reach.dsas[V], &linkspacevstart) == LESS) {
    movetumbler (&reach.dsas[V], vsaptr);     // append after existing text, < 2.0
```

So text content occupies V-positions **1.1 ≤ V < 2.0** (the first text atom lands at 1.1 in an empty document; subsequent atoms grow from there but are bounded below 2.0).

**`findnextlinkvsa`** [do2.c:151–167] governs where a new link reference is placed in the **containing** document:

```c
tumblerclear (&firstlink);
tumblerincrement (&firstlink, 0, 2, &firstlink);  // 2.0
tumblerincrement (&firstlink, 1, 1, &firstlink);  // → 2.1
…
if (tumblercmp (&vspanreach, &firstlink) == LESS)
    movetumbler (&firstlink, vsaptr);             // first link at 2.1
else
    movetumbler (&vspanreach, vsaptr);            // subsequent links packed after
```

Link ISA references occupy V-positions **≥ 2.1** in the containing document.

The boundary is therefore **V = 2.0**: text below, link ISA references above.

---

### 3. How `docreatelink` writes a link address into the containing document's arrangement

`docreatelink` [do1.c:195–221] does the following in sequence:

```c
createorglingranf(taskptr, granf, &hint, linkisaptr)    // allocate link's ISA
&& tumbler2spanset(taskptr, linkisaptr, &ispanset)       // make an I-span for the link's ISA
&& findnextlinkvsa(taskptr, docisaptr, &linkvsa)         // V-pos ≥ 2.1 in containing doc
&& docopy(taskptr, docisaptr, &linkvsa, ispanset)        // INSERT the link ISA into the doc's orgl at that V
```

So **yes**: the containing document's permutation-matrix enfilade (orgl) receives a node at V ≥ 2.1 whose I-coordinate is the link's own ISA. The document's arrangement literally holds link-space addresses.

---

### 4. A link document's own internal subspace layout

Inside the link document itself, `setlinkvsas` [do2.c:169–183] hardcodes three V-positions:

```c
from  → 1.1  (mantissa[0]=1, mantissa[1]=1)
to    → 2.1  (mantissa[0]=2, mantissa[1]=1)
three → 3.1  (mantissa[0]=3, mantissa[1]=1)
```

These are fed to `insertendsetsinorgl` [do2.c:130–149], which calls `insertpm` to place the endpoint sporgl-sets (I-span pointers back to the linked content) into the link's own orgl at those three V-slots. The predicates `istextcrum` [orglinks.c:246–253] and `islinkcrum` [orglinks.c:255–261] let traversal code distinguish these crums:

```c
bool islinkcrum(typecorecrum *crumptr) {
    if (crumptr->cdsp.dsas[V].mantissa[0] == 1 && crumptr->cdsp.dsas[V].mantissa[1] != 0)
        return TRUE;   // V-displacement is 1.n (n≠0): a link endpoint crum
    return FALSE;
}
bool istextcrum(typecorecrum *crumptr) {
    if (crumptr->cdsp.dsas[V].mantissa[1] == 0 && is1story(&crumptr->cwid.dsas[V]))
        return TRUE;   // single-digit V-displacement, single-digit width: pure text crum
    return FALSE;
}
```

`maxtextwid` [orglinks.c:224–245] skips `islinkcrum` nodes when computing the text-extent of a document that has both text and link content, so `retrievevspansetpm` [orglinks.c:173–221] can return separate text and link vspans.

---

### 5. The referential-integrity invariant — and its gap

The intended invariant is a strict **V-space partition**:

| Region | Owner | Allocator |
|---|---|---|
| V < 2.0 | text content | `findvsatoappend` [orglinks.c:37–48] |
| V ≥ 2.1 | link ISA references in containing doc | `findnextlinkvsa` [do2.c:156–163] |
| V = 1.1 / 2.1 / 3.1 | link endpoints inside link doc | `setlinkvsas` [do2.c:169–183] |

**The enforcement is purely by convention in the allocation functions.** The one place designed to enforce it at write time, `acceptablevsa` [do2.c:110–112], is a stub:

```c
bool acceptablevsa(tumbler *vsaptr, typeorgl orglptr)
{
    return (TRUE);
}
```

`docopy` [do1.c:45–65] calls this before every `insertpm`, but gets no protection:

```c
return (
   specset2ispanset(…)
&& findorgl(…)
&& acceptablevsa(vsaptr, docorgl)   // ← always TRUE
&& insertpm(…)
…
```

The FEBE protocol handler `copy` [fns.c:35–47] equally performs no subspace validation before passing the caller-supplied V-address to `docopy`. Any caller that constructs a V-address in the link subspace (e.g., 2.1) and issues a `copy` request will successfully insert content into the link-subspace portion of a text document.

The only read-path guards are the `islinkcrum`/`istextcrum` predicates used during retrieval traversal and the `retrievevspansetpm` separation logic — these are descriptive, not prescriptive.

---

### Summary

Udanax-green **explicitly and intentionally** places link addresses inside a document's arrangement: the containing document stores link ISA references at V ≥ 2.1, while a link document stores its endpoint content at V = 1.1 / 2.1 / 3.1. The architectural invariant is a **V-space partition at V = 2.0** maintained by the allocation functions `findvsatoappend` and `findnextlinkvsa`. However, `acceptablevsa` [do2.c:110–112] is an unimplemented stub, so nothing structurally prevents a caller from writing into the wrong subspace via the `docopy`/`copy` path. Subspace integrity is a **naming convention**, not a checked constraint.
