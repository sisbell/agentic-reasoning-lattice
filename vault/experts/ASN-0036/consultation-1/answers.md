# Revision Consultation — ASN-0036

**Review:** review-1.md
**Date:** 2026-03-14 15:30

## Summary

5 REVISE items analyzed: 3 internal, 2 consulted (1 nelson, 1 gregory)

## Consultation Results

### Issue 2: S7 derivation from T4 has two gaps

**Category:** NELSON
**Reason:** Part (b) is an internal type restriction, but part (a) — whether I-space allocation is architecturally required to scope addresses under the allocating document's tumbler prefix — is a design intent question. Gregory's evidence that the implementation does this is already in the ASN; what's missing is whether Nelson intended this as a structural guarantee or whether it's an implementation convention.

**Nelson question:** Is it a design requirement that every I-space address be allocated under (scoped beneath) the tumbler prefix of the document that created it, so that the document field of an I-address always identifies the originating document — or is this an implementation convention that a conforming system could organize differently?

**Nelson's Answer:**

## It is a design requirement, not a convention.

The scoping of I-space addresses under their originating document's tumbler prefix is structural — it is the mechanism through which several of Nelson's fundamental guarantees are delivered. A conforming system could not organize this differently without replacing the guarantee mechanism itself.

### The address IS the provenance

The I-address structure `Node.0.User.0.Document.0.Element` [LM 4/26] is not merely an organizational convenience. It is the basis for origin traceability:

> "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

This guarantee is **structural, not metadata**. Nelson does not say "the system maintains a table mapping bytes to their documents." He says the home document can be ascertained — directly from the address. The Document field of the I-address *is* the proof of origin. If bytes could be allocated at I-addresses outside their creating document's prefix, this ascertainment would require a separate lookup mechanism that Nelson never specifies.

### Native vs. non-native depends on address scoping

The entire transclusion model rests on distinguishing native from non-native bytes by their I-address prefix:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

"Under its control" refers to the tumbler subtree beneath the document's prefix. A byte is native to document D if and only if its I-address falls within D's tumbler subtree. Non-native bytes are "inclusions or virtual copies" [LM 4/11]. This binary distinction — which drives transclusion, attribution, and royalty splitting — is computable only because I-addresses are scoped under their originating documents.

### The baptism principle requires it

Nelson's forking mechanism makes document-scoped allocation the *only* way bytes can come into existence:

> "The owner of a given item controls the allocation of the numbers under it." [LM 4/20]

> "Whoever owns a specific node, account, document or version may in turn designate (respectively) new nodes, accounts, documents and versions, by forking their integers. We often call this the 'baptism' of new numbers." [LM 4/17]

A document owner baptizes element addresses under that document. There is no mechanism described for allocating I-addresses outside the creating document's subtree — no "free-floating" byte allocation, no cross-document I-address assignment. The baptism principle makes scoped allocation the sole path of creation.

### Downstream guarantees depend on it

Several operations and guarantees assume document-scoped I-addresses:

1. **FINDDOCSCONTAINING** — "returns a list of all documents containing any portion of the material included by \<vspec set\>" [LM 4/70]. This works by tracing I-addresses to their document prefixes.

2. **Royalty flow** — "royalty on every byte transmitted... paid automatically by the user to the owner" [LM 2/43]. The "owner" is identified from the Document field of the I-address.

3. **Correspondence** — shared I-space origin is how the system identifies matching parts across versions [LM 2/20]. If I-addresses were not document-scoped, the system could not distinguish "same bytes transcluded" from "different bytes that happen to be identical."

4. **Version comparison** — SHOWRELATIONOF2VERSIONS "returns a list of ordered pairs of the spans of the two spec-sets that correspond" [LM 4/70]. Correspondence via shared I-addresses requires those addresses to encode their originating document.

### The one caveat: versions as "accidental extensions"

Nelson does note one place where the tumbler hierarchy is weaker than it appears:

> "In a sense the version, or subdocument number is only an accidental extension of the document number, and strictly implies no specific relationship of derivation." [LM 4/29]

But this applies to the document-to-version relationship (whether document 5.3 is "really" a child of document 5), not to the byte-to-document relationship. For bytes, there is no corresponding disclaimer. The element subspace is not "accidental" — it is the structural foundation of origin traceability.

### Conclusion

A conforming system cannot decouple I-addresses from document scoping. The address structure is the guarantee mechanism — it is how attribution works, how native/non-native is determined, how royalties are routed, and how correspondence is computed. Reorganizing I-address allocation would not violate a convention; it would break the invariants that Nelson's design depends on.

### Issue 3: S8 correspondence run displacement is underspecified

**Category:** GREGORY
**Reason:** The formalization requires knowing how V-space positions are concretely structured — whether they are always element-level tumblers at a fixed depth, what "consecutive V-positions" means in the enfilade. This determines k's type and whether T12 spans can isolate individual positions for the degenerate decomposition.

**Gregory question:** In the V-enfilade implementation, are V-space positions always element-level tumblers at a fixed depth, and does "consecutive positions" mean incrementing only at the lowest-level ordinal — or can V-addresses appear at varying depths within a document's virtual address space?

**Gregory's Answer:**

## KB Synthesis

V-space positions in udanax-green are **not** element-level tumblers at varying depths — they are structurally shallow, fixed-depth tumblers, and "consecutive" means incrementing only the rightmost (ordinal) digit.

## Fixed-Depth Structure

From [SS-POOM-BOTTOM-CRUM], V-addresses in POOM bottom crums consistently use **2 tumbler digits** — e.g., `0.5`, `1.1`, `2.1` — while I-addresses use 6–9 digits. The V-width exponent is computed as `shift = tumblerlength(vsaptr) - 1`, so a V-address of length 2 yields `exp = -1`, encoding widths as fractions like `0.11`.

The pattern is always `{subspace_digit}.{ordinal}`:

- `1.x` — text content positions
- `2.x` — link orgl references  
- `3.x` — link type endpoints

[SS-SUBSPACE-CONVENTION] and [SS-TWO-BLADE-KNIFE] confirm this. The two-blade knife computes the second blade as `(N+1).1` for any insertion at `N.x` — this formula only works if all positions within a subspace share the same 2-digit depth. If V-addresses could appear at varying depths, the boundary `(N+1).1` wouldn't cleanly separate subspaces.

## "Consecutive" Means Increment at the Rightmost Digit

From [ST-INSERT] (Finding 0031), text insertion calls:

```c
tumblerincrement(&lsa, 0, textset->length, &lsa)
```

The `rightshift=0` parameter means the increment is applied at the **last significant digit** of the current address. So for a V-address `1.3`, inserting 5 characters produces positions `1.3`, `1.4`, `1.5`, `1.6`, `1.7` — plain ordinal counting at the second digit.

[INV-VSPAN-CONSOLIDATION] observes this directly: 100 sequential single-character inserts produce a single consolidated span `{start: 1.1, width: 0.100}` — not fragmented addresses at varying depths.

## The Inter-Character Gap Model

[SS-ADDRESS-SPACE] (Finding 0027) clarifies that V-positions are **inter-character cursors** (gaps between characters), not character indices. Position `1.1` is the gap before the first character, `1.2` before the second, etc. Each unit of V-space corresponds to exactly one byte [INV-SINGLE-CHAR-GRANULARITY] [SS-CONTENT-IDENTITY (Finding 0034)].

## No Depth Variation Within a Document

V-addresses do not appear at varying tumbler depths within the same document's virtual address space. The subspace boundary arithmetic in [SS-TWO-BLADE-KNIFE] (`findaddressofsecondcutforinsert` always produces `(N+1).1`) and the V-width encoding in [SS-INSERT-VWIDTH-ENCODING] both assume all same-subspace positions share the same tumbler length. A mixed-depth V-space would break the two-blade knife's subspace isolation guarantee and the V-width encoding's exponent assumption.

The only caveat: the zero tumbler and negative tumblers are technically valid tumblers, and [SS-POOM-BIJECTIVITY] notes that malformed DELETE sequences can produce POOM entries with negative V-positions — but these are pathological states, not valid document structure.

---

## Code Exploration

Good — I've now read all the critical evidence directly. Here is the full answer.

---

## V-Space Position Depth and Consecutive Addressing in udanax-green

**Short answer:** V-space positions are **not** at a fixed element-level depth. The virtual address space is hierarchically segmented, and addresses appear at varying depths depending on what they represent. "Consecutive" insertions of text increment only the lowest ordinal, but the base address from which they start is itself at a depth determined by document structure — not by a fixed convention.

---

### 1. The Tumbler Arithmetic Engine

The key primitive is `tumblerincrement` [`backend/tumble.c:599–623`]:

```c
int tumblerincrement(tumbler *aptr, INT rightshift, INT bint, tumbler *cptr)
{
    for (idx = NPLACES; aptr->mantissa[--idx] == 0 && idx > 0;);
    cptr->mantissa[idx + rightshift] += bint;   /* line 621 */
    tumblerjustify (cptr);
}
```

The `rightshift` parameter selects **which ordinal position is incremented**. It is not always zero (the lowest). When `rightshift` is 1, the increment happens one level above the current most-significant digit. When it is 2, two levels above. The actual depth touched is thus a function of the call site's intent, not a fixed convention.

`tumblerlength` [`backend/tumble.c:259–262`] returns the number of semantically significant ordinals in a given tumbler:

```c
INT tumblerlength(tumbler *tumblerptr)
{
    return (nstories (tumblerptr) - tumblerptr->exp);
}
```

This value varies per address, not per document or per type.

---

### 2. V-Space Is Hierarchically Segmented, Not Flat

The V-space in a document is divided into two subspaces, distinguished by the first mantissa ordinal:

**`istextcrum`** [`backend/orglinks.c:246–253`]:
```c
bool istextcrum(typecorecrum *crumptr)
{
    if(crumptr->cdsp.dsas[V].mantissa[1] == 0
       && is1story(&crumptr->cwid.dsas[V]))
        return TRUE;
    return FALSE;
}
```

**`islinkcrum`** [`backend/orglinks.c:255–261`]:
```c
bool islinkcrum(typecorecrum *crumptr)
{
    if(crumptr->cdsp.dsas[V].mantissa[0] == 1
       && crumptr->cdsp.dsas[V].mantissa[1] != 0)
        return TRUE;
    return FALSE;
}
```

The comment inline says it explicitly: *"if the whole crum is displaced into link space it is a link crum — this is true if the tumbler is a `1.n` tumbler where `n != 0`"*.

So the V-space structure is:

| Tumbler shape | `mantissa[0]` | `mantissa[1]` | Meaning |
|---|---|---|---|
| Text root | any | `== 0` | Text content (1-ordinal deep) |
| Link endpoint | `== 1` | `!= 0` | Link subspace (2-ordinal deep) |

These are structurally different depths. Text crums are 1-story; link crums are 2-story.

---

### 3. The Append Address Is Computed, Not Fixed-Depth

`findvsatoappend` [`backend/orglinks.c:29–49`] determines where to append new text in V-space:

```c
int findvsatoappend(typecorecrum *ptr, tumbler *vsaptr)
{
    tumblerincrement (&linkspacevstart, 0, 2, &linkspacevstart);  /* line 37: sets "2" threshold */
    prologuend (ptr, &offset, &grasp, &reach);
    if (iszerolock(...) || tumblercmp (&grasp.dsas[V], &linkspacevstart) != LESS) {
        tumblerincrement (vsaptr, 0, 1, vsaptr);   /* line 42 */
        tumblerincrement (vsaptr, 1, 1, vsaptr);   /* line 43 */
    } else if (tumblercmp (&reach.dsas[V], &linkspacevstart) == LESS) {
        movetumbler (&reach.dsas[V], vsaptr);      /* line 45: extend text at current depth */
    } else {
        findnextaddressinvspace (ptr, &grasp, &linkspacevstart, vsaptr);  /* line 47 */
    }
}
```

Three distinct cases arise:
- **Empty document:** Two separate `tumblerincrement` calls at `rightshift=0` then `rightshift=1` build a 2-ordinal address like `1.1`.
- **Text-only document (no links):** The append address is simply `reach.dsas[V]` — the current maximum reach, whatever depth that is.
- **Mixed document:** `findnextaddressinvspace` walks the tree recursively to find the next available position.

There is no fixed depth. The depth of the resulting V-address depends on which branch is taken.

---

### 4. Consecutive Text Insertions Do Increment the Lowest Ordinal

Within the `inserttextgr` loop [`backend/granf2.c:95–101`]:

```c
for (; textset; textset = textset->next) {
    insertseq ((typecuc*)fullcrumptr, &lsa, &locinfo);
    tumblerincrement (&lsa, 0, textset->length, &lsa);   /* line 100 */
}
```

Here `rightshift = 0`, so each successive text segment advances the cursor by `textset->length` at the **lowest significant ordinal**. This is the "leaf-level increment" intuition — but it applies only to the granfilade's I-space cursor (`lsa`), not to V-space. V-space positions are assigned after the fact through the orglink permutation matrix.

---

### 5. Address Allocation for Non-Atom Insertions Uses Variable Depth

`findisatoinsertnonmolecule` [`backend/granf2.c:203–242`] computes depth conditionally:

```c
depth = hintptr->supertype == hintptr->subtype ? 1 : 2;   /* line 209 */
```

And then uses that variable depth throughout:

```c
tumblerincrement(&hintptr->hintisa, depth, 1, isaptr);    /* line 237 */
/* ... */
tumblertruncate (&lowerbound, hintlength + depth, isaptr);
tumblerincrement(isaptr, tumblerlength(isaptr)==hintlength ? depth : 0, 1, isaptr);  /* line 240 */
```

When `supertype == subtype` (same-level hierarchy), depth is 1. Otherwise it is 2. The resulting address is `hintlength + depth` ordinals long — variable by design.

Similarly, `findisatoinsertmolecule` [`backend/granf2.c:158–181`] takes three entirely different paths depending on `atomtype`:

- `rightshift=2` for the upper bound search [`line 162`]
- Then `rightshift=2` again for `isaptr` plus `rightshift=1` step [`lines 166–167`] for same-length case
- `rightshift=0` increment when inserting a `TEXTATOM` into a shorter branch [`line 169`]
- `rightshift=2` then conditionally `rightshift=1` or `rightshift=0` for `LINKATOM` [`lines 171–175`]

There is no single, fixed rightshift for "consecutive positions."

---

### 6. V-Space Positions in the Permutation Matrix

The V-address assigned to a piece of content lives in the **orglink (permutation matrix enfilade)**, not in the granfilade. The POOM stores `(V-address, I-address)` pairs. The V-address is built during `doinsert` by calling `findvsatoappend` (for appends) or is supplied by the client directly. The I-address comes from the granfilade allocation.

Because `findvsatoappend` returns addresses of variable depth depending on document state (see §3 above), and because the POOM stores these as-is, the POOM contains V-addresses of varying depth across a single document.

---

### Conclusion

1. **V-space positions are not at a fixed element-level depth.** They vary based on document structure: 1-story for text root positions, 2-story for link endpoint positions, and computed depths for hierarchical document/account addressing in the granfilade.

2. **"Consecutive positions" does not uniformly mean incrementing only the leaf ordinal.** In the granfilade's I-space cursor (`lsa`), sequential text bytes do advance by `rightshift=0` increments [`granf2.c:100`]. But V-space append positions are computed by `findvsatoappend`, which may return the current tree-reach address (preserving whatever depth it has), a newly constructed 2-ordinal `1.1`-style address, or a recursively found address.

3. **The depth of a V-address is a property of its semantic role**, not a document-wide constant. The code explicitly tests `mantissa[1] == 0` vs. `mantissa[1] != 0` to distinguish text from link content [`orglinks.c:248`, `257`], proving the system relies on depth variation as a semantic signal, not a bug to be avoided.
