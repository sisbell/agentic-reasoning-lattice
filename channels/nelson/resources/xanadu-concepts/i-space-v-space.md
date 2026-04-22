# Istream and Vstream

Source: Literary Machines, 4/10-4/11 (pages 177-178)

## Semantic Intent

### What It Means

Xanadu has **two address spaces** that serve different purposes:

**Istream (Invariant Space)**
- Where content **permanently lives**
- Addresses are **absolute and immutable**
- Content at an Istream address **never changes**
- Think: "the library stacks" - books have permanent shelf locations

**Vstream (Virtual Space / Version Space)**
- The **document's arrangement** of content
- A **view** that references Istream content
- Can be **rearranged** across versions
- Think: "a reading list" - references books but can be reordered

### User Guarantee

**Istream guarantee:**
- Content you create gets a permanent Istream address
- That address will always return that exact content
- Content is immutable - it never changes after creation

**Vstream guarantee:**
- Your document's arrangement (V-stream) can evolve
- Each version has its own V-stream arrangement
- You can always access any previous arrangement (version)

### Principle Served

**Separation of content from arrangement.** This is the key to Xanadu's model:
- Content is permanent (Istream) → enables permanent citations, links
- Arrangement is flexible (Vstream) → enables editing, versions
- Links point to Istream → survive editing
- Edits change Vstream → don't destroy content

### How Users Experience It

Users don't see Istream vs Vstream directly. They experience the effects:
- Edit a document → you're changing Vstream arrangement
- Content you "delete" → still exists in Istream, recoverable from old version
- Links to content → work even after content is "deleted" (point to Istream)
- Create new version → new Vstream arrangement, same Istream content

### Analogy

```
Istream (Library)              Vstream (Reading Lists)
┌─────────────────────┐        ┌─────────────────────┐
│ Shelf A: "hello"    │        │ My Essay v1:        │
│ Shelf B: " world"   │   ──►  │   [ref A, ref B]    │  → "hello world"
│ Shelf C: "!"        │        │                     │
│                     │        │ My Essay v2:        │
│ (never changes)     │   ──►  │   [ref A, ref C]    │  → "hello!"
└─────────────────────┘        └─────────────────────┘
```

The library stacks (Istream) never change. Reading lists (Vstream) can be rearranged.

### Nelson's Words

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." (4/11)

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." (4/11)

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." (4/11)

> "The virtual byte stream of a document may include bytes from any other document." (4/10)

> "Logical addressing of the byte stream is in the form of virtual spans, or vspans. These are sequences of bytes in the document's virtual byte stream, regardless of their native origin." (4/11)

### Terminology Mapping

| Nelson's Term | Implementation Term | Meaning |
|--------------|---------------------|---------|
| Native bytes, "home location" | Istream, I-stream | Where content permanently lives |
| Virtual byte stream, vspan | Vstream, V-stream | Document's arrangement of content |
| Inclusions, virtual copies | Transclusions | References to non-native bytes |

---

## Related Concepts

| Concept | Relationship |
|---------|--------------|
| [tumblers](tumblers.md) | Addressing scheme for both Istream and Vstream |
| [transclusion](transclusion.md) | Vstream can reference Istream content from other documents |
| [versions](versions.md) | Each version is a different Vstream arrangement over same Istream |
| [correspondence](correspondence.md) | Shared Istream origin enables matching across versions |
| [documents](documents.md) | Documents own Istream content and have Vstream arrangements |
| [enfilades](enfilades.md) | Implementation: GRAN stores Istream, POOM maps V→I |

## FEBE Operations

This concept is foundational - nearly every operation involves Istream or Vstream:

| Operation | How Istream/Vstream applies |
|-----------|----------------------------|
| **INSERT** | Adds to Istream; updates Vstream arrangement |
| **APPEND** | Adds to Istream at document end |
| **DELETE** | Removes from Vstream only; Istream unchanged |
| **COPY** | Creates Vstream mapping to existing Istream (transclusion) |
| **REARRANGE** | Pure Vstream operation |
| **CREATENEWVERSION** | New Vstream arrangement, same Istream content |
| **FINDDOCSCONTAINING** | Searches Istream origin, returns Vstream locations |
| **SHOWRELATIONOF2VERSIONS** | Correspondence via shared Istream |

See [FEBE Protocol](../febe-protocol.md) for operation details.
See [Concept-Operation Map](../concept-operation-map.md) for full mapping.
