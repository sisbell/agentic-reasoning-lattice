## Question 1 [theory]

> Is arrangement reordering intended to be a permutation of a document's existing V-positions (preserving their depth and structure), or may it relocate content into V-positions at a new depth?

REARRANGE is a permutation of existing V-positions, not a mechanism for relocating content to a new "depth."

## What REARRANGE does

Nelson defines it as a transposition of contiguous regions within the document's linear byte stream:

> "Rearrange transposes two regions of text. With three cuts, the two regions are from cut 1 to cut 2, and from cut 2 to cut 3... With four cuts, the regions are from cut 1 to cut 2, and from cut 3 to cut 4." (4/67)

This is purely an ordering change. The operation cuts the V-stream at boundaries and swaps the resulting regions — it reorders bytes that are already in the document.

## Why "new depth" doesn't apply

A document's V-stream is a **flat, dense ordinal sequence** — byte positions 1, 2, 3, ... with no nesting or levels:

> "The digit after the one indicates the byte position in the current ordering of bytes. This is its virtual stream address." (4/30)

> "Logical addressing of the byte stream is in the form of virtual spans, or vspans. These are sequences of bytes in the document's virtual byte stream, regardless of their native origin." (4/11)

Because the V-stream has no internal depth structure to begin with, there is no "new depth" for content to be moved into. Rearrangement only changes *order* within that single linear level.

The notion of "depth" Nelson uses applies to the **tumbler line / docuverse tree**, where a span "may be visualized as a zone hanging down from the tumbler line — what is called in computer parlance a depth-first spanning tree" (4/25). But that depth describes the docuverse hierarchy (server → account → document → element), not positions *within* a document's byte arrangement. REARRANGE operates inside one document's V-stream, where content sits at a single element level.

## The invariant this preserves

Reordering is safe precisely because identity (I-addresses) is untouched while arrangement (V-positions) changes:

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." (4/30)

So REARRANGE permutes the existing V-positions of content the document already contains; it changes which ordinal positions bytes occupy, not their structural level, and it does not introduce, remove, or re-nest content.

(Note: Nelson never uses the word "depth" in the context of within-document rearrangement, so the framing of "relocate into V-positions at a new depth" has no counterpart in his specification — the V-stream is structurally flat.)
