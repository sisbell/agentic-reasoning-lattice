# I-Space and V-Space

Source: Literary Machines, 4/10-4/11 (pages 177-178)

## Semantic Intent

### What It Means

Xanadu has **two address spaces** that serve different purposes:

**I-Space (Invariant Space)**
- Where content **permanently lives**
- Addresses are **absolute and immutable**
- Content at an I-space address **never changes**
- Think: "the library stacks" - books have permanent shelf locations

**V-Space (Virtual Space / Version Space)**
- The **document's arrangement** of content
- A **view** that references I-space content
- Can be **rearranged** across versions
- Think: "a reading list" - references books but can be reordered

### User Guarantee

**I-Space guarantee:**
- Content you create gets a permanent I-space address
- That address will always return that exact content
- Content is immutable - it never changes after creation

**V-Space guarantee:**
- Your document's arrangement (V-stream) can evolve
- Each version has its own V-stream arrangement
- You can always access any previous arrangement (version)

### Principle Served

**Separation of content from arrangement.** This is the key to Xanadu's model:
- Content is permanent (I-space) → enables permanent citations, links
- Arrangement is flexible (V-space) → enables editing, versions
- Links point to I-space → survive editing
- Edits change V-space → don't destroy content

### How Users Experience It

Users don't see I-space vs V-space directly. They experience the effects:
- Edit a document → you're changing V-space arrangement
- Content you "delete" → still exists in I-space, recoverable from old version
- Links to content → work even after content is "deleted" (point to I-space)
- Create new version → new V-space arrangement, same I-space content

### Analogy

```
I-Space (Library)              V-Space (Reading Lists)
┌─────────────────────┐        ┌─────────────────────┐
│ Shelf A: "hello"    │        │ My Essay v1:        │
│ Shelf B: " world"   │   ──►  │   [ref A, ref B]    │  → "hello world"
│ Shelf C: "!"        │        │                     │
│                     │        │ My Essay v2:        │
│ (never changes)     │   ──►  │   [ref A, ref C]    │  → "hello!"
└─────────────────────┘        └─────────────────────┘
```

The library stacks (I-space) never change. Reading lists (V-space) can be rearranged.

### Nelson's Words

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." (4/11)

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." (4/11)

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." (4/11)

> "The virtual byte stream of a document may include bytes from any other document." (4/10)

> "Logical addressing of the byte stream is in the form of virtual spans, or vspans. These are sequences of bytes in the document's virtual byte stream, regardless of their native origin." (4/11)

### Terminology Mapping

| Nelson's Term | Implementation Term | Meaning |
|--------------|---------------------|---------|
| Native bytes, "home location" | I-space, I-stream | Where content permanently lives |
| Virtual byte stream, vspan | V-space, V-stream | Document's arrangement of content |
| Inclusions, virtual copies | Transclusions | References to non-native bytes |

---

## Related Concepts

| Concept | Relationship |
|---------|--------------|
| [tumblers](tumblers.md) | Addressing scheme for both I-space and V-space |
| [transclusion](transclusion.md) | V-space can reference I-space content from other documents |
| [versions](versions.md) | Each version is a different V-space arrangement over same I-space |
| [correspondence](correspondence.md) | Shared I-space origin enables matching across versions |
| [documents](documents.md) | Documents own I-space content and have V-space arrangements |
| [enfilades](enfilades.md) | Implementation: GRAN stores I-space, POOM maps V→I |

## FEBE Operations

This concept is foundational - nearly every operation involves I-space or V-space:

| Operation | How I-space/V-space applies |
|-----------|----------------------------|
| **INSERT** | Adds to I-space; updates V-space arrangement |
| **APPEND** | Adds to I-space at document end |
| **DELETE** | Removes from V-space only; I-space unchanged |
| **COPY** | Creates V-space mapping to existing I-space (transclusion) |
| **REARRANGE** | Pure V-space operation |
| **CREATENEWVERSION** | New V-space arrangement, same I-space content |
| **FINDDOCSCONTAINING** | Searches I-space origin, returns V-space locations |
| **SHOWRELATIONOF2VERSIONS** | Correspondence via shared I-space |

See [FEBE Protocol](../febe-protocol.md) for operation details.
See [Concept-Operation Map](../concept-operation-map.md) for full mapping.
