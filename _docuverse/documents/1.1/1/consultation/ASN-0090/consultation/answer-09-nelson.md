## Question 9 [nelson]

> Can a removal be partial — removing content from the middle of a single stored unit — or must removal always operate on whole units as they were originally contributed?

## Removal Is Partial — Down to the Individual Byte

Removal operates on **arbitrary V-spans**, not on "units as originally contributed." There is no concept of a "stored unit" that must be removed whole. The granularity is the individual byte.

### The Operation

DELETEVSPAN takes a span argument — any contiguous range of positions in the document's virtual byte stream:

> "This removes the given span from the given document." [LM 4/66]

The span can be as small as one byte or as large as the entire document. It bears no relation to how the content was originally inserted.

### Why This Works

The Istream/Vstream separation makes this clean. Content lives permanently at I-addresses; the document's arrangement is a V-to-I mapping. DELETE modifies the mapping, not the content:

> "Logical addressing of the byte stream is in the form of virtual spans, or vspans. These are sequences of bytes in the document's virtual byte stream, regardless of their native origin." [LM 4/11]

"Regardless of their native origin" is the key phrase. A V-span can cross boundaries between different insertions, between native and transcluded content, between content from different sources. The Vstream doesn't know or care about contribution boundaries.

### What Happens to the Removed Bytes

They remain in Istream. The diagram on 4/9 shows:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

And explicitly:

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

### Concrete Example

If you INSERT "Hello World" (11 bytes), those 11 bytes get 11 I-addresses and 11 V-addresses (say, positions 1–11). You can then DELETEVSPAN on positions 6–6 (just the space), or 6–10 ("World"), or 4–8 ("lo Wo") — any contiguous range. The deleted bytes vanish from the current arrangement but remain permanently in Istream, recoverable through historical backtrack or still visible in other versions and transclusions.

Similarly, REARRANGE operates on arbitrary regions defined by cut points, not by original contribution boundaries:

> "Rearrange transposes two regions of text. With three cuts, the two regions are from cut 1 to cut 2, and from cut 2 to cut 3." [LM 4/67]

### Summary

All editing operations — INSERT, DELETEVSPAN, REARRANGE, COPY — work at **byte-level granularity** on the **Vstream**. There is no notion of an indivisible "contribution unit." The system treats the document as a stream of individually addressable bytes that can be sliced at any point.
