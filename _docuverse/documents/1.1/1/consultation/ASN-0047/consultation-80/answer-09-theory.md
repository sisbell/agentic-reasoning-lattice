## Question 9 [theory]

> In Nelson's design, does "forking" (LM 4/29 "the new document's id will indicate its ancestry") refer specifically to version creation (k=1 in this ASN's terms), or does it cover all new-document-with-transclusion patterns including k=0 sibling and k=2 hierarchical descent?

Looking at this carefully, I need to first clarify the quote attribution, then address the substance.

**Quote location correction:** The phrase "the new document's id will indicate its ancestry" actually appears at **4/66** under `CREATENEWVERSION`, not 4/29. At 4/29 Nelson says something related but distinct:

> "The Document field of the tumbler may be continually subdivided, with new subfields in the tumbler indicating daughter documents and versions." [LM 4/29]

And critically, on the same page, he disclaims derivation semantics:

> "In a sense the version, or subdocument number is only an accidental extension of the document number, and strictly implies no specific relationship of derivation." [LM 4/29]

**Substantive answer:**

Nelson distinguishes between two different things that share the word "forking":

1. **Forking as a structural addressing mechanism** (4/19–4/20) is universal. It applies uniformly to all subdivision under owned addresses:
   > "One digit can become several by a forking or branching process. This consists of creating successive new digits to the right; we call these 'under' the previous digit." [LM 4/20]
   > "The entire tumbler works like that: nodes can spin off nodes; accounts can spin off accounts; nodes can spin off accounts; and so on." [LM 4/19]

   This mechanism covers your k=0 sibling, k=1 version, and k=2 hierarchical-descent patterns indifferently — they're all just sub-address allocation under owned numbers.

2. **CREATENEWVERSION (4/66)** is the *specific operation* that couples address-level forking with content-level transclusion:
   > "This creates a new document with the contents of document <doc id>. It returns the id of the new document. The new document's id will indicate its ancestry." [LM 4/66]

   This is the *only* FEBE operation Nelson specifies that combines a forked address with automatic full-content transclusion (your k=1).

3. **CREATENEWDOCUMENT (4/65)** creates an *empty* document — no transclusion:
   > "This creates an empty document. It returns the id of the new document." [LM 4/65]

**Direct answer to your question:**

The "ancestry indication" at 4/66 refers specifically to **k=1 version creation** as an operation. CREATENEWVERSION is the only operation Nelson defines that pairs forking with transclusion.

However, the *forking mechanism itself* (4/19–4/20, 4/29) is structurally indifferent to which k applies. And Nelson's disclaimer at 4/29 is decisive: the address subdivision is "accidental" and "strictly implies no specific relationship of derivation." Any "ancestry" an address signals is positional/structural, not semantic.

For k=0 sibling and k=2 hierarchical-descent patterns *with transclusion*: Nelson does not specify dedicated operations. They would have to be constructed by combining CREATENEWDOCUMENT with COPY operations (the COPY operation at 4/67 is the transclusion primitive). Whether the resulting address would be a "fork" of the source is a separate choice from whether content is transcluded — they're orthogonal in Nelson's design.

**The deeper intent:** Nelson decoupled address structure from derivation semantics deliberately. Derivation claims belong in *links* (supersession links, counterpart links, quote-links), not in the address itself. The address tells you where something *lives*; links tell you what it *means*. So "forking" as Nelson uses it should not be read as a semantic claim about derivation at all — for any value of k.

NEED_RAW: 4/29 (page-196), 4/65–4/66 (page-232–233) — to verify whether Nelson discusses k=0/k=2 transclusion patterns explicitly anywhere in the CREATENEWDOCUMENT/CREATENEWVERSION discussion that the curated extracts may have abbreviated.
