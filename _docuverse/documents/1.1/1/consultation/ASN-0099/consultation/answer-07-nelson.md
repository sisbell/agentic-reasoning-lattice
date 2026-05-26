## Question 7 [nelson]

> Does the design treat links originating from the content and links pointing to the content as equally discoverable, or does directionality affect what the query returns?

## Equal Discoverability: The Design Is Symmetric

The short answer: **both directions are equally discoverable.** Directionality is a semantic property of links (what "from" and "to" mean in context), not a constraint on what queries can find. The system indexes links by all three endsets and supports search from any direction.

---

### The Single Search Operation

There is one link search operation, and it handles all directions through a single mechanism:

> "This returns a list of all links which are (1) in \<home set\>, (2) from all or any part of \<from set\>, and (3) to all or any part of \<to set\> and \<three set\>." — 4/69

The operation takes four constraint parameters: home-set, from-set, to-set, and three-set (type). Any parameter can be set to the entire docuverse (unconstrained). This means:

- **Find what links FROM this content:** constrain the from-set, leave to-set as whole docuverse
- **Find what links TO this content:** constrain the to-set, leave from-set as whole docuverse
- **Find links OF a specific type:** constrain the three-set
- **Find links in a specific home document:** constrain the home-set

The same operation, the same indexing, the same performance guarantee. No asymmetry.

### The Satisfaction Model

Link search uses what Nelson calls "the AND of the ORs":

> "A link satisfies a search request if one span of each endset satisfies a corresponding part of the request." — 4/58

Each endset is checked independently against the corresponding constraint. The system does not privilege from-set over to-set or vice versa.

### The Performance Guarantee

> "THE QUANTITY OF LINKS NOT SATISFYING A REQUEST DOES NOT IN PRINCIPLE IMPEDE SEARCH ON OTHERS." — 4/60

This applies regardless of direction. Whether you're searching for outgoing or incoming links, the system scales the same way.

---

### Semantic Directionality vs. Structural Symmetry

Links are semantically directional — they have a from-set and a to-set with user-defined meaning:

> "A link is typically directional. Thus it has a from-set, the bytes the link is 'from,' and a to-set, the bytes the link is 'to.' (What 'from' and 'to' mean depend on the specific case.)" — 4/42

A citation link goes FROM the citing passage TO the source. A comment link goes FROM the commentary TO the subject. The direction carries meaning.

But structurally, the system treats both ends identically:

> "The from-set may be an arbitrary collection of spans, pointing anywhere in the docuverse. Similarly, the to-set may be an arbitrary collection of spans pointing anywhere in the docuverse. We adopt the same convention for link types." — 4/43

All three endsets follow the same convention, use the same indexing, and support the same search operations.

---

### The In-Link / Out-Link Distinction

Nelson does distinguish between a document's **out-links** (links it contains) and **in-links** (links stored elsewhere pointing to it):

> "Ordinarily a document consists of its contents (including history and alternatives) and its out-links, the links it contains that point to other documents. By contrast, a document's in-links are those stored elsewhere which point to it. These out-links are under control of its owner, whereas its in-links are not." — 2/31

But this distinction is about **ownership**, not **discoverability**. Out-links are owned by the document's owner. In-links are owned by whoever created them. Both are fully discoverable:

> "The reader should be able to ask, for a given document or place in the document, 'What connects here from other documents?'— and be shown all these outside connections without appreciable delay." — 2/46

Nelson explicitly requires that in-links (the "harder" direction in most systems) be shown "without appreciable delay." This is the backlinks problem, and the design solves it by indexing all endsets symmetrically.

---

### Summary

| Property | From-set | To-set | Type (3-set) |
|----------|----------|--------|--------------|
| Searchable? | Yes | Yes | Yes |
| Same operation? | Yes — FINDLINKSFROMTOTHREE | Same | Same |
| Same indexing? | Yes | Yes | Yes |
| Performance guarantee? | Same | Same | Same |
| Arbitrary span-set? | Yes | Yes | Yes |

Directionality tells you what a link **means**. It does not affect what a query **returns**. The design is structurally symmetric across all three endsets.
