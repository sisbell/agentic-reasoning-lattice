## Question 11 [gregory]

> When `docopy` creates a new POOM entry in the target document, does the bottom crum's I-displacement point to the exact same I-address as the source POOM entry, or is there any indirection or remapping layer between the source's I-address and the target's?

## KB Synthesis

**Direct answer: The I-displacement in the target POOM bottom crum is the exact same I-address as in the source — no indirection, no remapping.**

## Mechanism

The call chain makes this explicit [ST-VCOPY, Finding 0046]:

```
docopy(src, dst, vsa, ispanset)
  → insertpm(dst, vsa, ispanset)
  → insertnd(...)
  → isanextensionnd() or new crum creation
```

The sporgl is the carrier [INT-SPORGL-TRANSCLUSION]:

> "During vcopy, the data flow is: source V-spec → sporgls (via `vspanset2sporglset`) → `insertpm` into destination document. The sporgl carries the content's I-address identity through the copy operation. Because the sporgl preserves the original I-address (not a new one), the destination document ends up referencing the same content identities as the source."

The resulting bottom crum [SS-POOM-BOTTOM-CRUM] has:
- `cdsp.dsas[I]` = the I-address extracted from the source POOM — the **binary tumbler value is copied directly**
- `cdsp.dsas[V]` = the target V-position (re-encoded at V-space precision per [SS-INSERT-VWIDTH-ENCODING])

## No New Allocation

`docopy` never calls `findisatoinsertgr` or `inserttextingranf`. Contrast with INSERT, which calls those to allocate fresh I-addresses. [INV-IADDR-PROVENANCE]:

> "Every I-address has exactly one native document — the document where INSERT first allocated it. COPY does not allocate new I-addresses; it creates V→I mappings that reference existing ones."

## The `homedoc` Field

The `isanextensionnd` check [ST-VCOPY, Finding 0046] uses the `homedoc` field to test I-address origin — and this field records the **original allocation document**, not the current copy source. After a chain of three COPYs (A → B → C → D), the bottom crum in D's POOM still has `homedoc = A`. This is what makes transitive I-address contiguity work (or fail to consolidate across different origins).

## What Confirms This

[ST-COPY, Finding 0064]:

> "COPY is the identity-preserving operation... COPY shares the source's existing I-addresses in the target document's POOM via `insertpm`. When used to 'undelete' content... COPY restores both the V-space content AND the I-space identity."

[INV-TRANSITIVE-IDENTITY] — transitive transclusion works exactly because the I-addresses flow unchanged through the chain. If there were any remapping layer, the I-address intersection in `find_links` and `compare_versions` would break.

**Conclusion:** The target POOM bottom crum's `cdsp.dsas[I]` is the same tumbler bit-pattern as in the source entry. The sporgl is the literal carrier of that address through the copy path, and `insertpm` writes it directly into the new crum without transformation.

---

## Code Exploration

I now have everything needed to answer definitively. Here is the full analysis.

---

## Answer: I-Address in `docopy` — Direct Reference, No Remapping

The bottom crum in the target POOM gets the **exact same I-address** as the source. There is no indirection, offset, or remapping layer. Here is the full call chain with citations.

---

### Step 1 — `docopy` converts V-specs to I-spans

`do1.c:53-64`:
```c
return (
   specset2ispanset (taskptr, specset, &ispanset, NOBERTREQUIRED)
&& findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
...
/* the meat of docopy: */
&& insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset)
...
```

The `specset` parameter is typically a `VSPECID` (V-addresses in the *source* document). `specset2ispanset` converts them to I-spans by calling `vspanset2ispanset` → `permute(..., V, ispansetptr, I)` — walking the **source document's POOM** to find which I-addresses back those V-positions [`do2.c:34-38`]:
```c
findorgl (taskptr, granf, &((typevspec *)specset)->docisa, &docorgl, type)
&& (ispansetptr = vspanset2ispanset (taskptr, docorgl, 
                    ((typevspec *)specset)->vspanset, ispansetptr))
```

The resulting `ispanset` contains the **raw permascroll I-addresses** of the content. These are copied verbatim — `permute` does not relativize or offset them.

---

### Step 2 — `insertpm` builds the new crum from those I-addresses

`orglinks.c:100-131`:
```c
for (; sporglset; sporglset = ...) {
    unpacksporgl (sporglset, &lstream, &lwidth, &linfo);   // extracts I-addr

    movetumbler (&lstream, &crumorigin.dsas[I]);   // I-address goes in directly
    movetumbler (&lwidth,  &crumwidth.dsas[I]);    // I-width goes in directly
    movetumbler (vsaptr,   &crumorigin.dsas[V]);   // target V-address

    shift = tumblerlength (vsaptr) - 1;
    inc   = tumblerintdiff (&lwidth, &zero);
    tumblerincrement (&zero, shift, inc, &crumwidth.dsas[V]); // derives V-width

    insertnd (taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);
    tumbleradd (vsaptr, &crumwidth.dsas[V], vsaptr);  // advance V for next span
}
```

`lstream` is placed **directly** into `crumorigin.dsas[I]` with a plain `movetumbler` — a raw value copy with no arithmetic.

---

### Step 3 — `unpacksporgl` confirms no transformation on the I-side

`sporgl.c:178-202`. For an ISPANID element (which is what `specset2ispanset` produces):
```c
if (((typeitemheader *)sporglptr)->itemid == ISPANID) {
    movetumbler (&((typeispan *)sporglptr)->stream, streamptr);  // straight copy
    movetumbler (&((typeispan *)sporglptr)->width,  widthptr);
    tumblerclear (&infoptr->homedoc);                            // no home doc
}
```

No addition, no indirection. The `stream` field — which is the I-address produced by `permute` from the source POOM — passes through unchanged as `lstream`, and then becomes `crumorigin.dsas[I]` in the new target crum.

---

### Step 4 — `isanextensionnd` shows I-address identity is the crum's identity

`insertnd.c:301-309`: when deciding whether to extend an existing crum rather than create a new one, the check is:
```c
bool isanextensionnd(typecbc *ptr, ..., type2dbottomcruminfo *infoptr)
{
    if (!tumblereq (&infoptr->homedoc, &((type2dcbc *)ptr)->c2dinfo.homedoc))
        return (FALSE);
    prologuend ((typecorecrum*)ptr, offsetptr, &grasp, &reach);
    return (lockeq (reach.dsas, originptr->dsas, dspsize(ptr->cenftype)));
}
```

Two POOM entries are considered the *same run* of I-space only if they share the same `homedoc` and are I-address-contiguous. This only makes sense because I-addresses in both source and target POOMs are the same permascroll-absolute values.

---

### Conclusion

When `docopy` creates a new POOM entry in the target document:

1. The input V-addresses (in the source document) are **translated to I-addresses** by walking the *source document's* POOM via `specset2ispanset` / `vspanset2ispanset` / `permute`.
2. Those I-addresses are then placed **verbatim** into `crumorigin.dsas[I]` of the new target crum — `movetumbler` with no arithmetic [`orglinks.c:105`].
3. The only thing that changes is the `dsas[V]` component — the target V-address, supplied by the caller as `vsaptr`.

The target POOM crum's I-displacement points to the **identical permascroll I-address** as the source POOM crum. There is no indirection, remapping, or offset layer between them. Both documents' POOM trees point to the same I-space location; only the V-space position differs. This is the structural mechanism that makes transclu- content-sharing possible in udanax-green.
