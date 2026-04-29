## Question 6 [nelson]

> Must links that reference content by address continue to resolve correctly after any sequence of editing operations performed on the linked document?

# Yes — Links Must Resolve After Any Editing Sequence

This is one of the most fundamental guarantees I designed into Xanadu. Links attach to **bytes**, not to **positions**. Editing changes positions; it does not change bytes. Therefore editing cannot break links.

## The Mechanism

The key is the separation of I-space (permanent content) from V-space (current arrangement):

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." [LM 4/30]

When you INSERT, DELETE, or REARRANGE, you are modifying V-space — the document's current arrangement. The I-space addresses where content permanently lives are untouched. Links point to I-space. Therefore:

- **INSERT** shifts V-space positions after the insertion point. Links are unaffected — they don't point to V-space positions.
- **DELETE** removes content from V-space but not from I-space. The bytes still exist at their permanent addresses. Links still resolve.
- **REARRANGE** reorders V-space. The bytes themselves don't move in I-space. Links still resolve.
- **COPY** (transclusion) creates new V-space mappings to existing I-space content. Original links still point to the same I-space bytes.

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." [LM 4/11]

V-space addresses are ephemeral. I-space addresses are eternal. Links use I-space.

## The Survivability Guarantee

I stated this explicitly:

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes. This has a crucial advantage: it means that links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them. This also works for alternative versions in which part of each end has survived." [LM 4/42]

And the visual annotation on the facing page:

> "SURVIVABILITY: Links between bytes can survive deletions, insertions and rearrangements, **if anything is left at each end.**" [LM 4/43]

## The Qualification: "If Anything Is Left"

The one condition is that **some bytes must remain at each endset**. If every byte that a link's from-set or to-set references is deleted from V-space, the link has nothing to display in the current version.

But even this is not true destruction. Deleted bytes enter the state I described:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

The bytes still exist in I-space. The link still resolves to them. They are merely "not currently addressable" in the current V-space arrangement. Previous versions still contain them, other documents that transclude them still show them, and historical backtrack can reconstruct them.

## Why This Matters for Published Documents

This guarantee is not merely technical — it is the foundation of the publication contract:

> "It is in the common interest that a thing once published stay published, as in the world of paper. Other readers and users will come to depend on its accessibility. Consequently its author may not withdraw it except by lengthy due process." [LM 2/43]

> "However, for corrections and amendments, the author may readily publish a superseding document, but the former version must remain on the network. This is vital because of the links other users may have made to it — which can now reach through from the previous version (to which they were originally attached) into the newer version." [LM 2/43]

Links made by other users are **their property**, stored at **their addresses**. Those links depend on the continued resolvability of the content they reference. This is precisely why published content cannot be withdrawn — doing so would break others' property.

## Summary

The answer is **yes, unconditionally** at the I-space level. Links always resolve to the same permanent bytes regardless of editing. At the V-space level, the bytes may no longer appear in the current version (if deleted), but they remain in I-space, in previous versions, and in any other documents that transclude them. The link never "breaks" — the content it references is permanent by design.
