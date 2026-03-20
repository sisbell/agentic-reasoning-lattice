## Question 6 [nelson]

> Does the design require that the pieces of a document's arrangement follow the same order as the document's positions, with no piece's domain preceding another's yet following it in the content sequence?

No. The design explicitly allows the I-space origins of a document's V-stream spans to appear in any order relative to each other. This is the entire point of separating V-space from I-space.

## Evidence

**The REARRANGE operation produces out-of-order mappings by design:**

> "Rearrange transposes two regions of text. With three cuts, the two regions are from cut 1 to cut 2, and from cut 2 to cut 3." [LM 4/67]

After a REARRANGE, the V-stream's constituent I-space spans are no longer in I-space order. Content that was created later (higher I-addresses) now precedes content created earlier (lower I-addresses) in the V-stream.

**V-space order is independent of I-space order by architecture:**

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." [LM 4/30]

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing." [LM 4/11]

**COPY (transclusion) introduces I-space content from arbitrary locations:**

> "The virtual byte stream of a document may include bytes from any other document." [LM 4/10]

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document." [LM 4/11]

After a COPY, the V-stream contains I-space spans from entirely different documents — their I-addresses bear no ordering relationship to the native content whatsoever.

## What IS required

The V-stream itself must be dense and contiguous — V-addresses form a sequential numbering from 1 with no gaps. But the I-space spans underlying that sequence can appear in any I-space order. This is not a deficiency; it is the fundamental design principle:

> "Virtually all of computerdom is built around the destructive replacement of successive whole copies of each current version... A document is really an evolving ONGOING BRAID." [LM 2/14]

The "braid" metaphor is apt: strands (I-space content) are woven into arrangements (V-space orderings) that need not follow the chronological order of their creation or their permanent storage addresses.
