## Question 3 [theory]

> If the content at the selected end has been edited or rearranged since the link was made, must the returned specification still describe the same identified material the link committed to?

## Short answer

Yes. The link commits to *bytes*, not to positions, so the returned endset must still identify the same material — even after the content at that end has been edited or rearranged. Editing and rearrangement change where those bytes sit in the document's Vstream, but they do not change *which* bytes the link named. The only way the identified material shrinks is if some of the committed bytes were actually deleted; the link then holds whatever survives.

## Why this holds

A Xanadu link attaches to a *span of bytes*, identified through permanent Istream addresses. Nelson's "strap between bytes" image is exactly the commitment:

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes. This has a crucial advantage: it means that links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them. This also works for alternative versions in which part of each end has survived." (4/42)

Because the binding is to the bytes themselves, editorial reordering of the surrounding document doesn't detach or re-target the link:

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." (4/30)

The annotation on 4/43 states the survivability conditions explicitly:

> "SURVIVABILITY: Links between bytes can survive deletions, insertions and rearrangements, **if anything is left at each end**." (4/43)

## The three editing cases at the selected end

Mapping the survivability rule onto "must the returned spec describe the same material":

- **Rearrangement** — Same bytes, reordered in the Vstream. The committed material is identical. If the endset is reported in Vstream coordinates the span figures may look different (because positions shifted), but they resolve to the same identified bytes. The Vstream is just a view over the invariant content:
  > "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." (4/11)

- **Insertion** — New bytes added near the endset are *not* captured by the link; the strap holds only the bytes it originally seized. So the returned spec still describes exactly the committed material, not the inserted additions.

- **Deletion** — Only here does the identified material change, and only by shrinking. Deleted bytes are removed from the Vstream view ("not currently addressable") but the link persists on the surviving bytes, "if anything is left at each end." The returned endset then describes the surviving subset of the originally committed material — never different material.

So `RETRIEVEENDSETS` — which "returns a list of all link end-sets that are in `<spec set>`" (4/70) — yields endsets that continue to name the same underlying content the link committed to, subject only to dropout of bytes that have been deleted.

## The one caveat worth stating precisely

"Same identified material" means same *content identity* (same Istream bytes), not same *Vstream coordinates*. Rearrangement and insertion can change the numeric span addresses you'd use to describe those bytes today, but those addresses still point at the original committed bytes. The link's commitment is preserved; what is not preserved is any guarantee that the *describing coordinates* are unchanged, nor that deleted bytes remain part of the set.
