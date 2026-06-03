## Question 1 [theory]

> Was SHOWDELETIONS intended to compare content at I-address-set granularity (cross-document presence/absence), or to detect per-occurrence removal when an I-address occupies multiple V-positions within one document?

SHOWDELETIONS does not appear anywhere in my specification of Xanadu in *Literary Machines*. The FEBE protocol of XU.87.1 had exactly 17 commands, and the deletion- and comparison-related operations among them were `DELETEVSPAN` (removing a span from a document's Vstream) and `SHOWRELATIONOF2VERSIONS` (intercomparison). There is no command named SHOWDELETIONS in the curated, verified material.

So I must be precise about authority here: **I cannot tell you what SHOWDELETIONS was "intended" to do at either granularity, because I never specified such an operation.** If it exists in an implementation, it is an implementation invention, not a guarantee from the book. Treat any claim about its intent as derived from the implementation, not from me.

NEED_RAW: 4/61-4/70 — to confirm exhaustively that no command named SHOWDELETIONS appears in the FEBE listing (the curated operations summary covers 16 of the 17 commands and does not include it, but I cannot verify the full verbatim command table from the curated sources alone).

That said, I can speak to the underlying design principles your two interpretations turn on, because those *are* in the book.

**1. What deletion actually means.** Deletion is a Vstream operation, never an Istream one:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" (4/9)

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." (4/11)

So "deletion" is always relative to a particular document's arrangement. The same I-address content can be present (addressable) in one document and deleted (not addressable) in another.

**2. The cross-document / cross-version question is already served by existing operations.** Detecting presence/absence of shared I-address content across documents or versions is exactly what `FINDDOCSCONTAINING` and `SHOWRELATIONOF2VERSIONS` do:

> "This returns a list of all documents containing any portion of the material included by <vspec set>." (4/70, FINDDOCSCONTAINING)

> "This returns a list of ordered pairs of the spans of the two spec-sets that correspond." (4/70, SHOWRELATIONOF2VERSIONS)

Correspondence is computed structurally from shared I-addresses, not from metadata.

**3. The per-occurrence case is the genuinely interesting one — and it exposes a real ambiguity.** Your second interpretation hinges on whether a single I-address can occupy *multiple* V-positions within one document. It can: `COPY` (transclusion) maps existing Istream content into a document's Vstream as a reference, and nothing prevents the same Istream span from being mapped at several V-positions.

> "The material determined by <spec set> is copied to the document determined by <doc id> at the address determined by <doc vsa>." (4/67, COPY)

This matters because **I-address-set granularity is lossy with respect to occurrences.** Set membership ("is this I-address present?") cannot distinguish "this content appears 3 times and one occurrence was removed" from "it still appears." Per-occurrence removal detection is fundamentally a Vstream-position question, not an I-address-set question. My addressing model keeps these separate by design: links and correspondence attach to *bytes* (I-addresses) precisely so they survive editing —

> "A Xanadu link is not between points, but between spans of data... it means that links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them." (4/42)

— but that survivability guarantee is *agnostic to how many V-positions* an I-address occupies. The book's machinery, in other words, is built around I-address-set semantics for survivability and correspondence. Per-occurrence removal is not something I gave an operation for.

**Bottom line.** Nothing I wrote specifies SHOWDELETIONS, so neither granularity can claim my authority. But the grain of my design points toward the *first* interpretation: the verified operations all work at I-address / shared-origin granularity (presence, absence, correspondence). Per-occurrence removal within a single document — distinguishing which of several V-positions holding the same I-address went away — is a Vstream-position concern that my specified operations do not address, and any implementation doing it is going beyond what the book guarantees.
