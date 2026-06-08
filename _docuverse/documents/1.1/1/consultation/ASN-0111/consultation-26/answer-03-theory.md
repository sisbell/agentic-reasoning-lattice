## Question 3 [theory]

> Is recovering a link's owning home document from its address key intended to be a guaranteed part of the read interface, or merely an incidental consequence of the address layout?

## Answer: Intended and load-bearing — not merely incidental

Recovering a link's home document from its address is **intended** — the address layout was deliberately designed so that ownership is structurally recoverable, and Nelson's ownership model *depends* on this. But it is not exposed as a distinct read *operation*; it falls out of the tumbler field structure that a front end parses.

### Why it's intended, not incidental

**1. The address structurally encodes the home document.** A link's tumbler address *is* prefixed by its home document. Links live under their home document's address:

> "N.0.U.0.D.V.0.2.1 (the first link of the document, stored in the document's space)" (4/31)

> "The links designated by a tumbler address are in their permanent order of arrival. A document includes only the links of which it is the home document." (4/31)

The major dividers carry meaning here — they aren't arbitrary: the tumbler fields are Server, User, Document, Contents, and the zero-dividers have "lexical significance as punctuation" (4/28). So dropping a link's suffix yields its `N.0.U.0.D` home prefix by design.

**2. Nelson makes the home→owner mapping a semantic guarantee.** The ownership model is built *on* recoverability:

> "A link need not point anywhere in its home document. Its home document indicates who owns it, and not what it points to. Conversely, links connecting parts of a document need not reside in that document." (4/12)

> "A link's home (any home) is an element located on one side; and its three endsets map to the other sides." (4/46)

If you couldn't identify the home from the link's identity, this ownership semantics would be inoperable. That makes recovery load-bearing, not accidental.

**3. The read interface treats home as a first-class dimension.** `MAKELINK` returns the link's id (its tumbler address, which carries the home prefix), and `FINDLINKSFROMTOTHREE` takes a `home-set` as an explicit search parameter:

> "This returns a list of all links which are (1) in <home set>..." (operations, 4/69)

> "The document must be specified because that determines the actual residence of the link." (4/63)

### The qualification

There is **no dedicated FEBE operation** like "given a link address, return its home document." Recovery is a front-end parse of the tumbler's Node/User/Document fields, enabled by the deliberate address layout and made *meaningful* by the explicit ownership guarantee. So the precise framing is: the read interface guarantees that home/ownership is *determinable* (links are returned as addresses; home-set is queryable), while the act of extracting it from a given address key is structural parsing the design intends you to be able to do.

One boundary worth noting: Nelson elsewhere says "tumblers... only provide a mapping mechanism, and impose no categorization and no structure on the contents of a document" (4/17-4/18). That disclaimer is about *content/user-level* structure — it does not contradict field-level identification of node/user/document, which the dividers explicitly encode (4/28).
