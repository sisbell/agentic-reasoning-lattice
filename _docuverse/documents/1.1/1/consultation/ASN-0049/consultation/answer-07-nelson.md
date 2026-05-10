## Question 7 [nelson]

> If a document shares content from multiple sources, must the system guarantee that a reader can distinguish which portions came from which original documents?

# Yes — Absolutely and Structurally

This is one of the firmest guarantees in the entire system. It is not a feature bolted on; it is a consequence of the architecture itself.

## The Guarantee

> "This world nevertheless remains simple in design. The virtuality is simple in structure and repeats in layers. You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

For *any* character in *any* compound document, the system can identify which original document created it. This applies regardless of how many sources contribute content, how deeply nested the transclusions are, or how many times content has been re-transcluded.

## Why It Is Structural, Not Metadata

Every byte in the docuverse has a permanent I-space address encoding its origin:

```
Node.0.User.0.Document.0.Element
```

The Document field directly identifies which document created that byte. When content is transcluded, it is not copied — it is referenced at its permanent I-address:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

The system structurally distinguishes native bytes (created in this document) from included bytes (transcluded from elsewhere). To fetch transcluded content, the system *must* request it from its home location. The connection to the source cannot be severed because the retrieval mechanism requires it.

## The Glass Pane Model

Nelson's metaphor makes the distinction visual:

> "Think of the present document as a sheet of glass. It may have writing painted on it by the present author; it may have clear glass, windowing to something else; the next pane may be in turn made of more layers of painted glass, with more windows, and so on indefinitely." [LM 2/34]

A compound document has two kinds of content:
- **Painted content** — native bytes, created by this document's author
- **Windows** — transparent openings showing content from other documents

The layering can go arbitrarily deep. Document A windows to B, which windows to C. At every layer, the system knows which glass pane each character lives on.

## Content Identity vs. Content Value

The distinction goes deeper than "where did this come from." The system distinguishes *identity* from *coincidence*:

Two documents with identical text created independently have **different** I-addresses. Transcluded content **shares** the same I-address as the original. This is how the system distinguishes "wrote the same words" from "quoted from the original" — a distinction impossible in copy-based systems.

## The Reader's Power

The reader can always investigate provenance:

> "As already stated, it is possible for the reader to ask to see the materials which are windowed to by a given document. However, it must also be possible for the reader to ask to see whatever documents window to the current document. Both are available at any time." [LM 2/37-2/38]

And the FEBE protocol provides a specific operation:

> **FINDDOCSCONTAINING**: "This returns a list of all documents containing any portion of the material included by \<vspec set\>." [LM 4/70]

This lets you trace content in either direction — from a compound document, find all sources; from a source, find all documents that include it.

## One Nuance: Display vs. Structure

Nelson distinguishes between a **quote-link** (which explicitly marks quotation to the reader) and an **inclusion** (which may not be visually indicated by default) [LM 4/53]. This means the front end may not *always* visually highlight every transcluded portion by default.

But the structural guarantee is absolute. The system *always* knows. The reader can *always* ask. The front end chooses how prominently to display provenance, but it cannot hide what the architecture makes permanently discoverable.

## Summary

The guarantee is threefold:

1. **Structural** — Every byte's I-address encodes its home document. This cannot be stripped.
2. **Queryable** — The reader can always ask "where did this come from?" for any character.
3. **Bidirectional** — From any document, find its sources; from any source, find all documents that include it.

This is not an optional feature. It falls out of the I-space/V-space separation, the transclusion-not-copying model, and the permanent addressing system. A system that copies content instead of referencing it cannot provide this guarantee. That is precisely why Nelson rejected copying.
