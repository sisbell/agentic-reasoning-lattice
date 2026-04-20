## Question 9 [nelson]

> Can a link connect two spans within the same document, or must a connection always cross a document boundary?

## Yes — Links Can Connect Spans Within the Same Document

Nelson explicitly contemplates intra-document links. The clearest evidence is this statement:

> "A link need not point anywhere in its home document. Its home document indicates who owns it, and not what it points to. **Conversely, links connecting parts of a document need not reside in that document.**" [LM 4/12]

The phrase "links connecting parts of a document" (singular) directly acknowledges links whose from-set and to-set both point within the same document. The sentence then adds that such links don't even need to *reside* in that document — they could live in a different document entirely.

### The Architecture Imposes No Boundary Requirement

Endsets point to arbitrary spans "anywhere in the docuverse":

> "The from-set may be an arbitrary collection of spans, pointing anywhere in the docuverse. Similarly, the to-set may be an arbitrary collection of spans pointing anywhere in the docuverse." [LM 4/43]

"Anywhere" includes within the home document, within a different single document, or spanning multiple documents. The link mechanism is agnostic about document boundaries — it operates on byte addresses in tumbler-space, not on document containers.

### Standard Link Types That Are Explicitly Intra-Document

Several of the proposed standard link types only make sense within a single document:

| Type | Purpose |
|------|---------|
| **Heading Link** | "Internal heading or subtitle within document" [LM 4/53] |
| **Paragraph Link** | "Points front end to a paragraph for navigation" [LM 4/53] |
| **Footnote Link** | "Provides a break sequence for an author" [LM 4/53] |

These are structural markers — a heading link connects a title span to the section it names, all within the same document.

### Three Independent Concepts: Home, From, To

The MAKELINK operation makes the independence explicit:

> "The document must be specified because that determines the actual residence of the link — since a document may contain a link between two other documents." [LM 4/63]

The home document (ownership), the from-set targets, and the to-set targets are three independent concerns. All three can be the same document, all different, or any combination. The system doesn't distinguish these cases architecturally.

### Summary

Links are connections between byte-spans in tumbler-space. Document boundaries are organizational, not structural barriers. A link from paragraph 3 to paragraph 7 of the same document works identically to a link from your document to mine — same mechanism, same endset conventions, same search operations.
