## Question 10 [nelson]

> When content is permanently stored, does it receive a fixed identity at that moment, and must every document arrangement that uses that content refer to it by that same identity forever?

# Yes, on Both Counts

## Content Receives Fixed Identity at Storage Time

When you create content — when bytes are first stored — they receive a permanent I-space address. That address encodes their origin: which server, which account, which document, which element position. This address is **immutable**. The content at that address **never changes**.

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

The storage model is append-only:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

Nothing is overwritten. Nothing is reassigned. The I-address a byte receives at creation is the I-address it keeps forever.

## Every Arrangement Must Reference That Same Identity

A document's V-space (its current arrangement, the virtual byte stream the user sees) is a **mapping to I-space**. The document IS that mapping. When you "include" content from another document, you do not copy it — you create a V-space entry that points to the same I-space address where the content permanently lives.

> "The virtual byte stream of a document may include bytes from any other document." [LM 4/10]

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

The V-address — where the content appears in the document right now — may change constantly through editing. But the I-address it refers to does not:

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." [LM 4/11]

That quote describes V-space addresses (positions in the arrangement) being ephemeral. The I-space addresses they point to are permanent.

## Why This Matters

This separation is the architectural foundation for everything else in Xanadu:

**Link survivability.** Links point to I-space addresses. Editing changes V-space arrangements. Therefore links survive editing:

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." [LM 4/30]

**Correspondence across versions.** When two versions share I-space content, the system knows which parts correspond — because they reference the same I-addresses. This is structural, not metadata:

> "Of course, a facility that holds multiple versions of the same material, and allows historical backtrack, is not terribly useful unless it can help you intercompare them in detail — unless it can show you, word for word, what parts of two versions are the same." [LM 2/20]

**Transclusion.** When you quote someone, your document's V-space points to their I-space. The content is fetched from its home. Attribution cannot be severed because the reference mechanism requires the I-address:

> "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

**Non-destruction.** "Deleting" content removes it from V-space (the current arrangement) but not from I-space (permanent storage). Previous versions still contain it. Links to it still resolve.

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

## The Analogy

Think of I-space as library stacks where books have permanent shelf locations. V-space is a reading list that references those shelf locations. You can reorder the reading list, add entries, remove entries — but the books on the shelves never move. Two different reading lists that reference the same shelf location are referencing the same book. That identity — the shelf location — is fixed at the moment the book is shelved and never changes.

```
I-Space (permanent)              V-Space (arrangement)
┌─────────────────────┐          ┌─────────────────────┐
│ I-addr A: "hello"   │          │ Doc v1: [A, B]      │ → "hello world"
│ I-addr B: " world"  │     ──►  │ Doc v2: [A, C]      │ → "hello!"
│ I-addr C: "!"       │          │ Other doc: [A, B, C] │ → "hello world!"
│                     │          │                     │
│ (never changes)     │          │ (freely rearranged)  │
└─────────────────────┘          └─────────────────────┘
```

Every V-space arrangement, in every document, in every version, refers to content by its fixed I-space identity. That is not a convention — it is the architecture.
