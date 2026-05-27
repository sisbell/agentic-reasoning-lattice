## Question 7 [theory]

> Did the Xanadu design intend INSERT to provide composite-level atomicity (no other operation's elementary transitions interleave between INSERT's allocation, arrangement, and provenance steps for the same document), or was concurrent-INSERT serialisation left to the implementation as a separate concern?

# INSERT Atomicity in Xanadu

My specification of INSERT (and the other 16 commands in XU.87.1) addressed **what** the operation does, not **how** it must be serialised against concurrent requests. Composite-level atomicity for INSERT was not part of the design intent — concurrent-INSERT serialisation was left to the implementation.

## What I actually specified

INSERT is described purely as a semantic operation:

> "This inserts <text set> in document <doc id> at <doc vsa>. The v-stream addresses of any following characters in the document are increased by the length of the inserted text." [LM 4/66]

There is no mention of allocation/arrangement/provenance steps as a composite, no transactional bracketing, no language about interleaving. Of the 17 commands, only one (RETRIEVEV) was even concerned with content delivery [LM 4/61] — the rest, including INSERT, are described at the level of effect, not execution sequence.

## What I explicitly left to later work

In Chapter 4 I anticipated multi-user concurrency as a future concern:

> "In later versions of the storage system, we expect the back end to combine the search models of different users to create a barrel-roll shared search model which repeatedly crosses the address space on behalf of all a server's users simultaneously." [LM 4/59]

The phrase "in later versions" signals that simultaneous-user mechanics were a known concern deferred to back-end implementation, not a guarantee of the protocol.

## What I did not specify

My protocol is stateless at the command level — name a document by its tumbler address, issue a command, get a response. I did not provide:

- OPEN/CLOSE operations or session state on a document
- Read vs. write modes
- A locking protocol or any mention of concurrent editing of the same document
- A session lifecycle

The principle that grounds this absence is **"writing always succeeds"**: if you do not own the original, you create a version [LM 2/45]. Denial is a fork, not an error. This is a *semantic* answer to contention, not a *concurrency-control* answer.

## What was left to the implementor

Gregory's BERT (Back-End Request Token) mechanism — OPEN, CLOSE, READBERT, WRITEBERT, the lock table, denial-as-branching — is the session/atomicity layer that I left undesigned. It is consistent with my intent (ownership, writing-always-succeeds, no surveillance) but it is not specified by me. Any guarantee about the elementary transitions of INSERT not interleaving with another operation's transitions belongs to that implementation layer, not to the Literary Machines design.

## Bottom line

I designed at the level of "what owners may do to their documents and what readers may see," not at the level of "what happens when two requests arrive in flight." Composite-level atomicity for INSERT is an implementation property a Xanadu back end must provide to make my semantic guarantees (permanence, attribution, version history) hold under concurrency — but I did not mandate or describe it.

NEED_RAW: 4/66 (verify INSERT spec has no transactional language), 4/74-4/75 (network/concurrency discussion in BEBE section) — these would confirm by exhaustion that no atomicity language appears in the protocol chapters.
