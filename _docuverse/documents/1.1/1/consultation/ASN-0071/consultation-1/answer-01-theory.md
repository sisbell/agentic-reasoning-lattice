## Question 1 [theory]

> Was FINDDOCSCONTAINING intended to discover documents by their content-subspace references only, or to range over any V-position references including link-subspace ones?

Looking at the curated sources for FINDDOCSCONTAINING, I want to verify by reading the actual page.

[Reading raw page 237 (4/70) to verify the operation definition]

Based on the curated sources, here is my answer:

# FINDDOCSCONTAINING — Design Intent

**It was intended for content-subspace discovery — the dual of transclusion (COPY), not a general V-position lookup.**

The operation takes a `<vspec set>` and returns documents that have *included* that material via transclusion. The two quotes from Literary Machines make the intent unmistakable:

> "This returns a list of all documents containing any portion of the material included by `<vspec set>`." — 4/70

> "This returns a list of all documents containing any of the material specified by the span addresses, regardless of where the native copies are located." — 4/63

The phrase **"regardless of where the native copies are located"** is decisive. The terms "native" and "non-native" belong to the content/byte model:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." — 4/11

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." — 4/11

So FINDDOCSCONTAINING answers the inverse of transclusion: *"who has windowed to this content?"* That is fundamentally a byte/content-subspace question.

## Why the link-subspace case is degenerate

Links don't transclude. A link has exactly one home document, encoded in its tumbler address:

> "The links designated by a tumbler address are in their permanent order of arrival. **A document includes only the links of which it is the home document.**" — 4/31

> "A link need not point anywhere in its home document. **Its home document indicates who owns it, and not what it points to.**" — 4/12

If you handed a link's V-address (a `0.2.N` address) to FINDDOCSCONTAINING, the question collapses: a link is contained by exactly one document, and that document's identity is structurally derivable from the link's address itself. There is no transclusion graph to walk, no "where are the copies" question to answer.

## What I intended

The COPY/FINDDOCSCONTAINING pair was designed around **byte-level inclusion**. COPY creates non-native byte-spans (windows, virtual copies) at new V-positions; FINDDOCSCONTAINING walks that inclusion graph backward to find every document that windows the specified bytes. The whole point — *"regardless of where the native copies are located"* — is that you've decoupled the content's Istream origin from its many Vstream appearances, and you want to recover all those appearances.

Link-subspace addresses are technically well-formed V-positions, but they aren't *included*; they're owned. Asking FINDDOCSCONTAINING about a link address is a category mistake — answerable trivially by inspecting the address.

## NEED_RAW

NEED_RAW: 4/63, 4/70 — to confirm whether the surrounding prose explicitly excludes link-subspace addresses or merely assumes the byte/transclusion reading by context. The curated extracts strongly imply content-subspace intent, but the actual page text would settle whether this was an explicit specification choice or an implicit convention.
