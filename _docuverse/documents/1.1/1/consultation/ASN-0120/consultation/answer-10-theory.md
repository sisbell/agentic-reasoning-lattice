## Question 10 [theory]

> May a single link tie together endsets drawn from more than one document at once, and what must the system guarantee about each endset being faithfully recorded as a distinct region of content?

# A Single Link May Span Many Documents

Yes. This is not merely permitted but is a core design intent. A Xanadu link connects **endsets**, and each endset is an arbitrary collection of spans that may point anywhere in the docuverse—across as many documents as the connection requires.

## The Endset Is a Set, Not a Point

The fundamental generalization is from point-to-point linking to set-to-set linking. One end of a single link can touch bytes scattered across multiple documents:

> "We see from above that one end of a link may be on a broken, discontiguous set of bytes. This illustrates the endset: a link may be to or from an arbitrary set of bytes. These may be anywhere in the docuverse." [LM 4/42]

All three endsets share this property:

> "The from-set may be an arbitrary collection of spans, pointing anywhere in the docuverse. Similarly, the to-set may be an arbitrary collection of spans pointing anywhere in the docuverse. We adopt the same convention for link types." [LM 4/43]

So a single critique-link can hold three separate passages in three separate documents at one end—because the connected idea spans those several spots.

## What Must Be Guaranteed About Each Region

The endset machinery rests on the **universal tumbler address space**, and each span within an endset maps to its own distinct position there:

> "There is a universal address space, the tumbler line... We may visualize a link's endsets as mapping to it." [LM 4/45]

> "ENDSETS MAY POINT TO SPANS ANYWHERE IN THE DOCUVERSE" [LM 4/45, diagram caption]

Two guarantees follow from this faithful, address-based recording of each region:

**1. Each region is a distinct, traceable span.** Because a link "is not between points, but between spans of data" [LM 4/42], every region in an endset is recorded as a span of bytes with its own boundaries, mapping to its own place on the tumbler line. The home document of any byte remains ascertainable—origin traceability is structural, encoded in the I-address of each span, not stripped metadata.

**2. Each region survives editing independently.** Because the link attaches to bytes rather than positions, each distinct region persists as long as any of its bytes remain:

> "This has a crucial advantage: it means that links can survive editing. If any of the bytes are left to which a link is attached, the link remains on them. This also works for alternative versions in which part of each end has survived." [LM 4/42]

The diagram annotation on page 4/43 makes the survivability scope explicit:

> "SURVIVABILITY: Links between bytes can survive deletions, insertions and rearrangements, if anything is left at each end." [LM 4/43]

## Summary

A single link may bind content drawn from arbitrarily many documents at once—on any of its three endsets. The system's obligations for each constituent region are: record it as a distinct span of bytes mapped to its own permanent position on the universal tumbler line, preserve the traceability of its home document, and keep it attached to those bytes through editing so long as any of them survive.

I confirmed each quote against the curated endsets and links sources; all are verified at the cited pages.
