## Question 3 [nelson]

> When an editing action breaks a contiguous mapping unit into two pieces, what properties must each resulting piece independently preserve about its relationship to the original content?

## Properties Preserved When a Mapping Unit Splits

When an editing operation (INSERT, REARRANGE, DELETE of interior content) breaks a contiguous V→I mapping unit into two pieces, each resulting piece must independently preserve these properties:

### 1. I-address Mapping Fidelity

Each piece must continue to reference the **exact same I-addresses** as the corresponding portion of the original unit. Nothing changes in Istream; only the Vstream arrangement is altered.

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." [LM 4/11]

INSERT explicitly modifies only V-addresses: "The v-stream addresses of any following characters in the document are increased by the length of the inserted text." [LM 4/66]. The I-addresses are untouched.

### 2. Origin Traceability

Each piece independently encodes its content's home document in the I-address structure (`Node.0.User.0.Document.0.Element`). This is structural, not metadata — it cannot be severed by splitting.

> "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

Both pieces independently answer the question "where did this come from?" because each byte's I-address carries the answer.

### 3. Link Attachment

Links attached to bytes in the original unit remain attached to those same bytes regardless of which piece they end up in. Nelson is explicit that links bind to **bytes**, not to mapping units or positions:

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." [LM 4/30]

> "Links between bytes can survive deletions, insertions and rearrangements, if anything is left at each end." [LM 4/43]

Each piece independently serves as a valid link anchor. A link whose endset spans the split point now has its bytes distributed across two pieces, but the link survives because content at each end still exists.

### 4. Correspondence

Each piece independently establishes correspondence with any other V-position (in other versions or documents) that shares the same I-addresses. Version comparison works piece-by-piece because correspondence is a relation derived from shared Istream origin, not from the contiguity of the mapping.

> "a facility that holds multiple versions of the same material, and allows historical backtrack, is not terribly useful unless it can help you intercompare them in detail—unless it can show you, word for word, what parts of two versions are the same." [LM 2/20]

SHOWRELATIONOF2VERSIONS "returns a list of ordered pairs of the spans of the two spec-sets that correspond" [LM 4/70]. After a split, the correspondence computation produces two pairs where it previously produced one — but the relationship to the original content is fully preserved.

### 5. Transclusion Identity

If the original mapping unit was an inclusion (virtual copy), each piece independently remains a valid reference to its portion of the source content.

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

Each piece independently maintains the property of being "native elsewhere" — the transclusion relationship is per-byte, not per-mapping-unit.

### 6. Canonical Structural Validity

After the split, the document must remain in valid internal form. Nelson describes this as "canonical order" — the mandate that all changes leave the structure valid:

> "All changes, once made, left the file remaining in canonical order, which was an internal mandate of the system." [LM 1/34]

Each piece is a self-contained mapping unit that the enfilade can manage independently. The split produces two units that together cover exactly the same I-addresses as the original, with no gaps and no overlaps.

---

### Summary

The core principle is that **splitting is a Vstream operation that must be invisible to Istream properties**. Each piece inherits every property that derives from I-address identity: traceability, link attachment, correspondence, transclusion identity. The split changes how content is *arranged* (Vstream) without affecting what content *is* (Istream). This is the direct consequence of Nelson's separation of content from arrangement — the design choice that makes editing non-destructive.
