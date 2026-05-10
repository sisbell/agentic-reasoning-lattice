## Question 3 [nelson]

> Must link discovery span all documents in the system, or is it bounded to links defined within the same document as the queried content?

## Link discovery spans the entire docuverse

Nelson is unambiguous: link discovery is **not** bounded to the document containing the queried content. It must span all documents in the system. This is architecturally necessary and explicitly specified at multiple levels.

### The protocol proves it

The `FINDLINKSFROMTOTHREE` operation takes a **home-set** parameter that controls where to search for links. Nelson specifies:

> "This returns a list of all links which are (1) in \<home set\>, (2) from all or any part of \<from set\>, and (3) to all or any part of \<to set\> and \<three set\>." [LM 4/69]

> "If the home-set is the whole docuverse, all links between these two elements are returned." [LM 4/63]

The home-set can be narrowed for efficiency, but the *default scope* is the entire docuverse.

### The user-facing guarantee demands it

Nelson states the reader's right explicitly:

> "The reader should be able to ask, for a given document or place in the document, 'What connects here from other documents?'—and be shown all these outside connections without appreciable delay." [LM 2/46]

"From other documents" — not just within the current document.

### The link storage model requires it

Links live in their **home document**, which is determined by who created the link — not by what the link points to:

> "A link need not point anywhere in its home document. Its home document indicates who owns it, and not what it points to. Conversely, links connecting parts of a document need not reside in that document." [LM 4/12]

If Alice creates a comment link pointing to Bob's text, that link lives in Alice's document. Bob can only discover it if the system searches *across* documents. A document-local search would miss every incoming link from every other user. This would defeat the entire purpose of the link mechanism.

### The system is designed for global link scale

Nelson addresses the performance concern directly:

> "THE QUANTITY OF LINKS NOT SATISFYING A REQUEST DOES NOT IN PRINCIPLE IMPEDE SEARCH ON OTHERS." [LM 4/60]

This guarantee only matters if the search space includes links from across the docuverse. If search were document-local, the junk-link scaling problem wouldn't arise.

### The link mechanism's stated purpose is system-wide

> "The link mechanism ties together the whole corpus of materials on the Xanadu system. There is essentially nothing in the Xanadu system except documents and their arbitrary links." [LM 4/41]

"The whole corpus" — not individual documents.

### Filtering narrows scope; the default is global

Nelson provides filtering ("sieving") for managing the flood of cross-document links:

> "Thus it becomes necessary to apply some kind of filter, saying, 'What links come in from Spain? From last week? From persons of importance to me?'" [LM 2/47]

Filtering presupposes a global search that returns too much. If search were document-local, filtering would rarely be needed.

---

**Summary:** Link discovery must span the entire docuverse. The home-set parameter on `FINDLINKSFROMTOTHREE` allows *narrowing* the scope, but the architecture indexes links globally by all three endsets, enabling bidirectional discovery across all documents. A system that only found links within the queried document would violate the backlink guarantee, the cross-document connection guarantee, and the fundamental purpose of the link mechanism.
