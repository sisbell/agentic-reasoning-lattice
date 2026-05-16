## Question 2 [nelson]

> Must the system guarantee that a newly created link is immediately visible to all users who retrieve any content referenced by that link's endsets?

## No — Nelson Does Not Guarantee Immediate Link Visibility

Nelson specifies that link discovery should be *fast* and that the docuverse should *appear unified*, but he does not guarantee that a newly created link is immediately visible to all users across the network. Several aspects of his design actively work against such a guarantee.

### What Nelson DOES Say About Link Discovery Timing

The closest statement to a visibility guarantee is about *querying* existing links, not about propagation after creation:

> "The reader should be able to ask, for a given document or place in the document, 'What connects here from other documents?'— and be shown all these outside connections without appreciable delay." [LM 2/46]

"Without appreciable delay" addresses **query latency**, not **propagation latency**. It says: once the system knows about a link, finding it should be fast. It does not say: the system must know about a link everywhere instantly after creation.

### What Works Against Immediate Visibility

**1. Networks are assumed broken.**

> "It is a truism that 'computer networks are always broken.' Meaning that on the average some nodes are disconnected or not working." [LM 4/75]

If nodes are routinely disconnected, immediate global visibility is physically impossible. Nelson builds this assumption into the architecture rather than fighting it.

**2. Servers hold subrepresentations, not complete state.**

> "Each server contains a map and a subset of the whole — a microcosm that shrinks and grows." [LM 4/71]

> "Each server contains a continuously valid model or subrepresentation of the entire docuverse." [LM 4/72]

"Continuously valid" means internally consistent — not globally synchronized. Each server's view is correct for what it contains, but it doesn't contain everything.

**3. Content (and by extension, links) propagate gradually.**

> "A server's network model, from the null case on up, is at all times unified and operational; whatever information moves between servers is assimilated at once to its overall structure, leaving each server in canonical operating condition with a slightly improved map of what is elsewhere. The contents can slosh back and forth dynamically." [LM 4/72]

"Slosh back and forth dynamically" and "slightly improved map" describe eventual consistency — the network converges over time, not instantly. Material moves between servers for performance and redundancy reasons:

> "Material is moved between servers for a number of purposes: 1. for more rapid access to final material, 2. for more rapid access to needed material which indexes material on other servers, 3. for rebalance in keeping with demand, 4. for redundancy and backup purposes." [LM 4/71]

**4. The "inter-indexing mechanisms" are back-end maintenance, not real-time broadcast.**

> "A Xanadu link is a connective unit, a package of connecting or marking information. It is owned by a user. It is put in by a user (or a front end), and thereafter maintained by the back end through the back end's inter-indexing mechanisms." [LM 4/41]

"Thereafter maintained" implies ongoing maintenance — the back end keeps indexes up to date over time, not that index updates are instantaneous and global.

### The Local vs. Distributed Case

Nelson's FEBE protocol presents commands as request-response pairs (MAKELINK returns a link ID, FINDLINKSFROMTOTHREE returns matching links). For a single back-end server, the natural reading is that a created link is findable on subsequent queries to that same server. But Nelson does not explicitly state even this local guarantee.

For the distributed case, the architecture clearly contemplates delay. A link created on server A will become visible to users on server B through the BEBE forwarding and subrepresentation mechanisms — but on a timeline governed by network health, demand patterns, and caching, not by a hard consistency bound.

### What Nelson Guarantees Instead

Rather than immediate visibility, Nelson guarantees:

1. **Efficient search** — "THE QUANTITY OF LINKS NOT SATISFYING A REQUEST DOES NOT IN PRINCIPLE IMPEDE SEARCH ON OTHERS." [LM 4/60]

2. **Scalable performance** — the "soft corridor" ensures query times grow logarithmically, not linearly, as the docuverse expands [LM 4/2]

3. **Eventual completeness** — through subrepresentation growth and BEBE forwarding, links will propagate to servers where they're needed

4. **Resilience** — the system handles partial network failure gracefully rather than requiring global consistency

### Summary

Nelson designs for a world where link creation is local and link discovery is eventually global. The system prioritizes **availability and partition tolerance** over **immediate consistency** — a choice forced by his explicit assumption that "networks are always broken." The user-facing promise is that links are discoverable "without appreciable delay" once the system knows about them, not that the system knows about them everywhere the instant they are created.
