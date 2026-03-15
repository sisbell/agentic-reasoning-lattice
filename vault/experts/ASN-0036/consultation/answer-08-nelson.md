## Question 8 [nelson]

> Must the permanent content layer be append-only, or can stored content ever be modified in place after initial storage?

## The Permanent Content Layer Must Be Append-Only

Content in I-space **cannot be modified in place after initial storage**. This is not a preference but a structural requirement — the entire architecture depends on it.

### Nelson's Explicit Statement

Nelson proposes append-only storage as the foundation:

> "Virtually all of computerdom is built around the destructive replacement of successive whole copies of each current version." [LM 2/14]

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

He elaborates on what "true storage" must be:

> "The true storage of text should be in a system that stores each change and fragment individually, assimilating each change as it arrives, but keeping the former changes." [LM 2/15]

### Why Modification Is Structurally Impossible

Six system guarantees depend on I-space immutability:

**1. Permanent addresses.** An I-space address always returns the same bytes. If content could be modified in place, the address would return different content at different times, violating the permanence guarantee.

**2. Link survivability.** Links attach to I-space byte spans. If those bytes could change, links would still "survive" but would connect to different content — silently corrupting every link in the docuverse that references the modified bytes.

> "Links between bytes can survive deletions, insertions and rearrangements, if anything is left at each end." [LM 4/43]

This guarantee means the bytes themselves must be stable, not just their addresses.

**3. Transclusion integrity.** When document A transcludes content from document B, readers see B's bytes. If B's owner could modify those bytes in place, A's meaning would change without A's owner's knowledge or consent. Nelson explicitly says:

> "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate — without damaging the originals." [LM 2/45]

Modification in place would damage every document that transcludes the modified content.

**4. Version history / historical backtrack.** The ability to reconstruct any previous state depends on the permanence of stored content:

> "The file management system we are talking about automatically keeps track of the changes and the pieces, so that when you ask for a given part of a given version at a given time, it comes to your screen." [LM 2/15]

If I-space content could be overwritten, previous versions could not be reconstructed.

**5. Correspondence.** Version comparison works because shared I-space addresses identify corresponding parts across versions. Modifying content in place would break this structural relationship.

**6. Origin traceability.** Attribution is guaranteed because I-addresses encode the home document:

> "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

This only holds if the bytes at an I-address are the same bytes that were originally stored there.

### The FEBE Protocol Confirms It

Of the 17 FEBE commands Nelson specifies, **none modifies existing I-space content**. The editing operations work exclusively on V-space arrangements:

- **INSERT** — adds new bytes to I-space; updates V-space mapping [LM 4/66]
- **DELETEVSPAN** — removes a span from V-space only; I-space unchanged [LM 4/66]
- **COPY** — creates V-space mapping to existing I-space (transclusion) [LM 4/67]
- **REARRANGE** — pure V-space operation [LM 4/67]
- **APPEND** — adds new bytes to I-space at document end [LM 4/67]

There is no MODIFY, UPDATE, or REPLACE operation. The absence is deliberate.

### DELETE Does Not Modify I-Space

Nelson is explicit that deletion is a V-space operation:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

"Deleted" bytes continue to exist at their I-space addresses. They are removed from the current V-space view, nothing more.

### Summary

The permanent content layer is unconditionally append-only. Nelson designed the entire system around the rejection of "destructive replacement" [LM 2/14]. Every guarantee — permanence, attribution, link survivability, transclusion integrity, version history, and correspondence — depends on the invariant that **once a byte is stored at an I-space address, it is that byte forever**.
