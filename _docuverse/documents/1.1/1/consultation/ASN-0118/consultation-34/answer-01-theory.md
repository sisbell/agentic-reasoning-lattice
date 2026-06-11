## Question 1 [theory]

> In Nelson's span design, is the width tumbler intended to carry the same structural shape (tumbler length) as the start tumbler, or is it merely a difference/offset whose shape is unconstrained — i.e., is level-uniformity part of what a span *is*, or an artifact of one formalization?

**Short answer: level-uniformity is not part of what a span is. But the width tumbler is not a shapeless offset either — its shape is meaningful, and what it mirrors is the *end* of the span, not the start.** A formalization that requires the width tumbler to have the same digit-structure as the start tumbler has restricted itself to what I explicitly called the degenerate case.

## What a span is, semantically (LM 4/24–4/25)

A span is two positions on the tumbler line delimiting a subtree — not a count, not a same-level interval:

> "A span in the tumbler line, represented by two tumblers, refers to a subtree of the entire docuverse, (or merely to a series of elements of the same type, which is a degenerate case of a subtree). Thus we may have spans of characters, spans of links, spans of documents, spans of versions, and spans covering large combinations of them--including spans of servers with all their contents." [LM 4/24]

Note the parenthesis: the level-uniform span — a flat run of same-type elements — is named as the **degenerate case** of the general concept. And the endpoints are explicitly permitted to sit at different levels of the hierarchy:

> "The first point of a span may designate a server, an account, a document or an element; so may the last point. There is no choice as to what lies between; this is implicit in the choice of first and last point." [LM 4/25]

> "A span may be visualized as a zone hanging down from the tumbler line--what is called in computer parlance a depth-first spanning tree." [LM 4/25]

So the *intent* is that a span is defined by its two boundary points, with the contents implied by tree order — and the boundary points carry no requirement of matching depth.

## What the width tumbler's shape actually encodes (LM 4/32–4/34)

The arithmetic pages (my reading of `resources/literary-machines/raw/page-199.png` through `page-201.png`; paraphrased, not curated quotes) define the difference tumbler this way:

- **Leading zeros** mark how many digit-fields the two addresses share — i.e., the level at which the span diverges from its start. Address tumblers begin with a nonzero digit; difference tumblers begin with zero (4/32).
- **The first nonzero field** is the arithmetic difference at the divergence level (4/33).
- **Everything after that is copied from the greater (end) tumbler** (4/33). Correspondingly, in tumbler addition, the width's tail *replaces* whatever followed in the start address — the start's trailing digits are discarded (4/34).

This settles the question structurally: below the divergence point, the width's shape is the **end address's shape**. The start tumbler's depth beneath the divergence point plays no role at all — it is thrown away during addition. The only coupling to the start is the leading-zero prefix, which must correspond to a level present in the start address (it identifies which field gets incremented). So the width is neither a clone of the start's shape nor an arbitrary blob: it is a structured object encoding (a) the divergence level and (b) the end point's tail.

The 4/33 worked example (`1.2.165.7 − 1.2.3.1 = 0.0.162.7`) happens to have operands of equal length, which I suspect is where the level-uniform intuition gets smuggled in. The rule itself never references the start's length.

## My own canonical widths are counterexamples

The one-positions (LM 4/38) are widths whose whole point is to be shallower than the addresses they combine with:

> "A digit of 'one' may be used to designate all of a given version, all versions of a given document, all works of a given author, all documents in a given project, all documents on a given server--or the entire docuverse." [LM 4/38]

A width like `0.0.0.1` applied to a deep document address jumps to the next sibling at that level, sweeping up the entire subtree in between — the span endpoints are at different depths by construction. And remember:

> "A tumbler-span is not a conventional number, and it does not designate the number of bytes contained. It does not designate a number of anything." [LM 4/24]

> "A span that contains nothing today may at a later time contain a million documents." [LM 4/25]

## Where level-uniformity legitimately appears

Two honest concessions. First, there is one real structural constraint: widths only reach forward — "Starting from a given tumbler address, it may only be possible arithmetically to get to some places in the Docuverse--those notationally after that address" [LM 4/25] — so "unconstrained offset" overstates it in the other direction. Second, in FEBE practice, "A request set is a set of spans, or spanset, presented to the back end... Actually it is a V-spanset" [LM 4/37], and document-local V-spans of bytes *are* typically the degenerate same-level case. An implementation that only ever handles vspans within a document (as the udanax-green lineage largely does) can therefore get away with a same-shape width and never notice the loss.

**Conclusion:** if your formalization makes the width tumbler structurally congruent with the start tumbler, you have formalized the degenerate case of 4/24, not the span concept. The defining properties of the width are its leading-zero divergence prefix and an end-derived tail; level-uniformity is an artifact.
