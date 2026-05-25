## Question 2 [theory]

> When a link references content that has been edited, what determines whether the endset still resolves to visible content or becomes unreachable?

# When Edits Touch a Link: What Determines Survival

The determining principle is simple and structural: **links survive if any bytes remain at each end.**

## The Core Rule

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes. This has a crucial advantage: it means that links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them. This also works for alternative versions in which part of each end has survived." [LM 4/42]

And the visual annotation from page 4/43 puts it as plainly as possible:

> "SURVIVABILITY: Links between bytes can survive deletions, insertions and rearrangements, **if anything is left at each end.**" [LM 4/43]

## Why This Works: Istream Anchoring

Endsets point to permanent Istream addresses, not to Vstream positions. The content identity is fixed; the arrangement is fluid. So:

- **Insertion** — Vstream positions shift around the linked content, but Istream addresses don't change. The strap stays attached.
- **Rearrangement** — Same bytes, different order. The link travels with the bytes.
- **Deletion** — This is the interesting case, and it bifurcates.

## Deletion: Two Senses of "Reachable"

When you "delete" content, you are removing it from the current Vstream arrangement. You are *not* destroying it from Istream:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

So there are really two questions hiding inside "still reachable":

| Question | Answer |
|----------|--------|
| Does the link itself remain valid? | Yes, as long as *any* bytes at each endset survive in Istream |
| Is the linked content visible in the current Vstream of the home document? | Only if those bytes haven't been deleted from it |
| Is the linked content visible *somewhere*? | Yes — in prior versions, and in any document that transcludes those bytes |

## When an Endset Truly Becomes Unreachable

An endset only fails when **every** byte it references has been removed from its end. The threshold is "anything left" — not "everything intact." A link to a five-paragraph passage survives even if four paragraphs are deleted; one surviving byte at each end is enough.

And because deletion is non-destructive at the Istream layer, even an endset whose bytes are gone from the current version can be followed via historical backtrack to the version where those bytes still appear — or to any other document that transcludes them. Reachability in the strict Istream sense is preserved almost absolutely; what changes is *which view* shows the content.

## What Versions Add

The same logic extends across version boundaries:

> "Links may be refractively followed from a point or span in one version to corresponding places in any other version. Thus a link to one version of a Prismatic Document is a link to all versions." [LM 2/26]

A link made against an old version "reaches through" into newer versions wherever the corresponding bytes still exist. The endset doesn't become unreachable just because the document has moved on — it follows the content.

## Summary

The endset resolves to visible content whenever at least one byte at each end remains addressable in some accessible Vstream — current version, prior version, or another document that includes those bytes. It becomes "unreachable" in the strong sense only when every referenced byte has been removed from the docuverse entirely, which the architecture is specifically designed to prevent. The granularity of survival is "anything left at each end," not "everything intact."
