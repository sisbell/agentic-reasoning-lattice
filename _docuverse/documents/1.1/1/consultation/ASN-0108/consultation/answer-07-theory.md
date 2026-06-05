## Question 7 [theory]

> By what shared, durable identity does a reader mark its place between window requests, so that resuming continues exactly where it left off?

## Answer

The durable identity is the **permanent tumbler address** — specifically the immutable Istream (I-address). Nelson's protocol is stateless: there is no session token, no server-side cursor, no "reading session" that the back end remembers. A reader marks its place purely by recording a tumbler address, and resuming means re-issuing a request that names that same address.

### Why the tumbler address is the right "place-marker"

Tumbler addresses are designed to be permanent and never reassigned, which is exactly the property a bookmark needs:

> "New items may be continually inserted in tumbler-space while the other addresses remain valid. This means that any address of any document in an ever-growing network may be specified by a permanent tumbler address." (4/19)

> "Tumbler addressing is concerned with the management of storage--the spontaneous creation of places to put things, and remembrance of where they are." (4/16)

Because the address is the "common internal language throughout the search procedures of the system" (4/16), it is also *shared* — the same address means the same content from any access point, on any server, at any later time. That universality is what lets a place-mark recorded in one window request resolve identically in the next.

### The protocol is stateless — there is no session to resume

Nelson's FEBE commands carry no notion of an open reading session. As the curated `session-model.md` summary records:

> "Nelson's protocol is stateless at the command level: you name a document by its tumbler address, issue a command, and the back end responds."

So "resuming exactly where it left off" is not a server feature — it falls out of addressing. You re-name the tumbler and get the same bytes back.

### I-address vs. V-address matters here

The mark must be an **I-address**, not a V-address. Vstream positions shift under editing, so a place marked by V-position would drift:

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." (4/11)

The Istream address, by contrast, "never changes" and always returns that exact content — the stable handle a reader holds between requests.

### The one concrete "resume" example Nelson gives

The closest Nelson comes to a literal "pick up where I left off" mechanism is the mailbox, and it works by comparing against previously-seen material rather than any session state:

> "The user 'opens the mailbox' with a front-end request for items with a mail link more recent than the material already seen." (4/55)

Even here, the recoverable identity is the addressed/dated link — the front end remembers "what was already seen," the back end remains stateless.

### Summary

A reader marks its place by the **permanent tumbler / I-address** of the content. It is durable because addresses, once assigned, remain valid forever; it is shared because tumbler-space is one universal address space; and resumption needs no session because the protocol is stateless — naming the same address returns the same content.

A note on scope: Nelson does not name a dedicated "bookmark," "cursor," or session-resume primitive. The implementation-layer session/token machinery (e.g. Gregory's BERT) is *not* in Literary Machines; the answer above is built strictly from Nelson's permanent-addressing and stateless-protocol guarantees.
