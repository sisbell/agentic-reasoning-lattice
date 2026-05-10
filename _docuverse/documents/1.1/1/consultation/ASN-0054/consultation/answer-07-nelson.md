## Question 7 [nelson]

> If a document is edited so that content is inserted in the middle, what happens to the arrangement's existing pieces — must exactly one piece split into two, or can the restructuring be more complex?

## Insertion and Span Splitting

For the INSERT operation, **at most one existing piece splits into two**. The restructuring is always local and minimal.

### The Architecture

A document's V-stream (its current arrangement) is an ordered sequence of spans, each referencing a contiguous range of I-space content. When you insert at a V-space position, there are exactly two cases:

1. **Mid-span insertion**: The position falls within an existing span. That span splits into the portion before the insertion point and the portion after. The new content goes between them. **Exactly one piece becomes two.**

2. **Boundary insertion**: The position falls at the boundary between two existing spans. The new content is placed between them. **Zero pieces split.**

No other existing pieces are structurally affected. Their I-space references remain identical — only their V-addresses shift upward:

> "The v-stream addresses of any following characters in the document are increased by the length of the inserted text." (4/66)

### Why It Cannot Be More Complex

V-space is linear. Insertion happens at one point. Only the span containing that point can be affected. All other spans continue referencing exactly the same I-space bytes — the content hasn't moved, only the V-addresses have shifted. Since V-addresses are ephemeral ("may be constantly changing; the front-end application is unaware of this" — 4/11), this shift is purely a remapping, not a structural change to other pieces.

The I-space content is untouched by any V-space operation:

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." (4/11)

And the new content creates fresh I-space addresses:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." (2/14)

### What About COPY (Transclusion-Insert)?

COPY places existing I-space content at a V-position:

> "The material determined by \<spec set\> is copied to the document determined by \<doc id\> at the address determined by \<doc vsa\>." (4/67)

The spec-set can be multiple spans, so the *inserted* material may arrive as several pieces. But the effect on the *existing* arrangement is identical: at most one existing span splits at the insertion point.

### Where It Gets More Complex: REARRANGE

REARRANGE is a different story. It transposes two regions using multiple cut points:

> "Rearrange transposes two regions of text. With three cuts, the two regions are from cut 1 to cut 2, and from cut 2 to cut 3... With four cuts, the regions are from cut 1 to cut 2, and from cut 3 to cut 4." (4/67)

Each cut point that falls mid-span splits a piece. With four cuts, up to four existing pieces could split. So REARRANGE *can* produce more complex restructuring — but INSERT cannot.

### A Note on Nelson's Level of Specification

Nelson defines INSERT at the FEBE (semantic) level, not at the span-representation level. He specifies *what happens to V-addresses*, not *how the internal span list changes*. The span-splitting behavior I describe above is the necessary implementation consequence of the architecture (V-space as ordered spans over I-space), but Nelson leaves the mechanics to the enfilade data structure:

> "The Model T enfilade handles the revision of serial data very quickly and very cleanly." (1/33)

> "All changes, once made, left the file remaining in canonical order, which was an internal mandate of the system." (1/34)

The "canonical order" guarantee means the enfilade must produce exactly this result — one split, new content inserted, all addresses shifted — and remain structurally valid afterward.
