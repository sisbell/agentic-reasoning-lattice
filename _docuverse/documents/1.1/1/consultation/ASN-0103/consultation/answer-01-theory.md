## Question 1 [theory]

> What must a user be able to count on about a newly created document's identity remaining permanently distinct from every other document, including ones created later?

## What the user can count on

When you create a document, it receives a **permanent tumbler address** that is unique and will never be reused or collide with any other document — including documents created later. This guarantee rests on three properties of the tumbler addressing system.

**1. The address is permanent once assigned.**

> "New items may be continually inserted in tumbler-space while the other addresses remain valid. This means that any address of any document in an ever-growing network may be specified by a permanent tumbler address." [LM 4/19]

This is the core promise: later growth of the docuverse never invalidates or displaces an existing address.

**2. Distinctness is guaranteed by owned numbering ("baptism").**

New documents don't compete for a shared pool of names. Each is created by forking new digits *under* an address its owner already controls, so two creators can never independently mint the same address:

> "The basic principle is that of owned numbers. Numbers are owned by individuals or companies, and subnumbers under them are bestowed on other individuals and companies on whatever basis the owners choose. Whoever owns a specific node, account, document or version may in turn designate (respectively) new nodes, accounts, documents and versions, by forking their integers. We often call this the 'baptism' of new numbers." [LM 4/17]

> "The owner of a given item controls the allocation of the numbers under it." [LM 4/20]

Because allocation is delegated to owners within their own subtrees, no central authority is needed and no two documents can share an address — there is no mechanism by which a *later* document could be baptized onto an already-occupied position.

**3. The address itself is what makes documents distinct — not their content.**

Identity is structural, encoded in the four-field tumbler (`Node.0.User.0.Document.0.Element`):

> "There are four major fields, each expandable indefinitely, with three major dividers between them. These fields are Server, User, Document and Contents." [LM 4/26]

Two documents with byte-for-byte identical text still have different Document fields and therefore different identities; conversely, the same content shared by transclusion keeps the *original's* address. Distinct creation always means distinct address.

## The function this serves

Nelson frames the whole tumbler scheme as the management of permanent, collision-free naming in a system that grows without bound:

> "Tumbler addressing is concerned with the management of storage--the spontaneous creation of places to put things, and remembrance of where they are." [LM 4/16]

> "So the docuverse is all really one big forking document." [LM 4/18]

Because every document occupies its own branch of the single forking tree, a reference you make to a document today resolves to that same document forever — never to a later document, and never ambiguously to two documents at once. That permanence and distinctness is precisely what makes durable citation, surviving links, and stable transclusion possible.

(Note: distinct *identity/address* is permanent; Nelson treats continued *accessibility* of the content as a separate matter tied to ongoing storage payment, not to the address guarantee.)
