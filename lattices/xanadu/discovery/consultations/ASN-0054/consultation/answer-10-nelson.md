## Question 10 [nelson]

> When two documents share the same original content, must their arrangements reference that content identically, or can each document's arrangement decompose the shared content into differently sized pieces?

## Each Document Independently Decomposes Shared Content

No, arrangements need not reference shared content identically. Each document's V-space arrangement is an independent mapping from V-positions to I-space addresses, and there is no requirement that two documents decompose shared I-space content into spans of the same size.

### The V→I Mapping Is Per-Document

The document IS its V→I mapping. From the curated sources on V-space:

> "The mapping V -> I is the essence of document structure. The document IS the mapping from V-addresses to I-addresses. Each version defines a different mapping."

Each document independently defines how it arranges references to I-space content. Two documents that share the same underlying bytes maintain entirely separate V-space arrangements.

### Editing Operations Explicitly Break Span Boundaries

Nelson's editing operations demonstrate that span decomposition changes freely:

**REARRANGE** transposes regions of text [LM 4/67]. If Document A references I-space bytes 100-199 as one contiguous span, and the user rearranges by cutting at byte 150, the single span becomes two spans in a different order. The I-space content is unchanged; only the V-space decomposition differs.

**INSERT** shifts V-addresses and can split a transcluded span in two [LM 4/66]:

> "The v-stream addresses of any following characters in the document are increased by the length of the inserted text."

If you insert new content in the middle of a transcluded passage, the single I-space reference splits into two separate spans flanking the insertion.

**DELETE** removes from V-space without affecting I-space [LM 4/9]:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)"

Deleting part of a span shrinks the reference. Document A might reference I:100-199 while Document B (after a partial deletion) references only I:100-149.

### FINDDOCSCONTAINING Confirms Partial Inclusion

The operation that finds shared content explicitly handles partial overlap [LM 4/70]:

> "This returns a list of all documents containing **any portion** of the material included by \<vspec set\>."

The phrase "any portion" means documents routinely contain different-sized pieces of the same I-space content.

### Correspondence Works Across Different Decompositions

SHOWRELATIONOF2VERSIONS returns *pairs* of corresponding spans [LM 4/70]:

> "This returns a list of ordered pairs of the spans of the two spec-sets that correspond."

If both documents had to use identical span boundaries, a simple list would suffice. Returning *pairs* implies the two documents may decompose shared content differently—span boundaries in one version need not align with span boundaries in the other.

### The Byte-Level Foundation

The fundamental unit of identity is the individual byte, not the span. Spans are a convenience for addressing contiguous ranges, but correspondence and identity operate at the byte level:

> "Logical addressing of the byte stream is in the form of virtual spans, or vspans. These are sequences of bytes in the document's virtual byte stream, **regardless of their native origin**." [LM 4/11]

> "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

Attribution and identity trace to individual bytes via their I-addresses. How those bytes are grouped into spans in any particular document's V-space is that document's business.

### Concrete Example

Suppose Alice writes "Hello world" in Document A (I-addresses 100-110). Bob transcludes it into Document B as one span [I:100-110]. Carol transcludes it too, but then inserts a comma after "Hello", splitting her reference into [I:100-104], her new comma, [I:105-110]. Dave transcludes only "world" as [I:106-110].

All four documents share I-space content. None are required to use the same span decomposition. Correspondence still works—SHOWRELATIONOF2VERSIONS between any pair will find the shared I-addresses regardless of how each document groups them into spans.
