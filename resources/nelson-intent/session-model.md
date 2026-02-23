# Session Model and Access Control

Source: Literary Machines, 2/41-2/48, 4/61-4/79, 5/6-5/18

## What It Means

Nelson does not specify a session model. The term "BERT" does not appear in Literary Machines. Nelson's protocol is stateless at the command level: you name a document by its tumbler address, issue a command, and the back end responds.

What Nelson DOES specify is the access framework around which any session model must be built:

1. **Ownership is structural** -- the User field of the tumbler address IS the owner (4/15-4/29)
2. **Access is binary** -- documents are private (owner and designees only) or published (everyone) (2/42)
3. **Modification requires ownership** -- only the owner may insert, delete, rearrange, or copy-into (2/29)
4. **Writing always succeeds** -- if you cannot modify the original, you create a version (2/45)
5. **Linking is unrestricted** -- anyone may link to any published content (2/42-2/43)
6. **Privacy is best-effort** -- the system may not monitor reading, but cannot guarantee privacy (2/59)

### Terminology Note

Gregory's BERT (Back-End Request Token) mechanism -- OPEN, CLOSE, READBERT, WRITEBERT, the lock table, denial-as-branching -- is the implementation of the session layer that Nelson left undesigned. It is consistent with Nelson's intent but is not specified by Nelson.

## User Guarantee

**What users can rely on (from Nelson):**
- You own what you create; ownership is permanent and encoded in the address
- You can always write -- if not to the original, then to your own version
- Published documents are readable by anyone without restriction
- Private documents are accessible only to owner and designees
- The system will not monitor what you read
- Anyone can link to published content; the author cannot prevent it

**What Nelson explicitly left unimplemented in XU.87.1:**
- Private documents (4/79: "Currently all documents are visible to all users")
- Accounting and royalty (4/79)
- Multiple-server methods (4/79)

## Principle Served

**Separation of concerns.** Nelson designs at the semantic level: who owns what, who may see what, what happens on denial. He leaves the concurrency mechanics (locking, session state, token management) to the implementor.

**Writing always succeeds.** This is the deepest principle relevant to session design. In conventional systems, access denial is an error. In Xanadu, denial is a fork. The user gets a version. This means the session model must never produce a permanent "permission denied" -- only a redirect to a fresh document.

**No surveillance.** The system must not track reading behavior, which constrains what the session model may record.

## What Nelson Does NOT Specify

1. **No OPEN/CLOSE operations** -- Nelson's 17 commands establish no session state on a document
2. **No read vs. write modes** -- Nelson's model is: you own it (modify freely) or you do not (create a version)
3. **No locking protocol** -- no mention of concurrent editing of the same document
4. **No session lifecycle** -- no connect/authenticate/disconnect sequence
5. **No access control lists** -- only owner/designees/everyone; no per-user grants
6. **No "BERT"** -- the term is entirely from Gregory's implementation

## Nelson's Words

On the access model:
> "A document may be private or published. [...] A private document may be read and linked-to only by the owner and his or her associates. A published document is available to anyone, and may be read and linked-to by anyone." (2/42)

On ownership:
> "Typically, the user will have no control over the node address he, she or it is assigned; but once assigned a User account, the user will have full control over its subdivision forevermore." (4/29)

On modification producing versions:
> "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate--without damaging the originals." (2/45)

On the connection model:
> "The planned Xanadu network has two types of connections: the connections of individual users to storage nodes, or servers; and the connections between and among servers." (4/74)

On what is not implemented:
> "Private documents. (Currently all documents are visible to all users.)" (4/79)

On concurrent users (future):
> "In later versions of the storage system, we expect the back end to combine the search models of different users to create a barrel-roll shared search model which repeatedly crosses the address space on behalf of all a server's users simultaneously." (4/59)

On privacy:
> "The network will not, may not monitor what is read or what is written in private documents." (2/59)

On passwords:
> "Each published document has a cash register. [...] It is in the user's system area, along with passwords and accounting information." (5/13)
