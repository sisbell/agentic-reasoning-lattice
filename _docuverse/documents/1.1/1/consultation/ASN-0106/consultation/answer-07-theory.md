## Question 7 [theory]

> What does the combined reading reveal about adjacency — whether two fragments sit directly together in the document or are separated by unrequested content?

## Adjacency is carried by the addresses, not by the bytes

The short answer: **the combined byte content alone does not reveal adjacency — the span boundaries do.** Whether two fragments sit directly together or are separated by unrequested material is determined by their tumbler/V-stream addresses, because Vstream is a dense, contiguous address space.

### Why the bytes alone are silent

When you retrieve content, `RETRIEVEV` "returns the material (text and links) determined by `<spec set>`" (operations, 4/67). If two requested fragments are simply delivered one after another, the raw stream of bytes looks the same whether the fragments were neighbors or were drawn from opposite ends of the document. The content carries no inherent marker of the gap between them.

### Why the addresses are not silent

Adjacency becomes determinable because of how the addressing works:

1. **A single span is inherently gap-free.** Everything between its two endpoints is included, by definition:
   > "The first point of a span may designate a server, an account, a document or an element; so may the last point. There is no choice as to what lies between; this is implicit in the choice of first and last point." (spans, 4/25)

   So if two fragments fall inside one span, they are adjacent *with all the intervening content present* — there is no hidden gap.

2. **A span-set is the explicit signal of separation.** To pull out fragments *without* the material between them, you must use a span-set:
   > "if you want to designate a separated series of items exactly, including nothing else, you do this by a span-set, which is a series of spans." (spans, 4/25)

   The very choice of a span-set over a single span announces that the fragments are *not* contiguous — the omitted ranges between the spans are precisely the unrequested content.

3. **Vstream is dense, so the boundary arithmetic is exact.** V-addresses "form a contiguous sequence starting at 1" with "no gaps" (v-space-addresses, summarizing 4/11, 4/30). Logical addressing is "in the form of virtual spans, or vspans... sequences of bytes in the document's virtual byte stream" (4/11). Because the V-stream has no holes, two fragments are directly adjacent **if and only if** the end of one span immediately precedes the start of the next (e.g., a span ending at V-position 50 followed by a span beginning at V-position 51). Any larger jump between the end of one span and the start of the next is, by construction, unrequested content sitting between them.

### What this means in practice

- The front end already knows the spec-set it sent, so it can compare span endpoints and reconstruct exactly which fragments abut and which are separated — and by how much.
- "Combined reading" therefore reveals adjacency only when the addressing structure travels with it. The juxtaposed text shows fragment A then fragment B; the *span boundaries* tell you whether B genuinely followed A or whether a stretch of document was skipped.

### One caveat worth flagging

The curated description of `RETRIEVEV` says only that it "returns the material (text and links)" (4/67); it does not explicitly state whether the returned result re-tags each fragment with its originating span boundaries or returns a flat concatenation. The adjacency information is fully recoverable from the *requested* spec-set regardless, but if you want confirmation of how the returned structure itself is shaped (per-span vs. flattened), that detail isn't pinned down in the curated sources.

NEED_RAW: 4/67 (RETRIEVEV return structure), 4/24–4/25 (span/span-set delivery semantics)
