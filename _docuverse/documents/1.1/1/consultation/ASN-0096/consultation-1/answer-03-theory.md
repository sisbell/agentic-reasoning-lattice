## Question 3 [theory]

> Was projection designed as a single operation over endsets, or as distinct operations over endsets, spans, and individual I-addresses with different cardinality semantics?

Looking through the curated sources, I find no definition of "projection" as a named operation in Literary Machines. Let me verify against the raw pages covering endsets, links, and FEBE operations before answering.

[Note: User asked length limits be ≤25 words between tool calls.]

Let me check the relevant pages.

[I should read several pages to verify whether "projection" appears as a defined operation.]

Let me check the FEBE operations pages and the endset/link pages.

Based on my review of the curated sources, I need to flag this clearly:

**NEED_RAW: 4/41-4/60 (pages 208-227), 4/61-4/79 (pages 228-246)** — to verify "projection" as a term

## What I Can Say From the Verified Sources

**The term "projection" does not appear in any of the curated extracts I have for Literary Machines.** The curated sources cover endsets, links, spans, tumblers, FEBE operations, and the I-space/V-space distinction in detail, and none of them define an operation called "projection."

What the curated sources DO describe:

### Endsets are unified, but addressing primitives are distinct

An endset is "an arbitrary set of bytes...anywhere in the docuverse" [LM 4/42]. The three endsets of a link (from-set, to-set, type) are "symmetrical" — they follow the same convention [LM 4/44]. Endsets are constructed from spans, and spans are pairs of tumbler addresses.

This gives three distinct levels:

| Level | Cardinality | Nature |
|-------|-------------|--------|
| Endset | Set of spans (possibly discontiguous) | Arbitrary collection |
| Span | Pair of tumblers (contiguous range) | "from here to there" |
| Tumbler/I-address | Single point | Individual byte position |

### Mapping vs. projection

Nelson describes endsets as **mapping** to the tumbler line:

> "There is a universal address space, the tumbler line... We may visualize a link's endsets as mapping to it." [LM 4/45]

> "A link's home (any home) is an element located on one side; and its three endsets map to the other sides." [LM 4/46]

This is the closest concept I can find in the curated sources to what you might be calling "projection." But Nelson calls it **mapping**, and he describes it as a *visualization* of how endsets relate to tumbler-space — not as a named operation in FEBE.

### FEBE operations on endsets

The operations that touch endsets are:
- **MAKELINK** — creates a link with three endsets
- **FINDLINKSFROMTOTHREE** — searches by constraining any combination of endsets
- **RETRIEVEENDSETS** — returns from-set and to-set of specified links

These operate at the endset level. Nelson does not define separate operations for "project to spans" or "project to individual I-addresses" with different cardinality semantics.

## My Honest Assessment

If "projection" is being used in your current work (I see `link-projection displacement` in the recent commit log) as a term for the relation between an endset and the bytes it ultimately resolves to, that is a perfectly reasonable implementation concept — but it is **not a primitive I defined in Literary Machines**. I designed endsets as the unified addressing mechanism, with spans and tumblers as their constituents, and I described their relation to tumbler-space as a *mapping* for visualization purposes.

Whether your implementation should treat projection as one operation or three with different cardinalities is an implementation decision that depends on your back-end model. I did not specify it.

If you have raw-page text where "projection" appears, please point me to it and I can give a more authoritative answer.
