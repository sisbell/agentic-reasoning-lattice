## Question 1 [theory]

> In the design, may a retraction's from-set legitimately carry the link's own home document as a derivation source, or is the from-set strictly reserved for content the link derives *from* — making any home-span fill a non-derivation placeholder?

## Short answer

Yes — a retraction's from-set may legitimately carry the link's own home document. Nothing in the design reserves the from-set as a "derivation source," so a home-span there is not a placeholder; it is a meaningful designation of where the retraction issues from.

## Why the "derivation-only" premise doesn't hold in Nelson's design

The question imports an assumption — that from-set ≡ "content the link derives *from*" — that Nelson's design explicitly declines to make. He defines directionality but leaves the *meaning* of the two ends to the case:

> "A link is typically directional. Thus it has a from-set, the bytes the link is 'from,' and a to-set, the bytes the link is 'to.' (What 'from' and 'to' mean depend on the specific case.)" (4/42)

So "from" is not a fixed semantic role like "derivation source." It is whatever the link type makes it.

Nelson goes further with **one-sided links**, where the first endset (the "from-set") is used purely to *designate matter pointed at*, not to express derivation at all — and he flags the terminology as a misnomer precisely because of this:

> "since it has only one side, we use the first endset to designate the matter pointed at. To call this 'from' is inane." (4/48)

That confirms the from-set is a positional slot, not a reserved derivation channel.

## Endsets may point anywhere, including the home document

There is no exclusion of the home document from any endset. Endsets are arbitrary span-sets reaching anywhere:

> "The from-set may be an arbitrary collection of spans, pointing anywhere in the docuverse." (4/43)

And home/application are explicitly independent — a link can both reside in *and* point into the same document:

> "A link need not point anywhere in its home document. Its home document indicates who owns it, and not what it points to. Conversely, links connecting parts of a document need not reside in that document." (4/12)

So a from-set span that lands on the link's own home document is structurally ordinary, not anomalous.

## The metalink analogy supports it

The closest authored pattern is the metalink, where the *marker inside the document* is the from end and the whole target is the to end:

> "the 'author' and 'title' links will normally go from the author's name and the principal appearance of the title to the whole document." (4/52)

By the same shape, a retraction reads naturally as: **from** = the retracting statement (which lives in the home document) → **to** = the retracted content. Here the home-span in the from-set *is* the substance of the link, not a filler.

## Caveat on "retraction"

NEED_RAW: 4/52-4/55 — Nelson specifies a **Document Supersession Link** (a metalink declaring one document replaces another) but the curated sources contain no "retraction" link type by that name. The reasoning above applies Nelson's general from/to principles (4/12, 4/42, 4/43, 4/48) and the metalink pattern (4/52) by analogy; if "retraction" is a project-local link type with its own convention, that convention is an implementation choice layered on top of — not derived from — Nelson's design, which itself imposes no derivation-only meaning on the from-set.
