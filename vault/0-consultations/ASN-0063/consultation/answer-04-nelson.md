## Question 4 [nelson]

> What must the system guarantee about the relationship between a link's endsets and the original content they reference — must endsets always resolve to the exact content that existed when the link was created?

## Endset Resolution: What the System Guarantees

The short answer is: **yes and no**. Endsets always resolve to the same *Istream content* (which is immutable), but the *visible arrangement* of that content may change across versions. Nelson's design separates these two concerns deliberately.

### Istream Immutability: The Core Guarantee

Because endsets point to **Istream addresses** (permanent content identity), and Istream is append-only, the bytes referenced by an endset never change:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control" [LM 4/11]

Content at an I-address is permanent. A link created today pointing to I-address X will resolve to exactly the same bytes at X forever. This is not a feature of links — it is a property of Istream itself. Nothing in the system can modify content at an existing I-address.

### Survivability: Graceful Degradation, Not Exact Preservation

What the system does **not** guarantee is that the endset will always reference the same *quantity* of visible content. Nelson's survivability model explicitly allows partial degradation:

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes. This has a crucial advantage: it means that links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them." [LM 4/42]

And from the survivability diagram on 4/43:

> "Links between bytes can survive deletions, insertions and rearrangements, **if anything is left at each end.**"

So the guarantee is:

| Scenario | Endset resolves? | To what? |
|----------|-----------------|----------|
| Content unchanged | Yes | Exact original span |
| Content partially deleted from Vstream | Yes | Remaining bytes (subset of original) |
| Content rearranged in Vstream | Yes | Same bytes, possibly discontiguous |
| ALL bytes deleted from Vstream | Link breaks | I-content still exists but nothing visible at either end |

The endset doesn't "update" to track new content — it stays attached to the *same bytes*. If those bytes are scattered by editing, the endset becomes discontiguous but still references the original content. Nelson explicitly illustrates this:

> "We see from above that one end of a link may be on a broken, discontiguous set of bytes." [LM 4/42]

### Why This Works: The I/V Separation

The mechanism is the Istream/Vstream separation. Links point to I-addresses (permanent identity). Editing changes V-addresses (current arrangement). Since these are independent:

- **INSERT** in a document: V-addresses shift, I-addresses unaffected, links unaffected
- **DELETE** from a document: V-mapping removed, I-content remains, links still resolve to I-content
- **REARRANGE**: V-order changes, I-addresses unchanged, links follow the bytes

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." [LM 4/30]

### Version-Spanning: Refractive Following

When content evolves through versions, the system can follow links across version boundaries through **correspondence** (shared I-address origin):

> "Links may be refractively followed from a point or span in one version to corresponding places in any other version. Thus a link to one version of a Prismatic Document is a link to all versions." [LM 2/26]

This means the endset resolves to the same I-content always, but the *front end* can choose to show the user where that content appears in the current version — or any version. The link itself doesn't change; the presentation adapts.

### What the System Does NOT Guarantee

Nelson does not guarantee that:

1. **Endsets track editorial intent.** If you link to a paragraph and the author rewrites it (deleting old bytes, inserting new ones), your link stays on the old bytes — it does not "follow" to the replacement text. The old bytes still exist in Istream; the new text has different I-addresses.

2. **Endsets remain contiguous.** Editing may scatter the referenced bytes across the Vstream, producing a "broken, discontiguous set of bytes" [LM 4/42].

3. **Endsets remain visible.** If all referenced bytes are deleted from every Vstream arrangement, the link has nothing to display — though the I-content technically still exists in the permascroll.

### Summary

The guarantee is precise: **endsets resolve to the identical Istream bytes forever** (because Istream is immutable), but the **visible presentation** of those bytes — their position, contiguity, and presence in a given version's Vstream — may change through editing. Links degrade gracefully (surviving partial deletion) rather than breaking catastrophically. The only breaking condition is total removal of all referenced bytes from the Vstream at an end.

This is the "strap between bytes" metaphor in full: the strap doesn't care where the bytes move or how many survive — it holds onto whatever remains.
