## Question 10 [nelson]

> Must the system guarantee that the permanent content layer and the document arrangement layer are never merged — that no operation on arrangements can corrupt or alter stored content?

# Yes — The Separation of I-Space and V-Space Is a Structural Invariant

Nelson's design requires that no operation on arrangements (V-space) can corrupt or alter stored content (I-space). This is not merely an implementation preference but a load-bearing architectural invariant on which multiple guarantees depend.

## Nelson States the Separation Explicitly

The clearest statement comes from the discussion of derivative documents:

> "The integrity of each document is maintained by keeping the two aspects separate: derivative documents are permanently defined (and stored) in terms of the originals and the changes." [LM 2/37]

"The two aspects" are content (I-space) and arrangement (V-space). Nelson says integrity *depends on* keeping them separate — not that separation is convenient, but that it is necessary for integrity.

## I-Space Is Append-Only by Design

Nelson rejects the conventional model of destructive replacement:

> "Virtually all of computerdom is built around the destructive replacement of successive whole copies of each current version." [LM 2/14]

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

Content enters I-space and never changes. The I-space guarantee from the curated concept file states: "Content at an I-space address never changes" and "Content is immutable — it never changes after creation."

## Every FEBE Operation Respects the Boundary

Examining all editing operations Nelson specifies:

| Operation | I-Space Effect | V-Space Effect |
|-----------|---------------|----------------|
| **INSERT** | Appends *new* bytes | Updates arrangement |
| **APPEND** | Appends *new* bytes at end | Extends V-stream |
| **DELETEVSPAN** | None | Removes span from current view |
| **REARRANGE** | None | Transposes regions |
| **COPY** | None | Creates V-space mapping to *existing* I-space |
| **CREATENEWVERSION** | None | New V-space arrangement over same I-space |

No operation modifies existing I-space content. INSERT and APPEND create *new* I-space entries; they never touch existing ones. DELETE, REARRANGE, and COPY are pure V-space operations. COPY is especially telling — it is transclusion, meaning it creates a V-space reference to someone else's I-space bytes without duplicating or altering them.

Nelson describes DELETE explicitly:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

Delete removes from V-space. I-space is untouched.

## The Invariant Is Load-Bearing

If any V-space operation could mutate I-space content, the following guarantees would collapse:

**Historical backtrack** — Nelson promises "when you ask for a given part of a given version at a given time, it comes to your screen" [LM 2/15]. Reconstructing past states requires that the I-space fragments from which those states are assembled remain unchanged.

**Link survivability** — Links point to I-space bytes. Nelson: "since the links are to the bytes themselves, any links to those bytes remain stably attached to them" [LM 4/30]. If I-space content could be mutated by arrangement operations, links would silently point to altered content.

**Transclusion integrity** — When document A transcludes content from document B, both reference the same I-space bytes. If B's owner could corrupt those bytes through an editing operation, A's content would be silently damaged — violating "without damaging the originals" [LM 2/45].

**Origin traceability** — "You always know where you are, and can at once ascertain the home document of any specific word or character" [LM 2/40]. This depends on I-addresses being permanently meaningful. Mutated content at a stable address would make the address a lie.

**Correspondence** — Version comparison works by finding shared I-space origins: "a facility that holds multiple versions is not terribly useful unless it can help you intercompare them in detail" [LM 2/20]. If I-space content changed, the correspondence relation would become unreliable.

## The Analogy Nelson Uses

Nelson's library analogy captures the invariant precisely:

```
I-Space (Library)              V-Space (Reading Lists)
┌─────────────────────┐        ┌─────────────────────┐
│ Shelf A: "hello"    │        │ My Essay v1:        │
│ Shelf B: " world"   │   ──►  │   [ref A, ref B]    │
│ Shelf C: "!"        │        │ My Essay v2:        │
│ (never changes)     │   ──►  │   [ref A, ref C]    │
└─────────────────────┘        └─────────────────────┘
```

The library stacks never change. Reading lists can be rearranged, extended, or abandoned — but no reading-list operation alters the books on the shelves.

## Conclusion

The system must guarantee that the permanent content layer and the document arrangement layer are never merged. Nelson states this directly ("integrity... maintained by keeping the two aspects separate" [LM 2/37]), designs every operation to respect it, and builds at least five user-facing guarantees on top of it. Violating this invariant would not break one feature — it would break the architectural foundation on which permanence, survivability, transclusion, traceability, and version comparison all rest.
