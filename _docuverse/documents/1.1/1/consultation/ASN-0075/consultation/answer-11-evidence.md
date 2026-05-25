## Question 11 [evidence]

> Given two documents sharing history (via CREATENEWVERSION), can the difference between their POOMs be computed as the set-difference of I-address ranges, and does the implementation expose such an operation?

## KB Synthesis

## POOM Difference as I-Address Set-Difference

### Conceptual Correctness

Yes, the difference between two POOMs can be expressed as I-address set-difference — with significant caveats.

At version creation, both documents have identical I-address sets in their POOMs [ST-VERSION-CREATE]: `iaddrs(version) = iaddrs(original)`. Subsequent edits diverge the sets:

- **INSERT** adds fresh I-addresses to the modified document only [ST-INSERT], [INV-MONOTONIC]
- **DELETE** removes V→I mappings from the POOM but does **not** remove I-addresses from the granfilade [ST-DELETE], [FC-GRANF-ON-DELETE]
- **REARRANGE** does not change the I-address set at all [INV-REARRANGE-IDENTITY]

So for two documents A and B sharing a version ancestor:

```
shared(A, B)  = { i | poom_A maps some v to i } ∩ { i | poom_B maps some v to i }
unique_to_A   = iaddrs(A) \ iaddrs(B)
unique_to_B   = iaddrs(B) \ iaddrs(A)
```

The model holds at the POOM level (current V→I mappings). It is **not** the same as a granfilade or spanfilade set-difference — the granfilade is append-only and retains all I-addresses ever allocated [INV-NO-IADDR-REUSE]; the spanfilade retains stale entries after deletion [INV-SPANF-WRITE-ONLY], [EC-STALE-SPANF-REFERENCE].

### Key Caveats

**REARRANGE is invisible in this model.** Because rearrange preserves I-addresses [INV-REARRANGE-IDENTITY], content that was rearranged in one document appears as "shared" even though its V-position differs. The set-difference captures *what* changed but not *where* it moved.

**The POOM is a multimap** [SS-POOM-MULTIMAP]. The same I-address can appear at multiple V-positions (via internal transclusion). The I-address *set* (not multiset) difference discards this multiplicity — two documents could have the same I-address set but differ in how many times each appears.

**Deletion creates an asymmetry.** If A deletes content that was in both A and B at version creation, the deleted I-addresses disappear from A's POOM but remain in both the granfilade and B's POOM. The set-difference correctly captures these as "in B only" [ST-DELETE], [FC-DELETE-CROSS-DOC].

### Implementation Exposure

**The implementation does not directly expose the set-difference.** It exposes:

1. **`compare_versions` / `SHOWRELATIONOF2VERSIONS`** [SS-COMPARE-VERSIONS] — computes the I-address *intersection* and returns paired V-span correspondences. This is the shared portion only.

2. **`RETRIEVEDOCVSPANSET`** [SS-VSPAN-VS-VSPANSET] — returns each document's full V-span set, from which total I-address coverage can be derived per document.

To compute the difference, a client must:
1. Call `compare_versions(A, B)` → get shared V-spans
2. Call `retrieve_vspanset(A)` and `retrieve_vspanset(B)` → get full extents
3. Subtract shared spans from each document's total — the remainder is the unique content

This is **client-side arithmetic**, not a backend primitive.

**Critical implementation constraint:** `compare_versions` crashes when either document contains links [EC-COMPARE-VERSIONS-LINK-CRASH], [PRE-COMPARE-VERSIONS]. Both documents must be filtered to the text subspace (V-positions in 1.x) before the comparison. Link subspace content (2.x) must be excluded from any set-difference computation.

**`FINDDOCSCONTAINING` cannot substitute** for POOM-based difference. It queries the spanfilade, which is write-only and retains stale entries after deletion [INV-SPANF-WRITE-ONLY]. It returns a superset of current POOM associations [EC-STALE-SPANF-REFERENCE], making it unsuitable for accurate difference computation.

### Summary

The POOM difference-as-I-address-set-difference model is **conceptually correct** at the level of current document state. The implementation exposes the intersection (`compare_versions`) but not the difference directly — the difference must be assembled client-side from the intersection and individual document extents, restricted to the text subspace to avoid crashes.

---

## Code Exploration

I now have everything I need. Here is the full answer.

---

## Can POOM Differences Be Computed as I-Address Set-Difference?

### How `CREATENEWVERSION` Establishes Shared History

`docreatenewversion` [`do1.c:260`] follows four steps:

1. **Allocate a new document ISA** via `createorglingranf` [`do1.c:277`].
2. **Retrieve the ancestor's full V-span** — `doretrievedocvspanfoo` [`do1.c:281`] calls `findorgl` + `retrievedocumentpartofvspanpm` to obtain the parent's entire content range as a `typevspan`.
3. **Wrap it in a `typevspec`** [`do1.c:285–288`], which binds the V-span to the ancestor's ISA:
   ```c
   movetumbler(isaptr, &vspec.docisa);   /* ancestor's identity */
   vspec.vspanset = &vspan;              /* ancestor's V-range  */
   ```
4. **Call `docopyinternal`** [`do1.c:293`], passing the new document's ISA, the ancestor's V-start address, and the `vspec`.

`docopyinternal` [`do1.c:66`] then:
- Calls `specset2ispanset` [`do1.c:74`] → `do2.c:14`] to resolve the ancestor's V-spans into I-spans (permascroll addresses) via the ancestor's POOM.
- Calls `insertpm` and `insertspanf` to insert those I-spans into the *new* document's POOM, mapping them to the new document's V-address space.

**The result**: both documents' POOMs contain entries referencing the same I-address ranges. The I-space (permascroll) is global and shared; each document has its own independent POOM tree, but those trees point into overlapping regions of the same I-space.

---

### What a POOM Entry Looks Like

From `insertnd.c:100–117`, each crum in a POOM has two coordinate dimensions:

```c
movetumbler(&lstream, &crumorigin.dsas[I]);   /* I-dim: permascroll address */
movetumbler(&lwidth,  &crumwidth.dsas[I]);    /* I-dim: width               */
movetumbler(vsaptr,   &crumorigin.dsas[V]);   /* V-dim: document position   */
```

A POOM is thus a 2D enfilade (`cenftype = POOM` [`enf.h:13`]) that records bijective mappings: *this I-range lives at this V-position in this document*.

---

### Can the Difference Be Expressed as I-Address Set-Difference?

**Theoretically yes.** Because I-addresses are the global identity of content (permascroll), the set-theoretic relationship holds:

- **V₁.I_ranges ∩ V₂.I_ranges** = content shared by both versions (the inherited permascroll content).
- **V₁.I_ranges \ V₂.I_ranges** = content unique to V₁ (inserted after the fork, or deleted from V₂).
- **V₂.I_ranges \ V₁.I_ranges** = content unique to V₂.

This is the correct Xanadu semantic: I-addresses are content identity, not position, so the POOM delta between two related documents is exactly the symmetric difference of their I-span sets.

---

### What the Implementation Actually Exposes

**Intersection — yes, fully implemented:**

`doshowrelationof2versions` [`correspond.c:428`] implements the shared-content query:

```c
specset2ispanset(taskptr, version1, &version1ispans, READBERT)    /* V→I for doc1 */
&& specset2ispanset(taskptr, version2, &version2ispans, READBERT) /* V→I for doc2 */
&& intersectspansets(taskptr, version1ispans, version2ispans,
                     &commonispans, ISPANID)                       /* I₁ ∩ I₂     */
&& ispansetandspecsets2spanpairset(taskptr, commonispans,
                                   version1, version2, relation)  /* build pairs  */
```

`intersectspansets` [`correspond.c:145`] does a nested pairwise loop over the two span lists, calling `comparespans` → `spanintersection` [`correspond.c:210`] to compute each overlap range using tumbler arithmetic.

**Set-difference — partially present, but not composed into a full operation:**

`spansubtract` [`correspond.c:363`] exists, but it operates on a single pair of spans (comparing widths) and returns a residual:

```c
case GREATER:
    tumbleradd(&aptr->stream, &bptr->width, &cptr->stream);
    tumblersub(&aptr->width,  &bptr->width, &cptr->width);
```

This is a scalar span residual, not a set-difference of span lists. There is **no `subtractspansets`**, no `diffspansets`, and no function that takes two `typeispanset` lists and returns their set-difference as a new list.

`restrictspecsetsaccordingtoispans` [`correspond.c:18`] and `removespansnotinoriginal` [`correspond.c:92`] come closest: they restrict a specset to spans present in another specset (using `intersectspansets` internally [`correspond.c:116`]), which is the equivalent of retaining the intersection, not computing the complement.

**`specset2ispanset`** [`do2.c:14`] performs the V→I projection through a document's POOM (via `permute` / `vspanset2ispanset` [`orglinks.c:397`]), which is the prerequisite for any set operation on I-ranges.

---

### Summary

| Operation | Theoretical Validity | Implementation |
|---|---|---|
| I-addresses as content identity across versions | Yes — by design | Built into POOM structure [`insertnd.c:105`] |
| V→I projection per document | Yes | `specset2ispanset` → `vspanset2ispanset` → `permute` [`orglinks.c:397`] |
| I-span intersection (shared content) | Yes | `intersectspansets` [`correspond.c:145`], used in `doshowrelationof2versions` [`correspond.c:428`] |
| I-span set-difference (unique content) | Yes, theoretically correct | **Not implemented** — `spansubtract` [`correspond.c:363`] handles only single-span residuals, no list-level set-difference exists |

**Conclusion**: The architectural premise is correct — two documents sharing history through `CREATENEWVERSION` do share I-address ranges corresponding to their common content, and the POOM difference is exactly the I-address set-difference. However, the implementation only exposes the *intersection* (shared content) through `doshowrelationof2versions`. Computing content *unique to one version* (the set-difference complement) would require a `subtractspansets` built from the existing tumbler arithmetic in `spansubtract` [`correspond.c:363`] and the `typeispanset` linked-list infrastructure — the machinery is present, but the composition is absent.
