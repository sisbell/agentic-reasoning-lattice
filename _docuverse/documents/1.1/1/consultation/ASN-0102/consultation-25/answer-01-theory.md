## Question 1 [theory]

> Was the COPY/inclusion operation intended to stand alone as its own atomic act, or to be composable as a step within a larger editing transaction?

## Short answer

At the level Nelson actually specified — the FEBE protocol — **COPY stands alone as a single atomic command**. But Nelson never specified an "editing transaction" concept that would group several commands into one atomic unit, so the question of *transactional composability* is something his text does not address. What his authoring model *does* make clear is that COPY/inclusion is meant to be **composed into larger documents** alongside other operations and new material — composition at the document level, not transaction-level atomicity.

## What the sources support

**1. COPY is a discrete, standalone FEBE primitive.** It is one of seventeen commands in XU.87.1, listed beside INSERT, DELETEVSPAN, REARRANGE, and APPEND. Its specification is self-contained:

> "The material determined by `<spec set>` is copied to the document determined by `<doc id>` at the address determined by `<doc vsa>`." (4/67)

Nelson frames the editing commands as individually simple acts:

> "FEBE includes instructions for insertion in a document, deletion from a document, and rearrangements of unlimited size. These are comparatively simple." (4/61)

So as an operation, COPY is atomic — one command, one effect (a Vstream mapping sharing the source's I-addresses).

**2. The protocol is stateless at the command level — there is no transaction grouping.** Nelson's model names a document by tumbler address, issues a command, and gets a response. There is no OPEN/CLOSE, no multi-command transaction boundary, no locking protocol in his specification (these belong to Gregory's later implementation, not Nelson's text). So Nelson neither requires nor provides a mechanism to make COPY one step inside a larger *atomic* transaction.

**3. But COPY/inclusion is explicitly meant to compose at the document level.** The whole point of inclusion is that it is a building block combined with other material:

> "A compound document consists of parts of old documents together with new material. Or we may say it really consists of quote-links and new material." (2/32)

> "If anything which is already published can be included in anything newly published, any new viewpoint can be freely presented by an easily-made annotated collage." (2/45)

A "collage" of quote-links plus new writing implies COPY operations interleaved with INSERT/APPEND — composition, but as a sequence of independent acts producing one document, not as a bracketed atomic transaction.

## The distinction that matters

The question conflates two senses of "composable":

- **Composable as authoring** (COPY is one building step among many that together yield a compound document) — **yes, clearly intended.** This is the core of transclusion and the collage model.
- **Composable as a transaction** (COPY grouped with other commands so they commit or roll back as one atomic unit) — **Nelson does not address this.** His FEBE is command-atomic and stateless; there is no transaction envelope in the curated specification.

So COPY is both a standalone atomic act (at the protocol level) *and* a composable step (at the authoring level) — and these are not in tension, because they operate at different layers.

## Where the text is silent

NEED_RAW: 4/66–4/67 — if you want to confirm whether the prose immediately around the COPY/INSERT/REARRANGE command definitions says anything about ordering, dependency, or batching of commands, those two pages are the place to check; the curated extract gives the command definitions but not their surrounding discussion. Nelson's specification as captured above contains no transaction or atomic-grouping concept, so any claim that COPY *was* designed to participate in multi-command transactions would go beyond what the sources state.
