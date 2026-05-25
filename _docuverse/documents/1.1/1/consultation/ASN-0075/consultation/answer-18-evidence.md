## Question 18 [evidence]

> When comparing two documents that share history, does the I-address allocation parent (docISA) of unique I-spans reveal which document was the origin of the differing content?

## KB Synthesis

## Yes — with important nuance

**The structural encoding exists**

From [SS-ADDRESS-SPACE] Finding 0077, text content I-addresses are structured hierarchically under the document that allocated them:

```
1.1.0.1.0.1.3.0.1.1   ← text in document 1.1.0.1.0.1
1.1.0.1.0.1.1.3.0.1.1 ← text in version 1.1.0.1.0.1.1
```

The `makehint(DOCUMENT, ATOM, TEXTATOM, docisaptr, &hint)` call scopes every text allocation under the inserting document's address.

**Why this reveals origin**

[INV-IADDR-PROVENANCE] (Finding 0046) states each I-address has exactly one native document — INSERT allocates fresh I-addresses under the target document's content subspace; COPY and VCOPY share existing ones without allocating new ones.

[FC-GRANF-ON-VERSION] (Finding 0077) confirms that CREATENEWVERSION copies I-addresses but makes **no new content allocation**. Therefore, any I-span unique to a version (not returned by `compare_versions`) must have been inserted *after* versioning — its docISA prefix will be the **version's** address, not the original's.

**The nuance: shared vs. original-unique content share a prefix**

Content inserted into the *original* both before and after versioning carries the original's docISA prefix. You cannot distinguish "shared-before-versioning" from "unique-to-original" purely by prefix — you'd need to compare I-address ranges chronologically. However:

- Unique-to-version content: prefix = version docISA ✓
- Unique-to-original content (post-version inserts): prefix = original docISA ✓
- Shared content: prefix = original docISA (allocated there first) ✓

**For deeper transclusion chains**

[INV-TRANSITIVE-IDENTITY] (Findings 0002, 0007, 0018) holds because vcopy preserves I-addresses end-to-end. The I-address prefix of transcluded content always traces back to the document that *originated* it, not the document that copied it — consistent with [INV-IADDR-PROVENANCE].

**Caveat from [INT-LINK-INSERT] (Finding 0063)**

CREATELINK advances the granfilade's maximum I-address, which shifts subsequent text I-address allocation. This does not change the *prefix* structure, but it means text I-address ranges may not be contiguous across link-creation events, complicating range-based origin inference.

**Summary**: The docISA prefix of a unique I-span reliably identifies which document originated the content, because allocation is hierarchically scoped per document [SS-ADDRESS-SPACE] and I-addresses are immutable with a single native owner [INV-IADDR-PROVENANCE]. The practical limitation is that the original document's prefix appears on *both* shared and original-unique spans, so prefix alone cannot distinguish them without additional range analysis.

---

## Code Exploration

Now I have all the source evidence needed. Let me compile the precise answer.

---

## Answer

**Yes — but the mechanism is structural, not a field on the I-span itself.** The I-address prefix encodes the allocating document; the `docisa` field on `typevspec` is the lookup key used during V→I conversion to identify the right permutation matrix. Here is the full trace.

---

### 1. `docisa` — Definition and Role

`xanadu.h:78–83`:
```c
typedef struct structtypevspec{
    struct structtypevspec *next;
    typeitemid      itemid;
    typeisa docisa;         /* document's own ISA — the namespace key */
    typevspanset vspanset;
} typevspec;
```

A `typevspec` bundles two things: which document (`docisa`) and which V-spans within it. It is the external representation of "content in document D at V-positions P." `docisa` is a tumbler — the same type as any I-address in the system.

---

### 2. V→I Conversion Uses `docisa` to Find the Right Orgl

`do2.c:14–46`, `specset2ispanset`:
```c
} else if (((typeitemheader *)specset)->itemid == VSPECID) {
    if (iszerotumbler (&((typevspec *)specset)->docisa))
        qerror ("retrieve called with docisa 0\n");    /* do2.c:28–30 */
    if (!(
      findorgl (taskptr, granf, &((typevspec *)specset)->docisa, &docorgl, type)  /* do2.c:35 */
    && (ispansetptr = vspanset2ispanset (taskptr, docorgl, ((typevspec *)specset)->vspanset, ispansetptr)))){
           return (FALSE);
    }
}
```

`findorgl` uses `docisa` to retrieve that specific document's POOM enfilade. `vspanset2ispanset` then walks the orgl — the V→I mapping is document-specific because each document's edit history defines its own V-position-to-I-span correspondence. The same V-address means different content in different documents.

---

### 3. I-Address Allocation Embeds the Document ISA as a Structural Prefix

`do1.c:117–119`, `doinsert`:
```c
makehint(DOCUMENT, ATOM, TEXTATOM, docisaptr, &hint);  /* hint.hintisa = docisaptr */
ret = (inserttextingranf(taskptr, granf, &hint, textset, &ispanset)
    && docopy (taskptr, docisaptr, vsaptr, ispanset)
);
```

`granf2.c:130–156`, `findisatoinsertgr` routes to `findisatoinsertmolecule` for content atoms. `granf2.c:158–181`:
```c
static int findisatoinsertmolecule(typecuc *fullcrumptr, typehint *hintptr, typeisa *isaptr)
{
  typeisa upperbound, lowerbound;

    tumblerincrement (&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound);  /* line 162 */
    clear (&lowerbound, sizeof(lowerbound));
    findpreviousisagr ((typecorecrum*)fullcrumptr, &upperbound, &lowerbound);     /* line 164 */
    if (tumblerlength (&hintptr->hintisa) == tumblerlength (&lowerbound)) {
        tumblerincrement (&lowerbound, 2, hintptr->atomtype, isaptr);             /* line 166 */
        tumblerincrement (isaptr, 1, 1, isaptr);                                  /* line 167 */
    } else if (hintptr->atomtype == TEXTATOM) {
        tumblerincrement (&lowerbound, 0, 1, isaptr);                             /* line 169 */
    }
}
```

For a document with ISA `D`, `upperbound` is computed as `D + (2, TEXTATOM+1)`. `findpreviousisagr` finds the highest existing I-address below that bound. The new allocation is `lowerbound + 1`, which places it structurally inside the tumbler namespace rooted at `D`. Concretely: the first text in document `D` gets an address of the form `D.0.2.0.1` (two extra tumbler levels from the `tumblerincrement` calls at lines 166–167). Subsequent insertions increment from there. **The document's ISA is the structural parent of every I-address it allocates.**

---

### 4. `docreatenewversion` — New Document Gets Its Own ISA, Copied Content Retains Origin

`do1.c:260–299`, `docreatenewversion`:
```c
if (!createorglingranf(taskptr, granf, &hint, newisaptr)) {   /* line 277 — new ISA allocated */
    return (FALSE);
}
if (!doretrievedocvspanfoo (taskptr, isaptr, &vspan)) {        /* line 281 — get original's spans */
    return FALSE;
}
vspec.next = NULL;
vspec.itemid = VSPECID;
movetumbler(isaptr, &vspec.docisa);                            /* line 287 — docisa = ORIGINAL */
vspec.vspanset = &vspan;

docopyinternal(taskptr, newisaptr, &vspan.stream, &vspec);     /* line 293 */
```

The new version receives a fresh ISA (`newisaptr`). However, the content is copied with `vspec.docisa` set to the *original* document's ISA (`isaptr`, line 287). `docopyinternal` calls `specset2ispanset` with this `vspec`, which uses the original document's orgl (via `docisa`) to resolve V-spans → I-spans. Those I-spans — with their addresses rooted at the original document's ISA — are then inserted into the new document's own orgl.

---

### 5. What This Means for Unique Spans in a Comparison

`do1.c:428–449`, `doshowrelationof2versions`, converts each version's `typevspec` to I-spans and intersects them. The *unique* I-spans (in one document but not the other) fall into two cases:

**Case A — Content added to a document after versioning.** New insertions into document `X` (ISA = `X`) go through `doinsert` → `findisatoinsertmolecule` with `hintisa = X`. The resulting I-addresses have `X` as their structural parent. A unique I-span in document `X` with an address prefixed by `X`'s ISA was therefore created by document `X`.

**Case B — Content from the ancestor deleted from one fork.** The I-addresses of this content are prefixed with the ancestor document's ISA — they were allocated before the fork. Unique I-spans in document `A` with an address prefixed by the ancestor's ISA are content that `B` deleted (or never received).

**In both cases, the tumbler prefix of the I-address identifies the allocating document.** This is structural — there is no runtime `docisa` field attached to a bare `typeispan`; the encoding is in the tumbler value itself. The `docisa` field on `typevspec` is the pre-conversion handle that selects the right orgl for permutation; after that conversion, origin is readable from the I-address prefix.

---

### Summary

| Layer | Where origin is encoded | Mechanism |
|---|---|---|
| `typevspec.docisa` | Pre-conversion (V-space) | Explicit field; selects which orgl to use for V→I (`do2.c:35`) |
| I-address value | Post-conversion (I-space) | Structural prefix from allocation hint (`granf2.c:162–169`) |
| New version copy | `do1.c:287` | `docisa = original ISA` — I-spans of shared content retain the ancestor's prefix |

The `docisa` on a `typevspec` is the direct answer to "which document owns these V-spans" and is used as the lookup key for every V→I conversion (`do2.c:35`). For unique I-spans after a comparison, the I-address prefix answers which document allocated each span: post-versioning additions carry the allocating document's ISA as prefix; inherited-then-deleted content carries the ancestor's ISA as prefix.
