## Question 3 [theory]

> What must the count guarantee about links whose endpoints reference content that has since been superseded by a newer version?

## Short answer

A count of links touching superseded content must remain **complete and stable**: supersession does **not** decrement the count. Because superseding a document never destroys the older version (it "must remain on the network") and because links attach to permanent Istream bytes rather than positions, every link made against the superseded content still exists and must still be counted. Furthermore, since a link to one version is structurally a link to *all* versions, the count cannot treat a superseded endpoint as "gone."

## Why this follows from Nelson's guarantees

**1. Supersession does not delete — the old version persists.**

When a document is replaced by a newer one, the prior version is not removed:

> "However, for corrections and amendments, the author may readily publish a superseding document, but the former version must remain on the network. This is vital because of the links other users may have made to it—which can now reach through from the previous version (to which they were originally attached) into the newer version." (2/43)

So the very *reason* the former version stays is to keep the links to it valid. A count operation must reflect this: those links are still live.

**2. Links attach to bytes (Istream), so they survive.**

> "A Xanadu link is not between points, but between spans of data... This has a crucial advantage: it means that links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them. This also works for alternative versions in which part of each end has survived." (4/42)

A link endpoint into superseded content still resolves as long as any of its bytes remain in Istream. Supersession is a Vstream/arrangement event; it does not erase the Istream bytes the link straps to. Hence the link continues to satisfy a search/count.

**3. A link to one version is a link to all versions.**

> "Links may be refractively followed from a point or span in one version to corresponding places in any other version. Thus a link to one version of a Prismatic Document is a link to all versions." (2/26)

This means the count must not double-decrement or drop a link merely because a newer version now exists — the link's endpoint corresponds across versions through shared Istream origin.

**4. The count operation's own invariant.**

`FINDNUMOFLINKSFROMTOTHREE` counts links matching the endset request, and the search/count model guarantees that irrelevant links do not impede finding the relevant ones:

> "THE QUANTITY OF LINKS NOT SATISFYING A REQUEST DOES NOT IN PRINCIPLE IMPEDE SEARCH ON OTHERS." (4/60)

So a count constrained to the superseded content's spans must return all surviving links to those spans, regardless of how many newer versions or unrelated links exist.

## The net guarantee

Counting links whose endpoints reference superseded content must guarantee:

- **Completeness** — every link still strapped to surviving Istream bytes is included; supersession does not silently remove links from the tally.
- **Stability** — publishing a newer version does not change the count of links to the older version (the old version "must remain").
- **Version-spanning** — because endpoints correspond across versions, the count reflects links reachable through refractive following, not just links literally made against the textual position in one arrangement.

A link drops out of the count **only** if all the bytes at that endset are gone (4/42), which supersession by itself does not cause.

## Caveat

The curated sources fully support the underlying invariants (link survivability 4/42, persistence of superseded versions 2/43, refractive version-spanning 2/26, count/search non-impedance 4/60). They do **not** contain an explicit passage describing the *count* operation's behavior specifically with respect to *superseded* endpoints — that synthesis is mine, derived from those guarantees. If you need Nelson's exact treatment of the count operations against versioned/superseded content, see:

NEED_RAW: 4/58-4/60, 4/68-4/70
