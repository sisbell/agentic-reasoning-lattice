## Question 16 [gregory]

> CREATENEWVERSION copies text-subspace POOM entries — are the I-displacements in the version's POOM byte-identical copies of the original's, or are they recomputed, and could recomputation ever produce different tumbler representations for the same logical I-address?

## KB Synthesis

## CREATENEWVERSION: I-Displacement Copy vs. Recomputation

The answer requires distinguishing three separate things: the I-address origin values, the I-width tumblers, and the V-width tumblers.

### I-Address Origins: Logically Identical, Physically May Differ

The copy path is: `docreatenewversion` → `doretrievedocvspanfoo` → `docopyinternal` → `specset2ispanset` → `insertpm` → `setwispnd` [ST-VERSION, Finding 0077].

`specset2ispanset` reads the I-address tumblers **directly from the source POOM's bottom crums** — these are the same tumblers originally placed there by `inserttextingranf`. They are not recomputed from the permascroll content. The I-origins passed to `insertpm` are byte-identical copies of what `specset2ispanset` extracted.

However, once `insertpm` places these into the version's new enfilade tree, `setwispnd` recalculates relative displacements [INV-ENFILADE-RELATIVE-ADDRESSING, Finding 0066]:

> `absolute_grasp(node) = absolute_grasp(parent) + node.cdsp`

The `cdsp` field at any given tree node stores a **relative** value — the absolute address minus the parent's grasp. As the version's tree grows through sequential `insertpm` calls and `setwispnd` rebalances, the relative `cdsp` values depend on tree shape (insertion order, splits) and will generally **differ numerically** from the source tree's `cdsp` values, even though the absolute I-addresses they encode are identical.

### I-Width Tumblers: Byte-Identical

From [SS-INSERT-VWIDTH-ENCODING] (Finding 0076):

> `movetumbler(&lwidth, &crumwidth.dsas[I])` — I-width is copied directly without transformation.

The I-width in the version's POOM crums is a byte-identical copy of the source's.

### V-Width Tumblers: Re-Encoded, But Numerically Identical If V-Addresses Match

The V-width is **recomputed** during `insertpm` via [SS-INSERT-VWIDTH-ENCODING]:

```
shift = tumblerlength(vsaptr) - 1
inc   = tumblerintdiff(&lwidth, &zero)
tumblerincrement(&zero, shift, inc, &crumwidth.dsas[V])
```

This produces a tumbler with `exp = -shift` and `mantissa[0] = inc`. Since CREATENEWVERSION copies the text subspace V-span structure intact (same V-positions, same widths), `vsaptr` lengths are the same in both source and version, so `shift` and `inc` are identical, producing **byte-identical V-width tumblers**.

### The Normalization Question

[SS-TUMBLER] (Finding 0031) establishes that after `tumblerjustify`, tumbler equality is unambiguous — "no normalization ambiguity." The I-address origins extracted by `specset2ispanset` are already in normalized form from the source POOM. When written into the version, they remain normalized. There is no recomputation pathway that could produce a different tumbler representation for the same logical I-address value.

### Summary

| Component | Mechanism | Result |
|---|---|---|
| I-address origin (absolute) | Read from source POOM via `specset2ispanset` | Byte-identical |
| I-address origin (as `cdsp`) | Recomputed by `setwispnd` as relative displacement | Numerically differs by tree position |
| I-width tumbler | `movetumbler` direct copy | Byte-identical |
| V-width tumbler | Re-encoded via `tumblerincrement` | Byte-identical (same V-positions) |

The key risk the question probes — whether re-encoding could produce a different tumbler representation for the same logical I-address — does not arise, because the I-origins are never re-encoded. They are extracted and stored as-is. The only re-encoding occurs for V-widths, and that re-encoding is deterministic given the same V-address inputs. [ST-VERSION, ST-VERSION-CREATE, SS-POOM-BOTTOM-CRUM, SS-INSERT-VWIDTH-ENCODING, INV-ENFILADE-RELATIVE-ADDRESSING]

---

## Code Exploration

I have all the evidence I need. Here is my complete answer.

---

## Answer

### The short answer

The I-displacements in the new version's POOM are **not byte-identical copies** of the original's — they are recomputed by a full V→I permutation traversal. However, for a simple (flat, single-level) source POOM the recomputed absolute I-addresses happen to equal the source's stored values. For a deep (multi-level) source POOM the recomputation accumulates partial sums via `tumbleradd`, and a latent limitation in `absadd` creates a narrow but real risk that the result differs in representation from what direct storage would produce.

---

### Execution path

**`docreatenewversion`** [`do1.c:260`] never copies POOM crums. It:

1. Calls `doretrievedocvspanfoo` → `retrievedocumentpartofvspanpm` [`orglinks.c:155`], which reads the root POOM node's `cdsp.dsas[V]` and `cwid.dsas[V]` directly:
   ```c
   movetumbler (&((typecuc *) orgl)->cdsp.dsas[V], &vspanptr->stream);
   movetumbler (&((typecuc *) orgl)->cwid.dsas[V], &vspanptr->width);
   ```
   This gives the overall V-span of the original document.

2. Builds a `vspec` with `docisa = *isaptr` (original doc) and `vspanset = &vspan` [`do1.c:285-288`], then calls `docopyinternal(taskptr, newisaptr, &vspan.stream, &vspec)` [`do1.c:293`].

**`docopyinternal`** [`do1.c:66`] calls `specset2ispanset` → `vspanset2ispanset` → `permute`. This does **not** copy crums; it walks the source POOM to produce an I-spanset.

**`permute`** [`orglinks.c:404`] calls `span2spanset` → `retrieverestricted` → `findcbcinarea2d` [`retrie.c:229`]. At each matching bottom-level crum, `makecontextfromcbc` is called.

**`makecontextfromcbc`** [`context.c:151`]:
```c
movewisp(offsetptr, &context->totaloffset);          // accumulated parent offset
movewisp(&crumptr->cwid, &context->contextwid);
if (crumptr->cenftype != GRAN)
    dspadd(&context->totaloffset, &crumptr->cdsp,    // + this crum's displacement
           &context->totaloffset, (INT)crumptr->cenftype);
```
`context->totaloffset.dsas[I]` is now the **absolute** I-address of this crum (sum of all relative displacements from tree root to this leaf).

**`context2span`** [`context.c:176`] extracts the output:
```c
movetumbler (&grasp.dsas[idx2], &foundspanptr->stream);  // stream = absolute I-address
tumblersub(&reach.dsas[idx2],&grasp.dsas[idx2],&foundspanptr->width);
```

**`insertpm`** [`orglinks.c:100-131`] unpacks this ispan and writes it into the new POOM:
```c
unpacksporgl (sporglset, &lstream, &lwidth, &linfo);
movetumbler (&lstream, &crumorigin.dsas[I]);
movetumbler (vsaptr, &crumorigin.dsas[V]);
...
insertnd (taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);
```

For the **first** insertion into the fresh empty document, `insertnd` → `doinsertnd` → `firstinsertionnd` [`insertnd.c:199`] stores the value directly:
```c
movewisp (origin, &ptr->cdsp);   // ptr->cdsp.dsas[I] = lstream
```

For **subsequent** insertions (multiple I-spans), `insertcbcnd` [`insertnd.c:263`] stores a *relative* displacement in the new tree:
```c
dspsub (origin, grasp, &new->cdsp, (INT)father->cenftype);
```
where `grasp` is the accumulated offset within the *new* POOM.

---

### Are they byte-identical?

**Structurally, no.** The source POOM stores relative I-displacements (each crum's offset relative to its parent). The new POOM receives absolute I-addresses derived from summing those relative displacements via `makecontextfromcbc` + `dspadd`. For all but the first inserted section (in a multi-section document), the new POOM's crums then re-derive relative displacements within the *new* tree, which will generally differ from the source's relative displacements.

**For a flat single-level source POOM** (no splits have occurred): the source's one bottom crum has `cdsp.dsas[I]` equal to the absolute I-address (since the parent offset is zero). `makecontextfromcbc` computes `dspadd(zero, crum->cdsp.dsas[I])`, which by the identity check in `functiontumbleradd` [`tumble.c:368`] returns the source value unchanged:
```c
if (iszerotumbler(bptr)){
    movetumbler (aptr, cptr);  return;
} else if (iszerotumbler(aptr)){
    movetumbler (bptr, cptr);  return;  // <-- hits here: zero + source_value = source_value
}
```
In this case the I-address reaching `insertpm` is byte-for-byte the original. For a **single-section** document the new POOM crum's `cdsp.dsas[I]` is then exactly the source value (via `firstinsertionnd`).

---

### Could recomputation produce different tumbler representations for the same logical I-address?

Yes — **in principle, for deep source POOMs** — due to a limitation in `absadd` [`tumble.c:444`].

When `aptr->exp == bptr->exp` (Case 1, the case that arises when both operands are at the same hierarchical scale):
```c
if (aptr->exp == bptr->exp) {
    answer.exp = aptr->exp;
    ansmant[0] = amant[0] + bmant[0];   // adds only first digits
    i = j = 1;
}
...
while ( j <= NPLACES -1 ) {    
    ansmant[j++] = bmant[i++];           // copies b's remaining digits; a's are discarded
}
```
`amant[1], amant[2], ...` are **never added to anything**. The code silently discards the higher-order digits of the first operand. This is correct only when the first operand's `mantissa[1:]` are all zero — i.e., when relative displacements are single-digit integers (the overwhelmingly common case in practice).

For a **deep source POOM** where a relative I-displacement at some level happens to have two significant digits (which could arise after complex splits and re-insertions), `dspadd` → `lockadd` → `tumbleradd` → `absadd` would silently drop those higher digits, producing a `totaloffset` that misrepresents the absolute I-address. The new POOM would then record a wrong I-address — not merely a different representation of the same address, but a genuinely wrong logical address.

---

### Summary

| Scenario | Byte-identical? | Same logical address? |
|---|---|---|
| Flat source POOM, single-section document | **Yes** | Yes |
| Flat source POOM, multi-section document | No (new tree reindexes) | Yes |
| Deep source POOM, all single-digit displacements | No | Yes |
| Deep source POOM, any multi-digit I-displacement | No | **Not guaranteed** — `absadd` drops `amant[1:]` [`tumble.c:462-484`] |

The V→I path via `specset2ispanset` → `makecontextfromcbc` → `context2span` → `insertpm` always recomputes I-addresses rather than copying them. For the nearly universal case of single-digit integer I-displacements, the recomputed logical I-addresses are correct and the new POOM faithfully reflects the original permascroll addresses. But `absadd`'s inability to carry from digit[0] into digit[1] means that any source POOM crum whose accumulated I-offset requires two significant mantissa digits will produce a silently corrupted I-address in the copy — a different tumbler representation pointing to a different logical I-address.
