## Question 8 [nelson]

> Must the system distinguish between "content at this address was removed from this document" and "content at this address no longer exists anywhere in the system"?

## Answer: No — Because the Second State Cannot Occur

Nelson's architecture makes the distinction unnecessary. The state "content at this address no longer exists anywhere in the system" is **architecturally impossible** in Xanadu. There is only one kind of removal, and it is always V-space removal — never I-space destruction.

### I-Space Is Append-Only

Content in I-space is permanent. There is no operation that removes it:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

The `delete-semantics` extraction makes this explicit: "DELETE in Xanadu does NOT mean what it means in conventional systems. It removes content from a document's V-space (current arrangement) but does NOT remove it from I-space (permanent storage)."

### What "Deleted" Actually Means

The diagram on page 4/9 defines the only removal state the system recognizes:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

Note the careful language: **not currently addressable** — not "destroyed," not "gone," not "no longer exists." The bytes are still in I-space. They are simply no longer part of the document's current V-space arrangement.

And Nelson confirms the broader principle:

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

### Why the Distinction Is Moot

After a DELETE operation, the "removed" content remains accessible through:

1. **Historical backtrack** — previous versions of the same document still contain it
2. **Transclusions** — other documents that include-by-reference still show it
3. **I-address resolution** — links pointing to the I-address still resolve
4. **FINDDOCSCONTAINING** — the system can find all documents containing the material

The system always knows where the content lives (its I-address encodes the home document permanently). A front end encountering a V-space gap can always determine that content *was here but was removed from this arrangement* — and can trace the I-address to find the content itself.

### The Only Ambiguity: Operational Failure

Nelson does acknowledge that content could become *unreachable* through operational failure — vendor shutdown, network partition, storage corruption:

> "User acknowledges that due to possible unreliability of the software, unreliability and vulnerability of transmission systems, and myriad possibilities for intrusion and malicious mischief by unseen parties throughout the universe, all storage, and transmission of contents and links, and attempts to deliver such material, are at User's risk." [LM 5/18]

But this is a **failure mode**, not a **designed system state**. The architecture mitigates it through vendor backup obligations and distributed replication, not through semantic distinctions in the address model. The vendor contract requires orderly transition of all customer materials upon cancellation [LM 5/16]. The system is designed so that content *should* always exist somewhere — even if, in practice, operational failures could make it temporarily or permanently unreachable.

### Summary

The system needs only one concept: **V-space presence or absence**. Content is either in a document's current V-stream or it isn't. If it isn't, the content itself still exists in I-space — permanently, by architectural fiat. The question "does this content exist anywhere?" always has the answer "yes." The only meaningful question is "is this content part of this document's current arrangement?" — and that is simply the V-to-I mapping.
