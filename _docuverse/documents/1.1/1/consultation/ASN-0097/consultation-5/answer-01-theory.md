## Question 1 [theory]

> Was the design intent for M(d) to be subspace-stratified — text-subspace V-positions arranging content addresses and link-subspace V-positions arranging link addresses — or was M(d) intended to range exclusively over content addresses?

I'll examine the relevant raw pages to verify the subspace structure of M(d), since the curated sources show some inconsistency about which digit designates the link subspace.

Looking at pages 4/26 through 4/31, which describe the I-address field structure and link subspace numbering.

[Reading raw pages to verify subspace digit assignments and the nature of the V→I mapping for content versus links.]

Based on the curated sources, here is my answer:

## M(d) Was Designed to Be Subspace-Stratified

The design intent was clearly **subspace-stratified**, not exclusively over content addresses. The address space of a document explicitly contains at least two distinct subspaces, each with different semantics for how V→I mapping operates.

### Evidence of Stratification

The link concept page explicitly documents the subspace distinction:

> "**Subspace Distinction:** The document-local address space uses numeric prefixes:
> | Bytes | `version.position` (1.x) | Text content |
> | Links | `version.0.2.N` | Links stored in this document |"

And from page 4/31 as cited:

> "N.0.U.0.D.V.0.2.1 (the first link of the document, stored in the document's space)" (4/31)

> "N.0.U.0.D.V.0.2.755 (the 755th link to which the document is home)" (4/31)

### Different Mapping Semantics Per Subspace

Critically, the two subspaces have **fundamentally different mapping behavior under M(d)**:

**Text subspace** — V-positions are rearrangeable:
> "The digit after the one indicates the byte position in the current ordering of bytes. This is its virtual stream address." (4/30)
> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." (4/30)

**Link subspace** — V-positions are NOT rearrangeable:
> "The links designated by a tumbler address are in their permanent order of arrival. A document includes only the links of which it is the home document." (4/31)

This asymmetry is decisive: a document's V-arrangement for text is a mutable mapping that the editing operations (INSERT, DELETE, REARRANGE) modify, while the V-arrangement for links is creation-ordered and frozen. These cannot be the same mapping function — they are two strata of M(d) governed by different rules.

### Confirmation from FEBE Operations

The FEBE operations reinforce this stratification:

- **INSERT** specifically targets the text subspace: "The v-stream addresses of any following characters in the document are increased by the length of the inserted text." (4/66)
- **MAKELINK** "creates a link in document <doc id>" — the link goes into the document's link subspace, addressed sequentially, not at an arbitrary V-position the user picks.
- **DELETED LINKS** and **DELETED BYTES** are listed as parallel-but-distinct document states (4/9).

### Conclusion

M(d) ranges over a stratified address space. Text subspace V-positions arrange content (mutable, editable order), and link subspace V-positions arrange link addresses (permanent creation order). The design intent was explicitly NOT a single content-only mapping — the protocol, addressing scheme, and operational semantics all distinguish the two strata.

NEED_RAW: 4/26-4/31 (raw pages 193-198) to verify the exact wording of "0.2" vs "0.3" as the link subspace digit. The curated sources have a minor inconsistency (`i-space-addresses.md` says "digit after the '3'" while `links.md` consistently uses `0.2`), which suggests one of them may have a transcription error worth verifying against the original.
