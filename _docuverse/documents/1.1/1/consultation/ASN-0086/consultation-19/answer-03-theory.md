## Question 3 [theory]

> Did the tumbler design intend each document's depth-1 element-field allocator to enumerate positions across all subspaces (content, link, etc.) in a single sibling stream — with subspace identity determined by first-element-field value of each output — rather than maintaining independent allocators per subspace?

Looking at this question carefully — it asks whether Nelson's design uses ONE allocator that enumerates across all subspaces (with subspace identity as the first value in each output), or INDEPENDENT allocators per subspace.

Let me check the original pages on link/byte subspace structure to be thorough.

[Reading raw page on tumbler element-field structure]

Based on the curated sources, here is my answer:

**No.** Nelson's design uses **independent allocators per subspace**, with the subspace identity carried as a leading digit that distinguishes subspace 1 (bytes) from subspace 2 (links). Each subspace has its own enumeration sequence.

## Evidence from the Curated Sources

The address structure within the element field is:

- **Bytes**: `...D.V.0.1.position` — subspace 1, with byte position
- **Links**: `...D.V.0.2.N` — subspace 2, with link instance number

From the `links` curation (citing 4/31):

> "Breaking down the address:
> - `N.0.U.0.D` = node, account, document
> - `V` = version
> - `0.2` = delimiter + link subspace (vs `0.1` for bytes)
> - `N` = link instance number (sequential)"

The two subspaces use **different ordering principles**, which is the strongest evidence they cannot share a single allocator:

**Bytes** (subspace 1) use V-stream ordering that changes with editing:

> "The digit after the one indicates the byte position in the current ordering of bytes. This is its virtual stream address." [LM 4/30]

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." [LM 4/30]

**Links** (subspace 2) use permanent creation-order numbering that never changes:

> "The links designated by a tumbler address are in their permanent order of arrival. A document includes only the links of which it is the home document." [LM 4/31]

## Why a Unified Allocator Would Break the Design

If there were one combined allocator enumerating across both subspaces, then:

1. **Byte position 5 and link instance 5 could not both exist** — only one entity could occupy position 5 in a unified stream.
2. **V-stream rearrangement would renumber links** — since bytes shift positions with editing, any link interleaved with them in a single stream would also shift, violating Nelson's explicit guarantee of "permanent order of arrival" for links.
3. **The address `N.0.U.0.D.V.0.2.755` would lose its meaning** as "the 755th link" — it could land anywhere in a unified stream depending on how many bytes interleaved.

The `0.1` and `0.2` aren't output values of a single allocator — they are subspace **delimiters** identifying which independent counter you're indexing into.

## Extensibility Implied

From `links` curation, Nelson hints at further subspaces:

> "The subdivision of links by further digits (after '2' and the position) is a distinct possibility, and several possible uses have been discussed." [LM 4/31]

This phrasing ("after '2'") again presupposes that `2` is a subspace label preceding an independent position counter, not a value in a shared sequence.

## Caveat

NEED_RAW: 4/30-4/31 — The curated sources are clear that bytes and links use different ordering principles (V-stream vs. permanent arrival order), which rules out a single shared allocator. However, I did not directly inspect the original pages to confirm there is no passage describing the element-field as logically a single allocator with the subspace digit emerging as part of its output structure. The semantic conclusion (independent allocators) is well-supported, but if you need verbatim confirmation that Nelson described them as "separate" allocators rather than as one allocator outputting subspace-prefixed values, the original pages 4/29-4/35 (raw 196-202) should be checked.
