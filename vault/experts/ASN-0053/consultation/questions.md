# Sub-Questions — Span Operations

**Inquiry:** What properties do contiguous regions of the tumbler space have? How do spans cover, intersect, split, and compose?

1. [nelson] If two regions of content partially overlap, must the system always be able to identify the exact sub-region they share in common?
2. [nelson] When a contiguous region is divided at a chosen point, must the two resulting pieces together account for exactly the original region with nothing lost and nothing duplicated?
3. [nelson] If two adjacent regions share a boundary, must the system guarantee they can be merged into a single contiguous region, and must that merged region be identical to one that was specified directly?
4. [nelson] Can every collection of content positions be expressed as a finite set of contiguous regions, and must there be exactly one minimal such expression?
5. [nelson] When one region completely contains another, must the system be able to express the remainder — the containing region with the contained region removed — as contiguous pieces?
6. [nelson] If a set of contiguous regions collectively covers a larger contiguous region without gaps, must the system guarantee that this complete-coverage property is verifiable?
7. [nelson] Must two regions that share no positions in common be guaranteed to produce an empty result when intersected, and must this emptiness be distinguishable from a region of zero width?
8. [nelson] When multiple overlapping regions are combined, must the result be independent of the order in which they are combined — that is, must region combination be associative and commutative?
9. [gregory] When two spans are adjacent in tumbler space (the end of one equals the start of the next), under what conditions can they be merged into a single span, and when does the exponent difference between their width tumblers prevent merging?
10. [gregory] Is the intersection of two overlapping tumbler spans always representable as a single span, or can hierarchical boundary crossings produce a result that requires multiple spans?
11. [gregory] Given that tumblers use `.0.` as a hierarchical separator by convention but not enforcement, does a span starting at `1.1` with width `0.5` cover position `1.3.0.1` — i.e., do spans enumerate all tumblers within the range regardless of hierarchical depth?
12. [gregory] When `strongsub` returns its input unchanged due to the exponent guard, what does that imply about the algebraic closure of span difference — can subtracting one span's width from another's start position fail to produce a meaningful displacement?
13. [gregory] Is there a canonical representation for a given region of tumbler space, or can the same set of positions be described by spans with different (start, width) pairs using different exponent encodings?
14. [gregory] How does `tumblerlength` (significant digits: `nstories(t) - t.exp`) interact with span width — does a width tumbler with more significant digits subdivide positions more finely than one with fewer, and what happens when a span's width has a different `tumblerlength` than its start?
15. [gregory] When splitting a span at an interior point, does the split always produce exactly two non-empty sub-spans whose widths sum to the original width, or can tumbler arithmetic rounding cause the parts to not reconstruct the whole?
16. [gregory] In SpecSet composition, what ordering invariant do the component VSpecs maintain — must they be non-overlapping, sorted by start position, or can a SpecSet contain redundant or overlapping spans?
17. [gregory] Does the tumbler total order guarantee that all positions within a span `[start, start+width)` form a contiguous interval under `tumblercmp`, or can the hierarchical digit structure create positions that compare as "inside" the range but are not logically part of the span?
