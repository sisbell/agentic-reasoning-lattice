## Question 12 [theory]

> Did the design intend compound operations like create-document-with-initial-content or fork-with-population to be atomic from the docuverse's external semantics, or are the intermediate states between elementary steps conceptually observable to other agents in the system?

# Compound Operations and Observable Intermediate States

The curated sources and pages 4/61–4/63 give a clear answer: **Nelson did not design compound operation atomicity into the docuverse semantics.** The 17 FEBE commands are themselves the atomic units; compound user actions are *sequences* of those commands, with intermediate states conceptually observable.

## The Direct Evidence

Nelson explicitly addresses this on page 4/63:

> "FEBE is presented here in the form of a list of commands and what they do. Many of these commands may be considered 'subcommands' or 'subfunctions' used by complex front-end operations. For example, an insert command requires creating a link from the source to its new location and bringing the contents of that document up to date. This may be done by means of a sequence of FEBE commands." [LM 4/63]

And:

> "Note that all commands return some answer to the front end, even if only an acknowledgment that the procedure has been performed." [LM 4/63]

So compound semantics live at the **front end**, expressed as **sequences** of FEBE calls, each of which produces an observable acknowledgment. There is no transaction wrapper or commit boundary in the protocol.

## What This Means for the Two Examples

**Fork-with-population IS atomic — by being a single command.** Nelson chose to bundle it:

> "CREATENEWVERSION. This creates a new document with the contents of document <doc id>. It returns the id of the new document. The new document's id will indicate its ancestry." [LM 4/65–4/66, as quoted in operations.md]

This is the *only* compound operation Nelson made atomic at the protocol level. He apparently saw fork+populate as semantically inseparable.

**Create-document-with-initial-content is NOT atomic.** There is no such command. The flow is:

> "CREATENEWDOCUMENT. This creates an empty document. It returns the id of the new document." [LM 4/65, as quoted in operations.md]

…followed by INSERT or APPEND. The empty document exists, has a returned ID, and (per the system's stateless command model) is in principle visible to anyone who can address it.

## The Broader Gap

This is consistent with what Nelson explicitly leaves unspecified per `concepts/design-intent/session-model.md`:

- No OPEN/CLOSE operations on documents
- No locking protocol
- No session lifecycle
- No transaction boundaries beyond a single command

Each command is stateless, returns an acknowledgment, and leaves the system in a "canonical operating condition" — the BEBE language Nelson uses for server-to-server consistency:

> "A server's network model, from the full sweep up, is at all times unified and operational; whenever information moves between servers is incremental on its overall structure, leaving each server in canonical operating condition…" [LM 4/72]

So the unit of consistency is the individual command, not a user-meaningful compound flow.

## Implication

Intermediate states between elementary FEBE commands are conceptually observable in Nelson's design. The only compound flow he protected with atomicity was CREATENEWVERSION. Any other multi-step user action (create-then-populate, fork-then-edit, link-then-cross-reference) exposes intermediate states. Whether that matters in practice — concurrent readers, partial-failure recovery — is a session-layer concern Nelson left to implementors. (Gregory's BERT mechanism is one such implementation, but it is not in *Literary Machines*.)

NEED_RAW: 4/74–4/79 (BEBE forwarding behavior and what the 1987 implementation supports) if you want to know whether the back-end was thought to provide any cross-command consistency guarantee beyond single-command acknowledgment.
