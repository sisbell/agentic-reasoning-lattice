## Question 4 [theory]

> What relationship must a link's home document bear to the documents whose content regions its endsets reference — may a link live anywhere, independent of what it connects?

A link's home document is **completely independent** of the documents it connects. The home indicates *who owns* the link — not *what it points to*.

## The Core Principle

Nelson states this explicitly in the curated sources:

> "A link need not point anywhere in its home document. Its home document indicates who owns it, and not what it points to. Conversely, links connecting parts of a document need not reside in that document." (4/12)

This means a link's home and its endsets are decoupled along two dimensions:

1. **A link can live somewhere it doesn't point to** — its home document need not be referenced by any of its endsets.
2. **A link can point into documents it doesn't live in** — a link connecting parts of document X need not reside in X.

## What the Home Document Determines

The home document's only structural role is to establish **ownership**:

> "A link's home document indicates who owns it—not what it points to. Links connecting parts of a document need not reside in that document. Conversely, a link need not point anywhere in its home document. Ownership and application are independent." (documents.md, Chapter 4 summary)

The MAKELINK operation confirms this — the document is specified separately from the endsets precisely because it determines residence/ownership, not connection:

> "The document must be specified because that determines the actual residence of the link--since a document may contain a link between two other documents." (4/63, operations.md)

## Why This Design Matters

This independence is what makes annotation and commentary possible without modifying anyone else's work. From `links.md`:

> "Your links are yours (at your address, under your control). But they're visible to anyone reading the linked material. The link doesn't modify the target document - it exists independently."

You can comment on someone else's published document by creating a link whose endsets reach into their content, while the link itself lives at *your* address, under *your* ownership. The Tumbler Square visualization reinforces this geometry:

> "A link's home (any home) is an element located on one side; and its three endsets map to the other sides." (4/46, endsets.md)

The home sits on one side of the square; the from-set, to-set, and type reach out to arbitrary spans elsewhere in the docuverse.

## Answer in Brief

**A link may live anywhere, fully independent of what it connects.** There is no required relationship between a link's home document and the documents whose regions its endsets reference. The home determines ownership; the endsets determine connection; the two are orthogonal.
