## Question 5 [theory]

> What does presenting the text-extent and the link-extent together reveal about a document that asking for either one alone could never show?

The two operations sit side by side in FEBE for exactly this reason:

- **RETRIEVEDOCVSPAN** — "This returns a span determining the origin and extent of the V-stream of document <doc id>." (4/68)
- **RETRIEVEDOCVSPANSET** — "This returns a span-set indicating both the number of characters of text and the number of links in document <doc id>." (4/68)

## What each number alone tells you

A Xanadu document is not one thing but two interleaved things, living in two subspaces of the document's address space:

| Subspace | Address pattern | Contents |
|----------|-----------------|----------|
| Bytes | `version.position` (1.x) | Text content |
| Links | `version.0.2.N` | Links the document is home to |

The text-extent measures the first dimension; the link-extent measures the second. Ask for the text alone and you learn how much *matter* a document carries, but nothing about how *connected* it is. Ask for the link count alone and you learn how many connections the document anchors, but nothing about how much content those connections hang on.

## What the pair reveals

Presented together, the two extents reveal the document's **character — its ratio of original matter to connective structure**, which is the one thing neither number can show by itself. This matters because in Nelson's model a document can be made *entirely* of either:

> "By this convention, then, everything in the system is part of a document. No free-floating materials exist. Thus the 'Jabberwocky' is a document; and a set of links between them, were someone to create it, would yet be a separate document." (2/29)

So the span-set distinguishes kinds of document that look identical from one axis:

- **High text, near-zero links** → original prose, a piece of writing standing largely on its own.
- **Near-zero text, high link count** → a purely connective document: a directory document, a link-set, an annotation or commentary layer that contributes structure rather than words.
- **Both substantial** → a compound document or collage — new matter woven through with quote-links and connections, the "annotated collage" form Nelson describes (2/45).

This reflects what a document *is* in the design: "Ordinarily a document consists of its contents (including history and alternatives) and its out-links, the links it contains that point to other documents." (2/31) The span-set is the only retrieval that returns *both* halves of that definition at once — the complete shape of the document across both the dimensions that constitute it.

In short: either number gives you a size; together they give you a **proportion**, and the proportion is what tells you whether you are holding a piece of writing, a piece of connective tissue, or a weaving of the two.
