## Question 2 [theory]

> When two documents contain the same content, must the design treat that content as one shared entity rather than two copies?

**No.** The design distinguishes content by **provenance**, not by textual equivalence. Identical text in two documents may be one shared entity *or* two separate entities, depending on how each came to be.

The foundational distinction is between **native bytes** and **non-native bytes**:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

If Alice writes "the cat sat on the mat" and Bob *independently* types the same words, these are two distinct entities at two distinct Istream addresses. Neither quoted the other; neither owes the other royalty. If Bob *windows* Alice's sentence into his document, however, only one entity exists—Alice's—and Bob's document holds a reference, not a copy. The mechanism is transclusion:

> "Someone else may create a document which quotes it as much as desired. This mechanism we call the quote-window or quote-link. Through a 'window' in the new document we see a portion of the old." [LM 2/32]

**Why provenance and not equivalence?** Because the system must honor authorship. To treat coincidentally-identical text as "the same" would be to claim Bob quoted Alice when he did not. Transclusion is an *act*—a deliberate inclusion by reference—and that act is what creates sharing. The I-address records who created the bytes, not what they say.

The system does provide ways to discover or assert equivalence when it matters:
- **FINDDOCSCONTAINING** locates all documents that include specified material by Istream origin
- **Counterpart links** let users explicitly assert that two distinct entities correspond, e.g., for translations or parallel passages [LM 4/53]

So the design must *not* collapse the two cases. Transclusion gives users the ability to share one entity across many documents. Independent creation gives users the right to write the same words without being treated as quoters. Literature depends on that distinction.
