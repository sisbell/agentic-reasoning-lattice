## Question 6 [theory]

> How should the system treat content that was deleted from one document but remains present in another document sharing the same history?

# Deletion in Shared-History Documents

The system must treat such content as fully preserved and continuously accessible from the other document. Deletion is a Vstream operation only — it removes content from one document's current arrangement without touching the content itself or affecting any other document that shares it.

## The Core Guarantee

Nelson is explicit on this point at 4/11:

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included."

The diagram on 4/9 formalizes this with the "DELETED BYTES" state annotation:

> "(not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)"

## Why This Works

When two documents share history — whether via `CREATENEWVERSION` (a fork) or via transclusion windowing the original — both reference the same **Istream** content. They have independent **Vstream** arrangements but a shared Istream identity. Deleting from one document modifies only that document's view; the underlying bytes are untouched and remain visible to the other document's Vstream.

## The Governing Principle

This follows directly from Nelson's foundational rule that "modifications never damage originals" (LM 2/45):

> "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate--without damaging the originals. This is done by inclusion links."

And:

> "The old viewpoint is still present too--you can always say, 'Show me what this originally was.'" (LM 2/45)

## What the Deleting User Loses (Nothing Permanent)

Even from the deleter's perspective, nothing is destroyed:
- The content remains in Istream at its permanent I-address
- Previous versions of the deleter's own document still contain it
- Links pointing to that I-address still resolve
- Historical backtrack can restore it

## Ownership Asymmetry

A user who originally created content cannot reach across and "pull it back" from documents that have legitimately included it. Once content is published and others have windowed it, those other documents are governed by *their* owners' Vstream arrangements. Ownership of content does not confer veto over others' views of it — only over your own.

This is the entire point of Xanadu's reference-not-copy model: the deletion authority is scoped to the document, and the document is just a Vstream over shared Istream.
