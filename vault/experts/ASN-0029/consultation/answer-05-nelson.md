## Question 5 [nelson]

> Must every document in the docuverse be unique, and what prevents two users from creating documents that the system treats as identical?

## Document Uniqueness in the Docuverse

**No, documents need not be unique in content.** Two users can independently create documents with byte-for-byte identical text, and the system treats them as entirely distinct documents. Nothing prevents this, and nothing checks for it.

### Identity Is Structural, Not Value-Based

The critical distinction is between **content identity** (where bytes were created) and **content value** (what the bytes say). Xanadu tracks identity, not value.

Every document gets a unique tumbler address determined by its ownership path:

> "There are four major fields, each expandable indefinitely, with three major dividers between them. These fields are Server, User, Document and Contents." [LM 4/26]

If Alice creates a document, it lives at `ServerA.0.Alice.0.Doc1`. If Bob independently types the same text, his document lives at `ServerB.0.Bob.0.Doc1`. Different I-space addresses, different documents — regardless of identical content.

> "The basic principle is that of owned numbers. Numbers are owned by individuals or companies, and subnumbers under them are bestowed on other individuals and companies on whatever basis the owners choose." [LM 4/17]

The tumbler hierarchy guarantees address uniqueness through ownership delegation. No coordination is needed; no central authority checks for duplicates.

### Transclusion vs. Independent Creation

This design is what makes transclusion meaningful. From the provenance model:

- **Transcluded content SHARES I-addresses** — Alice windows Bob's paragraph, and both reference the same I-space bytes. The system knows they are the same content.
- **Independently created content has DIFFERENT I-addresses** — Alice types the same words Bob typed, but her bytes live at her address. The system treats them as unrelated.

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

This is how the system distinguishes "quoted from the original" from "happened to write the same words." The operation `FINDDOCSCONTAINING` finds documents sharing I-space material (transclusions), not documents with identical byte values.

### No Verification of Any Kind

The system explicitly disclaims content verification:

> "User acknowledges that all material on the network is stored by users under similar arrangements to User's own, without verification or assurance of truth, authenticity, accuracy, usefulness or other beneficial character of such materials." [LM 5/17]

There is no uniqueness check, no deduplication, no content hashing. The system does not examine what you store — it only tracks where you store it and who owns it.

### Why This Is By Design

This follows from two principles:

1. **Ownership is absolute.** Your document is yours. Its identity comes from your act of creation at your address, not from what you wrote. Two people writing the same sentence have each created something they own independently.

2. **Attribution is structural.** If the system deduplicated identical content, it would destroy attribution — whose document would the shared bytes "belong" to? By keeping I-addresses distinct per creation event, every byte has exactly one home document and one owner.

> "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

### The Practical Implication

If you want the system to know that your content came from someone else's document, you must **transclude** (use COPY in FEBE), not retype. Retyping creates new I-space bytes at your address. Transclusion creates a V-space reference to existing I-space bytes at the original address. Only transclusion preserves the connection, triggers royalties, and enables `FINDDOCSCONTAINING` to discover the relationship.
