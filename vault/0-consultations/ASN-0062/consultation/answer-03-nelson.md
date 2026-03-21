## Question 3 [nelson]

> Must the original content's permanent identity remain unchanged and retrievable at its original address after it is placed elsewhere?

## Yes — absolutely and by design.

This is one of Xanadu's most fundamental invariants. The original content's permanent identity (its Istream address) **must** remain unchanged and retrievable at its original address after being placed elsewhere. This is not a feature but the architectural foundation on which permanence, attribution, royalties, and link survivability all depend.

---

### The Istream Guarantee

Content lives permanently in Istream. Its address never changes, and the content at that address never changes:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

The phrase "home locations" is key. Content has a **home** — the document where it was originally created. That home is permanent. When content appears in another document, it is fetched from its home, not duplicated.

### COPY Is Reference, Not Duplication

The COPY operation — the mechanism by which content is "placed elsewhere" — creates a Vstream mapping to existing Istream content. It does **not** create new Istream content:

> "The material determined by \<spec set\> is copied to the document determined by \<doc id\> at the address determined by \<doc vsa\>." [LM 4/67]

The curated sources confirm: "This is transclusion — the copy shares I-addresses with the source." The destination document gains a virtual reference; the source document's Istream content is untouched.

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

The word "virtual" is doing essential work. These are not actual copies — they are references that resolve to the original Istream addresses.

### The Original Remains Retrievable

Nelson guarantees that you can always trace back to the source:

> "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

This is structural, not metadata. The I-address itself encodes the originating server, account, and document. To fetch the content, the system must request it from its home location. The connection **cannot** be severed because the fetching mechanism requires it.

### Even "Deletion" Cannot Remove the Original

If the owner deletes content from their current version, the Istream content persists:

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

The diagram on page 4/9 shows "DELETED BYTES" as content that is "not currently addressable, awaiting historical backtrack functions, may remain included in other versions." The Istream content is never destroyed.

### The Append-Only Foundation

The entire storage model is built on this principle:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

Content is appended to the permascroll. Nothing is overwritten. Nothing is removed. The I-address is a permanent coordinate in an ever-growing space.

### Why This Must Be So

Four of Nelson's fundamental guarantees depend on this invariant:

1. **Permanence**: "Any address of any document in an ever-growing network may be specified by a permanent tumbler address." [LM 4/19] — If placing content elsewhere could alter the original, addresses would not be permanent.

2. **Attribution**: The I-address encodes origin. If content were duplicated rather than referenced, the duplicate would have a different I-address, severing the attribution chain.

3. **Royalties**: "There is a royalty on every byte transmitted. This is paid automatically by the user to the owner every time a fragment is summoned." [LM 2/43] — Royalties flow to the owner of the home document. If the original were not retrievable at its original address, the royalty mechanism would break.

4. **Link survivability**: "Links between bytes can survive deletions, insertions and rearrangements, if anything is left at each end." [LM 4/43] — Links point to I-addresses. If placing content elsewhere could change those addresses, links would break.

### The Metaphor

Nelson's glass-pane metaphor captures this precisely:

> "Think of the present document as a sheet of glass. It may have writing painted on it by the present author; it may have clear glass, windowing to something else; the next pane may be in turn made of more layers of painted glass, with more windows, and so on indefinitely." [LM 2/34]

When you look through a window, you see the original — you do not see a copy that replaced it. The original is still there, at its original address, unchanged.

---

### Summary

The answer is **yes**, unconditionally. The original content's permanent identity must remain unchanged and retrievable at its original address after it is placed elsewhere. This is the central architectural invariant of Xanadu — the separation of permanent content (Istream) from mutable arrangement (Vstream). COPY creates references, not duplicates. The original is always at home, always retrievable, always attributable.
