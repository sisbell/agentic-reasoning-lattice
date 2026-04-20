## Question 5 [nelson]

> When a document is reorganized — passages reordered or moved to different positions — must links to those passages track the content rather than the location?

# Yes — Links Track Content, Not Location

This is one of the most emphatically stated design principles in Literary Machines. Links attach to **bytes** (Istream identity), not to **positions** (Vstream arrangement). When a document is reorganized, links follow the content wherever it moves.

## The Core Statement

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes. This has a crucial advantage: it means that links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them. This also works for alternative versions in which part of each end has survived."
> — [LM 4/42]

The "strap between bytes" metaphor is precise: a strap fastened to specific bytes stays attached to those bytes regardless of where they are moved, reordered, or rearranged.

## Why This Works: The Two Address Spaces

The mechanism that makes this possible is the separation of Istream (permanent content identity) from Vstream (current arrangement):

- **Istream addresses are permanent.** Every byte has an immutable identity address that never changes.
- **Vstream addresses are ephemeral.** They represent the document's current arrangement and shift with every edit.
- **Links point to Istream.** Therefore they are unaffected by Vstream rearrangement.

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them."
> — [LM 4/30]

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this."
> — [LM 4/11]

The V-address (position) changes constantly during editing. The I-address (identity) never changes. Links reference identity, so they are immune to positional changes.

## What Links Survive

The survivability guarantee from [LM 4/43]:

> "SURVIVABILITY: Links between bytes can survive deletions, insertions and rearrangements, **if anything is left at each end.**"

Specifically:

- **Rearrangements** — content moved to new positions: links follow
- **Insertions** — new content added around linked content: links unaffected
- **Deletions** — content removed: links survive if *any* bytes at each endset remain
- **Alternative versions** — content present in some versions but not others: links work wherever the bytes exist

Links break **only** when all bytes at one end are completely deleted — when there is literally nothing left for the "strap" to hold onto.

## The REARRANGE Operation Confirms This

The FEBE protocol includes an explicit REARRANGE operation:

> "Rearrange transposes two regions of text."
> — [LM 4/67]

This operation changes Vstream arrangement. It does not affect Istream content. Therefore it cannot break links. This is by design — the operation exists precisely because the architecture guarantees that reorganization is safe.

## Summary

The answer is unequivocal. Links **must** track content rather than location. This is not merely a desirable property but an architectural consequence of the Istream/Vstream separation. Links reference permanent content identity (I-addresses), not ephemeral arrangement positions (V-addresses). When you reorganize a document, you change only the Vstream mapping — the links, attached to Istream bytes, are structurally incapable of being affected.
