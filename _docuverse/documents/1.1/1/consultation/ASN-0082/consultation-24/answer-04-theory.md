## Question 4 [theory]

> Was contraction/deletion designed in Literary Machines as an operation on arbitrary V-position depths, or specifically scoped to the single-ordinal (depth-2) level analogous to a within-subspace span?

# Deletion Scope in FEBE

Based on the curated sources, **deletion in Xanadu was specifically scoped to within-subspace byte-stream spans (depth-2 level), not arbitrary V-position depths**.

## Evidence

### The operation name itself constrains scope

The FEBE operation is **DELETEVSPAN**, where "vspan" is defined as a byte-stream construct:

> "Logical addressing of the byte stream is in the form of virtual spans, or vspans. These are sequences of bytes in the document's virtual byte stream, regardless of their native origin." (LM 4/11)

A vspan is a sequence of *bytes*, not an arbitrary tumbler subtree. This places DELETE at the depth where byte positions live.

### The operation specification operates at byte granularity

> "DELETEVSPAN: This removes the given span from the given document." (LM 4/66)

Companion operations confirm byte-level semantics. INSERT explicitly shifts byte positions:

> "The v-stream addresses of any following characters in the document are increased by the length of the inserted text." (LM 4/66)

REARRANGE operates on "regions of text" with cuts (LM 4/67). All editing operations work at the character/byte level within a single subspace.

### Bytes and links are separate deletion states

The document content diagram at LM 4/9 treats them as distinct:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" (LM 4/9)

> "DELETED LINKS (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" (LM 4/9)

Link deletion is an ownership/administrative action by the link's home-document owner — not something done by issuing DELETEVSPAN across the byte/link subspace boundary.

## Caveat: span mechanism vs. operation scope

The general span mechanism is *capable* of designating arbitrary depths:

> "A tumbler-span may range in possible size from one byte to the whole docuverse on the whole network." (LM 4/24)

> "A digit of 'one' may be used to designate all of a given version, all versions of a given document..." (LM 4/38)

But this generality is about the addressing scheme, not about what DELETEVSPAN accepts. The "vspan" prefix on the operation name binds it to the byte subspace.

## What is not explicitly stated

NEED_RAW: 4/66, 4/79 — Nelson does not explicitly say "DELETEVSPAN rejects spans that cross subspace boundaries" or "DELETEVSPAN cannot target version-level or document-level spans." The constraint is inferred from terminology (vspan = byte stream) and from the parallel separate treatment of byte vs. link deletion at 4/9. A definitive design statement about whether contraction was *considered* at deeper hierarchical levels would require checking the FEBE spec pages directly.

## Summary

DELETE was designed as a within-subspace (byte) operation analogous to a depth-2 ordinal span — a contiguous range of byte positions in one document's V-stream. Link removal is a separate concern handled through ownership of the link's home document, and the cross-subspace or hierarchical deletion case is not part of the specified FEBE operation set.
