## Question 4 [nelson]

> Can the same content be added to multiple documents simultaneously, and if so, does each addition create separate content or does the system recognize them as the same material?

# Content Identity: Creation vs. Value

This question goes to the heart of Xanadu's architecture. The answer depends entirely on *how* the content arrives in each document, and the distinction is deliberate and fundamental.

## Two Scenarios, Two Different Answers

### Scenario 1: Independent INSERT into multiple documents

If you type "hello world" into Document A via INSERT, and independently type "hello world" into Document B via INSERT, you have created **two separate pieces of content** with **different I-space addresses**.

The system does **not** recognize them as "the same material." They happen to have identical byte values, but they are distinct content with distinct origins.

From the content provenance design intent:

> "Content identity is based on creation, not value. Two documents with identical text created independently have DIFFERENT I-addresses. Transcluded content SHARES the same I-address. This is how the system distinguishes 'wrote the same words' from 'quoted from the original.'"

Each INSERT creates new native bytes in I-space under the target document's control:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control." [LM 4/11]

### Scenario 2: COPY (transclusion) from one document to others

If you INSERT "hello world" into Document A, then COPY that content into Documents B and C, all three documents **share the same I-space addresses**. The system absolutely recognizes this as the same material.

The COPY operation is transclusion — it creates a V-space mapping to existing I-space content without creating new bytes:

> "The material determined by \<spec set\> is copied to the document determined by \<doc id\> at the address determined by \<doc vsa\>." [LM 4/67]

The curated operations source confirms: "This is transclusion — the copy shares I-addresses with the source."

In Documents B and C, those bytes are "inclusions" or "virtual copies":

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

## Why This Distinction Matters

The I-address is the proof of origin and the basis for:

1. **Attribution** — transcluded content traces back to Document A's owner
2. **Royalties** — when B or C is read, A's owner gets paid for their bytes
3. **Discovery** — `FINDDOCSCONTAINING` finds all documents sharing that I-space content: "This returns a list of all documents containing any portion of the material included by \<vspec set\>." [LM 4/70]
4. **Correspondence** — version comparison works because shared I-addresses reveal what's the same across documents

If identical text were automatically recognized as "the same," the system would conflate independent creation with deliberate quotation — destroying the distinction between "wrote the same words" and "quoted from the original." That distinction is what makes attribution structural rather than metadata.

## The Architectural Picture

```
Independent INSERT:                  COPY (transclusion):

I-Space:                             I-Space:
  Addr X: "hello world" (Doc A's)      Addr X: "hello world" (Doc A's)
  Addr Y: "hello world" (Doc B's)
                                     V-Space:
V-Space:                               Doc A: [ref X]  (native)
  Doc A: [ref X]                        Doc B: [ref X]  (inclusion)
  Doc B: [ref Y]                        Doc C: [ref X]  (inclusion)

System sees: TWO things              System sees: ONE thing, THREE views
```

## No Simultaneous Multi-Document Operation

The FEBE protocol does not provide a single operation to add content to multiple documents at once. Each INSERT and COPY targets one document. So "adding the same content to multiple documents" is always a sequence: first create it somewhere (INSERT), then share it (COPY). The first step creates content; subsequent COPYs reference it.

This is by design. Content has exactly one home — one I-address, one native document, one owner. The append-only permascroll records it once. Everything else is reference.
