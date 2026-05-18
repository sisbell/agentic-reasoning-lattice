## Question 8 [theory]

> Did the docuverse design assume sequentially-executed, atomically-committed operations at the protocol layer, or was concurrent operation contemplated — and if so, what serialization or transactional discipline did the design assume?

# Concurrency in the Xanadu Protocol

The FEBE protocol I specified was **command-at-a-time and stateless**. Each of the 17 commands in XU.87.1 was a discrete operation, and as I wrote:

> "What the Xanadu storage and hypertext system does--and thus is--is defined by the commands to which it responds." [LM 4/61]

I described the commands themselves as conceptually simple:

> "FEBE includes instructions for insertion in a document, deletion from a document, and rearrangements of unlimited size. These are conceptually simple." [LM 4/61]

## What I deliberately did NOT specify

In Literary Machines I left unspecified:

- OPEN/CLOSE or session establishment
- Locking protocols for concurrent editing
- Transaction boundaries grouping multiple commands
- Read/write modes
- Conflict detection or resolution

These I deferred to the implementor. Roger Gregory's BERT (Back-End Request Token) mechanism in udanax-green — with its lock table and read/write modes — is the implementation of the session layer I left undesigned. It is consistent with my intent but it is his work, not mine.

## What I did contemplate

**Concurrent users at the server level.** I described this as a future enhancement:

> "In later versions of the storage system, we expect the back end to combine the search models of different users to create a barrel-roll shared search model which repeatedly crosses the address space on behalf of all a server's users simultaneously." [LM 4/59]

The "simultaneously" was intentional. The back end was meant to serve many users at once.

**Atomic assimilation between servers.** For BEBE I specified that each server must remain in canonical state. The system model "is at all times unified and operational," and any information moving between servers leaves "each server in canonical operating condition with a slightly improved map of what is elsewhere. The contents can slosh back and forth dynamically." [LM 4/72]

This implies an atomic-like discipline at the BEBE layer — but I specified the invariant, not the mechanism to achieve it.

## Structural choices that sidestep most conflicts

The architecture was designed so that explicit transactions would be needed less often than in conventional systems:

1. **The Istream is append-only and immutable.** Once content is written at an I-address, that address always returns that content. Reads are inherently consistent — there is no stale-read problem at the content layer.

2. **Modification of others' documents produces versions, not conflicts.** If you cannot modify the original, you create a new document. As I wrote: "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate--without damaging the originals." [LM 2/45] Writing always succeeds — if not to the original, then to a fresh version.

3. **Links attach to spans of bytes, not positions.** They survive concurrent editing of the content they point to because the addressing target is content identity, not arrangement.

4. **The system was designed for partial failure.** As I noted: "It is a truism that 'computer networks are always broken.' Meaning that on the average some nodes are disconnected or not working." [LM 4/75]

## The honest answer

I assumed concurrent operation was both possible and necessary — the back end was meant to handle many users at once, and BEBE was meant to keep servers in canonical condition through ongoing exchange. But I did not specify the serialization discipline. The structural choices (append-only Istream, version-as-fork on conflict, span-based linking) were intended to **reduce** the need for explicit transactions, not to eliminate it. Where transactional discipline mattered — particularly at BEBE — I specified the invariant ("canonical operating condition") and left the protocol to implementation.

NEED_RAW: 4/59, 4/72 — for verifying exact wording of the barrel-roll and canonical-condition passages (the curated extracts show minor OCR variation between sources on 4/72).
