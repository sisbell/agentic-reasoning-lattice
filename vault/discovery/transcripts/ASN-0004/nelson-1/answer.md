# Yes — On Both Counts

Nelson's design makes inserted content both immediately available and permanently indestructible within the system. These are not incidental properties but load-bearing guarantees that the entire architecture depends upon.

## Immediate Retrievability

Nelson is explicit that content materializes the moment you request it:

> "THE PART YOU WANT COMES WHEN YOU ASK FOR IT." [LM 2/16]

> "We call this pounce. You pounce like a cat on a given thing, and it seems to be there, having been constructed while you wait, as it were, in midair." [LM 2/16]

This is a user-facing guarantee, not merely an aspiration. The system is designed so that once an operation completes, the content is part of the living docuverse — addressable, retrievable, linkable. There is no staging area, no pending state, no eventual consistency in Nelson's model. Content that has been inserted IS content in the system.

## Permanent Retrievability

No operation in the FEBE protocol destroys I-space content. Nelson's storage model is explicitly append-only:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

Every byte receives a permanent I-space address:

> "New items may be continually inserted in tumbler-space while the other addresses remain valid. This means that any address of any document in an ever-growing network may be specified by a permanent tumbler address." [LM 4/19]

## DELETE Cannot Make Content Vanish

The strongest evidence is what DELETE actually does. It operates on V-space (the document's current arrangement) and leaves I-space (permanent storage) untouched:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

The phrase "not currently addressable" is precise — the content is not gone, merely not visible in the current V-space arrangement. It remains in I-space, accessible through historical backtrack and still present in any other document that transcludes it.

## No Other Operation Threatens I-Space Content

Examining the FEBE operations:

- **INSERT** adds to I-space; never removes
- **DELETE** removes from V-space only
- **REARRANGE** is a pure V-space operation
- **COPY** creates V-space references to existing I-space content
- **CREATENEWVERSION** creates a new V-space arrangement over shared I-space content

There is no FEBE command that removes bytes from I-space. The operation set is designed so that I-space only grows.

## Published Content Has an Additional Social Lock

For published documents, Nelson adds an explicit social guarantee beyond the technical one:

> "It is in the common interest that a thing once published stay published, as in the world of paper. Other readers and users will come to depend on its accessibility. Consequently its author may not withdraw it except by lengthy due process." [LM 2/43]

This is because links made by other users depend on the content's continued existence:

> "However, for corrections and amendments, the author may readily publish a superseding document, but the former version must remain on the network. This is vital because of the links other users may have made to it." [LM 2/43]

## The Deeper Principle

Nelson's non-destruction guarantee is not just a feature — it is the architectural foundation:

> "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate — without damaging the originals. This is done by inclusion links." [LM 2/45]

> "Virtually all of computerdom is built around the destructive replacement of successive whole copies of each current version." [LM 2/14]

Xanadu exists precisely to abolish destructive replacement. If any operation could make inserted content vanish, the system would reduce to conventional file storage — the very thing Nelson designed Xanadu to transcend.

## Summary

The system must guarantee both properties:

1. **Immediate**: Once INSERT completes, the content is retrievable. It has a permanent I-space address, is part of the docuverse, and can be linked to, transcluded, and queried.

2. **Permanent**: No subsequent operation — not DELETE, not REARRANGE, not any combination of FEBE commands — can remove content from I-space. The only thing that can change is *which V-space arrangements reference it*. The content itself endures.

This is the meaning of the append-only storage model: I-space grows monotonically. Once bytes enter, they never leave. The entire edifice of permanent addresses, link survivability, historical backtrack, version comparison, and automatic attribution depends on this being true without exception.