## Question 8 [theory]

> Must the system guarantee that a link, once created, persists permanently and remains available even if the content at its endsets is later superseded by new versions?

## Short Answer

Yes—with a precise distinction. Supersession is *not* destruction. Because a superseding version never deletes the content it replaces, links to the superseded content remain attached to it and "reach through" into the new version. The system's guarantee that links persist comes from two interlocking principles: **published content cannot be withdrawn** (so the endset content never disappears), and **links survive as long as any bytes remain at each end**. The one qualification: permanence is not unconditional immortality—the *owner of a link* retains the right to delete their own link.

## 1. Supersession preserves the old; it does not destroy it

The premise of the question—"content superseded by new versions"—does not erase the original endsets. Nelson is explicit that the former version *must* remain, precisely so that existing links don't break:

> "However, for corrections and amendments, the author may readily publish a superseding document, but the former version must remain on the network. This is vital because of the links other users may have made to it—which can now reach through from the previous version (to which they were originally attached) into the newer version." (2/43)

So a link made to version 1 stays attached to version 1 (which persists permanently) and can refractively follow into version 2.

## 2. Links refractively span all versions

A link to one version is, in effect, a link to every version, because correspondence lets the system trace the same content across the version family:

> "Links may be refractively followed from a point or span in one version to corresponding places in any other version. Thus a link to one version of a Prismatic Document is a link to all versions." (2/26)

And the front end can transparently redirect the reader to the current version if the passage still exists there:

> "When a document is updated, a reader will ordinarily want to see the new version—but the reader may be following a link made to an older version. However, the user's front-end machine may easily be set up to follow the link to the same passage in the most recent version—if it's still there." (2/43)

Note the conditional: *if it's still there.* The link's availability into the *new* version depends on the corresponding content surviving; its attachment to the *old* version is guaranteed because the old version is preserved.

## 3. The mechanism: links survive as spans, not points

The reason editing and supersession don't break links is structural—links attach to bytes, not positions:

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes. This has a crucial advantage: it means that links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them. This also works for alternative versions in which part of each end has survived." (4/42)

The visual annotation on 4/43 states the rule and its precondition plainly:

> "SURVIVABILITY: Links between bytes can survive deletions, insertions and rearrangements, **if anything is left at each end.**" (4/43)

## 4. Why the endset content cannot simply vanish

For *published* content, the survivability precondition ("if anything is left at each end") is effectively guaranteed, because publication is permanent and content remains in Istream even when "deleted" from a current arrangement:

> "It is in the common interest that a thing once published stay published, as in the world of paper. Other readers and users will come to depend on its accessibility. Consequently its author may not withdraw it except by lengthy due process." (2/43)

And "deletion" in Xanadu only removes content from a Vstream arrangement; the bytes remain addressable in Istream and in prior versions—so links to them still resolve.

## 5. The qualification: persistence is not unconditional immortality

The system does **not** force a link to exist forever against its owner's will. Link *survivability* (protection against edits to endset content) is distinct from link *deletion* (an ownership right):

> "DELETED LINKS (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" (4/9)

> "A link need not point anywhere in its home document. Its home document indicates who owns it, and not what it points to." (4/12)

So the link's *owner* may withdraw it. What no one can do is break your link by editing or superseding the content you linked to—because that content is preserved, and the link is strapped to the surviving bytes.

## Summary

| Scenario | Does the link persist / remain available? |
|---|---|
| Endset content superseded by a new version | **Yes** — old version is preserved (2/43); link reaches through refractively (2/26) |
| Endset content "deleted" from current arrangement | **Yes** — bytes remain in Istream/prior versions; link still resolves |
| Endset content edited/rearranged | **Yes**, if any bytes remain at each end (4/42–4/43) |
| All bytes at an endset truly gone | The strap has nothing to hold—but for *published* content this cannot happen (2/43) |
| Link owner deletes their own link | The link becomes "not currently addressable" (4/9) — owner's prerogative |

So the correct framing is: the system guarantees links are not broken *by supersession or editing of their endset content*, because that content is never destroyed and links bind to surviving bytes. It does not guarantee a link is immortal independent of its owner's wishes.
