## Question 7 [theory]

> Where must links that were anchored to content after the insertion point come to rest once that content is displaced — must every link continue to designate exactly the same content it designated before?

Links must come to rest on **exactly the same bytes** they designated before — their target content is unchanged, even though that content's position in the document has moved.

## The mechanism

The key is that Xanadu links attach to **content (Istream bytes)**, not to **positions (Vstream addresses)**. When you insert content, the Vstream positions of everything after the insertion point shift forward, but the bytes themselves keep their permanent Istream identity — and links point to Istream.

From `concepts/links.md` (4/42):

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes. This has a crucial advantage: it means that links can survive editing. If any of the bytes are left to which a link is attached, the link remains on them."

So the "strap" stays bound to the same bytes. The content moves; the link moves with it, still designating identically the content it always designated.

## Why position-shift doesn't disturb the link

Nelson is explicit that the V-stream addresses of following characters increase on insertion — `Design Intent/operations.md` (4/66):

> "The v-stream addresses of any following characters in the document are increased by the length of the inserted text."

But the links are unaffected, because they are anchored to the bytes, not the V-positions. From `Design Intent/v-space-addresses.md` (4/30):

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them."

And the survivability annotation from page 4/43 (`concepts/endsets.md`):

> "SURVIVABILITY: Links between bytes can survive deletions, insertions and rearrangements, **if anything is left at each end.**"

## Direct answer to "must every link designate exactly the same content?"

Yes. For an **insertion** specifically, nothing is removed, so every link designates exactly the same content afterward — the displacement is purely positional (Vstream), and links live in content-space (Istream). The link "comes to rest" on the same bytes, now at a higher V-stream address.

The only case where a link's designated content can change is **deletion of bytes at one of its ends** — and even then it doesn't shift to *different* content; it simply survives on whatever bytes remain, and is destroyed only if *all* bytes at an end are removed. Insertion never causes that, because insertion removes nothing (`Design Intent/link-survivability.md`, 4/42):

> "If any of the bytes are left to which a link is attached, that link remains on them. This also works for alternative versions in which part of each end has survived."

So the governing invariant is: **a link always designates the same content (the same Istream bytes); editing changes where that content sits in the V-stream, never which content the link points to.**
