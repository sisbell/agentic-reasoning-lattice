## Question 8 [theory]

> When content appears in multiple documents through sharing, must each containing document be reported independently and identifiably?

# Answer

**Yes — absolutely.** When content appears in multiple documents through sharing (transclusion/windowing), each containing document must be reported as a distinct, identifiable entity. This is not merely a convenience; it is a structural requirement of the system.

## The Operational Guarantee

The FINDDOCSCONTAINING operation explicitly returns a *list of identifiable documents*:

> "FINDDOCSCONTAINING: This returns a list of all documents containing any portion of the material included by <vspec set>." [LM 4/70]

> "This returns a list of all documents containing any of the material specified by the span addresses, regardless of where the native copies are located." [LM 4/63]

A "list of documents" means each document is identified by its tumbler address — not bundled, not anonymized, not summarized. You get a discrete enumeration where each entry can be inspected, navigated to, and queried independently.

## Why This Is Required

Three principles force independent identification:

**1. Ownership.** Each containing document has its own owner who has rights and obligations:

> "Each compound document is like the other documents: it has an owner and receives royalties."

If a passage from my work appears in twenty different compound documents, the system must know which is which — because royalties split between original owner and each quoter must be calculated separately.

**2. Attribution traceability.** I built the system so that:

> "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

This works in both directions. From content, you trace to its home document. From a piece of content, you can also find every document that windows to it — and each must be identifiable to make that meaningful.

**3. Bidirectional discovery.** The reader must be able to ask: "What documents window to this one?" — and receive discrete answers:

> "However, it must also be possible for the reader to ask to see whatever documents window to the current document. Both are available at any time."

A reader cannot navigate to "some document somewhere" — they must be able to step into *that* document, *that* author's work, *that* compound presentation.

## What This Forbids

Implementations may NOT:
- Return shared content as a single combined report
- Anonymize which documents contain the material
- Deduplicate documents that happen to transclude overlapping spans
- Conflate multiple containing documents into a summary count

Each containing document is a first-class entity in the docuverse with its own tumbler address, owner, royalty stream, and identity. To collapse them would destroy attribution, break royalty accounting, and violate the bidirectional discovery guarantee.
