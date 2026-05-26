## Question 1 [theory]

> In Nelson's design, are observational operations like SHOWDELETIONS conceived as queries issued only at stable, transaction-boundary states, or are they expected to be runnable at any observable point in system state?

# Observational Operations and Transaction Boundaries

Nelson's curated specification does not describe transactional boundaries for FEBE operations. The protocol is described as **stateless at the command level**: "you name a document by its tumbler address, issue a command, and the back end responds" (see `session-model.md`).

Key evidence from the curated sources:

**No session/transaction framework exists in Nelson's spec.** From the session model summary:
- "No OPEN/CLOSE operations — Nelson's 17 commands establish no session state on a document"
- "No read vs. write modes"
- "No locking protocol — no mention of concurrent editing of the same document"
- "No session lifecycle — no connect/authenticate/disconnect sequence"

**Each command is conceived as a standalone request/response.** Nelson frames the system definitionally through commands: "What the Xanadu storage and hypertext system does—and thus is—is defined by the commands to which it responds." (4/61) The retrieval/observational operations enumerated (RETRIEVEV, RETRIEVEDOCVSPAN, FINDLINKSFROMTOTHREE, SHOWRELATIONOF2VERSIONS, FINDDOCSCONTAINING, etc.) are described as immediate query→response, with no precondition that the document be at a "stable" or "boundary" state.

**The append-only Istream model removes the usual transaction concern.** Because Istream content is permanent and edits are non-destructive (Vstream re-arrangement), there is no "torn write" state to observe — content either exists at its I-address or it doesn't. Deleted bytes are explicitly described as a valid observable state: "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" (4/9, via `delete-semantics.md`).

**Implication for SHOWDELETIONS:** Consistent with the rest of the protocol, an observational operation over deleted-but-preserved content would be runnable at any point — there's no transaction boundary Nelson defines for it to wait on.

NEED_RAW: 4/61-4/79 — the operation `SHOWDELETIONS` is not explicitly enumerated in the curated FEBE operations list (which captures the documented subset of "17 current commands in XU.87.1"). If you want to verify whether Nelson lists SHOWDELETIONS by name and gives it any distinct state-precondition language, the FEBE protocol pages (raw pages 228–246) would need to be consulted directly.
