## Question 3 [nelson]

> Must a link remain valid and meaningful even after the content it connects has been edited, rearranged, or extended by its author?

# Yes. Absolutely. This Is the Whole Point.

A link **must** survive editing, rearrangement, and extension of the content it connects. This is not a nice-to-have feature — it is the architectural reason Xanadu's addressing system exists at all.

## The Mechanism: Straps Between Bytes

I designed links to attach to **spans of bytes**, not to positions between bytes. Think of a link as a strap binding bytes together:

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes. This has a crucial advantage: it means that links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them. This also works for alternative versions in which part of each end has survived."
> — [LM 4/42]

The visual annotation on the following page makes this explicit:

> "SURVIVABILITY: Links between bytes can survive deletions, insertions and rearrangements, **if anything is left at each end.**"
> — [LM 4/43]

## Why This Works: I-Space vs V-Space

The deeper reason links survive editing is the separation of **I-space** (where content permanently lives) from **V-space** (the document's current arrangement).

When you edit a document, you change V-space — you rearrange, insert, delete from the current view. But the content itself remains at its permanent I-space address. Links point to I-space, not V-space. Therefore:

- **Insert** new content → V-space positions shift, but I-space addresses are unchanged. Links unaffected.
- **Rearrange** content → V-space order changes, but I-space identity unchanged. Links unaffected.
- **Delete** content → V-space mapping removed, but I-space content remains. Links still resolve to the I-space address.
- **Extend** with new material → new bytes get new I-space addresses. Existing links still point to existing bytes. Unaffected.

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them."
> — [LM 4/30]

## Links Across Versions

The question extends naturally to versioning. When a document is superseded by a new version, links made to the old version reach through into the new one:

> "However, for corrections and amendments, the author may readily publish a superseding document, but the former version must remain on the network. This is vital because of the links other users may have made to it—which can now reach through from the previous version (to which they were originally attached) into the newer version."
> — [LM 2/43]

> "Links may be refractively followed from a point or span in one version to corresponding places in any other version. Thus a link to one version of a Prismatic Document is a link to all versions."
> — [LM 2/26]

This is what I call **refractive following** — the system traces correspondence (shared I-space origin) to find the same content in a different version's arrangement. A link made to version 1 works in version 5, provided the bytes still exist somewhere.

## The Only Way a Link Breaks

A link breaks **only** when all the bytes at one of its endsets have been deleted from every version. As long as any bytes remain at each end, the link remains valid:

> "If any of the bytes are left to which a link is attached, that link remains on them."
> — [LM 4/42]

And even "deleted" bytes are not truly destroyed — they persist in I-space, recoverable through historical backtrack:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)"
> — [LM 4/9]

## Why This Must Be So

Links create **permanence obligations**. Once others have linked to your published document, you cannot withdraw it — their links depend on its accessibility:

> "It is in the common interest that a thing once published stay published, as in the world of paper. Other readers and users will come to depend on its accessibility."
> — [LM 2/43]

If links broke every time an author edited their document, the entire web of interconnected literature would be fragile and useless. The whole system exists to preserve the structure of literature — and that structure is made of links. If links don't survive editing, you don't have Xanadu. You have the World Wide Web, with its perpetual broken links and link rot.

## Summary

| Operation | Link survives? | Why |
|-----------|---------------|-----|
| **Insert** new content nearby | Yes | I-space addresses unchanged |
| **Rearrange** content order | Yes | Links follow bytes, not positions |
| **Delete** some linked bytes | Yes, if any remain | Partial survival by design |
| **Delete** all linked bytes | Structurally broken | But bytes persist in I-space for backtrack |
| **Extend** document | Yes | New bytes get new addresses; existing links unaffected |
| **Create new version** | Yes | Refractive following through correspondence |

The answer is not merely "yes" — it is that the entire architecture, from I-space/V-space separation to span-based endsets to tumbler addressing, was designed precisely to make this guarantee possible.
