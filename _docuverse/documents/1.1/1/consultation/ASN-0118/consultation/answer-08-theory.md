## Question 8 [theory]

> What must the system guarantee about the survival of links anchored to content that is reused through transclusion?

## The Guarantee: Links Survive Because They Bind to Istream, Which Transclusion Shares

The system must guarantee that **a link anchored to content survives the reuse of that content through transclusion, and remains valid even if the content is later deleted from its original document's current version.** This follows directly from how links and transclusion both attach to the permanent Istream address space.

### Why this holds

**1. Links bind to bytes, not positions.** A link is "a strap between bytes" whose anchors are Istream (content-identity) addresses, not Vstream positions:

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes. This has a crucial advantage: it means that links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them." (4/42)

> "Links between bytes can survive deletions, insertions and rearrangements, if anything is left at each end." (4/43)

**2. Transclusion shares the same Istream addresses.** Transcluded ("included") content is not a copy — it is the *same* bytes referenced from their home location:

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." (4/11)

Because the link's endset and the transclusion both map to the same positions on "the universal address space, the tumbler line" (endsets, 4/45), the link's anchor is preserved by the reuse rather than orphaned by it.

**3. The content cannot be destroyed out from under the link.** Crucially, deletion by the original owner does not break links into transcluded content, because the bytes persist:

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." (4/11)

Deletion is a Vstream operation, not an Istream one — deleted bytes are "not currently addressable, awaiting historical backtrack functions, may remain included in other versions" (4/9). So as long as the content survives anywhere (including in a transcluding document), the link's anchor survives.

### What this means concretely

- A link to content X remains valid when X is transcluded into a new document — the strap stays on the same bytes.
- The link survives even if the original author deletes X from their own current version, since X still exists in Istream and in the transclusion.
- Because link search matches by *address* (not by which document the bytes currently appear in), the link to transcluded content remains **discoverable** — you can ask "what links here?" against the reused content and still find it (bidirectional discovery, three-endset-links / 4/60: "THE QUANTITY OF LINKS NOT SATISFYING A REQUEST DOES NOT IN PRINCIPLE IMPEDE SEARCH ON OTHERS").

### The principle

This is the convergence of three of Nelson's guarantees — **permanence** (Istream addresses never change), **non-destruction** ("without damaging the originals," 2/45), and **link survivability** — all resting on the single architectural decision to anchor links to content identity rather than to position. Transclusion is reference, not copy, so reusing content carries its link-anchorability with it rather than severing it.

---

One framing above goes slightly beyond an explicit Nelson sentence: the curated sources never state in one place "links anchored to transcluded content survive the transclusion" as a single sentence. The conclusion is a synthesis of link-survivability (4/42–43), transclusion-as-shared-Istream (4/11), and delete-semantics (4/9, 4/11), each individually verified. If you want a verbatim passage tying links and inclusion together directly, I'd check: NEED_RAW: 4/49-4/53 (link-types, quote-link vs. inclusion discussion).
