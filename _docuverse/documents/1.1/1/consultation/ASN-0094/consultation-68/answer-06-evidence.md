## Question 6 [evidence]

> In udanax-green's link store, do links admit endsets whose spans cover document-container addresses directly (the equivalent of `dom(Σ.M)` entities), or do they exclusively cover content-level entities within documents?

## KB Synthesis

## Link Endsets Cover Content-Level Entities Only

Links in udanax-green's endsets exclusively cover content-level entities (permascroll bytes indexed by permascroll I-addresses), not document-container addresses.

### What Endsets Actually Contain

Endsets are sets of sporgls, where each sporgl carries three fields [SS-SPORGL]:
- `sporglorigin` — an **I-address identifying content in the permascroll**
- `sporglwidth` — the width of the content span
- `sporgladdress` — the document ISA as provenance metadata

The `sporglorigin` is always a permascroll I-address pointing to character bytes. The document ISA appears only as provenance metadata, not as the addressed entity [SS-LINK-ENDPOINT Finding 0037].

### Document-Container Addresses Are Inaccessible as V-Space Content

Document-container addresses (e.g., `1.1.0.1.0.1`) live in the granfilade as structural keys — they index document orgls but are not mapped into any document's V-space. Since link endsets are built by converting V-spans to I-spans via `vspanset2sporglset` [ST-LINK-CREATE Finding 0037], and document-container addresses never appear as content at any V-position, they cannot enter an endset.

### The Permascroll / Orgl ISA Distinction

The KB explicitly partitions the I-address space into two non-comparable sorts [SS-CONTENT-IDENTITY Finding 0015]:

| Sort | Example | Semantics |
|------|---------|-----------|
| Permascroll I-addresses | `2.1.0.5.0.123` | Content-bearing, shareable via transclusion |
| Link/doc orgl ISAs | `1.1.0.1.0.1.0.2.1` | Identity-bearing, unique — represent object identity |

Only permascroll addresses form valid endset content. Orgl ISAs are "unique references, not shareable content" [SS-CONTENT-IDENTITY Finding 0015]. `compare_versions` and link discovery rely on I-span intersection, which is only semantically defined over permascroll addresses.

### Link References at V:2.x Are Not Endset Targets

The 2.x V-subspace stores link orgl ISAs inside a document's V-stream [SS-DUAL-ENFILADE Finding 0009]. While the backend's unenforced convention (`acceptablevsa()` always returns TRUE [SS-SUBSPACE-CONVENTION Finding 0010]) means one could technically construct a link whose endset spans V:2.x, the resulting sporgls would carry link orgl ISAs — a convention violation that breaks link discovery and `compare_versions` [PRE-COMPARE-VERSIONS Finding 0009; EC-COMPARE-VERSIONS-LINK-CRASH].

### Precondition Confirms Content-Only Scope

The precondition for link creation requires "source content exists AND target content exists AND both endpoint widths >= 1" [PRE-LINK-CREATE Finding 0028]. The "content" here is permascroll content — the V-span at 1.x. No mechanism exists to link to a document-container address because such addresses are never in a document's content stream.

**Conclusion:** Link endsets exclusively cover content-level entities — permascroll bytes at permascroll I-addresses. Document-container addresses (`dom(Σ.M)`) are structural index entries inaccessible from V-space, and therefore cannot appear in any link endset.

---

## Code Exploration

I now have everything needed for a complete, code-grounded answer.

---

## Link Endsets: Document-Container vs. Content-Level Addressing

**Short answer**: Link endsets exclusively cover content-level entities within documents. Document-container addresses (`dom(Σ.M)` ISAs) cannot be span targets in an endset; they appear only as *locators* identifying which document a span lives in.

---

### The Endset Data Model

The entry point is `typevspec` [`xanadu.h:78-83`]:

```c
typedef struct structtypevspec {
    struct structtypevspec *next;
    typeitemid itemid;
    typeisa docisa;          /* document-container ISA — locator only */
    typevspanset vspanset;   /* content spans WITHIN that document */
} typevspec;
```

`docisa` is a tumbler from `dom(Σ.M)` — a document ISA — but it plays the role of **locator**, not span target. The actual endset coordinates are the `typevspanset` spans, which are V-addresses within the named document's content space.

The stored form is `typesporgl` [`xanadu.h:115-121`]:

```c
typedef struct structsporgl {
    struct structsporgl *next;
    typeitemid itemid;
    tumbler sporglorigin;    /* I-address (permascroll position) */
    tumbler sporglwidth;
    typeisa sporgladdress;   /* document ISA — again a locator */
} typesporgl;
```

After conversion, every endset entry is `(permascroll_position, document_ISA)`. The coordinate is always an I-address (content position), never a document-container ISA itself.

---

### The Creation Path

`docreatelink` [`do1.c:195-221`] takes three `typespecset` endset arguments and routes each through:

1. **`specset2sporglset`** [`sporgl.c:14-33`] — dispatches on item type:
   - `ISPANID`: raw I-spans pass through unchanged (content addresses)
   - `VSPECID`: calls `vspanset2sporglset`, which calls `vspanset2ispanset` → `permute(V→I)` [`orglinks.c:397-401`]

2. **`permute`** [`orglinks.c:404+`] — converts V-addresses (virtual, document-internal) to I-addresses (permascroll) using the document's enfilade. These are content-level coordinates, not ISA tumblers.

3. **`insertendsetsinspanf`** → **`insertspanf`** [`spanf1.c:15-54`] — writes sporgls into the spanfilade under `LINKFROMSPAN` (1), `LINKTOSPAN` (2), or `LINKTHREESPAN` (3) span-type slots using `SPANRANGE` (content) coordinates.

There is no code path that accepts a document-container ISA as the `sporglorigin`/`stream` of an endset span.

---

### The V-Address Partition Confirms the Boundary

`filter_vspanset_to_text_subspace` [`do1.c:386-411`] makes the partition explicit:

```c
/* V < 1.0: link metadata (sub-document structure)
 * V >= 1.0: text/content subspace */
tumblerincrement(&text_subspace_start, 0, 1, &text_subspace_start); /* → 1.0 */
if (tumblercmp(&vspanset->stream, &text_subspace_start) >= EQUAL) {
    /* keep — text subspace */
} /* else: skip — link metadata */
```

`setlinkvsas` [`do2.c:169-183`] shows where the three endsets are *stored* within the link document: V-addresses `1.1`, `2.1`, `3.1` (from/to/three). These are the link's internal V-space slots — not a constraint on what spans the endsets point at, but the metadata addresses within the link document itself.

`DOCISPAN` (4) [`xanadu.h:39`] is a distinct span-type constant used *only* by `docopy`/`docopyinternal` [`do1.c:62, 79`] for document-copy tracking — it is never passed to `insertspanf` during link creation.

---

### Conclusion

Links in udanax-green **cannot** have endsets whose spans cover document-container addresses. The `typevspec.docisa` field identifies which document the spans live in, but it is strictly a locator. Span coordinates (both at rest as V-addresses in `typevspanset` and after conversion as I-addresses in `typesporgl`) are always content-level positions within a document's permascroll. There is no discriminant, code path, or span-type constant that would allow a `dom(Σ.M)` ISA to serve as the stream/origin of an endset span entry.
