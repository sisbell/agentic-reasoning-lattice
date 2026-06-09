## Question 9 [theory]

> If linked content is later edited, what must remain stable about which links this inquiry would have returned, and what is permitted to change?

## What must remain stable

The **set of links returned** by the inquiry—the link identities—must remain stable, because Xanadu links attach to bytes (Istream content), not to positions. Editing rearranges the Vstream view but leaves the underlying byte identities intact, so a link that satisfied the inquiry before the edit still satisfies it after.

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes. This has a crucial advantage: it means that links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them." (4/42)

> "Links between bytes can survive deletions, insertions and rearrangements, if anything is left at each end." (4/43)

This stability holds precisely because the link binds to permanent Istream addresses, not to the shifting virtual order:

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." (4/30)

The link's own address is also stable—links keep their permanent creation-order addresses:

> "The links designated by a tumbler address are in their permanent order of arrival." (4/31)

## What is permitted to change

The **Vstream (virtual) positions** of the matched content may change. Insertion shifts following positions; deletion closes gaps; rearrangement reorders. The endsets the inquiry reports back may therefore resolve to different virtual addresses even though they reference the same bytes:

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." (4/11)

> "The v-stream addresses of any following characters in the document are increased by the length of the inserted text." (4/66)

## The one case where the returned set legitimately shrinks

A link drops out of the result **only if an entire endset is fully deleted**—when *nothing* is left at one end. Partial deletion preserves the link:

> "If any of the bytes are left to which a link is attached, that link remains on them. This also works for alternative versions in which part of each end has survived." (4/42)

So: the membership of the result set is invariant under editing **except** for links whose endset content is completely removed; the virtual addresses through which that membership is expressed are free to move.

(Note: this assumes the inquiry's from/to/three-set criteria are framed in terms of the content's byte identity. The search-satisfaction rule itself—"A link satisfies a search request if one span of each endset satisfies a corresponding part of the request" (4/58)—operates on those byte-based spans, which is why the matching set tracks the bytes rather than the positions.)
