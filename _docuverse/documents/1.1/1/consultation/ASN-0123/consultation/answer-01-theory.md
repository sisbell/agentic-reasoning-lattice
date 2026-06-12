## Question 1 [theory]

> When a new version is created from an existing document, what must be allocated as genuinely new — its identity, its ownership record, or both — and what must the design forbid from being duplicated at the moment of forking?

## What is genuinely new vs. what is inherited vs. what is forbidden

When a version is forked, exactly one thing is minted fresh — **its identity**. Ownership is **inherited, not re-allocated**, and the content (its Istream bytes and their I-addresses) is **forbidden from being duplicated**. So the answer to "identity, ownership record, or both?" is, for the ordinary case, **identity only** — and the design's hard prohibition is on copying the content.

Let me take the three pieces in turn.

### 1. Identity: genuinely new

`CREATENEWVERSION` allocates a fresh address. The new version is a new point on the tumbler line that did not exist before, and that address is constructed so as to record where it came from:

> "This creates a new document with the contents of document `<doc id>`. It returns the id of the new document. The new document's id will indicate its ancestry." [LM 4/66]

The mechanism is forking the Document field of the tumbler:

> "The Document field of the tumbler may be continually subdivided, with new subfields in the tumbler indicating daughter documents and versions." [LM 4/29]

Note the deliberate restraint in how much that address *asserts*:

> "In a sense the version, or subdocument number is only an accidental extension of the document number, and strictly implies no specific relationship of derivation." [LM 4/29]

The position is new; the *derivation* is recorded but the addressing arithmetic does not itself enforce a semantics of descent.

### 2. Ownership: inherited, never re-minted

There is no separate "ownership record" to create at forking, because ownership in my system is **structural** — it is the User field of the tumbler, sitting to the left of the Document field that gets subdivided. A version subdivides the Document number *underneath an unchanged User account*. The owner is the one doing the forking, by right of owning the number space:

> "Whoever owns a specific node, account, document or version may in turn designate (respectively) new nodes, accounts, documents and versions, by forking their integers. We often call this the 'baptism' of new numbers." [LM 4/17]

Creating a version is the owner *exercising* ownership, not transferring or duplicating it:

> "Only the owner has a right to withdraw a document or change it." [LM 2/29]

So: a new version does **not** require — and must not be given — a new owner.

### 3. What the design must forbid: duplicating the content

This is the cardinal prohibition. The version must **share** the parent's Istream content by reference; it must never copy it. `CREATENEWVERSION` produces "a new document *with the contents of*" the source [LM 4/66] — a new V-space arrangement laid over the **same** I-space bytes. The unchanged material keeps its original I-addresses; only genuinely *new* text written into the version earns new I-addresses (under the version's own number).

> "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate—without damaging the originals. This is done by inclusion links." [LM 2/45]

> "No copying operations are required among the documents throughout the system." [LM 2/36]

The prohibition is not aesthetic — three guarantees collapse the instant content is duplicated:

- **Correspondence.** Intercomparison is computed from shared I-addresses; two positions correspond *because* they are the same bytes. Duplicate the content and the system can no longer show you "word for word, what parts of two versions are the same" [LM 2/20]. This is the whole point of prismatic storage: "a given part… being prismatically refracted when we pass from one version to another" [LM 2/19] — refraction of *one* substance, not two copies.
- **Link survivability across versions.** "Links may be refractively followed from a point or span in one version to corresponding places in any other version. Thus a link to one version of a Prismatic Document is a link to all versions." [LM 2/26] That reach-through works *only* because the bytes are literally the same bytes. Copy them, and every link made to the parent is orphaned at the fork.
- **Honest attribution and royalty.** Bytes "remain in all other documents where they have been included" [LM 4/11]; tracing a byte to its home document is what lets royalty split "in proportion to who wrote what." Duplicated content forges that lineage.

### The symmetry, stated plainly

- **V-space (identity / arrangement):** allocate a **new** one for the version.
- **Ownership (the User field):** **inherit** it unchanged.
- **I-space (content):** **share** the existing addresses; duplication is forbidden.

### One nuance — when "both" becomes the right answer

The above is the canonical case: the owner forking *their own* document. There is a second case. When a *different* user makes an alternative version of a document they do **not** own, they cannot mint a number under your account, so the result is a new document under *their* account that windows your material:

> "Another user, however, is free to create his or her own alternative version of the document he or she does not own. This, then, becomes a windowing document using the shared materials by including them. We may call this versioning by inclusion." [LM 2/32–2/40, windowing discussion]

In *that* case, **both** identity and ownership are necessarily new — a new address under a new owner — yet the prohibition on duplicating content holds exactly as before: the shared material is *included*, never copied. So the rule generalizes cleanly: identity is always fresh; ownership is fresh only when the forker is a different party; content is never duplicated under any circumstance.

---

*Note on sourcing:* every quoted line above is drawn verbatim from the verified curated extracts, with one exception flagged inline — the "versioning by inclusion" passage is quoted from the windowing section of Chapter 2 but is not pinned to a single verified page in my extracts, so I have cited it to the section range [LM 2/32–2/40] rather than a precise page. If you want that one nailed to its exact page, NEED_RAW: 2/44–2/47.
