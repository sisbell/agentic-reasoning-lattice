## Question 6 [nelson]

> Can the same region of permanent content appear in more than one mapping unit within the same document, and if so, must each mapping be independently tracked?

## Yes — the same Istream content can appear at multiple Vstream positions within a single document, and each mapping must be independently tracked.

### The architecture permits it

The Vstream is a sequence of references to Istream addresses. Nothing in Nelson's specification restricts a given I-address range from appearing at more than one V-position. The COPY operation makes this explicit:

> "The material determined by \<spec set\> is copied to the document determined by \<doc id\> at the address determined by \<doc vsa\>." [LM 4/67]

The spec-set is unconstrained — it can reference any content in the docuverse, including content already present in the target document. A user could COPY the same source span to V-position 10 and again to V-position 50, producing two independent V→I mappings for the same I-content.

Nelson's description of virtual byte streams confirms this generality:

> "The virtual byte stream of a document may include bytes from any other document." [LM 4/10]

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

Each inclusion gets its own ordinal position in the byte stream regardless of origin — including the case where origin is shared.

### The windowing model makes it natural

Consider a literary essay that quotes the same passage at its opening and its conclusion. Each quote is a separate window to the same source:

> "A compound document consists of parts of old documents together with new material. Or we may say it really consists of quote-links and new material." [LM 2/32]

Each window is an independent mapping. The glass-pane metaphor illustrates this: two transparent openings in the same sheet can both look through to the same underlying content.

### Each mapping must be independently tracked

Three properties of the architecture require independent tracking:

**1. V-addresses are dense and contiguous.** If the document has 100 bytes, V-addresses run 1–100 with no gaps. If I-addresses 500–509 appear at both V-positions 10–19 and V-positions 60–69, the positional mapping (POOM enfilade) must maintain both entries to preserve the contiguous V-address sequence.

**2. Editing operations are V-addressed.** DELETEVSPAN removes a V-span; INSERT shifts V-addresses after the insertion point:

> "The v-stream addresses of any following characters in the document are increased by the length of the inserted text." [LM 4/66]

Deleting V-positions 10–19 must close that gap and shift subsequent V-addresses without disturbing V-positions 60–69 (now 50–59 after renumbering). This requires independent tracking of each V→I mapping.

**3. Links attach to content, not positions — but through V-addresses.** A link's endset specifies spans. If a user creates a link whose from-set covers V-positions 10–19 and another link covering V-positions 60–69, these are distinct links to distinct V-positions, even though both resolve to the same I-content. The link survivability guarantee applies independently to each:

> "Links between bytes can survive deletions, insertions and rearrangements, if anything is left at each end." [LM 4/43]

Deleting one occurrence leaves the other intact, and any links attached to the surviving occurrence remain valid.

### Correspondence recognizes the relationship

The correspondence mechanism detects when V-positions share Istream origin, whether across versions or within a single document:

> "Of course, a facility that holds multiple versions of the same material, and allows historical backtrack, is not terribly useful unless it can help you intercompare them in detail—unless it can show you, word for word, what parts of two versions are the same." [LM 2/20]

SHOWRELATIONOF2VERSIONS "returns a list of ordered pairs of the spans of the two spec-sets that correspond" [LM 4/70]. The same mechanism would identify that two V-regions within a single document share I-origin — useful for front-ends that want to highlight repeated content.

### Summary

The Vstream is a mapping, not a bijection. The same I-content can be mapped to multiple V-positions. Each mapping is a separate entry in the positional structure, independently subject to editing operations, independently targetable by links, and identifiable as corresponding through shared Istream origin.
