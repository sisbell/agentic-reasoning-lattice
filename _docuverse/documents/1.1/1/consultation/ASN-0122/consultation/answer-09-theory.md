## Question 9 [theory]

> If either document is rearranged after content is shared between them, what must remain stable about the correspondence the system reports before and after that rearrangement?

## The invariant: corresponding content is paired by identity, not by position

When two documents share content (through `COPY`/inclusion they come to share the same Istream addresses) and one of them is then rearranged, **what must remain stable is the identity-level pairing the correspondence expresses — the same bytes must still be reported as corresponding to the same bytes.** What is *allowed* (indeed required) to change is the surface of the report: the Vstream coordinates of the spans, because rearrangement moves where that shared content sits in the document's arrangement.

I designed correspondence this way on purpose. Correspondence is not positional metadata that I store alongside the text — it is a structural fact that falls out of shared Istream origin. Two spans correspond because they have the same home in Istream. Rearrangement (`REARRANGE`, or any insertion/deletion that shifts positions) is a *pure Vstream operation*: it re-orders the arrangement but never touches the Istream content or its permanent addresses. So the relation cannot be disturbed by it. No corresponding pair may appear or vanish merely because the order changed; the membership of the correspondence is conserved, and only its V-coordinates are re-resolved to the new arrangement.

This is the same principle that makes links survive editing — and it is the same principle for exactly the same reason:

> "A Xanadu link is not between points, but between spans of data... This has a crucial advantage: it means that links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them. **This also works for alternative versions in which part of each end has survived.**" [LM 4/42]

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, **any links to those bytes remain stably attached to them.**" [LM 4/30]

Because the attachment is to the bytes (Istream identity), reordering the bytes in Vstream re-addresses them but does not re-identify them. The byte that the front end never even sees a stable native address for —

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing... Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document." [LM 4/11]

— is nonetheless the *same byte*, and therefore the same corresponding element.

## What the report itself looks like, and what changes in it

`SHOWRELATIONOF2VERSIONS` is the operation that reports correspondence:

> "This returns a list of ordered pairs of the spans of the two spec-sets that correspond." [LM 4/70]

So the report is a set of ordered (span-in-A, span-in-B) pairs. After a rearrangement:

- **Stable:** the *content* each pair identifies on each side — the shared Istream bytes — and therefore which content corresponds to which. The relation reported is the same relation.
- **Re-expressed:** the Vstream span addresses on the rearranged side, recomputed against the new ordering.
- **May change form:** if a rearrangement splits a region that was previously one contiguous shared run, a single corresponding span may now have to be reported as a *span-set* (several spans) — the discontiguous case I built endsets and spans to handle — but the underlying content it names is unchanged.

The whole point of holding versions, and of correspondence, is intercomparison:

> "Of course, a facility that holds multiple versions of the same material, and allows historical backtrack, is not terribly useful unless it can help you intercompare them in detail — unless it can show you, word for word, what parts of two versions are the same." [LM 2/20]

If rearrangement could perturb *which* parts the system calls "the same," that guarantee would be hollow. It cannot, because "the same" is decided by shared Istream origin, which rearrangement does not reach. This is also why a link aimed at one arrangement still lands in the corresponding place in another:

> "Links may be refractively followed from a point or span in one version to corresponding places in any other version. Thus a link to one version of a Prismatic Document is a link to all versions." [LM 2/26]

## In one line

The Vstream coordinates in the correspondence report move with the rearrangement; the content-identity they encode — grounded in immutable shared Istream addresses — must not. The system must report the *same shared bytes as corresponding to the same shared bytes* before and after, re-addressed but never re-paired.

(The curated sources cover this fully; no raw-page consultation was needed.)
