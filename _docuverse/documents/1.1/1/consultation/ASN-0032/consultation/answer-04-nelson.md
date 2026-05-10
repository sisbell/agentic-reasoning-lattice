## Question 4 [nelson]

> Must a link be visible and discoverable from both ends — so that an author can always see who has linked to their content?

## Yes — Bidirectional Link Discovery Is a Core Guarantee

Nelson is emphatic on this point. The system architecturally ensures that for any published content, the author (or any reader) can discover all links pointing to it. This is not an optional feature but a structural property of how links work.

### The Explicit Guarantee

> "The reader should be able to ask, for a given document or place in the document, 'What connects here from other documents?'— and be shown all these outside connections without appreciable delay." [LM 2/46]

And from the windowing discussion:

> "It must also be possible for the reader to ask to see whatever documents window to the current document. Both are available at any time." [LM 2/37]

### Why This Works Architecturally

Links are indexed by **all three endsets** (from, to, type). The FEBE operation `FINDLINKSFROMTOTHREE` searches across any combination:

> "This returns a list of all links which are (1) in \<home set\>, (2) from all or any part of \<from set\>, and (3) to all or any part of \<to set\> and \<three set\>." [LM 4/69]

To find everything linking TO your document, you specify your document's address in the to-set parameter. The system returns all matching links regardless of who created them or where they live. Nelson guarantees this scales:

> "THE QUANTITY OF LINKS NOT SATISFYING A REQUEST DOES NOT IN PRINCIPLE IMPEDE SEARCH ON OTHERS." [LM 4/60]

### The Two-Sided Coin

Nelson frames this as inseparable from link freedom. You cannot have free linking without accepting discoverable incoming links:

> "Accessibility and free linking make a two-sided coin. On the one hand, each user is free to link to anything privately or publicly. By the same token, each author of a published work is relinquishing the right to control links into that work. This relinquishment must also be part of the publishing contract." [LM 2/43]

The author gives up **control** over incoming links — they cannot prevent or remove them. But they gain **visibility** — they can always see what connects to their work.

### Sieving the Avalanche

Nelson anticipated that popular documents would attract enormous numbers of incoming links, so he designed filtering:

> "Thus it becomes necessary to apply some kind of filter, saying, 'What links come in from Spain? From last week? From persons of importance to me?'" [LM 2/47]

> "This filtering by different attributes we call 'sieving', and it can only be set up for a comparatively small number of traits— say, location and author and time." [LM 2/47]

### The Private Link Nuance

One qualification: Nelson says users can link "privately or publicly" [LM 2/43]. A link in a private document would presumably be subject to that document's access restrictions. In XU.87.1 this is moot — "Currently all documents are visible to all users" [LM 4/79] — but in the full design, a private link to your published document may not be discoverable by you.

This is not a contradiction. The guarantee is that **the system provides the mechanism** for bidirectional discovery. Published links to published content are always discoverable from both ends. Private links respect their owner's privacy.

### Summary

Bidirectional link discovery is not merely supported — it is **required** by the architecture. The three-endset link structure with universal indexing means every published link is findable from the from-side, the to-side, or the type. An author can always see who has publicly linked to their work. This is what Nelson means when he says Xanadu solves "the backlinks problem" that conventional hyperlinks cannot.
