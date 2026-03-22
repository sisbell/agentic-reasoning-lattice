## Question 9 [nelson]

> Must a rearrangement operation be expressible purely in terms of the document's own content stream, or can it reference content positions as they exist in other documents that share the same material?

## REARRANGE Operates Purely on the Document's Own Vstream

A rearrangement must be expressed entirely in terms of the document's own virtual byte stream. It cannot reference positions in other documents, even when those documents share the same Istream content.

### The Evidence

**REARRANGE is document-scoped.** The operation takes cuts that are positions within a single document:

> "Rearrange transposes two regions of text. With three cuts, the two regions are from cut 1 to cut 2, and from cut 2 to cut 3... With four cuts, the regions are from cut 1 to cut 2, and from cut 3 to cut 4." [LM 4/67]

**All editing operations target a specific document.** INSERT takes `<doc id>` and `<doc vsa>` (a document virtual stream address). DELETEVSPAN removes "the given span from the given document." REARRANGE follows the same pattern — the cuts are V-addresses within the target document.

**REARRANGE is a pure Vstream operation.** It changes the arrangement of content without touching Istream. The concept mapping in [LM 4/11] lists REARRANGE alongside other editing operations that modify Vstream only.

### Why Other Documents Are Irrelevant

The V-address space treats all content uniformly, regardless of origin:

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

> "Logical addressing of the byte stream is in the form of virtual spans, or vspans. These are sequences of bytes in the document's virtual byte stream, **regardless of their native origin.**" [LM 4/11]

A document's Vstream already includes transcluded content from other documents. When you rearrange, you operate on V-addresses — and those V-addresses cover both native and non-native bytes indistinguishably. There is no need (and no mechanism) to reach into another document's address space.

### The Key Distinction

- **REARRANGE** = reorder content within your document's Vstream arrangement. All cuts are V-addresses in your document.
- **COPY** = bring content from another document into yours. This is the only editing operation that crosses document boundaries: "The material determined by `<spec set>` is copied to the document determined by `<doc id>` at the address determined by `<doc vsa>`." [LM 4/67]

COPY is how foreign content enters your Vstream. Once it's there, REARRANGE (and DELETE, INSERT) work on V-addresses without knowing or caring where the bytes originated. The I-address encodes origin permanently, but the V-address — which is what editing operations use — is purely local.

### Principle

This follows from the Istream/Vstream separation. Istream is identity (permanent, global, shared across documents). Vstream is arrangement (ephemeral, local, per-document). Editing operations — including REARRANGE — work on arrangement, not identity. They are scoped to a single document's Vstream by design.
