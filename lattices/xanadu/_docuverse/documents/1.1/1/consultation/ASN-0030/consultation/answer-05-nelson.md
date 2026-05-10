## Question 5 [nelson]

> When content is shared across multiple documents, does each document refer to the same address for that content, or does each receive its own address for its own copy?

## Each document refers to the same I-space address

When content is shared across multiple documents, every document points to the **same permanent I-space address**. There is no duplication. This is the central architectural insight of Xanadu.

### The mechanism

Content is created once and stored permanently at an I-space address. Documents are V-space arrangements — sequences of references to I-space content. When you "include" content from another document, your document's V-space simply adds a mapping to the same I-space bytes that already exist.

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

> "The virtual byte stream of a document may include bytes from any other document." [LM 4/10]

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

The word "virtual" is key. These are not copies in the conventional sense — they are references. The content exists at one I-space address, and multiple V-space arrangements point to it.

### The COPY operation is transclusion, not duplication

The FEBE COPY command does **not** create a second instance of the content:

> "The material determined by \<spec set\> is copied to the document determined by \<doc id\> at the address determined by \<doc vsa\>." [LM 4/67]

Despite the name "COPY," this creates a V-space mapping to existing I-space content. The destination document's V-stream now includes a reference to the same bytes at the same I-space address. No new bytes are stored.

### Identity is structural, not value-based

This distinction matters: content identity is determined by **where it was created**, not by what it says. If I type "hello" and you independently type "hello," those are different I-space addresses — different bytes, different origins. But if you transclude my "hello" into your document, your document points to **my** I-space address. We share the same bytes.

This is how the system knows the difference between coincidental similarity and actual quotation. Shared I-space addresses prove derivation; matching text alone does not.

### Why this matters

Because all documents sharing content point to the same I-space address:

1. **Attribution is automatic** — the I-address encodes which document created the bytes, so origin is always traceable: "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

2. **Correspondence is computable** — the system can identify shared content across versions and documents by comparing I-addresses: "a facility that holds multiple versions of the same material... is not terribly useful unless it can help you intercompare them in detail — unless it can show you, word for word, what parts of two versions are the same." [LM 2/20]

3. **Royalties flow correctly** — when shared bytes are delivered, the system knows whom to pay because the I-address identifies the owner.

4. **No distributed update problem** — since there is only one instance of the content, there is nothing to synchronize: "No copying operations are required among the documents throughout the system, and thus we solve the problems of update — especially the problem of updating documents which depend on other documents." [LM 2/36]

### The analogy

Think of I-space as a library where every book has a permanent shelf location. A document is a reading list — a sequence of references like "shelf A, pages 1-5; shelf B, pages 3-7." Multiple reading lists can reference the same shelf locations. The books are never duplicated; only the reading lists differ.

```
I-Space (permanent)           V-Space (per-document)
┌──────────────────┐          Document A: [ref X, ref Y]  → "hello world"
│ addr X: "hello"  │          Document B: [ref X, ref Z]  → "hello!"
│ addr Y: " world" │          Document C: [ref X, ref Y]  → "hello world"
│ addr Z: "!"      │
└──────────────────┘          A and C share the same I-addresses for
                              identical content — true transclusion.
```

Documents A and C both contain "hello world" and both point to the **same** I-space addresses X and Y. This shared origin is what makes them correspond — not the fact that they happen to display the same text.
