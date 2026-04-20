## Question 3 [nelson]

> If two adjacent pieces in a document both reference content from the same original, and that original content was itself contiguous, must those two pieces be merged into one?

# Must Adjacent Spans Be Merged?

**No.** Literary Machines does not require merging, nor does it address this question. It operates at a level below what I specified.

## The V-Stream Is Bytes, Not Spans

The document's virtual byte stream is defined at the **byte level**, not the span level. Each byte has a V-address and maps to an I-address:

> "Logical addressing of the byte stream is in the form of virtual spans, or vspans. These are sequences of bytes in the document's virtual byte stream, regardless of their native origin." [LM 4/11]

> "The digit after the one indicates the byte position in the current ordering of bytes. This is its virtual stream address." [LM 4/30]

The V-stream is a sequence of bytes. Spans are a **reference mechanism** — how you point at regions of that stream — not a storage format that the system must canonicalize.

## Spans Are for Pointing, Not for Mandating Internal Structure

Spans describe what you want to talk about:

> "A request set is a set of spans, or spanset, presented to the back end in the FEBE protocol... The manipulation of request sets is an important aspect of what front-end functions do." [LM 4/37]

Whether the enfilade machinery internally represents the V→I mapping as one merged span or two adjacent spans covering contiguous I-space is an implementation concern. The user sees an identical byte stream either way. RETRIEVEV returns the same bytes. FINDDOCSCONTAINING returns the same origin document. SHOWRELATIONOF2VERSIONS returns the same correspondence.

## The Enfilade Handles This

The internal representation is the province of the enfilade structures, which maintain "canonical order" as an internal mandate:

> "All changes, once made, left the file remaining in canonical order, which was an internal mandate of the system." [LM 1/34]

But "canonical order" here refers to the enfilade data structure remaining valid after mutations — not to a requirement that adjacent spans be merged. Whether the POOM enfilade (which maps V→I) coalesces adjacent entries pointing to contiguous I-space is an optimization choice, not a semantic requirement.

## Why It Doesn't Matter Semantically

Consider: you COPY bytes from I-space 100–105 into your document at V-position 5, then separately COPY bytes from I-space 106–110 at V-position 11. Two editorial acts producing adjacent V-space content referencing contiguous I-space.

Every user-visible operation produces identical results regardless of internal span count:

| Operation | One span (100–110) | Two spans (100–105, 106–110) |
|-----------|---------------------|-------------------------------|
| RETRIEVEV | Same bytes | Same bytes |
| FINDDOCSCONTAINING | Same origin | Same origin |
| SHOWRELATIONOF2VERSIONS | Same correspondence | Same correspondence |
| Link survivability | Same I-addresses | Same I-addresses |

The V-stream is what users see. How the system represents the V→I mapping internally is invisible to them.

## Summary

I designed Xanadu at the level of **what the system does** — permanent addresses, surviving links, traceable origins, version comparison. The question of whether adjacent references to contiguous I-space must be represented as one span or may remain as two is an **implementation optimization** below my specification. The enfilade machinery handles it. The user never knows the difference.
