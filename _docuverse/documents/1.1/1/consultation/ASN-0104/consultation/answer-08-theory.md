## Question 8 [theory]

> Can two distinct fragments ever share a single address, or must each piece of content carry an identity that is uniquely its own?

## Each fragment carries its own identity; distinct fragments never share an address

The short answer: **every piece of content carries a unique identity that is its own.** Two *distinct* fragments can never collide on a single address. But the same fragment appearing in many places is still *one* fragment with *one* address — that is transclusion, not collision.

### Identity is assigned at creation, by "baptism"

Every byte gets a permanent Istream address when it is created, allocated under the owner's account through forking:

> "The basic principle is that of owned numbers. Numbers are owned by individuals or companies, and subnumbers under them are bestowed on other individuals and companies on whatever basis the owners choose. Whoever owns a specific node, account, document or version may in turn designate (respectively) new nodes, accounts, documents and versions, by forking their integers. We often call this the 'baptism' of new numbers." (4/17)

Because addresses are forked rather than reused, no two creation events ever produce the same I-address. As the tumbler concept guarantees: "Every piece of content has a permanent, unique address."

### Identity is about origin, not value

This is the crux. Content identity in Xanadu is based on *where it was created*, not on what it says. Two documents that independently contain the identical word "the" hold **different** bytes at **different** I-addresses — they merely look alike. The curated provenance source states this directly:

> Two documents with identical text created independently have DIFFERENT I-addresses. Transcluded content SHARES the same I-address. (from the provenance concept, drawn from 4/10–4/11)

So sameness of *value* never forces sameness of *address*. Distinct fragments are distinct identities.

### The one case where an address is "shared": transclusion

When content appears in another document, it is not copied — it is included by reference. The same bytes (same single I-address) are pointed to from multiple Vstream locations:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." (4/11)

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." (4/11)

This is *not* two fragments sharing an address. It is one fragment (one identity, one home) appearing in many arrangements. The distinction Nelson draws is between the permanent **I-address** (identity, never duplicated) and the **V-address** (a position in a document's current arrangement, which is ephemeral and can repeat across documents):

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." (4/11)

### Why this matters

This is exactly what lets attribution be structural rather than strippable metadata. Because each fragment's identity is uniquely its own and traceable to a home document, "you always know where you are, and can at once ascertain the home document of any specific word or character" (2/40). If distinct fragments could share an address, origin would become ambiguous and the permanence, attribution, and royalty guarantees would all collapse.

**Conclusion:** Each piece of content must carry an identity uniquely its own — distinct fragments can never share an address. The only "sharing" in the system is one fragment, with one identity, being referenced (transcluded) into many places.
