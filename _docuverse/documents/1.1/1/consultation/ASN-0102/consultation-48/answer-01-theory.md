## Question 1 [theory]

> Was COPY intended to be combinable with other operations (e.g. a single COPY-then-DELETE) into one atomic transaction, or is it by design an isolated editing primitive that always stands alone?

Based on the curated sources, here's what I can determine.

## Short answer

Nelson presents COPY as a **discrete, standalone FEBE command**, not as something designed to be bundled with other operations into a single atomic transaction. There is no transaction or atomicity concept anywhere in the curated material — the protocol is defined command-by-command.

## What the sources support

Nelson defines the system entirely by its individual commands:

> "What the Xanadu storage and hypertext system does--and thus is--is defined by the commands to which it responds." (4/61)

COPY is one of 17 discrete commands in XU.87.1, with its own self-contained definition:

> "The material determined by <spec set> is copied to the document determined by <doc id> at the address determined by <doc vsa>." (4/67)

The editing primitives are listed as separate, simple operations:

> "FEBE includes instructions for insertion in a document, deletion from a document, and rearrangements of unlimited size. These are comparatively simple." (4/61)

The protocol is stateless at the command level — you name a document by tumbler address, issue one command, and the back end responds (per the session-model source). There is no OPEN/COMMIT envelope, no grouping mechanism, and no notion of multiple operations succeeding or failing together.

## The one telling counterexample: REARRANGE

The design *does* show Nelson's pattern for combining operations — and it argues for bundling at the level of a **single new primitive**, not a transaction wrapper:

> "Rearrange transposes two regions of text. With three cuts, the two regions are from cut 1 to cut 2, and from cut 2 to cut 3... With four cuts, the regions are from cut 1 to cut 2, and from cut 3 to cut 4." (4/67)

REARRANGE is effectively a move (a DELETE-and-reinsert) expressed as one atomic command — rather than asking the user to compose smaller operations. This suggests that *when* Nelson wanted compound behavior, he created a dedicated primitive for it. He did **not** do this for COPY-then-DELETE; he left COPY, DELETE, and INSERT as independent commands. So a "move via COPY+DELETE" is not specified as an atomic unit — REARRANGE is the intended primitive for relocation.

## Important caveat

The curated sources never use the words "transaction" or "atomic," and Nelson does not explicitly discuss whether commands can be grouped, sequenced atomically, or rolled back as a unit. So the conclusion above is drawn from the *structure* of the protocol (discrete, stateless commands) rather than an explicit statement that COPY must stand alone. The strongest verifiable claim is: **Nelson specifies COPY as an isolated primitive and provides no transaction-combination mechanism.**

To confirm there is no discussion of command grouping/atomicity in the full protocol section, I'd need the raw pages:

NEED_RAW: 4/61-4/70 (FEBE command definitions and any surrounding discussion of command sequencing/transactions)
