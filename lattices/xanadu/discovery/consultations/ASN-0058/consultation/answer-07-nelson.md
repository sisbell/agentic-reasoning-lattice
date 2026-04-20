## Question 7 [nelson]

> Within a single contiguous mapping unit, must the document order of characters match the original creation order, or can a mapping unit represent a reversal or other reordering?

## Within a Mapping Unit, Document Order Must Match Creation Order

A single contiguous mapping unit (span) **cannot represent a reversal or reordering**. Order-preservation is inherent in the span model.

### Why: Spans Are Defined by Endpoints on the Tumbler Line

A span is "represented by two tumblers" and "refers to a subtree of the entire docuverse" [LM 4/24]. The content within a span follows tumbler-line ordering by definition — there is no direction flag, no reversal marker, no internal permutation. A span says "from here to there," and the ordering between those endpoints is fixed by the tumbler line itself.

> "The first point of a span may designate a server, an account, a document or an element; so may the last point. There is no choice as to what lies between; this is implicit in the choice of first and last point." [LM 4/25]

"No choice as to what lies between" is the critical constraint. The internal ordering of a span is determined by the tumbler line, not by the mapping. A V-span mapped to an I-span inherits the I-span's tumbler ordering.

### The V→I Mapping Preserves Order Within Each Unit

The Vstream is a dense sequence of positions. The POOM enfilade maps V-positions to I-positions. Each mapping entry covers a contiguous run where V-position *k* maps to I-position *k* (offset by the span's starting addresses). This is why spans are efficient: you store only start-V, start-I, and length.

Nelson's description of V-stream addressing confirms this structure:

> "The digit after the one indicates the byte position in the current ordering of bytes. This is its virtual stream address." [LM 4/30]

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." [LM 4/30]

The V-order *across* mapping units can differ from I-order — that is the entire point of the V/I separation. But *within* a single unit, the correspondence is positional (first-to-first, second-to-second, etc.).

### No Operation Creates Reversed Mappings

None of Nelson's 17 FEBE commands produces a reversed span:

- **REARRANGE** "transposes two regions of text" [LM 4/67] — it swaps blocks but preserves internal order within each block.
- **INSERT** adds new content at a V-position — new I-bytes are appended chronologically.
- **COPY** (transclusion) maps a V-range to an existing I-range — same order.
- **DELETE** removes a V-range — no reordering involved.

There is no REVERSE operation. To achieve the effect of reversing "ABC" to "CBA," you would either:
1. **INSERT** new native bytes "CBA" (creating fresh I-stream content in the desired order), or
2. Create **three separate mapping units**, one per character, arranged in reverse V-order — each unit is order-preserving, but they appear in reversed sequence in the V-stream.

### Summary

The span is the atomic mapping unit. It maps a contiguous V-range to a contiguous I-range with identical internal ordering. Reordering is expressed by the *sequence of spans*, not by reversal within any single span. This is structural, not merely conventional — it follows from the definition of a span as a pair of tumbler-line endpoints with "no choice as to what lies between."

NEED_RAW: 4/32-4/39 — The detailed span mechanics pages may contain additional precision about the V→I mapping representation that the curated sources summarize but don't fully reproduce.
