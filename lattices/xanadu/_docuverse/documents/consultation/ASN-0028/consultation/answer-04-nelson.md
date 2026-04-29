## Question 4 [nelson]

> What does it mean for a document to be "open" versus "closed" — is this a property of the document's editability, its visibility, or its relationship to the user?

## "Open" vs "Closed" Documents in Nelson's Design

**Nelson does not define "open" vs "closed" as a document state.** The FEBE protocol contains no OPEN or CLOSE operations. His 17 commands are stateless — you name a tumbler address, issue a command, the back end responds.

### What Nelson Actually Specifies: Private vs Published

Nelson's access model is binary:

> "A document may be private or published. [...] A private document may be read and linked-to only by the owner and his or her associates. A published document is available to anyone, and may be read and linked-to by anyone." [2/42]

From the session-model analysis: "No OPEN/CLOSE operations — Nelson's 17 commands establish no session state on a document. No read vs. write modes — Nelson's model is: you own it (modify freely) or you do not (create a version)."

### Where "Open" and "Closed" DO Appear

Nelson uses these terms **philosophically**, not as document properties:

**"Open hypertext"** — one of his one-liners for the system: "A pluralistic publishing and archiving medium with open hypertext and semi-closed framing" [3/2]. Here "open" means anyone can link to, quote from, and annotate published content. Connections flow freely.

**"Closed systems"** — Nelson's term of condemnation for systems that forbid external contribution:

> "Though interactive videodiscs have begun to proliferate, it is only as closed systems to which others may not add or make variations. This is unacceptable in the long term." [3/23]

A "closed" system is one where the creator controls all connections. In Xanadu, published documents are deliberately NOT closed — "each author of a published work is relinquishing the right to control links into that work" [2/43].

### The Implementation Layer

The OPEN/CLOSE/BERT (Back-End Request Token) mechanism comes from **Roger Gregory's implementation**, not from Nelson's design. As the session-model analysis notes: "Gregory's BERT mechanism — OPEN, CLOSE, READBERT, WRITEBERT, the lock table, denial-as-branching — is the implementation of the session layer that Nelson left undesigned."

### So What Is the Answer?

For Nelson, the relevant distinction is not editability or session state but **relationship to the docuverse**:

- **Published** = open to the world: anyone can read, link, quote, annotate. The author relinquishes control over incoming connections. Royalties flow automatically.
- **Private** = restricted: only owner and designees. Can still link outward to published content.
- **"Closed"** = Nelson's pejorative for systems that prevent external connection. The opposite of what Xanadu is for.

Editability is determined by **ownership**, not by any open/closed state: "Only the owner has a right to withdraw a document or change it" [2/29]. If you don't own it, you don't edit it — you create a version.

NEED_RAW: [4/61-4/65, 4/79] — to verify there is no document-state terminology in the protocol preamble or the "not yet implemented" list that might relate to open/closed semantics.
