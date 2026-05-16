## Question 2 [theory]

> Does the design permit reordering of links within a document's link subspace, or is the "permanent order of arrival" for home-document links strict (i.e., link-subspace V-positions are fixed once allocated)?

I have sufficient evidence in the curated sources to answer this directly without further tools.

# Answer: Link order is strict — V-positions are fixed once allocated

The design treats link V-positions as **permanent and non-rearrangeable**, in deliberate contrast to byte V-positions (which can be reordered freely via REARRANGE).

## The direct statement

Nelson states explicitly on 4/31:

> "The links designated by a tumbler address are in their permanent order of arrival. A document includes only the links of which it is the home document." (LM 4/31)

The phrase "permanent order of arrival" is unambiguous: a link allocated as `N.0.U.0.D.V.0.2.755` is the 755th link the document ever owned, and it stays the 755th forever.

The curated extraction of Istream addressing reinforces this with the implementation-side note that "links are currently not rearrangeable" (see `i-space-addresses.md` element-field structure).

## Why this is asymmetric with bytes

Bytes in the `0.1` subspace are the opposite. From 4/11 and 4/30:

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." (LM 4/11)

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." (LM 4/30)

So bytes have ephemeral V-positions (rearrangeable via INSERT/DELETE/REARRANGE on Vstream), while links have fixed V-positions (creation-order, never renumbered).

## Implications

- Link `2.5` deleted does **not** cause `2.6`...`2.N` to renumber — addresses are stable for the lifetime of the document.
- A reference to "the 755th link" is permanently meaningful in that document's address space.
- REARRANGE applies to byte spans, not link spans.

## A door Nelson left open

He notes one form of structure that could be added on top, without contradicting the permanent-arrival rule:

> "The subdivision of links by further digits (after '2' and the position) is a distinct possibility, and several possible uses have been discussed." (LM 4/31)

That is forking sub-addresses *under* an existing link position, not reordering the positions themselves. The arrival order remains strict.

## Verdict

Strict. Link-subspace V-positions are fixed at allocation and are not subject to rearrangement, by deliberate contrast with the byte subspace. If an implementation needs an apparent "reordering" of links, it must do so through a separate user-facing index (e.g., a listing document or a metalink scheme), not by renumbering the `0.2.N` positions.
