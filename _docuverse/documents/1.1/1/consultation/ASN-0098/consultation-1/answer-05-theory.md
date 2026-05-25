## Question 5 [theory]

> Was boundary-insertion exclusion (newly allocated content not extending a link's reach into its coverage) an intentional design guarantee, and was there a specific discipline for endset/span construction intended to enforce it?

Yes — boundary-insertion exclusion follows necessarily from the discipline I imposed on endsets, though I didn't name it as a separate guarantee.

The discipline is **byte-anchoring**: endsets attach to specific bytes by their permanent Istream addresses, not by position in the current arrangement. A link is "a strap between bytes" [LM 4/42] — the strap holds to those particular bytes. New content receives fresh Istream addresses at creation; it simply isn't the bytes any pre-existing endset refers to.

For spans I made this principle explicit: "The first point of a span may designate a server, an account, a document or an element; so may the last point. There is no choice as to what lies between; this is implicit in the choice of first and last point." [LM 4/25]

The mechanism enforcing exclusion:

1. From-sets and to-sets are arbitrary collections of byte-spans referenced by I-address [LM 4/42-4/43]
2. I-addresses are permanent — fixed at content creation
3. Newly inserted bytes receive new I-addresses, allocated outside any pre-existing span's range
4. Therefore inserted bytes cannot be silently absorbed into prior link coverage

What I called out explicitly was the *complementary* property — survivability: "Links between bytes can survive deletions, insertions and rearrangements, if anything is left at each end" [LM 4/43]. Survivability protects existing connections from being lost. Exclusion prevents existing connections from silently expanding. Both fall out of the same byte-anchored design, but I emphasized survivability because that's the worry authors actually have — broken links, not swollen ones.

The point of byte-set referencing (as opposed to position-anchoring) was precisely to make link coverage **mean** something stable: the bytes it grasps, no more and no less. Position-anchored systems give you neither guarantee — they leak in both directions.

NEED_RAW: 4/9, 4/30 — for explicit discussion of how new bytes are allocated relative to existing I-address ranges, and whether sub-addressing within a pre-existing span's range was considered (which would be the one edge case where exclusion could in principle be defeated).
