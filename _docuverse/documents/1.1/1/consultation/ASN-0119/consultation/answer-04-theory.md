## Question 4 [theory]

> How must a link anchored entirely within one of the moved regions behave once that region appears at its new position?

A link anchored entirely within a moved region survives the REARRANGE fully intact and travels with the bytes to their new position. It is not broken, not re-anchored, and not altered — it simply continues to attach to the same bytes, which now appear at a different Vstream location.

## Why this is guaranteed

The key is that links attach to **bytes (Istream identity)**, not to **positions (Vstream arrangement)**. REARRANGE is a pure Vstream operation: it changes the order in which content is presented, but it does not touch the Istream content or its permanent addresses.

From `vault` curated source on Vstream addressing (4/30):

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." (4/30)

Because a link anchored *entirely within* the moved region has **both** of its surviving endsets inside that region, and REARRANGE deletes nothing, *all* of the bytes at each end persist. The survivability condition is therefore trivially met:

> "SURVIVABILITY: Links between bytes can survive deletions, insertions and rearrangements, **if anything is left at each end.**" (4/43)

Since the entire region survives (rearrangement only reorders it), the link's from-set and to-set both remain wholly populated. The link stays exactly as it was.

## What the user experiences

When the moved region appears at its new Vstream position, the link appears there with it. Its Vstream coordinates have shifted along with the content, but its underlying Istream endsets are unchanged. As the link concept summary puts it, the link is "a strap between bytes" — the strap stays attached to whatever bytes remain, regardless of where those bytes are arranged:

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes. This has a crucial advantage: it means that links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them." (4/42)

## Summary

- The link is **not** an editing casualty — REARRANGE preserves all bytes, so no end is emptied.
- The link **moves with its content** because its endsets are Istream addresses, which REARRANGE never changes.
- Its **Vstream position** changes (it now sits at the region's new location); its **Istream identity and address** do not.

This is the intended behavior: edits change arrangement (Vstream), never content identity (Istream), and links — which point to Istream — follow the content wherever it is rearranged.
