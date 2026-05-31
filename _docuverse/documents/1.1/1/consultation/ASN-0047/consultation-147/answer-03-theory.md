## Question 3 [theory]

> Was the link subspace deliberately designed to permit a freely-chosen positional depth (subdividable "by further digits", LM 4/31) while the byte/content subspace has a fixed positional depth per document, or were both intended to share a common positional discipline?

I can't open the raw page files in this session (only Drive auth is available, which isn't the local corpus), so I'll answer from the verified curated quotes and flag anything that goes beyond them.

## Answer

The two subspaces were **not** held to a common positional discipline — and the asymmetry is deliberate, rooted in how each subspace relates to rearrangement.

**Links: positional depth left open by design.** At 4/31 I explicitly flagged further subdivision as an open extension point:

> "The subdivision of links by further digits (after '2' and the position) is a distinct possibility, and several possible uses have been discussed." (4/31)

The language matters — "a distinct possibility," "several possible uses have been discussed." That is the vocabulary of an intentionally-reserved design space, not a closed specification. It sits naturally alongside the permanent-arrival ordering of links:

> "The links designated by a tumbler address are in their permanent order of arrival. A document includes only the links of which it is the home document." (4/31)

Because a link's position digit is **fixed at creation by arrival order** (links are not rearrangeable), it is safe to hang further digits beneath it — for compound links, faceted links, and link-to-link hierarchies, all of which I treat as built from the same primitive.

**Bytes: a single position tied to the Vstream.** The content position is one rearrangeable coordinate:

> "The digit after the one indicates the byte position in the current ordering of bytes. This is its virtual stream address." (4/30)

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." (4/30)

The byte position is *managed by the system* — the POOM continually reorders it as the document is edited. A coordinate the back end is free to renumber on every edit is the wrong place to invite the user to baptize permanent sub-digits. So the discipline differs because the underlying semantics differ: **links are permanent-by-arrival and therefore safely subdividable; bytes are rearrangeable-by-arrangement and therefore kept to a single managed position.**

## Caveat on intent vs. silence

What the verified text *states*: link subdivision is an explicitly contemplated open possibility (4/31); byte addressing is described with a single position digit (4/30). What the curated text does **not** contain is any sentence affirmatively forbidding subdivision of the byte position, or declaring byte depth "fixed per document" as a closed rule. So the cleanest reading the sources support is: I *deliberately reserved* freely-chosen positional depth for links, while leaving the byte subspace at one managed position — rather than the sources proving the byte subspace was sealed against further depth.

NEED_RAW: 4/30–4/31 (raw pages 197–198) to confirm whether the surrounding text states an explicit fixed-depth rule for the byte/content position, and to resolve the curated inconsistency over whether the link subspace digit is "2" (links.md) or "3" (i-space-addresses.md), which bears on exactly where the "further digits" attach.
