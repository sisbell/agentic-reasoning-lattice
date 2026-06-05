## Question 7 [theory]

> When a requested span extends beyond where the document's content ends, what must the system guarantee about the portion of the span that has no corresponding content?

Let me verify the span semantics against the original pages covering spans.

**File:** `resources/literary-machines/raw/page-191.txt`

The curated sources already contain verified quotes from 4/24-4/25. Let me check the relevant page image to confirm there's nothing specific to the "beyond content end" case.

Based on the curated, verified sources, here is my answer.

## Answer

The system must guarantee that the contentless portion of the span is **simply empty** — it yields nothing, it is not an error, and it remains a valid, addressable region. This follows directly from the most fundamental property of a Xanadu span: **a span is defined by its boundaries, not by a count of content.**

### Why: a span is "from here to there," not "this much"

Nelson is emphatic that a span does not promise any quantity of content:

> "A tumbler-span is not a conventional number, and it does not designate the number of bytes contained. It does not designate a number of anything." (4/24)

Because the span carries no count, there is nothing to "fall short." What the span returns is whatever content actually occupies the range — and the range's contents are **implicit in the endpoints**, not enumerated:

> "The first point of a span may designate a server, an account, a document or an element; so may the last point. There is no choice as to what lies between; this is implicit in the choice of first and last point." (4/25)

So if part of the requested span lies past where content ends, that part is determined to contain nothing — and that determination is correct and complete, not a failure.

### Empty is a first-class, valid state

The most direct statement that an empty span region is legitimate (and impermanent):

> "A span that contains nothing today may at a later time contain a million documents." (4/25)

This is the core guarantee about the contentless portion: it is **valid now and remains addressable later**. The system does not reject the request, does not pad the gap, and does not invalidate the address. The empty region is just an unoccupied part of the address space — consistent with how addressing works generally in Xanadu, where addresses exist independently of stored content (the "ghost elements" principle: "Only actual content needs storage; the address space itself costs nothing").

### How retrieval behaves

The retrieval operation reflects this — it returns the material that is actually there, determined by the request:

> "RETRIEVEV ... This returns the material (text and links) determined by <spec set>." (4/67)

It returns the *material determined by* the span — i.e., the content that genuinely exists within the boundaries. The contentless tail contributes nothing to the result.

### Summary of the guarantee

1. The span is honored by its endpoints; the empty portion is not an error.
2. The system returns only the content that actually exists in the range; the empty portion yields nothing (no padding, no failure).
3. The empty portion remains a permanent, valid address — it may be occupied by content in the future without the span reference ever becoming invalid.

---

NEED_RAW: 4/67 — The curated `operations.md` confirms RETRIEVEV returns "the material determined by <spec set>," but the exact behavior of RETRIEVEV when a span *partially* exceeds existing content (truncation vs. partial return vs. silent omission) is not spelled out verbatim in the curated sources. My claim that retrieval silently returns only existing content is inferred from the span semantics (4/24-4/25) plus the RETRIEVEV definition (4/67), not from an explicit statement about the over-extending case. Pages 4/61-4/67 (raw 228-234) would confirm whether Nelson specifies retrieval edge behavior directly.
