## Question 1 [theory]

> When CREATENEWVERSION creates a new version, must the new document's content begin byte-for-byte identical to the source — preserving both the relative order of content and any repeated/transcluded material — or only the set of included content?

Based on the curated sources, I can answer this from Nelson's Istream/Vstream model and the CREATENEWVERSION operation definition.

## Answer

**The new version must begin as an exact copy of the source document's entire Vstream arrangement — preserving relative order and any repeated/transcluded spans — not merely the set of included content.**

### The operation copies "the contents," i.e., the arrangement

The CREATENEWVERSION definition is explicit that the new document inherits the source's *contents*, with ancestry recorded:

> "This creates a new document with the contents of document <doc id>. It returns the id of the new document. The new document's id will indicate its ancestry." (4/66) — `Design Intent/operations.md`

In Xanadu, a document is not a *set* of bytes — it is a Vstream *arrangement* (an ordering) over Istream content. CREATENEWVERSION produces "New Vstream arrangement, same Istream content" (`i-space-v-space.md`, FEBE operations table). Functionally it is transclusion of the whole document: "CREATENEWVERSION is effectively transclusion of entire document" / "New version transcludes all content from source" (`versions.md`, `transclusion.md`). Transcluding the whole document copies its arrangement, not an unordered set.

### Order is intrinsic to what a version is

Vstream is defined by ordinal position, and that position is what the arrangement encodes:

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document." (4/11) — `i-space-v-space.md`

> "Each version is a different Vstream arrangement over same Istream content" — `i-space-v-space.md`

Because a version *is* an arrangement, a newly forked version necessarily starts with the source's exact ordering. Divergence only comes later, through INSERT/DELETE/REARRANGE, each of which operates on the current arrangement (e.g., INSERT: "The v-stream addresses of any following characters in the document are increased by the length of the inserted text." (4/66), `operations.md`).

### Correspondence requires an identical starting arrangement

The whole point of versioning is intercomparison, which depends on positional correspondence via shared Istream origin:

> "This returns a list of ordered pairs of the spans of the two spec-sets that correspond." (4/70) — SHOWRELATIONOF2VERSIONS, `operations.md`

> "Links may be refractively followed from a point or span in one version to corresponding places in any other version. Thus a link to one version of a Prismatic Document is a link to all versions." (2/26) — `correspondence.md`

Immediately after CREATENEWVERSION the two versions must correspond span-for-span; that is only true if the new version begins byte-for-byte identical in both content *and* order. A "set of content" model could not support refractive link-following or word-for-word intercomparison.

### Repeated/transcluded material is preserved as-is

Since the new version copies the entire Vstream (the arrangement, including every span and its position), any Istream content that appears multiple times in the source — whether repeated native content or transcluded inclusions — is reproduced in the same positions. Nelson notes that included (non-native) bytes are "as much a logical part of a document as native bytes" (4/11, `i-space-addresses.md` / `sporgl-provenance.md`), so they travel with the version exactly like native content. A set-of-content model would collapse duplicates and lose those positions; the arrangement model preserves them.

### Summary

CREATENEWVERSION forks a complete copy of the source's Vstream: same content, same relative order, same repeated/transcluded spans in the same positions. It is "the contents of document" (4/66) understood as an arrangement, not an unordered set — which is exactly what makes correspondence, refractive link-following, and word-for-word intercomparison possible.

One caveat: the curated sources verify the *order-preserving / arrangement* semantics directly. The specific phrasing "byte-for-byte identical" and the explicit treatment of *repeated/duplicated* spans on versioning are inferences from the Vstream/Istream and correspondence model rather than a verbatim Nelson statement. If you need Nelson's exact words on duplicate-span handling under versioning, NEED_RAW: 2/45-2/47, 4/66-4/67.
