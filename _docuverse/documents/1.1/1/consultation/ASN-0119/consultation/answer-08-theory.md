## Question 8 [theory]

> How must moved content remain discoverable to a user who looks for it under its new position in the document?

## Discoverability of Moved Content

When content is moved via REARRANGE, its position in the document's Vstream changes — but its **identity does not**. The guarantee is that everything attached to that content (links especially) follows it to its new position, so a user who looks under the new V-position finds not just the bytes but every connection they carried.

### The mechanism: identity is the I-address, not the V-position

Content is identified by its permanent Istream address. The document is a mapping from V-positions to I-addresses, and REARRANGE alters that mapping — it does not touch the content or its I-address. From the Vstream curated source (4/30):

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." (4/30)

So when a user looks under the new V-position, the system resolves that position to the same I-address the content always had. Anything indexed against that I-address is therefore found at the new location.

### Links are straps between bytes, so rearrangement carries them along

Because links attach to spans of bytes rather than positions, moving content cannot strand its links. The survivability annotation makes rearrangement explicit (4/42-4/43):

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes. This has a crucial advantage: it means that links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them." (4/42)

> "SURVIVABILITY: Links between bytes can survive deletions, insertions and rearrangements, **if anything is left at each end.**" (4/43)

### What this means for the user

A user who navigates to the content's new V-position is querying by content address. The link-search operation answers by address, not by old position, so the connections surface wherever the content now sits:

> "A link satisfies a search request if one span of each endset satisfies a corresponding part of the request." (4/58)

The same holds for origin: REARRANGE is a Vstream-only operation, so the home document and I-address are unchanged, and the user can still "at once ascertain the home document of any specific word or character" (2/40) at the new position.

### Summary

Moved content remains discoverable under its new position because:
1. **Position is not identity** — the content keeps its permanent I-address; only the V→I mapping changes (4/30).
2. **Links are byte-strapped** — they ride along to the new position since they bind bytes, not positions (4/42-4/43).
3. **Search is by address** — link queries resolve against content addresses, so connections appear at whatever V-position the content now occupies (4/58).

The net guarantee: a user looking under the new position finds the content *and* every link, annotation, and attribution it carried before the move — nothing is lost by relocation.
