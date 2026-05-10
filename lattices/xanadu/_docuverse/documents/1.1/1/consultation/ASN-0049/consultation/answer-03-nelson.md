## Question 3 [nelson]

> Can a document owner control the ordering and arrangement of shared content within their document independently of how it appears in the source document?

**Yes, absolutely.** This is one of the most fundamental architectural properties of Xanadu. Each document has its own independent V-space arrangement, and the document owner has full control over it — regardless of how the same content is arranged in its source document.

## The Architectural Basis: I-Space / V-Space Separation

The entire Xanadu model rests on separating **content identity** (I-space) from **content arrangement** (V-space):

- **I-Space**: Where content permanently lives. Immutable. Shared across documents.
- **V-Space**: The document's current arrangement. Mutable. Per-document, per-version.

When you transclude content, you are creating a V-space mapping in *your* document that points to I-space content owned by *someone else*. Your V-space is entirely yours to arrange.

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

The phrase "just as if they were native" is the key guarantee. Transcluded bytes participate in your V-space on equal footing with bytes you wrote yourself. They have positions in *your* virtual byte stream that *you* control.

## Operations Confirm Owner Control

The FEBE protocol makes this explicit. The COPY operation (which creates transclusions) places content at a V-address the owner specifies:

> "The material determined by \<spec set\> is copied to the document determined by \<doc id\> at the address determined by \<doc vsa\>." [LM 4/67]

The owner chooses *where* in their document the transcluded content goes. And REARRANGE lets them move it later:

> "Rearrange transposes two regions of text." [LM 4/67]

INSERT and DELETE also operate on the owner's V-space freely, regardless of whether the affected regions contain native or transcluded content.

## The Shakespeare Example

Nelson provides a vivid illustration. If *Hamlet* is already published in the system, E.G. Jewett can create his own version:

> "a quote-link to the first part of the original, just up to 'in the soliloquy'; then the word 'luge'; then a quote-link to the rest of the play." [LM 2/33]

Jewett has taken Shakespeare's content and arranged it in his own V-space — splitting it, inserting his own material between the pieces, creating a completely different arrangement than the original. The original *Hamlet* is untouched:

> "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate — without damaging the originals. This is done by inclusion links." [LM 2/45]

## The Glass Pane Metaphor

Nelson's metaphor makes the independence visual:

> "Think of the present document as a sheet of glass. It may have writing painted on it by the present author; it may have clear glass, windowing to something else; the next pane may be in turn made of more layers of painted glass, with more windows, and so on indefinitely." [LM 2/34]

Your glass pane is *yours*. You decide where to paint, where to leave windows, and in what order. The content visible through those windows comes from elsewhere, but the arrangement of the pane itself — where each window is placed relative to your painted text — is entirely under your control.

## Compound Documents as Independent Entities

Nelson explicitly states that compound documents (those containing transclusions) are full documents with independent ownership:

> "Each compound document is like the other documents: it has an owner and receives royalties." [LM 2/33]

And the version-by-inclusion model confirms that alternative arrangements are first-class:

> "There is thus no 'basic' version of a document set apart from other versions — 'alternative' versions — any more than one arrangement of the same materials is a priori better than other arrangements." [LM 2/19]

## Summary

The answer is an unqualified yes. V-space arrangement is per-document and under the document owner's exclusive control. What is *shared* across documents is I-space identity (the permanent bytes). What is *independent* is V-space arrangement (how those bytes are ordered and composed). This separation is the architectural core of Xanadu — it is what makes editing non-destructive, versions meaningful, and compound documents possible.
