## Question 4 [nelson]

> Must the address of content be determined solely by when it was created, or may the system reassign addresses to optimize retrieval?

# Addresses Are Permanent: The Non-Negotiable Invariant

**The address of content is determined at creation and may never be reassigned.** This is not a design preference — it is the invariant upon which the entire system depends.

## The Two Address Spaces

Xanadu has two address spaces with fundamentally different permanence properties:

**I-Space addresses are permanent and immutable.** Content gets an I-space address when created, and that address returns that exact content forever. The permascroll is append-only:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

**V-Space addresses are explicitly ephemeral.** They change with every edit:

> "The v-stream addresses of any following characters in the document are increased by the length of the inserted text." [LM 4/66]

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." [LM 4/30]

V-space is the system's built-in mechanism for "reassigning" the user-visible arrangement without touching content identity.

## Why I-Space Reassignment Is Forbidden

The permanence of I-space addresses is the foundation for every major guarantee:

| Guarantee | Depends on permanent I-addresses because... |
|-----------|----------------------------------------------|
| **Link survivability** | Links point to I-space; they survive editing because I-addresses don't change |
| **Transclusion** | Inclusion by reference works because the reference (I-address) is stable |
| **Version comparison** | Correspondence is detected via shared I-space origin |
| **Origin traceability** | The I-address encodes the home document — reassignment would sever attribution |
| **Permanent citation** | A reference made today must work forever |

Nelson states this directly:

> "New items may be continually inserted in tumbler-space while the other addresses remain valid. This means that any address of any document in an ever-growing network may be specified by a permanent tumbler address." [LM 4/19]

## Physical Location May Change; Addresses May Not

The system explicitly separates logical address from physical location. The BEBE protocol moves content between servers for performance optimization:

> "Material is moved between servers for a number of purposes: 1. for more rapid access to final material, 2. for more rapid access to needed material which indexes material on other servers, 3. for rebalance in keeping with demand, 4. for redundancy and backup purposes." [LM 4/71]

> "The contents can slosh back and forth dynamically." [LM 4/72]

This is the correct place for retrieval optimization: move the bytes closer to demand, cache popular content, replicate for resilience — but the tumbler address stays fixed. The user sees the same address regardless of which server physically holds the content.

## The Enfilade Solution

Nelson's enfilades are specifically designed to make permanent addressing efficient despite continuous editing:

> "His new method would allow linkages to keep up with all changes. It was instantaneous and permanent and could grow indefinitely. All changes, once made, left the file remaining in canonical order, which was an internal mandate of the system." [LM 1/34]

The enfilades maintain the V→I mapping (POOM enfilade) and the content storage (GRAN enfilade) so that retrieval remains fast even as the mapping grows complex. The "eye in the pyramid" insight was precisely about making permanent addresses work efficiently — solving the performance problem without sacrificing the permanence invariant.

## Time Is Not the Address

One subtlety: while I-space is append-only (chronological), time itself is not encoded in the tumbler:

> "Note that 'time' is not included in the tumbler. Time is kept track of separately." [LM 4/18]

The address encodes *provenance* (server, user, document, element position), not timestamp. Within a document's I-stream, later-created content gets higher element numbers because append-only storage is sequential — but the address is a structural identifier, not a temporal one.

## Summary

The system has a clear answer to your question:

- **I-space addresses**: determined solely at creation, permanent, never reassigned — this is inviolable
- **V-space addresses**: ephemeral by design, change with every edit — this is the intended mechanism for rearrangement
- **Physical location**: may change freely for optimization — BEBE handles this transparently
- **Performance**: achieved through data structures (enfilades) and caching (subrepresentations), never through address reassignment

Reassigning I-space addresses would be like reassigning DNA — it would sever every relationship (links, transclusions, version correspondence, attribution) that depends on content identity. The entire docuverse is built on the assumption that I-space addresses are eternal.
