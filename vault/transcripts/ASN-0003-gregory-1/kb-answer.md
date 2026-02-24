## REARRANGE

REARRANGE operates purely in V-space — it reorders existing POOM entries by adding computed offsets to their V-dimension displacements. No I-addresses are allocated, freed, or modified. [INV-REARRANGE-IDENTITY]

### Two modes

**Pivot (3 cuts)** `rearrange(doc, [c0, c1, c2])` swaps two adjacent regions:
- Region 1 = `[c0, c1)`: offset `+= c2 - c1` (moves right by size of region 2)
- Region 2 = `[c1, c2)`: offset `-= c1 - c0` (moves left by size of region 1)
- Content outside `[c0, c2)`: unchanged [FC-REARRANGE-EXTERIOR]

Example: `"ABCDE"`, cuts `[1.2, 1.4, 1.6]` → `"ADEBC"`

**Swap (4 cuts)** `rearrange(doc, [c0, c1, c2, c3])` swaps two non-adjacent regions, preserving the middle:
- Region 1 = `[c0, c1)`: offset `+= c2 - c0`
- Middle `[c1, c2)`: offset `+= (c3 - c2) - (c1 - c0)` (shifts only if regions differ in size)
- Region 3 = `[c2, c3)`: offset `-= c2 - c0`

Example: `"ABCDEFGH"`, cuts `[1.2, 1.4, 1.6, 1.8]` → `"AFGDEBCH"`

### Mechanism

`sortknives()` normalizes cut order (misordered inputs silently accepted). `makeoffsetsfor3or4cuts()` computes offsets from cut positions alone — all in the pre-move address space. `rearrangecutsectionnd()` classifies each POOM crum by section. `tumbleradd()` applies offset to each crum's V-displacement in place. [ST-REARRANGE Finding 0056]

### Preconditions

- Exactly 3 or 4 cuts — enforced; 2 cuts causes abort. [PRE-REARRANGE Finding 0006]
- Cut points in valid V-space — not enforced.
- All cuts within same subspace — **not enforced**. Cross-subspace cuts produce cross-subspace content displacement, violating content discipline. [EC-REARRANGE-CROSS-SUBSPACE, PRE-REARRANGE Finding 0051]
- WRITEBERT token — advisory only; response is sent before the check. [EC-RESPONSE-BEFORE-CHECK]

---

## COPY (docopy / vcopy)

COPY shares existing I-addresses from a source span into the target document's POOM at a specified V-position. Unlike INSERT, it does **not** allocate fresh I-addresses — it places existing ones. This is the mechanism by which content identity is preserved across transclusion. [ST-VCOPY Finding 0002]

### Shifting behavior

COPY uses the identical POOM insertion path as INSERT: `insertpm → insertnd → makegappm`. [ST-INSERT Finding 0052]

`makegappm` shifts all POOM entries within `[insertion_point, next_subspace_boundary)` rightward by the copied width. So yes — COPY shifts subsequent content exactly like INSERT. Content before the target position is unchanged; content at or after is displaced. [FC-SUBSPACE, SS-TWO-BLADE-KNIFE]

### Coalescing

`isanextensionnd()` checks if the new mapping is contiguous with an adjacent crum (same `homedoc` AND reach == new origin in both V and I dimensions). If so, the existing crum's width is extended in place (zero new crums). Otherwise, a new crum is created. This is rightward-only extension. [ST-VCOPY Finding 0046]

Crums from different source documents are never merged — the `homedoc` field preserves provenance. [INV-IADDR-PROVENANCE]

### DOCISPAN creation

COPY calls `insertspanf(..., DOCISPAN)` — one entry per I-span in the source, not per byte. So copying k contiguous bytes creates 1 DOCISPAN entry; copying fragmented content (N I-spans) creates N entries. [SS-DOCISPAN Finding 0047]

### Preconditions

From [PRE-COPY Finding 0046]:
- Source document must exist and be valid
- Source V-span must have content
- Target document must exist and be valid
- Both documents must be open (required by `findorgl`) [PRE-RETRIEVE-CONTENTS, SS-DOCUMENT-LIFECYCLE]
- **No** uniqueness precondition: the same I-addresses may already exist in the target at other V-positions. Repeated copies of the same content are accepted unconditionally. `insertpm` does not check for duplicate I-addresses.
- Subspace convention must be respected by the caller (not enforced). [PRE-SUBSPACE-CONVENTION]

### Key distinction from INSERT

| Property | INSERT | COPY |
|----------|--------|------|
| I-address allocation | Fresh addresses allocated | Existing addresses shared |
| Content identity | New, disjoint from all prior | Preserved from source |
| `compare_versions` result | No shared span with prior content | Shared span with source |
| DOCISPAN | Created | Created |
| V-space shift | Yes, via `makegappm` | Yes, same path |
| Self-operation | N/A | `source == target` is valid [EC-SELF-TRANSCLUSION] |

COPY is the identity-preserving restoration mechanism: after DELETE removes content from V-space, COPY from a version retaining the original I-addresses is the only way to restore identity. INSERT at the same position creates unrelated new I-addresses. [INV-DELETE-NOT-INVERSE]