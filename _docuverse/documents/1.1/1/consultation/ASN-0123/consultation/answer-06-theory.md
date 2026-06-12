## Question 6 [theory]

> What does forking reveal about the boundary between a document's identity and its content that creating a fresh empty document cannot — namely, that identity can be new while content is entirely inherited?

## Identity and Content Are Independently Variable — and Forking Proves It at the Hard Case

Creating a fresh empty document and forking a document both mint a *new identity*. The protocol makes the parallel exact:

> "This creates an empty document. It returns the id of the new document." — CREATENEWDOCUMENT [LM 4/65]

> "This creates a new document with the contents of document <doc id>. It returns the id of the new document. The new document's id will indicate its ancestry." — CREATENEWVERSION [LM 4/66]

Both return a new id. The difference is everything: the empty document arrives with *no* content; the fork arrives with content that is *entirely* its source's. That difference is what exposes the boundary.

### What the empty document can teach, and where it stops

The empty document shows only the weak separation: that identity can exist *before* content — a container can be named while still vacant. But this leaves a tempting misreading intact. One could still suppose that a document's identity is just "a name plus whatever content accretes under it," and that an empty document is merely the degenerate starting point of that accretion — the name awaiting the content that will *become* its identity. On that reading, content and identity are still bundled; you begin from nothing and build your own.

The empty document cannot refute this, because it never presents identity and content *together* in a way that forces them apart. It separates them by subtraction — by removing the content entirely.

### What forking reveals that subtraction cannot

Forking separates them at the opposite extreme — at *maximal* content. A forked version begins life **full**, yet **none of that content is its own**. Its identity is brand new; its body is wholly inherited. So the question "does identity come from content?" is asked under the most demanding condition, and answered *no*: here is a document whose every byte was authored elsewhere, and it is nonetheless a distinct document with a distinct address.

And the demonstration is stronger still, because the inheritance is by **reference, not copy**. The new version does not receive duplicates; it transcludes the source's content — the very same Istream bytes:

> "The virtual byte stream of a document may include bytes from any other document." [LM 4/10]

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

> "Non-native bytes are as much a logical part of a document as native bytes." [LM 4/11]

This is the crux. If forking made a *copy*, the parent and child would have *different* content (two copies), and you could still claim that distinct identity merely tracked distinct content. But because forking *shares* the content, at the instant of the fork the parent and child are byte-for-byte the same. **Two identities, one body of content.** That is the conclusive proof that identity is not constituted by content — you cannot have arrived at two identities by way of two contents, because there is only one content.

### Why the architecture permits this: identity forks in V-space, content stays in I-space

The boundary the question asks about is the Istream/Vstream boundary made visible. Identity is a *Vstream* fact — a position in the forking tumbler tree:

> "So the docuverse is all really one big forking document." [LM 4/18]

> "One digit can become several by a forking or branching process. This consists of creating successive new digits to the right; we call these 'under' the previous digit." [LM 4/20]

Content is an *Istream* fact — bytes living at their home locations, "found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations" [LM 4/11]. The address says nothing about the content; it is "only a mapping mechanism," and imposes "no categorization and no structure on the contents of a document" [LM 4/17–4/18].

So forking is two independent acts that the empty document only ever performs as one:
1. **Mint identity** — bestow a new daughter address in the tree (the same baptismal act by which any document, empty or full, is born).
2. **Inherit content** — point that new Vstream at the source's entire Istream.

The empty document does step 1 and skips step 2. Forking does both — and by doing both *at once* shows they were never the same act.

### The deepest tell: derivation is *indicated*, not *constitutive*

There is a subtle confirmation in how I number versions. The id "will indicate its ancestry" [LM 4/66] — and yet:

> "In a sense the version, or subdocument number is only an accidental extension of the document number, and strictly implies no specific relationship of derivation." [LM 4/29]

Read those two together. The address *advertises* lineage as a courtesy, but structurally the version-number is just *another fork* — a new identity in the tree, no different in kind from any other daughter:

> "The Document field of the tumbler may be continually subdivided, with new subfields in the tumbler indicating daughter documents and versions." [LM 4/29]

The *derivation* — the fact that the content is inherited — does not live in the identity at all. It lives in the shared Istream. Identity records *that* a fork happened; content records *what was inherited*. They are kept in separate ledgers, and forking is the operation that writes to both at once, which is precisely why it lets you see that they are two ledgers.

### Consequences that fall out of this separation

Because the fork shares the source's Istream rather than copying it, three guarantees follow immediately — none of which an empty document can exhibit, since an empty document corresponds to nothing and inherits nothing:

- **Automatic correspondence.** Shared origin means the system can compute, with no extra bookkeeping, which parts of the two documents are the same — "a list of ordered pairs of the spans of the two spec-sets that correspond" [LM 4/70].
- **Version-spanning links.** A link made to the source reaches into the fork, because both ends rest on the same bytes.
- **No privileged original.** Since neither document's content is more "real" than the other's, there is "no 'basic' version of a document set apart from other versions... any more than one arrangement of the same materials is a priori better than other arrangements" [LM 2/19]. The parent is not the owner of the meaning; it is one arrangement among peers.

### In one sentence

The empty document shows identity can stand *without* content; forking shows identity can stand *apart from* content even when content is total and shared — and that is the stronger truth, because it locates the boundary not where content is absent, but exactly where two documents hold the very same bytes and remain, indelibly, two.
